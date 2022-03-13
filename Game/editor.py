from turtle import width
import pygame
from tile import Tile
from player import Player

class Editor:
    def __init__(self, size, font, WIN):
        self.editorActive = False

        self.cameraSpeed = 5
        self.cameraX = 0
        self.cameraY = 0

        self.activePlayer = None
        self.rotationCooldown = 0
        self.rotationCooldownDuration = 20

        self.tiles = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.playerIndex = 0

        self.size = size
        self.font = font
        self.WIN = WIN

        width = self.WIN.get_width()
        self.exitButton = pygame.surface.Surface((20, 20)).convert_alpha()
        self.exitButton.fill("white")
        self.exitButtonRect = self.exitButton.get_rect(center = (width-20, 20))

        self.restartButton = pygame.surface.Surface((20, 20)).convert_alpha()
        self.restartButton.fill("white")
        self.restartButtonRect = self.restartButton.get_rect(center = (width-60, 20))

        self.playButton = pygame.surface.Surface((20, 20)).convert_alpha()
        self.playButton.fill("white")
        self.playButtonRect = self.playButton.get_rect(center = (width-100, 20))

        self.equationKeys = {pygame.K_0: "0",
                             pygame.K_1: "1",
                             pygame.K_2: "2",
                             pygame.K_3: "3",
                             pygame.K_4: "4",
                             pygame.K_5: "5",
                             pygame.K_6: "6",
                             pygame.K_7: "7",
                             pygame.K_8: "8",
                             pygame.K_9: "9",
                             pygame.K_EQUALS: "=",
                             pygame.K_x: "x",
                             pygame.K_SLASH: "÷",
                             pygame.K_p: "+",
                             pygame.K_MINUS: "-"}

    def initialise(self, width, height):
        self.tiles.empty()
        self.players.empty()

        self.width = width
        self.height = height
        self.cameraX = width/2-0.5
        self.cameraY = height/2-0.5

        self.tilePositions = [[" "]*width for i in range(height)]
        for index in range(width):
            self.tilePositions[0][index] = "t"
            self.tilePositions[-1][index] = "t"
            newTile = Tile(index, 0, self.size)
            self.tiles.add(newTile)
            newTile = Tile(index, height-1, self.size)
            self.tiles.add(newTile)
        for index,tileRow in enumerate(self.tilePositions):
            tileRow[0] = "t"
            tileRow[width-1] = "t"
            newTile = Tile(0, index, self.size)
            self.tiles.add(newTile)
            newTile = Tile(width-1, index, self.size)
            self.tiles.add(newTile)

    def doMovement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.cameraY -= self.cameraSpeed/self.size
        if keys[pygame.K_s]:
            self.cameraY += self.cameraSpeed/self.size
        if keys[pygame.K_a]:
            self.cameraX -= self.cameraSpeed/self.size
        if keys[pygame.K_d]:
            self.cameraX += self.cameraSpeed/self.size
        if keys[pygame.K_t]:
            self.placeTile()
        for key in self.equationKeys:
            if keys[key]:
                self.activePlayer.type = self.equationKeys[key]
                self.activePlayer.text.updateText(self.equationKeys[key])
        if keys[pygame.K_BACKSPACE]:
            self.tilePositions[self.activePlayer.y][self.activePlayer.x] = " "
            self.players.remove(self.activePlayer)
        if self.rotationCooldown == 0:
            if keys[pygame.K_r]:
                self.activePlayer.rotation += 90
                self.activePlayer.updateRotation()
                self.rotationCooldown = self.rotationCooldownDuration
        else:
            self.rotationCooldown -= 1
        self.convertLayoutToList()

    def validLevel(self):
        for player in self.players:
            if player.type == "=":
                return True
        return False

    def mouseClick(self):
        for player in self.players:
            #gets the pixel location of the center of the player
            playerScreenPosX = (player.x - self.cameraX) * self.size + self.WIN.get_width()/2
            playerScreenPosY = (player.y - self.cameraY) * self.size + self.WIN.get_height()/2
            rect = player.image.get_rect(center = (playerScreenPosX, playerScreenPosY))
            if rect.collidepoint(pygame.mouse.get_pos()):
                self.setActivePlayer(player)

    def setActivePlayer(self, player):
        if self.activePlayer != None:
            self.activePlayer.original_image.fill("white")
            self.activePlayer.image = self.activePlayer.original_image
        self.activePlayer = player
        self.activePlayer.original_image.fill("grey")
        self.activePlayer.image = self.activePlayer.original_image

    def placeTile(self):
        mousePos = pygame.mouse.get_pos()
        mousePosX = (mousePos[0]-self.WIN.get_width()/2)/self.size
        mousePosY = (mousePos[1]-self.WIN.get_height()/2)/self.size
        gridX = mousePosX + self.cameraX
        gridY = mousePosY + self.cameraY
        gridX = round(gridX)
        gridY = round(gridY)
        if gridX > 0 and gridX < self.width-1 and gridY > 0 and gridY < self.height-1:
            unoccupied = True
            for player in self.players:
                if gridX == player.x and gridY == player.y:
                    unoccupied = False
            if unoccupied:
                newPlayer = Player(self.playerIndex, " ", gridX, gridY, 0, self)
                self.players.add(newPlayer)
                self.setActivePlayer(newPlayer)
                self.playerIndex += 1

    def updateIndividual(self, object, shiftX, shiftY):
        x = round(self.size*(object.x + shiftX))
        y = round(self.size*(object.y + shiftY))
        rect = object.image.get_rect(center = (x, y))
        self.WIN.blit(object.image, rect)

    def updateEditor(self):
        screenCenterX = self.WIN.get_width()/(2*self.size)
        screenCenterY = self.WIN.get_height()/(2*self.size)
        shiftX = screenCenterX - self.cameraX
        shiftY = screenCenterY - self.cameraY
        for tile in self.tiles:
            self.updateIndividual(tile, shiftX, shiftY)
        for player in self.players:
            self.updateIndividual(player, shiftX, shiftY)
            self.updateIndividual(player.text, shiftX, shiftY)
        self.WIN.blit(self.exitButton, self.exitButtonRect)
        self.WIN.blit(self.restartButton, self.restartButtonRect)
        self.WIN.blit(self.playButton, self.playButtonRect)

    def convertLayoutToList(self):
        self.tileRotations = [[" "]*self.width for i in range(self.height)]
        for player in self.players:
            if player.type == " ": player.type = "t"
            self.tilePositions[player.y][player.x] = player.type
            self.tileRotations[player.y][player.x] = str(int(player.rotation % 360 / 90))

        self.layout = []
        for row in range(self.height):
            positionsRow = ""
            rotationsRow = ""
            for position in self.tilePositions[row]:
                positionsRow += position
            for rotation in self.tileRotations[row]:
                rotationsRow += rotation
            rowData = [positionsRow, rotationsRow]
            self.layout.append(rowData)
