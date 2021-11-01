from pathlib import Path
import shelve

import pygame

from events import Events
from sprites import Player, Enemy, Earth, Explosion
from models import Screen, Button
from utils import text_objects
from scoreboard import ScoreBoard


class Game:
    def __init__(self) -> None:
        self.title = "Final Space"
        self.font_color = (200, 200, 200)

        pygame.init()
        pygame.mixer.init()
        pygame.display.set_icon(pygame.image.load(Path("assets") / "icon.ico"))
        pygame.display.set_caption('Final Space')

        self.offset = 100
        self.main_screen_dims = Screen(width=1600, height=1200)
        self.main_screen = pygame.display.set_mode(
            (self.main_screen_dims.width, self.main_screen_dims.height)
        )

        self.screen_dims = Screen(width=self.main_screen_dims.width, height=self.main_screen_dims.height - self.offset)
        self.screen = self.main_screen.subsurface(
            pygame.Rect(0, self.offset, self.screen_dims.width, self.screen_dims.height)
        )
        pygame.time.set_timer(Events.ADDENEMY, 750)
        pygame.time.set_timer(Events.NEXT_LEVEL, 750 * 10)
        self.background_music = pygame.mixer.music.load(Path("assets") / "background-theme.mp3")
        self.clock = pygame.time.Clock()
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.01)
        self.reset()

    def reset(self) -> None:
        self.scoreboard = ScoreBoard(self.main_screen, height=self.offset)
        self.db = shelve.open(str(Path("assets") / "highscore"))
        self.highscore = self.db.get("score", 0)
        self.level = 0

    def intro(self) -> None:

        buttons = [
            Button("GO!", self.main_screen_dims.width/4 - self.offset, int(0.75*self.main_screen_dims.height), 100, 50, on_click=self.run, font_size=32, font_color=(0, 0, 0)),
            Button("Quit", 3*(self.main_screen_dims.width/4) - self.offset, int(0.75*self.main_screen_dims.height), 100, 50, on_click=pygame.quit, font_size=32, font_color=(0, 0, 0)),
        ]

        self._intro = True

        while self._intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self._intro = False

            self.main_screen.fill((0, 0, 0))
            largeText = pygame.font.Font("freesansbold.ttf", 115)

            TextSurf, TextRect = text_objects(self.title, largeText, self.font_color)
            TextRect.center = ((self.main_screen_dims.width / 2), (self.main_screen_dims.height / 2) - self.offset)
            self.main_screen.blit(TextSurf, TextRect)

            for button in buttons:
                button.display(self.main_screen)

            smallText = pygame.font.SysFont("freesansbold.ttf", 20)
            TextSurf, TextRect = text_objects(f"Highscore: {self.highscore}", smallText, self.font_color)
            TextRect.center = ((self.main_screen_dims.width / 2), int(0.75*self.main_screen_dims.height) + 25)
            self.main_screen.blit(TextSurf, TextRect)

            pygame.display.update()
            self.clock.tick(15)

    def __set_volume(self) -> None:
        pygame.mixer.music.set_volume(len(self.enemies) / 200)

    def __create_window(self, width: int, height: int) -> None:
        self.screen = pygame.display.set_mode((width, height), Events.RESIZABLE)

    def __handle_events(self) -> None:
        for event in pygame.event.get():
            match event.type:
                case Events.NEXT_LEVEL:
                    self.level += 1
                    self.earth.spin_speed += 1
                    pygame.time.set_timer(Events.ADDENEMY, max(100, 750 - (50 * self.level)))
                case Events.ADDENEMY:
                    if not self.player.is_active:
                        self.player.is_active = True
                    if not self.is_paused:
                        new_enemy = Enemy(self.screen_dims)
                        self.enemies.add(new_enemy)
                        self.all_sprites.add(new_enemy)
                case Events.KEYDOWN:
                    match event.key:
                        case Events.K_ESCAPE:
                            self.running = False
                        case Events.PAUSE:
                            if self.is_paused:
                                pygame.mixer.music.unpause()
                            if not self.is_paused:
                                pygame.mixer.music.pause()
                            self.is_paused = not self.is_paused
                        case _:
                            pass
                case Events.QUIT:
                    self.end_game(silent=True)
                    pygame.quit()
                case _:
                    pass

    def end_game(self, silent: bool = False) -> None:
        self.highscore = max(self.scoreboard.score, self.highscore)
        self.db["score"] = self.highscore
        if not silent:
            self.player.kill()
            while pygame.mixer.get_busy():
                continue
        self.running = False
        self.db.close()

    def run(self) -> None:
        self.reset()

        self.player = Player(self.screen_dims)
        self.earth = Earth(self.screen_dims)
        self.enemies = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.all_sprites.add(self.earth)
        self.all_sprites.add(self.player)

        self.running = True
        self.is_paused = False
        self._intro = False
        self.__set_volume()

        while self.running:
            self.__handle_events()

            if not self.is_paused:
                self.player.update()
                self.explosions.update()
                self.enemies.update()
                self.earth.animate()
                self.scoreboard.score += 1
                self.scoreboard.display()

                self.screen.fill((0, 0, 0))

            for explosion in self.explosions:
                explosion.animate()
                self.screen.blit(explosion.image, explosion.rect)

            for entity in self.all_sprites:
                self.screen.blit(entity.image, entity.rect)

            for projectile in self.player.projectiles:
                projectile.draw(self.screen)
                for enemy in self.enemies:
                    if pygame.Rect.colliderect(projectile.rect, enemy):

                        enemy.kill()
                        projectile.kill()

            for enemy in self.enemies:
                hits = pygame.sprite.spritecollide(self.earth, self.enemies, False, pygame.sprite.collide_mask)
                for hit in hits:
                    self.scoreboard.health -= hit.size ** 2
                    self.explosions.add(
                        Explosion(
                            x=hit.rect.center[0] - hit.rect.width / 2,
                            y=hit.rect.center[1] - hit.rect.height / 2,
                            size=hit.rect.width,
                        )
                    )
                    hit.kill()
                if pygame.Rect.colliderect(self.player.rect, enemy):
                    self.scoreboard.lives -= 1
                    enemy.kill()
                    if self.scoreboard.lives >= 1:
                        self.player.ouch.play()

            if self.scoreboard.health <= 0 or self.scoreboard.lives <= 0:
                self.end_game()

            pygame.display.flip()

            self.clock.tick(60)
            self.__set_volume()

        self.intro()


if __name__ == "__main__":
    import logging

    logger = logging.getLogger()
    try:
        game = Game()
        game.intro()
    except:
        logger.error("Failed", exc_info=True)
