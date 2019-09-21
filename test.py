#!/usr/bin/python3

import curses

# screen = curses.initscr()
# screen.addstr(1,1, "Hello")
# screen.refresh()
# curses.napms(3000)
# curses.endwin
playerIcon = "Y"
emptyBlock = "_"

# Displaying Characters
def display(character, posY, posX, screen):
    screen.addstr(posY, posX, character)


def main(stdscr):
    row = 10
    col = 20
    playerPosY = 0
    playerPosX = 0
    player = playerIcon
    trueCol = col * 2
    curses.curs_set(0)



    for y in range (0, row):
        for x in range (0, trueCol):
            if x % 2 == 0:
                stdscr.addstr(y,x, "_")
            else:
                stdscr.addstr(y,x, " ")

    #HardCoded initial position for player Y
    stdscr.addstr(0, 0, player)

    while True:
        key = stdscr.getch()
        # stdscr.clear()
        if key == curses.KEY_UP:
            display(emptyBlock, playerPosY, playerPosX, stdscr)
            playerPosY = playerPosY - 1
            display(player, playerPosY, playerPosX, stdscr)
        elif key == curses.KEY_DOWN:
            display(emptyBlock, playerPosY, playerPosX, stdscr)
            playerPosY = playerPosY + 1
            display(player, playerPosY, playerPosX, stdscr)
        elif key == curses.KEY_LEFT:
            display(emptyBlock, playerPosY, playerPosX, stdscr)
            playerPosX = playerPosX - 2
            display(player, playerPosY, playerPosX, stdscr)
        elif key == curses.KEY_RIGHT:
            display(emptyBlock, playerPosY, playerPosX, stdscr)
            playerPosX = playerPosX + 2
            display(player, playerPosY, playerPosX, stdscr)
        stdscr.refresh()

curses.wrapper(main)

