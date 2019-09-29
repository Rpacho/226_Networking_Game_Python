#!/usr/bin/python3

import socket
import threading
import DrawGui
import struct

HOST_IP = ''
PORT = 12345

# Player Config
MAX_PLAYER = 2
playerID = 1
spawnPoint_1 = [0,0]
spawnPoint_2 = [9,38]

#Flag for transmiting data
FLAG_SPAWN_POINT = 0b0001
FLAG_POSITION = 0b0011
FLAG_BOARD_SIZE = 0b0111
FLAG_BOARD_TREASURE = 0b1111
FLAG_CREATE_PLAYER = 0b0010
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
def transmitting(con, dataY, dataX):
    try:
        data = con.recv(1024)
        print(len(data))
        if not data:
            return False   
        dataReceive = struct.unpack('!Bbb', data)
        if(dataReceive[0] == FLAG_CREATE_PLAYER):
            playerData = struct.pack('!Bbb', FLAG_CREATE_PLAYER, playerID, NO_DATA) # 0 means no data
            print(struct.unpack('!Bbb', playerData))
            con.sendall(playerData)
        if(dataReceive[0] == FLAG_BOARD_SIZE):
            dataToSend2 = struct.pack('!Bbb', FLAG_BOARD_SIZE, row, col)
            con.sendall(dataToSend2)
        if(dataReceive[0] == FLAG_SPAWN_POINT):
            dataToSend3 = struct.pack('!Bbb', FLAG_SPAWN_POINT, spawnPoint_2[0], spawnPoint_2[1])
            con.sendall(dataToSend3)
        if(dataReceive[0] == FLAG_POSITION):
            dataToSend = struct.pack('!Bbb', FLAG_POSITION, dataReceive[1], dataReceive[2])
            print("Player position at :", dataToSend[1], dataToSend[2])
            con.sendall(dataToSend)
        #con.sendall(b'')
    except Exception as e:
        print(e)


# Isolating the connection of the player by threading
def thread_player(con, playerID):
    msg = "Welcome to server"
    con.sendall(msg.encode())
    spawnPoint = getSpawnPoint()
    positionY = spawnPoint[0]
    positionX = spawnPoint[1]
    while True:
        try:
            if((transmitting(con, positionY, positionX)) == False):
                break

        except Exception as e:
            print(e)
            break
    print("Connection lost")
    con.close()

# Client connect to Server
while True:
    con, socketname = connect.accept()
    # Send player id
    # start the game
    threading.Thread(target=thread_player, args=(con, playerID)).start()
