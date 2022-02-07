import pygame
from player import Player
from world import World

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)

FPS = 60

clock = pygame.time.Clock()

#Jeff is a basic square, basic sounds like Bezos, Bezos -> Jeff, also Jeff is a basic name
jeff = Player()
world = World()


def calculateMovement():
    jeff.doMovement()
    
    
def update():
    WIN.fill("black")
    WIN.blit(jeff.image, jeff.rect)
    pygame.display.update()

def main():
    world.load(0, (0, 0), 80)
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
