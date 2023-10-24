# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games
from connectionHandler import sendInfo, createServer, unpackInfo
from typing import Union, Dict
import socket
import threading

# Game Settings
screenWidth:int = 640
screenHeight:int = 480

# Create an event to shutdown
shutdownClients:threading.Event = threading.Event()

# Create a lock to protect information updates
lockClients:threading.Lock = threading.Lock()

# Our game information, atomic transactions (do not search if a key exist)
gameInfo = {
    0: {
        "ready": False,
        "Moving": "",
        "X": 0,
        "Y": 0,
    },
    1: {
        "ready": False,
        "Moving": "",
        "X": 0,
        "Y": 0,
    },
    "Ball": {
        "X": 0,
        "Y": 0,
    },
    "Score": {
        "lScore": 0,
        "rScore": 0
    },
    "Sync": 0,
}

def clientControl(client:socket.socket, player:int) -> None:
    global gameInfo, shutdownClients, lockClients, screenWidth, screenHeight

    clientInfo:Dict[str, Union[int, bool, str]] = {
        "startGame": False,
        "player": "",
        "screenWidth": screenWidth,
        "screenHeight": screenHeight,
    }

    if player == 1:
        clientInfo['player'] = "left"
    elif player == 0:
        clientInfo['player'] = "right"
    else:
        clientInfo['player'] = "spectate"

    opponentPlayer = 0 if player == 1 else 1

    # Continue running until we shut down
    while not shutdownClients.is_set():
        try:
            # Grab our clients request
            request = client.recv(512).decode()

        # Did we get an error?
        except ConnectionResetError:
            request = False

        # If it doesn't exist, client closed connection
        if not request:
            print("Client Exited Early")
            shutdownClients.set()
            continue

        # Did we successfully unpack our information?
        success, newInfo = unpackInfo(request)
        if not success:
            continue
        
        # Client is checking if it can start
        if newInfo["Type"] == "Start":
            # Notify our client is ready to start
            if player == 1 or player == 0:
                gameInfo[player]["ready"] = True

            # Is the other client ready to start?
            if gameInfo[0]["ready"] and gameInfo[1]["ready"]:
                clientInfo["startGame"] = True

            # Send information to client
            success = sendInfo(client, clientInfo)

            # End connection/game, timed out
            if not success:
                print(f"Client {player} timed out, game shutting down")
                shutdownClients.set()

        '''
        Example of Update
        
        update = {
            "Type": "Update",
            "Paddle": {
                "Moving":"",
                "X": 0,
                "Y": 1,
            }
            "Score": {
                "lScore":0,
                "rScore":0,
            }
            "Ball": {
                "X":0,
                "Y":0,
            }
            "Sync": 0,
        }
        '''

        # Client is updating the server
        if newInfo["Type"] == "Update":
            # Update the Players' Information
            with lockClients:
                gameInfo[player]["Moving"] = newInfo["Paddle"]["Moving"]
                gameInfo[player]["X"] = newInfo["Paddle"]["X"]
                gameInfo[player]["Y"] = newInfo["Paddle"]["Y"]

            # Do we update the ball and score?
            if newInfo["Sync"] > gameInfo["Sync"]:
                with lockClients:
                    gameInfo["Sync"] = newInfo["Sync"]
                    gameInfo["Ball"] = newInfo["Ball"]
                    gameInfo["Score"] = newInfo["Score"]

        # Client is grabbing information
        if newInfo["Type"] == "Grab":
            with lockClients:
                toSend = {
                    "Type": "Grab",
                    "Paddle": gameInfo[opponentPlayer],
                    "Ball": gameInfo["Ball"],
                    "Score": gameInfo["Score"],
                    "Sync": gameInfo["Sync"]
                }

            # Send the information, did we succeed?
            success = sendInfo(client, toSend)
            if not success:
                # Can modify to attempt to send again, if we reach so many failed attempts shut down the game
                pass
        
        if newInfo["Type"] == "Spectator":
            #with lockClients:
            toSend = {
                "Type": "Spectator",
                "lPaddle": gameInfo[1],
                "rPaddle": gameInfo[0],
                "Ball": gameInfo["Ball"],
                "Score": gameInfo["Score"],
                "Sync": gameInfo["Sync"]
            }

            # Send the information, did we succeed?
            success = sendInfo(client, toSend)
            if not success:
                # Can modify to attempt to send again, if we reach so many failed attempts shut down the game
                pass

    client.close()

def main() -> None:
    print("Server Start")

    # Create our server
    server = createServer()

    # Only allow 2 players to connect
    maxPlayers = 2
    currentPlayers = 0

    # Hold our client threads
    clientThreads = []

    # Grab the incoming client connections
    while currentPlayers < maxPlayers:
        # Accept our new client
        client, _ = server.accept()

        # Create a new thread
        newThread = threading.Thread(target=clientControl, args=(client, currentPlayers))
        newThread.start()

        # Add to our list of threads
        clientThreads.append(newThread)

        # Increment our currentPlayers
        currentPlayers += 1

    # Close our server to incoming connections
    server.close()

    # Wait for our threads to finish (clients all close)
    for thread in clientThreads:
        thread.join()
    
    print("Server Shutdown")

if __name__ == "__main__":
    main()