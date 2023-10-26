# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

from typing import Tuple, Union
from configureSettings import serverIP, serverPort
import json, socket, ssl

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

# Attempts to join the server
def clientJoin() -> Tuple[bool, Union[socket.socket, socket.error]]:
    # Create our client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ## We Need To Add Encryption ##
    ## We Need To Add Encryption ##
    ## We Need To Add Encryption ##
    ## We Need To Add Encryption ##
    ## We Need To Add Encryption ##

    # Attempt to connect to server
    try:
        client.connect((serverIP, int(serverPort)))
    except socket.error as errorMessage:
        return False, errorMessage

    return True, client

# Creates a server
def createServer() -> socket.socket:
    # Creates a socket and binds it to a host/port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((serverIP, int(serverPort)))

    ## We Need To Add Encryption ##
    ## We Need To Add Encryption ##
    ## We Need To Add Encryption ##
    ## We Need To Add Encryption ##
    ## We Need To Add Encryption ##

    # Listens for clients
    server.listen()
    return server