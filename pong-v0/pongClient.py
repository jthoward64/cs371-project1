# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

from assets.code.helperCode import *
from connectionHandler import clientJoin, unpackInfo, sendInfo
from playGame import playGame
import tkinter as tk
import socket

# Updates our errorLabel
def updateLabel(errorLabel: tk.Label, message:str, app: tk.Tk) -> None:
    errorLabel.config(text=message)
    app.update()

# This is where you will connect to the server to get the info required to call the game loop.  Mainly
# the screen width, height and player paddle (either "left" or "right")
# If you want to hard code the screen's dimensions into the code, that's fine, but you will need to know
# which client is which
def joinServer(ip: str, port: str, errorLabel: tk.Label, app: tk.Tk) -> None:
    success, client = clientJoin(ip, port)
    if not success:
        # errorLabel, Message = client error, app
        updateLabel(errorLabel, f"Error, unable to connect to {ip}, port: {port}", app)

    # Ensure we have a client connected
    if type(client) == socket.socket:

        startGame = False
        pingFails = 0

        updateLabel(errorLabel, f"Waiting for Opponent to Join", app)

        while not startGame and pingFails < 10:
            # Ask the server to tell us when to start the game
            success = sendInfo(client, {"Type": "Start"})

            # Begin waiting to play
            try:
                unpackedResponse = client.recv(512).decode()
            # Did we get an error?
            except ConnectionResetError:
                unpackedResponse = False

            # Check if the server quit
            if not unpackedResponse:
                # Exit, server disconnected
                print("Server Error: Did not respond")
                pingFails += 1
                continue

            # Unpack the response
            unpacked, response = unpackInfo(unpackedResponse)

            # Did we error in unpacking?
            if not unpacked:
                continue
            
            if response["startGame"]:
                # Don't loop again
                startGame = True

                # Hide window and start the game
                app.withdraw()
                playGame(
                    response["screenWidth"],
                    response["screenHeight"],
                    response["player"],
                    client,
                )

        # Disconnect from client
        client.close()
        
        # Did we disconnect due to pingFails?
        if pingFails == 10:
            updateLabel(errorLabel, "Server Failed to Respond after 10 Attempts", app)
        else:
            # Quit the app, game is over
            app.quit()

# This displays the opening screen, you don't need to edit this (but may if you like)
def startScreen() -> None:
    app = tk.Tk()
    app.title("Server Info")

    image = tk.PhotoImage(file="./assets/images/logo.png")

    titleLabel = tk.Label(image=image)
    titleLabel.grid(column=0, row=0, columnspan=2)

    ipLabel = tk.Label(text="Server IP:")
    ipLabel.grid(column=0, row=1, sticky="W", padx=8)

    ipEntry = tk.Entry(app)
    ipEntry.grid(column=1, row=1)

    portLabel = tk.Label(text="Server Port:")
    portLabel.grid(column=0, row=2, sticky="W", padx=8)

    portEntry = tk.Entry(app)
    portEntry.grid(column=1, row=2)

    errorLabel = tk.Label(text="")
    errorLabel.grid(column=0, row=4, columnspan=2)

    joinButton = tk.Button(
        text="Join",
        command=lambda: joinServer(ipEntry.get(), portEntry.get(), errorLabel, app),
    )
    joinButton.grid(column=0, row=3, columnspan=2)

    app.mainloop()


if __name__ == "__main__":
    startScreen()

    # Uncomment the line below if you want to play the game without a server to see how it should work
    # the startScreen() function should call playGame with the arguments given to it by the server this is
    # here for demo purposes only
    # playGame(640, 480,"left",socket.socket(socket.AF_INET, socket.SOCK_STREAM))
