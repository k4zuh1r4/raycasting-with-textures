from spritesHandling import *
from npc import *
class SpritesMapper:
    def __init__(self, game):
        self._game = game
        self._spritesList = []
        self._NPCList = []
        self._NPCPath = 'resources/sprites/npc/'
        self._staticSpritePath = 'resources/sprites/static_sprites/'
        self._animatedSpritePath = 'resources/sprites/animated_sprites/'
        loadSprite = self.loadSprite #spriteMapping starts here.
        loadNPC = self.loadNPC 
        loadSprite(StaticSprite(game,'resources/sprites/static_sprites/candlebra.png',(10.5, 3.5)))
        loadSprite(AnimatedSprite(game,'resources/sprites/animated_sprites/green_light/0.png',(11.5, 3.5)))
        loadNPC(NPC(game,'resources/sprites/npc/minotaur/0.png', (2.5,3.5)))
    def spriteUpdate(self):
        for sprite in self._spritesList:
            sprite.update()
        for NPCSprite in self._NPCList:
            NPCSprite.update()
    def loadSprite(self, sprite):
        self._spritesList.append(sprite)
    def loadNPC(self, NPCSprite):
        self._NPCList.append(NPCSprite)
