from code.lobby import LobbyServer

from helpers.leaderboard import run_server

if __name__ == "__main__":
    print("Starting Lobby Server")
    run_server()
    run_game = LobbyServer()
    print("Lobby Server Closed")
