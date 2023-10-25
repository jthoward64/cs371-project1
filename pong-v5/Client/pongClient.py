# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

from Helpers.connectionHandler import clientJoin, unpackInfo, sendInfo
from Helpers.configureSettings import screenHeight, screenWidth
from Helpers.frameHandler import *
from Helpers.appHandler import *

from assets.code.helperCode import *
import socket, time, threading

from playGame import playGame

# Updates our errorLabel
def updateLabel(errorLabel: tk.Label, message:str, app: tk.Tk) -> None:
    errorLabel.config(text=message)
    app.update()

# Logins to the server
# argsList=[username.get(), password.get(), errorLabel, app.root]
def loginServer(username:str, password:str, errorLabel:tk.Label, app:tk.Tk, holder:mainApp) -> None:
    app.quit()

# Request to make our account
# argsList=[username.get(), password.get(), passwordConfirm.get(), errorLabel, app.root]
def makeAccount(username:str, password:str, passwordConfirm:str, errorLabel:tk.Label, app:tk.Tk, holder:mainApp) -> None:
    app.quit()

# Takes us to our registration page
def accountMenu(app:mainApp) -> None:
    app.changeFrame("accountCreation")

# Takes us back to our regular login page
def mainMenu(app:mainApp) -> None:
    app.changeFrame("loginScreen")

# Countdown timer
def sleepWait(timeOut:int, errorLabel:tk.Label) -> None:
    numLeft = timeOut
    while numLeft > 0:
        errorLabel.config(text=f'Failed to Join! Retrying in: {numLeft} seconds')
        time.sleep(1)
        numLeft -= 1

# Do we stop the Thread?
stopThreads = False

# Connects the client to the server
def connectServer(errorLabel:tk.Label, app:mainApp) -> None:
    # Our stop method
    global stopThreads
    
    # Loop until we connect
    numTries = 0
    while not stopThreads:
        if numTries > 0:
            # Wait 2^(numTries) seconds before attempting again, 1-64 seconds
            sleepWait(2**(numTries), errorLabel)
    
        # Start our client
        success, client = clientJoin()
        if success and type(client) == socket.socket:
            app.client = client
            app.changeFrame("loginScreen")
            return
        
        if numTries < 5:
            numTries += 1
    
def onClose(app) -> None:
    global stopThreads

    # Stop all threads
    stopThreads = True

    # Close the client
    if hasattr(app, 'client') and app.client:
        app.client.close()
    
    # Destroy the root safely
    app.root.destroy()

def startScreen() -> None:
    # Create our Application
    # def __init__(self:object, screenWidth:int, screenHeight:int) -> None:
    app = mainApp()

    # What if we close the window? Safely close.
    app.root.protocol("WM_DELETE_WINDOW", lambda: onClose(app))

    # Start our loading page
    loadingPage(app)

    # Load our login starter screen
    loginScreen(app)

    # Load our account creation screen
    accountCreation(app)

    # Set the Frame Window
    app.changeFrame("loadingPage")

    # Start attempting to connect to the server
    thread = threading.Thread(target=connectServer, args=(app.frames["loadingPage"].widgets['errorLabel'], app))
    thread.start()

    app.root.mainloop()

    # Wait for the thread to join
    thread.join()

if __name__ == "__main__":
    startScreen()
