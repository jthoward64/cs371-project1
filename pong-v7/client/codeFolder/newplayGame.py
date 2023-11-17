import pygame
import tkinter as tk
import sys
import socket

from helperCode import *

# This is the main game loop.  For the most part, you will not need to modify this.  The sections
# where you should add to the code are marked.  Feel free to change any part of this project
# to suit your needs.
def playGame(screenWidth:int, screenHeight:int, playerPaddle:str, client:socket.socket, lInitial:str, rInitial:str) -> None:
    
    # Pygame inits
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()

    # Constants
    WHITE = (255,255,255)
    clock = pygame.time.Clock()
    scoreFont = pygame.font.Font("./assets/fonts/pong-score.ttf", 32)
    winFont = pygame.font.Font("./assets/fonts/visitor.ttf", 48)
    bottomFont = pygame.font.Font(None, 24)
    restartFont = pygame.font.Font(None, 32)
    pointSound = pygame.mixer.Sound("./assets/sounds/point.wav")
    bounceSound = pygame.mixer.Sound("./assets/sounds/bounce.wav")

    # Display objects
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    winMessage = pygame.Rect(0,0,0,0)

    topWall = pygame.Rect(-10,0,screenWidth+20, 10)
    bottomWall = pygame.Rect(-10, screenHeight-40, screenWidth+20, 10)

    bottomMessageSurface = bottomFont.render("Game Code: 0fmNq!", True, WHITE)
    bottomtargetRect = pygame.Rect(0, screenHeight - 40, screenWidth, 50)
    bottomtext_x = bottomtargetRect.x + (bottomtargetRect.width - bottomMessageSurface.get_width()) // 2
    bottomtext_y = bottomtargetRect.y + (bottomtargetRect.height - bottomMessageSurface.get_height()) // 2

    restartText = restartFont.render("Press 'r' to restart", True, WHITE)
    restartText_center = (screenWidth/2-100, screenHeight/2+30)
    restartHolder = pygame.Rect(0,0,0,0)

    waitingText = restartFont.render("Waiting on other player...", True, WHITE)
    waitingText_center = (screenWidth/2-125, screenHeight/2+30)

    leftTextScore = bottomFont.render(f"{lInitial}: 0", True, WHITE)
    leftText_x = 10
    leftText_y = bottomtargetRect.y + (bottomtargetRect.height - bottomMessageSurface.get_height()) // 2

    rightTextScore = bottomFont.render(f"{rInitial}: 0", True, WHITE)
    rightText_x = 100
    rightText_y = bottomtargetRect.y + (bottomtargetRect.height - bottomMessageSurface.get_height()) // 2

    centerLine = []
    for i in range(0, screenHeight-40, 10):
        centerLine.append(pygame.Rect((screenWidth/2)-5,i,5,5))

    # Paddle properties and init
    paddleHeight = 50
    paddleWidth = 10
    paddleStartPosY = (screenHeight/2)-(paddleHeight/2)
    leftPaddle = Paddle(pygame.Rect(10,paddleStartPosY, paddleWidth, paddleHeight))
    rightPaddle = Paddle(pygame.Rect(screenWidth-20, paddleStartPosY, paddleWidth, paddleHeight))

    ball = Ball(pygame.Rect(screenWidth/2, screenHeight/2, 5, 5), -5, 0)

    # Set to false when we're not running
    running = True
    restart = False

    if playerPaddle == "left":
        opponentPaddleObj = rightPaddle
        playerPaddleObj = leftPaddle
    else:
        opponentPaddleObj = leftPaddle
        playerPaddleObj = rightPaddle

    lScore = 0
    rScore = 0

    lWins = 0
    rWins = 0

    sync = 0

    while True:
        # Wiping the screen
        screen.fill((0,0,0))

        # Blit the bottomMessage
        gameMessage = screen.blit(bottomMessageSurface, (bottomtext_x, bottomtext_y)) 
        leftMessage = screen.blit(leftTextScore, (leftText_x, leftText_y))
        rightMessage = screen.blit(rightTextScore, (rightText_x, rightText_y))

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

                # Did we request to restart?
                elif event.key == pygame.K_r and running is False:
                    # Restart to True
                    restart = True

            elif event.type == pygame.KEYUP:
                playerPaddleObj.moving = ""


        # =========================================================================================
        # Your code here to send an update to the server on your paddle's information,
        # where the ball is and the current score.
        # Feel free to change when the score is updated to suit your needs/requirements
        
        # Only send an update if the game is currently running
        if running:
            pass
        
        # =========================================================================================

        # Update the player paddle and opponent paddle's location on the screen
        for paddle in [playerPaddleObj, opponentPaddleObj]:
            if paddle.moving == "down":
                if paddle.rect.bottomleft[1] < screenHeight-10:
                    paddle.rect.y += paddle.speed
            elif paddle.moving == "up":
                if paddle.rect.topleft[1] > 10:
                    paddle.rect.y -= paddle.speed

        # If the game is over, display the win message
        if lScore > 4 or rScore > 4 or running is False:
            # Add our win message
            winText = "Player 1 Wins! " if lScore > 4 else "Player 2 Wins! "
            textSurface = winFont.render(winText, False, WHITE, (0,0,0))
            textRect = textSurface.get_rect()
            textRect.center = ((screenWidth/2), screenHeight/2)
            winMessage = screen.blit(textSurface, textRect)

            # Add our message to restart the game
            running = False
            if not restart:
                restartHolder = screen.blit(restartText, restartText_center)
            else:
                restartHolder = screen.blit(waitingText, waitingText_center)

                ################################################################ SEND TO SERVERF "START GAME" REQUEST #################################################################
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
            
            pygame.draw.rect(screen, WHITE, ball)
            # ==== End Ball Logic =================================================================

        # Drawing the dotted line in the center
        if running is True:
            for i in centerLine:
                pygame.draw.rect(screen, WHITE, i)
        
        # Drawing the player's new location
        for paddle in [playerPaddleObj, opponentPaddleObj]:
            pygame.draw.rect(screen, WHITE, paddle)

        pygame.draw.rect(screen, WHITE, topWall)
        pygame.draw.rect(screen, WHITE, bottomWall)
        scoreRect = updateScore(lScore, rScore, screen, WHITE, scoreFont)
        pygame.display.update([topWall, bottomWall, ball, leftPaddle, rightPaddle, scoreRect, winMessage, gameMessage, restartHolder, leftMessage, rightMessage])
        clock.tick(60)
        
        # This number should be synchronized between you and your opponent.  If your number is larger
        # then you are ahead of them in time, if theirs is larger, they are ahead of you, and you need to
        # catch up (use their info)
        sync += 1
        # =========================================================================================
        # Send your server update here at the end of the game loop to sync your game with your
        # opponent's game

        # Only grab an update if the game is currently running
        if running:
            leftTextScore = bottomFont.render(f"{lInitial}: {lWins}", True, WHITE)
            rightTextScore = bottomFont.render(f"{rInitial}: {rWins}", True, WHITE)
            pass

        # =========================================================================================