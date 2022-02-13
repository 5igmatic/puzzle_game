import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile, offset, location, size):
        super().__init__()

        self.image = pygame.Surface((size, size)).convert_alpha()
        if tile == "t":
            self.image.fill("white")

        #goal tiles
        if tile == "0":
            self.image.fill((255, 0, 0, 150))

        
        self.x = offset[0]+location[0]*size
        self.y = offset[1]+location[1]*size