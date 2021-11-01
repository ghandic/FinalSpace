import pygame


class GIFSprite(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.index = 0
        self.last_update = 0
        self.fps = 100
        self.images = []

    def animate(self, kill: bool = False) -> None:
        if pygame.time.get_ticks() - self.last_update > self.fps:
            self.index += 1
            self.last_update = pygame.time.get_ticks()

        if self.index >= len(self.images):
            if kill:
                self.kill()
                return
            self.index = 0

        self.image = self.images[self.index]
