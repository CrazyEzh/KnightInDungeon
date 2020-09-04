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
            self.MapList = ['000000000000000000000000000000000000000',
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
            self.Map = list(map(list, self.MapList))
            for i in self.Map:
                for j in range(len(i)):
                    i[j] = wall if i[j] == '0' else floor1

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
            self.MapList = [[0 for _ in range(41)] for _ in range(41)]
            self.Map = list(map(list, self.MapList))
            for i in range(41):
                for j in range(41):
                    if i == 0 or j == 0 or i == 40 or j == 40:
                        self.Map[j][i] = wall
                    else:
                        self.Map[j][i] = [wall, floor1, floor2, floor3, floor1,
                                          floor2, floor3, floor1, floor2][random.randint(0, 8)]

        def get_map(self):
            return self.Map

    class Objects:

        def __init__(self):
            self.objects = []

        def get_objects(self, _map):

            for obj_name in object_list_prob['objects']:
                prop = object_list_prob['objects'][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = (random.randint(1, 39), random.randint(1, 39))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, 39),
                                     random.randint(1, 39))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, 39),
                                         random.randint(1, 39))

                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))

            for obj_name in object_list_prob['ally']:
                prop = object_list_prob['ally'][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = (random.randint(1, 39), random.randint(1, 39))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, 39),
                                     random.randint(1, 39))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, 39),
                                         random.randint(1, 39))
                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))

            for obj_name in object_list_prob['enemies']:
                prop = object_list_prob['enemies'][obj_name]
                for i in range(random.randint(0, 5)):
                    coord = (random.randint(1, 30), random.randint(1, 22))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, 39),
                                     random.randint(1, 39))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, 39),
                                         random.randint(1, 39))

                    self.objects.append(Objects.Enemy(
                        prop['sprite'], prop, prop['experience'], coord))

            return self.objects


class EmptyMap(MapFactory):
    yaml_tag = "!empty_map"

    class Map:

        def __init__(self):
            self.MapList = ['000000000000000000000000000000',
                            '0                            0',
                            '0                            0',
                            '0                            0',
                            '0                            0',
                            '0                            0',
                            '0                            0',
                            '0                            0',
                            '0                            0',
                            '0                            0',
                            '000000000000000000000000000000'
                            ]

            self.Map = list(map(list, self.MapList))
            for i in range(len(self.Map)):
                for j in range(len(self.Map[0])):
                    self.Map[i][j] = wall if self.Map[i][j] == '0' else floor1

        def get_map(self):
            return self.Map

    class Objects:

        def __init__(self):
            self.objects = []

        def get_objects(self, _map):

            prop = object_list_prob['objects']["stairs"]
            coord = (random.randint(1, len(_map[0]) - 1), random.randint(1, len(_map) - 1))
            intersect = True
            while intersect:
                intersect = False
                if _map[coord[1]][coord[0]] == wall:
                    intersect = True
                    coord = (random.randint(1, len(_map[0]) - 1), random.randint(1, len(_map) - 1))
                    continue
                for obj in self.objects:
                    if coord == obj.position or coord == (1, 1):
                        intersect = True
                        coord = (random.randint(1, len(_map[0]) - 1), random.randint(1, len(_map) - 1))

            self.objects.append(Objects.Ally(
                prop['sprite'], prop['action'], coord))
            return self.objects


class SpecialMap(MapFactory):
    yaml_tag = "!special_map"

    class Map:

        def __init__(self):
            self.Map = self.get_table()
            self.maze_generator()
            self.MapList = self.Map.copy()
            for i in range(41):
                for j in range(41):
                    if i == 0 or j == 0 or i == 40 or j == 40:
                        self.Map[j][i] = wall
                        continue
                    if self.Map[j][i] == 0:
                        if random.randint(0, 4) != 1:  # убираем 20% стен в случайном порядке
                            self.Map[j][i] = wall
                            continue
                    self.Map[j][i] = floor1

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
                # unvisited_list = self.get_unvisited_cells()

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
            cells = []
            cells.append((cell[0], cell[1] - 2))
            cells.append((cell[0], cell[1] + 2))
            cells.append((cell[0] - 2, cell[1]))
            cells.append((cell[0] + 2, cell[1]))
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
                        _map[j][i] = 0
                    else:
                        _map[j][i] = " "
            return _map

        def get_map(self):
            return self.Map

    class Objects:

        def __init__(self):
            self.objects = []

        def get_objects(self, _map):

            for obj_name in object_list_prob['enemies']:
                prop = object_list_prob['enemies'][obj_name]
                for i in range(random.randint(0, 5)):
                    coord = (random.randint(1, 30), random.randint(1, 22))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, 39),
                                     random.randint(1, 39))
                            continue
                        for obj in self.objects:
                            if coord == (1, 1) or coord == obj.position:
                                intersect = True
                                coord = (random.randint(1, 39),
                                         random.randint(1, 39))

                    self.objects.append(Objects.Enemy(
                        prop['sprite'], prop, prop['experience'], coord))

            for obj_name in object_list_prob['objects']:
                prop = object_list_prob['objects'][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = (random.randint(1, 39), random.randint(1, 39))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, 39),
                                     random.randint(1, 39))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, 39),
                                         random.randint(1, 39))

                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))

            for obj_name in object_list_prob['ally']:
                prop = object_list_prob['ally'][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = (random.randint(1, 39), random.randint(1, 39))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, 39),
                                     random.randint(1, 39))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, 39),
                                         random.randint(1, 39))
                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))

            return self.objects