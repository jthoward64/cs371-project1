# =================================================================================================
# Contributing Authors:	    Michael Stacy, Name Here, Name Here
# Email Addresses:          jmst231@uky.edu, Email Here, Email Here
# Date:                     October 29th, 2023
# Purpose:                  Implements the Game Server to allow incoming connections
# Misc:                     
# =================================================================================================

# For Database Handling
from typing import List
from .database import Database as db

# Import our Server creation
from .sockethelper import Connection, SSLSocket, Client, EncodeMessage, DecodeMessage

# Multithreading and Multiprocessing Needed
import threading as th
from multiprocessing.synchronize import Event

# For database management
from .database import Database as db

class Paddle:
    Lock:th.Lock = th.Lock()
    def __init__(self) -> None: 
        '''Contains the Paddle Information X, Y, Moving'''
        self.X:int = 0
        self.Y:int = 0
        self.Moving:str = ''

class Ball:
    Lock:th.Lock = th.Lock()
    def __init__(self) -> None:
        '''Contains the Ball Information X, Y'''
        self.X:int = 0
        self.Y:int = 0
        
class Score:
    Lock:th.Lock = th.Lock()
    def __init__(self) -> None:
        '''Contains the Score Information left_score and right_score'''
        self.left_score:int = 0
        self.right_score:int = 0

class Information:
    Lock:th.Lock = th.Lock()
    def __init__(self) -> None: 
        '''Contains the left_player, right_player, left_initial, right_initial, sync'''
        # Our player usernames
        self.left_player:str = ''
        self.right_player:str = ''

        # Initials for Game Play
        self.left_initial:str = ''
        self.right_initial:str = ''

        # Number of Clients
        self.client_number:int = 0
        
        # Sync of the Clients
        self.sync:int = 0

class Game:
    def __init__(self, port:int, code:str, shut_down:Event) -> None:
        
        # Game Information
        self.information = Information()

        # Paddles
        self.left_paddle = Paddle()
        self.right_paddle = Paddle()

        # Ball information
        self.ball = Ball()

        # Score of the current game
        self.score = Score()

        # Clients Ready to Start
        self.left_play:th.Event = th.Event()
        self.right_play:th.Event = th.Event()

        # Main Server shut_down information
        self.shut_down:Event = shut_down

        # Game Server shutdown
        self.game_down:th.Event = th.Event()

        # Inform clients round is over
        self.round_over:th.Event = th.Event()

        # The game code to join
        self.code = code

        # Create our Server
        # DO NOT ALLOW CLIENTS ACCESS (No Self)
        new_server = Connection(port)

        # List of Client Threads
        client_threads:List[th.Thread] = []

        # Begin accepting new connections
        while not shut_down.is_set() and not self.game_down.is_set():

            # Accept a new connection
            success = new_server.accept()

            if not success:
                continue
            
            # Create a new thread
            new_thread = th.Thread(target=self.client, args=(success,))
            new_thread.start()

            client_threads.append(new_thread)
            self.information.client_number +=  1

        # Game Shutting down
        new_server.close()
        for thread in client_threads:
            thread.join()

    def client(self, connection:SSLSocket):
        '''Handles the Client Connections'''
        # Game Information
        username:str = ''
        player:str = ''

        # Database Connection
        database = db()

        # The socket connection
        control = Client(connection)

        # Do we need to turn this client thread off?
        shut_client = False

        while not self.shut_down.is_set() and not self.game_down.is_set() and not shut_client:
            # Grab incoming client connection
            success = control.recv()

            # Did our success fail and is the connection closed?
            if not success:
                with self.information.Lock:
                    if username != '' and (username == self.information.left_player or username == self.information.right_player):
                        # A player has exited, quit the game
                        self.game_down.set()
                continue
            
            new_message = success.message
            
            # It's impossible for new_message to be anything but a dict as we only return dict
            # when success is true.
            assert isinstance(new_message, dict), f'Expected dict, got {type(new_message)}'

            # Requesting to join the game
            if new_message['request'] == 'join_game':
                # Check if username is valid, else exit this client
                validated, message = database.validate_user(new_message['username'], new_message['password'])
                if not validated:
                    control.send(EncodeMessage({'request': 'join_game', 'return':False, 'message': message}))
                    shut_client = True
                    control.close()
                    continue
                
                # Update our username
                username = new_message['username']
                
                # Inform Client of Success, add to Player List
                with self.information.Lock:
                    if self.information.left_player == '':
                        self.information.left_player = username
                        player = 'left_player'
                    elif self.information.right_player == '':
                        self.information.right_player = username
                        player = 'right_player'
                    else:
                        player = 'spectate'
                    
                control.send(EncodeMessage({'request': 'join_game', 'return':True, 'message':player}))
                continue

            # # # Block Non-Validated Clients # # #
            if username == '' or player == '':
                continue

            if new_message['request'] == 'game_info':
                # Return Message
                with self.information.Lock:
                    message = {
                        'left_player':self.information.left_initial,
                        'right_player':self.information.right_initial,
                        'client_number':self.information.client_number,
                        'game_code':self.code
                    }

                control.send(EncodeMessage({'request': 'game_info', 'return':True, 'message':message}))
                continue
            
            # Requesting to Start the Game
            if new_message['request'] == 'start_game':
                if player == 'left_player':
                    self.left_play.set()
                elif player == 'right_player':
                    self.right_play.set()

                # Return Message
                with self.information.Lock:
                    message = {
                        'left_player':self.information.left_initial,
                        'right_player':self.information.right_initial,
                        'client_number':self.information.client_number,
                        'game_code':self.code
                    }

                # Are clients ready to start?
                start:bool = True if self.left_play.is_set() and self.right_play.is_set() and not self.round_over.is_set() else False
                control.send(EncodeMessage({'request': 'ready', 'return':start, 'message':message}))
                continue

            # Checking if the player can start the game
            if new_message['request'] == 'grab_game':
            
                if self.round_over.is_set():
                    # Inform the client the round is over
                    control.send(EncodeMessage({'request': 'grab_game', 'return':False, 'message':None}))
                    continue
                
                # Prepare information
                game_info:dict = {}
                with self.left_paddle.Lock:
                    game_info['left_player'] = {
                        'X':self.left_paddle.X,
                        'Y':self.left_paddle.Y,
                        'Moving':self.left_paddle.Moving
                    }
                with self.right_paddle.Lock:
                    game_info['right_player'] = {
                        'X':self.right_paddle.X,
                        'Y':self.right_paddle.Y,
                        'Moving':self.right_paddle.Moving
                    }
                with self.score.Lock:
                    game_info['score'] = {
                        'lScore':self.score.left_score,
                        'rScore':self.score.right_score,
                    }
                with self.information.Lock:
                    game_info['sync'] = self.information.sync

                # Send it
                control.send(EncodeMessage({'request': 'grab_game', 'return':True, 'message':game_info}))
                continue

            if new_message['request'] == 'update_game' and player != 'spectate':

                if self.round_over.is_set():
                    control.send(EncodeMessage({'request': 'update_game', 'return':False, 'message':None}))
                    continue
                
                # Check if we need to update the game information
                with self.information.Lock:
                    if new_message['message']['sync'] > self.information.sync:
                        # Update Sync
                        self.information.sync = new_message['message']['sync']

                        # Update Score
                        with self.score.Lock:
                            self.score.left_score = new_message['message']['score']['lScore']
                            self.score.right_score = new_message['message']['score']['rScore']
                            if self.score.left_score > 4 or self.score.right_score > 4 and not self.round_over.is_set():
                                self.round_over.set()

                                # Winner
                                with self.information.Lock:
                                    winner:str = self.information.left_player if self.score.left_score > 4 else self.information.right_player

                                # Award Points
                                database.increment_win(winner)

                        # Update Ball
                        with self.ball.Lock:
                            self.ball.X = new_message['message']['ball']['X']
                            self.ball.Y = new_message['message']['ball']['Y']

                if player == 'left_player':
                    # Update Left
                    with self.left_paddle.Lock:
                        self.left_paddle.X = new_message['message']['Paddle']['X']
                        self.left_paddle.X = new_message['message']['Paddle']['Y']
                        self.left_paddle.Moving = new_message['message']['Paddle']['Moving']
                else:
                    # Update Right
                    with self.right_paddle.Lock:
                        self.right_paddle.X = new_message['message']['Paddle']['X']
                        self.right_paddle.X = new_message['message']['Paddle']['Y']
                        self.right_paddle.Moving = new_message['message']['Paddle']['Moving']

                control.send(EncodeMessage({'request': 'update_game', 'return':True, 'message':None}))
                continue

        # Client Exiting
        self.information.client_number -=  1