import pygame
from player import Player
from world import World

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)

FPS = 60
size = 80

clock = pygame.time.Clock()

world = World(size)
#Jeff is a basic square, basic sounds like Bezos, Bezos -> Jeff, also Jeff is a basic name
jeff = Player(size, world)


def calculateMovement():
    jeff.doMovement()
    
    
def update():
    WIN.fill("black")
    WIN.blit(jeff.image, jeff.rect)
    world.update(WIN)
    pygame.display.update()

def main():
    world.load(0, (60, 140))
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        calculateMovement()
        update()

if __name__ == "__main__":
    main()
