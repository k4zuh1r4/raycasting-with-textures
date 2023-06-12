import pygame as pg
import sys
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
from settings import *
from map import *
from player import *
from graphicsEngine import *
from textureMapping import *
from spritesHandling import *
from spriteMapping import *
from weapons import *
from sfx import *
class MainGame:
    def __init__(self):
        pg.init()
        self._screen = pg.display.set_mode(RESOLUTION)
        self._clock = pg.time.Clock()
        self._runState = True
        self._deltaTime = 1
        self.gameLoad()
    def gameLoad(self):
        self._map = MapHandler(self)
        self._player = Player(self)
        self._textureHandling = GraphicsRendering(self)
        self._rayCasting = RayCasting(self)
        self._spriteMap = SpritesMapper(self)
        self._weapon = Shotgun(self)
        self._soundHandler = Sound(self)
        pg.mixer.music.play(-1)
    def updateLoop(self):
        self._player.movementUpdate()
        self._rayCasting.engineUpdate()
        self._spriteMap.spriteUpdate()
        self._weapon.weaponDraw()
        self._weapon.weaponUpdate()
        pg.display.flip()
        self._deltaTime = self._clock.tick(FRAMERATE)
        pg.display.set_caption(f'{self._clock.get_fps() :.1f}') #display framerate on screen
    def drawLoop(self):
        self._screen.fill((27,27,26), rect=(0,0,WIDTH,HEIGHT/2))
        self._screen.fill((27,27,26), rect=(0,HEIGHT/2,WIDTH,HEIGHT/2))
        self._textureHandling.graphicsDraw()
#        self._map.drawMap()
#        self._player.playerDraw()
    def eventHandler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key ==pg.K_ESCAPE):
                pg.quit()
                sys.exit()       
            self._player.fireSingleEvent(event)
    def execution(self):
        while self._runState == True:
            self.updateLoop()
            self.drawLoop()
            self.eventHandler()
if __name__ == '__main__':
    gameExec = MainGame()
    gameExec.execution()


