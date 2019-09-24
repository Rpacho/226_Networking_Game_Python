#!/usr/bin/python3

import curses
import GameManager
import time

row = 10
col = 20
posY = 0
posX = 0

def update(positionY, positionX):
    posY = positionY
    posX = positionX

def main(stdscr):
    GameManager.DrawBoard(row,col,stdscr)
    while True:
        stdscr.addstr(posY,posX, "Y")
        stdscr.refresh()
curses.wrapper(main)