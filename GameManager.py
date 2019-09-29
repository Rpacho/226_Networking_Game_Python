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
        self.player1Turn = False
        self.player2Turn = False

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
class GameDataManager():
    def __init__(self, conPlayer1, gameID, numPlayer):
        self.con1 = conPlayer1
        self.con2 = conPlayer1
        self.game_id = gameID
        self.num_player = numPlayer
        self.isItReady = False
        self.playe1Ready = False
        self.player2Ready = False

    ### Getters ### for GameDataManager

    # This function returns the player 1 connection
    def getPlayerConnection(self):
        return self.con1
    # This function returns the player 2 connection
    def getPlayerConnection2(self):
        return self.con2
    # This function returns game id
    def getGameID(self):
        return self.game_id
    # This function returns the number of players
    def getNumPlayer(self):
        return self.num_player
    def getReady(self):
        return self.isItReady

    #### Setters ### for GameDataManager

    # This function sets if all players is ready
    def setReady(self):
        if (self.playe1Ready == True and self.player2Ready == True):
            self.isItReady = True
    # This function sets if player 2 connection
    # @param , socket con
    def setPlayer2Con(self, con):
        self.con2 = con
    # This function sets the number of player
    # @param , int numPlayer
    def setNumPlayer(self, numPlayer):
        self.num_player = numPlayer
    # This function sets if player 1 is ready
    # @param , bool ready
    def setPlayer1Ready(self, ready):
        self.playe1Ready = ready
    # This function sets if player 2 is ready
    # @param , bool ready
    def setPlayer2Ready(self, ready):
        self.player2Ready = ready
    


    
    

