import random, pygame, time
from pygame.locals import *
from tkinter import *

pygame.init()
clock = pygame.time.Clock()
fonte_opcao = pygame.font.SysFont('Arial', 40)                  # Fonte para as opções
fonte_status = pygame.font.SysFont('Calibri', 15)               # Fonte para a barra de status

janela_p = pygame.display.set_mode((500, 530), 0, 32)           # Janela
pygame.display.set_caption("Gênius")                            # Titulo da janela
icone_img = pygame.image.load('logo.png')                       # Imagem do icone do jogo
pygame.display.set_icon(icone_img)
barra_status = pygame.Surface((janela_p.get_width(), 30))       # Barra de status
barra_status.fill((60, 30, 190))                                # Cor da barra de status

background = pygame.image.load('Fundo.png')                     # Imagem de fundo

# Cores
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)
AZUL = (50, 190, 255)
BRANCO = (255, 255, 255)

# Sons
sons = {'som_do': 'som/do.wav', 'som_re': 'som/re.wav', 'som_mi': 'som/mi.wav', 'som_fa': 'som/fa.wav',
        'perdeu': 'som/perdeu_jogo.wav', 'clique': 'som/clique.wav'}

# Poligonos que detectam a escolha com o clique do mouse
cor_verde = pygame.draw.polygon(janela_p, VERDE, ((81, 317), (230, 317), (230, 159)))
cor_amarelo = pygame.draw.polygon(janela_p, AMARELO, ((409, 315), (263, 315), (263, 168)))
cor_vermelha = pygame.draw.polygon(janela_p, VERMELHO, ((80, 345), (230, 346), (230, 495)))
cor_azul = pygame.draw.polygon(janela_p, AZUL, ((411, 345), (265, 347), (263, 495)))

# Textos
comecar_text = fonte_opcao.render('Começar', True, (0, 0, 0))   # Texto do botao começar
texto = ' '

pontos = 0                                                      # Pontuação
cores_sequencia = []                                            # Sequencia de cores que vao piscar
jogando = False

ranking_jogo = {'pontos': '', 'nome': ''}                       # Armazena quem esta no ranking
nome_jogador = ''                                               # Nome do jogador


# Ranking
def Ranking(modo):
    if modo == 'escrever':
        ranking_file = open('ranking.txt', 'w')
        ranking_file.write('p{}\nn{}'.format(str(pontos), nome_jogador))
        ranking_file.close()
    elif modo == 'ler':
        ranking_file = open('ranking.txt', 'r')
        ranking = ranking_file.readlines()
        for linha in ranking:
            if linha.startswith('p'):
                ranking_jogo['pontos'] = linha[1:]
            elif linha.startswith('n'):
                ranking_jogo['nome'] = linha[1:]
            else:
                pass
        ranking_file.close()
    else:
        pass


# Escolhe uma cor para piscar aleatorimanete
def escolherCorAleatoria():
    luz_verde = {'cor': VERDE, 'posicao': ((81, 317), (230, 317), (230, 169)), 'som': sons['som_do']}
    luz_amarela = {'cor': AMARELO, 'posicao': ((409, 315), (263, 315), (263, 168)), 'som': sons['som_fa']}
    luz_azul = {'cor': AZUL, 'posicao': ((411, 345), (264, 346), (263, 495)), 'som': sons['som_mi']}
    luz_vermelha = {'cor': VERMELHO, 'posicao': ((80, 345), (230, 346), (230, 495)), 'som': sons['som_re']}

    cores = [luz_verde, luz_amarela, luz_vermelha, luz_azul]
    return random.choice(cores)


# Pisca as cores que estao na sequencia
def piscarCores(lista_cores):
    for cor in lista_cores:
        tocaSom(cor['som'])
        pygame.draw.polygon(janela_p, cor['cor'], cor['posicao'])
        pygame.display.update()
        time.sleep(0.3)                                         # Tempo para mostrar a proxima cor

        janela_p.blit(background, (0, 30))
        pygame.display.update()
        time.sleep(0.3)                                         # Tempo que a cor fica apagada


# Aguarda a resposta do jogador e retorna a resposta
def recolheResposta(quantidade_cores):
    palpite_usuario = []

    while 1 <= quantidade_cores:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                quit()
            if evento.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if cor_verde.collidepoint(mouse):
                    tocaSom(sons['som_do'])
                    palpite_usuario.append(VERDE)
                    quantidade_cores -= 1
                elif cor_amarelo.collidepoint(mouse):
                    tocaSom(sons['som_fa'])
                    palpite_usuario.append(AMARELO)
                    quantidade_cores -= 1
                elif cor_vermelha.collidepoint(mouse):
                    tocaSom(sons['som_re'])
                    palpite_usuario.append(VERMELHO)
                    quantidade_cores -= 1
                elif cor_azul.collidepoint(mouse):
                    tocaSom(sons['som_mi'])
                    palpite_usuario.append(AZUL)
                    quantidade_cores -= 1
                else:
                    tocaSom(sons['clique'])
                    mostrarStatus(pontos, 'Clicou fora', ranking_jogo)
    return palpite_usuario


# Confere a resposta do jogador com as cores da sequencia
def confereResposta(jogador_resp, lista_seq):
    lista_cores_seq = []
    for cor in lista_seq:
        lista_cores_seq.append(cor['cor'])

    if jogador_resp == lista_cores_seq:
        return True
    else:
        return False


# Muda status
def mostrarStatus(pontos, texto, rank_dados):
    barra_status.fill((60, 30, 190))

    pontuacao = fonte_status.render('Pontos: ' + str(pontos), True, (BRANCO))
    status_txt = fonte_status.render(texto, True, (255, 255, 255))  # Texto para apresentar na barra de status
    rank = fonte_status.render('Ranking: ' + rank_dados['nome'] + ' - ' + rank_dados['pontos'][0:-1], False, (BRANCO))

    barra_status.blit(pontuacao, (10, 6))
    barra_status.blit(status_txt, (120, 6))
    barra_status.blit(rank, (310, 6))

    janela_p.blit(barra_status, (0, 0))
    pygame.display.update()


# Função para jogar novamente
def jogarNovamente():
    jogar_novamente = fonte_opcao.render('Jogar Novamente', True, (0, 0, 0))  # Texto do botao jogar novamete

    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                quit()
            if evento.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if jogar_novamente_btn.collidepoint(mouse):
                    janela_p.blit(background, (0, 30))
                    pygame.display.update()
                    return True
                else:
                    return False

        janela_p.blit(background, (0, 30))
        jogar_novamente_btn = pygame.draw.rect(janela_p, (70, 200, 230), (110, 60, 270, 50))  # Desenha botao
        janela_p.blit(jogar_novamente, (115, 60))               # Desenha texto no botao
        pygame.display.update()
        clock.tick(27)


# Toca os son
def tocaSom(tipo_som):
    pygame.mixer.music.load(tipo_som)
    pygame.mixer.music.play()


def JanelaRank(pontos):

    def salvarNome():
        global nome_jogador

        if nome_usuario.get() == '':
            pass
        else:
            nome_jogador = nome_usuario.get()
            janela.destroy()

    janela = Tk()
    janela.title("Ranking")

    janela1 = Frame()
    janela2 = Frame()
    janela3 = Frame()
    janela4 = Frame()

    janela1['pady'] = 10
    janela1.pack()

    janela2['padx'] = 20
    janela2.pack()

    janela3['pady'] = 20
    janela3.pack()

    janela4['pady'] = 20
    janela4.pack()

    titulo = Label(janela1, text="Novo Ranking", font=("Arial", "10", "bold"))
    titulo.pack()

    nome_label = Label(janela2, text="Nome", font=("Verdana", "16"))
    nome_label.pack(side=LEFT)
    nome_usuario = Entry(janela2, width=20, font=("Arial", "12"))
    nome_usuario.pack(side=LEFT)

    pontos_label = Label(janela3, text="Pontos", font=("Verdana", "16"))
    pontos_label.pack(side=LEFT)
    pontos_jogador = Label(janela3, text=pontos, width=20, font=("Arial", "12"))
    pontos_jogador.pack(side=LEFT)

    botao = Button(janela4, text="Salvar", width=12, font=("Calibri", "10"), command=salvarNome)
    botao.pack()

    janela.mainloop()


while not jogando:
    for evento in pygame.event.get():
        if evento.type == QUIT:
            quit()
        if evento.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if comecar_btn.collidepoint(mouse):
                jogando = True

    janela_p.blit(background, (0, 30))
    janela_p.blit(barra_status, (0, 0))
    comecar_btn = pygame.draw.rect(janela_p, (70, 200, 230), (175, 60, 150, 50))  # Desenha botao
    janela_p.blit(comecar_text, (183, 60))                      # Desenha texto no botao
    pygame.display.update()
    clock.tick(27)

janela_p.blit(background, (0, 30))
pygame.display.update()
Ranking('ler')

while jogando:
    mostrarStatus(pontos, 'Decore a sequência de cores', ranking_jogo)
    time.sleep(1)                                               # Tempo para começar a proxima sequencia

    for evento in pygame.event.get():
        if evento.type == QUIT:
            quit()

    cores_sequencia.append(escolherCorAleatoria())              # Escolhe uma cor e adiciona a lista de sequencia
    piscarCores(cores_sequencia)                                # Pisca as cores que estao na sequencia

    mostrarStatus(pontos, 'Repita a sequência de cores', ranking_jogo)
    resposta_jogador = recolheResposta(len(cores_sequencia))    # Aguarda a resposta do jogador

    if confereResposta(resposta_jogador, cores_sequencia):      # Confere a resposta do jogador
        pontos += 100                                           # Soma pontuação
        continue
    else:
        mostrarStatus(pontos, 'Errou a sequencia', ranking_jogo)
        tocaSom(sons['perdeu'])

        if pontos > int(ranking_jogo['pontos']):                # Verifica se o jogador ultrapassou o ranking
            JanelaRank(str(pontos))
            Ranking('escrever')                                 # Falta pegar o nome

        jogando = jogarNovamente()                              # Pergunta se quer jogar novamente

        if jogando:
            Ranking('ler')
            pontos = 0                                          # Zera pontuação
            cores_sequencia = []                                # Zera a sequencia
            continue
        else:
            quit()

    pygame.display.update()
    clock.tick(27)
