# =================================================================================================
# Contributing Authors:	    Michael Stacy, Name Here, Name Here
# Email Addresses:          jmst231@uky.edu, Email Here, Email Here
# Date:                     October 29th, 2023
# Purpose:                  Our GameInformation containing thread-safe game_codes
# Misc:                     
# =================================================================================================

# For our Threading Lock
from threading import Lock

import psutil, string, random

from .settings import LOWER_PORT, UPPER_PORT

# Type Hinting
from typing import List, Dict, Optional, Tuple
from multiprocessing import Process

class GameInformation:
    _lock = Lock()
    def __init__(self) -> None:
        # 'CodeHere': Port Number
        self.game_codes:Dict[str, int] = {}

        # Our List of Game Processes
        self.game_process:List[Process] = []

    def check_port(self, port:int) -> bool:
        '''Return True if Port is in Use'''
        for conn in psutil.net_connections(kind='inet'):
            assert conn.laddr, 'Connections should not be empty'
            if conn.laddr.port == port:
                return True
    
        return False

    def generate_code(self) -> Tuple[str, int]:
        '''Generate a Random Game Code'''
        # Grab the list of ascii characters and digits
        choice_list = string.ascii_letters+string.digits+'.'+'!'+'-'+';'

        # Generate a random port between acceptable range
        test_port = random.randint(LOWER_PORT, UPPER_PORT)

        # Populate a 255 Character Long Token
        new_code = ''.join(random.choice(choice_list) for _ in range(6))

        with self._lock:
            if self.game_codes[new_code]:
                return self.generate_code()
        
            # Check if the port is in usage
            while self.check_port(test_port):
                test_port = random.randint(LOWER_PORT, UPPER_PORT)

            self.game_codes[new_code] = test_port
        
        return new_code, test_port

    def check_code(self, code:str) -> Optional[int]:
        '''Check if a code exists'''
        with self._lock:
            if code in self.game_codes:
                return self.game_codes[code]
            
        return None
    
    def add_code(self, code:str, port:int) -> bool:
        '''Adds a Game Code to the List'''
        if self.check_code(code) is None:
            return False
        
        with self._lock:
            self.game_codes[code] = port

        return True
    
    def remove_code(self, code:str) -> None:
        '''Removes the Game Code'''
        if self.check_code(code) is None:
            return
        
        with self._lock:
            self.game_codes.pop(code)

