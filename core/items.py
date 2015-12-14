# -*- coding: utf-8 -*-

class Chest:
    def __init__(self, y, x, size, items=[]):
        self.x = x
        self.y = y
        self.size = size
        self.items = items

class Item:
    def __init__(self, name, itemType, desc=""):
        self.name = name
        self.type = itemType
        self.desc = desc

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, item):
        self.__dict__[key] = item

class Weapon(Item):
    def __init__(self, name, desc="", damage=0):
        super().__init__(name, "Weapon", desc)
        self.damage = damage

class Armor(Item):
    def __init__(self, name, desc="", armor=0):
        super().__init__(name, "Armor", desc)
        self.armor = armor