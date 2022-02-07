from logging import setLogRecordFactory
from tkinter import CENTER
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, offset, location, size):
        super().__init__()
        self.image = pygame.Surface((size, size)).convert_alpha()
        pos = (offset[0]+location[0]*size, offset[1]+location[1]*size)
        self.rect = self.image.get_rect(center = pos)
