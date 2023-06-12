import pygame as pg
from settings import *
import os
from collections import deque
class StaticSprite:
    def __init__(self, game, path, pos, scale=0.7, shift=0.27):
        self.game = game
        self.player = game._player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screenX, self.dist, self.normalDist = 0, 0, 0, 0, 1, 1
        self.spriteHalfWidth = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift
    def getSpriteProjection(self):
        projectionSprite = SCREEN_DISTANCE / self.normalDist * self.SPRITE_SCALE
        projectionSpriteWidth, projectionSpriteHeight = projectionSprite * self.IMAGE_RATIO, projectionSprite
        image = pg.transform.scale(self.image, (projectionSpriteWidth, projectionSpriteHeight))
        self.spriteHalfWidth = projectionSprite // 2
        heightShift = projectionSpriteHeight * self.SPRITE_HEIGHT_SHIFT
        pos = self.screenX - self.spriteHalfWidth, HEIGHT//2 - projectionSpriteHeight // 2 + heightShift
        self.game._rayCasting._renderingTarget.append((self.normalDist, image, pos))
    def getSprite(self):
        dx = self.x - self.player._playerPosX
        dy = self.y - self.player._playerPosY
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player._playerAngle
        if (dx > 0 and self.player._playerAngle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau
        deltaRays = delta / DELTA_ANGLE
        self.screenX = ((RAY_AMOUNT//2) + deltaRays) * TEXTURE_SCALE
        self.dist = math.hypot(dx, dy)
        self.normalDist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screenX < (WIDTH + self.IMAGE_HALF_WIDTH) and self.normalDist > 0.5:
            self.getSpriteProjection()
    def update(self):
        self.getSprite()

class AnimatedSprite(StaticSprite):
    def __init__(self, game, path, pos=(11.5, 3.5), scale=0.8, shift=0.16, animationTime=120):
        super().__init__(game, path, pos, scale, shift)
        self.animationTime = animationTime
        self.path = path.rsplit('/', 1)[0]
        self.images = self.getImages(self.path)
        self.animationTimePrev = pg.time.get_ticks()
        self.animationTrigger = False

    def update(self):
        super().update()
        self.checkAnimationTime()
        self.animate(self.images)

    def animate(self, images):
        if self.animationTrigger:
            images.rotate(-1)
            self.image = images[0]

    def checkAnimationTime(self):
        self.animationTrigger = False
        currentTime= pg.time.get_ticks()
        if currentTime - self.animationTimePrev > self.animationTime:
            self.animationTimePrev = currentTime
            self.animationTrigger = True

    def getImages(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images
