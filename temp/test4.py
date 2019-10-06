#!/usr/bin/python3

import curses
import socket
import struct
import ReceivingData
import time

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345

# error check if no argument given

# Initiating socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
    print("Connected to the server")
    print('Client:', sock.getsockname())

except Exception:
    print("Failed to connect to the server")
    exit()

# screen = curses.initscr()
# curses.noecho()
# curses.cbreak()
# screen.keypad(True)


curses.endwin

playerIcon = "Y"
emptyBlock = "_"

# Displaying Characters


def display(character, posY, posX, screen):
    screen.addstr(posY, posX, character)


def sendData(posY, posX):
    data = struct.pack('!II', posY, posX)
    sock.sendall(data)


def dataRecieve():
    data = sock.recv(1024)
    unpack = struct.unpack('!I', data)
    return unpack


def main(stdscr):
    curses.curs_set(1)
    x = 0
    y = 0
    while True:
        stdscr.clear()
        i = 0
        while i < 10:
            stdscr.addstr(x, y, "Y")
            time.sleep(1)
            i = i + 1
            x = x + 1
            y = y + 1
        key = stdscr.getch()
        # i = dataRecieve()
        # stdscr.addstr(i[0], 0, "Y")
        # stdscr.clear()
        stdscr.refresh()

curses.wrapper(main)
        



