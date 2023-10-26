from typing import Union, List, Dict, Optional
from Helpers.configureSettings import receiverSize
from Helpers.connectionHandler import *
from threading import Lock
import threading

# Our game controller
class gameInstance:
    def __init__(self, instanceName:str, creatorUsername:str) -> None:

        # Game Instance Settings
        self.Running:bool = True
        self.Round:bool = False

        # Set our process name and the username of who created the game instance
        self.instanceName:str = instanceName
        self.Creator:str = creatorUsername

        # Are the players ready to start?
        self.readyLock:Lock = threading.Lock()
        self.leftReady:bool = False
        self.rightReady:bool = False
        

        # Do players wish to play again?
        self.againLock:Lock = threading.Lock()
        self.leftAgain:bool = False
        self.rightAgain:bool = False
        

        # List of all spectators
        self.spectateLock:Lock = threading.Lock()
        self.Spectators:List[str] = []
        

        # Ball Information
        self.ballLock:Lock = threading.Lock()
        self.Ball:Dict[str, int] = {
            'X':0,
            'Y':0,
        }
        
        # leftPlayer Information
        self.leftLock:Lock = threading.Lock()
        self.leftPlayer:Dict[str, Union[None, str, Dict[str, Union[int,str]]]] = {
            'Username': None,
            'Paddle': {
                'X': 0,
                'Y': 0,
                'Moving': ''
            },
        }

        # rightPlayer Information
        self.rightLock:Lock = threading.Lock()
        self.rightPlayer:Dict[str, Union[None, str, Dict[str, Union[int,str]]]] = {
            'Username': None,
            'Paddle': {
                'X': 0,
                'Y': 0,
                'Moving': ''
            },
        }

        # Game Information
        self.infoLock:Lock = threading.Lock()
        self.lScore:int = 0
        self.rScore:int = 0
        self.Sync:int = 0

        # Game History of how many wins each player has
        self.historyLock:Lock = threading.Lock()
        self.gameHistory:Dict[str, Union[int, Lock]] = {
            'leftPlayer':0,
            'rightPlayer':0,
        }

        # Event to shutdown the game
        self.shutDown = threading.Event()

    # Check if the game is ready to play
    def gameReady(self) -> bool:
        # Thread Safety
        with self.readyLock:
            return self.leftReady and self.rightReady
    
    # Can the person requesting to be a player, be a player?
    def joinStatus(self, Username:str) -> Optional[str]:
        # Thread Safety
        with self.leftLock:
            # Is there a leftPlayer
            if self.leftPlayer['Username'] == None:
                # Update leftPlayer Status
                self.leftPlayer['Username'] = Username
                return 'Left'
            
        with self.rightLock:
            # Is there a rightPlayer
            if self.rightPlayer['Username'] == None:
                # Update rightPlayer Status
                self.rightPlayer['Username'] = Username
                return 'Right'
            
        return None
    
    def updateGame(self, newData:dict, playerStatus:str) -> None:
        with self.infoLock:
            # Check if we need to update the Sync, Ball, and Scores
            if newData['Sync'] > self.Sync:

                # Update scores and sync information
                self.lScore = newData['lScore']
                self.rScore = newData['rScore']
                self.Sync = newData['Sync']
                        
                # Update ball information
                with self.ballLock:
                    self.Ball['X'] = newData['Ball']['X']
                    self.Ball['Y'] = newData['Ball']['Y']

        # Check which player
        if playerStatus == 'Left':
            # Lock the leftPlayer
            with self.leftLock:
                self.leftPlayer = newData['Player']
                return

        # Lock the rightPlayer
        with self.rightLock:
            self.rightPlayer = newData['Player']

    # Our formatting of the data
    def grabData(self) -> dict:
        returnData = {}

        # Grab leftPlayer Data
        with self.leftLock:
            returnData['leftPlayer'] = self.leftPlayer

        # Grab rightPlayer Data
        with self.rightLock:
            returnData['rightPlayer'] = self.rightPlayer

        # Grab Ball Data
        with self.ballLock:
            returnData['Ball'] = self.Ball

        # Grab Score and Sync
        with self.infoLock:
            returnData['Score'] = {
                'lScore': self.lScore,
                'rScore': self.rScore
            }
            returnData['Sync'] = self.Sync

        # Grab Game History
        with self.historyLock:
            returnData['gameHistory'] = self.gameHistory

        return returnData
    
    # Our client thread in the process
    def joinGame(self, Username:str, clientSocket:socket.socket, playRequest:bool) -> None:
        
        # Check if the client is requesting to be a player
        playerStatus = self.joinStatus(Username) if playRequest else None # None = Spectator, 'Left' = leftPlayer, 'Right' = rightPlayer

        # Check if the client wishes to leave the game
        clientExit = False

        if not playerStatus:
            with self.spectateLock:
                self.Spectators.append(Username)

        # Loop through requests
        while not self.shutDown.is_set() and not clientExit:
            # Grab our next set of data
            unpackedSuccess, newData = unpackInfo(clientSocket.recv(receiverSize).decode())

            # Ask client to resend data as we had an error unpacking it
            if not unpackedSuccess:
                sendInfo(clientSocket, {'Request': 'sendAgain'})
                continue

            if newData['Request'] == 'playerStatus':
                if playerStatus:
                    sendInfo(clientSocket, {'Request': 'playerStatus', 'playerInfo': playerStatus})
                else:
                    sendInfo(clientSocket, {'Request': 'playerStatus', 'playerInfo': 'Spectator'})
                
                continue

            if newData['Request'] == 'startGame':
                if self.gameReady():
                    if playerStatus:
                        sendInfo(clientSocket, {'Request': 'startGame', 'playerInfo': playerStatus})
                    else:
                        sendInfo(clientSocket, {'Request': 'startGame', 'playerInfo': 'Spectator'})

                continue
            
            # Check if we are needing to update the game
            if newData['Request'] == 'updateGame' and playerStatus and self.Round:
                self.updateGame(newData, playerStatus)
                continue

            # Check if we are needing to grab the game
            if newData['Request'] == 'grabGame':
                # Create new dictionary to send off
                returnData = self.grabData()
                sendInfo(clientSocket, returnData)
                continue

            if newData['Request'] == 'quitGame':
                clientExit = True

                # Check if we need to shutdown the process or remove from spectator list
                if playerStatus:
                    self.shutDown.set()
                else:
                    with self.spectateLock:
                        self.Spectators.remove(Username)
        
        # Do we need to inform the client to quit?
        if not clientExit:
            # Game Instance over, shutDown was set
            sendInfo(clientSocket, {'Request': 'exitGame'})