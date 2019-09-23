#!/usr/bin/python3

import socket

class Network():
    def __init__(self):
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER_IP = '127.0.0.1'
        self.SERVER_PORT = 12345
        self.addr = (self.SERVER_IP, self.SERVER_PORT)
        self.StartToConnect(self.addr)

    def StartToConnect(self, addr):
        try:
            self.con.connect(addr)
            return self.recv(2048).decode()
        except:
            pass
    
    def sendData(self, data):
        try:
            self.con.send(str.encode(data))
            return self.con.recv(1024) 
        except socket.error as e:
            print(e)

n = Network()
print(n.sendData("Hello"))
