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
from typing import Tuple, Optional, Union

# Our Address Family and Socket Type
from .settings import MAIN_ADDRESS, ADDRESS_FAMILY, SOCKET_KIND, CERTFILE, RECEIVER_SIZE

class ClientSocket:
    # The socket
    origin_socket:socket.socket

    # Main Socket
    client_socket:SSLSocket

    # The SSL Encryption Context
    context:ssl.SSLContext

    # Port Connection
    port:int

    # Is our connection open?
    client_open:bool

    def __init__(self, port:int) -> None:
        '''This class creates a Server to handle incoming Client Connections'''
        # Grab our Address Family and Socket Stream
        self.origin_socket = socket.socket(ADDRESS_FAMILY, SOCKET_KIND)
        self.load_context()

        # Connect to our server
        return_check, message = self.bind_client(port)
        if not return_check:
            print('Error could not connect to server')

        self.client_open = True

    def bind_client(self, port:int) -> Tuple[bool, Optional[OSError]]:
        '''Binds the server to the Specified Address and Port'''
        # Attempt to bind the server_socket to the given address/port
        try:
            self.client_socket.connect((MAIN_ADDRESS, port))
        except socket.error as new_error:
            return False, new_error
        
        # Update to our selected port number
        self.port = port

        return True, None
    
    def load_context(self) -> Tuple[bool, Optional[ssl.SSLError]]:
        '''Loads the SSL Context for Encryption'''
        # Attempt to encrypt the TLS Connection
        try:
            # Load our context to encrypt the connection
            self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            self.context.load_verify_locations(CERTFILE)

            # Ignore Certificate Authorities, but still require server's self-certification
            self.context.check_hostname = False
            self.context.verify_mode = ssl.CERT_REQUIRED

            # Wrap our socket
            self.client_socket = self.context.wrap_socket(self.origin_socket, server_hostname=MAIN_ADDRESS)
        except ssl.SSLError as new_error:
            return False, new_error
        
        return True, None
    
    def send(self, message:dict) -> Tuple[bool, Union[None, BrokenPipeError, EOFError, ConnectionError, UnicodeEncodeError]]:
        '''Attempts to send the message to the client socket'''
        try:
            self.client_socket.send(json.dumps(message).encode())
        except UnicodeEncodeError as new_error:
            return False, new_error
        except BrokenPipeError as new_error:
            self.close()
            return False, new_error
        except EOFError as new_error:
            return False, new_error
        except ConnectionError as new_error:
            self.close()
            return False, new_error
        
        return True, None
    
    def recv(self) -> Tuple[bool, Union[dict, BrokenPipeError, EOFError, ConnectionError, json.JSONDecodeError, UnicodeDecodeError]]:
        try:
            new_message = json.loads(self.client_socket.recv(RECEIVER_SIZE).decode())
            if not new_message:
                self.close()
                return False, EOFError('Connection Closed')
        except UnicodeDecodeError as new_error:
            return False, new_error
        except json.JSONDecodeError as new_error:
            return False, new_error
        except BrokenPipeError as new_error:
            self.close()
            return False, new_error
        except ConnectionError as new_error:
            self.close()
            return False, new_error

        return True, new_message
    
    def is_closed(self) -> bool:
        '''Will return True if the connection is closed'''
        return not self.client_open

    def close(self) -> None:
        '''Turns off the Connections, Shutsdown'''
        self.client_socket.close()
        del self.client_socket
        del self.context