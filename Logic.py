import pygame


class GameEngine:
    objects = []
    map = None
    hero = None
    level = -1
    working = True
    subscribers = set()
    score = 0.
    game_process = True
    show_help = False
    show_minimap = True

    def subscribe(self, obj):
        self.subscribers.add(obj)

    def unsubscribe(self, obj):
        if obj in self.subscribers:
            self.subscribers.remove(obj)

    def notify(self, message):
        for i in self.subscribers:
            i.update(message)

    # HERO
    def add_hero(self, hero):
        self.hero = hero

    def interact(self):
        for obj in self.objects:
            if list(obj.position) == self.hero.position:
                self.delete_object(obj)
                obj.interact(self, self.hero)

        for msg in self.hero.level_up():
            self.notify(msg)

    # MOVEMENT
    def move_up(self):
        self.score -= 0.02
        if not self.map[self.hero.position[0]][self.hero.position[1] - 1].free:
            return
        self.hero.position[1] -= 1
        self.interact()

    def move_down(self):
        self.score -= 0.02
        if not self.map[self.hero.position[0]][self.hero.position[1] + 1].free:
            return
        self.hero.position[1] += 1
        self.interact()

    def move_left(self):
        self.score -= 0.02
        if not self.map[self.hero.position[0] - 1][self.hero.position[1]].free:
            return
        self.hero.position[0] -= 1
        self.interact()

    def move_right(self):
        self.score -= 0.02
        if not self.map[self.hero.position[0] + 1][self.hero.position[1]].free:
            return
        self.hero.position[0] += 1
        self.interact()

    # MAP
    def load_map(self, game_map):
        self.map = game_map

    # OBJECTS
    def add_object(self, obj):
        self.objects.append(obj)

    def add_objects(self, objects):
        self.objects.extend(objects)

    def delete_object(self, obj):
        self.objects.remove(obj)

    def zoom_in(self):
        self.sprite_size += 1 if self.sprite_size < 120 else 0
        self.resize_sprite()

    def zoom_out(self):
        self.sprite_size -= 1 if self.sprite_size > 1 else 0
        self.resize_sprite()

    def resize_sprite(self):
        for obj in self.objects:
            new_sprite = pygame.transform.scale(obj.orig_sprite, (self.sprite_size, self.sprite_size))
            obj.sprite = new_sprite

        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                new_sprite = pygame.transform.scale(self.map[j][i].orig_sprite, (self.sprite_size, self.sprite_size))
                self.map[j][i].sprite = new_sprite


