import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, type, size, x, y, world):
        super().__init__()
        self.type = type
        self.size = size
        self.x = x
        self.y = y
        self.rotation = 0

        self.world = world

        self.original_image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.original_image.fill("red")
        self.image = self.original_image
        self.rotation = 0
        self.moving = False
        self.walking = False
        self.falling = False
        self.right = False
        self.animationFrame = 0

        self.walkFrames = 30
        self.fallFrames = 18

        self.walkPivot = (0, 0)

    def doMovement(self):
        if not self.moving:
            self.checkInputs()
        if self.falling:
            self.fall()
        if self.walking:
            self.walk()
        self.setRotation()

    def checkInputs(self):
        if self.world.isFalling(self.type):
            self.moving = True
            self.falling = True
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and not self.world.isBlocked(self.type, False):
                self.walking = True
                self.right = False
                self.moving = True
                self.walkPivot = (self.x - self.size/2, self.y + self.size/2)
            elif keys[pygame.K_d] and not self.world.isBlocked(self.type, True):
                self.walking = True
                self.right = True
                self.moving = True
                self.walkPivot = (self.x + self.size/2, self.y + self.size/2)
            elif keys[pygame.K_w] and self.world.playerChangeCooldown == 0:
                shift = 1
                self.world.changePlayer(shift)
            elif keys[pygame.K_s] and self.world.playerChangeCooldown == 0:
                shift = -1
                self.world.changePlayer(shift)

    def walk(self):
        if self.animationFrame >= self.walkFrames:
            if self.right:
                shift = [1, 0]
            else:
                shift = [-1, 0]
            self.world.updateLocation(self.type, shift)
            self.moving = False
            self.walking = False
            self.animationFrame = 0
        else:
            self.animationFrame += 1
            direction = -1
            if self.right: direction = 1
            angle = 90 + direction*45 - direction*self.animationFrame*90/self.walkFrames
            radians = angle * math.pi / 180
            self.x = self.walkPivot[0] + self.size/math.sqrt(2) * math.cos(radians)
            self.y = self.walkPivot[1] - self.size/math.sqrt(2) * math.sin(radians)
            self.rotation = angle - 90 - direction * 45

    def fall(self):
        if self.animationFrame >= self.fallFrames:
            shift = [0, 1]
            self.world.updateLocation(self.type, shift)
            self.moving = False
            self.falling = False
            self.animationFrame = 0
        else:
            self.animationFrame += 1
            self.y += self.size/self.fallFrames

    def setRotation(self):
        self.image = pygame.transform.rotate(self.original_image, self.rotation)

