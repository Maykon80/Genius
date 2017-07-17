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

# Sons
fundo_som = pygame.mixer.Sound('som/som_background.wav')
som = {'inicio_jogo': 'som/inicio_jogo.wav', 'perdeu': 'som/perdeu_jogo.wav', 'clique_fora': 'som/clique_fora.wav',
       'subiu_nivel': 'som/subiu_nivel.wav', 'subiu_dificuldade': 'som/subir_dificuldade.wav',
       'clique': 'som/clique.wav'}

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
def recolheResposta(dificuldade):
    resp = []
    while 1 <= dificuldade:

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if circulo_detecta_red.collidepoint(mouse):
                    tocaSom(som['clique'], 0)
                    resp.append(VERMELHO)
                    dificuldade -= 1
                elif circulo_detecta_yeloow.collidepoint(mouse):
                    tocaSom(som['clique'], 0)
                    resp.append(AMARELO)
                    dificuldade -= 1
                elif circulo_detecta_green.collidepoint(mouse):
                    tocaSom(som['clique'], 0)
                    resp.append(VERDE)
                    dificuldade -= 1
                elif circulo_detecta_blue.collidepoint(mouse):
                    tocaSom(som['clique'], 0)
                    resp.append(AZUL)
                    dificuldade -= 1
                else:
                    mudaStatus(pontos, dificuldade, "Clicou fora da cor!")
                    tocaSom(som['clique_fora'], 0)

    return resp


# Função para comparar as cores que piscaram com as que o jogador forneceu
def confereResp(seq_aleatoria, resp_jogador):
    if seq_aleatoria == resp_jogador:
        return True
    else:
        return False


# Função para modificar a barra de status
def mudaStatus(pontos, dificuldade, texto):
    barra_status.fill((60, 30, 190))

    pontuacao = fonte_status.render('Pontuação: ' + str(pontos), True, (255, 255, 255))
    status_dificuldade = fonte_status.render('Dificuldade: ' + str(dificuldade), True, (255, 255, 255))
    status_txt = fonte_status.render(texto, True, (255, 255, 255))  # Texto para apresentar na barra de status

    barra_status.blit(pontuacao, (10, 4))
    barra_status.blit(status_dificuldade, (160, 4))
    barra_status.blit(status_txt, (350, 4))

    janela.blit(barra_status, (0, 0))
    pygame.display.update()


# Reproduz som
def tocaSom(tipo_som, loop):
    pygame.mixer.music.load(tipo_som)
    pygame.mixer.music.play(loop)


# Função para verificar se o jogador quer jogar novamente
def jogarNovamente():
    jogar_novamente_text = fonte_opcao.render('Jogar Novamente?', True, (0, 0, 0))  # Botao jogar Novamente
    jogar_novamente_btn = pygame.draw.rect(janela, (70, 200, 230), (275, 90, 280, 50))

    janela.blit(jogar_novamente_text, (280, 90))
    pygame.display.update()

    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                quit()
            if evento.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if jogar_novamente_btn.collidepoint(mouse):
                    janela.blit(background, (0, 30))
                    pygame.display.update()
                    return True
                else:
                    quit()


pontos = 0
dificuldade = 4
jogando = False


# Textos
comecar_text = fonte_opcao.render('Começar', True, (0, 0, 0))  # Texto do botao começar
texto = ' '  # Textos

tocaSom(som['inicio_jogo'], -1)  # Toca a musica de inicio do jogo enquanto nao começar o jogo

# Aguarda o começo do jogo
while not jogando:
    for evento in pygame.event.get():
        if evento.type == QUIT:
            quit()
        if evento.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if comecar_btn.collidepoint(mouse): # Detecta se clicou no botao
                jogando = True

    mudaStatus(pontos, dificuldade, "Decore as cores que piscarem")
    janela.blit(barra_status, (0, 0))
    janela.blit(background, (0, 30))
    comecar_btn = pygame.draw.rect(janela, (70, 200, 230), (332, 90, 150, 50))   # Desenha botao
    janela.blit(comecar_text, (340, 90))    # Desenha texto no botao
    pygame.display.update()
    clock.tick(27)

pygame.mixer.music.stop()  # Para o som de inicio quando o jogo começar
fundo_som.play(-1)  # Inicia o som de fundo do jogo
janela.blit(background, (0, 30))  # Limpa a tela antes de piscar as cores
pygame.display.update()

# Loop principal do jogo
while jogando:
    mudaStatus(pontos, dificuldade, "Decore as cores que piscarem")  # Muda os status
    time.sleep(2.5)  # Tempo para as cores começarem a piscar

    for event in pygame.event.get():
        if event.type == QUIT:
            quit()

    cores_aleatorias = gerarCoresAleatorias(dificuldade)  # Armazena as cores geradas na variavel

    mudaStatus(pontos, dificuldade, "Repita na ordem certa as cores que acenderam")

    resp_jogador = recolheResposta(dificuldade)  # Recolhe a resposta do jogador

    if confereResp(cores_aleatorias, resp_jogador):  # Verifica se o jogador acertou

        pontos += 100  # Acrescenta mais 100 aos pontos
        tocaSom(som['subiu_nivel'], 0)

        if (pontos % 500 == 0) and (pontos != 0):  # Verifica se pode aumentar a dificuldade
            dificuldade += 1
            tocaSom(som['subiu_dificuldade'], 0)
    else:
        mudaStatus(pontos, dificuldade, "Errou as cores!")
        fundo_som.stop()
        tocaSom(som['perdeu'], 0)
        jogando = jogarNovamente()
        if jogando:
            pontos = 0
            dificuldade = 4
            fundo_som.play(-1)  # Inicia o som de fundo do jogo
            continue

    janela.blit(background, (0, 30))
    pygame.display.update()
    clock.tick(27)
