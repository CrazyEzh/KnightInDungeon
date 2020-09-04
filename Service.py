import pygame
import random
import yaml
import os
import Objects
import Settings


class Cell:
    """
    Класс для описания ячейски карты, содержит спрайт и проходиомсть участка
    """

    def __init__(self, sprite, free=True):
        self.sprite = sprite
        self.orig_sprite = sprite
        self.free = free


class MapFactory(yaml.YAMLObject):

    @classmethod
    def from_yaml(cls, loader, node):
        _map = cls.create_map()
        _obj = cls.create_object()
        return {'map': _map, 'obj': _obj}

    @classmethod
    def create_map(cls):
        return cls.Map()

    @classmethod
    def create_object(cls):
        return cls.Objects()


class EndMap(MapFactory):
    yaml_tag = "!end_map"

    class Map:
        def __init__(self):
            self.Map = ['000000000000000000000000000000000000000',
                        '0                                     0',
                        '0                                     0',
                        '0  0   0   000   0   0  00000  0   0  0',
                        '0  0  0   0   0  0   0  0      0   0  0',
                        '0  000    0   0  00000  0000   0   0  0',
                        '0  0  0   0   0  0   0  0      0   0  0',
                        '0  0   0   000   0   0  00000  00000  0',
                        '0                                   0 0',
                        '0                                     0',
                        '000000000000000000000000000000000000000'
                        ]
            self.Map = list(map(list, self.Map))
            for i in self.Map:
                for j in range(len(i)):
                    i[j] = Cell(wall, free=False) if i[j] == '0' else Cell(floor1)

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            return self.objects


class RandomMap(MapFactory):
    yaml_tag = "!random_map"

    class Map:

        def __init__(self):
            self.Map = [[0 for _ in range(41)] for _ in range(41)]
            self.Map = list(map(list, self.Map))
            for i in range(41):
                for j in range(41):
                    if i == 0 or j == 0 or i == 40 or j == 40:
                        self.Map[j][i] = Cell(wall, free=False)
                    else:
                        rnd_sprite = [wall, floor1, floor2, floor3, floor1,
                                      floor2, floor3, floor1, floor2][random.randint(0, 8)]
                        if rnd_sprite == wall:
                            self.Map[j][i] = Cell(wall, free=False)
                        else:
                            self.Map[j][i] = Cell(rnd_sprite)

        def get_map(self):
            return self.Map

    class Objects:

        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            self.objects = get_objects(_map)
            return self.objects


class EmptyMap(MapFactory):
    yaml_tag = "!empty_map"

    class Map:

        def __init__(self):
            self.Map = [[0 for _ in range(41)] for _ in range(41)]
            self.Map = list(map(list, self.Map))
            for i in range(41):
                for j in range(41):
                    if i == 0 or j == 0 or i == 40 or j == 40:
                        self.Map[j][i] = Cell(wall, free=False)
                    else:
                        self.Map[j][i] = Cell(floor1)

        def get_map(self):
            return self.Map

    class Objects:

        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            self.objects = get_objects(_map)
            return self.objects


class SpecialMap(MapFactory):
    yaml_tag = "!special_map"

    class Map:

        def __init__(self):
            self.Map = self.get_table()
            self.maze_generator()
            for i in range(41):
                for j in range(41):
                    if i == 0 or j == 0 or i == 40 or j == 40:
                        self.Map[j][i] = Cell(wall, free=False)
                        continue
                    if self.Map[j][i] == "0":
                        if random.randint(0, 4) != 1:
                            self.Map[j][i] = Cell(wall, free=False)  # убираем 20% стен в случайном порядке
                            continue
                    rnd_sprite = [floor1, floor2, floor3, floor1,
                                  floor2, floor3, floor1, floor2][random.randint(0, 7)]
                    self.Map[j][i] = Cell(rnd_sprite)

        def maze_generator(self):
            current_position = (1, 1)
            self.Map[1][1] = 1
            unvisited_list = self.get_unvisited_cells()
            height = len(self.Map[0]) - 1
            width = len(self.Map) - 1
            path = [(1, 1)]
            while len(unvisited_list) > 0:
                neighbours = self.get_neighbours(current_position, width, height)
                if len(neighbours) > 0:
                    rand_cell = random.randint(0, len(neighbours) - 1)
                    neighbour = neighbours[rand_cell]
                    self.remove_wall(current_position, neighbour)
                    current_position = (neighbour[0], neighbour[1])
                    self.Map[neighbour[0]][neighbour[1]] = 1
                    path.append(current_position)
                elif len(path) > 0:
                    current_position = path.pop()
                else:
                    rnd_unvisited = random.randint(0, len(unvisited_list) - 1)
                    current_position = unvisited_list[rnd_unvisited]
                if current_position in unvisited_list:
                    unvisited_list.remove(current_position)

        def remove_wall(self, start, end):
            x_diff = end[0] - start[0]
            y_diff = end[1] - start[1]

            add_x = x_diff / abs(x_diff) if x_diff != 0 else 0
            add_y = y_diff / abs(y_diff) if y_diff != 0 else 0
            target_x = start[0] + int(add_x)
            target_y = start[1] + int(add_y)
            self.Map[target_x][target_y] = 1

        def get_unvisited_cells(self):
            result = []
            for i in range(len(self.Map)):
                for j in range(len(self.Map[0])):
                    if self.Map[j][i] == " ":
                        result.append((j, i))
            return result

        def get_neighbours(self, cell, width, height):
            cells = [(cell[0], cell[1] - 2), (cell[0], cell[1] + 2), (cell[0] - 2, cell[1]), (cell[0] + 2, cell[1])]
            result = []
            for i in cells:
                if 0 < i[0] < width and 0 < i[1] < height:
                    if self.Map[i[0]][i[1]] == " ":
                        result.append(i)
            return result

        def get_table(self):
            _map = [[0 for _ in range(41)] for _ in range(41)]
            for i in range(41):
                for j in range(41):
                    if i % 2 == 0 or j % 2 == 0:
                        _map[j][i] = "0"
                    else:
                        _map[j][i] = " "
            return _map

        def get_map(self):
            return self.Map

    class Objects:

        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            self.objects = get_objects(_map)
            return self.objects


def get_objects(_map):
    objects = []
    for obj_name in object_list_prob['objects']:
        prop = object_list_prob['objects'][obj_name]
        for i in range(random.randint(prop['min-count'], prop['max-count'])):
            coord = (random.randint(1, 39), random.randint(1, 39))
            intersect = True
            while intersect:
                intersect = False
                if not _map[coord[0]][coord[1]].free:
                    intersect = True
                    coord = (random.randint(1, 39),
                             random.randint(1, 39))
                    continue
                for obj in objects:
                    if coord == obj.position or coord == (1, 1):
                        intersect = True
                        coord = (random.randint(1, 39),
                                 random.randint(1, 39))

            objects.append(Objects.Ally(
                prop['sprite'], prop['action'], coord))

    for obj_name in object_list_prob['ally']:
        prop = object_list_prob['ally'][obj_name]
        for i in range(random.randint(prop['min-count'], prop['max-count'])):
            coord = (random.randint(1, 39), random.randint(1, 39))
            intersect = True
            while intersect:
                intersect = False
                if not _map[coord[0]][coord[1]].free:
                    intersect = True
                    coord = (random.randint(1, 39),
                             random.randint(1, 39))
                    continue
                for obj in objects:
                    if coord == obj.position or coord == (1, 1):
                        intersect = True
                        coord = (random.randint(1, 39),
                                 random.randint(1, 39))
            objects.append(Objects.Ally(
                prop['sprite'], prop['action'], coord))

    for obj_name in object_list_prob['enemies']:
        prop = object_list_prob['enemies'][obj_name]
        for i in range(random.randint(0, 5)):
            coord = (random.randint(1, 30), random.randint(1, 22))
            intersect = True
            while intersect:
                intersect = False
                if not _map[coord[0]][coord[1]].free:
                    intersect = True
                    coord = (random.randint(1, 39),
                             random.randint(1, 39))
                    continue
                for obj in objects:
                    if coord == obj.position or coord == (1, 1):
                        intersect = True
                        coord = (random.randint(1, 39),
                                 random.randint(1, 39))

            objects.append(Objects.Enemy(
                prop['sprite'], prop, prop['experience'], coord))

    return objects


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
    sprite.blit(icon, (0, 0))
    return sprite


def restore_hp(engine, hero):
    engine.score += 0.1
    hero.hp = hero.max_hp
    engine.notify("HP restored")


def apply_blessing(engine, hero):
    if hero.gold >= int(20 * 1.5 ** engine.level) - 2 * hero.stats["intelligence"]:
        engine.score += 0.2
        hero.gold -= int(20 * 1.5 ** engine.level) - \
                     2 * hero.stats["intelligence"]
        if random.randint(0, 1) == 0:
            engine.hero = Objects.Blessing(hero)
            engine.hero.calc_max_HP()
            engine.notify("Blessing applied")
        else:
            engine.hero = Objects.Berserk(hero)
            engine.hero.calc_max_HP()
            engine.notify("Berserk applied")
    else:
        engine.score -= 0.1


def apply_power(engine, hero):
    if hero.gold >= int(20 * 1.5 ** engine.level) - 2 * hero.stats["intelligence"]:
        engine.score += 0.2
        hero.gold -= int(20 * 1.5 ** engine.level) - \
                     2 * hero.stats["intelligence"]
        engine.hero = Objects.Power(hero)
        engine.notify("Power applied")
    else:
        engine.score -= 0.1


def remove_effect(engine, hero):
    if hero.gold >= int(10 * 1.5 ** engine.level) - 2 * hero.stats["intelligence"] and "base" in dir(hero):
        hero.gold -= int(10 * 1.5 ** engine.level) - \
                     2 * hero.stats["intelligence"]
        engine.hero = hero.base
        engine.hero.calc_max_HP()
        if engine.hero.hp > engine.hero.max_hp:
            engine.hero.hp = engine.hero.max_hp
        engine.notify("Effect removed")


def add_gold(engine, hero):
    if random.randint(1, 10) == 1:
        engine.score -= 0.05
        engine.hero = Objects.Weakness(hero)
        engine.hero.calc_max_HP()
        engine.notify("You were cursed")
    else:
        engine.score += 0.1
        gold = int(random.randint(10, 1000) * (1.1 ** (engine.hero.level - 1)))
        hero.gold += gold
        engine.notify(f"{gold} gold added")


def reload_game(engine, hero):
    global level_list
    level_list_max = len(level_list) - 1
    engine.level += 1
    hero.position = [1, 1]
    engine.objects = []
    generator = level_list[min(engine.level, level_list_max)]
    _map = generator['map'].get_map()
    engine.load_map(_map)
    engine.add_objects(generator['obj'].get_objects(_map))
    engine.add_hero(hero)


def service_init(sprite_size, full=True):
    global object_list_prob, level_list
    global wall, floor1, floor2, floor3
    wall = create_sprite(os.path.join("texture", "wall.png"), sprite_size)
    floor1 = create_sprite(os.path.join("texture", "Ground_1.png"), sprite_size)
    floor2 = create_sprite(os.path.join("texture", "Ground_2.png"), sprite_size)
    floor3 = create_sprite(os.path.join("texture", "Ground_3.png"), sprite_size)

    file = open("objects.yml", "r")

    object_list_tmp = yaml.load(file.read())
    if full:
        object_list_prob = object_list_tmp

    object_list_actions = {'reload_game': reload_game,
                           'add_gold': add_gold,
                           'apply_blessing': apply_blessing,
                           'apply_power': apply_power,
                           'remove_effect': remove_effect,
                           'restore_hp': restore_hp}

    for obj in object_list_prob['objects']:
        prop = object_list_prob['objects'][obj]
        prop_tmp = object_list_tmp['objects'][obj]
        prop['sprite'] = create_sprite(
            os.path.join(Settings.OBJECT_TEXTURE, prop_tmp['sprite'][0]), sprite_size)
        prop['action'] = object_list_actions[prop_tmp['action']]
        prop['img'] = prop_tmp['sprite']

    for ally in object_list_prob['ally']:
        prop = object_list_prob['ally'][ally]
        prop_tmp = object_list_tmp['ally'][ally]
        prop['sprite'] = create_sprite(
            os.path.join(Settings.ALLY_TEXTURE, prop_tmp['sprite'][0]), sprite_size)
        prop['action'] = object_list_actions[prop_tmp['action']]
        prop['img'] = prop_tmp['sprite']

    for enemy in object_list_prob['enemies']:
        prop = object_list_prob['enemies'][enemy]
        prop_tmp = object_list_tmp['enemies'][enemy]
        prop['sprite'] = create_sprite(
            os.path.join(Settings.ENEMY_TEXTURE, prop_tmp['sprite'][0]), sprite_size)
        prop['img'] = prop_tmp['sprite']

    file.close()

    if full:
        file = open("levels.yml", "r")
        level_list = yaml.load(file.read())['levels']
        level_list.append({'map': EndMap.Map(), 'obj': EndMap.Objects()})
        file.close()
