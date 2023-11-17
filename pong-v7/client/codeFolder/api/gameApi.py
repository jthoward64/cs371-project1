from email import message
from typing import Literal, Optional, TypedDict, Union

from ..sockethelper import Connection


class JoinGameResponse(TypedDict):
    player: Literal["left_player", "right_player", "spectate"]


class GameApi:
    connection: Connection

    def __init__(self, connection: Connection):
        self.connection = connection

    def send_and_check(
        self, request: str, data: Optional[dict] = None
    ) -> Union[dict, str]:
        success = self.connection.send({"request": request, **(data or {})})
        if success:
            response = self.connection.recv()
            if response is not None and response.get("request") == request:
                ok = response.get("return", False)
                if ok:
                    return response
                else:
                    return response.get("message", "Unknown error")
            else:
                return "Invalid response from server"
        else:
            return "Failed to send request to server"

    def join_game(self, username: str, password: str) -> Union[JoinGameResponse, str]:
        response = self.send_and_check(
            "join_game", {"username": username, "password": password}
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
