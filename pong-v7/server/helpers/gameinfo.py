# =================================================================================================
# Contributing Authors:	    Michael Stacy, Tag Howard, Juliann Hyatt
# Email Addresses:          jmst231@uky.edu, jtho264@uky.edu, jnhy222@uky.edu
# Date:                     October 29th, 2023
# Purpose:                  Our GameInformation containing thread-safe game_codes
# Misc:
# =================================================================================================

import random
import string
from multiprocessing import Process

# For our Threading Lock
from threading import Lock

# Type Hinting
from typing import Dict, List, Optional

# ServerSocket Gaming Process
from helpers.serversocket import ServerSocket

class GameInformation:
    _lock = Lock()

    def __init__(self) -> None:
        # 'CodeHere': Port Number
        self.game_codes: Dict[str, int] = {}

        # Our List of Game Processes
        self.game_process: List[Process] = []

    def generate_code(self, game_server:ServerSocket) -> str:
        """Generate a Random Game Code"""
        # Grab the list of ascii characters and digits
        choice_list = string.ascii_letters + string.digits + "." + "!" + "-" + ";"

        # Populate a 255 Character Long Token
        new_code = "".join(random.choice(choice_list) for _ in range(6))

        with self._lock:
            while self.game_codes.get(new_code):
                new_code = "".join(random.choice(choice_list) for _ in range(6))

            self.game_codes[new_code] = ServerSocket.port

        return new_code

    def check_code(self, code: str) -> Optional[int]:
        """Check if a code exists"""
        with self._lock:
            if code in self.game_codes:
                return self.game_codes[code]

        return None

    def add_code(self, code: str, port: int) -> bool:
        """Adds a Game Code to the List"""
        if self.check_code(code) is None:
            return False

        with self._lock:
            self.game_codes[code] = port

        return True

    def remove_code(self, code: str) -> None:
        """Removes the Game Code"""
        if self.check_code(code) is None:
            return

        with self._lock:
            self.game_codes.pop(code)
