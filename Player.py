#!/usr/bin/python3


class MakePlayer:

    # Player Constructor 
    # param 1 is player unique identification
    # param 2 current y position of the player
    # param 3 current x position of the player
    def __init__(self, id, positionY, positionX):
        self.playerID = id
        #self.connection = con
        self.posY = positionY
        self.posX = positionX
    # Getter
    # returns this player id
    def getPlayerID(self):
        return self.playerID
    # returns this connection
    def getPlayerConnection(self):
        return self.connection
    # return this current y position of the player
    def getPlayerPosY(self):
        return self.posY
    # return this current x position of the player
    def getPlayerPosX(self):
        return self.posX
    #Setter
    def setPlayerPosition(self, positionY, positionX):
        self.posY = positionY
        self.posX = positionX
