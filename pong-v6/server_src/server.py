# =================================================================================================
# Contributing Authors:	    Michael Stacy, Name Here, Name Here
# Email Addresses:          jmst231@uky.edu, Email Here, Email Here
# Date:                     October 29th, 2023
# Purpose:                  Our Main Server that spawns new Game Instances and validates incoming Clients
# Misc:                     
# =================================================================================================

# SSLSocket
from ssl import SSLSocket

# For Typing
from types import FrameType
from typing import List, Dict, Optional

# String and Random Manipulation for Code Generation
import string, random

# For Signals
import signal

# Our Game Object Manager
from code.game import Game

# How we control the database
from code.database import Database as db

# We need Multiprocessing and Threading
import multiprocessing as mp
import threading as th

# Server and Port Information
from code.sockethelper import Connection, EncodeMessage, DecodeMessage, Client
from code.settings import MAIN_PORT, LOWER_PORT, UPPER_PORT, ERROR_LIST

# To see which ports are in use
import psutil

def check_port(port:int) -> bool:
    '''Return True if Port is in Use'''
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port:
            return True
    
    return False

class Lobby:
    def __init__(self):
        
        # Our method to shut the entire thing down
        self.shut_down = mp.Event()

        # Gracefully shutdown
        signal.signal(signal.SIGINT, self.signal_hanlder)
        signal.signal(signal.SIGTERM, self.signal_hanlder)

        # Our main server to accept clients
        new_server = Connection(MAIN_PORT)

        # Our game threads
        self.game_servers:List[th.Thread] = []

        # Game Codes for Clients to Enter
        self.game_code_lock:th.Lock = th.Lock()
        self.game_codes:Dict[str, int] = {}

        # Holds our list of client threads
        thread_list:List[th.Thread] = []

        while not self.shut_down.is_set():
            
            # Grab incoming client
            success = new_server.accept()

            if not success:
                continue

            # Create a new client thread
            new_thread = th.Thread(target=self.client_handler, args=(success,))
            new_thread.start()

        # Wait for all clients to finish
        for thread in thread_list:
            thread.join()
        for thread in self.game_servers:
            thread.join()

    def signal_hanlder(self, signal_name:int, frame:Optional[FrameType]) -> None:
        self.shut_down.set()

    def generate_code(self) -> str:
        '''Generate a Random Game Code'''
        # Grab the list of ascii characters and digits
        choice_list = string.ascii_letters+string.digits+'.'+'!'+'-'+';'

        # Populate a 255 Character Long Token
        new_code = ''.join(random.choice(choice_list) for _ in range(6))

        if self.game_codes[new_code]:
            return self.generate_code()
        
        return new_code
    
    def generate_port(self) -> int:
        # Generate a random port between acceptable range
        test_port = random.randint(LOWER_PORT, UPPER_PORT)
        
        # Check if the port is in usage
        while check_port(test_port):
            test_port = random.randint(LOWER_PORT, UPPER_PORT)
        
        return test_port

    def client_handler(self, socket:SSLSocket) -> None:
        # Is the client validated?
        logged_in = False

        # Our connection
        connection = Client(socket)

        # Do we need to close the client?
        close_client = False

        # Our Database Access
        database = db()

        while not self.shut_down.is_set() and not close_client:

            success = connection.recv()

            # Close client if we can't establish connection
            if not success:
                close_client = True
                continue

            new_message = success.message

            # It's impossible for new_message to be anything but a dict as we only return dict
            # when success is true.
            assert isinstance(new_message, dict), f'Expected dict, got {type(new_message)}'
            
            # Requesting to Login
            if new_message['request'] == 'login':
                validated, message = database.validate_user(new_message['username'], new_message['password'])
                if validated:
                    logged_in = True
                    connection.send(EncodeMessage({'request':'login', 'return':True, 'message':'Incorrect Login'}))
                    continue

                connection.send(EncodeMessage({'request':'login', 'return':False, 'message':'Success'}))
                continue
            
            # Prevent accessing games
            if not logged_in:
                continue

            if new_message['request'] == 'create_game':

                # Create a new game
                new_code = self.generate_code()
                new_port = self.generate_port()

                # Create our new game handler thread
                new_game = th.Thread(target=self.game_handler, args=(new_code, new_port))
                new_game.start()

                # Add to our list
                self.game_codes[new_code] = new_port

                # Add thread to our list of servers
                self.game_servers.append(new_game)

                # Inform the client to move to the new game server
                connection.send(EncodeMessage({'request':'create_game', 'return':True, 'message':new_port}))
                continue

            if new_message['request'] == 'join_game':

                with self.game_code_lock:
                    # Check if the code exists
                    if self.game_codes[new_message['code']]:
                        # Inform the client to move to that game server
                        connection.send(EncodeMessage({'request':'join_game', 'return':True, 'message':self.game_codes[new_message['code']]}))
                        continue
                
                # Failed, code doesn't exist
                connection.send(EncodeMessage({'request':'join_game', 'return':False, 'message':'Game does not exist'}))
                continue

        connection.close()

    def game_handler(self, new_code:str, new_port:int) -> None:
        # Create a Game Process
        # self, port:int, code:str, shut_down:Event,
        new_game = mp.Process(target=Game, args=(new_port, new_code, self.shut_down))
        new_game.start()

        # Await for Game to close
        new_game.join()

        # Remove from the list of game_codes
        with self.game_code_lock:
            self.game_codes.pop(new_code)


if __name__ == '__main__':
    new_lobby = Lobby()