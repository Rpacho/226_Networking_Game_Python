#!/usr/bin/python3

import socket
import threading
import DrawGui
import struct
from GameManager import GameDataManager
import logging
import logging.handlers
logger = logging.getLogger('GameServer.py')
logger.setLevel(logging.DEBUG)
handle = logging.FileHandler('Serverlog.txt')
logger.addHandler(handle)

HOST_IP = ''
PORT = 12345

# Player Config
MAX_PLAYER = 2
playerID = 0 # We can also use this for getting the # of current players online
spawnPoint_1 = [0,0]
spawnPoint_2 = [9,38]
countAllPlayerTurn = 0

#Flag for transmiting data
FLAG_SPAWN_POINT = 0b0001
FLAG_POSITION = 0b0011
FLAG_BOARD_SIZE = 0b0111
FLAG_BOARD_TREASURE = 0b1111
FLAG_CREATE_PLAYER = 0b0010
FLAG_GAME_START = 0b0100
FLAG_CREATE_OP = 0b0101
FLAG_SPAWN_OP = 0b0110
FLAG_PLAYER_TURNS = 0b1001
FLAG_DONE_TURNS = 0b1000
NO_DATA = 0
connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the network
try:
    connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect.bind((HOST_IP, PORT))
    connect.listen()
    print("Connection connected. Server is up!")
except:
    print("Cannnot establish connection. Server Down!")

row = 10
col = 20

# Semaphores
locks = []
for i in range(2):
    locks.append(threading.Semaphore())
    locks[-1].acquire()
global gameManager
# This return the spawnpoint for different player
def getSpawnPoint():
    if playerID == 0:
        return spawnPoint_1
    if playerID == 1:
        return spawnPoint_2
# GUI


## This function is for receiving and sending data
def transmitting(con, spawnPoint, thisPlayerID):
    try:
        print('Player ', thisPlayerID)
        print('Player 1 turn ', gameManager.getPlayer1Turn())
        print('Player 2 turn ', gameManager.getPlayer2Turn())
        data = con.recv(1024)
        if not data:
            return False   
        dataReceive = struct.unpack('!Bbb', data)
        if(dataReceive[0] == FLAG_GAME_START):
            playerData = struct.pack('!Bbb', FLAG_GAME_START, 1, NO_DATA) # 0 means no data
            #print(struct.unpack('!Bbb', playerData))
            con.sendall(playerData)
        if(dataReceive[0] == FLAG_CREATE_PLAYER):
            playerData = struct.pack('!Bbb', FLAG_CREATE_PLAYER, thisPlayerID, NO_DATA) # 0 means no data
            #print(struct.unpack('!Bbb', playerData))
            con.sendall(playerData)
        if(dataReceive[0] == FLAG_BOARD_SIZE):
            dataToSend2 = struct.pack('!Bbb', FLAG_BOARD_SIZE, row, col)
            con.sendall(dataToSend2)
        if(dataReceive[0] == FLAG_SPAWN_POINT):
            dataToSend3 = struct.pack('!Bbb', FLAG_SPAWN_POINT, spawnPoint[0], spawnPoint[1])
            con.sendall(dataToSend3)
        #con.sendall(b'')
        ### PLAYER WHO ###
        if(thisPlayerID == 0):
            if(dataReceive[0] == FLAG_POSITION):
                gameManager.setPlayer1PosY(dataReceive[1])
                gameManager.setPlayer1PosX(dataReceive[2])
                dataToSend = struct.pack('!Bbb', FLAG_POSITION, gameManager.getPlayer1PosY(), gameManager.getPlayer1PosX())
                con.sendall(dataToSend)
                dataToSendP2 = struct.pack('!Bbb', FLAG_SPAWN_OP, gameManager.getPlayer1PosY(), gameManager.getPlayer1PosX())
                gameManager.getPlayerConnection2().sendall(dataToSendP2)
            if(dataReceive[0] == FLAG_PLAYER_TURNS):
                dataToSend2 = struct.pack('!Bbb', FLAG_PLAYER_TURNS, gameManager.getPlayer1Turn(), NO_DATA)
                con.sendall(dataToSend2)
            if(dataReceive[0] == FLAG_DONE_TURNS):
                logger.debug(thisPlayerID)
                logger.debug(dataReceive[0])
                dataToSend2 = struct.pack('!Bbb', FLAG_DONE_TURNS, NO_DATA, NO_DATA)
                con.sendall(dataToSend2)
                if dataToSend2[1] == True:
                    gameManager.setPlayer1Turn(False)
                    gameManager.setPlayer2Turn(True)
            if(dataReceive[0] == FLAG_CREATE_OP):
                playerData = struct.pack('!Bbb', FLAG_CREATE_OP, gameManager.getPlayer2ID(), NO_DATA)
                con.sendall(playerData)
            if(dataReceive[0] == FLAG_SPAWN_OP):
                dataToSend3 = struct.pack('!Bbb', FLAG_SPAWN_OP, gameManager.getPlayer2PosY(), gameManager.getPlayer2PosX())
                con.sendall(dataToSend3)
        elif(thisPlayerID == 1):
            if(dataReceive[0] == FLAG_POSITION):
                gameManager.setPlayer2PosY(dataReceive[1])
                gameManager.setPlayer2PosX(dataReceive[2])
                dataToSend = struct.pack('!Bbb', FLAG_POSITION, gameManager.getPlayer2PosY(), gameManager.getPlayer2PosX())
                con.sendall(dataToSend)
                dataToSendP2 = struct.pack('!Bbb', FLAG_SPAWN_OP, gameManager.getPlayer1PosY(), gameManager.getPlayer1PosX())
                gameManager.getPlayerConnection2().sendall(dataToSendP2)
            if(dataReceive[0] == FLAG_DONE_TURNS):
                logger.debug(thisPlayerID)
                logger.debug(dataReceive[0])
                dataToSend2 = struct.pack('!Bbb', FLAG_DONE_TURNS, NO_DATA, NO_DATA)
                con.sendall(dataToSend2)
                if dataToSend2[1] == True:
                    gameManager.setPlayer1Turn(True)
                    gameManager.setPlayer2Turn(False)
            if(dataReceive[0] == FLAG_PLAYER_TURNS):
                dataToSend2 = struct.pack('!Bbb', FLAG_PLAYER_TURNS, gameManager.getPlayer2Turn(), NO_DATA)
                con.sendall(dataToSend2)
            if(dataReceive[0] == FLAG_CREATE_OP):
                playerData = struct.pack('!Bbb', FLAG_CREATE_OP, gameManager.getPlayer1ID(), NO_DATA)
                con.sendall(playerData)
            if(dataReceive[0] == FLAG_SPAWN_OP):
                dataToSend3 = struct.pack('!Bbb', FLAG_SPAWN_OP, gameManager.getPlayer1PosY(), gameManager.getPlayer1PosX())
                con.sendall(dataToSend3)
    except Exception as e:
        print(e)


# def otherTransmmiting(con, spawnPoint, thisPlayerID):


# Isolating the connection of the player by threading
def thread_player(con):
    global playerID
    msg = "Welcome to server"
    print(msg, ' Player ', playerID)
    # con.sendall(msg.encode())
    spawnPoint = getSpawnPoint()
    positionY = spawnPoint[0]
    positionX = spawnPoint[1]
    thisPlayerID = playerID
    ## Initial settings for players
    if(thisPlayerID == 0):
        gameManager.setPlayer1PosY(positionY)
        gameManager.setPlayer1PosX(positionX)
        gameManager.setPlayer1ID(thisPlayerID)
        #gameManager.setPlayer1Ready(True)
        gameManager.setPlayer1Turn(True)
        print("Waiting for other players to get ready..")
    elif(thisPlayerID == 1):
        gameManager.setPlayer2PosY(positionY)
        gameManager.setPlayer2PosX(positionX)
        gameManager.setPlayer2ID(thisPlayerID)
        gameManager.setPlayer2Ready(True)
        #gameManager.setPlayer2Turn(False)
        #gameManager.setPlayer2Turn(True)
        print("Players 2 are ready.. \n Game Starting...")
    playerID += 1
    while True:
        locks[thisPlayerID].acquire()
        try:
            print("Player 1 ", gameManager.getPlayer1Turn())
            # #print(thisPlayerID)
            print("Player 2 ", gameManager.getPlayer2Turn())
            if((transmitting(con, spawnPoint, thisPlayerID)) == False):
                continue
        except Exception as e:
            print(e)
            break
        locks[(thisPlayerID + 1) % 2].release()
    print("Connection lost Player ", thisPlayerID)
    con.close()

def gameStart(num_player):
    if num_player == 2:
        for i in range(num_player):
            if i == 0:
                playerCon = gameManager.getPlayerConnection1()
            if i == 1:
                playerCon = gameManager.getPlayerConnection2()
            threading.Thread(target=thread_player, args=(playerCon,)).start()
        locks[0].release()

# Client connect to Server
player = 0
while True:
    con, socketname = connect.accept()
    gameID = 1
    print(player)
    if gameID == 1 and player == 0:   # Should always execute first when first player connects
        gameManager = GameDataManager(gameID, playerID)
        gameManager.setPlayer1Con(con)
        player += 1
    elif(gameID == 1 and player == 1):
        gameManager.setPlayer2Con(con)
        gameManager.setNumPlayer(playerID)
        #gameID += 1
        player += 1
    # Temporary
    print(con.getpeername())
    #con.close()
    gameStart(player)
    
