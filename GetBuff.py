#!/usr/bin/python3
import struct
BUF_SIZE = 1024




def getbuf(current_socket, expected_size):
    """
    Get the expected data in the socket.
    @type current_socket: object
    @param current_socket: bring a current socket
    @type expected_size: int
    @param expected_size: expected size of the buffer in the current socket
    @rtype: int
    @returns: return the requested size of bytes 
    """
    current_size = 0
    buffer = b''
    while current_size < expected_size:
        requested_size = min(expected_size - current_size, BUF_SIZE)
        data = current_socket.recv(requested_size)
        buffer = buffer + data
        current_size = current_size + len(data)
    return struct.unpack('!Bbb', buffer)