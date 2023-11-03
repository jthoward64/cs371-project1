# =================================================================================================
# Contributing Authors:	    Michael Stacy, Name Here, Name Here
# Email Addresses:          jmst231@uky.edu, Email Here, Email Here
# Date:                     October 29th, 2023
# Purpose:                  Our GameInformation containing thread-safe game_codes
# Misc:                     
# =================================================================================================

# For our Threading Lock
from threading import Lock

# Type Hinting
from typing import Any, List, Dict, Optional
from multiprocessing import Process

class GameInformation:
    _lock = Lock()
    def __init__(self) -> None:
        # 'CodeHere': Port Number
        self.game_codes:Dict[str, int] = {}

        # Our List of Game Processes
        self.game_process:List[Process] = []

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