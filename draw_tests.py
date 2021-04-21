import sys
import pygame
from Constants import Colors

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([600,600])

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Change here
    box = [50,50,150,150]
    pygame.draw.rect(screen,Colors.DARKBLUE,box,border_radius=7)

    pygame.display.flip()
    screen.fill(Colors.BLACK)