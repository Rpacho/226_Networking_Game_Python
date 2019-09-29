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
numPlayers = 0

# data Transmitting protocol
FLAG_SPAWN_POINT = 0b0001
FLAG_POSITION = 0b0011
FLAG_BOARD_SIZE = 0b0111
FLAG_BOARD_TREASURE = 0b1111
FLAG_CREATE_PLAYER = 0b0010

# This function is to update the position
def updatePosition(stdscr, player):
    stdscr.addstr(player.getPlayerPosY(), player.getPlayerPosX(), player.getPlayerIcon())

def createPlayer(playerID, posY, posX):
    # We have to add -1 in the index because server playerID is start at 1
    players.append(GamePlayerManager(playerID, posY, posX))
    for i in range(len(players)):
        if(players[i].getPlayerID() == playerID):
            return i



# This function is to identify who is turn to move
# def getUpdate():

# This function return the player new id
def getPlayerSetUp(playerUID, posY, posX):
    if(playerUID[0] == FLAG_CREATE_PLAYER):
        playerIndex = createPlayer(playerUID[1], posY, posX)
        return playerIndex
    return False
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
    # For other player data
    otherPlayerUID = net.sendData(FLAG_CREATE_PLAYER, NO_DATA, NO_DATA)
    otherSpawnPosition = net.sendData(FLAG_SPAWN_POINT, NO_DATA, NO_DATA)
    try:    # Validating that the data we receive is right
        #### This Player ####
        # Draw the Board
        if(gameBoardSize[0] == FLAG_BOARD_SIZE):
            DrawGui.DrawBoard(gameBoardSize[1], gameBoardSize[2], stdscr)
        # Take the spawnPoint
        if(spawnPosition[0] == FLAG_SPAWN_POINT):
            playerPosY = spawnPosition[1]
            playerPosX = spawnPosition[2]
        # To get This player id
        player_id = getPlayerSetUp(playerUID, playerPosY, playerPosX)
        #### Other Player ####
        # To get other player id
        # Take other spawnPoint
        if(otherSpawnPosition[0] == FLAG_SPAWN_POINT):
            OtherPlayerPosY = otherSpawnPosition[1]
            OtherPlayerPosX = otherSpawnPosition[2]
        otherPlayer_id = getPlayerSetUp(otherPlayerUI, OtherPlayerPosY, OtherPlayerPosX)
    except:
        print("Error: Setting up the game client.. Failed!")



    # Create This(this object) player
    # playerIndex = createPlayer(player_id, playerPosY, playerPosX)
    # # Spawn the player
    updatePosition(stdscr, players[player_id])
    numPlayers += 1
    updatePosition(stdscr, players[otherPlayer_id])
    numPlayers += 1
    
    while True:
        # otherPlayer = net.sendData(FLAG_CREATE_PLAYER, NO_DATA, NO_DATA)
        # if(otherPlayer[1] > 1): # more than 1 player
        #     getPlayerSetUp(otherPlayer)
        key = stdscr.getch()
        if key == curses.KEY_UP:
            stdscr.addstr(playerPosY, playerPosX, "_")
            playerPosY = playerPosY - 1
            movePosition(net, stdscr, playerPosY, playerPosX, players[playerIndex])
        elif key == curses.KEY_DOWN:
            stdscr.addstr(playerPosY, playerPosX, "_")
            playerPosY = playerPosY + 1
            movePosition(net, stdscr, playerPosY, playerPosX, players[playerIndex])
        elif key == curses.KEY_LEFT:
            stdscr.addstr(playerPosY, playerPosX, "_")
            playerPosX = playerPosX - 2
            movePosition(net, stdscr, playerPosY, playerPosX, players[playerIndex])
        elif key == curses.KEY_RIGHT:
            stdscr.addstr(playerPosY, playerPosX, "_")
            playerPosX = playerPosX + 2
            movePosition(net, stdscr, playerPosY, playerPosX, players[playerIndex])
        elif key == curses.KEY_ENTER:
            exit()
        stdscr.refresh()

curses.wrapper(main)
