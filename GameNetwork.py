#!/usr/bin/python3

import socket
import struct
import ReadingData  # Testing library for lab 1 need to delete later before handing in

# This Class is for creating a network that connect to the server
class Network():
    def __init__(self):
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.SERVER_IP = '10.51.11.59'
        self.SERVER_IP = '127.0.0.1'
        self.SERVER_PORT = 12345
        self.addr = (self.SERVER_IP, self.SERVER_PORT)
        self.StartToConnect(self.addr)

    def StartToConnect(self, addr):
        try:
            self.con.connect(addr)
            # data = self.con.recv(1024)
            # print(data.decode())
        except Exception as e:
            print(e)
            pass
    
    def sendData(self, flag, dataY, dataX):
        try:
            data = struct.pack('!Bbb', flag, dataY, dataX)
            self.con.sendall((data))
            reply = self.con.recv(1024)
            #print(reply)
            if not reply:
                return False
            unpackReply = struct.unpack('!Bbb', reply)
            return unpackReply
        except socket.error as e:
            print(e)


# FLAG_CREATE_PLAYER = 0b0010
# net = Network()
# # playerUID = n.sendData(FLAG_CREATE_PLAYER, 0, 0)
# # print(playerUID)
# # #print(n.sendData("Hello"))
# # data = struct.pack('!BBB', 2, 3, 0b0111)
# # data2 = n.sendData(data)
# # print(struct.unpack('!BBB', data2))
# #print(n.sendData(0b0111, 0, 0))
# FLAG_GAME_START = 0b0100
# FLAG_POSITION = 0b0011
# FLAG_BOARD_SIZE = 0b0111
# FLAG_BOARD_TREASURE = 0b1111
# FLAG_SPAWN_POINT = 0b0001
# FLAG_CREATE_OP = 0b0101
# FLAG_SPAWN_OP = 0b0110
# NO_DATA = 0
# while True:
#     gameStart = net.sendData(FLAG_GAME_START, NO_DATA, NO_DATA)
#     if gameStart[0] == FLAG_GAME_START:
#         if gameStart[1] != 1:
#             continue
#         # Ask the server for player id
#     playerUID = net.sendData(FLAG_CREATE_PLAYER, NO_DATA, NO_DATA)
#     # Ask the server for the size of the board
#     gameBoardSize = net.sendData(FLAG_BOARD_SIZE, NO_DATA, NO_DATA)
#     # Ask the server for the spawn position of this player
#     spawnPosition = net.sendData(FLAG_SPAWN_POINT, NO_DATA, NO_DATA)
#     otherPlayerUID = net.sendData(FLAG_CREATE_OP, NO_DATA, NO_DATA)
#     otherSpawnPosition = net.sendData(FLAG_SPAWN_OP, NO_DATA, NO_DATA)
#     print('playerUID: ',playerUID)
#     print('gameBoardSize: ',gameBoardSize)
#     print('spawnPosition: ',spawnPosition)
#     #if(otherPlayerUID[0] == FLAG_CREATE_OP):
#     print('otherPlayerUID: ',otherPlayerUID)
#     # #if(otherSpawnPosition[0] == FLAG_SPAWN_OP):
#     print('otherSpawnPosition: ', otherSpawnPosition)
#     break
