import math
from pathlib import Path

import pygame

from .gif_sprite import GIFSprite


class Projectile(GIFSprite):
    def __init__(self, x: int, y: int) -> None:
        super(Projectile, self).__init__()
        self.x = x
        self.y = y
        self.speed = 8
        self.__set_direction()

        images = [pygame.image.load(Path("assets") / "mooncake" / "shoot" / f"pixil-frame-{i}.png") for i in range(8)]
        self.images = [pygame.transform.scale(image, (3 * 9, 3 * 9)) for image in images]

        self.image = self.images[self.index]
        self.rect = pygame.Rect(self.x, self.y, 3 * 9, 3 * 9)

    def __set_direction(self) -> None:
        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - self.x, my - self.y)

        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    def update(self) -> None:
        self.animate()
        dx = self.dir[0] * self.speed
        dy = self.dir[1] * self.speed
        self.rect.move_ip(dx, dy)
