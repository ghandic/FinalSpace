from dataclasses import dataclass
from typing import Callable

import pygame


@dataclass
class Screen:
    width: int
    height: int


@dataclass
class Button:
    message: str = ""
    x: int = 0
    y: int = 0
    w: int = 100
    h: int = 50
    inactive_color: tuple[int, int, int] = (255, 255, 255)
    active_color: tuple[int, int, int] = (255, 255, 255)
    font_color: tuple[int, int, int] = (200, 200, 200)
    font_size: int = 20
    on_click: Callable = lambda: None

    def display(self, screen: pygame.Surface) -> None:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        offset = screen.get_abs_offset()
        if (
            self.x + self.w + offset[0] > mouse[0] > self.x + offset[0]
            and self.y + self.h + offset[1] > mouse[1] > self.y + offset[1]
        ):
            pygame.draw.rect(screen, self.active_color, (self.x, self.y, self.w, self.h))

            if click[0] == 1:
                self.on_click()
        else:
            pygame.draw.rect(screen, self.inactive_color, (self.x, self.y, self.w, self.h))

        smallText = pygame.font.SysFont("freesansbold.ttf", self.font_size)
        textSurface = smallText.render(self.message, True, self.font_color)
        textSurf, textRect = textSurface, textSurface.get_rect()
        textRect.center = ((self.x + (self.w / 2)), (self.y + (self.h / 2)))
        screen.blit(textSurf, textRect)
