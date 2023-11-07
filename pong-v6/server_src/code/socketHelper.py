# =================================================================================================
# Contributing Authors:	    Michael Stacy, Tag Howard, Juliann Hyatt
# Email Addresses:          jmst231@uky.edu, jtho264@uky.edu, jnhy222@uky.edu
# Date:                     October 29th, 2023
# Purpose:                  A way to create an encrypted Server Socket for Games and Main Server
# Misc:                     Documentation: https://docs.python.org/3/library/ssl.html
# =================================================================================================

# Need json for encoding/decoding dictionary
import json

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


class EncodeMessage:
    def __init__(self, message: dict):
        try:
            # Convert to Binary
            self.binary = json.dumps(message).encode("utf-8")

        except UnicodeEncodeError as new_error:
            print("Encoding Error: ", new_error)
            return


class DecodeMessage:
    # The original bytes
    def __init__(self, incoming: bytes) -> None:
        try:
            # Decode
            self.message = json.loads(incoming.decode("utf-8"))

        except UnicodeDecodeError as new_error:
            print("Decoding Error: ", new_error)
            return
        except json.JSONDecodeError as new_error:
            print("JSON Loading Error: ", new_error)
            return


class Client:
    connection_open: bool = True

    def __init__(self, connection: SSLSocket) -> None:
        self.client = connection

    def send(self, message: EncodeMessage) -> bool:
        """Attempts to Send the Message to the Server"""
        try:
            self.client.send(message.binary)
        except ssl.SSLError as new_error:
            print("Error on Send: ", new_error)
            self.client.close()
            self.connection_open = False
            return False

        return True

    def recv(self) -> Optional[DecodeMessage]:
        """Attempts to Send the Message to the Server"""
        try:
            new_message = DecodeMessage(self.client.recv())
        except ssl.SSLError as new_error:
            print("Error on Send: ", new_error)
            self.client.close()
            self.connection_open = False
            return None
        except socket.timeout as new_error:
            print("Recv Timed Out")
            return None

        return new_message

    def close(self) -> None:
        self.client.close()
        self.connection_open = False


class Connection:
    # Is our connection open?
    connection_open: bool = False

    # Our port number
    port: int

    def __init__(self, port: int) -> None:
        """Create a new connection to the server"""
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
            return
        except socket.error as new_error:
            print("Error on Socket:", new_error)
            return

        # Success, inform we are open to the server
        self.port = port
        self.connection_open = True

    def accept(self) -> Optional[SSLSocket]:
        """Attempts to accept an incoming connection"""
        try:
            # Attempt to accept new client
            new_socket, _ = self.client.accept()
        except ssl.SSLError as new_error:
            print("Error on Accept: ", new_error)
            return None
        except socket.timeout as new_error:
            print("Accept Timed Out")
            return None

        return new_socket

    def close(self) -> None:
        """Closes our connection"""
        self.client.close()
        self.connection_open = False
