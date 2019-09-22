#!/usr/bin/python3

import socket
import sys
import struct

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345

# error check if no argument given

# Initiating socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
print('Client:', sock.getsockname())


reply = sock.recv(BUF_SIZE)
data = struct.unpack('!II', reply)
print(data[0])
print(data[1])
