#!/usr/bin/python3

# This class is for creating a player
# this class is for keeping track of the game
class GamePlayerManager():

    # @param
    # int playerID - the unique id of the player
    # int startPosY, int startPosX - the starting Y and X position of the player
    def __init__(self, playerID, startPosY, startPosX, sock):
        self.playerUID = playerID  # Don't put setter function on this
        self.playerIcon = self.setPlayerIcon(playerID)  
        self.playerPosY = startPosY
        self.playerPosX = startPosX
        self.con = sock


    def setPlayerIcon(self, id):
    """
    Set player's identity.
    @type id: int
    @param id: set the unique id of the player
    @rtype: str
    @returns: player's identity
    """
        playerIcon = ""
        if id == 0:
            playerIcon = "Y"
        elif id == 1:
            playerIcon = "X"
        return playerIcon
    
    ### SETTER ###
    def setPlayerPosY(self, posY):
    """
    Set Y player's initial position.
    @type posY: int
    @param posY: setting the value of playerPosY to PosY
    """
        self.playerPosY = posY
        
    def setPlayerPosX(self, posX):
    """
    Set X player's initial position.
    @type posX: int
    @param posX: setting the value of playerPosX to PosX
    """
        self.playerPosX = posX


    ### GETTER ###
    def getPlayerPosY(self):
    """
    Get the current Y position of the player.
    @rtype: int
    @returns: the current Y position of the player
    """
        return self.playerPosY

    def getPlayerPosX(self):
    """
    Get the current X position of the player.
    @rtype: int
    @returns: the current X position of the player
    """
        return self.playerPosX

    def getPlayerID(self):
    """
    get this player id
    @rtype: int
    @returns: this player id
    """
        return self.playerUID

    def getPlayerIcon(self):
    """
    Get this player icon.
    @rtype: int
    @returns: this player id
    """
        return self.playerIcon

    def getPlayerCon(self):
    """
    Get this player's socket.
    @rtype: object
    @returns: this player's socket
    """
        return self.con




    


    
    

