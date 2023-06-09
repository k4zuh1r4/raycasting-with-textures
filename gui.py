from settings import *
import pygame as pg
import math

class Menu:
    def __init__(self, game):
        self._game = game
        self._guiScreen = self._game._screen
        self._mainGuiResolution = (WIDTH,HEIGHT)
        self._buttonResolution = (WIDTH//4, HEIGHT//4)
        self._
    @staticmethod
    def guiTextureGrab(path, resolution): #texture res = texture size^2, a fucking square.
        texture = pg.image.load(path).convert_alpha() #converts into a scaled image to fit the screen, faster rendering and keeps the alpha channel of the image, also supporting transparent pngs.
        return pg.transform.scale(texture, resolution)
    def menuRendering(self):
        #for image, position in ???:      
        #    self._screen.blit(image,position)
        pass
    def menuTexture(self):
        return {
            0: self.guiTextureGrab('resources/textures/BRICK_1B.png'),
            1: self.guiTextureGrab('resources/textures/BRICK_1B.png'),                     
            }

