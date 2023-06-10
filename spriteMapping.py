from spritesHandling import *
class spritesMapper:
    def __init__(self, game):
        self._game = game
        self._spritesList = []
        self._staticSpritePath = 'resources/sprites/static_sprites/'
        self._dynamicSpritePath = 'resources/sprites/animated_sprites/'