#!/usr/bin/python3

import socket
import threading
import DrawGui
import struct
from GameManager import GameDataManager

HOST_IP = ''
PORT = 12345

# Player Config
MAX_PLAYER = 2
playerID = 1 # We can also use this for getting the # of current players online
spawnPoint_1 = [0,0]
spawnPoint_2 = [9,38]

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
NO_DATA = 0
connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the network
try:
    connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect.bind((HOST_IP, PORT))
    connect.listen(MAX_PLAYER)
    print("Connection connected. Server is up!")
except:
    print("Cannnot establish connection. Server Down!")

row = 10
col = 20
# This return the spawnpoint for different player
def getSpawnPoint():
    if playerID == 1:
        return spawnPoint_1
    if playerID == 2:
        return spawnPoint_2
# GUI
## This function is for receiving and sending data
def transmitting(con, spawnPoint, thisPlayerID):
    try:
        data = con.recv(1024)
        #print(len(data))
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
        if(thisPlayerID == 1):
            #Sending
            if(dataReceive[0] == FLAG_POSITION):
                gameManager.setPlayer1PosY(dataReceive[1])
                gameManager.setPlayer1PosX(dataReceive[2])
                dataToSend = struct.pack('!Bbb', FLAG_POSITION, gameManager.getPlayer1PosY()
                , gameManager.getPlayer1PosX())
                #print("Player position at :", dataToSend[1], dataToSend[2])
                con.sendall(dataToSend)
                # gameManager.setPlayer1Turn(False)
                # gameManager.setPlayer2Turn(True)
                
                #print('Player 2 Turn',gameManager.getPlayer2Turn())
            if(dataReceive[0] == FLAG_PLAYER_TURNS):
                dataToSend2 = struct.pack('!Bbb', FLAG_PLAYER_TURNS, gameManager.getPlayer1Turn(), NO_DATA)
                con.sendall(dataToSend2)
                
            #Receiving
            #print("Player 1", thisPlayerID)
            if(dataReceive[0] == FLAG_CREATE_OP):
                playerData = struct.pack('!Bbb', FLAG_CREATE_OP, gameManager.getPlayer2ID(), NO_DATA)
                con.sendall(playerData)
            if(dataReceive[0] == FLAG_SPAWN_OP):
                dataToSend3 = struct.pack('!Bbb', FLAG_SPAWN_OP, gameManager.getPlayer2PosY(), gameManager.getPlayer2PosX())
                con.sendall(dataToSend3)
        else:
            # Sending
            if(dataReceive[0] == FLAG_POSITION):
                gameManager.setPlayer2PosY(dataReceive[1])
                gameManager.setPlayer2PosX(dataReceive[2])
                dataToSend = struct.pack('!Bbb', FLAG_POSITION, gameManager.getPlayer2PosY()
                , gameManager.getPlayer2PosX())
                #print("Player position at :", dataToSend[1], dataToSend[2])
                con.sendall(dataToSend)
                # gameManager.setPlayer2Turn(False)
                # gameManager.setPlayer1Turn(True)
                #print('Player 1 Turn ', gameManager.getPlayer1Turn())
            if(dataReceive[0] == FLAG_PLAYER_TURNS):
                dataToSend2 = struct.pack('!Bbb', FLAG_PLAYER_TURNS, gameManager.getPlayer2Turn(), NO_DATA)
                con.sendall(dataToSend2)
            # Receiving
            #print("Player 2", thisPlayerID)
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
def thread_player(con, player):
    global playerID
    msg = "Welcome to server"
    print(msg, ' Player ', playerID)
    # con.sendall(msg.encode())
    spawnPoint = getSpawnPoint()
    positionY = spawnPoint[0]
    positionX = spawnPoint[1]
    thisPlayerID = playerID
    ## Initial settings for players
    if(thisPlayerID == 1):
        gameManager.setPlayer1PosY(positionY)
        gameManager.setPlayer1PosX(positionX)
        gameManager.setPlayer1ID(thisPlayerID)
        gameManager.setPlayer1Ready(True)
        gameManager.setPlayer1Turn(True)
        print("Waiting for other players to get ready..")
    elif(thisPlayerID == 2):
        gameManager.setPlayer2PosY(positionY)
        gameManager.setPlayer2PosX(positionX)
        gameManager.setPlayer2ID(thisPlayerID)
        gameManager.setPlayer2Ready(True)
        #gameManager.setPlayer2Turn(True)
        print("Players 2 are ready.. \n Game Starting...")
    playerID += 1
    while True:
        gameManager.setReady() # sets if all players are ready
        if gameManager.getReady() == False:
            continue
        try:
            # player 1 Transmmiting data
            # if(thisPlayerID == 1):
            #     if((transmitting(gameManager.getPlayerConnection1(), spawnPoint, thisPlayerID)) == False):
            #         break
            # elif(thisPlayerID == 2):
            #     if((transmitting(gameManager.getPlayerConnection2(), spawnPoint, thisPlayerID)) == False):
            #         break
            print('Player 1 Turn ', gameManager.getPlayer1Turn())
            print('Player 2 Turn ', gameManager.getPlayer2Turn())
            if((transmitting(con, spawnPoint, thisPlayerID)) == False):
                break
            # player 2 Transmmiting data
            # if(thisPlayerID == 1):
            #     print('player 1, confirming: ', thisPlayerID, ' sending data to player 2')
            #     if((transmitting(gameManager.getPlayerConnection2(), spawnPoint, thisPlayerID)) == False):
            #         break
            # elif(thisPlayerID == 2):
            #     print('player 2, confirming: ', thisPlayerID, ' sending data to player 1')
            #     if((transmitting(gameManager.getPlayerConnection1(), spawnPoint, thisPlayerID)) == False):
            #         break
        except Exception as e:
            print(e)
            break
    print("Connection lost Player ", thisPlayerID)
    con.close()

# Client connect to Server
while True:
    con, socketname = connect.accept()
    gameID = 1
    player = 0
    global gameManager
    if gameID == 1 and playerID == 1:   # Should always execute first when first player connects
        gameManager = GameDataManager(gameID, playerID)
        gameManager.setPlayer1Con(con)
        player = 1
    elif(gameID == 1 and playerID == 2):
        gameManager.setPlayer2Con(con)
        gameManager.setNumPlayer(playerID)
        gameID += 1
        player = 2
    # Temporary
    
    threading.Thread(target=thread_player, args=(con, player)).start()
