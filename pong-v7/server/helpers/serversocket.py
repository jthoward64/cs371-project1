# =================================================================================================
# Contributing Authors:	    Michael Stacy, Tag Howard, Juliann Hyatt
# Email Addresses:          jmst231@uky.edu, jtho264@uky.edu, jnhy222@uky.edu
# Date:                     October 29th, 2023
# Purpose:                  Creates our Server to accept incoming Clients
# Misc:                     Documentation: https://docs.python.org/3/library/socket.html
# Misc:                     Documentation: https://docs.python.org/3/library/ssl.html#module-ssl
# =================================================================================================

# Module to create a Server Socket
import socket
import ssl
from ssl import SSLSocket

# For Typing
from typing import Optional

# Our Address Family and Socket Type
from .settings import (
    ADDRESS_FAMILY,
    CERTFILE,
    KEYFILE,
    MAIN_ADDRESS,
    PASSWORD,
    SOCKET_KIND,
)

class ServerSocket:
    # Is our connection open?
    connection_open: bool = False

    # Our port number
    port: int

    # Author:        Michael Stacy
    # Purpose:       To simplify the Socket Connection and Bind the Server
    # Pre:           Port Int
    # Post:          None
    def __init__(self, port: int) -> None:
        """Create a new connection to the server"""
        # Bind the server
        self.bind(port)

    # Author:        Michael Stacy
    # Purpose:       To set up the binding and SSL encryption
    # Pre:           Port Int
    # Post:          Bool
    def bind(self, port: int) -> bool:
        try:
            # Create our Socket and Bind it
            self._holder = socket.socket(ADDRESS_FAMILY, SOCKET_KIND)
            self._holder.bind((MAIN_ADDRESS, port))

            # Load our context for encryption
            self._context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self._context.load_cert_chain(
                certfile=CERTFILE, keyfile=KEYFILE, password=PASSWORD
            )

            # Wrap our Socket
            self.client: SSLSocket = self._context.wrap_socket(
                self._holder, server_hostname=MAIN_ADDRESS
            )

            # Listen for incoming connections
            self.client.listen()
            self.connection_open = True

            # Set a timeout
            self.client.settimeout(2)

            # Begin Listening on Socket
        except ssl.SSLError as new_error:
            print("Error on SSL Socket: ", new_error)
            self._holder.close()
            return False
        except socket.error as new_error:
            print("Error on Socket:", new_error)
            self._holder.close()
            return False

        # Success, inform we are open to the server
        self.port = self.client.getsockname()[1] if port == 0 else port
        self.connection_open = True
        return True

    # Author:        Michael Stacy
    # Purpose:       Accepts an incoming client connection
    # Pre:           None
    # Post:          SSL Socket or None
    def accept(self) -> Optional[SSLSocket]:
        """Attempts to accept an incoming connection"""
        try:
            # Attempt to accept new client
            new_socket, _ = self.client.accept()
        except ssl.SSLError as new_error:
            print("Error on Accept: ", new_error)
            return None
        except socket.timeout as new_error:
            return None

        return new_socket

    # Author:        Michael Stacy
    # Purpose:       Closes the Server Socket
    # Pre:           None
    # Post:          None
    def close(self) -> None:
        """Closes our connection"""
        self.client.close()
        self.connection_open = False
