import pygame

class Text(pygame.sprite.Sprite):
    def __init__(self, type, x, y, font):
        self.type = type
        self.font = font
        self.original_image = font.render(type, True, "red")
        self.image = self.original_image
        self.x = x
        self.y = y

    def updateText(self, type):
        self.type = type
        self.original_image = self.font.render(type, True, "red")
        self.image = self.original_image