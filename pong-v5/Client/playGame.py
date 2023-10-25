# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

from Helpers.connectionHandler import sendInfo, unpackInfo
from assets.code.helperCode import *
import pygame, socket

# This is the main game loop.  For the most part, you will not need to modify this.  The sections
# where you should add to the code are marked.  Feel free to change any part of this project
# to suit your needs.
def playGame(screenWidth: int, screenHeight: int, playerPaddle: str, client: socket.socket) -> None:
    # Pygame inits
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    
    # Set the currentPlayer to the correct playerPaddle
    currentPlayer = 1 if playerPaddle == "left" else 2
    pygame.display.set_caption(f"Player: {currentPlayer}")

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
                return
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
        """ Last Modified October 14th, 2023 ************************************************************************************************ """

        '''
        Example of Update
        
        update = {
            "Type": "Update",
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
        '''

        update = {
            "Type": "Update",
            "Paddle": {
                "Moving": playerPaddleObj.moving,
                "X": playerPaddleObj.rect.x,
                "Y": playerPaddleObj.rect.y,
            },
            "Score": {
                "lScore": lScore,
                "rScore": rScore,
            },
            "Ball": {
                "X": ball.rect.x,
                "Y": ball.rect.y,
            },
            "Sync": sync
        }

        success = sendInfo(client, update)
        if not success:
            # Add an option here in case it fails to send to the server
            pass

        """ Last Modified October 14th, 2023 ************************************************************************************************ """

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
            ''' ---------------------------------------------------------------- Modify for Game Restart ---------------------------------------------------------------- '''
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

        """ Last Modified October 14th, 2023 ************************************************************************************************ """

        success = sendInfo(client, {"Type": "Grab"})

        if not success:
            # What do we do when there isn't a success?
            # I suggest continue or looping until we get a success
            pass
        
        try:
            # Our updated information
            responsePackage = client.recv(512).decode()
        except ConnectionResetError:
            responsePackage = False

        # Did our server disconnect?
        if not responsePackage:
            print("Server Disconnected")
            pygame.quit()
            return

        # Try opening the JSON
        success, newInfo = unpackInfo(responsePackage)

        if not success:
            # Failed to unpack, skip because we can't grab info
            # Can also add a loop here to attempt again a few times
            continue
        
        '''
        Example of Update
        
        update = {
            "Type": "Grab",
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
        '''

        # Update opponent paddle information
        opponentPaddleObj.rect.x = newInfo["Paddle"]["X"]
        opponentPaddleObj.rect.y = newInfo["Paddle"]["Y"]
        opponentPaddleObj.moving =newInfo["Paddle"]["Moving"]

        # Check if we need to update the ball and score
        if newInfo["Sync"] > sync:
            ball.rect.x = newInfo["Ball"]["X"]
            ball.rect.y = newInfo["Ball"]["Y"]
            lScore = newInfo["Score"]["lScore"]
            rScore = newInfo["Score"]["rScore"]
            sync = newInfo["Sync"]

        """ Last Modified October 14th, 2023 ************************************************************************************************ """
