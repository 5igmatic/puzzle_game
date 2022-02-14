from tile import Tile
from player import Player
import pygame

class World:
    def __init__(self, size, startLevel):
        self.traversableTiles = " 01"

        self.levels = {1: ["ttttttt",
                           "t     t",
                           "t    0t",
                           "ttttttt"],
            
                       2: ["ttttttt",
                           "t     t",
                           "t     t",
                           "tttt 0t",
                           "   tttt"],
                           
                       3: ["ttttttttt",
                           "t       t",
                           "t       t",
                           "t       t",
                           "t       t",
                           "t0     0t",
                           "ttttttttt"]}
        #playerType (start location)
        self.levelData = {1: [[0, [2, 2]]],
                          2: [[0, [2, 2]]],
                          3: [[0, [6, 5]], [0, [3, 5]]]}
        self.tiles = pygame.sprite.Group()
        self.size = size
        self.playerLocations = []
        self.currentLevel = startLevel
        self.players = [0, 1]
        self.currentPlayers = pygame.sprite.Group()
        self.activePlayerIndex = 0

        self.playerChangeCooldown = 0
        #the player can only change Players every 30 frames
        self.playerChangeCooldownDuration = 30

    def load(self):
        self.tiles.empty()
        self.currentPlayers.empty()
        self.playerLocations.clear()
        levelLayout = self.levels[self.currentLevel]
        self.getCurrentPlayers()
        rowIndex = 0
        for row in levelLayout:
            tileIndex = 0
            for tile in row:
                if tile != " ":
                    self.tiles.add(Tile(tile, (tileIndex, rowIndex), self.size))
                tileIndex += 1
            rowIndex += 1

    def getCurrentPlayers(self):
        currentLevelData = self.levelData[self.currentLevel]
        for playerIndex, playerData in enumerate(currentLevelData):
            playerType = playerData[0]
            playerPosition = playerData[1]
            self.playerLocations.append(playerPosition)
            x = playerPosition[0]*self.size
            y = playerPosition[1]*self.size
            player = Player(playerIndex, playerType, self.size, x, y, self)
            self.currentPlayers.add(player)
        self.activePlayerIndex = 0

    #Accessed by the Player class
    def changePlayer(self, shift):
        self.playerChangeCooldown = self.playerChangeCooldownDuration
        players = len(self.currentPlayers.sprites())
        self.activePlayerIndex += shift
        self.activePlayerIndex %= players

    def doMovement(self):
        for index,player in enumerate(self.currentPlayers):
            if index == self.activePlayerIndex:
                player.doMovement()

        if(self.playerChangeCooldown > 0):
            self.playerChangeCooldown -= 1

    def updateIndividual(self, object, WIN, shiftX, shiftY):
        rect = object.image.get_rect(center = (object.x + shiftX, object.y + shiftY))
        WIN.blit(object.image, rect)

    def update(self, WIN):
        screenCenterX = WIN.get_width()/2
        screenCenterY = WIN.get_height()/2
        for index,player in enumerate(self.currentPlayers):
            if index == self.activePlayerIndex:
                focusX = player.x
                focusY = player.y
        shiftX = screenCenterX - focusX
        shiftY = screenCenterY - focusY
        for tile in self.tiles:
            self.updateIndividual(tile, WIN, shiftX, shiftY)
        for player in self.currentPlayers:
            self.updateIndividual(player, WIN, shiftX, shiftY)

    #update for jump compatability
    #Accessed by the Player class
    def updateLocation(self, player, shift):
        self.playerLocations[player][0] += shift[0]
        self.playerLocations[player][1] += shift[1]
        self.checkCompletion()

    #update for jump compatability
    #Accessed by the Player class
    def isBlocked(self, player, right):
        moveLocation = list(self.playerLocations[player])
        if right:
            moveLocation[0] += 1
        else:
            moveLocation[0] -= 1
        for playerLocation in self.playerLocations:
            if playerLocation == [moveLocation[0], moveLocation[1]]:
                return True
        if self.levels[self.currentLevel][moveLocation[1]][moveLocation[0]] in self.traversableTiles:
            return False
        #print(moveLocation)
        return True

    def isFalling(self, player):
        moveLocation = list(self.playerLocations[player])
        moveLocation[1] += 1
        if self.levels[self.currentLevel][moveLocation[1]][moveLocation[0]] in self.traversableTiles:   
            print(moveLocation)
            print(self.levels[self.currentLevel][moveLocation[1]][moveLocation[0]])
            return True
        return False

    def checkCompletion(self):
        level = self.levels[self.currentLevel]
        complete = True

        for player in self.currentPlayers:
            playerType = player.type
            playerIndex = player.index
            location = self.playerLocations[playerIndex]
            if level[location[1]][location[0]] != str(playerType):
                complete = False

        if complete:
            self.currentLevel += 1
            self.load()