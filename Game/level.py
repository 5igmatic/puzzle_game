from turtle import width
from tile import Tile
from player import Player
import pygame
import copy
import time

class Level:
    def __init__(self, size, font, WIN, MENU, startLevel):
        self.currentLevel = startLevel
        self.WIN = WIN
        self.MENU = MENU
        self.levelActive = False
        self.editorLevel = False

        width = self.WIN.get_width()
        self.exitButton = pygame.surface.Surface((20, 20)).convert_alpha()
        self.exitButton.fill("white")
        self.exitButtonRect = self.exitButton.get_rect(center = (width-20, 20))

        self.restartButton = pygame.surface.Surface((20, 20)).convert_alpha()
        self.restartButton.fill("white")
        self.restartButtonRect = self.restartButton.get_rect(center = (width-60, 20))


        #playerType (start location)
        self.playerPositionIndecies = []
        self.playerPositionSymbols = []
        self.tiles = pygame.sprite.Group()

        self.font = font

        self.size = size
        self.trueSize = size
        self.sizeScaler = 1.01
        self.players = [0, 1]
        self.currentPlayers = pygame.sprite.Group()
        self.activePlayerIndex = 0
        self.previousPlayerIndex = 0

        self.playerChangeCooldown = 0
        #prevents the player from being changed within 30 frames of another change
        self.playerChangeCooldownDuration = 30

    def load(self, levelLayout):
        self.tiles.empty()
        self.currentPlayers.empty()

        rows = len(levelLayout)
        columns = len(levelLayout[0][0])
        self.playerPositionIndecies = [[None]*columns for i in range(rows)]
        self.playerPositionSymbols = [[None]*columns for i in range(rows)]

        rowIndex = 0
        playerIndex = 0
        for row in levelLayout:
            columnIndex = 0
            rowObjects = row[0]
            rowRotations = row[1]
            for object in rowObjects:
                if object != " ":
                    if object == "t":
                        self.tiles.add(Tile(columnIndex, rowIndex, self.size))
                    else:
                        playerRotation = int(rowRotations[columnIndex]) * 90
                        player = Player(playerIndex, object, columnIndex, rowIndex, playerRotation, self)
                        player.updateRotation()
                        self.currentPlayers.add(player)
                        self.playerPositionIndecies[rowIndex][columnIndex] = playerIndex
                        self.playerPositionSymbols[rowIndex][columnIndex] = object
                        playerIndex += 1
                columnIndex += 1
            rowIndex += 1
        self.activePlayerIndex = 0
        #dont know if this is needed: self.previousPlayerIndex = 0

        #sets the initial player to highlighted colour
        self.changePlayer(0)

    #Accessed by the Player class
    def changePlayer(self, shift):
        self.playerChangeCooldown = self.playerChangeCooldownDuration
        players = len(self.currentPlayers.sprites())
        self.activePlayerIndex += shift
        self.activePlayerIndex %= players
        for player in self.currentPlayers:
            if player.index == self.previousPlayerIndex:
                player.original_image.fill("white")
            if player.index == self.activePlayerIndex:
                player.original_image.fill("grey")
            player.image = pygame.transform.rotate(player.original_image, player.rotation)

    def getPlayerFocus(self):
        focusX = 0
        focusY = 0
        previousWeight = self.playerChangeCooldown/self.playerChangeCooldownDuration
        activeWeight = 1 - previousWeight
        for player in self.currentPlayers:
            if player.index == self.activePlayerIndex:
                focusX += player.x * activeWeight
                focusY += player.y * activeWeight
            if player.index == self.previousPlayerIndex:
                focusX += player.x * previousWeight
                focusY += player.y * previousWeight
        return (focusX, focusY)

    def doMovement(self):
        for player in self.currentPlayers:
            if player.index == self.activePlayerIndex:
                player.doMovement()
                if player.instruction == 0:
                    self.checkCompletion()

        if(self.playerChangeCooldown > 0):
            self.playerChangeCooldown -= 1
            if(self.playerChangeCooldown == 0):
                self.previousPlayerIndex = self.activePlayerIndex        

    def updateIndividual(self, object, shiftX, shiftY):
        x = round(self.size*(object.x + shiftX))
        y = round(self.size*(object.y + shiftY))
        rect = object.image.get_rect(center = (x, y))
        self.WIN.blit(object.image, rect)

    # def updateSize(self):
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_UP]:
    #         self.trueSize *= 1/self.sizeScaler
    #         self.size = round(self.trueSize)
    #         for tile in self.tiles:
    #             tile.updateSize(self.size)
    #         for player in self.currentPlayers:
    #             player.updateSize(self.size)
    #     if keys[pygame.K_DOWN]:
    #         self.trueSize *= self.sizeScaler
    #         self.size = round(self.trueSize)
    #         for tile in self.tiles:
    #             tile.updateSize(self.size)
    #         for player in self.currentPlayers:
    #             player.updateSize(self.size)
        
    #     print(self.size)
        

    def updateLevel(self):
        #self.updateSize()
        screenCenterX = self.WIN.get_width()/(2*self.size)
        screenCenterY = self.WIN.get_height()/(2*self.size)
        focus = self.getPlayerFocus()
        shiftX = screenCenterX - focus[0]
        shiftY = screenCenterY - focus[1]
        for tile in self.tiles:
            self.updateIndividual(tile, shiftX, shiftY)
        for player in self.currentPlayers:
            self.updateIndividual(player, shiftX, shiftY)
            self.updateIndividual(player.text, shiftX, shiftY)
        self.WIN.blit(self.exitButton, self.exitButtonRect)
        self.WIN.blit(self.restartButton, self.restartButtonRect)

    def collision(self, checkPlayer):
        collision = False
        checkPlayerRect = checkPlayer.image.get_rect(center = (round(self.size*checkPlayer.x), round(self.size*checkPlayer.y)))
        for tile in self.tiles:
            tileRect = tile.image.get_rect(center = (self.size*tile.x, self.size*tile.y))
            if tileRect.colliderect(checkPlayerRect):
                collision = True
        for player in self.currentPlayers:
            playerRect = player.image.get_rect(center = (self.size*player.x, self.size*player.y))
            if player.index != checkPlayer.index and playerRect.colliderect(checkPlayerRect):
                collision = True
        return collision

#
# process for checking if the produced equation is correct
#

    def determineEquation(self, equalsPos, increment):
        equation = []
        equationIndecies = []
        checkPos = copy.copy(equalsPos)
        while(self.playerPositionSymbols[checkPos[0]][checkPos[1]] != None):
            equationIndecies.append(self.playerPositionIndecies[checkPos[0]][checkPos[1]])
            if checkPos != equalsPos: equation.append(self.playerPositionSymbols[checkPos[0]][checkPos[1]])
            checkPos[1] += increment
        return equation, equationIndecies

    def validSymbolRotation(self, equationIndecies):
        rotationallySymmetric = ["-x÷=", "+"]
        valid = True
        for equationIndeciesSide in equationIndecies:
            for player in self.currentPlayers:
                if player.index in equationIndeciesSide:
                    if player.type in rotationallySymmetric[0]:
                        mod = 180
                    elif player.type in rotationallySymmetric[1]:
                        mod = 90
                    else:
                        mod = 360
                    if player.rotation % mod != 0:
                        valid = False   
        return valid

    #converts adjacent digits into multi-digit numbers
    def order1Calculation(self, equation):
        digits = "1234567890"
        #initialised with None to allow for -1 indexing
        outEquation = [[None], [None]]
        for equationIndex, equationSide in enumerate(equation):
            for symbol in equationSide:
                if symbol in digits:
                    if type(outEquation[equationIndex][-1]) is int:
                        outEquation[equationIndex][-1] = outEquation[equationIndex][-1] * 10 + int(symbol)
                    else:
                        outEquation[equationIndex].append(int(symbol)) 
                else:
                    outEquation[equationIndex].append(symbol)
        #remove Nones from beginning
        outEquation[0].pop(0)
        outEquation[1].pop(0)
        return outEquation

    #multiplies numbers seperated by an x
    def order2Calculation(self, equation):
        #initialised with None to allow for -1 indexing
        outEquation = [[None], [None]]
        for equationIndex, equationSide in enumerate(equation):
            multiply = False
            for element in equationSide:
                if multiply and len(outEquation[equationIndex]) > 1:
                    outEquation[equationIndex][-1] *= element
                    multiply = False
                elif element == "x":
                    multiply = True
                else:
                    outEquation[equationIndex].append(element)
        #remove Nones from beginning
        outEquation[0].pop(0)
        outEquation[1].pop(0)
        return outEquation

    #adds and subtracts numbers seperated by a + or -        
    def order3Calculation(self, equation):
        #initialised with None to allow for -1 indexing
        outEquation = [[None], [None]]
        for equationIndex, equationSide in enumerate(equation):
            add = False
            subtract = False
            for element in equationSide:
                if add and len(outEquation[equationIndex]) > 1:
                    outEquation[equationIndex][-1] += element
                    add = False
                elif subtract and len(outEquation[equationIndex]) > 1:
                    outEquation[equationIndex][-1] -= element
                    subtract = False
                elif element == "+":
                    add = True
                elif element == "-":
                    subtract = True
                else:
                    outEquation[equationIndex].append(element)
        #remove Nones from beginning
        outEquation[0].pop(0)
        outEquation[1].pop(0)
        return outEquation

    def checkCompletion(self):
        rows = len(self.playerPositionSymbols)
        columns = len(self.playerPositionSymbols[0])
        equalsPos = None
        equation = [[], []]
        equationIndecies = [[], []]

        for i in range(rows):
            for j in range(columns):
                if self.playerPositionSymbols[i][j] == "=":
                    equalsPos = [i, j]
        equation[0], equationIndecies[0] = self.determineEquation(equalsPos, -1)
        if len(equation[0])>0: equation[0].reverse()
        equation[1], equationIndecies[1] = self.determineEquation(equalsPos, 1)
        
        if self.validSymbolRotation(equationIndecies):
            equation = self.order1Calculation(equation)
            equation = self.order2Calculation(equation)
            equation = self.order3Calculation(equation)
            if equation[0] == equation[1] and equation[0] != []:
                time.sleep(0.5)
                self.currentLevel += 1
                self.MENU.loadNext()
