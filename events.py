import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, RLEACCEL, RESIZABLE, VIDEORESIZE, K_p


class Events:
    K_ESCAPE: int = K_ESCAPE
    KEYDOWN: int = KEYDOWN
    ADDENEMY: int = pygame.USEREVENT + 1
    NEXT_LEVEL: int = pygame.USEREVENT + 2
    QUIT: int = QUIT
    RLEACCEL: int = RLEACCEL
    RESIZABLE: int = RESIZABLE
    VIDEORESIZE: int = VIDEORESIZE
    PAUSE: int = K_p
