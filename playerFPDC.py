from settings import *
import pygame as pg
import math
import time
class Player:
    def __init__(self, game):
        self.game = game
        self._playerPosX, self._playerPosY = PLAYER_POS
        self._playerAngle = PLAYER_ANGLE
        self.last_input_time = time.time()
    def movement(self):
        current_time = time.time()
        if current_time - self.last_input_time >= 0.1:
            dx, dy = 0, 0
            _movementEvent = pg.key.get_pressed()          
            if _movementEvent[pg.K_w]:
                dx += round(math.cos(self._playerAngle))
                dy += round(math.sin(self._playerAngle))
            elif _movementEvent[pg.K_s]:
                dx += round(-math.cos(self._playerAngle))
                dy += round(-math.sin(self._playerAngle))
            elif _movementEvent[pg.K_LEFT]:
                self._playerAngle -= math.radians(90)
            elif _movementEvent[pg.K_RIGHT]:
                self._playerAngle += math.radians(90)
            self._playerAngle %= math.tau
            self.collisionCheck(dx, dy)
            self.last_input_time = current_time
    def wallCheck(self, x, y):
        return False if (x, y) in self.game._map._convertedMap else True
    def collisionCheck(self, dx, dy):
        hitboxLimitScale = PLAYER_SIZE_SCALE / self.game._deltaTime
        if self.wallCheck(int(self._playerPosX + dx*hitboxLimitScale), int(self._playerPosY)):
            self._playerPosX += dx
        if self.wallCheck(int(self._playerPosX), int(self._playerPosY + dy*hitboxLimitScale)):
            self._playerPosY += dy
    def playerDraw(self):
        pg.draw.line(self.game._screen, 'green',(self._playerPosX*100, self._playerPosY*100),
                     ((self._playerPosX*100 + WIDTH*math.cos(self._playerAngle)),(self._playerPosY*100 + WIDTH*math.sin(self._playerAngle))), 2)
        pg.draw.circle(self.game._screen, 'yellow',(self._playerPosX*100, self._playerPosY*100), 15)
    def movementUpdate(self):
        self.movement()
    @property
    def pos(self):
        return self._playerPosX, self._playerPosY 
    @property
    def mapPos(self):
        return int(self._playerPosX), int(self._playerPosY)