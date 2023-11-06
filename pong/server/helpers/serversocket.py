# =================================================================================================
# Contributing Authors:	    Michael Stacy, Name Here, Name Here
# Email Addresses:          jmst231@uky.edu, Email Here, Email Here
# Date:                     October 29th, 2023
# Purpose:                  Creates our Server to accept incoming Clients
# Misc:                     Documentation: https://docs.python.org/3/library/socket.html
# Misc:                     Documentation: https://docs.python.org/3/library/ssl.html#module-ssl
# =================================================================================================

# Module to create a Server Socket
import socket, ssl
from ssl import SSLSocket

# For Typing
from typing import Optional

# Our Address Family and Socket Type
from .settings import MAIN_ADDRESS, ADDRESS_FAMILY, SOCKET_KIND, CERTFILE, KEYFILE, PASSWORD

class ServerSocket:
    # Is our connection open?
    connection_open:bool = False

    # Our port number
    port:int

    def __init__(self, port:int) -> None:
        '''Create a new connection to the server'''
        # Bind the server
        self.bind(port)
        
    def bind(self, port:int) -> bool:
        try:
            # Create our Socket and Bind it
            self._holder = socket.socket(ADDRESS_FAMILY, SOCKET_KIND)
            self._holder.bind((MAIN_ADDRESS, port))

            # Load our context for encryption
            self._context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self._context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE, password=PASSWORD)

            # Wrap our Socket
            self.client:SSLSocket = self._context.wrap_socket(self._holder, server_hostname=MAIN_ADDRESS)

            # Listen for incoming connections
            self.client.listen()
            self.connection_open = True

            # Set a timeout
            self.client.settimeout(2)
        
            # Begin Listening on Socket
        except ssl.SSLError as new_error:
            print('Error on SSL Socket: ', new_error)
            self._holder.close()
            return False
        except socket.error as new_error:
            print('Error on Socket:', new_error)
            self._holder.close()
            return False
        
        # Success, inform we are open to the server
        self.port = port
        self.connection_open = True
        return True
    
    def accept(self) -> Optional[SSLSocket]:
        '''Attempts to accept an incoming connection'''
        try:
            # Attempt to accept new client
            new_socket, _ = self.client.accept()
        except ssl.SSLError as new_error:
            print('Error on Accept: ', new_error)
            return None
        except socket.timeout as new_error:
            print('Accept Timed Out')
            return None
    
        return new_socket
    
    def close(self) -> None:
        '''Closes our connection'''
        self.client.close()
        self.connection_open = False