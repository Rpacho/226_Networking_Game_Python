#!/usr/bin/python3

# This class is for creating a player
class GamePlayerManager():
    # @param
    # int playerID - the unique id of the player
    # int startPosY, int startPosX - the starting Y and X position of the player
    def __init__(self, playerID, startPosY, startPosX, ):
        self.playerIcon = self.setPlayerIcon(playerID)
        self.playerUID = playerID   # Don't put setter function on this
        self.playerPosY = startPosY
        self.playerPosX = startPosX

    # This function return the icon of the player.
    # @param
    # int playerID - the unique id of the player
    def setPlayerIcon(self, id):
        playerIcon = ""
        if id == 1:
            playerIcon = "Y"
        elif id == 2:
            playerIcon = "X"
        return playerIcon
    
    ### SETTER ###

    # This function is for setting the Y position of player
    # @param; int posY - setting the value of playerPosY to PosY
    def setPlayerPosY(self, posY):
        self.playerPosY = posY
    # This function is for setting the X position of player
    # @param; int posX - setting the value of playerPosX to PosX
    def setPlayerPosX(self, posX):
        self.playerPosX = posX

    ### GETTER ###

    # This function returns the current Y position of the player
    def getPlayerPosY(self):
        return self.playerPosY
    #This function returns the current X position of the player
    def getPlayerPosX(self):
        return self.playerPosX
    #This function returns this player id
    def getPlayerID(self):
        return self.playerUID
    # This function returns this player icon
    def getPlayerIcon(self):
        return self.playerIcon


# this class is for keeping track of the game
# class GameDataManager():
#     def __init__(self, connection, gameID, numPlayer)


    
    

