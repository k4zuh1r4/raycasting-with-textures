from settings import *
import pygame as pg
import math
class Player:
    def __init__(self, game):
        self.game = game
        self._playerPosX, self._playerPosY = PLAYER_POS
        self._playerAngle = PLAYER_ANGLE
        self.playerSpeed = PLAYER_SPEED * self.game._deltaTime
        self._shotState = False
        self._playerHealth = 100
    def checkPlayerState(self):
        if self._playerHealth < 1:
            self.game._textureHandling.gameOverScreen()
            pg.time.delay(5000)
            self.game.gameLoad()
    def receiveDamage(self, damage):
        self._playerHealth -= damage
        self.game._soundHandler._playerDamage.play()
        self.checkPlayerState()
    def fireSingleEvent(self,event):
        if event.type == pg.MOUSEBUTTONDOWN:            
            if event.button == 1 and self._shotState == False and self.game._weapon._reloadState == False:            
                self.game._soundHandler._shotgunSFX.play()
                self._shotState = True            
                self.game._weapon._reloadState = True
    def movement(self):
        dx, dy = 0,0
        playerSpeed = PLAYER_SPEED * self.game._deltaTime
        _movementEvent = pg.key.get_pressed()
        speedCos = playerSpeed * math.cos(self._playerAngle)
        speedSin = playerSpeed * math.sin(self._playerAngle)
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
        #if  _movementEvent[pg.K_LEFT]:
            #self._playerAngle -= self.game._deltaTime*PLAYER_ROTATION_SPEED
        #if  _movementEvent[pg.K_RIGHT]:
            #self._playerAngle += self.game._deltaTime*PLAYER_ROTATION_SPEED
        self._playerAngle %= math.tau #2*pi                                                 
        self.collisionCheck(dx,dy)
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
    def mouseSupport(self):
        mouseX, mouseY = pg.mouse.get_pos()
        if mouseX < MOUSE_LEFT_BORDER or mouseX > MOUSE_RIGHT_BORDER:
            pg.mouse.set_pos([WIDTH//2, HEIGHT//2])
        self._deltaMovement = pg.mouse.get_rel()[0]
        self._deltaMovement = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self._deltaMovement))
        self._playerAngle += self._deltaMovement*MOUSE_SENSITIVITY*self.game._deltaTime
    def movementUpdate(self):
        self.movement()
        self.mouseSupport()
    @property
    def pos(self):
        return self._playerPosX, self._playerPosY 
    @property
    def mapPos(self):
        return int(self._playerPosX), int(self._playerPosY)


