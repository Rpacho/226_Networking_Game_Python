#!/usr/bin/python3

import curses
import socket
import struct
import ReceivingData
import threading

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
# screen.addstr(1,1, "Hello")
# screen.refresh()
# curses.napms(3000)
# curses.endwin
playerIcon = "Y"
emptyBlock = "_"

# Displaying Characters
def display(character, posY, posX, screen):
    screen.addstr(posY, posX, character)

def sendData(posY, posX):
    data = struct.pack('!II', posY, posX)
    sock.sendall(data)
data2 = b''
# def dataRecieve():
#     data = sock.recv(1024)
#     data2 = data
#     if data != b'':
#         unpack = struct.unpack('!II', data)
#         posX = unpack[0]
#         posY = unpack[1]

#threading.Thread(target=dataRecieve).start()


def main(stdscr):

    # data = ReceivingData.receiveData(sock)
    # row = data[0]
    # col = data[1]
    row = 10
    col = 20
    playerPosY = 0
    playerPosX = 0
    player = playerIcon
    trueCol = col * 2
    curses.curs_set(0)

    for y in range (0, row):
        for x in range (0, trueCol):
            if x % 2 == 0:
                stdscr.addstr(y,x, "_")
            else:
                stdscr.addstr(y,x, " ")

    #HardCoded initial position for player Y
    stdscr.addstr(0, 0, player)

    while True:
        key = stdscr.getch()
        #i = dataRecieve()
        #stdscr.clear()
        #stdscr.addstr(i[0], 0, "Y")
        if key == curses.KEY_UP:
            #display("T", posY, posX, stdscr)
            display(emptyBlock, playerPosY, playerPosX, stdscr)
            playerPosY = playerPosY - 1
            display(player, playerPosY, playerPosX, stdscr)
            sendData(playerPosY, playerPosX)
        elif key == curses.KEY_DOWN:
            display(emptyBlock, playerPosY, playerPosX, stdscr)
            playerPosY = playerPosY + 1
            display(player, playerPosY, playerPosX, stdscr)
            sendData(playerPosY, playerPosX)
        elif key == curses.KEY_LEFT:
            display(emptyBlock, playerPosY, playerPosX, stdscr)
            playerPosX = playerPosX - 2
            display(player, playerPosY, playerPosX, stdscr)
            sendData(playerPosY, playerPosX)
        elif key == curses.KEY_RIGHT:
            display(emptyBlock, playerPosY, playerPosX, stdscr)
            playerPosX = playerPosX + 2
            display(player, playerPosY, playerPosX, stdscr)
            sendData(playerPosY, playerPosX)
        stdscr.refresh()


curses.wrapper(main)

