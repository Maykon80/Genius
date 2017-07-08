import random

import time

"""
    Esse codigo foi feito para fazer a dinamica do jogo sem a parte grafica. A finalidade é pensar nas funções que
    o jogo precisara. As cores apagadas sao representadas por seus nomes em minusculo, e acesa por MAIUSCULO. 
"""

# Lista que faz alusao as cores no jogo
lista = ["vermelho", "amarelo", "verde", "azul"]


# Função para escolher aleatoriamente X(num_seq) posicoes que iram acender e retorna uma lista com esses valores
def sequencia(seq_num):
    lista_gerada = []  # Lista gerada com as posições das cores que acenderam aleatoriamente
    con = 1

    while con <= seq_num:
        rand = random.randint(0, len(lista) - 1)  # Posicao aleatoria da lista
        lista_gerada.append(str(rand))  # Adiciona à lista_gerada o numero da posicao da cor na lista
        lista[rand] = lista[rand].upper()  # Pisca a cor
        print(lista)  # Mostra a cor
        lista[rand] = lista[rand].lower()  # Apaga a cor
        time.sleep(2)  # Aguarda dois segundos
        con += 1

    return lista_gerada


# Função para conferir se a lista_gerada(Cores que piscou) é igual a lista(Cores) que o jogador forneceu
def confere_resp(lista_gerada, resp):
    if lista_gerada == resp:
        return True
    else:
        return False


while True:
    lista_gerada_aleatoriamente = sequencia(4)
    print(lista_gerada_aleatoriamente)  # Da a resposta do jogo

    # Palpite do usuario, a principio aqui o palpite é dado por uma string do numero das posicoes
    resp = list(input('>>> '))

    print(confere_resp(lista_gerada_aleatoriamente, resp))  # Retorna se o jogador acertou
    lista_gerada_aleatoriamente = []  # Zera a lista
