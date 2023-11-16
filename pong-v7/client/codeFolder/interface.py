# =================================================================================================
# Contributing Authors:	    Michael Stacy, Juliann Hyatt, Name Here
# Email Addresses:          jmst231@uky.edu, jnhy222@uky.com, Email Here
# Date:                     October 31st, 2023
# Purpose:                  Our Tkinter Interface for Clients
# Misc:
# =================================================================================================

import tkinter as tk
from tkinter import ttk
from typing import Callable, Union

from .settings import MAIN_PORT
from .sockethelper import Connection

from .settings import MAIN_PORT, WINDOW_HEIGHT, WINDOW_WIDTH

from .spectateGame import playGame as spectateGame
from .playGame import playGame


class Image(tk.Frame):
    def __init__(self, parent: tk.Widget, label_image: tk.Image) -> None:
        super().__init__(parent)

        self.label = ttk.Label(self, image=label_image)
        self.label.pack(side="top", fill="x")

        self.pack(side="top", fill="both", expand=True)


class Label(tk.Frame):
    def __init__(self, parent: tk.Widget, label_name: str, label_text: str) -> None:
        super().__init__(parent)

        self.label = ttk.Label(self, name=label_name, text=label_text)
        self.label.pack(side="left", fill="x")

        self.pack()

    def set_text(self, new_text: str) -> None:
        self.label["text"] = new_text


class TextBox(tk.Frame):
    def __init__(self, parent: tk.Widget, label_name: str, label_text: str) -> None:
        super().__init__(parent)

        # Spacer
        self.label2 = ttk.Label(self, name="label2")
        self.label2.pack(side="left", fill="x")

        # Our label for box
        self.label = ttk.Label(self, name=label_name, text=label_text)
        self.label.pack(side="left", fill="x")

        # Our box
        self.box = ttk.Entry(self)
        self.box.pack(side="left", fill="x", padx=(20, 10))

        self.pack()


class TwoButton(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        left_text: str,
        left_button: Callable,
        right_text: str,
        right_button: Callable,
    ) -> None:
        super().__init__(parent)

        # Spacer
        self.label = ttk.Label(self, name="label1")
        self.label.pack(side="left", fill="x")

        # Create button and add it to the frame
        self.button_left = ttk.Button(self, text=left_text, command=left_button)
        self.button_left.pack(side="left", fill="x")

        # Create button and add it to the frame
        self.button_right = ttk.Button(self, text=right_text, command=right_button)
        self.button_right.pack(side="left", fill="x")

        # Spacer
        self.label2 = ttk.Label(self, name="label2")
        self.label2.pack(side="left", fill="x")

        self.pack()


class MainMenu(tk.Frame):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)

        # Our image item
        self.image_item = tk.PhotoImage(file="assets/images/logo.png")

        # Our image
        self.image = Image(self, self.image_item)

        # Username and Password
        self.username = TextBox(
            self, label_name="username_label", label_text="Username:"
        )
        self.password = TextBox(
            self, label_name="password_label", label_text="Password:"
        )

        self.pack(side="top", fill="both", expand=True)


class CodeMenu(tk.Frame):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)

        # Our image item
        self.image_item = tk.PhotoImage(file="assets/images/logo.png")

        # Our image
        self.image = Image(self, self.image_item)

        # Game Code
        self.code = TextBox(self, label_name="code_label", label_text="Game Code:")

        self.pack(side="top", fill="both", expand=True)


class CreateMenu(tk.Frame):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)

        # Our image item
        self.image_item = tk.PhotoImage(file="assets/images/logo.png")
        # Our image
        self.image = Image(self, self.image_item)

        # Username and Password
        self.initials = TextBox(
            self, label_name="initial_label", label_text="Initials:"
        )
        self.username = TextBox(
            self, label_name="username_label", label_text="Username:"
        )
        self.password = TextBox(
            self, label_name="password_label", label_text="Password:"
        )
        self.confirm = TextBox(self, label_name="confirm_label", label_text="Password:")

        self.pack(side="top", fill="both", expand=True)


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set title and size
        self.title("Pong Login")

        # Create our Socket Interface for the Main Server
        self.server_socket: Connection = Connection(MAIN_PORT)

        # Create our Login Page
        self.main_frame = MainMenu(self)
        self.main_buttons = TwoButton(
            self.main_frame,
            left_text="Login",
            right_text="Create Account",
            left_button=lambda: self.login(
                self.main_frame.username.box.get(), self.main_frame.password.box.get()
            ),
            right_button=lambda: self.change_menu(self.create_frame),
        )
        self.main_error = Label(
            self.main_frame, label_name="error_label", label_text=""
        )

        # Our Code Menu
        self.code_frame = CodeMenu(self)
        self.code_buttons = TwoButton(
            self.code_frame,
            left_text="Join Game",
            right_text="Create Game",
            left_button=lambda: self.join(self.code_frame.code.box.get()),
            right_button=lambda: self.make(),
        )
        self.code_error = Label(
            self.code_frame, label_name="error_label", label_text=""
        )

        # Create Account Menu
        self.create_frame = CreateMenu(self)
        self.create_buttons = TwoButton(
            self.create_frame,
            left_text="Back",
            right_text="Create Account",
            left_button=lambda: self.change_menu(self.main_frame),
            right_button=lambda: self.create(
                self.create_frame.username.box.get(),
                self.create_frame.password.box.get(),
                self.create_frame.confirm.box.get(),
                self.create_frame.initials.box.get(),
            ),
        )
        self.create_error = Label(
            self.create_frame, label_name="error_label", label_text=""
        )

        # Start by setting to Login Page
        self.change_menu(self.main_frame)

    def game_connect(self, port:int) -> bool:
        '''Attempts to join the Game Server'''
        self.game_server = Connection(port)
        
        # Check if the connection is established
        if not self.game_server.connection_open:
            return False

        # Success, close the socket
        self.server_socket.close()

        self.game_server.send({'request':'join_game', 'username':self.username, 'password':self.password})

        new_message = self.game_server.recv()

        if new_message is None:
            print('Error, message is empty')
            return False
        
        if new_message['player'] == 'spectate':
            spectateGame(WINDOW_WIDTH, WINDOW_HEIGHT, self.game_server)
        elif new_message['player'] == 'right_player':
            playGame(WINDOW_WIDTH, WINDOW_HEIGHT, "right", self.game_server)
        elif new_message['player'] == 'left_player':
            playGame(WINDOW_WIDTH, WINDOW_HEIGHT, "left", self.game_server)

        return True

    def change_menu(self, frame:Union[MainMenu, CreateMenu, CodeMenu]) -> None:
        '''Change the Frame Menu'''
        self.main_frame.pack_forget()
        self.create_frame.pack_forget()
        self.code_frame.pack_forget()

        frame.pack(side="top", fill="both", expand=True)

    def login(self, username: str, password: str) -> None:
        """Send a Request to the Server for Login Validation"""
        # Send the server our login
        print(f"Attempting to login. Username: ({username}), Password: ({password})")
        self.server_socket.send(
            {"request": "login", "username": username, "password": password}
        )

        # Grab the return message
        new_message = self.server_socket.recv()

        # Check if we have a success
        if not new_message:
            # Check if our connection is closed, if so inform user the server isn't connected
            return

        if new_message["return"] == False:
            # Inform the user the login failed
            self.main_error.label.config(text=new_message["error"])
            return

        # Login Successful, go to code_frame
        self.username = username
        self.password = password
        self.change_menu(frame=self.code_frame)

    def join(self, code: str) -> None:
        """Send a Request to the Server to Join a Game"""
        print(f"Attempting to Join game. Code: ({code})")
        self.server_socket.send({"request": "join_game", "code": code})

        new_message = self.server_socket.recv()
        if not new_message:
            return

        if new_message["return"] == False:
            self.code_error.label.config(text=new_message["error"])
            return

        if not self.game_connect(new_message['message']):
            self.code_error.label.config(text='Error: could not connect to game server')
        
    def make(self) -> None:
        """Send a Request to the Server to Make a Game"""
        print(f"Attempting to make game.")
        self.server_socket.send({"request": "create_game"})

        new_message = self.server_socket.recv()
        if not new_message:
            return

        print(
            f'Create Return: {new_message["return"]}, Type: {type(new_message["return"])}'
        )

        if new_message["return"] == False:
            self.code_error.label.config(text=new_message["error"])
            return
        
        if not self.game_connect(new_message['message']):
            self.code_error.label.config(text='Error: could not connect to game server')

    def create(self, username: str, password: str, confirm: str, initials: str) -> None:
        """Send a Request to the Server to Create an Account"""
        print(
            f"Attempting to create account. Username: ({username}), Password: ({password}), Initials: ({initials})"
        )
        # Validate if the confirm and password are the same
        if password != confirm:
            self.create_error.label.config(text="Passwords do not match")
            return

        # Request the server to create a new account
        # new_message['username'], new_message['password'], new_message['initials']
        self.server_socket.send(
            {
                "request": "create_account",
                "username": username,
                "password": password,
                "initials": initials,
            }
        )

        # Grab the return message
        new_message = self.server_socket.recv()
        if not new_message:
            return

        if new_message["return"] == False:
            self.create_error.label.config(text=new_message["error"])
            return

        self.change_menu(self.code_frame)