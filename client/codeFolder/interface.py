# =================================================================================================
# Contributing Authors:	    Tag Howard, John Michael Stacy, Juliann Hyatt
# Email Addresses:          jtho264@uky.edu, jmst231@uky.edu, jnhy222@uky.edu
# Date:                     October 31st, 2023
# Purpose:                  Our Tkinter Interface for Clients
# Misc:
# =================================================================================================

import os.path as path
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, Optional, Union

from .api.gameApi import GameApi
from .playGame import playGame
from .settings import MAIN_PORT, WINDOW_HEIGHT, WINDOW_WIDTH
from .sockethelper import Connection

current_dir = path.abspath(path.dirname(__file__))
assets_dir = path.join(current_dir, "..", "assets")


class Image(tk.Frame):
    # Author:        Michael Stacy
    # Purpose:       To create an image for Tkinter
    # Pre:           Tk Widget, Label images, Tk Image
    # Post:          None
    def __init__(self, parent: tk.Widget, label_image: tk.Image) -> None:
        super().__init__(parent)

        self.label = ttk.Label(self, image=label_image)
        self.label.pack(side="top", fill="x")

        self.pack(side="top", fill="both", expand=True)


class Label(tk.Frame):
    # Author:        Michael Stacy
    # Purpose:       To create an label
    # Pre:           Various Tk Widgets, Label Names, Label Text
    # Post:          None
    def __init__(self, parent: tk.Widget, label_name: str, label_text: str) -> None:
        super().__init__(parent)

        self.label = ttk.Label(self, name=label_name, text=label_text)
        self.label.pack(side="left", fill="x")

        self.pack()

    def set_text(self, new_text: str) -> None:
        self.label["text"] = new_text


class TextBox(tk.Frame):
    # Author:        Michael Stacy
    # Purpose:       To create a TextBox
    # Pre:           Parent, Label Name, Label Text
    # Post:          None
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
    # Author:        Michael Stacy
    # Purpose:       Create our Two Buttons
    # Pre:           Parent, Left_Text, Left_Button, Right_Text, Right_Button
    # Post:          None
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
    # Author:        Michael Stacy
    # Purpose:       To create our MainMenu
    # Pre:           Parent TK TK
    # Post:          None
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)

        # Our image item
        self.image_item = tk.PhotoImage(
            file=path.join(assets_dir, "images", "logo.png")
        )

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
    # Author:        Michael Stacy
    # Purpose:       To control the Code Menu
    # Pre:           Parent
    # Post:          None
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)

        # Our image item
        self.image_item = tk.PhotoImage(
            file=path.join(assets_dir, "images", "logo.png")
        )

        # Our image
        self.image = Image(self, self.image_item)

        # Game Code
        self.code = TextBox(self, label_name="code_label", label_text="Game Code:")

        self.pack(side="top", fill="both", expand=True)


class CreateMenu(tk.Frame):
    # Author:        Michael Stacy
    # Purpose:       Create the Menu
    # Pre:           Parent
    # Post:          None
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)

        # Our image item
        self.image_item = tk.PhotoImage(
            file=path.join(assets_dir, "images", "logo.png")
        )
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
    game_api: Optional[GameApi] = None

    # Author:        Michael Stacy
    # Purpose:       To create the Main Window
    # Pre:           None
    # Post:          None
    def __init__(self):
        super().__init__()

        # Set title and size
        self.title("Pong Login")

        # Create our Socket Interface for the Main Server
        self.server_socket: Connection = Connection(MAIN_PORT)

        if self.server_socket.maybe_server_issue:
            self.withdraw()
            messagebox.showerror(
                "Connection Error",
                "Failed to connect to server. Please check that the server is reachable and that you have configured the client correctly. Configuration can be set in settings.py or by passing an argument (see '--help' for more information).",
                parent=self,
            )
            self.destroy()
            return

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

    # Author:        Michael Stacy
    # Purpose:       Game Connection
    # Pre:           Port
    # Post:          Failed to Connect or Success
    def game_connect(self, port: int) -> Optional[str]:
        """Attempts to join the Game Server"""
        game_server = Connection(port)

        if game_server.maybe_server_issue:
            messagebox.showerror(
                "Connection Error",
                "Failed to connect to game server. Please check that the server is reachable and that you have configured the client correctly. Configuration can be set in settings.py or by passing an argument (see '--help' for more information).",
                parent=self,
            )
            return "Failed to Connect"

        # Check if the connection is established
        if not game_server.connection_open:
            return "Failed to Connect"

        self.game_api = GameApi(game_server)

        # Success, close the socket
        self.server_socket.close()

        join_game_response = self.game_api.join_game(self.username, self.password)

        if isinstance(join_game_response, str):
            print(f"Error: {join_game_response}")
            self.code_error.label.config(text=join_game_response)
            return

        self.withdraw()
        try:
            if join_game_response["player"] == "right_player":
                playGame(WINDOW_WIDTH, WINDOW_HEIGHT, "right", self.game_api)
            elif join_game_response["player"] == "left_player":
                playGame(WINDOW_WIDTH, WINDOW_HEIGHT, "left", self.game_api)
            else:
                print("Error, player is not a valid value")
                self.code_error.label.config(text="Error: player is not a valid value")
                return "Error: player is not a valid value"
        finally:
            self.deiconify()

        return None

    # Author:        Michael Stacy
    # Purpose:       Change our Menu
    # Pre:           Union Frame
    # Post:          None
    def change_menu(self, frame: Union[MainMenu, CreateMenu, CodeMenu]) -> None:
        """Change the Frame Menu"""
        self.main_frame.pack_forget()
        self.create_frame.pack_forget()
        self.code_frame.pack_forget()

        frame.pack(side="top", fill="both", expand=True)

    # Author:        Michael Stacy
    # Purpose:       Login and Validate the User Client
    # Pre:           String Username, Password
    # Post:          None
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

    # Author:        Michael Stacy
    # Purpose:       To join a game
    # Pre:           Code String
    # Post:          None
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

        if not self.game_connect(new_message["message"]):
            self.code_error.label.config(text="Error: could not connect to game server")

    # Author:        Michael Stacy
    # Purpose:       To make a game
    # Pre:           None
    # Post:          None
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

        if not self.game_connect(new_message["message"]):
            self.code_error.label.config(text="Error: could not connect to game server")

    # Author:        Michael Stacy
    # Purpose:       To create an account
    # Pre:           Username, Password, Confirmation Password, Initials
    # Post:          None
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

        self.username = username
        self.password = password

        self.change_menu(self.code_frame)
