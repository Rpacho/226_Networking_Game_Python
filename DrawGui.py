#!/usr/bin/python3

import curses

# this Function is for Drawing the board
def DrawBoard(row, col, stdscr):
    trueCol = col * 2 # spacing
    for y in range(0, row):
        for x in range(0, trueCol):
            if x % 2 == 0:
                stdscr.addstr(y, x, "_")
            else:
                stdscr.addstr(y, x, " ")


