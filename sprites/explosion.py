from pathlib import Path

import pygame

from .gif_sprite import GIFSprite


class Explosion(GIFSprite):
    def __init__(self, x: int, y: int, size: int) -> None:
        super().__init__()
        images = [pygame.image.load(Path("assets") / "explosion" / f"pixil-frame-{i}.png") for i in range(6)]
        self.images = [pygame.transform.scale(image, (size, size)) for image in images]
        rect = images[0].get_rect()
        self.rect = rect.move((x, y))
        pygame.mixer.Sound(Path("assets") / "pew.mp3").play()

    def animate(self) -> None:
        super().animate(kill=True)
