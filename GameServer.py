#!/usr/bin/python3
import socket
import threading
import DrawGui
import struct
from GameManager import GamePlayerManager
import logging
import logging.handlers
import GetBuff
import TreasureLocation
from GameServerGui import serverGui
import curses
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
players = []
#Flag for transmiting data
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
NO_DATA = 0
TYPE = '!Bbb'
connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

row = 10
col = 20
# Connect to the network
try:
    connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect.bind((HOST_IP, PORT))
    connect.listen()
    print("Connection connected. Server is up!")
except:
    print("Cannnot establish connection. Server Down!")

def getSpawnPoint():
    if playerID == 0:
        return spawnPoint_1
    if playerID == 1:
        return spawnPoint_2

def packData(flag, data1, data2):
    return struct.pack('!Bbb', flag, data1, data2)

# Semaphores
locks = []
for i in range(2):
    locks.append(threading.Semaphore())
    locks[-1].acquire()

def setUpTheGame(con, player_id):
    while True:
        data = GetBuff.getbuf(con, 3)
        if data[0] == FLAG_CREATE_PLAYER:
            sendData = packData(FLAG_CREATE_PLAYER, player_id, NO_DATA)
            print('Player ', playerID, 'Sending ', player_id)
            con.sendall(sendData)
        if data[0] == FLAG_BOARD_SIZE:
            sendData = packData(FLAG_BOARD_SIZE, row, col)
            con.sendall(sendData)
        if data[0] == FLAG_SPAWN_POINT:
            sendData = packData(FLAG_SPAWN_POINT, players[player_id].getPlayerPosY(), players[player_id].getPlayerPosX())
            con.sendall(sendData)
        if data[0] == FLAG_DONE_TURNS:
            sendData = packData(FLAG_DONE_TURNS, True, NO_DATA)
            con.sendall(sendData)
            return True

def sendPosition():
    # Sending player2 position to player 1
    sendPlayer2Pos = packData(FLAG_PLAYER2_POSITION, players[1].getPlayerPosY(), players[1].getPlayerPosX())
    players[0].getPlayerCon().sendall(sendPlayer2Pos)
    # Sending player1 position to player 2
    sendPlayer1Pos = packData(FLAG_PLAYER2_POSITION, players[0].getPlayerPosY(), players[0].getPlayerPosX())
    players[1].getPlayerCon().sendall(sendPlayer1Pos)

def update(con, player_id):
    # Put here outside the loop and lock
    while True:
        try:
            locks[player_id].acquire()  #### LOCK #####
            # Tell players its your turn
            #print('Player Sending Turn flags', player_id)
            sendData = packData(FLAG_PLAYER_TURNS, NO_DATA, NO_DATA)
            players[player_id].getPlayerCon().sendall(sendData)

            #print('Player asking for data')
            data = GetBuff.getbuf(con, 3)
            if data[0] == FLAG_POSITION:
                players[player_id].setPlayerPosY(data[1])
                players[player_id].setPlayerPosX(data[2])
                serverDisplay.updatePosition(players[0].getPlayerPosY(), players[0].getPlayerPosX(), players[1].getPlayerPosY(), players[1].getPlayerPosX())
            # Send your turn to other players
            #print('Player sending position to all')
            sendPosition()

            locks[(player_id + 1) % 2].release()    #### RELEASE ####
        except Exception as e:
            print(e)
            break
    print("Connection lost Player ", player_id)
    players[player_id].getPlayerCon().close()

def startTheGame():
    # Sending player2 id to player 1
    sendPlayer2ID = packData(FLAG_PLAYER2_CREATE, players[1].getPlayerID(), NO_DATA)
    players[0].getPlayerCon().sendall(sendPlayer2ID)
    # Sending player1 id to player 2
    sendPlayer1ID = packData(FLAG_PLAYER2_CREATE, players[0].getPlayerID(), NO_DATA)
    players[1].getPlayerCon().sendall(sendPlayer1ID)
    sendPosition()
    # Create a GUI for the server
    global serverDisplay
    serverDisplay = serverGui(players[0].getPlayerPosY(), players[0].getPlayerPosX(), players[1].getPlayerPosY(), players[1].getPlayerPosX(), row, col)
    # Send the treasure location for both player
    TreasureLocation.sendLocation(players[0].getPlayerCon(), players[1].getPlayerCon(), serverDisplay)

    # Start Moving!!
    for i in range(2):
        threading.Thread(target=update, args=(players[i].getPlayerCon(), players[i].getPlayerID())).start()
    locks[0].release()

    curses.wrapper(serverDisplay.main)

while True:
    con, socketname = connect.accept()
    print(con.getpeername())
    spawnPoint = getSpawnPoint()
    players.append(GamePlayerManager(playerID, spawnPoint[0], spawnPoint[1], con))
    if(setUpTheGame(con, playerID) == True):
        playerID += 1
    if(playerID == 2):
        startTheGame()



    
