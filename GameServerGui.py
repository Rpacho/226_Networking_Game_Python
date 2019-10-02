#!/usr/bin/python3

import curses
import time
import DrawGui

class serverGui():
    def __init__(self, p1PosY, p1PosX, p2PosY, p2PosX, row, col):
        self.player1PosY = p1PosY
        self.player1PosX = p1PosX
        self.player2PosY = p2PosY
        self.player2PosX = p2PosX
        self.rowSize = row
        self.colSize = col
        self.treasurePosY = []
        self.treasurePosX = []
        self.prevPlayer1PosY = p1PosY
        self.prevPlayer1PosX = p1PosX
        self.prevPlayer2PosY = p2PosY
        self.prevPlayer2PosX = p2PosX

    def updatePosition(self, p1PosY, p1PosX2, p2PosY, p2PosX):
        self.storePrevLocation()
        self.player1PosY = p1PosY
        self.player1PosX = p1PosX2
        self.player2PosY = p2PosY
        self.player2PosX = p2PosX

    def storePrevLocation(self):
        self.prevPlayer1PosY = self.player1PosY
        self.prevPlayer1PosX = self.player1PosX
        self.prevPlayer2PosY = self.player2PosY
        self.prevPlayer2PosX = self.player2PosX

    def addTreasure(self, posY, posX):
        self.treasurePosY.append(posY)
        self.treasurePosX.append(posX)

    def main(self, stdscr):
        DrawGui.DrawBoard(self.rowSize, self.colSize, stdscr)
        for i in range(len(self.treasurePosX)):
            stdscr.addstr(self.treasurePosY[i], self.treasurePosX[i], "$")
        while True:
            stdscr.addstr(self.prevPlayer1PosY, self.prevPlayer1PosX, "_")
            stdscr.addstr(self.prevPlayer2PosY, self.prevPlayer2PosX, "_")
            stdscr.addstr(self.player1PosY, self.player1PosX, "Y")
            stdscr.addstr(self.player2PosY, self.player2PosX, "X")
            stdscr.refresh()
