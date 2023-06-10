import pygame as pg
import math
from settings import *
class RayCasting:
    def __init__(self,game):
        self._game = game
        self._rayCastingRecord = [] #stores the positions of walls for raycasting.
        self._renderingTarget =[]
        self._shadowData = []
        self.wallRender = self._game._textureHandling._wallTextures
    def render(self):
        self._renderingTarget = []
        for ray, values in enumerate(self._rayCastingRecord): #rendering the walls based on data stored in self._rayCastingRecord.
            depth, projectionHeight, textures, offset = values
            if projectionHeight < HEIGHT:            
                wallColumn = self.wallRender[textures].subsurface(offset*(TEXTURE_SIZE- TEXTURE_SCALE), 0, TEXTURE_SCALE, TEXTURE_SIZE) #calculates rendering positions of wall and image.
                wallColumn = pg.transform.scale(wallColumn,(TEXTURE_SCALE, projectionHeight)) #transform into image.          
                wallPosition = (ray * TEXTURE_SCALE, (HEIGHT//2) - (projectionHeight//2))
            else:
                textureHeight = TEXTURE_SIZE*HEIGHT/projectionHeight
                wallColumn = self.wallRender[textures].subsurface(offset*(TEXTURE_SIZE- TEXTURE_SCALE), TEXTURE_SIZE//2 - textureHeight//2, TEXTURE_SCALE, textureHeight) #calculates rendering positions of wall and image.
                wallColumn = pg.transform.scale(wallColumn,(TEXTURE_SCALE, HEIGHT))
                wallPosition = (ray * TEXTURE_SCALE, 0)
            self._renderingTarget.append((depth, wallColumn, wallPosition))
    def engine(self):
        self._rayCastingRecord = [] #reset list at beginning of func, saves memory and performance.
        oX,oY = self._game._player.pos #get playerpos via @property
        xMap, yMap = self._game._player.mapPos #get wall coords in mapPos via @property.
        rayAngle = self._game._player._playerAngle - HALF_FOV +0.000001 # prevents the angle goes to 0. can use exception handling but too lazy.
        verticalTextures, horizontalTextures = 1, 1 #prevent undefined variable.
        verticalFloorTiles, horizontalFloorTiles = 1,1
        for ray in range(RAY_AMOUNT):
            # horizontal calculation
            if math.sin(rayAngle) > 0:           
                horizontalY = yMap + 1           
                dy =  1
            else:
                horizontalY = yMap - 1e-6
                dy = -1
            horizontalDepth = (horizontalY - oY) / math.sin(rayAngle)
            horizontalX = oX + horizontalDepth * math.cos(rayAngle)
            deltaDepth = dy / math.sin(rayAngle)
            dx = deltaDepth * math.cos(rayAngle)

            for horizontalCounter in range(DRAW_DISTANCE):
                horizontalTiles = int(horizontalX), int(horizontalY)
                horizontalFloorTiles = int(horizontalX), int(horizontalY)
                if horizontalTiles in self._game._map._convertedMap:                   
                    horizontalTextures = self._game._map._convertedMap[horizontalTiles]
                    break
                if horizontalFloorTiles in self._game._map._convertedFloor:
                    horizontalFloorTiles = self._game._map._convertedFloor[horizontalFloorTiles]
                    break
                horizontalX += dx
                horizontalY += dy
                horizontalDepth += deltaDepth
            #vertical calculation
            if math.cos(rayAngle) > 0:              
                verticalX = xMap + 1 
                dx = 1
            else:               
                verticalX = xMap - 1e-6               
                dx = -1
            verticalDepth = (verticalX - oX) / math.cos(rayAngle)
            verticalY = oY + verticalDepth * math.sin(rayAngle)
            deltaDepth = dx / math.cos(rayAngle)
            dy = deltaDepth * math.sin(rayAngle)

            for verticalCounter in range(DRAW_DISTANCE):
                verticalTiles = int(verticalX), int(verticalY)
                verticalFloorTiles = int(verticalX), int(verticalY)
                if verticalTiles in self._game._map._convertedMap:  
                    verticalTextures = self._game._map._convertedMap[verticalTiles]
                    break 
                if verticalFloorTiles in self._game._map._convertedFloor:
                    verticalFloorTiles = self._game._map._convertedFloor[verticalFloorTiles]
                    break
                verticalX += dx
                verticalY += dy
                verticalDepth += deltaDepth
            # depth accuracy
            if verticalDepth < horizontalDepth:
                depth, texture = verticalDepth, verticalTextures
                verticalY %= 1
                if math.cos(rayAngle) > 0:
                    offset = verticalY
                else:
                    offset = 1 - verticalY
            else:
                depth, texture = horizontalDepth, horizontalTextures
                horizontalX %=1
                if math.sin(rayAngle) > 0:
                    offset = 1 - horizontalX
                else:
                    offset = horizontalX
            depth *=math.cos(self._game._player._playerAngle - rayAngle) #fishbowl fix
            projectionHeight = SCREEN_DISTANCE/ (depth +0.00001) #prevents going to 0.
            #pg.draw.line(self._game._screen, 'red',(100*oX, 100*oY),                                              
            #             (100*oX + 100*depth*math.cos(rayAngle), 100*oY + 100*depth*math.sin(rayAngle)),2) #test draw for rays

            #color = (255/(1+ depth** 5 *0.00002),255/(1+ depth** 5 *0.00002),255/(1+ depth** 5 *0.00002)) #formula for calculating colors, no idea.
            #pg.draw.rect(self._game._screen, color, 
            #             (ray*TEXTURE_SCALE, HEIGHT//2 - projectionHeight//2, TEXTURE_SCALE, projectionHeight))
            self._rayCastingRecord.append((depth, projectionHeight,texture,offset))

            rayAngle += DELTA_ANGLE
    def engineUpdate(self):
        self.engine()
        self.render()