# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import pygame

from .helperCode import *
from .sockethelper import Connection


# This is the main game loop.  For the most part, you will not need to modify this.  The sections
# where you should add to the code are marked.  Feel free to change any part of this project
# to suit your needs.
def playGame(screenWidth: int, screenHeight: int, client: Connection) -> None:
    # Pygame inits
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()

    # Set to spectator mode
    pygame.display.set_caption(f"Currently Spectating")

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

    lScore = 0
    rScore = 0

    while True:
        # Wiping the screen
        screen.fill((0, 0, 0))

        # Getting keypress events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Update the player paddle and opponent paddle's location on the screen
        for paddle in [rightPaddle, leftPaddle]:
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
            if ball.rect.colliderect(leftPaddle.rect):
                bounceSound.play()
                ball.hitPaddle(leftPaddle.rect.center[1])
            elif ball.rect.colliderect(rightPaddle.rect):
                bounceSound.play()
                ball.hitPaddle(rightPaddle.rect.center[1])

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
        for paddle in [leftPaddle, rightPaddle]:
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

        if not client.send({"Type": "Spectator"}):
            print("Server Disconnected")
            pygame.quit()
            return

        newInfo = client.recv()

        if not newInfo:
            # Failed to unpack, skip because we can't grab info
            # Can also add a loop here to attempt again a few times
            continue

        """
        Example of Update
        
        update = {
            "Type": "Spectator",
            "Paddle": {
                "Moving":"",
                "X": 0,
                "Y": 1,
            }
            "Score": {
                "lScore":0,
                "rScore":0,
            }
            "Ball": {
                "X":0,
                "Y":0,
            }
            "Sync": 0,
        }
        """

        # Update paddle information
        leftPaddle.rect.x = newInfo["lPaddle"]["X"]
        leftPaddle.rect.y = newInfo["lPaddle"]["Y"]
        leftPaddle.moving = newInfo["lPaddle"]["moving"]
        rightPaddle.rect.x = newInfo["rPaddle"]["X"]
        rightPaddle.rect.y = newInfo["rPaddle"]["Y"]
        rightPaddle.moving = newInfo["rPaddle"]["Moving"]

        # Update ball and score information
        ball.rect.x = newInfo["Ball"]["X"]
        ball.rect.y = newInfo["Ball"]["Y"]
        lScore = newInfo["Score"]["lScore"]
        rScore = newInfo["Score"]["rScore"]