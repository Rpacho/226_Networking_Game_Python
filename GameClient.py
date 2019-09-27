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

def movePosition(net,stdscr, posY, posX):
    position = net.sendData(FLAG_POSITION, posY, posX)
    stdscr.addstr(position[1], position[2], player1)
    return
######### MAIN #########
# Initiate prepack Curses and start the game
def main(stdscr):
    net = Network()
    curses.curs_set(0)
    #GameManager.DrawBoard(10, 20, stdscr)

    gameBoardSize = net.sendData(FLAG_BOARD_SIZE, 0, 0)
    spawnPosition = net.sendData(FLAG_SPAWN_POINT, 0, 0)
    if(gameBoardSize[0] == FLAG_BOARD_SIZE):
        GameManager.DrawBoard(gameBoardSize[1], gameBoardSize[2], stdscr)
        #print(gameBoardSize[1], gameBoardSize[2])
    if(spawnPosition[0] == FLAG_SPAWN_POINT):
        stdscr.addstr(spawnPosition[1], spawnPosition[2], player1)
        playerPosY = spawnPosition[1]
        playerPosX = spawnPosition[2]
            #print(spawnPosition[1], spawnPosition[2])
    stdscr.refresh()
    #time.sleep(3)
# Player Control
    # key = stdscr.getch()

    # if key == curses.KEY_UP:
    #     print("x")
    #     #movePosition(net)
    #     stdscr.addstr(playerPosY -1, playerPosX, player1)
    
    while True:
        #stdscr.addstr(playerPosY, playerPosX, player1)
        key = stdscr.getch()
        if key == curses.KEY_UP:
            stdscr.addstr(playerPosY, playerPosX, "_")
            playerPosY = playerPosY - 1
            movePosition(net, stdscr, playerPosY, playerPosX)
        elif key == curses.KEY_DOWN:
            stdscr.addstr(playerPosY, playerPosX, "_")
            playerPosY = playerPosY + 1
            movePosition(net, stdscr, playerPosY, playerPosX)
        elif key == curses.KEY_LEFT:
            stdscr.addstr(playerPosY, playerPosX, "_")
            playerPosX = playerPosX - 2
            movePosition(net, stdscr, playerPosY, playerPosX)
        elif key == curses.KEY_RIGHT:
            stdscr.addstr(playerPosY, playerPosX, "_")
            playerPosX = playerPosX + 2
            movePosition(net, stdscr, playerPosY, playerPosX)
        elif key == curses.KEY_ENTER:
            exit()
        stdscr.refresh()

curses.wrapper(main)
