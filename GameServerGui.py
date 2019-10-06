#!/usr/bin/python3

import curses
import time
import DrawGui

class serverGui():

    # @param self: serverGui constructor itself
    # @param p1PosY, p2PosY: displaying same posistion of Y in both two plyers
    # @param p1PosX, p1PosY: displaying same posistion of X in both two plyers
    # @param row, col: each rows and cols' address in the map
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
    """
    Update position of X and Y.
    @type self: object
    @param self: passing serverGui constructor
    @type p1PosY: int
    @param p1PosY: update posistion of Y in player 1
    @type p1PosX2: int 
    @param p1PosX2: update position of X in player 1
    @type p2PosY: int
    @param p2PosY: update position of Y in player 2 
    @type p2PosX: int
    @param p2PosX: update position of X in player 2
    """
        self.storePrevLocation()
        self.player1PosY = p1PosY
        self.player1PosX = p1PosX2
        self.player2PosY = p2PosY
        self.player2PosX = p2PosX

    def storePrevLocation(self):
    """
    Store previous location of X and Y.
    @type self: object
    @param self: passing serverGui constructor
    """
        self.prevPlayer1PosY = self.player1PosY
        self.prevPlayer1PosX = self.player1PosX
        self.prevPlayer2PosY = self.player2PosY
        self.prevPlayer2PosX = self.player2PosX

    def addTreasure(self, posY, posX):
    """
    Refer treasure location in both player 1 and player 2.
    @type self: object
    @param self: passing serverGui constructor
    @type posY: int
    @param posY: treasure posision in player 1
    @type posX: int
    @param posX: treasure posision in player 2
    """
        self.treasurePosY.append(posY)
        self.treasurePosX.append(posX)

    """
    Keep refreshing board when coordination of X or Y is updated.
    @type self: object
    @param self: passing serverGui constructor
    @type stdscr: object
    @param stdscr: update and refresh of the board
    """
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
