# =================================================================================================
# Contributing Authors:	    Michael Stacy, Tag Howard, Juliann Hyatt
# Email Addresses:          jmst231@uky.edu, jtho264@uky.edu, jnhy222@uky.edu
# Date:                     October 29th, 2023
# Purpose:                  Creates our Client Thread to Manage Request from Client
# Misc:                     A part of the Lobby Server
# =================================================================================================

# Used in Game Processing
import multiprocessing as mp

# For Type Hinting
from multiprocessing.synchronize import Event

# Our Client Socket and Server Management
from helpers.clientwrapper import ClientWrapper

# Our database connection
from helpers.database import Database

# Game Information
from helpers.gameinfo import GameInformation

# Used to create our Game Server
from helpers.serversocket import ServerSocket

# Game Server
from .game import GameServer


class Client:
    def __init__(
        self, connection: ClientWrapper, shut_down: Event, game_info: GameInformation
    ) -> None:
        """Creates the Client Thread to handle requests from the Client"""
        # Our connection and Event
        self.connection = connection
        self.shut_down = shut_down

        # Create the thread's database connection
        self.database = Database()

        # Is the client authenticated?
        self.authenticated = False
        self.username: str = ""
        self.wins: int = 0

        # Game information holder
        self.game_info = game_info

        # Accessible Functions
        self.access_functions = {
            "create_game": self.create_game,
            "join_game": self.join_game,
        }

        self.run_thread()

    def grab_wins(self) -> None:
        success, error_message, wins = self.database.grab_wins(self.username)
        if not success:
            print("Failure to grab wins: ", error_message)
            return

        if wins is not None:
            self.wins = wins

    def try_login(self, request: dict) -> None:
        """Returns True if Login Successful"""
        if "username" not in request or "password" not in request:
            self.connection.send(
                {
                    "request": "login",
                    "return": False,
                    "error": "Missing username or password",
                }
            )

        success, error_message = self.database.validate_user(
            request["username"], request["password"]
        )
        if not success:
            self.connection.send(
                {"request": "login", "return": False, "error": error_message}
            )

        # We succeeded! Grab wins, set username, set authenticated
        self.username = request["username"]
        self.grab_wins()
        self.authenticated = True

        self.connection.send({"request": "login", "return": True, "message": "Success"})

    def create_account(self, request: dict) -> None:
        """Attempts to create account"""
        if (
            "username" not in request
            or "password" not in request
            or "initials" not in request
        ):
            self.connection.send(
                {"request": "login", "return": False, "error": "Missing Information"}
            )

        success = self.database.create_user(
            request["username"], request["password"], request["initials"]
        )
        if not success:
            self.connection.send(
                {
                    "request": "login",
                    "return": False,
                    "error": "Failed to create account",
                }
            )

        # We succeeded!
        self.username = request["username"]
        self.wins = 0
        self.authenticated = True

        self.connection.send({"request": "login", "return": True, "message": "Success"})

    def create_game(self, request: dict) -> None:
        """Attempts to create a new game instance"""

        # Generate new code, return it to the Client
        new_code = self.game_info.generate_code()

        # A pipe to send the port back to the main process from the game process
        send_port, recv_port = mp.Pipe()

        # Generate a new game process
        new_game = mp.Process(
            target=GameServer,
            args=(new_code, self.shut_down, send_port),
        )
        with self.game_info._lock:
            self.game_info.game_process.append(new_game)

        new_game.start()

        # Grab the port from the game process
        game_server_port = recv_port.recv()

        self.game_info.add_code(new_code, game_server_port)

        self.connection.send(
            {"request": "create_game", "return": True, "message": game_server_port}
        )

    def join_game(self, request: dict) -> None:
        """Informs Client to Start Game if Exists"""
        # Check if Code exists
        if "code" not in request:
            self.connection.send(
                {"request": "join_game", "return": False, "error": "Missing Code"}
            )
            return

        # Check if code is in game_codes
        new_port = self.game_info.check_code(request["code"])
        if new_port is None:
            print("Invalid Game Code")
            self.connection.send(
                {"request": "join_game", "return": False, "error": "Invalid Game Code"}
            )
            return

        # Success, send the message
        print("Valid Game Code")
        self.connection.send(
            {"request": "join_game", "return": True, "message": new_port}
        )

    def run_thread(self) -> None:
        """Our main function for the Client Thread"""
        while not self.shut_down.is_set():
            # Grab our next message
            request = self.connection.recv()

            # Check if the new_message happened, if not check if the connection is open
            if not request:
                if not self.connection.connection_open:
                    print("Client Thread Closing")
                    return

                print("Client Timed Out")
                continue

            print("Message Receieved")

            if request["request"] == "login":
                self.try_login(request)
                continue
            elif request["request"] == "create_account":
                self.create_account(request)
                continue

            # Authenticated Required
            if not self.authenticated:
                self.connection.send(
                    {
                        "request": request["request"],
                        "return": False,
                        "error": "Not Authorized",
                    }
                )
                continue
            else:
                self.access_functions[request["request"]](request)
