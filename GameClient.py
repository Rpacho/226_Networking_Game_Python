#!/usr/bin/python3

import curses
import socket
import DrawGui
from GameNetwork import Network
import struct
import time
from GameManager import GamePlayerManager
import logging
import logging.handlers
logger = logging.getLogger('GameClient.py')
logger.setLevel(logging.DEBUG)
handle = logging.FileHandler('Clientlog.txt')
logger.addHandler(handle)
NO_DATA = 0

# Game config
player_id = 0
players = []
numPlayers = 0
myTurn = False
# data Transmitting protocol
FLAG_SPAWN_POINT = 0b0001 #1
FLAG_POSITION = 0b0011  #3
FLAG_BOARD_SIZE = 0b0111   #7
FLAG_BOARD_TREASURE = 0b1111    #15
FLAG_CREATE_PLAYER = 0b0010 #2
FLAG_GAME_START = 0b0100    #4
FLAG_CREATE_OP = 0b0101 #5
FLAG_SPAWN_OP = 0b0110  #6
FLAG_PLAYER_TURNS = 0b1001  #9
FLAG_DONE_TURNS = 0b1000    #8

# This function is to update the position
def updatePosition(stdscr, player):
    stdscr.addstr(player.getPlayerPosY(), player.getPlayerPosX(), player.getPlayerIcon())
    stdscr.refresh()

# This function is to create the new player
def createPlayer(playerID, posY, posX):
    # We have to add -1 in the index because server playerID is start at 1
    players.append(GamePlayerManager(playerID, posY, posX))
    for i in range(len(players)):
        if(players[i].getPlayerID() == playerID):
            return i

# This function is update the other player position
def getUpdate(net, otherPlayer, stdscr):
    #playerTurn = net.sendData(FLAG_PLAYER_TURNS, NO_DATA, NO_DATA)
    otherSpawnPosition = net.sendData(FLAG_SPAWN_OP, NO_DATA, NO_DATA)
    if(otherSpawnPosition[0] == FLAG_SPAWN_OP):
        stdscr.addstr(otherPlayer.getPlayerPosY(), otherPlayer.getPlayerPosX(), "_")
        OtherPlayerPosY = otherSpawnPosition[1]
        OtherPlayerPosX = otherSpawnPosition[2]
        otherPlayer.setPlayerPosY(OtherPlayerPosY)
        otherPlayer.setPlayerPosX(OtherPlayerPosX)
        updatePosition(stdscr, otherPlayer)
    # if playerTurn[0] == FLAG_PLAYER_TURNS:
    #     if playerTurn[1] == True:
    #         return True
    # return False

# This function return the player new id
def getPlayerSetUp(playerUID, posY, posX):
    if(playerUID[0] == FLAG_CREATE_PLAYER):
        playerIndex = createPlayer(playerUID[1], posY, posX)
        return playerIndex
    if(playerUID[0] == FLAG_CREATE_OP):
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
        # logger.debug(player.getPlayerPosY())
        # logger.debug(player.getPlayerPosY())
        updatePosition(stdscr, player)
    except:
        print("Error: movePosition Function GameClient Not Sending Data")

    return
def getMoveTurn(net, player_id):
    playerTurn = net.sendData(FLAG_PLAYER_TURNS, NO_DATA, NO_DATA)
    logger.debug(player_id)
    logger.debug(playerTurn)
    if playerTurn[1] == True:
        return True
    else:
        return False


######### MAIN #########
# Initiate prepack Curses and start the game
def main(stdscr):
    global myTurn
    net = Network()
    curses.curs_set(0)

    while True:
        # Ask the server for player id
        playerUID = net.sendData(FLAG_CREATE_PLAYER, NO_DATA, NO_DATA)
        # Ask the server for the size of the board
        gameBoardSize = net.sendData(FLAG_BOARD_SIZE, NO_DATA, NO_DATA)
        # Ask the server for the spawn position of this player
        spawnPosition = net.sendData(FLAG_SPAWN_POINT, NO_DATA, NO_DATA)
        otherPlayerUID = net.sendData(FLAG_CREATE_OP, NO_DATA, NO_DATA)
        otherSpawnPosition = net.sendData(FLAG_SPAWN_OP, NO_DATA, NO_DATA)
        try:    # Validating that the data we receive is right
            #### This Player ####
            # Draw the Board
            if(gameBoardSize[0] == FLAG_BOARD_SIZE):
                DrawGui.DrawBoard(gameBoardSize[1], gameBoardSize[2], stdscr)
            # Take the spawnPoint
            if(spawnPosition[0] == FLAG_SPAWN_POINT):
                playerPosY = spawnPosition[1]
                playerPosX = spawnPosition[2]
            #### Other Player ####
                # Take other spawnPoint
            if(otherSpawnPosition[0] == FLAG_SPAWN_OP):
                OtherPlayerPosY = otherSpawnPosition[1]
                OtherPlayerPosX = otherSpawnPosition[2]
        except:
            print("Error: Setting up the game client.. Failed!")

        # To get This player id
        player_id = getPlayerSetUp(playerUID, playerPosY, playerPosX)
        #To get other player id
        #print(OtherPlayerPosY, OtherPlayerPosX)
        #Create This(this object) player
        otherPlayer_id = getPlayerSetUp(otherPlayerUID, OtherPlayerPosY, OtherPlayerPosX)
        # Spawn the player
        updatePosition(stdscr, players[player_id])
        updatePosition(stdscr, players[otherPlayer_id])
        # time.sleep(3)
        # break

        ### Second iteration
        while True:
            getUpdate(net, players[otherPlayer_id], stdscr)
            stdscr.refresh()
            if(getMoveTurn(net, playerUID[1]) == True):
                stdscr.addstr(0, 60, "Your Turn")
                stdscr.addstr(1, 60, str(players[player_id].getPlayerID()))
                key = stdscr.getch()
                if key == curses.KEY_DOWN:
                    stdscr.addstr(playerPosY, playerPosX, "_")
                    playerPosY = playerPosY + 1
                    movePosition(net, stdscr, playerPosY, playerPosX, players[player_id])
                getUpdate(net, players[otherPlayer_id], stdscr)
                stdscr.refresh()
                logger.debug(net.sendData(FLAG_DONE_TURNS, True, NO_DATA))
            elif(getMoveTurn(net, playerUID[1]) == False):
                stdscr.addstr(0, 60, "Wait For Your Turn")
                continue
                # stdscr.addstr(playerPosY, playerPosX, "_")
                # playerPosY = playerPosY + 1
                # movePosition(net, stdscr, playerPosY, playerPosX, players[player_id])
                # if key == curses.KEY_UP:
                #     stdscr.addstr(playerPosY, playerPosX, "_")
                #     playerPosY = playerPosY - 1
                #     movePosition(net, stdscr, playerPosY, playerPosX, players[player_id])
                # elif key == curses.KEY_DOWN:
                #     stdscr.addstr(playerPosY, playerPosX, "_")
                #     playerPosY = playerPosY + 1
                #     movePosition(net, stdscr, playerPosY, playerPosX, players[player_id])
                # elif key == curses.KEY_LEFT:
                #     stdscr.addstr(playerPosY, playerPosX, "_")
                #     playerPosX = playerPosX - 2
                #     movePosition(net, stdscr, playerPosY, playerPosX, players[player_id])
                # elif key == curses.KEY_RIGHT:
                #     stdscr.addstr(playerPosY, playerPosX, "_")
                #     playerPosX = playerPosX + 2
                #     movePosition(net, stdscr, playerPosY, playerPosX, players[player_id])
                # elif key == curses.KEY_ENTER:
                #     exit()
                #     #stdscr.refresh()


curses.wrapper(main)


