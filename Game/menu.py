import pygame
import pickle

class MainMenu:
    def __init__(self, WIN):
        self.WIN = WIN
        self.LEVEL = None
        self.EDITOR = None

        with open('levels.txt', 'rb') as f:
            self.levels = pickle.load(f)
        
        #self.background = pygame.surface.Surface()
        self.playButton = pygame.surface.Surface((400, 150)).convert_alpha()
        self.playButton.fill("white")
        self.playButtonRect = self.playButton.get_rect(center = (0, 0))
        #self.playText = pygame.surface.Surface()

        self.editorButton = pygame.surface.Surface((400, 150)).convert_alpha()
        self.editorButton.fill("white")
        self.editorButtonRect = self.editorButton.get_rect(center = (0, 0))
    
    def updateDisplay(self):
        width = self.WIN.get_width()
        height = self.WIN.get_height()
        self.playButtonRect = self.playButton.get_rect(center = (width/2, height/2-200))
        self.editorButtonRect = self.editorButton.get_rect(center = (width/2, height/2+200))
        self.LEVEL.exitButtonRect = self.LEVEL.exitButton.get_rect(center = (width-20, 20))
        self.EDITOR.exitButtonRect = self.EDITOR.exitButton.get_rect(center = (width-20, 20))
        self.LEVEL.restartButtonRect = self.LEVEL.restartButton.get_rect(center = (width-60, 20))
        self.EDITOR.restartButtonRect = self.EDITOR.restartButton.get_rect(center = (width-60, 20))
        self.EDITOR.playButtonRect = self.EDITOR.playButton.get_rect(center = (width-100, 20))
        self.display()

    def display(self):
        self.WIN.blit(self.playButton, self.playButtonRect)
        self.WIN.blit(self.editorButton, self.editorButtonRect)

    def mouseClick(self):
        mousePosition = pygame.mouse.get_pos()
        if self.LEVEL.levelActive:
            if self.LEVEL.exitButtonRect.collidepoint(mousePosition):
                self.LEVEL.levelActive = False
                if self.LEVEL.editorLevel:
                    self.EDITOR.editorActive = True
                    self.LEVEL.editorLevel = False
            if self.LEVEL.restartButtonRect.collidepoint(mousePosition):
                if self.LEVEL.editorLevel:
                    self.loadEditor()
                else:
                    self.loadNext()

        elif self.EDITOR.editorActive:
            if self.EDITOR.exitButtonRect.collidepoint(mousePosition):
                self.EDITOR.editorActive = False
            if self.EDITOR.restartButtonRect.collidepoint(mousePosition):
                self.EDITOR.initialise(10, 8)
            if self.EDITOR.playButtonRect.collidepoint(mousePosition) and self.EDITOR.validLevel():
                self.loadEditor()
            self.EDITOR.mouseClick()

        else:
            if self.playButtonRect.collidepoint(mousePosition):
                self.loadNext()
            if self.editorButtonRect.collidepoint(mousePosition):
                self.EDITOR.editorActive = True
                self.EDITOR.initialise(10, 8)

    def loadNext(self):
        self.LEVEL.levelActive = True
        self.LEVEL.load(self.levels[self.LEVEL.currentLevel])

    def loadEditor(self):
        self.LEVEL.levelActive = True
        self.LEVEL.editorLevel = True
        self.EDITOR.editorActive = False
        self.LEVEL.load(self.EDITOR.layout)




# class LevelSelector:
#     def __init__(self):