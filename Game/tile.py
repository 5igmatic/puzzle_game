import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile, x, y, size):
        super().__init__()

        self.image = pygame.Surface((size, size)).convert_alpha()
        self.type = tile
        if tile == "t":
            self.image.fill("grey")
        
        self.x = x
        self.y = y

    # def updateSize(self, size):
    #     self.size = size
    #     self.image = pygame.transform.scale(self.image, (size, size))