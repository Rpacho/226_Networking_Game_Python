#!/usr/bin/python3

import socket
import threading
import struct
import ReceivingData
import curses
# Connection config
HOST_IP = ''
PORT = 12345
playerid = 1

# establishing connection
connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connect.bind((HOST_IP, PORT))
connect.listen()
print("Server is Up")
asd = 12
a = struct.pack('!Q', asd)

def listen(con):
    while True:
        # print("ASDASDASDASDASDAS")
        msg = input("Message: ").encode()
        con.sendall(msg)
        reply = con.recv(1024)
        con.sendall(b'ACK')
        if len(reply) > 0:
            print(reply.decode('utf-8'))

while True:
    print("debug")
    con, socketname = connect.accept()
    listen(con)
    print("ASDASDASDASDASDAS")
    
    





# a = b'12'
# b = b'11'
# c = b'13'
# d = b'14'
# e = b'15'
# f = b'16'
# while True:
#     
#     con.sendall(a)
#     con.sendall(b)
#     con.sendall(c)
#     con.sendall(d)
#     con.sendall(e)
#     con.sendall(f)
