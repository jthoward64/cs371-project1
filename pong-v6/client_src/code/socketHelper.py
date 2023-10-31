# =================================================================================================
# Contributing Authors:	    Michael Stacy, Name Here, Name Here
# Email Addresses:          jmst231@uky.edu, Email Here, Email Here
# Date:                     October 29th, 2023
# Purpose:                  A way to create an encrypted Server Socket for Games and Main Server
# Misc:                     Documentation: https://docs.python.org/3/library/ssl.html
# =================================================================================================

# Module to create a Server Socket
import socket, ssl
from ssl import SSLSocket

# Need json for encoding/decoding dictionary
import json

# For Typing
from typing import Optional

# Our Address Family and Socket Type
from .settings import MAIN_ADDRESS, ADDRESS_FAMILY, SOCKET_KIND, CERTFILE, RECEIVER_SIZE

class EncodeMessage:
    # The original dictionary
    _origin:dict

    def __init__(self, message:dict):
        try:
            # Save a copy of our origin message
            self._origin = message

            # Convert to JSON
            self._message = json.dumps(message)

            # Convert to Binary
            self.binary = self._message.encode('utf-8')

        except UnicodeEncodeError as new_error:
            print('Encoding Error: ', new_error)
            return
        
class DecodeMessage:
    # The original bytes
    _origin:bytes

    def __init__(self, message:bytes) -> None:
        try:
            # Save a copy
            self._origin = message

            # Decode
            self._message = message.decode('utf-8')

            # Convert to dictionary
            self.message = json.loads(self._message)

        except UnicodeDecodeError as new_error:
            print('Decoding Error: ', new_error)
            return
        except json.JSONDecodeError as new_error:
            print('JSON Loading Error: ', new_error)
            return

class Connection:
    # Create our socket
    __holder:socket.socket = socket.socket(ADDRESS_FAMILY, SOCKET_KIND)

    # Is our connection open?
    connection_open:bool = False

    # Our port number
    port:int

    def __init__(self, port:int) -> None:
        '''Create a new connection to the server'''
        try:
            # Load our context to encrypt the connection
            self.__context = ssl.create_default_context()
            self.__context.load_verify_locations(CERTFILE)

            # Ignore the Certificate Authority, but require server's self-certification
            # Ignore Certificate Authorities, but still require server's self-certification
            self.__context.check_hostname = False
            self.__context.verify_mode = ssl.CERT_REQUIRED

            # Wrap our Socket
            self.client:SSLSocket = self.__context.wrap_socket(self.__holder, server_hostname=MAIN_ADDRESS)

            # Set a timer
            self.client.settimeout(2)

            # Connect to the Server
            self.client.connect((MAIN_ADDRESS, port))

        except ssl.SSLError as new_error:
            print('Error on SSL Socket: ', new_error)
            del self.client
            return
        except socket.error as new_error:
            print('Error on Socket:', new_error)
            del self.client
            return

        # Success, inform we are open to the server
        self.port = port
        self.connection_open = True

    def send(self, message:EncodeMessage) -> bool:
        '''Attempts to Send the Message to the Server'''
        try:
            self.client.send(message.binary)
        except ssl.SSLError as new_error:
            print('Error on Send: ', new_error)
            self.client.close()
            self.connection_open = False
            return False
        
        return True
    
    def recv(self) -> Optional[DecodeMessage]:
        '''Attempts to Send the Message to the Server'''
        try:
            new_message = DecodeMessage(self.client.recv())
        except ssl.SSLError as new_error:
            print('Error on Recv: ', new_error)
            self.client.close()
            self.connection_open = False
            return None
        except socket.timeout as new_error:
            print('Recv Timed Out')
            return None
        
        return new_message
    
    def close(self) -> None:
        self.client.close()
        self.connection_open = False