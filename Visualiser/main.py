from tkinter import Widget
import pygame

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#alter the dimensions of the collider and starting position for different results
collider = pygame.Surface((WIDTH, 100))
collider.fill('white')
collider_rect = collider.get_rect(topleft = (0, 500))
WIN.blit(collider, collider_rect)

vertical_line = pygame.Surface((1, HEIGHT))
vertical_line.fill('white')
for i in range(8):
    WIN.blit(vertical_line, (100*i, 0))

horizontal_line = pygame.Surface((WIDTH, 1))
horizontal_line.fill('white')
for i in range(8):
    WIN.blit(horizontal_line, (0, 100*i))

for i in range(1001):
    x = i/200
    y = -(2/3)*(x*x-4*x)
    character = pygame.Surface((100, 100)).convert_alpha()
    intensity = i/4
    colour = (255, intensity, 255-intensity)
    character.fill(colour)
    character = pygame.transform.rotate(character, -x*90%360)
    character_rect = character.get_rect(center = (100*x+150, 500-100*y-50))

    if character_rect.colliderect(collider_rect):
        break

    WIN.blit(character, character_rect)
    pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
