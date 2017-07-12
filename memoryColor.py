import random
import time
import pygame
from pygame.locals import *

pygame.init()  # Inicia Pygame
clock = pygame.time.Clock()  # clock do jogo
fontes = pygame.font.SysFont('Arial', 40)

janela = pygame.display.set_mode((800, 400), 0, 32)  # Janela
pygame.display.set_caption("memoryColor")

background = pygame.image.load('Fundo.png').convert()  # Fundo

# Cores
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Circulos
circulo_red = {'cor': VERMELHO, 'posicao': (103, 255)}
circulo_yellow = {'cor': AMARELO, 'posicao': (303, 255)}
circulo_green = {'cor': VERDE, 'posicao': (503, 255)}
circulo_blue = {'cor': AZUL, 'posicao': (703, 255)}

circulos = [circulo_yellow, circulo_green, circulo_red, circulo_blue]  # Lista com os circulos

# Circulos que detectam a escolha
circulo_detecta_red = pygame.draw.circle(background, (155, 0, 0), (103, 255), 71, 0)
circulo_detecta_yeloow = pygame.draw.circle(background, (155, 155, 0), (303, 255), 71, 0)
circulo_detecta_green = pygame.draw.circle(background, (0, 155, 0), (503, 255), 71, 0)
circulo_detecta_blue = pygame.draw.circle(background, (0, 0, 155), (703, 255), 71, 0)

# Texto começar
comecar_text = fontes.render('Comecar', True, (0, 0, 0))
comecar_rect = comecar_text.get_rect()
comecar_rect.left = 350
comecar_rect.top = 80


def sequencia_circulo(seq_num):
    cores_piscadas = []  # Variavel para armazenar as cores que piscaram

    while 1 <= seq_num:
        circulo_random = random.choice(circulos)  # Escolhe a cor para piscar aleatoriamnete
        print(circulo_random['cor'])
        cores_piscadas.append(circulo_random['cor'])  # Adiciona a cor que piscou à variavel cores_piscadas
        pygame.draw.circle(janela, circulo_random['cor'], circulo_random['posicao'], 71, 0)  # Pisca a cor
        pygame.display.update()
        time.sleep(2)  # Tempo que a cor fica acesa

        seq_num -= 1
        janela.blit(background, (0, 0))  # Limpa a tela
        pygame.display.update()
        time.sleep(0.5)  # Tempo que a cor fica apagada

    return cores_piscadas


def recolhe_resposta(seq_num):

    while 1 <= seq_num:

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if circulo_detecta_red.collidepoint(mouse):
                    print("Vermelho")
                    seq_num -= 1
                elif circulo_detecta_yeloow.collidepoint(mouse):
                    print("Amarelo")
                    seq_num -= 1
                elif circulo_detecta_green.collidepoint(mouse):
                    print("Verde")
                    seq_num -= 1
                elif circulo_detecta_blue.collidepoint(mouse):
                    print("Azul")
                    seq_num -= 1
                else:
                    print("Clicou fora")

jogando = False

# Aguarda o começo do jogo
while not jogando:
    for evento in pygame.event.get():
        if evento.type == QUIT:
            quit()
        if evento.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if comecar_rect.collidepoint(mouse):
                jogando = True

    janela.blit(background, (0, 0))
    janela.blit(comecar_text, (340, 80))
    pygame.display.update()
    clock.tick(27)

janela.blit(background, (0, 0))  # Limpa a tela antes de piscar as cores
pygame.display.update()

# Loop principal do jogo
while jogando:
    pygame.display.set_caption("Decore a sequencia")
    time.sleep(2)  # Tempo para as cores comecarem a piscar

    for event in pygame.event.get():
        if event.type == QUIT:
            quit()

    sequencia_circulo(4)
    pygame.display.set_caption("Refaça a sequencia")
    recolhe_resposta(4)
    quit()

    janela.blit(background, (0, 0))
    pygame.display.update()
    clock.tick(27)