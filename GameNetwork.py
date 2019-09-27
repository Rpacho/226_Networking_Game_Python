#!/usr/bin/python3

import socket
import struct
import ReadingData

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
            data = self.con.recv(1024)
            print(data.decode())
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


# n = Network()
# #print(n.sendData("Hello"))
# data = struct.pack('!BBB', 2, 3, 0b0111)
# data2 = n.sendData(data)
# print(struct.unpack('!BBB', data2))
#print(n.sendData(0b0111, 0, 0))

# FLAG_POSITION = 0b0011
# FLAG_BOARD_SIZE = 0b0111
# FLAG_BOARD_TREASURE = 0b1111
# FLAG_SPAWN_POINT = 0b0001
# try:
#         gameBoardSize = n.sendData(FLAG_BOARD_SIZE, 0, 0)
#         print(gameBoardSize)
#         if(gameBoardSize[0] == FLAG_BOARD_SIZE):
#             #GameManager.DrawBoard(gameBoardSize[1], gameBoardSize[2], stdscr)
#             print(gameBoardSize[1], gameBoardSize[2])
#         spawnPosition = n.sendData(FLAG_SPAWN_POINT, 0, 0)
#         if(spawnPosition[0] == FLAG_SPAWN_POINT):
#             #stdscr.addstr(spawnPosition[1], spawnPosition[2], player1)
#             print(spawnPosition[1], spawnPosition[2])
#         #stdscr.refresh() #temp
#         print(spawnPosition)
# except Exception as e:
#     print(e)

# print(n.sendData(FLAG_BOARD_SIZE, 1, 1))
# print(n.sendData(FLAG_BOARD_SIZE, 2, 1))
# print(n.sendData(FLAG_BOARD_SIZE, 3, 1))
# print(n.sendData(FLAG_BOARD_SIZE, 4, 1))
# gameBoardSize = n.sendData(FLAG_BOARD_SIZE, 0, 0)
# print(gameBoardSize)
# spawnPosition = n.sendData(FLAG_SPAWN_POINT, 0, 0)
# print(spawnPosition)

# if(gameBoardSize[0] == FLAG_BOARD_SIZE):
#     print(gameBoardSize[1], gameBoardSize[2])
# if(spawnPosition[0] == FLAG_SPAWN_POINT):
#     print(spawnPosition[1], spawnPosition[2])
