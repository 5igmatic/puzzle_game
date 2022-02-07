import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile, offset, location, size):
        super().__init__()

        if tile == "t":
            self.image = pygame.Surface((size, size)).convert_alpha()
            self.image.fill("white")
            pos = (offset[0]+location[0]*size, offset[1]+location[1]*size)
            print(pos)
            self.rect = self.image.get_rect(center = pos)

    def update(self, WIN):
        WIN.blit(self.image, self.rect)