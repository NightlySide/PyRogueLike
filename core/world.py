# -*- coding: utf-8 -*-

import math

from core import gfx
from core import utils
from core import log
from core import entity

class World:
    def __init__(self):
        #self.map = utils.textToMap("data/map.txt")
        self.map = utils.generateMap(29,71)
        self.min_y = 0
        self.min_x = 0
        self.w = len(self.map[0])
        self.h = len(self.map)
        self.seen = [[0 for i in range(self.w)] for j in range(self.h)]
        self.player = entity.Player("Character Random Name", 4, 6)
        self.entities = utils.jsonToEntities("data/ent_map.json")
        self.chests = utils.jsonToChests("data/items.json")
        self.moving = True
        self.fov = None

        log.log("{} entité(s) chargée(s)".format(len(self.entities)))

        log.log("-----Debut Map------")
        for y in self.map:
            tLigne = ""
            for x in y:
                tLigne+=x
            log.log(tLigne)
        log.log("-----Fin Map------")
        log.log("Taille map : {}x{}".format(self.h, self.w))

    def cellData(self, y, x):
        data = None
        for e in self.entities:
            if (e.y, e.x) == (y, x):
                data = e
        for c in self.chests:
            if (c.y, c.x) == (y, x):
                data = c
        return data

    def is_free(self, y, x):
        if x < 0 or y < 0 or x >= self.w or y >= self.h:
            return False
        c = self.map[y][x]
        if c != "#" and c != "H":
            empty = True
            ent = None
            for e in self.entities:
                if (e.x, e.y) == (x, y):
                    empty = False
                    ent = e
            if (self.player.x, self.player.y) == (x, y):
                empty = False
                ent = e
            if empty:
                return True
            else:
                return ent
        return False

    def draw(self):
        gfx.clear()
        if self.moving:
            self.fov = self.raycast(10, 3)
            self.max_y = gfx.scr().getmaxyx()[0]
            self.max_x = int(0.60*gfx.scr().getmaxyx()[1])
            for e in self.entities:
                e.randomMove(self)
            self.moving = False
        for y in range(self.min_y, self.max_y):
            for x in range(self.min_x, self.max_x):
                if (self.player.x, self.player.y) == (x, y):
                    gfx.draw(y, x, "☺", "b")
                elif y>=0 and x>=0 and y<len(self.fov) and x<len(self.fov[0]):
                    if self.fov[y][x] == 1:
                        empty = True
                        for e in self.entities:
                            if (x, y) == (e.x, e.y):
                                empty = False
                                gfx.draw(y, x, e.char, "r")
                        for c in self.chests:
                            if (c.x, c.y) == (x, y):
                                empty = False
                                gfx.draw(y, x, "÷", "c")
                        if empty:
                                c = self.map[y][x]
                                gfx.draw(y, x, c, "g" if c == "." else "y")
                        self.seen[y][x] = 1
                    elif self.seen[y][x]:
                        empty = True
                        for c in self.chests:
                            if (c.x, c.y) == (x, y):
                                empty = False
                                gfx.draw(y, x, "÷", "dc")
                        if empty:
                            c = self.map[y][x]
                            gfx.draw(y, x, c, "dg" if c == "." else "dy")

    def raycast(self, radius, step=3):
        fov = [[0 for i in range(self.w)] for j in range(self.h)]

        for i in range(0, 360+1, step):
            ax = math.sin(i)
            ay = math.cos(i)

            x = self.player.x
            y = self.player.y

            for z in range(radius):
                x += ax
                y += ay
                if x < 0 or y < 0 or x > self.w or y > self.h:
                    break

                try:
                    fov[int(round(y))][int(round(x))] = 1

                    if self.map[int(round(y))][int(round(x))] == "#":
                        break
                except: pass
        return fov