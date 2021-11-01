from pathlib import Path

import pygame

from controls import Controls
from models import Screen
from .projectile import Projectile
from .gif_sprite import GIFSprite


class Player(GIFSprite):
    def __init__(self, screen: Screen) -> None:
        super().__init__()
        self.images = [pygame.image.load(Path("assets") / "mooncake" / f"mooncake-right-{i}.png") for i in range(1, 8)]
        self.is_active = False

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.screen = screen
        self.chookity = pygame.mixer.Sound(Path("assets") / "mooncake" / "chookity.mp3")
        self.die = pygame.mixer.Sound(Path("assets") / "mooncake" / "die.mp3")
        self.ouch = pygame.mixer.Sound(Path("assets") / "mooncake" / "ouch.mp3")
        self.projectiles = pygame.sprite.Group()
        self.lives = 3

    def shoot(self) -> None:
        if not self.is_active:
            return
        self.projectiles.add(Projectile(*self.rect.center))
        self.chookity.play()

    def update(self) -> None:
        pressed_keys = pygame.key.get_pressed()
        click = pygame.mouse.get_pressed()

        self.animate()
        if pressed_keys[Controls.UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[Controls.DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[Controls.LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[Controls.RIGHT]:
            self.rect.move_ip(5, 0)
        if click[0] == 1 and not pygame.mixer.get_busy():
            self.shoot()

        for projectile in self.projectiles:
            projectile.update()
            if projectile.x >= self.screen.width or projectile.x <= 0:
                projectile.kill()

        # Keep player on the screen
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, self.screen.width)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, self.screen.height)

    def kill(self) -> None:
        super().kill()
        self.die.play()
