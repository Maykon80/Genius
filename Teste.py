import pygame
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

janela = pygame.display.set_mode((800, 400), 0, 32)

background = pygame.Surface(janela.get_size()).convert()
background.fill((255, 255, 255))

circulo_red = pygame.draw.circle(background, (255, 0, 0), (100, 250), 80, 0)
circulo_yeloow = pygame.draw.circle(background, (255, 255, 0), (300, 250), 80, 0)
circulo_green = pygame.draw.circle(background, (0, 255, 0), (500, 250), 80, 0)
circulo_blue = pygame.draw.circle(background, (0, 128, 255), (700, 250), 80, 0)

while True:
    for evento in pygame.event.get():
        if evento.type == QUIT:
            quit()

    janela.blit(background, (0, 0))
    pygame.display.update()
    clock.tick(27)