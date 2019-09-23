#!/usr/bin/python3

import socket
import threading
import curses

HOST_IP = ''
PORT = 12345

# Player Config
MAX_PLAYER = 4
playerID = 0

connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the network
try:
    connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect.bind((HOST_IP, PORT))
    connect.listen(MAX_PLAYER)
    print("Connection connected. Server is up!")
except:
    print("Cannnot establish connection. Server Down!")

# Isolating the connection of the player by threading
def thread_player(con, playerID):
    startMsg = "Welcome to the server"
    con.sendall(startMsg.encode())
    while True:
        print("debug")
        try:
            print("debug2")
            data = con.recv((1024).decode())
            print("debug3")
            if not data:
                break
            else:
                print("Receiving: " , data)
                print("Sending: ", data)
                con.sendall(data.encode())

        except:
            break
    print("Connection lost")
    con.close()

# Client connect to Server
while True:
    con, socketname = connect.accept()
    playerID += 1
    threading.Thread(target=thread_player, args=(con, playerID)).start()
