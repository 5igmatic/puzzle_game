import pygame
from level import Level
from menu import MainMenu

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, vsync=1)

FPS = 6000
size = 80
startLevel = 3
font = pygame.font.SysFont('mathtt', size)

clock = pygame.time.Clock()

startLevel = 1
MENU = MainMenu(WIN)
LEVEL = Level(size, font, WIN, MENU, startLevel)
MENU.LEVEL = LEVEL

#overarching update of entire world

def main():
    while True:
        clock.tick(FPS)
        #checks for window operations
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.VIDEORESIZE:
                WIN.blit(pygame.transform.scale(WIN, event.dict['size']), (0, 0))
                MENU.updateDisplay()
                pygame.display.update()
            elif event.type == pygame.VIDEOEXPOSE:  # handles window minimising/maximising
                WIN.fill((0, 0, 0))
                WIN.blit(pygame.transform.scale(WIN, WIN.get_size()), (0, 0))
                MENU.updateDisplay()
                pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                MENU.mouseClick()
     
        WIN.fill("black")
        if LEVEL.levelActive:
            LEVEL.doMovement()
            LEVEL.updateLevel()
        else:
            MENU.updateDisplay()
        pygame.display.update()

if __name__ == "__main__":
    main()
