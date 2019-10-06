#!/usr/bin/python3
import random
import socket
import struct
FLAG_BOARD_TREASURE = 0b1111



def randLocation():
    """ 
    Generate the random location of treasures.
    @rtype: list
    @returns: a list of int
    """
    location = []
    location.append(random.randint(1,9))
    location.append(random.randint(1, 36))
    return location



def sendLocation(con1, con2, serverGui):
    """
    Send the randomly generated location from the randLocation() to the server.
    @type con1: byte
    @param con1: a socket which contains a data of tresures location
    @type con2: byte
    @param con2: a socket which contains a data of tresures location
    @type serverGui: object
    @param serverGui: dispay location with GUI
    """
    for i in range(10):
        location = randLocation()
        if location[1] % 2 == 1:
            location[1] = location[1] - 1
        dataLocation = struct.pack('!Bbb', FLAG_BOARD_TREASURE, location[0], location[1])
        con1.sendall(dataLocation)
        con2.sendall(dataLocation)
        serverGui.addTreasure(location[0], location[1])
