import pygame
import pickle

class MainMenu:
    def __init__(self, WIN):
        self.WIN = WIN
        self.LEVEL = None

        with open('levels.txt', 'rb') as f:
            self.levels = pickle.load(f)
        
        #self.background = pygame.surface.Surface()
        self.playButton = pygame.surface.Surface((400, 150)).convert_alpha()
        self.playButton.fill("white")
        self.playButtonRect = self.playButton.get_rect(center = (0, 0))
        #self.playText = pygame.surface.Surface()
    
    def updateDisplay(self):
        width = self.WIN.get_width()
        height = self.WIN.get_height()
        self.playButtonRect = self.playButton.get_rect(center = (width/2, height/2-200))
        self.LEVEL.exitButtonRect = self.LEVEL.exitButton.get_rect(center = (width-20, 20))
        self.display()

    def display(self):
        self.WIN.blit(self.playButton, self.playButtonRect)

    def mouseClick(self):
        mousePosition = pygame.mouse.get_pos()
        if self.LEVEL.levelActive:
            if self.LEVEL.exitButtonRect.collidepoint(mousePosition):
                self.LEVEL.levelActive = False
        else:
            if self.playButtonRect.collidepoint(mousePosition):
                self.loadNext()

    def loadNext(self):
        self.LEVEL.levelActive = True
        self.LEVEL.load(self.levels[self.LEVEL.currentLevel])




# class LevelSelector:
#     def __init__(self):