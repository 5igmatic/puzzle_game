from tkinter import CENTER, HORIZONTAL
import pygame

WIDTH, HEIGHT = 700, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


vertical_line = pygame.Surface((1, 600))
vertical_line.fill('white')
for i in range(8):
    WIN.blit(vertical_line, (100*i, 0))

horizontal_line = pygame.Surface((700, 1))
horizontal_line.fill('white')
for i in range(7):
    WIN.blit(horizontal_line, (0, 100*i))

for i in range(801):
    x = i/200
    y = -(2/3)*(x*x-4*x)
    character = pygame.Surface((100, 100)).convert_alpha()
    intensity = i/3.14
    colour = (255, intensity, 255-intensity)
    character.fill(colour)
    character = pygame.transform.rotate(character, -x*90)
    character_rect = character.get_rect(center = (100*x+150, 500-100*y-50))
    WIN.blit(character, character_rect)
    pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()