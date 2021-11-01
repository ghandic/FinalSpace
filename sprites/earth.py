from pathlib import Path

import pygame

from models import Screen


def rot_center(image: pygame.Surface, angle: int):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class Earth(pygame.sprite.Sprite):
    def __init__(self, screen: Screen) -> None:
        super(Earth, self).__init__()
        image = pygame.image.load(Path("assets") / "earth.png")
        self._image = pygame.transform.scale(image, (screen.height, screen.height))
        rect = self._image.get_rect()
        self.rect = rect.move((-int(0.8 * screen.height), 0))
        self.mask = pygame.mask.from_surface(self._image)
        self.screen = screen
        self.health = 10
        self.angle = 0
        self.spin_speed = 1
        self.image = self._image

    def animate(self) -> None:
        self.angle = (self.angle + (0.1 * self.spin_speed)) % 360
        self.image = rot_center(self._image, self.angle)
