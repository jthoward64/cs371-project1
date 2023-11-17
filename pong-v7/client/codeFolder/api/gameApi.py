from email import message
from typing import Literal, Optional, TypedDict, Union

from ..sockethelper import Connection


class JoinGameResponse(TypedDict):
    player: Literal["left_player", "right_player", "spectate"]


class GameMeta(TypedDict):
    left_player_initials: str
    right_player_initials: str
    game_code: str


class PaddleInfo(TypedDict):
    x: int
    y: int
    moving: Optional[Literal["up", "down"]]


class BallInfo(TypedDict):
    x: int
    y: int
    x_vel: int
    y_vel: int


class GameInfo(TypedDict):
    opponent_paddle: PaddleInfo
    ball: BallInfo
    left_score: int
    right_score: int
    sync: int


class GameApi:
    connection: Connection

    def __init__(self, connection: Connection):
        self.connection = connection

    def send_and_check(
        self, request: str, data: Optional[dict], checkOk: bool = True
    ) -> Union[dict, str]:
        success = self.connection.send({"request": request, **(data or {})})
        if success:
            response = self.connection.recv()
            if response is not None and response.get("request") == request:
                ok = response.get("return", False)
                if ok or not checkOk:
                    return response
                else:
                    return response.get("message", "Unknown error")
            else:
                return "Invalid response from server"
        else:
            return "Failed to send request to server"

    def join_game(
        self, username: str, password: str, initials: str
    ) -> Union[JoinGameResponse, str]:
        response = self.send_and_check(
            "join_game",
            {"username": username, "password": password, "initials": initials},
        )
        if isinstance(response, dict):
            request = response.get("message", None)
            if (
                request == "left_player"
                or request == "right_player"
                or request == "spectate"
            ):
                return {"player": request}
            else:
                return "Invalid response from server (message was not a valid player)"
        else:
            return response

    def game_info(self) -> Union[GameMeta, str]:
        response = self.send_and_check("game_info", None)
        if isinstance(response, dict):
            left_player_initials = response.get("left_player_initials", "N/A")
            right_player_initials = response.get("right_player_initials", "N/A")
            game_code = response.get("game_code", None)
            if game_code is None:
                return "Invalid response from server (game_code was None)"
            else:
                return {
                    "left_player_initials": left_player_initials,
                    "right_player_initials": right_player_initials,
                    "game_code": game_code,
                }
        else:
            return response

    def start_game(self) -> Union[GameMeta, Literal[False], str]:
        """
        Returns GameInfoResponse if successful and ready to play, False if not ready to play, and str if error
        """
        response = self.send_and_check("start_game", None, False)
        if isinstance(response, dict):
            if response.get("return", False):
                return False
            else:
                left_player_initials = response.get("left_player_initials", "N/A")
                right_player_initials = response.get("right_player_initials", "N/A")
                game_code = response.get("game_code", None)
                if game_code is None:
                    return "Invalid response from server (game_code was None)"
                else:
                    return {
                        "left_player_initials": left_player_initials,
                        "right_player_initials": right_player_initials,
                        "game_code": game_code,
                    }
        else:
            return response

    def grab_game(self) -> Union[GameInfo, str]:
        response = self.send_and_check("grab_game", None)
        if isinstance(response, dict):
            paddle = response.get("paddle", None)
            ball = response.get("ball", None)
            left_score = response.get("lScore", None)
            right_score = response.get("rScore", None)
            sync = response.get("sync", None)
            if (
                paddle is None
                or ball is None
                or left_score is None
                or right_score is None
                or sync is None
            ):
                return "Invalid response from server (missing data)"
            else:
                paddle_x = paddle.get("x", None)
                paddle_y = paddle.get("y", None)
                paddle_moving = paddle.get("moving", None)
                ball_x = ball.get("x", None)
                ball_y = ball.get("y", None)
                ball_x_vel = ball.get("xVel", None)
                ball_y_vel = ball.get("yVel", None)
                left_score = left_score
                right_score = right_score
                sync = sync

                if (
                    paddle_x is None
                    or paddle_y is None
                    or paddle_moving is None
                    or ball_x is None
                    or ball_y is None
                    or ball_x_vel is None
                    or ball_y_vel is None
                    or left_score is None
                    or right_score is None
                    or sync is None
                ):
                    return "Invalid response from server (missing data)"
                else:
                    if paddle_moving == "up":
                        parsed_paddle_moving = "up"
                    elif paddle_moving == "down":
                        parsed_paddle_moving = "down"
                    elif paddle_moving == "":
                        parsed_paddle_moving = None
                    else:
                        return "Invalid response from server (paddle moving was not up, down, or empty string)"

                    return {
                        "opponent_paddle": {
                            "x": paddle_x,
                            "y": paddle_y,
                            "moving": parsed_paddle_moving,
                        },
                        "ball": {
                            "x": ball_x,
                            "y": ball_y,
                            "x_vel": ball_x_vel,
                            "y_vel": ball_y_vel,
                        },
                        "left_score": left_score,
                        "right_score": right_score,
                        "sync": sync,
                    }
        else:
            return response

    def update_game(
        self,
        own_paddle: PaddleInfo,
        ball: BallInfo,
        left_score: int,
        right_score: int,
        sync: int,
    ) -> bool:
        return self.connection.send(
            {
                "request": "update_game",
                "message": {
                    "paddle": {
                        "x": own_paddle["x"],
                        "y": own_paddle["y"],
                        "moving": own_paddle["moving"] or "",
                    },
                    "ball": {
                        "x": ball["x"],
                        "y": ball["y"],
                        "xVel": ball["x_vel"],
                        "yVel": ball["y_vel"],
                    },
                    "score": {"lscore": left_score, "rscore": right_score},
                    "sync": sync,
                },
            }
        )
