from Database.dbHandler import Database

from Helpers.configureSettings import receiverSize
from Helpers.connectionHandler import *

from typing import Optional
from types import FrameType
import threading, signal, errno

# Connect to our database
playerDatabase = Database()

# Our gameHolder is a dictionary containing game instances. 
# Each game instance is a different game going on at the same time.
# Each game instance contains:
    # Running: Is the game running?
    # leftPlayer and rightPlayer: Is the player "Ready" to play? Is the player wanting to "playAgain"?

gameHolder = {
    'exampleInstance': {
        'Running': False, # Is there a current game running?
        'leftPlayer': {
            'Ready': False, # Player is ready for first game
            'playAgain': False, # Does the player wish to play again?
            'paddleInfo': {
                'X':0, # Position X
                'Y':0, # Position Y
                'Moving': '', # Which direction is the paddle moving
            }
        },
        'rightPlayer': {
            'Ready': False, # Player is ready for first game
            'playAgain': False, # Does the player wish to play again?
            'paddleInfo': {
                'X':0, # Position X
                'Y':0, # Position Y
                'Moving': '', # Which direction is the paddle moving
            }
        },
        'ballInfo': {
            'X':0, # Ball Poisition X
            'Y':0, # Ball Position Y
        },
        'scoreInfo': {
            'lScore':0, # Current game score of left
            'rScore':0, # Current game score of right
        },
        'gameHistory': {
            'leftPlayer':0, # How many times the leftPlayer has won
            'rightPlayer':0, # How many times the rightPlayer has won
        },
        'syncNumber': 0, # Used to identify the current syncing (who is ahead)
        'gameEnd': threading.Event(), # Used to notify all clients to exit the game instance back to main menu
        'gameLock': threading.Lock() # Used when updating the instance settings
    },
}

# Mechanism to shutdown the server
serverShutdown = threading.Event()

def clientControl(clientSocket:socket.socket, addressInfo:socket._RetAddress) -> None:

    clientInfo = {
        # We logged in?
        'loggedIn': False,

        # We playing game or spectating? If so, which gameHolder instance?
        'playingGame': False,
        'spectating': False,
        'gameInstance': None,

        # The username and initals of the player
        'Username': None,
        'Initials': None
    }
    
    while not serverShutdown.is_set():

        # Grab the next data packet from the client
        unpackedSuccess, newData = unpackInfo(clientSocket.recv(receiverSize).decode())

        # Logging in
        if newData['Request'] == 'Login':
            Username = newData['Username']
            crossCheck = playerDatabase.fetchData(table='Account', comparisonLogic=f'Username = "{Username}"', returnAttributes='Password')
            if not crossCheck:
                success = sendInfo(clientSocket, {'Request': 'Login', 'Success':False})
                if not success:
                    print('Failure to send error data to client')
                continue

            if crossCheck != newData['Password']:
                success = sendInfo(clientSocket, {'Request': 'Login', 'Success':False})
                if not success:
                    print('Failure to send failure data to client')
                continue
            
            # Send success on login
            success = sendInfo(clientSocket, {'Request': 'Login', 'Success':True})

            # Update clientInfo
            clientInfo['loggedIn'] = True
            clientInfo['Username'] = newData['Username']
            clientInfo['Initials'] = newData['Initials']

            if not success:
                print('Failure to send success data to client')

        # Account Creation
        if newData['Request'] == 'CreateAccount':
            # Grab the new username
            Username = newData['Username']

            # Check if that username already exists
            accountExists = playerDatabase.fetchData(table='Account', returnAttributes='Username', comparisonLogic=f'Username = "{Username}"')
            if accountExists:
                # Account already exists
                sendInfo(clientSocket, {'Request': 'CreateAccount', 'Success':False, 'Message': 'Account already exists'})
                continue
            
            success = playerDatabase.insertData(table='Account', information={'Username': Username, 'Password': newData['Password'], 'Initials': newData['Initials']})
            if not success:
                # Failure, could not add account to database
                sendInfo(clientSocket, {'Request': 'CreateAccount', 'Success': False, 'Message': 'Could not create account'})
                continue
            
            # Inform client of successfully making account
            sendInfo(clientSocket, {'Request': 'CreateAccount', 'Success': True})
        
        # Prevent unauthorized activity
        if not clientInfo['loggedIn']:
            success = sendInfo(clientSocket, {'Request': 'Login', 'Success':False})
            if not success:
                print('Failure to send error data to client')
                continue

        # Check if we need to start a game
        if newData['Request'] == 'startGame':
            # Return game instance info for ready status
            pass

        # Create Game Instance
        if newData['Request'] == 'newInstance':
            # Generate random key for instance
            # Set player as leftPlayer
            # Set player ready status
            # Set clientInfo for instance
            # Set clientInfo for playinggame
            pass

        # Delete Game Instance
        if newData['Request'] == 'deleteInstance':
            # Check that our Instance exists
            # Check that the client is one of the players in that instance
            # Use gameEnd.set()
            pass

        # Start Game Instance
        if newData['Request'] == 'joinGame':
            # Check if instance exist
            # Check if there is only one player
            # Set player ready status
            # Set clientInfo for instance
            # Set clientInfo for playinggame
            pass
        
        # Client request to restart game
        if newData['Request'] == 'restartGame':
            # Check if instance still exists
            # Check if other player exists still
            # Set player again status
            pass
        
        # Spectate a game?
        if newData['Request'] == 'spectateGame':
            # Check if instance exists
            # Check if there is are two players
            # Set clientInfo for spectating
            # Set clientInfo for instance
            pass

        # Leave Game Instance
        if newData['Request'] == 'leaveGame':
            # Leave the game. Reset clientInfo
            pass

        if newData['Request'] == 'updateGame':
            # Check if the client is a player
            # Check if instance exists
            # Update player paddle info
            # Check if sync > game instance sync
                # Update Ball and Score
            pass

        if newData['Request'] == 'grabGame':
            # Return game information about an instance
            pass

def shutdownSignal(signalNumber:int, frame:Optional[FrameType]) -> None:
    print('Server will now shut down')
    serverShutdown.set()

def runServer() -> None:
    global serverShutdown

    # Check for SIGINT and SIGTERM, our method to shut down the server
    signal.signal(signal.SIGINT, shutdownSignal)
    signal.signal(signal.SIGTERM, shutdownSignal)

    # Create our server, create a thread list
    serverSocket = createServer()
    threadList = []

    while not serverShutdown.is_set():

        # Prevent accept() from blocking us checking for serverShutdown
        serverSocket.setblocking(False)
        
        try:
            # Accept a new client
            newClient, addressInfo = serverSocket.accept()
        except socket.error as errorNote:
            if errorNote.errno == errno.EAGAIN or errorNote.errno == errno.EWOULDBLOCK:
                continue
            else:
                raise
        
        # Start a thread to handle client request
        newThread = threading.Thread(target=clientControl, args=(newClient, addressInfo))

        # Add thread to our list
        threadList.append(newThread)
        newThread.start()

    # Prevent incoming connections
    serverSocket.close()
    
    # Join all threads
    for thread in threadList:
        thread.join()

    print('Server Shutdown')

if __name__ == "__main__":
    runServer()