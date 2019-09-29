#!/usr/bin/python3

import curses
import socket
import DrawGui
from GameNetwork import Network
import struct
import time
from GameManager import GamePlayerManager

NO_DATA = 0

# Game config
player_id = 0
players = []

# data Transmitting protocol
FLAG_SPAWN_POINT = 0b0001
FLAG_POSITION = 0b0011
FLAG_BOARD_SIZE = 0b0111
FLAG_BOARD_TREASURE = 0b1111
FLAG_CREATE_PLAYER = 0b0010

# This function is to update the position
def updatePosition(stdscr, player):
    stdscr.addstr(player.getPlayerPosY(), player.getPlayerPosX(), player.getPlayerIcon())


# This function is to identify who is turn to move

#This function is to receive the position of the
def movePosition(net, stdscr, posY, posX, player):
    try:
        position = net.sendData(FLAG_POSITION, posY, posX)
        positionY = position[1]
        positionX = position[2]
        player.setPlayerPosY(positionY)
        player.setPlayerPosX(positionX)
        updatePosition(stdscr, player)
    except:
        print("Error: movePosition Function GameClient Not Sending Data")

    return
######### MAIN #########
# Initiate prepack Curses and start the game
def main(stdscr):
    net = Network()
    curses.curs_set(0)
    
    # Ask the server for player id
    playerUID = net.sendData(FLAG_CREATE_PLAYER, NO_DATA, NO_DATA)
    # Ask the server for the size of the board
    gameBoardSize = net.sendData(FLAG_BOARD_SIZE, NO_DATA, NO_DATA)
    # Ask the server for the spawn position of this player
    spawnPosition = net.sendData(FLAG_SPAWN_POINT, NO_DATA, NO_DATA)
    try:
        # Validating that the data we receive is right
        if(playerUID[0] == FLAG_CREATE_PLAYER):
            player_id = playerUID[1]
        # Draw the Board
        if(gameBoardSize[0] == FLAG_BOARD_SIZE):
            DrawGui.DrawBoard(gameBoardSize[1], gameBoardSize[2], stdscr)
        # Take the spawnPoint
        if(spawnPosition[0] == FLAG_SPAWN_POINT):
            playerPosY = spawnPosition[1]
            playerPosX = spawnPosition[2]
    except:
        print("Error: Setting up the game client.. Failed!")


    # Create class for player
    player = GamePlayerManager(player_id, playerPosY, playerPosX)
    # Set the Icon
    #playerIcon = player.getPlayerIcon(player_id)
    # Set the spawn position
    stdscr.addstr(playerPosY, playerPosX, player.getPlayerIcon())



    while True:
        #stdscr.addstr(playerPosY, playerPosX, player1)
        key = stdscr.getch()
        if key == curses.KEY_UP:
            stdscr.addstr(playerPosY, playerPosX, "_")
            playerPosY = playerPosY - 1
            movePosition(net, stdscr, playerPosY, playerPosX, player)
        elif key == curses.KEY_DOWN:
            stdscr.addstr(playerPosY, playerPosX, "_")
            playerPosY = playerPosY + 1
            movePosition(net, stdscr, playerPosY, playerPosX, player)
        elif key == curses.KEY_LEFT:
            stdscr.addstr(playerPosY, playerPosX, "_")
            playerPosX = playerPosX - 2
            movePosition(net, stdscr, playerPosY, playerPosX, player)
        elif key == curses.KEY_RIGHT:
            stdscr.addstr(playerPosY, playerPosX, "_")
            playerPosX = playerPosX + 2
            movePosition(net, stdscr, playerPosY, playerPosX, player)
        elif key == curses.KEY_ENTER:
            exit()
        stdscr.refresh()

curses.wrapper(main)
