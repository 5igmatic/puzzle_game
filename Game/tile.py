import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile, location, size):
        super().__init__()

        self.image = pygame.Surface((size, size)).convert_alpha()
        if tile == "t":
            self.image.fill("white")

        #goal tiles
        if tile == "0":
            self.image.fill((255, 0, 0, 150))

        
        self.x = location[0]*size
        self.y = location[1]*size