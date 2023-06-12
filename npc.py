from spritesHandling import *
from random import randint, choice, random

class NPC(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/npc/minotaur/0.png', pos=(0,0),scale=0.6, shift=0.38, animationTime = 200):
        super().__init__(game, path,pos,scale,shift,animationTime)
        self._attackSprite = self.getImages(self.path + '/attack')
        self._deathSprite = self.getImages(self.path + '/death')
        self._idleSprite = self.getImages(self.path + '/idle')
        self._painSprite = self.getImages(self.path + '/pain')
        self._walkSprite = self.getImages(self.path+ '/walk')

        self._NPCRange = randint(2,4)
        self._NPCDamage = 6.9420
        self._NPCSpeed = 0.03
        self._NPCSize = 10
        self._NPCHealth = 100
        self._NPCAccuracy = 0.4
        self._alive = True
        self._pain = False
        self._aimingRay = False
        self._deathFrameCounter = 0

    def NPCDamageReceiveAnimation(self):
        self.animate(self._painSprite)
        if self.animationTrigger == True:
            self._pain = False
    def NPCHitDectection(self):
        if self._ObstructCheck == True and self.game._player._shotState == True:            
            if (((HEIGHT//2) - self.spriteHalfWidth) < self.screenX < ((WIDTH//2) + self.spriteHalfWidth)):
                self.game._soundHandler._NPCDamage.play()
                self.game._player._shotState == False
                self._pain = True
                self._NPCHealth -= self.game._weapon.damage
                self.NPCStatus()
    def NPCStatus(self):
        if self._NPCHealth < 1:
            self._alive = False
            self.game._soundHandler._NPCDeath.play()
    def NPCAttack(self):
        if self.animationTrigger == True:
            self.game._soundHandler._NPCAttack.play()
            if random() < self._NPCAccuracy:
                self.game._player.receiveDamage(self._NPCDamage)
    def NPCBehavior(self):
        if self._alive == True:
            self._ObstructCheck = self.NPCDistance()
            self.NPCHitDectection()
            if self._pain == True: #animate
                #self.NPCDamageReceiveAnimation()
                self.animate(self._painSprite)
                if self.animationTrigger == True:
                    self._pain = False
            elif self._ObstructCheck == True:
                self.animate(self._walkSprite)
                self.NPCMovement()
                if self.dist < self._NPCRange:
                    self.animate(self._attackSprite)
                    self.NPCAttack()
            else:            
                self.animate(self._idleSprite)
        elif not self._alive:
            if self.animationTrigger == True and self._deathFrameCounter < len(self._deathSprite) -1:
                self._deathSprite.rotate(-1)
                self.image = self._deathSprite[0]
                self._deathFrameCounter += 1
    def update(self):   
        self.checkAnimationTime()
        self.getSprite()
        self.NPCBehavior()
        #self.NPCDistanceDraw()
    def NPCMovement(self):
        targetPosition = self.game._player.mapPos
        targetX, targetY = targetPosition
        NPCAngle = math.atan2(targetY + 0.5 - self.y, targetX + 0.5 - self.x)
        dx = math.cos(NPCAngle)*self._NPCSpeed
        dy = math.sin(NPCAngle)*self._NPCSpeed
        self.collisionCheckNPC(dx,dy)
    def wallCheckNPC(self, x,y):
        return False if (x,y) in self.game._map._convertedMap else True #return False and disallow player to go through wall when touched the wall coords
    def collisionCheckNPC(self,dx,dy):            
        if self.wallCheckNPC(int(self.x + dx*self._NPCSize),int(self.y)): #checks for wall in x dimension
            self.x += dx
        if self.wallCheckNPC(int(self.x), int(self.y+ dy*self._NPCSize)): #checks for wall in y dimension                  
            self.y += dy
    @property
    def mapPos(self):
        return int(self.x), int(self.y)

    def NPCDistance(self):
        if self.game._player.mapPos == self.mapPos:
            return True
        wallDistanceVertical, wallDistanceHorizontal = 0,0
        playerDistanceVertical, playerDistanceHorizontal = 0,0
        oX,oY = self.game._player.pos
        xMap, yMap = self.game._player.mapPos 
        rayAngleNPC = self.theta
        if math.sin(rayAngleNPC) > 0:           
            horizontalY = yMap + 1           
            dy =  1
        else:
            horizontalY = yMap - 1e-6
            dy = -1
        horizontalDepth = (horizontalY - oY) / math.sin(rayAngleNPC)
        horizontalX = oX + horizontalDepth * math.cos(rayAngleNPC)
        deltaDepth = dy / math.sin(rayAngleNPC)
        dx = deltaDepth * math.cos(rayAngleNPC)
        for horizontalCounter in range(DRAW_DISTANCE):
            horizontalTiles = int(horizontalX), int(horizontalY)
            if horizontalTiles == self.mapPos:
                playerDistanceHorizontal = horizontalDepth
                break
            if horizontalTiles in self.game._map._convertedMap:                   
                wallDistanceHorizontal = horizontalDepth
                break
            horizontalX += dx
            horizontalY += dy
            horizontalDepth += deltaDepth
        #vertical calculation
        if math.cos(rayAngleNPC) > 0:              
            verticalX = xMap + 1 
            dx = 1
        else:               
            verticalX = xMap - 1e-6               
            dx = -1
        verticalDepth = (verticalX - oX) / math.cos(rayAngleNPC)
        verticalY = oY + verticalDepth * math.sin(rayAngleNPC)
        deltaDepth = dx / math.cos(rayAngleNPC)
        dy = deltaDepth * math.sin(rayAngleNPC)
        for verticalCounter in range(DRAW_DISTANCE):
            verticalTiles = int(verticalX), int(verticalY)
            if verticalTiles == self.mapPos:
                playerDistanceVertical = verticalDepth
                break
            if verticalTiles in self.game._map._convertedMap:  
                wallDistanceVertical = verticalDepth
                break 
            verticalX += dx
            verticalY += dy
            verticalDepth += deltaDepth
        playerDistance = max(playerDistanceHorizontal,playerDistanceVertical)
        wallDistance = max(wallDistanceHorizontal, wallDistanceVertical)
        if 0 < playerDistance < wallDistance or not wallDistance:
            return True
        return False
    def NPCDistanceDraw(self): # for debugging purpose
        pg.draw.circle(self.game._screen, 'red', (100*self.x, 100*self.y),15)
        if self.NPCDistance() == True:
            pg.draw.line(self.game._screen, 'orange', (100*self.game._player._playerPosX, 100*self.game._player._playerPosY), (100*self.x, 100*self.y),2)

