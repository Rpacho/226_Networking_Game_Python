#!/usr/bin/python3

import socket
import threading
import struct
import ReceivingData
# Connection config
HOST_IP = ''
PORT = 12345

# establishing connection
connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connect.bind((HOST_IP, PORT))
connect.listen()
print("Server is up")

# Player Config
totalRow = 10
totalCol = 20
# initial position of player spawn
x = 0
y = 0

playerID = 1    #player Identifier

# This Class is for assigning a player
class Player:
    def __init__(self, con, id):
        self.playerID = id
        self.connection = con

    def getPlayerID(self):
        return self.playerID
    def getPlayerConnection(self):
        return self.connection

# This function is for initializing board
def initBoardSize(con):
    row = struct.pack('!II', totalRow, totalCol)
    col = 20
    con.sendall(row)


# This function is for printing player position
def serverLog(data, player_ID):
    print('Player: ', player_ID, " Position: ", data)
# # This function is for receiving data from client
def receivingData(con, player):
    player_ID = player.getPlayerID()
    while True:
        data = ReceivingData.receiveData(con)
        serverLog(data, player_ID)


# # This function is for sending data to client
# def sendingData(connection, data):
#     connection.sendall(data)


## This functiong is for initiating a player
def playerInitiate(con, playerID):
    player = Player(con, playerID)
    initBoardSize(con)
    receivingData(con, player)


# This function is for displaying who connected to the server
#def initConnectionLog():
    

## Player connecting to server
while True:
    con, socketname = connect.accept()
    # if theres a new client connected
    # create a unique identifier for player
    if(con):
        print("Player " + str(playerID) + " connected! IP address and source PORT: " , con.getpeername())
        threading.Thread(target=playerInitiate, args=(con, playerID)).start()
        playerID = playerID + 1
    #data = con.recv(1024)
    
