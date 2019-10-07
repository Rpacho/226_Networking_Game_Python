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
import GetBuff
logger = logging.getLogger('GameClient.py') # Create a GameClient.py logger
logger.setLevel(logging.DEBUG) # Create debug handler
handle = logging.FileHandler('Clientlog.txt') # Create file handler
logger.addHandler(handle) # add handler to the logger
NO_DATA = 0

# Game config
player_id = 0
players = []
numPlayers = 0
treasurePosY = []
treasurePosX = []
# data Transmitting protocol
FLAG_SPAWN_POINT = 0b0001
FLAG_POSITION = 0b0011
FLAG_BOARD_SIZE = 0b0111
FLAG_BOARD_TREASURE = 0b1111
FLAG_CREATE_PLAYER = 0b0010
FLAG_CLEAR_BUFFER = 0b0100
FLAG_PLAYER2_POSITION = 0b0101
FLAG_PLAYER2_CREATE = 0b0110
FLAG_PLAYER_TURNS = 0b1001
FLAG_DONE_TURNS = 0b1000


def updatePosition(stdscr, player):
    """
    Update the position.
    @type stdscr: object
    @param stdscr: cursers
    @type player: object
    @param player: passing player object to get the players' position
    """   
    stdscr.addstr(player.getPlayerPosY(), player.getPlayerPosX(), player.getPlayerIcon())
    stdscr.refresh()

# This function is to create the new player
def createPlayer(playerID, posY, posX):
    """
    Create player in a designated location.
    @type playerID: list
    @param playerID: the value of the player
    @type posY: int
    @param posY: one of the location of rows
    @type posX: int
    @param posX: one of the location of cols
    """ 
    players.append(GamePlayerManager(playerID, posY, posX, NO_DATA))

# This function is update the other player position
# @param player2 - player object
def setPositionPlayer2(player2, posY, posX):
    """
    Set player2 in a designated location.
    @type player2: object
    @param player2: passing player2 object to set it's location
    @type posY: int
    @param posY: one of the location of rows
    @type posX: int
    @param posX: one of the location of cols
    """ 
    player2.setPlayerPosY(posY)
    player2.setPlayerPosX(posX)

def reDrawMyPreviousLocation(stdscr, player_id):
    """
    Overwrite "_" to the previous locaiton of the player.
    @type stdscr: object
    @param stdscr: cursers
    @type player_id: object
    @param player_id: passing player_id object to get the position of the player
    """ 
    posY = player_id.getPlayerPosY()Packing flags' data into string.
    posX = player_id.getPlayerPosX()
    stdscr.addstr(posY, posX, "_")

#This function is to receive the position of the
def movePosition(net, stdscr, posY, posX, player):
    """
    Receive the locaiton of the player's moved.
    @type posY: int
    @param posY: location of cols
    @type posX: int
    @param posX: location of cols
    @type player: object
    @param player: passing player object to set the location of the player
    """ 
    try:
        player.setPlayerPosY(posY)
        player.setPlayerPosX(posX)
        position = net.sendData(FLAG_POSITION, posY, posX)
        updatePosition(stdscr, player)
    except:
        print("Error: movePosition Function GameClient Not Sending Data")

    return
def treasureCollosion(posX, posY):
    """
    Prevent the collapse of treasure position. 
    @type posX: int
    @param posX: location of rows
    @type posY: int
    @param posY: location of cols
    @rtype: bool
    @returns: true
    """ 
    for i in range (len(treasurePosY)):
        if posY == treasurePosY[i]:
            if posX == treasurePosX[i]:
                return True

def checkCollosion(posY, posX):
    """
    Check between a treasure location and a player's location.
    @type posY: int
    @param posY: location of cols
    @type posX: int
    @param posX: location of rows
    @rtype: bool
    @returns: false
    """ 
    player2PosY = players[1].getPlayerPosY()
    player2PosX = players[1].getPlayerPosX()
    # Collosion on the wall
    if posY < 0:    # end first of row
        return False
    if posY > 9:    # end last of row
        return False
    if posX < 0:    # end first of col
        return False
    if posX > 38:   # end last of col
        return False
    # Collosion on the Treasure
    if (treasureCollosion(posX, posY) == True):
        return False
    # Collosion on the other player
    if((posY == player2PosY and posX == player2PosX)):
        return False

    # For this player
def controller(stdscr, net):
    """
    Control handling for a player.
    @type stdscr: object 
    @param stdscr: cursers object
    @type net: object
    @param net: network object
    @rtype: bool
    @returns: true or false depends on key is typed or not
    """ 
    stdscr.addstr(0 , 60, "Your Turn         ")
    posY = players[0].getPlayerPosY()
    posX = players[0].getPlayerPosX()
    key = stdscr.getch()
    logger.debug("Pressed Keys" + str(players[0].getPlayerID()))
    if key == curses.KEY_UP:
        playerPosY = posY - 1
        # Checking the collosion
        if(checkCollosion(playerPosY, posX) == False):
            return False
        reDrawMyPreviousLocation(stdscr, players[0])
        movePosition(net, stdscr, playerPosY, posX, players[0])
        return True
    elif key == curses.KEY_DOWN:
        playerPosY = posY + 1
        if(checkCollosion(playerPosY, posX) == False):
            return False
        reDrawMyPreviousLocation(stdscr, players[0])
        movePosition(net, stdscr, playerPosY, posX, players[0])
        return True
    elif key == curses.KEY_LEFT:
        playerPosX = posX - 2
        if(checkCollosion(posY, playerPosX) == False):
            return False
        reDrawMyPreviousLocation(stdscr, players[0])
        movePosition(net, stdscr, posY, playerPosX, players[0])
        return True
    elif key == curses.KEY_RIGHT:
        playerPosX = posX + 2
        if(checkCollosion(posY, playerPosX) == False):
            return False
        reDrawMyPreviousLocation(stdscr, players[0])
        movePosition(net, stdscr, posY, playerPosX, players[0])
        return True
    else:
        stdscr.addstr(0, 60, "Invalid input    ")
        stdscr.refresh()
    return False

######### MAIN #########
# Initiate prepack Curses and start the game
def main(stdscr):
    """
    Receive data of board size, spawn position of the player,
    screen display and other player.
    """
    net = Network()
    curses.curs_set(0)
    playerUID = net.sendData(FLAG_CREATE_PLAYER, NO_DATA, NO_DATA)
    # Ask the server for the size of the board
    gameBoardSize = net.sendData(FLAG_BOARD_SIZE, NO_DATA, NO_DATA)
    # Ask the server for the spawn position of this player
    spawnPosition = net.sendData(FLAG_SPAWN_POINT, NO_DATA, NO_DATA)
    thisIsReady = net.sendData(FLAG_DONE_TURNS, NO_DATA, NO_DATA)
    ## Drawing the screen
    DrawGui.DrawBoard(gameBoardSize[1], gameBoardSize[2], stdscr)
    player_id = createPlayer(playerUID[1], spawnPosition[1], spawnPosition[2])
    # Index 0 will always be this player
    updatePosition(stdscr, players[0])
    stdscr.refresh()
    while True:
        stdscr.addstr(0, 60, "Wait for your Turn")
        stdscr.keypad(0)
        stdscr.refresh()
        data = GetBuff.getbuf(net.con, 3)
        stdscr.keypad(1)
        if len(data) > 0:
        # If other players are connected and we receive thier data, store them in our players collection
            if data[0] == FLAG_PLAYER2_CREATE:
                player2 = createPlayer(data[1], NO_DATA, NO_DATA)
            if data[0] == FLAG_BOARD_TREASURE:
                stdscr.addstr(data[1], data[2], '$')
                treasurePosY.append(data[1])
                treasurePosX.append(data[2])
                stdscr.refresh()
            if data[0] == FLAG_PLAYER2_POSITION:
                reDrawMyPreviousLocation(stdscr, players[1])
                setPositionPlayer2(players[1], data[1], data[2])    # Index 1 will always be player 2
                updatePosition(stdscr, players[0]) # Temporary fix
                updatePosition(stdscr, players[1])
            stdscr.addstr(1, 60, "           ")
            if data[0] == FLAG_PLAYER_TURNS:
                while True:
                    validInput = controller(stdscr, net)
                    if(validInput == True):
                        break
                    

        
    

curses.wrapper(main)


