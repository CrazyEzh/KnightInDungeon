import pygame
import collections
from Objects import Ally, Enemy

colors = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 0, 0, 255),
    "green": (0, 255, 0, 255),
    "blue": (0, 0, 255, 255),
    "wooden": (153, 92, 0, 255),
}


class ScreenHandle(pygame.Surface):

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            self.successor = args[-1]
            self.next_coord = args[-2]
            args = args[:-2]
        else:
            self.successor = None
            self.next_coord = (0, 0)
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def draw(self, canvas):
        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)

    def connect_engine(self, engine):
        if self.successor is not None:
            self.successor.connect_engine(engine)

    def update(self, value):
        pass


class GameSurface(ScreenHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_size = self.get_size()
        self.map_corner = [0, 0]

    def connect_engine(self, engine):
        self.game_engine = engine
        super().connect_engine(self.game_engine)

    def draw_hero(self):
        self.draw_object(self.game_engine.hero.sprite, self.game_engine.hero.position)

    def prepare_view(self):
        hero_pos = self.game_engine.hero.position
        map_size = [len(self.game_engine.map), len(self.game_engine.map[0])]
        size = self.game_engine.sprite_size
        max_size = self.screen_size
        for i in range(len(hero_pos)):
            self.map_corner[i] = hero_pos[i] * size + size // 2 - max_size[i] // 2
            max_corner = map_size[i] * size - max_size[i]

            if self.map_corner[i] < 0:
                self.map_corner[i] = 0
            if self.map_corner[i] > max_corner:
                self.map_corner[i] = max_corner
                if self.map_corner[i] < 0:
                    self.map_corner[i] = self.map_corner[i] // 2

    def get_pos(self, coords):
        size = self.game_engine.sprite_size
        x = coords[0] * size - self.map_corner[0]
        y = coords[1] * size - self.map_corner[1]
        return x, y

    def draw_map(self):
        self.fill(colors["wooden"])
        map_size = [len(self.game_engine.map), len(self.game_engine.map[0])]

        if self.game_engine.map:
            for i in range(map_size[0]):
                for j in range(map_size[1]):
                    self.draw_object(self.game_engine.map[i][j].sprite, (i, j))
        else:
            self.fill(colors["white"])

    def draw_object(self, sprite, coord):
        x, y = self.get_pos((coord[0], coord[1]))
        self.blit(sprite, (x, y))

    def draw(self, canvas):
        self.prepare_view()
        self.draw_map()

        for obj in self.game_engine.objects:
            self.draw_object(obj.sprite, obj.position)

        self.draw_hero()

        super().draw(canvas)


class MiniMap(ScreenHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = 4
        self.alpha = 198
        self.colors = {"hero": (255, 0, 255),
                       "wall": (80, 15, 15, self.alpha),
                       "ground": (168, 168, 168, self.alpha),
                       "object": (255, 255, 0),
                       "enemy": (255, 0, 0),
                       "ally": (0, 255, 0)
                       }

    def connect_engine(self, engine):
        self.game_engine = engine
        super().connect_engine(self.game_engine)

    def get_position(self, x, y):
        return x * self.size, y * self.size

    def draw_object(self, color, coord):
        x, y = self.get_position(coord[0], coord[1])
        pygame.draw.rect(self, color, (x, y, self.size, self.size))

    def draw(self, canvas):
        self.fill((0, 0, 0, 0))
        if self.game_engine.show_minimap:
            for i in range(len(self.game_engine.map)):
                for j in range(len(self.game_engine.map[0])):
                    if not self.game_engine.map[i][j].free:
                        self.draw_object(self.colors["wall"], (i, j))
                    else:
                        self.draw_object(self.colors["ground"], (i, j))

            for obj in self.game_engine.objects:
                if isinstance(obj, Ally):
                    self.draw_object(self.colors["ally"], obj.position)
                if isinstance(obj, Enemy):
                    self.draw_object(self.colors["enemy"], obj.position)

            self.draw_object(self.colors["hero"], self.game_engine.hero.position)
        super().draw(canvas)


class ProgressBar(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def connect_engine(self, engine):
        self.game_engine = engine
        super().connect_engine(self.game_engine)

    def draw(self, canvas):
        self.fill(colors["wooden"])
        pygame.draw.rect(self, colors["black"], (50, 30, 200, 30), 2)
        pygame.draw.rect(self, colors["black"], (50, 70, 200, 30), 2)

        pygame.draw.rect(self, colors[
            "red"], (50, 30, 200 * self.game_engine.hero.hp / self.game_engine.hero.max_hp, 30))
        pygame.draw.rect(self, colors["green"], (50, 70,
                                                 200 * self.game_engine.hero.exp / (
                                                         100 * (2 ** (self.game_engine.hero.level - 1))), 30))

        font = pygame.font.SysFont("comicsansms", 16)
        self.blit(font.render(f'Hero at {self.game_engine.hero.position}', True, colors["black"]),
                  (250, 0))

        self.blit(font.render(f'{self.game_engine.level} floor', True, colors["black"]),
                  (10, 0))

        self.blit(font.render(f'HP', True, colors["black"]),
                  (10, 30))
        self.blit(font.render(f'Exp', True, colors["black"]),
                  (10, 70))

        self.blit(font.render(f'{self.game_engine.hero.hp}/{self.game_engine.hero.max_hp}', True, colors["black"]),
                  (60, 30))
        self.blit(
            font.render(f'{self.game_engine.hero.exp}/{(100 * (2 ** (self.game_engine.hero.level - 1)))}', True,
                        colors["black"]),
            (60, 70))

        self.blit(font.render(f'Level', True, colors["black"]),
                  (300, 30))
        self.blit(font.render(f'Gold', True, colors["black"]),
                  (300, 70))

        self.blit(font.render(f'{self.game_engine.hero.level}', True, colors["black"]),
                  (360, 30))
        self.blit(font.render(f'{self.game_engine.hero.gold}', True, colors["black"]),
                  (360, 70))

        self.blit(font.render(f'Str', True, colors["black"]),
                  (420, 30))
        self.blit(font.render(f'Luck', True, colors["black"]),
                  (420, 70))

        self.blit(font.render(f'{self.game_engine.hero.stats["strength"]}', True, colors["black"]),
                  (480, 30))
        self.blit(font.render(f'{self.game_engine.hero.stats["luck"]}', True, colors["black"]),
                  (480, 70))

        self.blit(font.render(f'SCORE', True, colors["black"]),
                  (550, 30))
        self.blit(font.render(f'{self.game_engine.score:.4f}', True, colors["black"]),
                  (550, 70))

        super().draw(canvas)


class InfoWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)

    def update(self, value):
        self.data.append(f"> {str(value)}")

    def draw(self, canvas):
        self.fill(colors["wooden"])

        font = pygame.font.SysFont("comicsansms", 10)
        for i, text in enumerate(self.data):
            self.blit(font.render(text, True, colors["black"]),
                      (5, 20 + 18 * i))

        super().draw(canvas)

    def connect_engine(self, engine):
        engine.subscribe(self)
        self.game_engine = engine
        super().connect_engine(self.game_engine)


class HelpWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)
        self.data.append([" →", "Move Right"])
        self.data.append([" ←", "Move Left"])
        self.data.append([" ↑ ", "Move Top"])
        self.data.append([" ↓ ", "Move Bottom"])
        self.data.append([" H ", "Show Help"])
        self.data.append(["Num+", "Zoom +"])
        self.data.append(["Num-", "Zoom -"])
        self.data.append([" R ", "Restart Game"])
        self.data.append([" M ", "Show/Hide Minimap"])
        self.data.append([" C ", "Show/Hide stats"])

    def connect_engine(self, engine):
        self.game_engine = engine
        super().connect_engine(self.game_engine)

    def draw(self, canvas):
        alpha = 0
        if self.game_engine.show_help:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        if self.game_engine.show_help:
            pygame.draw.lines(self, (255, 0, 0, 255), True, [
                (0, 0), (700, 0), (700, 500), (0, 500)], 5)
            for i, text in enumerate(self.data):
                self.blit(font1.render(text[0], True, ((128, 128, 255))),
                          (50, 50 + 30 * i))
                self.blit(font2.render(text[1] + " " + str(i), True, ((128, 128, 255))),
                          (150, 50 + 30 * i))

        super().draw(canvas)
