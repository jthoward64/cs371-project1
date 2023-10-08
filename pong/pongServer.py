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

''' Last Modified October 8th, 2023 ************************************************************************************************ '''
'''
    Information Example from Client on Game Update and Server to Client
    
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
'''

gameInfo = {
    # Left Paddle
    'leftPaddleX': 0,
    'leftPaddleY': 0,

    # Right Paddle
    'rightPaddleX': 0,
    'rightPaddleY': 0,

    # Ball Information
    'ballX': 0,
    'ballY': 0,

    # Score
    'scoreLeft':0,
    'scoreRight':0,

    # Sync Status
    'sync':0
}

# Game Settings
screenWidth = 640
screenHeight = 480

# Create an event to shutdown
shutdownClients = threading.Event()

# Create a lock to protect information updates
lockClients = threading.Lock()

# Our thread instance when we have a new client
def clientHandler(client:socket.socket, clientNumber:int):
    # Information on Starter Information when Client Sends: "starterPack"
    newInfo = {
        'screenWidth':screenWidth,
        'screenHeight':screenHeight,
        'playerPaddle': "left" if clientNumber == 0 else "right",
    }

    # Begin receiving information
    while not shutdownClients.is_set():
        # Receive Infomation
        package = json.loads(client.recv(4096).decode())

        # Asking for starter information?
        if package['Request'] == 0:
            # Send our game starter information
            client.send(json.dump(newInfo).encode())
        
        # Sending us an update?
        if package['Request'] == 1:
            # Update information
            ''' Need to Modify ******************************************************************************************************************************** '''
            pass

        # Requesting an update?
        if package['Request'] == 2:
            # Send Updated Information
            ''' Need to Modify ******************************************************************************************************************************** '''
            pass

    # Close the client, end the thread
    client.close()

# Our main function to grab connections
def startServer():
    
    # Set up the socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind('localhost', 400)
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
        newHandler = threading.Threat(target=clientHandler, args=(clientSocket, clientAddress, clientNumber,))
        threadList.append(newHandler)

    # Lock server from incoming connections
    server.close()

    # Wait for clients to disconnect
    for thread in threadList:
        thread.join()

    print('Server Shutdown')

    
if __name__ == "__main__":
    startServer()
''' Last Modified October 8th, 2023 ************************************************************************************************ '''