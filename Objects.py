from abc import ABC, abstractmethod
import pygame
import random


class Interactive(ABC):
    @abstractmethod
    def interact(self, engine, hero):
        pass


class AbstractObject(ABC):
    def __init__(self):
        pass

    def draw(self, display):
        display.blit(self.sprite, self.position)


class Creature(AbstractObject):
    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.orig_sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2


class Hero(Creature):
    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.hero_size = icon.get_height()
        self.dead = False
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp


class Ally(AbstractObject, Interactive):
    def __init__(self, icon, action, position):
        self.sprite = icon
        self.orig_sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


class Enemy(Creature, Interactive):
    def __init__(self, icon, stats, exp, position):
        super().__init__(icon, stats, position)
        self.exp = exp
        self.calc_max_HP()
        self.hp = self.max_hp

    def interact(self, engine, hero):

        while hero.hp > 0 and self.hp > 0:
            if self.critical(hero.stats["luck"], self.stats["luck"]):
                self.hp -= hero.stats["strength"] * 2
            else:
                self.hp -= hero.stats["strength"]
            if self.hp <= 0:
                break
            hero.hp -= self.stats["strength"]

        if hero.hp > 0:
            hero.exp += self.exp
            gold = self.exp + random.randint(1, self.exp)
            hero.gold += gold
            engine.notify(f"{gold} gold added")
            engine.score += self.exp / 100
        else:
            hero.dead = True

    def critical(self, hero_luck, enemy_luck):
        h_chance = random.randint(0, hero_luck)
        e_chance = random.randint(0, enemy_luck)
        if h_chance >= e_chance:
            return True
        else:
            return False


class Effect(Hero):
    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @sprite.setter
    def sprite(self, value):
        self.base.sprite = value

    @property
    def hero_size(self):
        return self.base.hero_size

    @property
    def dead(self):
        return self.base.dead

    @dead.setter
    def dead(self, value):
        self.base.dead = value

    @abstractmethod
    def apply_effect(self):
        pass


class Berserk(Effect):
    def apply_effect(self):
        self.stats["strength"] += 7
        self.stats["endurance"] += 7
        self.stats["luck"] += 7
        self.stats["intelligence"] -= 3
        self.calc_max_HP()
        super().apply_effect()


class Blessing(Effect):
    def apply_effect(self):
        self.stats["strength"] += 2
        self.stats["endurance"] += 2
        self.stats["luck"] += 2
        self.stats["intelligence"] += 2
        self.calc_max_HP()
        super().apply_effect()


class Weakness(Effect):
    def apply_effect(self):
        self.stats["strength"] -= 4
        self.stats["endurance"] -= 4
        super().apply_effect()

class Power(Effect):
    def apply_effect(self):
        self.stats["strength"] += 15
        super().apply_effect()
