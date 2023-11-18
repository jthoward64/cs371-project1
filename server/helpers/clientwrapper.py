# =================================================================================================
# Contributing Authors:	    Michael Stacy, Tag Howard, Juliann Hyatt
# Email Addresses:          jmst231@uky.edu, jtho264@uky.edu, jnhy222@uky.edu
# Date:                     October 29th, 2023
# Purpose:                  Wraps the Client Sockets for Communication Handling
# Misc:                     Documentation: https://docs.python.org/3/library/socket.html
# Misc:                     Documentation: https://docs.python.org/3/library/ssl.html#module-ssl
# =================================================================================================

# Need json for encoding/decoding dictionary
import json
from socket import timeout

# Module to create a Server Socket
from ssl import SSLError, SSLSocket

# For Typing
from typing import Optional

# The size of the receiver
from .settings import RECEIVER_SIZE


class ClientWrapper:
    connection_open: bool = True

    # Author:        Michael Stacy
    # Purpose:       To simplify the SSL Socket Control
    # Pre:           SSLSocket
    # Post:          None
    def __init__(self, connection: SSLSocket) -> None:
        """Creates a new ClientWrapper to handle the SSLSocket Connection"""
        self.client = connection

    def send(self, message: dict) -> bool:
        """Attempts to Send the Message to the Server"""
        try:
            # Encode the Message and Send
            new_message = self._encode_message(message)
            if not new_message:
                print("Error Encoding Message")
                return False

            self.client.send(new_message)
        except SSLError as new_error:
            # Error, report and close connection
            print("Error on Send: ", new_error)
            self.client.close()
            self.connection_open = False
            return False

        return True

    # Author:        Michael Stacy
    # Purpose:       To receive messages from the SSLSocket
    # Pre:           None
    # Post:          Dictionary Items
    def recv(self) -> Optional[dict]:
        """Attempts to Send the Message to the Server"""
        new_message = self._decode_message()

        return new_message

    # Author:        Michael Stacy
    # Purpose:       To encode the data
    # Pre:           Message Dict
    # Post:          Encoded Bytes
    def _encode_message(self, message: dict) -> Optional[bytes]:
        try:
            # Convert to Binary
            binary = json.dumps(message).encode("utf-8")
        except UnicodeEncodeError as new_error:
            print("Encoding Error: ", new_error)
            return None

        return binary

    # Author:        Michael Stacy
    # Purpose:       To decode a message
    # Pre:           None
    # Post:          Dictionary Data
    def _decode_message(self) -> Optional[dict]:
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
        except timeout as new_error:
            print("Recv Timed Out")
            return None
        except SSLError as new_error:
            print("Error on Send: ", new_error)
            self.client.close()
            self.connection_open = False
            return None

        return message

    # Author:        Michael Stacy
    # Purpose:       To close the SSL Socket
    # Pre:           None
    # Post:          None
    def close(self) -> None:
        self.client.close()
        self.connection_open = False
