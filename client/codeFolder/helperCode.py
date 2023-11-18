# You don't need to edit this file at all unless you really want to
from typing import Literal, Optional

import pygame


# This draws the score to the screen
# had to cast textRect as int as it was reading as a float -JNH
def updateScore(
    lScore: int,
    rScore: int,
    screen: pygame.surface.Surface,
    color,
    scoreFont: pygame.font.Font,
) -> pygame.Rect:
    textSurface = scoreFont.render(f"{lScore}   {rScore}", False, color)
    textRect = textSurface.get_rect()
    screenWidth = screen.get_width()
    textRect.center = (int(screenWidth / 2) + 5, 50)
    return screen.blit(textSurface, textRect)


class Paddle:
    rect: pygame.Rect
    moving: Optional[Literal["up", "down"]]
    speed: int

    def __init__(self, rect: pygame.Rect) -> None:
        self.rect = rect
        self.moving = None
        self.speed = 5


class Ball:
    def __init__(self, rect: pygame.Rect, startXvel: int, startYvel: int) -> None:
        self.rect = rect
        self.xVel = startXvel
        self.yVel = startYvel
        self.startXpos = rect.x
        self.startYpos = rect.y

    def updatePos(self, deltaTime: int) -> None:
        self.rect.x += int(self.xVel * (deltaTime / 1000) * 60)
        self.rect.y += self.yVel

    def hitPaddle(self, paddleCenter: int) -> None:
        self.xVel *= -1
        self.yVel = (self.rect.center[1] - paddleCenter) // 3

    def hitWall(self) -> None:
        self.yVel *= -1

    def reset(self, nowGoing: str) -> None:
        # nowGoing  The direction the ball should be going after the reset
        self.rect.x = self.startXpos
        self.rect.y = self.startYpos
        self.xVel = -5 if nowGoing == "left" else 5
        self.yVel = 0
