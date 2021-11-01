from pathlib import Path

import pygame

from utils import text_objects


class ScoreBoard:
    def __init__(self, screen: pygame.Surface, height: int = 50) -> None:
        self.screen = screen
        self.lives = 3
        self.score = 0
        self.health = 100
        _, _, self.width, _ = self.screen.get_rect()
        self.height = height
        self.font_color = (0, 0, 0)

    def display(self) -> None:
        pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, self.width, self.height / 2))
        smallText = pygame.font.SysFont("freesansbold.ttf", int(self.height / 2))
        text_y = lambda textRect: (self.height - textRect.height) / 2 - 5

        textSurf, textRect = text_objects(f"World Health: {self.health}", smallText, self.font_color)
        textRect.center = (textRect.width / 2 + 5, text_y(textRect))
        self.screen.blit(textSurf, textRect)

        textSurf, textRect = text_objects(f"Score: {int(self.score)}", smallText, self.font_color)
        textRect.center = (self.width - (textRect.width / 2 + 5), text_y(textRect))
        self.screen.blit(textSurf, textRect)

        textSurf, textRect = text_objects("Lives: ", smallText, self.font_color)
        textRect.center = (self.width / 2 - (textRect.width / 2 + 5), text_y(textRect))
        self.screen.blit(textSurf, textRect)
        image = pygame.image.load(Path("assets") / "mooncake" / "mooncake-right-1.png")
        size = (self.height / 2) - 5
        image = pygame.transform.scale(image, (size, size))
        for i in range(self.lives):
            rect = image.get_rect()
            rect = rect.move(i * (size + i) + (self.width / 2), 5 / 2)
            self.screen.blit(image, rect)
