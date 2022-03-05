import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, index, type, size, x, y, world):
        super().__init__()
        self.index = index
        self.type = type
        self.size = size
        self.x = x
        self.y = y
        self.rotation = 0

        self.world = world

        self.original_image = pygame.Surface((self.size, self.size)).convert_alpha()
        if type == 0:
            self.original_image.fill("red")
        if type == 1:
            self.original_image.fill("green")
        self.image = self.original_image
        self.rotation = 0
        self.right = False
        self.animationFrame = -1

        self.directions = []

        self.walkAnglePerFrame = 3
        self.walkFrames = 30
        self.fallFrames = 18
        self.jumpFrames = 24

        self.pivot = (0, 0)

    def doMovement(self):
        if len(self.directions) == 0:
            self.x = round(self.x)
            self.y = round(self.y)
            self.checkInputs()

        if len(self.directions) > 1:
            nextDirection = self.directions[0]
            if nextDirection[0] == 0:
                self.fall(nextDirection[1])
            if nextDirection[0] == 1:
                self.walk(nextDirection[1])
            if nextDirection[0] == 2:
                self.jump(nextDirection[1])
        
        if len(self.directions) == 1:
            shift = self.directions[-1]
            if not self.right:
                shift[0] = -shift[0]
            self.world.updateLocation(self.index, shift)
            self.directions.pop()
        
        self.setRotation()

    def checkInputs(self):
        self.directions = self.world.move(self.index, "fall", True)
        if len(self.directions) == 0 and self.world.playerChangeCooldown == 0:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.directions = self.world.move(self.index, "walk", False)
                self.right = False
            elif keys[pygame.K_d]:
                self.directions = self.world.move(self.index, "walk", True)
                self.right = True
            elif keys[pygame.K_q]:
                self.directions = self.world.move(self.index, "jump", False)
                self.right = False
            elif keys[pygame.K_e]:
                self.directions = self.world.move(self.index, "jump", True)
                self.right = True
            elif keys[pygame.K_w] and self.world.playerChangeCooldown == 0:
                shift = 1
                self.world.changePlayer(shift)
            elif keys[pygame.K_s] and self.world.playerChangeCooldown == 0:
                shift = -1
                self.world.changePlayer(shift)

    def walk(self, duration):
        direction = -1
        if self.right: direction = 1

        if self.animationFrame == -1:
            self.animationFrame = (1-duration)*self.walkFrames
            angle = 90 + direction*45 - direction*self.animationFrame*90/self.walkFrames
            radians = angle * math.pi / 180
            self.pivot = (self.x - self.size/math.sqrt(2) * math.cos(radians), self.y + self.size/math.sqrt(2) * math.sin(radians))
        if self.animationFrame + 1 > self.walkFrames:
            remainingChange = self.walkFrames - self.animationFrame
            self.walkMovement(remainingChange, direction)
            self.animationFrame = -1
            self.directions.pop(0)
            return None
        
        self.walkMovement(1, direction)

    def walkMovement(self, change, direction):
            self.animationFrame += change
            angle = 90 + direction*45 - direction*self.animationFrame*90/self.walkFrames
            radians = angle * math.pi / 180
            self.x = self.pivot[0] + self.size/math.sqrt(2) * math.cos(radians)
            self.y = self.pivot[1] - self.size/math.sqrt(2) * math.sin(radians)
            self.rotation = angle - 90 - direction * 45

    def fall(self, duration):
        if self.animationFrame == -1:
            self.animationFrame = 0
            self.pivot = [self.x, self.y]
        if self.animationFrame == duration*self.fallFrames:
            self.animationFrame = -1
            self.directions.pop(0)
        else:
            self.animationFrame += 1
            self.y = self.pivot[1] + self.size*self.animationFrame/self.fallFrames

    def jump(self, duration):
        internalDirection = 1
        initialRotation = 0
        if duration < 0:
            internalDirection = -1
            duration *= -1

        if self.animationFrame == -1:
            if internalDirection == 1:
                self.pivot = [self.x, self.y]
                self.animationFrame = 0
            else:
                self.animationFrame = duration*self.jumpFrames
        
        self.jumpMovement(internalDirection, initialRotation)

        if self.animationFrame + 1 > duration*self.jumpFrames or self.animationFrame - 1 < 0:
            if(internalDirection == 1):
                remainingChange = duration*self.jumpFrames - self.animationFrame
            else:
                remainingChange = self.animationFrame
            self.jumpMovement(remainingChange, initialRotation)
            self.animationFrame = -1
            self.directions.pop(0)
            return None

    def jumpMovement(self, change, initialRotation):
        direction = -1
        if self.right: direction = 1
        self.animationFrame += change
        xShift = self.animationFrame/self.jumpFrames
        self.x = direction * self.size * xShift + self.pivot[0]
        self.y = self.size * (2/3)*(xShift*xShift-4*xShift) + self.pivot[1]
        self.rotation = initialRotation - direction * self.animationFrame * 90/self.jumpFrames

    def setRotation(self):
        self.image = pygame.transform.rotate(self.original_image, self.rotation)

