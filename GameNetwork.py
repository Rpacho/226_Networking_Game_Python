#!/usr/bin/python3

import socket
import struct
import GetBuff  # Testing library for lab 1 need to delete later before handing in

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
            reply = GetBuff.getbuf(self.con, 3)
            #print(reply)
            if not reply:
                return False
            #unpackReply = struct.unpack('!Bbb', reply)
            return reply
        except socket.error as e:
            print(e)


# FLAG_SPAWN_POINT = 0b0001  # 1
# FLAG_POSITION = 0b0011  # 3
# FLAG_BOARD_SIZE = 0b0111  # 7
# FLAG_BOARD_TREASURE = 0b1111  # 15
# FLAG_CREATE_PLAYER = 0b0010  # 2
# FLAG_GAME_START = 0b0100  # 4
# FLAG_PLAYER2_POSITION = 0b0101  # 5
# FLAG_PLAYER2_CREATE = 0b0110  # 6
# FLAG_PLAYER_TURNS = 0b1001  # 9
# FLAG_DONE_TURNS = 0b1000  # 8
# NO_DATA = 0
# n = Network()

# print(n.sendData(FLAG_CREATE_PLAYER, NO_DATA, NO_DATA))
# print(n.sendData(FLAG_BOARD_SIZE, NO_DATA, NO_DATA))
# print(n.sendData(FLAG_SPAWN_POINT, NO_DATA, NO_DATA))
# print(n.sendData(FLAG_DONE_TURNS, NO_DATA, NO_DATA))
# def input1():
#     x = input("Enter Int ")
#     i = int(x)
#     n.sendData(FLAG_POSITION, i, NO_DATA)
# while True:
    
#     data = GetBuff.getbuf(n.con, 3)
#     if len(data) > 0:
#         if data[0] == FLAG_PLAYER2_CREATE:
#             print(data)
#         if data[0] == FLAG_PLAYER2_POSITION:
#             print(data)
#         if data[0] == FLAG_PLAYER_TURNS:
#             input1()


        

