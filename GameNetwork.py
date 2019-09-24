#!/usr/bin/python3

import socket
import struct

class Network():
    def __init__(self):
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER_IP = '10.51.11.59'
        self.SERVER_PORT = 12345
        self.addr = (self.SERVER_IP, self.SERVER_PORT)
        self.StartToConnect(self.addr)

    def StartToConnect(self, addr):
        try:
            self.con.connect(addr)
            data = self.con.recv(2048)
            return data.decode()
        except Exception as e:
            print(e)
            pass
    
    def sendData(self, data):
        try:
            if isinstance(data, str):
                self.con.send(str.encode(data))
            else: 
                self.con.send(data)
            # else:
            #     self.con.send(data)
            # data = self.con.recv(2048)
            # if isinstance(data.decode(), str) == False:
            #     return struct.unpack('!II', data)
            return self.con.recv(2048).decode()
        except socket.error as e:
            print(e)

n = Network()
print(n.sendData("Hello"))
data = [1,2]
print(n.sendData(bytes(data)))
