# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import pygame
import tkinter as tk
import sys
import socket
import json

from assets.code.helperCode import *


# This is the main game loop.  For the most part, you will not need to modify this.  The sections
# where you should add to the code are marked.  Feel free to change any part of this project
# to suit your needs.
def playGame(
    screenWidth: int, screenHeight: int, playerPaddle: str, client: socket.socket
) -> None:
    # Pygame inits
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()

    # Constants
    WHITE = (255, 255, 255)
    clock = pygame.time.Clock()
    scoreFont = pygame.font.Font("./assets/fonts/pong-score.ttf", 32)
    winFont = pygame.font.Font("./assets/fonts/visitor.ttf", 48)
    pointSound = pygame.mixer.Sound("./assets/sounds/point.wav")
    bounceSound = pygame.mixer.Sound("./assets/sounds/bounce.wav")

    # Display objects
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    winMessage = pygame.Rect(0, 0, 0, 0)
    topWall = pygame.Rect(-10, 0, screenWidth + 20, 10)
    bottomWall = pygame.Rect(-10, screenHeight - 10, screenWidth + 20, 10)
    centerLine = []
    for i in range(0, screenHeight, 10):
        centerLine.append(pygame.Rect((screenWidth / 2) - 5, i, 5, 5))

    # Paddle properties and init
    paddleHeight = 50
    paddleWidth = 10
    paddleStartPosY = (screenHeight / 2) - (paddleHeight / 2)
    leftPaddle = Paddle(pygame.Rect(10, paddleStartPosY, paddleWidth, paddleHeight))
    rightPaddle = Paddle(
        pygame.Rect(screenWidth - 20, paddleStartPosY, paddleWidth, paddleHeight)
    )

    ball = Ball(pygame.Rect(screenWidth / 2, screenHeight / 2, 5, 5), -5, 0)

    if playerPaddle == "left":
        opponentPaddleObj = rightPaddle
        playerPaddleObj = leftPaddle
    else:
        opponentPaddleObj = leftPaddle
        playerPaddleObj = rightPaddle

    lScore = 0
    rScore = 0

    sync = 0

    while True:
        # Wiping the screen
        screen.fill((0, 0, 0))

        # Getting keypress events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    playerPaddleObj.moving = "down"

                elif event.key == pygame.K_UP:
                    playerPaddleObj.moving = "up"

            elif event.type == pygame.KEYUP:
                playerPaddleObj.moving = ""

        # =========================================================================================
        # Your code here to send an update to the server on your paddle's information,
        # where the ball is and the current score.
        # Feel free to change when the score is updated to suit your needs/requirements

        """ Last Modified October 8th, 2023 ************************************************************************************************ """

        """
            Notes:
            1) Look up playerPaddleObj
            2) What is the variable holding the position of the ball
            3) What is the current score variable
            4) Remember syncing
        """

        informationToSend = {
            # Type of Information: 0 = Game Start, 1 = Update Game, 2 = Server Update
            "Request": 1,
            # Paddle Information
            "paddleX": playerPaddleObj.rect.x,
            "paddleY": playerPaddleObj.rect.y,
            "paddleMoving": playerPaddleObj.moving,
            # Ball Information
            "ballX": ball.rect.x,
            "ballY": ball.rect.y,
            # Score Information
            "scoreLeft": lScore,
            "scoreRight": rScore,
            # Sync Status
            "sync": sync,
        }

        # Bundle it into JSON
        packageDump = json.dumps(informationToSend).encode()

        # Send the information
        try:
            client.send(packageDump)
        except socket.error as errorMessage:
            print(f"Error on client update to server: {errorMessage}")

        """ Last Modified October 8th, 2023 ************************************************************************************************ """

        # =========================================================================================

        # Update the player paddle and opponent paddle's location on the screen
        for paddle in [playerPaddleObj, opponentPaddleObj]:
            if paddle.moving == "down":
                if paddle.rect.bottomleft[1] < screenHeight - 10:
                    paddle.rect.y += paddle.speed
            elif paddle.moving == "up":
                if paddle.rect.topleft[1] > 10:
                    paddle.rect.y -= paddle.speed

        # If the game is over, display the win message
        if lScore > 4 or rScore > 4:
            winText = "Player 1 Wins! " if lScore > 4 else "Player 2 Wins! "
            textSurface = winFont.render(winText, False, WHITE, (0, 0, 0))
            textRect = textSurface.get_rect()
            textRect.centerx = int(screenWidth / 2)
            textRect.centery = int(screenHeight / 2)
            winMessage = screen.blit(textSurface, textRect)
        else:
            # ==== Ball Logic =====================================================================
            ball.updatePos()

            # If the ball makes it past the edge of the screen, update score, etc.
            if ball.rect.x > screenWidth:
                lScore += 1
                pointSound.play()
                ball.reset(nowGoing="left")
            elif ball.rect.x < 0:
                rScore += 1
                pointSound.play()
                ball.reset(nowGoing="right")

            # If the ball hits a paddle
            if ball.rect.colliderect(playerPaddleObj.rect):
                bounceSound.play()
                ball.hitPaddle(playerPaddleObj.rect.center[1])
            elif ball.rect.colliderect(opponentPaddleObj.rect):
                bounceSound.play()
                ball.hitPaddle(opponentPaddleObj.rect.center[1])

            # If the ball hits a wall
            if ball.rect.colliderect(topWall) or ball.rect.colliderect(bottomWall):
                bounceSound.play()
                ball.hitWall()

            pygame.draw.rect(screen, WHITE, ball.rect)
            # ==== End Ball Logic =================================================================

        # Drawing the dotted line in the center
        for i in centerLine:
            pygame.draw.rect(screen, WHITE, i)

        # Drawing the player's new location
        for paddle in [playerPaddleObj, opponentPaddleObj]:
            pygame.draw.rect(screen, WHITE, paddle.rect)

        pygame.draw.rect(screen, WHITE, topWall)
        pygame.draw.rect(screen, WHITE, bottomWall)
        scoreRect = updateScore(lScore, rScore, screen, WHITE, scoreFont)
        pygame.display.update(
            [
                topWall,
                bottomWall,
                ball.rect,
                leftPaddle.rect,
                rightPaddle.rect,
                scoreRect,
                winMessage,
            ]
        )
        clock.tick(60)

        # This number should be synchronized between you and your opponent.  If your number is larger
        # then you are ahead of them in time, if theirs is larger, they are ahead of you, and you need to
        # catch up (use their info)
        sync += 1
        # =========================================================================================
        # Send your server update here at the end of the game loop to sync your game with your
        # opponent's game

        # Inform the server we want an update
        client.send(json.dumps({"Request": 2}).encode())

        # Our updated information
        responsePackage = client.recv(512).decode()

        # Did our server disconnect?
        if not responsePackage:
            print("Server Disconnected")
            pygame.quit()
            exit()

        # Try opening the JSON
        try:
            newInfo = json.loads(responsePackage)
        except json.JSONDecodeError:
            print("Error failed to grab Server Info using Request 2")
            continue

        """Opponent Information Example
        
        newInfo = {
            # Type of Information: 0 = Game Start, 1 = Update Game, 2 = Server Update
            'Request': 3,

            # Did the opponent quit?
            'exitStatus': False,
            
            # Paddle Information
            'paddleX': opponentPaddleObj.rect.x,
            'paddleY': opponentPaddleObj.rect.y,
            'paddleMoving': opponentPaddleObj.moving,

            # Ball Information
            'ballX': ball.rect.x,
            'ballY': ball.rect.y,
            
            # Score Information
            'scoreLeft':lScore,
            'scoreRight':rScore,
            
            # Sync Status
            'sync':sync
        }
        
        """

        '''################################ MODIFY FOR WHEN OPPONENT EXIT (exitStatus) ################################'''
        if newInfo["exitStatus"] == True:
            print("Opponent Quit")
            pygame.quit()
            exit()
        '''################################ MODIFY FOR WHEN OPPONENT EXIT (exitStatus) ################################'''
        
        # Update opponent paddle information
        opponentPaddleObj.rect.x = newInfo["paddleX"]
        opponentPaddleObj.rect.y = newInfo["paddleY"]
        opponentPaddleObj.moving = newInfo["paddleMoving"]

        # Check if we need to update the ball and score
        if newInfo["sync"] > sync:
            ball.rect.x = newInfo["ballX"]
            ball.rect.y = newInfo["ballY"]
            lScore = newInfo["scoreLeft"]
            rScore = newInfo["scoreRight"]
            sync = newInfo["sync"]

        # =========================================================================================
