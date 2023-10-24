# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

from newpong.handler.appHandler import *
from pongClient import loginServer, mainMenu, makeAccount, accountMenu

def loginScreen(app:mainApp) -> frameHolder:
    # Create our Frame
    # def __init__(self:object, app:object, name:str, widgets:dict):
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
    # def __init__(self:object, app:object, name:str, widgets:dict):
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
    # def __init__(self:object, app:object, name:str, widgets:dict):
    mainFrame = frameHolder(app.root, app, "loadingPage")

    # Load our Image into mainFrame
    mainFrame.createPhoto(widgetName='Photo', filePath='./assets/images/logo.png', setColumn=0, setRow=0, setSticky='nsew', setColumnspan=2)

    # Create our two labels for username and password
    mainFrame.createLabel(widgetName='gameWait', setText='Connecting to Server', setColumn=0, setRow=1, setColumnspan=2, setSticky='EW', setPadx=2)
    
    # Create our errorLabel
    mainFrame.createLabel(widgetName='errorLabel',setColumn=0, setRow=2, setColumnspan=2)
    
    return mainFrame