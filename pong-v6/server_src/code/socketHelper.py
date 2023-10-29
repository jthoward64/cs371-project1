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

# For Typing
from typing import Tuple, Optional, Union

# Our Address Family and Socket Type
from .settings import MAIN_ADDRESS, ADDRESS_FAMILY, SOCKET_KIND, CERTFILE, KEYFILE, PASSWORD

class Server:
    # The socket
    server_socket:socket.socket

    # The SSL Encryption Context
    context:ssl.SSLContext

    # Server Port Number
    port:int

    # Is the server open and listening for new clients?
    is_listening:bool = False

    def __init__(self, port:int) -> None:
        '''This class creates a Server to handle incoming Client Connections'''
        # Grab our Address Family and Socket Stream
        self.server_socket = socket.socket(ADDRESS_FAMILY, SOCKET_KIND)
        
        # Bind the Server, load the SSL Context
        self.bind_server(port)
        self.load_context()

    def bind_server(self, port:int) -> Tuple[bool, Optional[OSError]]:
        '''Binds the server to the Specified Address and Port'''
        # Attempt to bind the server_socket to the given address/port
        try:
            self.server_socket.bind((MAIN_ADDRESS, port))
        except socket.error as new_error:
            return False, new_error
        
        # Update to our selected port number
        self.port = port

        return True, None
    
    def load_context(self) -> Tuple[bool, Optional[ssl.SSLError]]:
        '''Loads the SSL Context for Encryption'''
        # Attempt to encrypt the TLS Connection
        try:
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self.context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE, password=PASSWORD)

        except ssl.SSLError as new_error:
            return False, new_error
        
        return True, None
    
    def accept(self) -> Tuple[bool, Union[SSLSocket, socket.error]]:
        '''Accepts Incoming Connections from new Clients'''
        try:
            client_socket, _ = self.server_socket.accept()
            secure_socket = self.context.wrap_socket(client_socket, server_side=True)
            return True, secure_socket
        except socket.error as new_error:
            return False, new_error
        
    def listen(self) -> Tuple[bool, Optional[socket.error]]:
        '''Listens for Incoming Connections'''
        try:
            self.server_socket.listen()
            self.is_listening = True
        except socket.error as new_error:
            return False, new_error
        
        return True, None
    
    def close(self) -> None:
        '''Turns off the Connections, Shutsdown'''
        self.is_listening = False
        self.server_socket.close()
        del self.server_socket
        del self.context
