#!/usr/bin/python3

import socket
import struct

BUFF_SIZE = 1024

def receiveData(connection):
    data = connection.recv(BUFF_SIZE)
    if data != b'Ack':
        unpackData = struct.unpack('!II', data)
        return unpackData
    return
    # dataReceive = []
    # while True:
    #     data = connection.recv(BUFF_SIZE)
    #     if len(data) > 0:
    #         unpackData = struct.unpack('!II', data)
    #         for i in unpackData:
    #             dataReceive.append(i)
    #     else:
    #         return dataReceive
    #         break
    # return False

