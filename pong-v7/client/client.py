# =================================================================================================
# Contributing Authors:	    Tag Howard, John Michael Stacy, Juliann Hyatt
# Email Addresses:          jtho264@uky.edu, jmst231@uky.edu, jnhy222@uky.edu
# Date:                     November 7th, 2023
# Purpose:                  Main Function
# Misc:
# =================================================================================================

# Our user interface
from codeFolder.interface import MainWindow

import threading as th

# Our game interface for players
#from code.gameplay import Game

# Our spectate interface for spectators
#from code.spectate import Spectator

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()