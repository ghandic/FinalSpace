from pathlib import Path
import random

import pygame

from models import Screen


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen: Screen) -> None:
        super(Enemy, self).__init__()
        self.image = pygame.image.load(Path("assets") / "enemies" / "fluffles" / "fluffles-1.png")
        self.size = random.randint(1, 3)
        height = int(28 * self.size)
        self.image = pygame.transform.scale(self.image, (int(44 * self.size), int(28 * self.size)))
        self.rect = self.image.get_rect(
            center=(
                random.randint(screen.width + 20, screen.width + 100),
                random.randint(height, screen.height - height),
            )
        )
        self.speed = random.randint(1, 3)

    def update(self) -> None:
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
