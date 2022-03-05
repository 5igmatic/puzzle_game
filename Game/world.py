from tile import Tile
from player import Player
import pygame
import copy

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
                           "t0     1t",
                           "ttttttttt"]}
        #playerType (start location)
        self.levelData = {1: [[0, [2, 2]]],
                          2: [[0, [2, 2]]],
                          3: [[0, [6, 4]], [1, [3, 5]]]}
        self.tiles = pygame.sprite.Group()
        self.size = size
        self.playerLocations = []
        self.currentLevel = startLevel
        self.players = [0, 1]
        self.currentPlayers = pygame.sprite.Group()
        self.activePlayerIndex = 0
        self.previousPlayerIndex = 0

        self.playerMovementInstruction = {"fall": [[[0, 1]], [[], [[0, 1], [0, 1]]]],
                                          "walk": [[[1, 0], [0, -1], [1, -1]], [[], [], [], [[1, 1], [1, 0]]]],
                                          "jump": [[[1, 0], [0, -1], [1, -1], [0, -2], [1, -2], [1, -3], [2, -2], [2, -3], [3, -3], [3, -2], [4, -2], [4, -1], [4, 0], [5, 1]], 
                                                  [[], [], [], [[2, 1/3], [2, -1/3], [0, 0]], [[2, 0.4], [2, -0.4], [0, 0]], [[2, 1], [1, -2]], [[2, 1], [1, -2]], [[2, 1], [1, -2]], [[2, 2], [0, 2/3], [2, -2]], [[2, 2], [0, 2/3], [2, -2]], [[2, 3], [3, -2]], [[2, 3], [3, -2]], [[2, 3.4792], [1, 0.5208], [4, -1]], [[2, 4], [4, 0]], []]]}

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
        self.previousPlayerIndex = self.activePlayerIndex
        self.activePlayerIndex += shift
        self.activePlayerIndex %= players

    def doMovement(self):
        for index,player in enumerate(self.currentPlayers):
            if index == self.activePlayerIndex:
                player.doMovement()

        if(self.playerChangeCooldown > 0):
            self.playerChangeCooldown -= 1
            if(self.playerChangeCooldown == 0):
                self.previousPlayerIndex = self.activePlayerIndex

    def updateIndividual(self, object, WIN, shiftX, shiftY):
        rect = object.image.get_rect(center = (object.x + shiftX, object.y + shiftY))
        WIN.blit(object.image, rect)

    def update(self, WIN):
        screenCenterX = WIN.get_width()/2
        screenCenterY = WIN.get_height()/2
        focusX = 0
        focusY = 0
        previousWeight = self.playerChangeCooldown/self.playerChangeCooldownDuration
        activeWeight = 1 - previousWeight
        for index,player in enumerate(self.currentPlayers):
            if index == self.activePlayerIndex:
                focusX += player.x * activeWeight
                focusY += player.y * activeWeight
            if index == self.previousPlayerIndex:
                focusX += player.x * previousWeight
                focusY += player.y * previousWeight

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


    #returns if the region being moved into is blocked
    def isBlocked(self, moveLocation):
        for playerLocation in self.playerLocations:
                if playerLocation == [moveLocation[0], moveLocation[1]]:
                    return True
        if self.levels[self.currentLevel][moveLocation[1]][moveLocation[0]] in self.traversableTiles:
            return False
        return True

    #accessed by the Player class
    def move(self, player, movementType, right):
        moveOrigin = list(self.playerLocations[player])
        multiplier = 1
        if not right:
            multiplier = -1

        instructions = copy.deepcopy(self.playerMovementInstruction[movementType])
        checkList = instructions[0]
        directions = instructions[1]

        for index,check in enumerate(checkList):
            moveLocation = [moveOrigin[0]+check[0]*multiplier, moveOrigin[1]+check[1]]
            if self.isBlocked(moveLocation):
                return directions[index]
        return directions[-1]

    # def isFallBlocked(self, player):
    #     moveLocation = list(self.playerLocations[player])
    #     moveLocation[1] += 1
    #     return self.isBlocked(moveLocation)

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