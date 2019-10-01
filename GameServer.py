#!/usr/bin/python3

import socket
import threading
import DrawGui
import struct
from GameManager import GameDataManager
import logging
import logging.handlers
import GetBuff
logger = logging.getLogger('GameServer.py')
logger.setLevel(logging.DEBUG)
handle = logging.FileHandler('Serverlog.txt')
logger.addHandler(handle)

HOST_IP = ''
PORT = 12345
# Player Config
MAX_PLAYER = 2
playerID = 0 # We can also use this for getting the # of current players online
spawnPoint_1 = [0,0]
spawnPoint_2 = [9,38]
countAllPlayerTurn = 0

#Flag for transmiting data
FLAG_SPAWN_POINT = 0b0001
FLAG_POSITION = 0b0011
FLAG_BOARD_SIZE = 0b0111
FLAG_BOARD_TREASURE = 0b1111
FLAG_CREATE_PLAYER = 0b0010
FLAG_GAME_START = 0b0100
FLAG_CREATE_OP = 0b0101
FLAG_SPAWN_OP = 0b0110
FLAG_PLAYER_TURNS = 0b1001
FLAG_DONE_TURNS = 0b1000
NO_DATA = 0
connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the network
try:
    connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect.bind((HOST_IP, PORT))
    connect.listen()
    print("Connection connected. Server is up!")
except:
    print("Cannnot establish connection. Server Down!")

row = 10
col = 20

# Semaphores
locks = []
for i in range(2):
    locks.append(threading.Semaphore())
    locks[-1].acquire()
def setUpTheGame():
    data = GetBuff(con, 3)
    if (data[0] == FLAG_BOARD_SIZE)


while True:
    con, socketname = connect.accept()

    
