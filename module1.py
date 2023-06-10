def render(self):
        self._renderingTarget = []

        # Render walls (your original code)
        # ...

        # Render floors and ceilings
        for ray, values in enumerate(self._rayCastingRecord):
            depth, projectionHeight, textures, offset = values
            floor_offset, ceiling_offset = offset, offset  # Assuming the same offset for both floor and ceiling
            floor_tex, ceiling_tex = self._game._textureHandling._floorTextures, self._game._textureHandling._ceilingTextures            
            # Calculate floor and ceiling y coordinates
            floor_y = (projectionHeight // 2) + (projectionHeight // 2) // 2
            ceiling_y = (projectionHeight // 2) - (projectionHeight // 2) // 2
            
            # Get floor and ceiling textures and render
            floor_tex_column = self.wallRender[1].subsurface(floor_offset * (TEXTURE_SIZE - TEXTURE_SCALE), 0, TEXTURE_SCALE, TEXTURE_SIZE)
            floor_tex_column = pg.transform.scale(floor_tex_column, (TEXTURE_SCALE, TEXTURE_SIZE // 2))
            floor_position = (ray * TEXTURE_SCALE, floor_y)
            self._renderingTarget.append((depth, floor_tex_column, floor_position))

            ceiling_tex_column = self.wallRender[1].subsurface(ceiling_offset * (TEXTURE_SIZE - TEXTURE_SCALE), 0, TEXTURE_SCALE, TEXTURE_SIZE)
            ceiling_tex_column = pg.transform.scale(ceiling_tex_column, (TEXTURE_SCALE, TEXTURE_SIZE // 2))
            ceiling_position = (ray * TEXTURE_SCALE, ceiling_y)
            self._renderingTarget.append((depth, ceiling_tex_column, ceiling_position))


def render(self):
    self._renderingTarget = []
    self._floorRenderingTarget = []
    self._ceilingRenderingTarget = []

    for ray, values in enumerate(self._rayCastingRecord):
        depth, projectionHeight, textures, offset = values

        # Wall rendering code (unaltered)

        # Calculate floor and ceiling positions
        floorY = (HEIGHT // 2) + (projectionHeight // 2)
        ceilingY = (HEIGHT // 2) - (projectionHeight // 2)

        # Create floor and ceiling surfaces
        floorColumn = self.wallRender[textures].subsurface(offset * (TEXTURE_SIZE - TEXTURE_SCALE), 0, TEXTURE_SCALE, TEXTURE_SIZE)
        floorColumn = pg.transform.scale(floorColumn, (TEXTURE_SCALE, HEIGHT - floorY))
        ceilingColumn = self.wallRender[textures].subsurface(offset * (TEXTURE_SIZE - TEXTURE_SCALE), 0, TEXTURE_SCALE, TEXTURE_SIZE)
        ceilingColumn = pg.transform.scale(ceilingColumn, (TEXTURE_SCALE, ceilingY))

        # Append floor and ceiling surfaces to rendering target lists
        self._floorRenderingTarget.append((depth, floorColumn, (ray * TEXTURE_SCALE, floorY)))
        self._ceilingRenderingTarget.append((depth, ceilingColumn, (ray * TEXTURE_SCALE, ceilingY - ceilingColumn.get_height())))

    # Drawing loop (update to include floor and ceiling rendering)
    for depth, wallColumn, wallPosition in self._renderingTarget:
        self._game._screen.blit(wallColumn, wallPosition)

    for depth, floorColumn, floorPosition in self._floorRenderingTarget:
        self._game._screen.blit(floorColumn, floorPosition)

    for depth, ceilingColumn, ceilingPosition in self._ceilingRenderingTarget:
        self._game._screen.blit(ceilingColumn, ceilingPosition)

import os
import pygame as pg
from collections import deque


class AnimatedSpriteHandler(StaticSpriteHandler):
    def __init__(self, game, path='resources/sprites/animated_sprites/green_light/0.png', pos=(11.5, 3.5),
                 scale=0.8, shift=0.16, animationTime=120):
        super().__init__(game, path, pos, scale, shift)
        self.animationTime = animationTime
        self.path = path.rsplit('/', 1)[0]
        self.images = self.getImages(self.path)
        self.animationTimePrev = pg.time.get_ticks()
        self.animationTrigger = False

    def update(self):
        super().spriteUpdate()
        self.checkAnimationTime()
        self.animate(self.images)

    def animate(self, images):
        if self.animationTrigger:
            images.rotate(-1)
            self.image = images[0]

    def checkAnimationTime(self):
        self.animationTrigger = False
        currentTime = pg.time.get_ticks()
        if currentTime - self.animationTimePrev > self.animationTime:
            self.animationTimePrev = currentTime
            self.animationTrigger = True

    def getImages(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images