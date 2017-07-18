import random, pygame, time
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
fonte_opcao = pygame.font.SysFont('Arial', 40)
fonte_status = pygame.font.SysFont('Arial', 20)

janela = pygame.display.set_mode((500, 530), 0, 32)             # Janela
pygame.display.set_caption("Gênius")                            # Titulo da janela
barra_status = pygame.Surface((janela.get_width(), 30))         # Barra de status
barra_status.fill((60, 30, 190))                                # Cor da barra de status

background = pygame.image.load('Fundo.png')

# Detectar colisao
cor_verde = pygame.draw.polygon(janela, (0, 155, 0), ((81, 317), (230, 317), (230, 159)))
cor_amarelo = pygame.draw.polygon(janela, (155, 155, 0), ((409, 315), (263, 315), (263, 168)))
cor_vermelha = pygame.draw.polygon(janela, (155, 0, 0), ((80, 345), (230, 346), (230, 495)))
cor_azul = pygame.draw.polygon(janela, (50, 190, 255), ((411, 345), (265, 347), (263, 495)))


def escolherCorAleatoria():
    luz_verde = {'cor': (0, 255, 0), 'posicao': ((81, 317), (230, 317), (230, 169))}
    luz_amarela = {'cor': (255, 255, 0), 'posicao': ((409, 315), (263, 315), (263, 168))}
    luz_azul = {'cor': (50, 190, 255), 'posicao': ((411, 345), (265, 346), (263, 495))}
    luz_vermelha = {'cor': (255, 0, 0), 'posicao': ((80, 345), (230, 347), (230, 495))}

    cores = [luz_verde, luz_amarela, luz_vermelha, luz_azul]
    return random.choice(cores)


def piscarCores(lista_cores):
    for cor in lista_cores:
        pygame.draw.polygon(janela, cor['cor'], cor['posicao'])
        pygame.display.update()
        time.sleep(1.5)

        janela.blit(background, (0, 30))
        pygame.display.update()
        time.sleep(0.5)


def recolheResposta(quantidade_cores):
    palpite_usuario = []

    while 1 <= quantidade_cores:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                quit()
            if evento.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if cor_verde.collidepoint(mouse):
                    palpite_usuario.append((0, 255, 0))
                    quantidade_cores -= 1
                elif cor_amarelo.collidepoint(mouse):
                    palpite_usuario.append((255, 255, 0))
                    quantidade_cores -= 1
                elif cor_vermelha.collidepoint(mouse):
                    palpite_usuario.append((255, 0, 0))
                    quantidade_cores -= 1
                elif cor_azul.collidepoint(mouse):
                    palpite_usuario.append((50, 190, 255))
                    quantidade_cores -= 1
                else:
                    mostrarStatus(pontos, 'Clicou fora')
    return palpite_usuario


def confereResposta(jogador_resp, lista_seq):
    lista_cores_seq = []
    for cor in lista_seq:
        lista_cores_seq.append(cor['cor'])

    if jogador_resp == lista_cores_seq:
        return True
    else:
        return False


def mostrarStatus(pontos, texto):
    barra_status.fill((60, 30, 190))

    pontuacao = fonte_status.render('Pontuação: ' + str(pontos), True, (255, 255, 255))
    status_txt = fonte_status.render(texto, True, (255, 255, 255))  # Texto para apresentar na barra de status

    barra_status.blit(pontuacao, (10, 4))
    barra_status.blit(status_txt, (150, 4))

    janela.blit(barra_status, (0, 0))
    pygame.display.update()


def jogarNovamente():
    jogar_novamente = fonte_opcao.render('Jogar Novamente', True, (0, 0, 0))

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
                    return False

        janela.blit(background, (0, 30))
        jogar_novamente_btn = pygame.draw.rect(janela, (70, 200, 230), (110, 60, 270, 50))  # Desenha botao
        janela.blit(jogar_novamente, (115, 60))  # Desenha texto no botao
        pygame.display.update()
        clock.tick(27)


# Textos
comecar_text = fonte_opcao.render('Começar', True, (0, 0, 0))  # Texto do botao começar
texto = ' '

pontos = 0
cores_sequencia = []
jogando = False

while not jogando:
    for evento in pygame.event.get():
        if evento.type == QUIT:
            quit()
        if evento.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if comecar_btn.collidepoint(mouse):
                jogando = True

    janela.blit(background, (0, 30))
    janela.blit(barra_status, (0, 0))
    comecar_btn = pygame.draw.rect(janela, (70, 200, 230), (175, 60, 150, 50))  # Desenha botao
    janela.blit(comecar_text, (183, 60))  # Desenha texto no botao
    pygame.display.update()
    clock.tick(27)

janela.blit(background, (0, 30))
pygame.display.update()

while jogando:
    mostrarStatus(pontos, 'Decore a sequência de cores')
    time.sleep(1)

    for evento in pygame.event.get():
        if evento.type == QUIT:
            quit()

    cores_sequencia.append(escolherCorAleatoria())
    piscarCores(cores_sequencia)

    mostrarStatus(pontos, 'Repita a sequência de cores')
    resposta_jogador = recolheResposta(len(cores_sequencia))

    if confereResposta(resposta_jogador, cores_sequencia):
        pontos += 100
        continue
    else:
        mostrarStatus(pontos, 'Errou a sequencia')
        jogando = jogarNovamente()

        if jogando:
            pontos = 0
            cores_sequencia = []
            continue
        else:
            quit()

    pygame.display.update()
    clock.tick(27)
