# Module to understand SSLSockets
from ssl import SSLSocket

# Need JSON for Dumping/Loading
import json

# For Typing
from typing import Tuple, Union

# Settings
from .settings import RECEIVER_SIZE

class ClientConnection:
    def __init__(self, client_socket:SSLSocket) -> None:
        '''Our connection object'''
        self.client_socket:SSLSocket = client_socket

        self.client_open = True

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
        if self.client_socket:
            self.client_open = False
            self.client_socket.close()