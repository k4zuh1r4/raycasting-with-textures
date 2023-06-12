import pygame as pg

class Sound:
    def __init__(self, game):
        self._game = game
        pg.mixer.init()
        self._sfxPath = 'resources/sfx/'
        self._shotgunSFX = pg.mixer.Sound(self._sfxPath + 'shot.wav')
        self._shotgunSFX.set_volume(0.4)
        self._bgTheme = pg.mixer.music.load(self._sfxPath + 'shibuya_smt.mp3')
        self._NPCDamage = pg.mixer.Sound(self._sfxPath + 'hit.wav')
        self._NPCDeath = pg.mixer.Sound(self._sfxPath + 'dead.wav')
        self._NPCAttack = pg.mixer.Sound(self._sfxPath + 'npcAttack.wav')
        self._playerDamage = pg.mixer.Sound(self._sfxPath + 'damaged.wav')
        pg.mixer.music.set_volume(0.8)