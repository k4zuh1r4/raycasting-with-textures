import pygame as pg
import math
import os
from collections import deque
from settings import *
class StaticSpriteHandler:
    def __init__(self, game, path='resources/sprites/static_sprites/BARREL_1.png', pos=(10.5,3.5), scale = 0.6, shift =0.27):
        self._game = game
        self._playerSprite = game._player
        self.x, self.y = pos
        self._spriteImage = pg.image.load(path).convert_alpha()
        self._spriteWidth = self._spriteImage.get_width()
        self._halfSpriteWidth = self._spriteImage.get_width()//2
        self._spriteRatio = self._spriteWidth/self._spriteImage.get_height()
        self.dx, self.dy, self._thetaAngle, self._screenSpriteX, self._spriteDistance, self._trueSpriteDistance = 0,0,0,0,1,1
        self._spriteScale = scale
        self._sprightHeightShift = shift
    def getSpriteProjection(self):
        projectionSprite = SCREEN_DISTANCE / self._spriteDistance*self._spriteScale # = projectionSpriteHeight
        projectionSpriteWidth,projectionSpriteHeight = (projectionSprite*self._spriteRatio),(projectionSprite) 
        transformedSpriteImage = pg.transform.scale(self._spriteImage,(projectionSpriteWidth,projectionSprite))
        heightShift = projectionSpriteHeight*self._sprightHeightShift
        spritePosition = (self._screenSpriteX - (projectionSpriteWidth//2)), ((HEIGHT//2) - projectionSprite//2 +heightShift)        
        self._game._rayCasting._renderingTarget.append((self._trueSpriteDistance,transformedSpriteImage,spritePosition))
    def getSprite(self):
        dx = self.x - self._playerSprite._playerPosX
        dy = self.y - self._playerSprite._playerPosY
        self.dx, self.dy = dx, dy
        self._thetaAngle = math.atan2(dy,dx)
        deltaSpriteAngle = self._thetaAngle - self._playerSprite._playerAngle
        if (dx > 0 and self._playerSprite._playerAngle > math.pi) or (dx <0 and dy<0):
            deltaSpriteAngle += math.tau
        deltaRays = deltaSpriteAngle/DELTA_ANGLE
        self._screenSpriteX = (RAY_AMOUNT//2 + deltaRays)* TEXTURE_SCALE
        self._spriteDistance = math.hypot(dx, dy)
        self._trueSpriteDistance =self._spriteDistance*math.cos(deltaSpriteAngle) #fishbowl removal.
        if -self._spriteWidth//2 < self._screenSpriteX < (WIDTH + self._halfSpriteWidth) and self._trueSpriteDistance > 0.5:
            self.getSpriteProjection()
    def spriteUpdate(self):
        self.getSprite()

class AnimatedSpritesHandler(StaticSpriteHandler):
    def __init__(self, game, path = 'resources/sprites/animated_sprites/green_light/0.png', pos =(14.5,3.5), scale = 0.8, shift = 0.15, animationTime = 120):
        super().__init__(game,path,pos,scale,shift)
        self._animationTime = animationTime
        self.path = path.rsplit('/',1)[0]
        self._AniSpriteImages = self.getAniSprite(self.path)
        self._animationPrevTicks = pg.time.get_ticks()
        self._animationTrigger = False
    def update(self):
        super().spriteUpdate()
        self.checkAnimationTime()
        self.animate(self._AniSpriteImages)
    def animate(self, images):
        if self._animationTrigger:
            images.rotate(-1)
            self.image = images[0]
    def checkAnimationTime(self):
        self._animationTrigger = False
        currentTime = pg.time.get_ticks()
        if (currentTime - self._animationPrevTicks) > self._animationTime:
            self._animationPrevTicks = currentTime
            self._animationTrigger = True
    def getAniSprite(self,path):
        sprites = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path+ '/' +file_name).convert_alpha()
                sprites.append(img)
        return sprites

        
