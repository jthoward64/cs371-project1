# =================================================================================================
# Contributing Authors:	    Michael Stacy, Tag Howard, Juliann Hyatt
# Email Addresses:          jmst231@uky.edu, jtho264@uky.edu, jnhy222@uky.edu
# Date:                     October 29th, 2023
# Purpose:                  Creates our Server to accept incoming Clients
# Misc:
# =================================================================================================

# Used in Client Threads and Game Processing
import threading as th
from multiprocessing.connection import Connection

# For Type Hinting
from multiprocessing.synchronize import Event

# Typing Requisites
from typing import List

# Our Client Socket and Server Management
from helpers.clientwrapper import ClientWrapper

# Our database connection
from helpers.database import Database as db
from helpers.serversocket import ServerSocket

# Our game information
from .playinfo import GameInfo

class GameServer:
    # new_game = mp.Process(target=GameServer, args=(new_code, new_port, self.shut_down, self.game_info))
    def __init__(self, new_code: str, shut_down: Event, port_pipe: Connection) -> None:
        """Creates the Lobby Server"""
        self.game_server = ServerSocket(0)

        self.code = new_code

        # Ensure our connection is established
        if not self.game_server.connection_open:
            print("Failed to create Lobby Server")
            return

        port_pipe.send(self.game_server.port)

        # Game Information
        self.game_info = GameInfo()

        # Game Server shutdown
        self.game_down: th.Event = th.Event()

        # Main Server shut_down information
        self.shut_down: Event = shut_down

        # Our list of Client Threads
        self.thread_list: List[th.Thread] = []

        while not self.shut_down.is_set():
            # Accept an incoming Client
            new_client = self.game_server.accept()

            # Ensure no error ocurred and that the new_client exists
            if not new_client:
                continue

            # Create a new wrapper
            new_wrap = ClientWrapper(new_client)

            # Ensure the newly created wrapper is open, that no errors ocurred
            if not new_wrap.connection_open:
                continue

            print("Client Connected")

            # Create a thread for the client to interact with
            new_thread = th.Thread(target=self.client, args=(new_wrap,))

            # Add to the list
            self.thread_list.append(new_thread)

            # Start the thread
            new_thread.start()

        for thread in self.thread_list:
            thread.join()

    def client(self, control: ClientWrapper) -> None:
        """Handles the Client Connections"""
        # Game Information
        username: str = ""
        player: str = ""
        initials: str = ""

        # Database Connection
        database = db()

        # Do we need to turn this client thread off?
        shut_client = False

        while (not self.shut_down.is_set() and not self.game_down.is_set() and not shut_client):
            # Grab incoming client connection
            success = control.recv()

            # Did our success fail and is the connection closed?
            if success is None:
                if self.game_info.player_check(username):
                    self.game_down.set()
                continue

            new_message = success

            # Requesting to join the 
            print(new_message)
            if new_message["request"] == "join_game":
                # Check if username is valid, else exit this client
                validated, message = database.validate_user(new_message["username"], new_message["password"])
                if not validated:
                    control.send({"request": "join_game", "return": False, "message": message})
                    shut_client = True
                    control.close()
                    continue

                # Update our username
                username = new_message['username']
                initials = new_message['initials']

                # Inform Client of Success, add to Player List
                player_type = self.game_info.set_player(username, initials)

                if player_type == 'spectate':
                    player = 'spectate'
                else:
                    player = 'left' if player_type == 'left_player' else 'right'
                
                control.send({"request": "join_game", "return": True, "message": player_type})
                continue

            # # # Block Non-Validated Clients # # #
            if username == "" or player == "":
                continue

            if new_message["request"] == "game_info":
                # Return Message
                message = {}
                message['left_player'], message['right_player'] = self.game_info.grab_players()
                message['game_code'] = self.code
            
                control.send({"request": "game_info", "return": True, "message": message})
                continue

            # Requesting to Start the Game
            if new_message["request"] == "start_game":
                # Return Message
                message = {}
                message['left_player'], message['right_player'] = self.game_info.grab_players()
                message['game_code'] = self.code

                # Are clients ready to start?
                start: bool = self.game_info.start_game(player)

                control.send({"request": "ready", "return": start, "message": message})
                continue

            # Checking if the player can start the game
            if new_message["request"] == "grab_game":
                if not self.game_info.continue_game():
                    # Inform the client the round is over
                    control.send({"request": "grab_game", "return": False, "message": None})
                    continue

                # Prepare information
                game_info: dict = self.game_info.grab_game()

                # Send it
                control.send({"request": "grab_game", "return": True, "message": game_info})
                continue

            if new_message["request"] == "update_game" and player != "spectate":
                if not self.game_info.continue_game():
                    control.send({"request": "update_game", "return": False, "message": None})
                    continue

                self.game_info.update_game(player, new_message['message'])

                if new_message['message']['lScore'] > 4:
                    self.game_info.increment_win('left')
                    self.game_info.reset_game()
                elif new_message['message']['rScore'] > 4:
                    self.game_info.increment_win('right')
                    self.game_info.reset_game()

                control.send({"request": "update_game", "return": True, "message": None})
                continue
