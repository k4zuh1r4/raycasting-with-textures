import pygame as pg
from settings import *

class GraphicsRendering:
    def __init__(self, game):
        self._game = game
        self._screen = game._screen
        self._wallTextures = self.wallMapping()
        self._gameOverTempImage = self.textureGrab('resources/gameover.jpg', (WIDTH,HEIGHT))
    def graphicsDraw(self):
        self.wallRendering()
    def gameOverScreen(self):
        self._screen.blit(self._gameOverTempImage, (0,0))
    def wallRendering(self):
        renderMap = sorted(self._game._rayCasting._renderingTarget,key=lambda t: t[0], reverse=True)
        for depth,image, position in renderMap:
            self._screen.blit(image,position)
    @staticmethod
    def textureGrab(path, resolution =(TEXTURE_SIZE, TEXTURE_SIZE)): #texture res = texture size^2, a fucking square.
        texture = pg.image.load(path).convert_alpha() #converts into a scaled image to fit the screen, faster rendering and keeps the alpha channel of the image, also supporting transparent pngs.
        return pg.transform.scale(texture, resolution)
    def wallMapping(self):
        return {
            0: self.textureGrab('resources/textures/BRICK_1B.png'),
            1: self.textureGrab('resources/textures/CONCRETE_2C.png'),
            2: self.textureGrab('resources/textures/CONCRETE_3A.png')
            }

