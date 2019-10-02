#!/usr/bin/python3
import random
import socket
import struct
FLAG_BOARD_TREASURE = 0b1111

def randLocation():
    location = []
    location.append(random.randint(1,9))
    location.append(random.randint(1, 36))
    return location

def sendLocation(con1, con2, serverGui):
    
    for i in range(10):
        location = randLocation()
        if location[1] % 2 == 1:
            location[1] = location[1] - 1
        dataLocation = struct.pack('!Bbb', FLAG_BOARD_TREASURE, location[0], location[1])
        con1.sendall(dataLocation)
        con2.sendall(dataLocation)
        serverGui.addTreasure(location[0], location[1])
