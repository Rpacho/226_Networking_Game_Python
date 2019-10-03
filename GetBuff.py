#!/usr/bin/python3
import struct
BUF_SIZE = 1024

def getbuf(current_socket, expected_size):
    current_size = 0
    buffer = b''
    while current_size < expected_size:
        requested_size = min(expected_size - current_size, BUF_SIZE)
        data = current_socket.recv(requested_size)
        buffer = buffer + data
        current_size = current_size + len(data)
    return struct.unpack('!Bbb', buffer)