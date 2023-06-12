from spritesHandling import *
class Shotgun(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/shotgunSmall/0.png', scale=2.3, animationTime=90):
        super().__init__(game=game, path=path, scale=scale, animationTime=animationTime)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weaponPosition = (WIDTH//2 - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self._reloadState = False
        self._frameLength = len(self.images)
        self._frameCounter = 0
        self.damage = 20
    def shotAnimation(self):
        if self._reloadState == True:
            self.game._player._shotState = False
            if self.animationTrigger == True:
                self.images.rotate(-1)
                self.image = self.images[0]
                self._frameCounter += 1
                if self._frameCounter == len(self.images):
                    self._reloadState = False
                    self._frameCounter = 0

    def weaponDraw(self):
        self.game._screen.blit(self.images[0], self.weaponPosition)
    def weaponUpdate(self):
        self.checkAnimationTime()
        self.shotAnimation()