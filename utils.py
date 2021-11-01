import pygame


def text_objects(text: str, font: pygame.font.Font, color: tuple[int, int, int]) -> tuple[pygame.Surface, pygame.Rect]:
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
