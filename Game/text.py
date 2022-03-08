import pygame

class Text(pygame.sprite.Sprite):
    def __init__(self, type, x, y, font):
        self.original_image = font.render(type, True, "red")
        self.image = self.original_image
        self.x = x
        self.y = y


    