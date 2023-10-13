# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket, threading, json

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

""" Last Modified October 9th, 2023 ************************************************************************************************ """
"""
    Information Example from Client on Game Update
    
    newInfo = {
        # Type of Information: 0 = Game Start, 1 = Update Game
        'Request': 1,

        # Paddle Information
        'paddleX': playerPaddleObj.rect.x,      -- Integer
        'paddleY': playerPaddleObj.rect.y,      -- Integer
        'paddleMoving': playerPaddleObj.moving, -- String

        # Ball Information
        'ballX': ball.rect.x,                   -- Integer
        'ballY': ball.rect.y,                   -- Integer
            
        # Score Information
        'scoreLeft':lScore,                     -- Integer
        'scoreRight':rScore,                    -- Integer
            
        # Sync Status
        'sync':sync                             -- Integer
        }
    
    Example of Server Information
"""
# Use Lock when updating this information
gameInfo = {
    # Ball Information
    "ballX": 0,
    "ballY": 0,
    # Score
    "scoreLeft": 0,
    "scoreRight": 0,
    # Sync Status
    "sync": 0,
}

# Free to update
leftInfo = {
    "paddleX": 0,
    "paddleY": 0,
    "paddleMoving": "",
}

# Free to update
rightInfo = {
    "paddleX": 0,
    "paddleY": 0,
    "paddleMoving": "",
}

# Game Settings
screenWidth = 640
screenHeight = 480

# Create an event to shutdown
shutdownClients = threading.Event()

# Create a lock to protect information updates
lockClients = threading.Lock()


# Our thread instance when we have a new client
def clientHandler(client: socket.socket, clientNumber: int):
    # Information on Starter Information when Client Sends: "starterPack"
    newInfo = {
        "screenWidth": screenWidth,
        "screenHeight": screenHeight,
        "playerPaddle": "left" if clientNumber == 0 else "right",
    }

    # Begin receiving information
    while not shutdownClients.is_set():
        # Check if score is greater than 4?
        if gameInfo["scoreLeft"] > 3 or gameInfo["scoreRight"] > 3:
            """Need to Modify *************************************************************************************************"""
            pass

        # Receive Infomation
        package = json.loads(client.recv(512).decode())

        # Print Information
        #print(f"Client {clientNumber} Information: {package}")

        # Asking for starter information?
        if package["Request"] == 0:
            # Send our game starter information
            client.send(json.dumps(newInfo).encode())

        # Sending us an update?
        if package["Request"] == 1:
            # Update information
            if clientNumber == 0:
                # Left is updating
                leftInfo["paddleMoving"] = package["paddleMoving"]
                leftInfo["paddleX"] = package["paddleX"]
                leftInfo["paddleY"] = package["paddleY"]
            else:
                # Right is updating
                rightInfo["paddleMoving"] = package["paddleMoving"]
                rightInfo["paddleX"] = package["paddleX"]
                rightInfo["paddleY"] = package["paddleY"]

            # Update Sync if ahead
            if package["sync"] > gameInfo["sync"]:
                with lockClients:
                    # Update information
                    gameInfo["sync"] = package["sync"]
                    gameInfo["ballX"] = package["ballX"]
                    gameInfo["ballY"] = package["ballY"]
                    gameInfo["scoreLeft"] = package["scoreLeft"]
                    gameInfo["scoreRight"] = package["scoreRight"]

        # Requesting an update?
        if package["Request"] == 2:
            # Send Updated Information
            # Left Paddle, need to send Right's Information
            # Right Paddle, need to send Left's Information
            client.send(
                json.dumps(
                    {
                        "paddleMoving": rightInfo["paddleMoving"]
                        if clientNumber == 0
                        else leftInfo["paddleMoving"],
                        "paddleX": rightInfo["paddleX"]
                        if clientNumber == 0
                        else leftInfo["paddleX"],
                        "paddleY": rightInfo["paddleY"]
                        if clientNumber == 0
                        else leftInfo["paddleY"],
                        "ballX": gameInfo["ballX"],
                        "ballY": gameInfo["ballY"],
                        "scoreLeft": gameInfo["scoreLeft"],
                        "scoreRight": gameInfo["scoreRight"],
                        "sync": gameInfo["sync"],
                    }
                ).encode()
            )

    # Close the client, end the thread
    client.close()


# Our main function to grab connections
def startServer():
    # Set up the socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 4000))
    server.listen()

    # Max Players: 2
    maxClientAllowed = 2
    clientNumber = 0

    # Thread Control
    threadList = []

    # Open a path for new connections
    while clientNumber < maxClientAllowed:
        # Accept a new client
        clientSocket, clientAddress = server.accept()

        # Create a new thread to handle the client's incoming information
        newHandler = threading.Thread(
            target=clientHandler,
            args=(
                clientSocket,
                #clientAddress,
                clientNumber,
            ),
        )
        # Increase client number 
        clientNumber += 1

        # Add to array handler
        threadList.append(newHandler)
        newHandler.start()

    # Lock server from incoming connections
    server.close()

    # Wait for clients to disconnect
    for thread in threadList:
        thread.join()

    print("Server Shutdown")


if __name__ == "__main__":
    startServer()
""" Last Modified October 9th, 2023 ************************************************************************************************ """
