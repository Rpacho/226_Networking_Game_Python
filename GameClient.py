#!/usr/bin/python3

import curses
import socket
import GameManager
from GameNetwork import Network
import struct
import time

playerIcon = "Y"
row = 10
col = 20
player1 = playerIcon

# data Transmitting protocol
FLAG_POSITION = 0b0011
FLAG_BOARD_SIZE = 0b0111
FLAG_BOARD_TREASURE = 0b1111
FLAG_SPAWN_POINT = 0b0001

######### MAIN #########
# Initiate prepack Curses and start the game
def main(stdscr):
    net = Network()
    playerPosY = 0
    playerPosX = 0
    curses.curs_set(0)
    #GameManager.DrawBoard(10, 20, stdscr)
    try:
        gameBoardSize = net.sendData(FLAG_BOARD_SIZE, 0, 0)
        spawnPosition = net.sendData(FLAG_SPAWN_POINT, 0, 0)
        if(gameBoardSize[0] == FLAG_BOARD_SIZE):
            GameManager.DrawBoard(gameBoardSize[1], gameBoardSize[2], stdscr)
            #print(gameBoardSize[1], gameBoardSize[2])
        if(spawnPosition[0] == FLAG_SPAWN_POINT):
            stdscr.addstr(spawnPosition[1], spawnPosition[2], player1)
            #print(spawnPosition[1], spawnPosition[2])
        stdscr.refresh() #temp
    except Exception as e:
        print(e)
    time.sleep(5)

# Player Control
    #while True:
        # key = stdscr.getch()
        # if key == curses.KEY_UP:
        #     asd = player.sendData(0b0011, )
        #     stdscr.addstr(10, 40, asd)
        #     playerPosY = playerPosY - 1
        #     stdscr.addstr(playerPosY, playerPosX, player)
        # elif key == curses.KEY_DOWN:
        #     stdscr.addstr(playerPosY, playerPosX, "_")
        #     playerPosY = playerPosY + 1
        #     stdscr.addstr(playerPosY, playerPosX, player)
        #     dataPack = [playerPosY, playerPosX]
        #     asd = player.sendData(bytes(dataPack))
        # elif key == curses.KEY_LEFT:
        #     stdscr.addstr(playerPosY, playerPosX, "_")
        #     playerPosX = playerPosX - 2
        #     stdscr.addstr(playerPosY, playerPosX, player)
        # elif key == curses.KEY_RIGHT:
        #     stdscr.addstr(playerPosY, playerPosX, "_")
        #     playerPosX = playerPosX + 2
        #     stdscr.addstr(playerPosY, playerPosX, player)
        # elif key == curses.KEY_ENTER:
        #     player.sendData("FIN")
        #stdscr.refresh()

curses.wrapper(main)
