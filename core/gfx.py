# -*- coding: utf-8 -*-

import unicurses as curses
from core import log

def color(fg="w"):
    fg = fg.lower()

    colors = ["n","k","db","dg","dc","dr","dp","dy","dw","dn","b","g","c","r","p","y","w"]

    if fg not in colors:
        fg = "w"

    i = colors.index(fg)

    if fg == "w":
        return curses.color_pair(0)

    #log.log("Couleur : "+str(i))

    return curses.color_pair(i)

def start():
    global screen
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    screen.keypad(1)
    screen.nodelay(1)
    curses.nonl()
    screen.scrollok(False)
    curses.start_color()

    for i in range(0, 17):
        curses.init_pair(i+1, i, 0)
        #log.log("Pair : ({}, {}, 0)".format(i+1,i))

    h, w = screen.getmaxyx()
    log.log("Screen size : {}x{}".format(h, w))


def stop():
    global screen
    curses.nocbreak()
    screen.timeout(-1)
    curses.curs_set(1)
    screen.keypad(0)
    curses.nl()
    screen.scrollok(True)
    curses.echo()
    curses.endwin()

def scr():
    return screen

def clear():
    global screen
    if screen:
        screen.erase()

def draw(y, x, c, col=""):
    global screen
    if screen:
        h, w = screen.getmaxyx()
        if x >= 0 and x < w and y >=0 and y < h and (x,y) != (w-1, h-1):
            screen.addch(y, x, c, color(col))