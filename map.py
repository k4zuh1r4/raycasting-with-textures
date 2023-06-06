import pygame as pg
testMap = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],    
]

class MapHandler:
    def __init__(self, game):
        self._game = game
        self._testMap = testMap
        self._convertedMap = {}
        self._convertedFloor = {}
        self.getMap()
    def getMap(self):
        for j, row in enumerate(self._testMap):
            for i, value in enumerate(row):
                if value >= 1:
                    self._convertedMap[(i,j)] = value #assign tiled maps into _worldMap dictionary with coords
        for floorJ, floorRow in enumerate(self._testMap):
            for floorI, floorValue in enumerate(row):
                if floorValue == 0:
                    self._convertedFloor[(i,j)] = floorValue
    def drawMap(self):
        for pos in self._convertedMap:       
            pg.draw.rect(self._game._screen, 'darkgray',(pos[0] * 100, pos[1] * 100, 100, 100), 2) #100x100 WxH, 2 pixels border, position calculated using pos[0]*100, pos[1]*100
        for floorPos in self._convertedFloor:       
            pg.draw.rect(self._game._screen, 'white',(pos[0] * 100, pos[1] * 100, 100, 100), 2)
