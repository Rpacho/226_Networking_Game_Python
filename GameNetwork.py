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
            unpackReply = struct.unpack('!Bbb', reply)
            return unpackReply
        except socket.error as e:
            print(e)


