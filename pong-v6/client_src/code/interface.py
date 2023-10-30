# =================================================================================================
# Contributing Authors:	    Michael Stacy, Name Here, Name Here
# Email Addresses:          jmst231@uky.edu, Email Here, Email Here
# Date:                     October 30th, 2023
# Purpose:                  Our user interface for the Client's Main Menu
# Misc:                     
# =================================================================================================
import tkinter as tk

class Application:
    def __init__(self):
        # Create our application window
        self.app = tk.Tk()
        self.app.title('Pong Game')

        # Load our Logo
        self.image_item = tk.PhotoImage(file="assets/images/logo.png")

        # Load our menus
        self.main_menu()
        self.code_menu()
        self.create_menu()

        # Select the main_frame to present
        self.change_frame('main_frame')

        # Run the main_loop
        self.app.mainloop()

    def create_account(self, username:str, password:str, confirm:str) -> None:
        pass

    def create_game(self) -> None:
        pass

    def join_game(self, code:str) -> None:
        pass

    def try_login(self, username:str, password:str) -> None:

        # Go to the code_frame if the correct username and password are provided
        self.change_frame('code_frame')
        pass

    def change_frame(self, frame_name:str) -> None:
        # Hide all frames and remember, grab the visible frame's center point
        for frame in self.app.children.values():
            # Remove the frame from the grid
            frame.grid_remove()

        # Show the frame you want to display
        next_frame = self.app.children[frame_name]
        next_frame.grid()

    def main_menu(self) -> None:
        '''Our main menu frame for login'''
        # Create our frame
        new_frame = tk.Frame(self.app, name='main_frame')
        new_frame.grid(row=0, column=0)

        # Load our image
        image_label = tk.Label(new_frame, image=self.image_item)
        image_label.grid(column=0, row=0, columnspan=2, sticky='nsew')

        # Load our username label
        username_label = tk.Label(new_frame, text='Username:')
        username_label.grid(column=0, row=1, columnspan=1, sticky='e')

        # Load our username box
        username_box = tk.Entry(new_frame)
        username_box.grid(column=1, row=1, columnspan=1, sticky='e')

        # Load our password label
        password_label = tk.Label(new_frame, text='Password:')
        password_label.grid(column=0, row=2, columnspan=1, sticky='e')

        # Load our password box
        password_box = tk.Entry(new_frame)
        password_box.grid(column=1, row=2, columnspan=1, sticky='e')

        # Create our space label
        space = tk.Label(new_frame, name='space')
        space.grid(column=0, row=3, columnspan=2)

        # Load our button
        login_button = tk.Button(new_frame, text='Login', command=lambda:self.try_login(username_box.get(), password_box.get()))
        login_button.grid(column=0, row=4, columnspan=1, sticky='ew')

        # Load our button
        create_button = tk.Button(new_frame, text='Create Account', command=lambda:self.change_frame('create_frame'))
        create_button.grid(column=1, row=4, columnspan=1, sticky='ew')

        # Create our error label
        error_label = tk.Label(new_frame, name='error_label')
        error_label.grid(column=0, row=5, columnspan=2)

    def create_menu(self) -> None:
        '''Our main menu frame for login'''
        # Create our frame
        new_frame = tk.Frame(self.app, name='create_frame')
        new_frame.grid(row=0, column=0)

        # Load our image
        image_label = tk.Label(new_frame, image=self.image_item)
        image_label.grid(column=0, row=0, columnspan=2, sticky='nsew')

        # Load our username label
        username_label = tk.Label(new_frame, text='Username:')
        username_label.grid(column=0, row=1, columnspan=1, sticky='e')

        # Load our username box
        username_box = tk.Entry(new_frame)
        username_box.grid(column=1, row=1, columnspan=1, sticky='e')

        # Load our password label
        password_label = tk.Label(new_frame, text='Password:')
        password_label.grid(column=0, row=2, columnspan=1, sticky='e')

        # Load our password box
        password_box = tk.Entry(new_frame)
        password_box.grid(column=1, row=2, columnspan=1, sticky='e')

        # Load our confirmation password label
        password_label_confirm = tk.Label(new_frame, text='Confirm Password:')
        password_label_confirm.grid(column=0, row=3, columnspan=1, sticky='e')

        # Load our confirmation password box
        password_box_confirm = tk.Entry(new_frame)
        password_box_confirm.grid(column=1, row=3, columnspan=1, sticky='e')

        # Load our button
        login_button = tk.Button(new_frame, text='Create Account', command=lambda:self.create_account(username_box.get(), password_box.get(), password_box_confirm.get()))
        login_button.grid(column=1, row=4, columnspan=1, sticky='ew')

        # Load our button
        create_button = tk.Button(new_frame, text='Back', command=lambda:self.change_frame('main_frame'))
        create_button.grid(column=0, row=4, columnspan=1, sticky='ew')

        # Create our error label
        error_label = tk.Label(new_frame, name='error_label')
        error_label.grid(column=0, row=5, columnspan=2)

    def code_menu(self) -> None:
        '''Our code menu to enter a code'''
        # Create our frame
        new_frame = tk.Frame(self.app, name='code_frame')
        new_frame.grid(row=0, column=0)

        # Load our image
        image_label = tk.Label(new_frame, image=self.image_item)
        image_label.grid(column=0, row=0, columnspan=2, sticky='nsew')

        # Load our code label
        code_label = tk.Label(new_frame, text='Game Code:')
        code_label.grid(column=0, row=1, columnspan=1, sticky='e')

        # Load our code box
        code_box = tk.Entry(new_frame)
        code_box.grid(column=1, row=1, columnspan=1, sticky='e')

        # Create our space label
        space = tk.Label(new_frame, name='space')
        space.grid(column=0, row=2, columnspan=2)

        # Create our space label
        space = tk.Label(new_frame, name='space')
        space.grid(column=0, row=3, columnspan=2)

        # Load our button to join a game
        login_button = tk.Button(new_frame, text='Join Game', command=lambda:self.join_game(code_box.get()))
        login_button.grid(column=0, row=4, columnspan=1, sticky='ew')

        # Load our button to create a game
        create_button = tk.Button(new_frame, text='Create Game', command=self.create_game)
        create_button.grid(column=1, row=4, columnspan=1, sticky='ew')

        # Create our error label
        error_label = tk.Label(new_frame, name='error_label')
        error_label.grid(column=0, row=5, columnspan=2)
