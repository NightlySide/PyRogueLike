# -*- coding: utf-8 -*-

import unicurses as curses
from core import gfx
from core import world
from core import gui
from core import log
from core import items

class Game():
    def __init__(self):
        self.screen = None
        self.running = False
        self.world = world.World()
        self.gui = gui.Gui()
        self.console = None

    def loop(self):
        c = None
        while self.running:
            c = self.screen.getch()
            self.keys(c)

            #Drawing Graphics
            self.world.draw()
            self.gui.draw()

    def keys(self, c):
        if c == curses.KEY_UP:              self.world.player.move(0, -1, self.world)
        elif c == curses.KEY_DOWN:          self.world.player.move(0, 1, self.world)
        elif c == curses.KEY_LEFT:          self.world.player.move(-1, 0, self.world)
        elif c == curses.KEY_RIGHT:         self.world.player.move(1, 0, self.world)
        elif c == ord("q"):                 self.running = False #Touche esc
        elif c == ord("o"):
            d = self.world.cellData(self.world.player.y, self.world.player.x)
            if isinstance(d, items.Chest):
                self.gui.log("Chest Found !!")
            else:
                self.gui.log("There is nothing to open")
        elif c == ord("h"):
            self.world.player.life += 1
            self.gui.log("Healed !")
        elif c == ord("m"):
            self.gui.open_modal("[Quest] Your first one", "This has been a long time.\nYou won't be disappointed!")

    def play(self):
        log.log("Launching the game")
        gfx.start()
        self.running = True
        self.screen = gfx.scr()
        self.gui.init()
        self.gui.owner = self.world.player

        self.loop()
        self.quit()

    def quit(self):
        gfx.stop()
        log.log("Stopping the game")