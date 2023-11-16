# =================================================================================================
# Contributing Authors:	    <Juliann Hyatt,Anyone who touched the code>
# Email Addresses:          <jnhy222@uky.com Your uky.edu email addresses>
# Date:                     <11-12-2023>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================


import socket
import pygame
from .helperCode import *
from .sockethelper import Connection

class gameInstance:
    def __init__(self,screenWidth: int, screenHeight: int, playerPaddle: str, client: Connection):
        self.isBuilt = 0
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.playerPaddle = playerPaddle
        self.client = client     
        #These are initialized during game setup
        self.currentPlayer = 0
        # Constants
        self.WHITE = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.scoreFont = pygame.font.Font("./assets/fonts/pong-score.ttf", 32)
        self.winFont = pygame.font.Font("./assets/fonts/visitor.ttf", 48)
        self.pointSound = pygame.mixer.Sound("./assets/sounds/point.wav")
        self.bounceSound = pygame.mixer.Sound("./assets/sounds/bounce.wav")
        # Display objects
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        self.winMessage = pygame.Rect(0, 0, 0, 0)
        self.topWall = pygame.Rect(-10, 0, screenWidth + 20, 10)
        self.bottomWall = pygame.Rect(-10, screenHeight - 10, screenWidth + 20, 10)
        self.centerLine = []
        for i in range(0, screenHeight, 10):
            self.centerLine.append(pygame.Rect((screenWidth / 2) - 5, i, 5, 5))
        # Paddle properties and init
        self.paddleHeight = 50
        self.paddleWidth = 10
        self.paddleStartPosY = (screenHeight / 2) - (self.paddleHeight / 2)
        self.leftPaddle = Paddle(pygame.Rect(10, self.paddleStartPosY, self.paddleWidth, self.paddleHeight))
        self.rightPaddle = Paddle(
            pygame.Rect(screenWidth - 20, self.paddleStartPosY, self.paddleWidth, self.paddleHeight)
        )
        self.ball = Ball(pygame.Rect(screenWidth / 2, screenHeight / 2, 5, 5), -5, 0) 
        self.isBuilt = 1
        
        
        # Author:      Juliann Hyatt
        # Purpose:     Reset game instance to original state
        # Pre:         Assumes conclusion of game reached
        # Post:        resets gameInstance for play again
        
    def reset(self) :
        self.isBuilt = 0
        #These are initialized during game setup
        self.currentPlayer = 0
        # Constants
        self.WHITE = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.paddleStartPosY = (self.screenHeight / 2) - (self.paddleHeight / 2)
        self.leftPaddle = Paddle(pygame.Rect(10, self.paddleStartPosY, self.paddleWidth, self.paddleHeight))
        self.rightPaddle = Paddle(
            pygame.Rect(self.screenWidth - 20, self.paddleStartPosY, self.paddleWidth, self.paddleHeight)
        )
        self.ball = Ball(pygame.Rect(self.screenWidth / 2, self.screenHeight / 2, 5, 5), -5, 0) 
        self.isBuilt = 1
