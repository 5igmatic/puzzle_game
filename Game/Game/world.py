from tile import Tile
from player import Player
import pygame

class World:
    def __init__(self, size, offset, startLevel):
        self.traversableTiles = " 0"

        self.levels = {0: ["ttttttt",
                           "t     t",
                           "t    0t",
                           "ttttttt"],
            
                       1: ["ttttttt",
                           "t     t",
                           "t     t",
                           "tttt 0t",
                           "   tttt"],
                           
                       2: ["ttttttttt",
                           "t       t",
                           "t       t",
                           "t       t",
                           "t       t",
                           "t      0t",
                           "ttttttttt"]}
        #players (start location)
        self.levelData = {0: [[0, [2, 2]]],
                          1: [[0, [3, 2]]],
                          2: [[0, [3, 4]]]}
        self.tiles = pygame.sprite.Group()
        self.size = size
        self.offset = offset
        self.playerLocations = {"square": [0, 0]}
        self.currentLevel = startLevel
        self.players = ["square"]
        self.currentPlayers = pygame.sprite.Group()
        self.activePlayerIndex = 0

        self.playerChangeCooldown = 0
        #the player can only change Players every 30 frames
        self.playerChangeCooldownDuration = 30

    def load(self):
        self.tiles.empty()
        self.currentPlayers.empty()
        levelLayout = self.levels[self.currentLevel]
        self.getCurrentPlayers()
        rowIndex = 0
        for row in levelLayout:
            tileIndex = 0
            for tile in row:
                if tile != " ":
                    self.tiles.add(Tile(tile, self.offset, (tileIndex, rowIndex), self.size))
                tileIndex += 1
            rowIndex += 1

    def getCurrentPlayers(self):
        currentLevelData = self.levelData[self.currentLevel]
        first = True
        for playerData in currentLevelData:
            playerIndex = playerData[0]
            playerPosition = playerData[1]
            playerType = self.players[playerIndex]
            self.playerLocations[playerType] = playerPosition
            x = playerPosition[0]*self.size + self.offset[0]
            y = playerPosition[1]*self.size + self.offset[1]
            player = Player(playerType, self.size, x, y, self)
            self.currentPlayers.add(player)
        self.activePlayerIndex = 0

    #Accessed by the Player class
    def changePlayer(self, shift):
        self.playerChangeCooldown = self.playerChangeCooldownDuration
        players = len(self.currentPlayers.sprites())
        self.activePlayerIndex += shift
        self.activePlayerIndex %= players
        print(self.activePlayerIndex)

    def doMovement(self):
        for index,player in enumerate(self.currentPlayers):
            if index == self.activePlayerIndex:
                player.doMovement()

        if(self.playerChangeCooldown > 0):
            self.playerChangeCooldown -= 1

    def updateIndividual(self, object, WIN):
        WIN.blit(object.image, object.rect)

    def update(self, WIN):
        for tile in self.tiles:
            self.updateIndividual(tile, WIN)
        for player in self.currentPlayers:
            self.updateIndividual(player, WIN)

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
        if self.levels[self.currentLevel][moveLocation[1]][moveLocation[0]] in self.traversableTiles:
            return False
        return True

    def isFalling(self, player):
        moveLocation = list(self.playerLocations[player])
        moveLocation[1] += 1
        if self.levels[self.currentLevel][moveLocation[1]][moveLocation[0]] in self.traversableTiles:
            return True
        return False

    def checkCompletion(self):
        level = self.levels[self.currentLevel]
        complete = True

        for player in self.currentPlayers:
            playerClass = player.type
            location = self.playerLocations[playerClass]
            playerGoalID = self.players.index(playerClass)
            if level[location[1]][location[0]] != str(playerGoalID):
                complete = False

        if complete:
            self.currentLevel += 1
            self.load()