import random
import time
import pygame
from pygame.locals import *

pygame.init()                                                                   # Inicia Pygame
clock = pygame.time.Clock()                                                     # clock do jogo
fontes = pygame.font.SysFont('Arial', 40)

janela = pygame.display.set_mode((800, 400), 0, 32)                             # Janela

background = pygame.image.load('Fundo.png').convert()                           # Fundo

# Circulos
circulo_red = {'cor': [(155, 0, 0), (255, 0, 0)], 'posicao': (103, 255)}
circulo_yellow = {'cor': [(155, 155, 0), (255, 255, 0)], 'posicao': (303, 255)}
circulo_green = {'cor': [(0, 155, 0), (0, 255, 0)], 'posicao': (503, 255)}
circulo_blue = {'cor': [(0, 0, 155), (0, 0, 255)], 'posicao': (703, 255)}

circulos = [circulo_yellow, circulo_green, circulo_red, circulo_blue]           # Lista com os circulos

# Texto começar
comecar_text = fontes.render('Comecar', True, (0, 0, 0))
comecar_rect = comecar_text.get_rect()
comecar_rect.left = 350
comecar_rect.top = 80


def sequencia_circulo():

    circulo_random = random.choice(circulos)
    pygame.draw.circle(janela, circulo_random['cor'][1], circulo_random['posicao'], 71, 0)
    pygame.display.update()
    time.sleep(2)

jogando = False

while not jogando:
    for evento in pygame.event.get():
        if evento.type == QUIT:
            quit()
        if evento.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if comecar_rect.collidepoint(mouse):
                jogando = True

    janela.blit(background, (0, 0))
    background.blit(comecar_text, (340, 80))
    pygame.display.update()
    clock.tick(27)

while jogando:
    for evento in pygame.event.get():
        if evento.type == QUIT:
            quit()

    sequencia_circulo()

    janela.blit(background, (0, 0))
    pygame.display.update()
    clock.tick(27)
