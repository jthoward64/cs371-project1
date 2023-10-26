# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

from Helpers.appHandler import *
from Client.pongClient import loginServer, mainMenu, makeAccount, accountMenu

def loginScreen(app:mainApp) -> frameHolder:
    # Create our Frame
    # def __init__(self:object, app:object, name:str):
    mainFrame = frameHolder(app.root, app, "loginScreen")

    # Load our Image into mainFrame
    mainFrame.createPhoto(widgetName='Photo',filePath='./assets/images/logo.png', setColumn=0, setRow=0, setSticky='nsew', setColumnspan=2)

    # Create our two labels for username and password
    mainFrame.createLabel(widgetName='labelUsername',setText='Username', setColumn=0, setRow=1, setSticky='E', setPadx=2)
    mainFrame.createLabel(widgetName='labelPassword',setText='Passsword', setColumn=0, setRow=2, setSticky='E', setPadx=2)

    # Grab our entry boxes
    username = mainFrame.createBox(widgetName='username', setColumn=1, setRow=1, setSticky='E')
    password = mainFrame.createBox(widgetName='password', setColumn=1, setRow=2, setSticky='E')
    
    # Create our errorLabel
    errorLabel = mainFrame.createLabel(widgetName='errorLabel',setColumn=0, setRow=5, setColumnspan=2)

    # Our Login Button
    mainFrame.createButton(widgetName='loginButton',commandFunction=loginServer, setText='Login', argsList=[username.get(), password.get(), errorLabel, app.root, app], setColumn=0, setRow=3, setColumnspan=2)

    # Our Create Account Button
    mainFrame.createButton(widgetName='createAccountButton',commandFunction=accountMenu, setText='Create Account', argsList=[app], setColumn=0, setRow=4, setColumnspan=2)

    return mainFrame

def accountCreation(app:mainApp) -> frameHolder:
    # Create our Frame
    # def __init__(self:object, app:object, name:str):
    mainFrame = frameHolder(app.root, app, "accountCreation")

    # Load our Image into mainFrame
    mainFrame.createPhoto(widgetName='Photo', filePath='./assets/images/logo.png', setColumn=0, setRow=0, setSticky='nsew', setColumnspan=2)

    # Create our two labels for username and password
    mainFrame.createLabel(widgetName='checkUsername', setText='New Username', setColumn=0, setRow=1, setSticky='E', setPadx=2)
    mainFrame.createLabel(widgetName='checkPassword',setText='Passsword', setColumn=0, setRow=2, setSticky='E', setPadx=2)
    mainFrame.createLabel(widgetName='confirmPassword',setText='Confirm Passsword', setColumn=0, setRow=3, setSticky='E', setPadx=2)

    # Grab our entry boxes
    username = mainFrame.createBox(widgetName='username', setColumn=1,setRow=1,setSticky='E')
    password = mainFrame.createBox(widgetName='password',setColumn=1,setRow=2,setSticky='E')
    passwordConfirm = mainFrame.createBox(widgetName='confirm',setColumn=1,setRow=3,setSticky='E')
    
    # Create our errorLabel
    errorLabel = mainFrame.createLabel(widgetName='errorLabel',setColumn=0, setRow=6, setColumnspan=2)

    # Our Login Button
    mainFrame.createButton(commandFunction=makeAccount, setText='Register', argsList=[username.get(), password.get(), passwordConfirm.get(), errorLabel, app.root, app], setColumn=0, setRow=4, setColumnspan=2)

    mainFrame.createButton(commandFunction=mainMenu, setText='Back', argsList=[app], setColumn=0, setRow=5, setColumnspan=2)
    
    return mainFrame

def loadingPage(app:mainApp) -> frameHolder:
    # Create our Frame
    # def __init__(self:object, app:object, name:str):
    mainFrame = frameHolder(app.root, app, "loadingPage")

    # Load our Image into mainFrame
    mainFrame.createPhoto(widgetName='Photo', filePath='./assets/images/logo.png', setColumn=0, setRow=0, setSticky='nsew', setColumnspan=2)

    # Create our two labels for username and password
    mainFrame.createLabel(widgetName='gameWait', setText='Connecting to Server', setColumn=0, setRow=1, setColumnspan=2, setSticky='EW', setPadx=2)
    
    # Create our errorLabel
    mainFrame.createLabel(widgetName='errorLabel',setColumn=0, setRow=2, setColumnspan=2)
    
    return mainFrame


### TO DO ###

# 1. Create a Frame for the List of Game Instances we can join
# Can simply be a Scrolling Frame (scrollable) with a list of Game Instances in Grid Pattern
# Two Buttons "Join Game" and "Spectate" on each Game Instances
# Reload Scrolling Frame with refreshed Instances using a "Refresh" button.
# When you click "Join Game" or "Spectate" and the Instance no longer exists, configure the errorLabel to say something like "Game Full"
'''
    Note: We will need a Canvas inside the Frame to enable a scrollable section.
    tk.Canvas
    tk.Scrollbar

    Makeup Diagram:

    -> App
        -> instancePage
            -> Canvas
                -> innerFrame
                    -> instanceFrame
                        -> Attribute: gameInstanceID, Grid Location or (X/Y)
                        -> Instance Name Label, Join Button, Spectate Button
                    -> instanceFrame
                        -> Attribute: gameInstanceID, Grid Location or (X/Y)
                        -> Instance Name Label, Join Button, Spectate Button
                    -> instanceFrame
                        -> Attribute: gameInstanceID, Grid Location (or X/Y)
                        -> Instance Name Label, Join Button, Spectate Button
                    ...
'''
def instancePage(app:mainApp) -> frameHolder:
    # Create a Frame
    # def __init__(self:object, app:object, name:str)
    mainFrame = frameHolder(app.root, app, "instancePage")

    return mainFrame

# 2. Create a button in Client's playGame and spectateGame for "Replay" and "Exit". "Exit" should be in both playGame and spectateGame. "Replay" should only be in playGame.
# When both clients are ready to replay, turn their replay's off and restart the game. Possibly use a threading event?
'''-----------------------------Need to complete in playGame.py and spectateGame.py-----------------------------------
    Suggestions:
        Revamp and Modify playGame.py and spectateGame.py to be more efficient/optimized to current solution.
        Add Reply and Exit as needed to both files.
        On click button, send server a request to replay.
        Make sure to gracefully exit the Pygame Window and return to Tkinter "instancePage" in the event that a player client exits the game
'''