import random
import threading as th
from typing import Literal, Tuple, TypedDict

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
    wins: SendWins


class GameInfo:
    def __init__(self) -> None:
        self.game_data: None = None

        # Lock for basic game data
        self.shared_lock = th.Lock()
        self.shared_data: SharedGameInfo
        self.starting_direction: Literal["left", "right"]

        # Lock for the player's data
        self.left_lock = th.Lock()
        self.left_data: PlayerData
        self.right_lock = th.Lock()
        self.right_data: PlayerData

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

        # Win Counter
        self.wins = {"left": 0, "right": 0}

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
                "wins": {
                    "left_player": self.left_data["wins"],
                    "right_player": self.right_data["wins"],
                },
            }

            return new_info

    def update_game(self, player: str, data: dict) -> None:
        """Updates the game data"""
        with self.shared_lock:
            self.shared_data["sync"] = data["sync"]
            self.shared_data["ball"] = data["ball"]
        if player == "left":
            with self.left_lock:
                self.left_data["paddle"] = data["paddle"]
                self.left_data["score"] = data["score"]
                self.left_data["wins"] = data["wins"]
        elif player == "right":
            with self.right_lock:
                self.right_data["paddle"] = data["paddle"]
                self.right_data["score"] = data["score"]
                self.right_data["wins"] = data["wins"]

    def start_game(self, player: str) -> bool:
        """Starts the Game Sequence"""
        with self.shared_lock:
            self.ready[player] = True
            self.game_running = self.ready["left"] and self.ready["right"]
            return self.game_running

    def reset_start(self) -> None:
        """Resets the Start Sequence"""
        with self.shared_lock:
            self.ready = {
                "left": False,
                "right": False,
            }

    def reset_game(self) -> None:
        with self.shared_lock and self.left_lock and self.right_lock:
            self.shared_data = {
                "ball": {
                    "x": 0,
                    "y": 0,
                    "xVel": 0,
                    "yVel": 0,
                },
                "sync": 0,
            }
            self.left_data = {
                "paddle": {
                    "x": 0,
                    "y": 0,
                    "moving": "",
                },
                "score": 0,
                "wins": 0,
            }
            self.right_data = {
                "paddle": {
                    "x": 0,
                    "y": 0,
                    "moving": "",
                },
                "score": 0,
                "wins": 0,
            }

            self.starting_direction = random.choice(["left", "right"])

            self.game_running = False

    def set_player(self, user: str, initials: str) -> str:
        with self.shared_lock:
            if self.user["left"] == "":
                self.user["left"] = user
                self.initials["left"] = initials
                return "left_player"
            if self.user["right"] == "":
                self.user["right"] = user
                self.initials["right"] = initials
                return "right_player"

            return "spectate"

    def grab_players(self) -> Tuple[str, str]:
        with self.shared_lock:
            return self.initials["left"], self.initials["right"]

    def grab_starting_direction(self) -> str:
        with self.shared_lock:
            return self.starting_direction

    def continue_game(self) -> bool:
        with self.shared_lock:
            return self.game_running

    def player_check(self, user: str) -> bool:
        with self.shared_lock:
            return self.user["left"] == user or self.user["right"] == user

    def increment_win(self, player: str):
        """Increments the Wins in a Player"""
        with self.shared_lock:
            # Prevent us from incrementing where we already have
            if not self.game_running:
                return

            self.reset_game()

            username = self.user[player]
            self.wins[player] += 1

            if player == "left":
                with self.left_lock:
                    self.left_data["wins"] += 1
            elif player == "right":
                with self.right_lock:
                    self.right_data["wins"] += 1

            success, message, wins_number = self.database.grab_wins(username)

            if not success:
                print(f"Error: unable to grab wins,", message)
                return

            wins_number += 1

            success, message = self.database.update_wins(username, wins_number)

            if not success:
                print("Error: unable to update wins: ", message)
