# -*- coding: utf-8 -*-

import random

class Entity:
    def __init__(self, name, y, x, char="", life = 10, level = 1):
        self.name = name
        self.x = x
        self.y = y
        self.isDead = False
        self.target = None
        self.maxlife = life
        self.life = self.maxlife*0.4
        self.level = level
        self.strength = 5

        if char != "":
            self.char = char
        else:
            self.char = name[0]

    def getLifePercentage(self):
        return self.life/self.maxlife

    def move(self, x, y, world):
        if not self.isDead:
            pos = self.y+y, self.x+x
            cellfree = world.is_free(*pos)
            if cellfree:
                self.y, self.x = pos
            elif isinstance(cellfree, Entity):
                ent = cellfree
                self.attack(ent)

    def randomMove(self, world):
        if random.random() > 0.5:
            mov = [[0,0], [0,1], [1,0], [0,-1], [-1,0]]
            r = random.randrange(len(mov))
            movement = mov[r]
            self.move(*movement, world)

    def attack(self, entity):
        self.entity.life -= self.strength
        entity.checkIsAlive()

    def checkIsAlive(self):
        if self.life<=0:
            self.isDead = True
        if self.isDead:
            self.char = "%"

class Enemy(Entity):
    def __init__(self, name, y, x, char = "", life = 10, level = 1):
        super().__init__(name, y, x, char, life, level)
        self.target = None

    def randomMove(self, world):
        if not self.isDead:
            d = ((world.player.x-self.x)**2+(world.player.y-self.y)**2)**(1/2)
            if d < 10:
                if random.random() < 0.9:
                    x = 0
                    y = 0
                    if world.player.x-self.x<0:
                        x = -1
                    elif world.player.x-self.x == 0:
                        x = 0
                    else:
                        x = 1
                    if world.player.y-self.y<0:
                        y = -1
                    elif world.player.y-self.y == 0:
                        y = 0
                    else:
                        y = 1
                    if y != 0 and x != 0:
                        if random.random() < 0.5:
                            y = 0
                        else:
                            x = 0
                    self.move(x, y, world)
            else:
                super().randomMove(world)

class Player(Entity):
    def __init__(self, name, y, x, life = 20, level = 1):
        super().__init__(name, y, x, "☺", life, level)
        self.isInMenu = False

    def move(self, x, y, world):
        super().move(x, y, world)
        world.moving = True