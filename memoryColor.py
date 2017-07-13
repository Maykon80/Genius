import random
import time
import pygame
from pygame.locals import *

pygame.init()  # Inicia Pygame
clock = pygame.time.Clock()  # clock do jogo
fonte_opcao = pygame.font.SysFont('Arial', 40)
fonte_status = pygame.font.SysFont('Arial', 20)

janela = pygame.display.set_mode((800, 400), 0, 32)  # Janela
# Barra de status para mostrar, imagine o que... os status do jogo!
barra_status = pygame.Surface((janela.get_width(), 30))
barra_status.fill((60, 30, 190))  # Cor da barra de status
pygame.display.set_caption("memoryColor")  # Titulo da janela do jogo

background = pygame.image.load('Fundo.png').convert()  # Fundo

# Cores
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Circulos
circulo_red = {'cor': VERMELHO, 'posicao': (103, 285)}
circulo_yellow = {'cor': AMARELO, 'posicao': (303, 285)}
circulo_green = {'cor': VERDE, 'posicao': (503, 285)}
circulo_blue = {'cor': AZUL, 'posicao': (703, 285)}

circulos = [circulo_yellow, circulo_green, circulo_red, circulo_blue]  # Lista com os circulos

# Circulos invisiveis que detectam a escolha do usuario
circulo_detecta_red = pygame.draw.circle(background, (155, 0, 0), (103, 255), 69, 0)
circulo_detecta_yeloow = pygame.draw.circle(background, (155, 155, 0), (303, 255), 69, 0)
circulo_detecta_green = pygame.draw.circle(background, (0, 155, 0), (503, 255), 69, 0)
circulo_detecta_blue = pygame.draw.circle(background, (0, 0, 155), (703, 255), 69, 0)


# Função para piscar aleatoriamente as cores
def gerarCoresAleatorias(dificuldade):
    cores_piscadas = []  # Variavel para armazenar as cores que piscaram

    while 1 <= dificuldade:
        circulo_random = random.choice(circulos)  # Escolhe a cor para piscar aleatoriamnete
        cores_piscadas.append(circulo_random['cor'])  # Adiciona a cor que piscou à variavel cores_piscadas
        print(circulo_random['cor'])
        pygame.draw.circle(janela, circulo_random['cor'], circulo_random['posicao'], 71, 0)  # Pisca a cor
        pygame.display.update()
        time.sleep(1.5)  # Tempo que a cor fica acesa

        dificuldade -= 1
        janela.blit(background, (0, 30))  # Limpa a tela
        pygame.display.update()
        time.sleep(0.5)  # Tempo que a cor fica apagada

    return cores_piscadas


# Função para recolher o palpite do jogador
def recolhe_resposta(dificuldade):
    resp = []
    while 1 <= dificuldade:

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if circulo_detecta_red.collidepoint(mouse):
                    resp.append(VERMELHO)
                    dificuldade -= 1
                elif circulo_detecta_yeloow.collidepoint(mouse):
                    resp.append(AMARELO)
                    dificuldade -= 1
                elif circulo_detecta_green.collidepoint(mouse):
                    resp.append(VERDE)
                    dificuldade -= 1
                elif circulo_detecta_blue.collidepoint(mouse):
                    resp.append(AZUL)
                    dificuldade -= 1
                else:
                    print("Fora!")

    return resp


# Função para comparar as cores que piscaram com as que o jogador forneceu
def confere_resp(seq_aleatoria, resp_jogador):
    if seq_aleatoria == resp_jogador:
        return True
    else:
        return False


# Função para modificar a barra de status
def muda_status(pontos, dificuldade, texto):
    barra_status.fill((60, 30, 190))

    pontuacao = fonte_status.render('Pontuação: ' + str(pontos), True, (255, 255, 255))
    status_dificuldade = fonte_status.render('Dificuldade: ' + str(dificuldade), True, (255, 255, 255))
    status_txt = fonte_status.render(texto, True, (255, 255, 255))  # Texto para apresentar na barra de status

    barra_status.blit(pontuacao, (10, 4))
    barra_status.blit(status_dificuldade, (160, 4))
    barra_status.blit(status_txt, (350, 4))

    janela.blit(barra_status, (0, 0))
    pygame.display.update()


pontos = 0
dificuldade = 4
jogando = False

# Textos
comecar_text = fonte_opcao.render('Começar', True, (0, 0, 0))  # Botao começar
comecar_rect = comecar_text.get_rect()
comecar_rect.left = 350
comecar_rect.top = 80
texto = ' '  # Textos

# Aguarda o começo do jogo
while not jogando:
    for evento in pygame.event.get():
        if evento.type == QUIT:
            quit()
        if evento.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if comecar_rect.collidepoint(mouse):
                jogando = True

    muda_status(pontos, dificuldade, "Decore as cores que piscarem")
    janela.blit(barra_status, (0, 0))
    janela.blit(background, (0, 30))
    janela.blit(comecar_text, (340, 80))
    pygame.display.update()
    clock.tick(27)

janela.blit(background, (0, 30))  # Limpa a tela antes de piscar as cores
pygame.display.update()

# Loop principal do jogo
while jogando:
    muda_status(pontos, dificuldade, "Decore as cores que piscarem")  # Muda os status
    time.sleep(2.5)  # Tempo para as cores começarem a piscar

    for event in pygame.event.get():
        if event.type == QUIT:
            quit()

    cores_aleatorias = gerarCoresAleatorias(dificuldade)  # Armazena as cores geradas na variavel

    muda_status(pontos, dificuldade, "Repita na ordem certa as cores que acenderam")

    resp_jogador = recolhe_resposta(dificuldade)    # Recolhe a resposta do jogador

    if confere_resp(cores_aleatorias, resp_jogador):  # Verifica se o jogador acertou

        pontos += 100  # Acrescenta mais 100 aos pontos

        if (pontos % 500 == 0) and (pontos != 0):   # Verifica se pode aumentar a dificuldade
            dificuldade += 1
    else:
        quit()

    janela.blit(background, (0, 30))
    pygame.display.update()
    clock.tick(27)
