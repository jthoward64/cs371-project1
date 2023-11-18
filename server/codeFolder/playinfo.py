# =================================================================================================
# Contributing Authors:	    Michael Stacy, Tag Howard, Juliann Hyatt
# Email Addresses:          jmst231@uky.edu, jtho264@uky.edu, jnhy222@uky.edu
# Date:                     
# Purpose:                  
# Misc:
# =================================================================================================
import random
import threading as th
from typing import Literal, Optional, Tuple, TypedDict

from helpers.database import Database as db


class BallInfo(TypedDict):
    x: int
    y: int
    xVel: int
    yVel: int


class SharedGameInfo(TypedDict):
    ball: BallInfo
    sync: int


class PaddleInfo(TypedDict):
    x: int
    y: int
    moving: Literal["up", "down", ""]


class PlayerData(TypedDict):
    paddle: PaddleInfo
    score: int
    wins: int


class SendScore(TypedDict):
    lScore: int
    rScore: int


class SendWins(TypedDict):
    left_player: int
    right_player: int


class SendGameInfo(TypedDict):
    left_paddle: PaddleInfo
    right_paddle: PaddleInfo
    ball: BallInfo
    score: SendScore
    sync: int


default_shared_data: SharedGameInfo = {
    "ball": {
        "x": 0,
        "y": 0,
        "xVel": 0,
        "yVel": 0,
    },
    "sync": 0,
}

default_paddle: PaddleInfo = {
    "x": 0,
    "y": 0,
    "moving": "",
}

default_player_data: PlayerData = {
    "paddle": default_paddle,
    "score": 0,
    "wins": 0,
}


class GameInfo:
    # Author:        Michael Stacy
    # Purpose:       To create our game server data model
    # Pre:           None
    # Post:          None
    def __init__(self) -> None:
        self.game_data: None = None

        # Lock for basic game data
        self.shared_lock = th.Lock()
        self.shared_data: SharedGameInfo = default_shared_data
        self.starting_direction: Literal["left", "right"]

        # Lock for the player's data
        self.left_lock = th.Lock()

        self.left_data: PlayerData = default_player_data
        self.right_lock = th.Lock()
        self.right_data: PlayerData = default_player_data

        self.database = db()

        self.reset_game()

        # Is the game running
        self.game_running = False

        # Are the clients ready?
        self.ready = {
            "left": False,
            "right": False,
        }

        # Username of the Players
        self.user = {"left": "", "right": ""}

        # Initials of the Players
        self.initials = {"left": "", "right": ""}

    # Author:        Michael Stacy
    # Purpose:       To send game information to the client
    # Pre:           None
    # Post:          Sends off the Game Information via a Socket Connection API
    def grab_game(self) -> SendGameInfo:
        """Returns the current game data"""
        with self.shared_lock and self.left_lock and self.right_lock:
            new_info: SendGameInfo = {
                "left_paddle": self.left_data["paddle"],
                "right_paddle": self.right_data["paddle"],
                "ball": self.shared_data["ball"],
                "score": {
                    "lScore": self.left_data["score"],
                    "rScore": self.right_data["score"],
                },
                "sync": self.shared_data["sync"],
            }

            return new_info
        
    # Author:        Michael Stacy
    # Purpose:       To update the server from the client
    # Pre:           Player String, Data Dictionary
    # Post:          None
    def update_game(self, player: str, data: dict) -> None:
        """Updates the game data"""
        with self.shared_lock:
            self.shared_data["sync"] = data["sync"]
            if player == self.starting_direction:
                # We only want one client deciding the ball's position, let's use the
                # starting direction to decide which one
                self.shared_data["ball"] = data["ball"]
        with self.left_lock and self.right_lock:
            if player == "left":
                self.left_data["paddle"] = data["paddle"]
            elif player == "right":
                self.right_data["paddle"] = data["paddle"]
            self.left_data["score"] = data["lScore"]
            self.right_data["score"] = data["rScore"]

    # Author:        Michael Stacy
    # Purpose:       To start the game request
    # Pre:           Player String
    # Post:          Returns a Yes or No and Dictionary
    def start_game(self, player: str) -> Tuple[bool, dict]:
        """Starts the Game Sequence"""
        with self.shared_lock:
            self.ready[player] = True
            self.game_running = self.ready["left"] and self.ready["right"]
            wins = {
                "left_player": self.left_data["wins"],
                "right_player": self.right_data["wins"],
            }
            return self.game_running, wins

    # Author:        Michael Stacy
    # Purpose:       To reset the game start
    # Pre:           None
    # Post:          None
    def reset_start(self) -> None:
        """Resets the Start Sequence"""
        with self.shared_lock:
            self.ready = {
                "left": False,
                "right": False,
            }

    # Author:        Michael Stacy
    # Purpose:       To reset the game state
    # Pre:           None
    # Post:          None
    def reset_game(self) -> None:
        with self.shared_lock and self.left_lock and self.right_lock:
            self.shared_data = default_shared_data
            self.left_data = {
                "paddle": default_paddle,
                "score": 0,
                "wins": self.left_data.get("wins", 0),
            }
            self.right_data = {
                "paddle": default_paddle,
                "score": 0,
                "wins": self.right_data.get("wins", 0),
            }

            self.ready = {
                "left": False,
                "right": False,
            }

            self.starting_direction = random.choice(["left", "right"])

            self.game_running = False

    # Author:        Michael Stacy
    # Purpose:       To select the player's option for connecting
    # Pre:           None
    # Post:          Which player they are String
    def set_player(self, user: str, initials: str) -> Optional[str]:
        with self.shared_lock:
            if self.user["left"] == "":
                self.user["left"] = user
                self.initials["left"] = initials
                return "left_player"
            if self.user["right"] == "":
                self.user["right"] = user
                self.initials["right"] = initials
                return "right_player"

            return None

    # Author:        Michael Stacy
    # Purpose:       To return the player information (Initials)
    # Pre:           None
    # Post:          String Initials
    def grab_players(self) -> Tuple[str, str]:
        with self.shared_lock:
            return self.initials["left"], self.initials["right"]

    # Author:        Tag Howard
    # Purpose:       Returns the starting direction
    # Pre:           None
    # Post:          Direction String
    def grab_starting_direction(self) -> str:
        with self.shared_lock:
            return self.starting_direction

    # Author:        Michael Stacy
    # Purpose:       Do we continue the game?
    # Pre:           None
    # Post:          Bool True or False
    def continue_game(self) -> bool:
        with self.shared_lock:
            return self.game_running

    # Author:        Michael Stacy
    # Purpose:       Player Check to see if they're the left or right player
    # Pre:           None
    # Post:          Bool True or False
    def player_check(self, user: str) -> bool:
        with self.shared_lock:
            return self.user["left"] == user or self.user["right"] == user

    # Author:        Michael Stacy, Tag Howard
    # Purpose:       To increment the number of wins and reset the game
    # Pre:           Player String, Database
    # Post:          None
    def increment_win(self, player: str, database: db) -> None:
        """Increments the Wins in a Player"""
        with self.shared_lock:
            # Prevent us from incrementing where we already have
            if not self.game_running:
                return

            self.reset_game()

            username = self.user[player]

            if player == "left":
                with self.left_lock:
                    self.left_data["wins"] += 1
            elif player == "right":
                with self.right_lock:
                    self.right_data["wins"] += 1

            success, message, wins_number = database.grab_wins(username)

            if not success:
                print(f"Error: unable to grab wins,", message)
                return

            wins_number += 1

            success, message = database.update_wins(username, wins_number)

            if not success:
                print("Error: unable to update wins: ", message)
