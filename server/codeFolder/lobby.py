# =================================================================================================
# Contributing Authors:	    Michael Stacy, Tag Howard, Juliann Hyatt
# Email Addresses:          jmst231@uky.edu, jtho264@uky.edu, jnhy222@uky.edu
# Date:                     October 29th, 2023
# Purpose:                  Creates our Server to accept incoming Clients
# Misc:
# =================================================================================================

import json
import multiprocessing as mp

# Our Signal to shut down the server gracefully
import signal

# Used in Client Threads and Game Processing
import threading as th

# For Type Hinting
from multiprocessing.synchronize import Event
from types import FrameType
from typing import List, Optional

# Our Client Socket and Server Management
from helpers.clientwrapper import ClientWrapper

# Our game information
from helpers.gameinfo import GameInformation
from helpers.serversocket import ServerSocket

# Our Address Family and Socket Type
from helpers.settings import MAIN_PORT

# Our Client Handler
from .client import Client


class LobbyServer:
    # Author:        Michael Stacy
    # Purpose:       To run the Lobby Server Thread to allow clients to connect to games
    # Pre:           None
    # Post:          None
    def __init__(self) -> None:
        """Creates the Lobby Server"""
        self.lobby = ServerSocket(MAIN_PORT)

        # Ensure our connection is established
        if not self.lobby.connection_open:
            print("Failed to create Lobby Server")
            return

        # Add signals for gracefully shutting down
        signal.signal(signal.SIGINT, self.signal_shutdown)
        signal.signal(signal.SIGTERM, self.signal_shutdown)

        self.lobby

        # Grab our Game Information
        self.game_info = GameInformation()

        # Our list of Client Threads
        self.thread_list: List[th.Thread] = []

        # For shutting down entire server
        self.shut_down:Event = mp.Event()

        while not self.shut_down.is_set():
            # Accept an incoming Client
            new_client = self.lobby.accept()

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
            new_thread = th.Thread(target=Client, args=(new_wrap, self.shut_down, self.game_info))

            # Add to the list
            self.thread_list.append(new_thread)

            # Start the thread
            new_thread.start()

        # Wait for all threads to finish
        for thread in self.thread_list:
            thread.join()
        for process in self.game_info.game_process:
            process.join()

    # Author:        Michael Stacy
    # Purpose:       To shut down the server when SIGTERM and SIGKILL are done
    # Pre:           Optional Signal/Frame
    # Post:          None
    def signal_shutdown(self, signal: int, frame: Optional[FrameType]) -> None:
        """Handles the signal for shutting down"""
        self.shut_down.set()