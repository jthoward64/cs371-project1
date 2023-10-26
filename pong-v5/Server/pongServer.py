# Socket Helper
from Helpers.connectionHandler import sendInfo, unpackInfo, createServer

# Server Settings
from Helpers.configureSettings import receiverSize, serverIP, serverPort

# Database
from Database.dbHandler import Database

# Type Hinting
from typing import Dict, Union, Optional, List
from types import FrameType
from threading import Lock

# Processing/Threads/Sockets/Random/Error Handling/Signals
import multiprocessing, threading, socket, random, errno, signal

# Our gameInstances
from gameInstance import gameInstance

# Do we shut down our server?
serverShutdown = threading.Event()

# Connect to our database
playerDatabase = Database()

# List of all gameInstance objects
gameManager = multiprocessing.Manager()
gameInstances = gameManager.dict()

# multiprocessing.Process(target=newInstance, args=(gameInstances, clientSocket, clientInfo['Username']))
def newInstance(gamesList:dict, Creator:socket.socket, Username:str) -> None:
    
    # Grab new gameInstances
    newName = f'IG{random.randint(1,9999)}'
    while newName in gamesList:
        newName = f'IG{random.randint(1,9999)}'
    
    # Create new gameInstance
    newGame = gameInstance(newName, Username)

    # Add to gameInstances
    gameInstances[newName] = newGame

    # Join Game
    newGame.joinGame(Username, Creator, True)

    # Game has Ended, remove from gameInstances
    gameInstances.pop(newName)

def clientControl(clientSocket:socket.socket, addressInfo:socket._RetAddress) -> None:

    clientInfo = {
        # We logged in?
        'loggedIn': False,

        # We playing game? If so, which gameHolder instance?
        'playingGame': False,
        'gameInstance': None,

        # The username and initals of the player
        'Username': None,
        'Initials': None
    }
    
    while not serverShutdown.is_set():

        # Grab the next data packet from the client
        unpackedSuccess, newData = unpackInfo(clientSocket.recv(receiverSize).decode())
        if not unpackedSuccess:
            sendInfo(clientSocket, {'Request': 'sendAgain'})

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
        
        # Do they want to create a server?
        if newData['Request'] == 'createGame':

            # Create a new game
            newGame = multiprocessing.Process(target=newInstance, args=(gameInstances, clientSocket, clientInfo['Username']))
            newGame.start()

            # Wait for client to exit process
            newGame.join()

        # Do they want an updated list of servers?
        if newData['Request'] == 'grabServers':
            # Grab our list of servers
            returnData = {'Request': 'grabServers', 'Servers': gameInstances.keys()}
            sendInfo(clientSocket, returnData)

        # Do they want to join a server?
        if newData['Request'] == 'joinGame':
            if newData['gameName'] in gameInstances:
                # Start gaming!
                gameInstances[newData['gameName']].joinGame(clientInfo['Username'], clientSocket, newData['toPlay'])


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