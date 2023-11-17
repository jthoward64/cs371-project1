# =================================================================================================
# Contributing Authors:	    Michael Stacy, Juliann Hyatt, Name Here
# Email Addresses:          jmst231@uky.edu, jnhy222@uky.edu, Email Here
# Date:                     October 29th, 2023
# Purpose:                  A way to create an encrypted Server Socket for Games and Main Server
# Misc:                     Documentation: https://docs.python.org/3/library/ssl.html
# =================================================================================================

# Need json for encoding/decoding dictionary
import json

# Module to create a Server Socket
import socket
import ssl
import traceback
from ssl import SSLSocket

# For Typing
from typing import Literal, Optional

# Our Address Family and Socket Type
from .settings import ADDRESS_FAMILY, CERTFILE, MAIN_ADDRESS, RECEIVER_SIZE, SOCKET_KIND


class Connection:
    # Is our connection open?
    connection_open: bool = False

    maybe_server_issue: bool = False

    # Our port number
    port: int

    def __init__(self, port: int) -> None:
        """Create a new connection to the server"""
        try:
            self.__holder = socket.create_connection((MAIN_ADDRESS, port), 3)

            # Load our context to encrypt the connection
            self.__context = ssl.create_default_context()
            self.__context.load_verify_locations(CERTFILE)

            # Ignore the Certificate Authority, but require server's self-certification
            # Ignore Certificate Authorities, but still require server's self-certification
            self.__context.check_hostname = False
            self.__context.verify_mode = ssl.CERT_REQUIRED

            # Wrap our Socket
            self.client: SSLSocket = self.__context.wrap_socket(
                self.__holder, server_hostname=MAIN_ADDRESS
            )

        except socket.timeout as new_error:
            print("Socket Timeout: ", new_error)
            self.maybe_server_issue = True
            return
        except ssl.SSLError as new_error:
            print("SSL Error on Socket: ", new_error, traceback.format_exc())
            return
        except socket.error as new_error:
            if new_error.errno == 111:
                print("Connection Refused")
                self.maybe_server_issue = True
                return
            else:
                print("Error on Socket:", new_error, traceback.format_exc())
            return

        # Success, inform we are open to the server
        self.port = port
        self.connection_open = True

    def send(self, message: dict) -> bool:
        if not self.connection_open:
            print(
                "Tried to send message when connection is closed",
                traceback.format_exc(),
            )
            return False

        """Attempts to Send the Message to the Server"""
        try:
            # Encode the Message and Send
            new_message = self.encode_message(message)
            if not new_message:
                print("Error Encoding Message")
                return False

            self.client.send(new_message)
        except ssl.SSLError as new_error:
            # Error, report and close connection
            print("Error on Send: ", new_error)
            self.client.close()
            self.connection_open = False
            return False

        return True

    def recv(self) -> Optional[dict]:
        """Attempts to Send the Message to the Server"""
        new_message = self.decode_message()

        return new_message

    def encode_message(self, message: dict) -> Optional[bytes]:
        try:
            # Convert to Binary
            binary = json.dumps(message).encode("utf-8")
        except UnicodeEncodeError as new_error:
            print("Encoding Error: ", new_error)
            return None

        return binary

    def decode_message(self) -> Optional[dict]:
        if not self.connection_open:
            print(
                "Tried to send message when connection is closed",
                traceback.format_exc(),
            )
            return None

        try:
            # Decode
            incoming = self.client.recv(RECEIVER_SIZE)
            message = json.loads(incoming.decode("utf-8"))
        except UnicodeDecodeError as new_error:
            print("Decoding Error: ", new_error)
            return None
        except json.JSONDecodeError as new_error:
            print("JSON Loading Error: ", new_error)
            self.client.close()
            self.connection_open = False
            return None
        except ssl.SSLError as new_error:
            print("Error on Send: ", new_error)
            self.client.close()
            self.connection_open = False
            return None

        return message

    def close(self) -> None:
        self.client.close()
        self.connection_open = False
