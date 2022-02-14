import pygame
from world import World

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, vsync=1)

FPS = 60
size = 80
startLevel = 1

clock = pygame.time.Clock()

world = World(size, startLevel)

def update():
    WIN.fill("black")
    world.update(WIN)
    pygame.display.update()

def main():
    world.load()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.VIDEORESIZE:
                WIN.blit(pygame.transform.scale(WIN, event.dict['size']), (0, 0))
                pygame.display.update()
            elif event.type == pygame.VIDEOEXPOSE:  # handles window minimising/maximising
                WIN.fill((0, 0, 0))
                WIN.blit(pygame.transform.scale(WIN, WIN.get_size()), (0, 0))
                pygame.display.update()

        world.doMovement()
        update()

if __name__ == "__main__":
    main()
