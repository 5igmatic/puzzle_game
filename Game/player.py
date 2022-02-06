import pygame
import math

class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 100
        self.x = 300
        self.y = 300
        self.rotation = 0

        self.original_image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.original_image.fill("white")
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.rotation = 0
        self.moving = False
        self.walking = False
        self.right = False
        self.animationFrame = 0

        self.walkFrames = 30

        self.walkPivot = (0, 0)

    def doMovement(self):
        if not self.moving:
            self.checkInputs()
        if self.walking:
            self.walk()
        self.setRotation()
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def checkInputs(self):
        keys = pygame.key.get_pressed()
        #check if blocked
        if keys[pygame.K_a]:
            self.walking = True
            self.right = False
            self.moving = True
            self.walkPivot = (self.x - self.size/2, self.y + self.size/2)
        elif keys[pygame.K_d]:
            self.walking = True
            self.right = True
            self.moving = True
            self.walkPivot = (self.x + self.size/2, self.y + self.size/2)

    def walk(self):
        if self.animationFrame >= self.walkFrames:
            self.moving = False
            self.walking = False
            self.animationFrame = 0
        else:
            self.animationFrame += 1
            direction = -1
            if self.right: direction = 1
            angle = 90 + direction*45 - direction*self.animationFrame*90/self.walkFrames
            print(angle)
            radians = angle * math.pi / 180
            print(radians)
            self.x = self.walkPivot[0] + self.size/math.sqrt(2) * math.cos(radians)
            self.y = self.walkPivot[1] - self.size/math.sqrt(2) * math.sin(radians)
            self.rotation = angle - 90 - direction * 45

    def setRotation(self):
        self.image = pygame.transform.rotate(self.original_image, self.rotation)

