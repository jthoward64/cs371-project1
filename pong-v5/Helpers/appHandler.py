# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

from typing import Dict, Optional, List, Callable, Union
from tkinter import Widget
import tkinter as tk
import socket

class mainApp:
    def __init__(self) -> None:
        # Create our root and title
        self.root:tk.Tk = tk.Tk()
        self.root.title("Pong Game")

        # Holds our frames
        self.frames:Dict[str, frameHolder] = {}

        # Our client
        self.client:Optional[socket.socket] = None

        # What is our current frame?
        self.activeFrame:Optional[str] = None

    def centerResize(self, screenWidth:int, screenHeight:int) -> None:
        # Update the window to fit its content
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        # For centering
        self.CenterX = int(self.root.winfo_screenwidth()/2 - self.screenWidth/2)
        self.CenterY = int(self.root.winfo_screenheight()/2 - self.screenHeight/2)

        # Center the Window
        self.root.geometry(f'{self.screenWidth}x{self.screenHeight}+{self.CenterX}+{self.CenterY}')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Show our window
        self.root.deiconify()

    def changeFrame(self, frameName:str) -> None:
        # Ensure that our next frame exists
        if frameName not in self.frames:
            print(f'Error: {frameName} is not a frame in app.')
            return
        
        # Hide our Window
        self.root.withdraw()
        
        # Hide our active frame if it exists
        if self.activeFrame:
            # Hide the active frame
            self.frames[self.activeFrame].frame.grid_forget()
        
        # Show our next frame
        self.frames[frameName].frame.grid(sticky="nsew", column=0, row=0)
        screenWidth = self.frames[frameName].frame.winfo_reqwidth()
        screenHeight = self.frames[frameName].frame.winfo_reqheight()

        # Set to the activeFrame
        self.activeFrame = frameName

        # Resize and Center Frame
        self.centerResize(screenWidth, screenHeight)


class frameHolder:
    def __init__(self, parent:Union[tk.Tk, tk.Frame], app:mainApp, name:str) -> None:
        # Name of our Frame
        self.name = name

        # Our image
        self.images:List[tk.PhotoImage] = []

        # Our Frame Root
        self.frame:tk.Frame = tk.Frame(parent)
        self.app:mainApp = app

        # Hold our Widgets
        self.widgets:Dict[str, Widget] = {}

        # Add our frame object to the app
        if name not in app.frames:
            app.frames[name] = self
        else:
            print(f'Error, {name} already exist as a frame!')

    def createLabel(self, widgetName:str='', setText:str='', setColumn:int=0, setRow:int=0, setSticky:str='', setColumnspan:int=1, setPadx:int=0) -> tk.Label:
        # Create a Label to hold our Text
        newLabel = tk.Label(self.frame, text=setText)

        # Select our Grid Layout
        newLabel.grid(column=setColumn, row=setRow, sticky=setSticky, columnspan=setColumnspan, padx=setPadx)

        # Add to our wdigets
        self.widgets[widgetName] = newLabel
        return newLabel

    def createPhoto(self, widgetName:str='', filePath:str='', setColumn:int=0, setRow:int=0, setSticky:str='', setColumnspan:int=1) -> tk.Label:
        # Grab the Image File
        newImage = tk.PhotoImage(file=filePath)
        self.images.append(newImage)

        # Create a Label to Hold the Image
        newLabel = tk.Label(self.frame, image=newImage)

        # Select our Grid Layout
        newLabel.grid(column=setColumn, row=setRow, sticky=setSticky, columnspan=setColumnspan)

        # Add to our widgets
        self.widgets[widgetName] = newLabel
        return newLabel
                                                                                    #[username.get(), password.get(), passwordConfirm.get(), errorLabel, app.root, app]
    def createButton(self, widgetName:str='', commandFunction:Optional[Callable]=None, setText:str='', argsList:List[Union[str, int, tk.Label, tk.Tk, mainApp]]=[], setColumn:int=0, setRow:int=0, setSticky:str='', setColumnspan:int=1) -> tk.Button:
        # Create the Button
        newButton = tk.Button(
            self.frame,
            text=setText,
            command=lambda: commandFunction(*argsList) if commandFunction else None
        )

        # Select our Grid Layout
        newButton.grid(column=setColumn, row=setRow, sticky=setSticky, columnspan=setColumnspan)
        
        # Add to our widgets
        self.widgets[widgetName] = newButton
        return newButton

    def createBox(self, widgetName:str='', setColumn:int=0, setRow:int=0, setSticky:str='', setColumnspan:int=1) -> tk.Entry:
        # Create the entry box
        newEntry = tk.Entry(self.frame)

        # Select our Grid Layout
        newEntry.grid(column=setColumn, row=setRow, sticky=setSticky, columnspan=setColumnspan)

        # Add to our widgets
        self.widgets[widgetName] = newEntry
        return newEntry
    


    