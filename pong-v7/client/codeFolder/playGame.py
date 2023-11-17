# =================================================================================================
# Contributing Authors:	    <Juliann Hyatt,Anyone who touched the code>
# Email Addresses:          <jnhy222@uky.com Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import pygame

from .gameSetup import *
from .helperCode import *
from .sockethelper import Connection


# This is the main game loop.  For the most part, you will not need to modify this.  The sections
# where you should add to the code are marked.  Feel free to change any part of this project
# to suit your needs.
def playGame(
    screenWidth: int,
    screenHeight: int,
    playerPaddle: str,
    client: Connection,
) -> None:
    pygame.init()
    gameInt = gameInstance(screenWidth, screenHeight, playerPaddle, client)

    client.send({"request": "game_info"})
    game_info = client.recv()  # type: ignore
    if not game_info:
        print("Server Disconnected")
        pygame.quit()
        return
    game_code = game_info["message"].get("game_code", "Unknown Code")

    pygame.mixer.pre_init(44100, -16, 2, 2048)
    gameInt.currentPlayer = 1 if gameInt.playerPaddle == "left" else 2
    pygame.display.set_caption(f"Player: {gameInt.currentPlayer} - {game_code}")

    if gameInt.currentPlayer == 1:
        opponentPaddleObj = gameInt.rightPaddle
        playerPaddleObj = gameInt.leftPaddle
    else:
        opponentPaddleObj = gameInt.leftPaddle
        playerPaddleObj = gameInt.rightPaddle
    #FIXME wait for player 2
    client.send({"request":"start_game"})
    client.recv()

    
    playAgain = True
    while playAgain:
        playAgain = False
        lScore = 0
        rScore = 0
        sync = 0

        while True:
            # Wiping the screen
            gameInt.screen.fill((0, 0, 0))

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

            # Getting keypress events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    playAgain = False
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

            '''Update the Server using 'request' and information here'''
            newDict = {
                'request': 'update_game',
                'message': {
                    'Paddle': {
                        'X': playerPaddleObj.rect.x,
                        'Y': playerPaddleObj.rect.y,
                        'Moving': playerPaddleObj.moving
                    },
                    'score': {
                        'lScore':lScore,
                        'rScore':rScore,
                    },
                    'ball': {
                        'X': gameInt.ball.rect.x,
                        'Y': gameInt.ball.rect.y,
                        'xVel': gameInt.ball.xVel,
                        'yVel': gameInt.ball.yVel,
                    },
                    'sync': sync,
                }
            }
            client.send(newDict)
            
            # =========================================================================================

            # Update the player paddle and opponent paddle's location on the screen
            for paddle in [playerPaddleObj, opponentPaddleObj]:
                if paddle.moving == "down":
                    if paddle.rect.bottomleft[1] < gameInt.screenHeight - 10:
                        paddle.rect.y += paddle.speed
                elif paddle.moving == "up":
                    if paddle.rect.topleft[1] > 10:
                        paddle.rect.y -= paddle.speed

            # If the game is over, display the win message
            if lScore > 4 or rScore > 4:
                winText = "Player 1 Wins! " if lScore > 4 else "Player 2 Wins! "
                winText = winText + "\n P to Play Again"
                textSurface = gameInt.winFont.render(
                    winText, False, gameInt.WHITE, (0, 0, 0)
                )
                textRect = textSurface.get_rect()
                textRect.centerx = int(gameInt.screenWidth / 2)
                textRect.centery = int(gameInt.screenHeight / 2)
                gameInt.winMessage = gameInt.screen.blit(textSurface, textRect)
                for event in pygame.event.get():
                    if event.key == pygame.K_p:
                        gameInt.reset()
                        playAgain = True

                """ ---------------------------------------------------------------- Modify for Game Restart ---------------------------------------------------------------- """
            else:
                # ==== Ball Logic =====================================================================
                gameInt.ball.updatePos()

                # If the ball makes it past the edge of the screen, update score, etc.
                if gameInt.ball.rect.x > screenWidth:
                    lScore += 1
                    gameInt.pointSound.play()
                    gameInt.ball.reset(nowGoing="left")
                elif gameInt.ball.rect.x < 0:
                    rScore += 1
                    gameInt.pointSound.play()
                    gameInt.ball.reset(nowGoing="right")

                # If the ball hits a paddle
                if gameInt.ball.rect.colliderect(playerPaddleObj.rect):
                    gameInt.bounceSound.play()
                    gameInt.ball.hitPaddle(playerPaddleObj.rect.center[1])
                elif gameInt.ball.rect.colliderect(opponentPaddleObj.rect):
                    gameInt.bounceSound.play()
                    gameInt.ball.hitPaddle(opponentPaddleObj.rect.center[1])

                # If the ball hits a wall
                if gameInt.ball.rect.colliderect(
                    gameInt.topWall
                ) or gameInt.ball.rect.colliderect(gameInt.bottomWall):
                    gameInt.bounceSound.play()
                    gameInt.ball.hitWall()

                pygame.draw.rect(gameInt.screen, gameInt.WHITE, gameInt.ball.rect)
                # ==== End Ball Logic =================================================================

                # Drawing the dotted line in the center
                for i in gameInt.centerLine:
                    pygame.draw.rect(gameInt.screen, gameInt.WHITE, i)

                # Drawing the player's new location
                for paddle in [playerPaddleObj, opponentPaddleObj]:
                    pygame.draw.rect(gameInt.screen, gameInt.WHITE, paddle.rect)

                pygame.draw.rect(gameInt.screen, gameInt.WHITE, gameInt.topWall)
                pygame.draw.rect(gameInt.screen, gameInt.WHITE, gameInt.bottomWall)
                scoreRect = updateScore(
                    lScore, rScore, gameInt.screen, gameInt.WHITE, gameInt.scoreFont
                )
                pygame.display.update(
                    [
                        gameInt.topWall,
                        gameInt.bottomWall,
                        gameInt.ball.rect,
                        gameInt.leftPaddle.rect,
                        gameInt.rightPaddle.rect,
                        scoreRect,
                        gameInt.winMessage,
                    ]
                )
                gameInt.clock.tick(60)

                # This number should be synchronized between you and your opponent.  If your number is larger
                # then you are ahead of them in time, if theirs is larger, they are ahead of you, and you need to
                # catch up (use their info)
                sync += 1
            # =========================================================================================
            # Send your server update here at the end of the game loop to sync your game with your
            # opponent's game

            '''Use 'request' not Type'''
            client.send({'request':'grab_game'})

            msg = client.recv()
            if msg is None:
                # Error? Idk what to do here
                continue

            key = 'right_player' if gameInt.playerPaddle == 'right' else 'left_player'
            opponentPaddleObj.rect.y = msg[key]['Y']
            opponentPaddleObj.moving = msg[key]['Moving']
            lScore = msg['score']['lScore']
            rScore = msg['score']['rScore']
            gameInt.ball.rect.x = msg['ball']['X']
            gameInt.ball.rect.y = msg['ball']['Y']
            gameInt.ball.xVel = msg['ball']['xVel']
            gameInt.ball.yVel = msg['ball']['yVel']
            sync = msg['sync']
