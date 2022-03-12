import pygame
import math
from text import Text

class Player(pygame.sprite.Sprite):
    def __init__(self, index, type, x, y, rotation, world):
        super().__init__()
        self.index = index
        self.type = type
        self.x = x
        self.y = y
        self.rotation = rotation
        self.size = world.size

        self.world = world

        self.original_image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.original_image.fill("white")
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        
        self.text = Text(type, x, y, world.font)

        self.instruction = 0
        self.direction = 1
        self.jumpDirection = 1

        self.walkFrames = 30
        self.walkRotation = 0
        self.fallFrames = 18
        self.jumpFrames = 24
        self.jumpedDist = 0

        self.cornerLeeway = 0.2


        self.triedDirections = []

    # def updateSize(self, size):
    #     self.size = size
    #     self.image = pygame.transform.scale(self.image, (size, size))

    def doMovement(self):
        if self.instruction == 0 and self.world.playerChangeCooldown == 0:
            self.checkInputs()
            #if a movement has just been initiated, remove the player from its previous position
            if self.instruction != 0:
                self.world.playerPositionIndecies[round(self.y)][round(self.x)] = None
                self.world.playerPositionSymbols[round(self.y)][round(self.x)] = None

        if self.instruction == 1:
            self.fall()
        if self.instruction == 2:
            self.walk()
        if self.instruction == 3:
            self.jump()
        self.triedDirections.clear()
        self.text.x = self.x
        self.text.y = self.y
        self.updateRotation()

    def updateRotation(self):
        self.text.image = pygame.transform.rotate(self.text.original_image, self.rotation)
        self.image = pygame.transform.rotate(self.original_image, self.rotation)

    def checkInputs(self):
        keys = pygame.key.get_pressed()
        if 1 not in self.triedDirections:
            self.instruction = 1
            self.triedDirections.append(1)
        elif keys[pygame.K_a] and [2, -1] not in self.triedDirections:
            self.instruction = 2
            self.direction = -1
            self.walkRotation = self.rotation % 90 + 45
            self.triedDirections.append([2, -1])
        elif keys[pygame.K_d] and [2, 1] not in self.triedDirections:
            self.instruction = 2
            self.direction = 1
            self.walkRotation = self.rotation % 90 + 135
            self.triedDirections.append([2, 1])
        elif keys[pygame.K_q] and [3, -1] not in self.triedDirections:
            self.instruction = 3
            self.direction = -1
            self.jumpedDist = 0
            self.jumpDirection = 1
            self.triedDirections.append([3, -1])
        elif keys[pygame.K_e] and [3, 1] not in self.triedDirections:
            self.instruction = 3
            self.direction = 1
            self.jumpedDist = 0
            self.jumpDirection = 1
            self.triedDirections.append([3, 1])
        elif keys[pygame.K_w]:
            shift = 1
            self.world.changePlayer(shift)
        elif keys[pygame.K_s]:
            shift = -1
            self.world.changePlayer(shift)

    def movementEnd(self):
        self.instruction = 0
        self.x = round(self.x*self.size)/self.size
        self.y = round(self.y*self.size)/self.size
        self.world.playerPositionIndecies[round(self.y)][round(self.x)] = self.index
        self.world.playerPositionSymbols[round(self.y)][round(self.x)] = self.type
        self.doMovement()

    def fall(self):
        self.y += 1/self.fallFrames
        if self.world.collision(self):
            self.y -= 1/self.fallFrames
            self.movementEnd()
        
    def walk(self):
        self.walkMovement(90/self.walkFrames)
        if self.world.collision(self):
            change = self.rotation % 90
            if change > 45: change -= 90
            else: change = -change
            self.walkMovement(change)
            self.movementEnd()

    def walkMovement(self, change):
        previousRotation = self.walkRotation
        self.walkRotation -= self.direction * change
        self.rotation -= self.direction * change
        self.x += math.sqrt(2)/2*(math.cos(self.walkRotation*math.pi/180) - math.cos(previousRotation*math.pi/180))
        self.y -= math.sqrt(2)/2*(math.sin(self.walkRotation*math.pi/180) - math.sin(previousRotation*math.pi/180))
        self.image = pygame.transform.rotate(self.original_image, self.rotation)

    def jump(self):
        self.jumpMovement(self.jumpDirection/self.jumpFrames)
        if self.world.collision(self):
            self.jumpMovement(-self.jumpDirection/self.jumpFrames)
            if self.rotation % 90 == 0:
                self.jumpedDist = 0     
                self.movementEnd()
            else:
                angle = 135 - self.rotation % 90
                cornerX = self.x + math.sqrt(2)/2*(math.cos(angle*math.pi/180))
                cornerY = self.y + math.sqrt(2)/2*(math.sin(angle*math.pi/180))
                if cornerX % 1 < 0.5 + self.cornerLeeway and cornerX % 1 > 0.5 - self.cornerLeeway and cornerY % 1 < 0.5 + self.cornerLeeway and cornerY % 1 > 0.5 - self.cornerLeeway:
                    self.instruction = 2        
                    self.jumpedDist = 0
                    self.walkRotation = self.rotation % 90 + 45
                    cornerX = round(cornerX-0.5)+0.5
                    cornerY = round(cornerY-0.5)+0.5
                    self.x = cornerX - math.sqrt(2)/2*(math.cos(angle*math.pi/180))
                    self.y = cornerY - math.sqrt(2)/2*(math.sin(angle*math.pi/180))
                else: 
                    self.instruction = 3
                    self.jumpDirection = -1
                self.doMovement()

    def jumpMovement(self, change):
        self.x += self.direction * change
        self.y += (2/3)*(((self.jumpedDist+change)*(self.jumpedDist+change)-4*(self.jumpedDist+change)) - (self.jumpedDist*self.jumpedDist-4*self.jumpedDist))
        self.jumpedDist += change
        self.rotation -= self.direction * 90 * change
        self.image = pygame.transform.rotate(self.original_image, self.rotation)