import tkinter as tk
import sys
import socket
import json

from playGame import playGame


# This is where you will connect to the server to get the info required to call the game loop.  Mainly
# the screen width, height and player paddle (either "left" or "right")
# If you want to hard code the screen's dimensions into the code, that's fine, but you will need to know
# which client is which
def joinServer(ip: str, port: str, errorLabel: tk.Label, app: tk.Tk) -> None:
    # Purpose:      This method is fired when the join button is clicked
    # Arguments:
    # ip            A string holding the IP address of the server
    # port          A string holding the port the server is using
    # errorLabel    A tk label widget, modify it's text to display messages to the user (example below)
    # app           The tk window object, needed to kill the window

    # Create a socket and connect to the server
    # You don't have to use SOCK_STREAM, use what you think is best
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Last Modified October 8th, 2023 ************************************************************************************************ """
    # Attempt to connect to server
    try:
        client.connect((ip, int(port)))
    except socket.error as errorMessage:
        errorLabel.config(text=f"Failure to connect to server: IP{ip}, Port: {port}")
        print(f"Error: {errorMessage}")

    # Get the required information from your server (screen width, height & player paddle, "left or "right)

    # Request the starter information from the server
    package = json.dumps({"Request": 0})
    try:
        client.send(package.encode())
    except socket.error as errorMessage:
        errorLabel.config(f"Starter Information Failed: {errorMessage}")

    # Server will use JSON to send information to unpack
    responseJSON = client.recv(512).decode()  # Client gets stuck here
    response = json.loads(responseJSON)

    # Example of a server response
    """
    response = {
        'screenWidth':0,
        'screenHeight':0,
        'playerPaddle': "",
    }
    """

    # If you have messages you'd like to show the user use the errorLabel widget like so
    errorLabel.config(text=f"Connected to game. IP: {ip}, Port: {port}")

    # You may or may not need to call this, depending on how many times you update the label
    # errorLabel.update(text=f'Game Start')

    # Close this window and start the game with the info passed to you from the server
    app.withdraw()  # Hides the window (we'll kill it later)
    playGame(
        response["screenWidth"],
        response["screenHeight"],
        response["playerPaddle"],
        client,
    )  # User will be either left or right paddle
    client.close()  # Client disconnects from the server on game end
    app.quit()  # Kills the window
    """ Last Modified October 8th, 2023 ************************************************************************************************ """
