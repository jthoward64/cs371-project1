from configureSettings import serverIP, serverPort
from typing import Tuple
import json, socket

# Creates the server instance
def createServer() -> socket.socket:
    
    # Create a AF_INET SOCK_STREAM socket
    newServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the serverIP and serverPort
    newServer.bind((serverIP, serverPort))

    # Allow incoming connections
    newServer.listen()

    ## We Need To Add Encryption ##
    ## We Need To Add Encryption ##
    ## We Need To Add Encryption ##
    ## We Need To Add Encryption ##
    ## We Need To Add Encryption ##

    return newServer

# Attempts to send a message to the client
def sendInfo(client:socket.socket, infoToSend:dict) -> bool:
    # Encode the information
    newInfo = json.dumps(infoToSend).encode()

    # Attempt to send
    try:
        client.send(newInfo)
    except socket.error:
        print("Error, unable to send to client")
        return False

    return True

# Attempts to unpack via JSON, will return false if we fail
def unpackInfo(request:str) -> Tuple[bool, dict]:
    # Attempt to decode the request
    try:
        requestInfo = json.loads(request)
    except json.JSONDecodeError:
        print("Error, unable to decode requestInfo")
        return False, {}
    
    return True, requestInfo