#!/usr/bin/python3

import curses


def DrawBoard(row, col, stdscr):
    """
    Drawing the board.
    @type row: int
    @param row: how many rows
    @type col: int
    @param col: how many coloums
    @type stdscr: object
    @param stdscr: determind the size of the board
    """
    trueCol = col * 2 # spacing
    for y in range(0, row):
        for x in range(0, trueCol):
            if x % 2 == 0:
                stdscr.addstr(y, x, "_")
            else:
                stdscr.addstr(y, x, " ")


