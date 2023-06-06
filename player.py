from settings import *
import pygame as pg
import math
class Player:
    def __init__(self, game):
        self.game = game
        self._playerPosX, self._playerPosY = PLAYER_POS
        self._playerAngle = PLAYER_ANGLE        
    def movement(self):
        dx, dy = 0,0
        playerSpeed = PLAYER_SPEED * self.game._deltaTime
        speedCos = playerSpeed * math.cos(self._playerAngle)
        speedSin = playerSpeed * math.sin(self._playerAngle)
        _movementEvent = pg.key.get_pressed()
        if  _movementEvent[pg.K_w]:           
            dx +=speedCos                                                         
            dy +=speedSin                   
        if  _movementEvent[pg.K_s]:          
            dx += -speedCos                                                          
            dy += -speedSin                                
        if  _movementEvent[pg.K_a]:                                                
            dx += -speedCos                                                                 
            dy += speedSin                                           
        if  _movementEvent[pg.K_d]:
            dx += speedCos                                                      
            dy += -speedSin       
        self.collisionCheck(dx,dy)
        if  _movementEvent[pg.K_LEFT]:           
            self._playerAngle -= PLAYER_ROTATION_SPEED * self.game._deltaTime        
        if  _movementEvent[pg.K_RIGHT]:                          
            self._playerAngle += PLAYER_ROTATION_SPEED * self.game._deltaTime
        self._playerAngle %= math.tau #2*pi
    def wallCheck(self, x,y):
        return False if (x,y) in self.game._map._convertedMap else True #return False and disallow player to go through wall when touched the wall coords
    def collisionCheck(self,dx,dy):
        if self.wallCheck(int(self._playerPosX + dx),int(self._playerPosY)): #checks for wall in x dimension       
            self._playerPosX += dx 
        if self.wallCheck(int(self._playerPosX), int(self._playerPosY+ dy)): #checks for wall in y dimension     
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


