# -*- coding: utf-8 -*-

import unicurses as curses

from core import gfx
from core import log
from core import utils

class Gui:
    def __init__(self):
        self.max_x = None
        self.max_y = None
        self.x = None
        self.y = None
        self.owner = None
        self.logs = []
        self.nbLines = 11
        self.show_modal = False
        self.modal = {}

    def init(self):
        self.max_x = gfx.scr().getmaxyx()[1]-1
        self.max_y = gfx.scr().getmaxyx()[0]-1
        self.x = int(0.60*self.max_x)
        self.y = 0

    def draw(self):
        self.draw_edges(self.y, self.x, self.max_y, self.max_x)
        self.draw_player_infos()

        #Console
        self.draw_separator(int(self.max_y/2)+2)
        self._print(int(self.max_y/2)+2, self.x+2, "[Console logs]", "dn")
        self.drawConsole()

        #Modal
        if self.show_modal:
            self.draw_modal(self.modal["title"], self.modal["text"])

        #Quit button
        off = 30
        self._print(self.max_y-1, self.x+off, "[", "w")
        self._print(self.max_y-1, self.x+off+1, "Press ", "n")
        self._print(self.max_y-1, self.x+off+7, "q", "g")
        self._print(self.max_y-1, self.x+off+8, " to quit", "n")
        self._print(self.max_y-1, self.x+off+16, "]", "w")

    def draw_player_infos(self):
        self._print(self.y+1, self.x+1, "Name : {}".format(self.owner.name))
        #Life and Mana
        self._print(self.y+2, self.x+1, "Life : ")
        w = int(((self.max_x-self.x) - len("Life : "))/2)-1
        self.draw_lifebar(self.y+2, self.x+8, w, self.owner.getLifePercentage(), "g")
        self.draw_lifebar(self.y+2, self.x+9+w, w, self.owner.getLifePercentage(), "c")

    def open_modal(self, title, text):
        self.show_modal = True
        self.modal = {"title" : title, "text" : text}

    def close_modal(self):
        self.show_modal = False

    def draw_modal(self, title, text):
        lines = text.split("\n")
        nbLines = len(lines)
        self.clear(4, 4, self.max_y-4, self.x-4)
        self.draw_edges(4, 4, self.max_y-4, self.x-4)
        self._print(4,8, title, "dn")
        for i in range(nbLines):
            self._print(6+i, 6, lines[i])
        #Close button
        off = 40
        self._print(self.max_y-5, 4+off, "[", "w")
        self._print(self.max_y-5, 4+off+1, "Press ", "n")
        self._print(self.max_y-5, 4+off+7, "Enter", "g")
        self._print(self.max_y-5, 4+off+12, " to close", "n")
        self._print(self.max_y-5, 4+off+21, "]", "w")
        #Waitforinput
        utils.waitForInput(utils.ENTER_KEY)
        self.close_modal()

    def _print(self, y, x, text, col="w", limit=0):
        i = 0
        j = 0
        for char in text:
            if limit != 0 and i >= limit:
                i = 0
                j += 1
            gfx.draw(y+j, x+i, char, col)
            i+=1

    def draw_lifebar(self, y, x, size, percent, col="g"):
        gfx.draw(y, x, "[", "w")
        gfx.draw(y, x+size, "]", "w")
        barsize = int((size-1)*percent)
        for i in range(0, barsize):
            gfx.draw(y, x+i+1, ":", col)

    def draw_edges(self, minY, minX, maxY, maxX):
        for i in range(minY+1, maxY-1):
            gfx.draw(i, minX, "║", "w")
            gfx.draw(i, maxX, "║", "w")

        for i in range(minX+1, maxX):
            gfx.draw(minY, i, "═", "w")
            gfx.draw(maxY-1, i, "═", "w")

        gfx.draw(minY, maxX, "╗", "w")
        gfx.draw(maxY-1, maxX, "╝", "w")
        gfx.draw(maxY-1, minX, "╚", "w")
        gfx.draw(minY, minX, "╔", "w")

    def draw_separator(self, y):
        gfx.draw(y, self.x, "╠", "w")
        gfx.draw(y, self.max_x, "╣", "w")
        for i in range(self.x+1, self.max_x):
            gfx.draw(y, i, "═", "w")

    def log(self, text):
        self.logs.append(text)
        if len(self.logs)>self.nbLines+15:
            self.logs.remove(self.logs[0])
        log.log(text)

    def drawConsole(self):
        nb=0
        rlogs = self.logs.copy()
        rlogs.reverse()
        if len(self.logs)<self.nbLines:
            nb = len(self.logs)
        else:
            nb = self.nbLines
        for i in range(nb):
            self._print(int(self.max_y/2)+2+self.nbLines-i,self.x+1, rlogs[i])

    def clear(self, minY, minX, maxY, maxX):
        for j in range(minY, maxY):
            for i in range(minX, maxX):
                gfx.draw(j, i, " ")