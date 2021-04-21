import sys
import pygame

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([600,600])
font = pygame.font.SysFont('Georgia',30)

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    text = 'Testing'
    word = font.render(text,False,[120,120,120])
    screen.blit(word,[250,250])

    pygame.display.flip()
    screen.fill((0,0,0))