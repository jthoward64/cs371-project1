# Our user interface
from code.interface import MainWindow

import threading as th

# Our game interface for players
#from code.gameplay import Game

# Our spectate interface for spectators
#from code.spectate import Spectator

    

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()