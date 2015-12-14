# -*- coding: utf-8 -*-

import math
import random
import json
import xml.etree.ElementTree as ET

from core import entity
from core import items
from core import gfx, log

ENTER_KEY = 13
SPACEBAR_KEY = 32

def neighbors(x, y, radius):
    report = []
    for i in range(x-radius, x+radius+1):
        for j in range(y-radius, y+radius+1):
            if (i, j) != (x, y):
                if math.sqrt(pow(x-i,2)+pow(y-j,2)) < radius+0.1:
                    report.append((i, j))
    return report

def waitForInput(key = None):
    c = -1
    if key == None:
        while str(c)=="-1":
            c = gfx.scr().getch()
        return c
    else:
        while str(c) != str(key):
            c = gfx.scr().getch()
            if c!=-1:
                log.log(str(c))

def textToMap(fileName):
    tMap = []
    file = open(fileName, "r")
    for line in file:
        tLine = []
        for char in line:
            if char == " ":
                tLine.append(".")
            elif char != "\n":
                tLine.append(char)
        tMap.append(tLine)
    return tMap

def xmlToEntities(fileName):
    tree = ET.parse(fileName)
    root = tree.getroot()
    ents = []
    for child in root:
        name = child.find("name").text
        position = child.find("position").attrib
        ent = entity.Entity(name, int(position["y"]), int(position["x"]), "%")
        ents.append(ent)
    return ents

def jsonToEntities(fileName):
    file = open(fileName, "r")
    data = json.load(file)
    ents = []
    for i in data:
        ent = data[i]
        name = ent["name"]
        position = ent["position"]
        char = ent["char"]
        entType = ent["type"].lower()
        if entType == "enemy":
            e = entity.Enemy(name, int(position["y"]), int(position["x"]))
        else:
            e = entity.Entity(name, int(position["y"]), int(position["x"]), char)
            greetings = ent["greetings"]
        ents.append(e)
    return ents

def jsonToChests(fileName):
    file = open(fileName, "r")
    data = json.load(file)
    chests = []
    for i in data:
        chest = data[i]
        size = chest["size"]
        cItems = []
        for i in chest["items"]:
            it = chest["items"][i]
            ite = dictToItem(it)
            cItems.append(ite)
        position = chest["position"]
        c = items.Chest(int(position["y"]), int(position["x"]), size, cItems)
        chests.append(c)
    return chests

def dictToItem(dic):
    name = dic["name"]
    desc = dic["description"]
    iType = dic["type"].lower()
    i = None
    if iType == "weapon":
        damage = dic["damage"]
        i = items.Weapon(name, desc, damage)
    elif iType == "armor":
        armor = dic["armor"]
        i = items.Armor(name, desc, armor)
    return i

def generateMap(h, w):
    carte = [["." for x in range(w)] for y in range(h)]
    nb = 150
    npose = 0
    while npose<nb:
        x = random.randrange(0, w)
        y = random.randrange(0, h)
        if carte[y][x] == ".":
            carte[y][x] = "#"
            npose += 1
    return carte