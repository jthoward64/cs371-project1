# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

from typing import Tuple, Union
import json, socket

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

# Creates a server
def createServer(host:str='localhost', port:str='4000') -> socket.socket:
    # Creates a socket and binds it to a host/port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))

    # Listens for clients
    server.listen()
    return server

# Attempts to join the server
def clientJoin(ip: str, port: str) -> Tuple[bool, Union[socket.socket, socket.error]]:
    # Create our client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Attempt to connect to server
    try:
        client.connect((ip, int(port)))
    except socket.error as errorMessage:
        return False, errorMessage

    return True, client