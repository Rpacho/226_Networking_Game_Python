#!/usr/bin/python3

import curses
import socket
import GameManager
from GameNetwork import Network
import struct

playerIcon = "Y"
row = 10
col = 20
player1 = playerIcon


######### MAIN #########
# Initiate prepack Curses and start the game
def main(stdscr):
    player = Network()
    playerPosY = 0
    playerPosX = 0
    curses.curs_set(0)

    # Calling the Function that draw the board
    GameManager.DrawBoard(row, col, stdscr)

    stdscr.addstr(playerPosY, playerPosX, player1)
# Player Control
    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP:
            asd = player.sendData("P")
            stdscr.addstr(10, 40, asd)
        #     playerPosY = playerPosY - 1
        #     stdscr.addstr(playerPosY, playerPosX, player)
        elif key == curses.KEY_DOWN:
            stdscr.addstr(playerPosY, playerPosX, "_")
            playerPosY = playerPosY + 1
            stdscr.addstr(playerPosY, playerPosX, player)
            dataPack = [playerPosY, playerPosX]
            asd = player.sendData(bytes(dataPack))
        elif key == curses.KEY_LEFT:
            stdscr.addstr(playerPosY, playerPosX, "_")
            playerPosX = playerPosX - 2
            stdscr.addstr(playerPosY, playerPosX, player)
        elif key == curses.KEY_RIGHT:
            stdscr.addstr(playerPosY, playerPosX, "_")
            playerPosX = playerPosX + 2
            stdscr.addstr(playerPosY, playerPosX, player)
        elif key == curses.KEY_ENTER:
            player.sendData("FIN")
        stdscr.refresh()

curses.wrapper(main)
