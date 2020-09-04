import pygame
import os
import Objects
from ScreenEngine import GameSurface, ProgressBar, InfoWindow, HelpWindow, ScreenHandle, MiniMap
import Logic
import Service
from Settings import Settings

SCREEN_DIM = (800, 600)
KEYBOARD_CONTROL = True

if not KEYBOARD_CONTROL:
    import numpy as np


class Game:
    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode(SCREEN_DIM)
        pygame.display.set_caption("MyRPG")

        if not KEYBOARD_CONTROL:
            answer = np.zeros(4, dtype=float)

        self.settings = Settings()
        self.engine = Logic.GameEngine()
        self.drawer = None
        self.iteration = 0
        self.size = 60

    def start(self):
        self.create_game(self.size, True)
        self.check_events()
        pygame.display.quit()
        pygame.quit()
        exit(0)

    def create_game(self, sprite_size, is_new):
        if is_new:
            self.engine = Logic.GameEngine()
            self.engine.hero = Objects.Hero(self.settings.base_stats, Service.create_sprite(
                os.path.join("texture", "Hero.png"), sprite_size))
            Service.service_init(sprite_size)
            Service.reload_game(self.engine, self.engine.hero)
            self.set_chain()
        else:
            self.engine.sprite_size = sprite_size
            self.engine.hero.sprite = Service.create_sprite(
                os.path.join("texture", "Hero.png"), sprite_size)
            Service.service_init(sprite_size, False)

        Logic.GameEngine.sprite_size = sprite_size

        self.drawer.connect_engine(self.engine)

        self.iteration = 0

    def set_chain(self):
        self.drawer = ScreenHandle((0, 0))
        self.drawer = HelpWindow((700, 500), pygame.SRCALPHA, (0, 0), self.drawer)
        self.drawer = MiniMap((164, 164), pygame.SRCALPHA, (20, 20), self.drawer)
        self.drawer = InfoWindow((160, 600), (476, 0), self.drawer)
        self.drawer = ProgressBar((640, 120), (640, 0), self.drawer)
        self.drawer = GameSurface((640, 480), pygame.SRCALPHA, (0, 480), self.drawer)

    def check_events(self):
        while self.engine.working:
            if self.engine.hero.dead:
                self.engine.hero.dead = not self.engine.hero.dead
                self.create_game(self.size, True)
                self.engine.notify("Hero dead. Game restarted")

            if KEYBOARD_CONTROL:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.engine.working = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_h:
                            self.engine.show_help = not self.engine.show_help
                        if event.key == pygame.K_KP_PLUS:
                            self.engine.zoom_in()
                            self.size = self.engine.sprite_size
                            self.create_game(self.size, False)
                        if event.key == pygame.K_KP_MINUS:
                            self.engine.zoom_out()
                            self.size = self.engine.sprite_size
                            self.create_game(self.size, False)
                        if event.key == pygame.K_r:
                            self.create_game(self.size, True)
                        if event.key == pygame.K_m:
                            self.engine.show_minimap = not self.engine.show_minimap
                        if event.key == pygame.K_ESCAPE:
                            self.engine.working = False
                        if self.engine.game_process:
                            if event.key == pygame.K_UP:
                                self.engine.move_up()
                                self.iteration += 1
                            elif event.key == pygame.K_DOWN:
                                self.engine.move_down()
                                self.iteration += 1
                            elif event.key == pygame.K_LEFT:
                                self.engine.move_left()
                                self.iteration += 1
                            elif event.key == pygame.K_RIGHT:
                                self.engine.move_right()
                                self.iteration += 1
                        else:
                            if event.key == pygame.K_RETURN:
                                self.create_game()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.engine.working = False
                if self.engine.game_process:
                    actions = [
                        self.engine.move_right,
                        self.engine.move_left,
                        self.engine.move_up,
                        self.engine.move_down,
                    ]
                    answer = np.random.randint(0, 100, 4)
                    prev_score = self.engine.score
                    move = actions[np.argmax(answer)]()
                    state = pygame.surfarray.array3d(self.gameDisplay)
                    reward = self.engine.score - prev_score
                    print(reward)
                else:
                    self.create_game()

            self.gameDisplay.blit(self.drawer, (0, 0))
            self.drawer.draw(self.gameDisplay)

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.start()
