#!/usr/bin/python3

import curses
import socket
import struct
import ReceivingData
import threading
from Player import MakePlayer

BUF_SIZE = 1024
HOST = '192.168.1.77'
PORT = 12345
players = []

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

def dataRecieve():
    data = sock.recv(1024)
    sock.sendall(b'Ack')
    playerAlreadyExist = False
    if data != b'Ack':
        unpackData = struct.unpack('!III', data)
        for i in range(len(players)):
            if players[i].getPlayerID() == unpackData[0]:
                return i
        if playerAlreadyExist == False:
            players.append(MakePlayer(unpackData[0], unpackData[1], unpackData[2]))
    return playerAlreadyExist

def main(stdscr):

    # boardInitData = sock.recv(1024)
    # unpackBoardInitData = struct.unpack('!II', boardInitData)
    # sock.sendall(b'Ack')
    # row = unpackBoardInitData[0]
    # col = unpackBoardInitData[1]
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

    while True:
        key = stdscr.getch()
        data = dataRecieve()
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

