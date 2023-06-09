import pygame as pg
from settings import *

class GraphicsRendering:
    def __init__(self, game):
        self._game = game
        self._screen = game._screen
        self._wallTextures = self.wallMapping()
    def graphicsDraw(self):
        self.wallRendering()
    def wallRendering(self):
        wallMap = self._game._rayCasting._renderingTarget
        for depth,image, position in wallMap:
            self._screen.blit(image,position)                     
    @staticmethod
    def textureGrab(path, resolution =(TEXTURE_SIZE, TEXTURE_SIZE)): #texture res = texture size^2, a fucking square.
        texture = pg.image.load(path).convert_alpha() #converts into a scaled image to fit the screen, faster rendering and keeps the alpha channel of the image, also supporting transparent pngs.
        return pg.transform.scale(texture, resolution)

    def wallMapping(self):
        return {
            0: self.textureGrab('resources/textures/BRICK_1B.png'),
            1: self.textureGrab('resources/textures/BRICK_1A.png'),
            2: self.textureGrab('resources/textures/BRICK_2A.png')
            }

