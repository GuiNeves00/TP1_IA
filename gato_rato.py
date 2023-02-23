#!/usr/bin/env python3
# -*- codificacao: utf-8 -*-
"""
Created on Sun Sep 23 15:33:59 2018
@author: talles medeiros, decsi-ufop
"""

"""
Este código servirá de exemplo para o aprendizado do algoritmo MINIMAX 
na disciplina de Inteligência Artificial - CSI457
Semestre: 2018/2
"""

#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
from os import system
import copy

"""
Algoritmo MINIMAX para o Jogo do Gato e Ratos.
"""

# Representando a variável que identifica cada jogador
# HUMANO = Gato
# COMP = Rato (Agente Inteligente)
# tabuleiro = dicionário (matriz) com os valores em cada posição (x,y)
# indicando o jogador que movimentou nessa posição.
# Começa com os ratos na linha 2 ([1]), agrupados de tres em tres
# O gato na linha 8 ([7])
# 0 -> espaco vazio
HUMANO = -1
COMP = +1
tabuleiro = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, -1, 0, 0, 0, 0],
]
#*Variavies globais, utilizadas na funcao minimax e IA_vez
origem_x_global = 0
origem_y_global = 0
cont_global = -1
"""
Funcao para avaliacao heuristica do estado.
:parametro (estado): o estado atual do tabuleiro
:returna: +1 se COMP vence; -1 se HUMANO vence; 0 se der empate
"""
def avaliacao(estado):
    
    if vitoria(estado, COMP):
        placar = +1
    elif vitoria(estado, HUMANO):
        placar = -1
    else:
        placar = 0

    return placar
""" fim avaliacao (estado)------------------------------------- """

#TODO pode ser possivel ganhar desempenho ao fazer:
#* ter um parametro "jogador", testar a condicao de vitoria apenas pro jogador atual
def vitoria(estado, jogador):
    """
    Esta funcao testa se um jogador especifico vence. Possibilidades:
    *Gato (HUMANO) Vence:
    *    "if 1 not in tabuleiro"
    *    a posicao do gato nao importa
    
    *Rato (COMP) Vence:
    *   "if -1 not in tabuleiro" or
    *   "if 1 in tabuleiro[7][0:7]" (se tem um rato na ultima linha)"
    *   a posicao do gato e dos demais ratos nao importa
    :param. (estado): o estado atual do tabuleiro
    :param. (jogador): um HUMANO ou um Computador
    :return: True se JOGADOR vence ou False se JOGADOR perde
    #! essa logica pode dar problemas (False se jogador perde) ou nao fazer sentido
    #! principalmente em termos de desempenho
    """
    if jogador == HUMANO:
        #*GATO VENCE
        if not any(1 in x for x in estado): #Nenhum rato presente no tabuleiro
            return True
    
        #*RATO VENCE
        elif not any(-1 in y for y in estado) or 1 in estado[7]: #Gato capturado ou rato na linha de chegada
            return False

    if jogador == COMP:
        #*RATO VENCE
        if not any(-1 in y for y in estado) or 1 in estado[7]: #Gato capturado ou rato na linha de chegada
            return True

        #*GATO VENCE
        if not any(1 in x for x in estado): #Nenhum rato presente no tabuleiro
            return False
""" ---------------------------------------------------------- """

"""
Testa fim de jogo para ambos jogadores de acordo com estado atual
return: será fim de jogo caso ocorra vitória de um dos jogadores.
"""
def fim_jogo(estado):
    return vitoria(estado, HUMANO) or vitoria(estado, COMP)
""" ---------------------------------------------------------- """

"""
Verifica celulas vazias e insere na lista para informar posições
ainda permitidas para próximas jogadas.
"""
#TODO checar se essa funcao realmente eh necessaria
def celulas_vazias(estado):
    celulas = []
    for x, row in enumerate(estado):
        for y, cell in enumerate(row):
            if cell == 0: 
                celulas.append([x, y])
    return celulas
""" ---------------------------------------------------------- """

"""
Um movimento é valido se:
:param (jogador): jogador = comp -> movimento valido se nao for na diagonal sem ter um gato nela, ou se nao for mais de uma celula vertical partindo da origem, exceto primeira jogada, onde pode ser duas celulas para frente. Se jogador == HUMANO -> ...
:param (origem_x): de qual linha o jogador esta indo
:param (origem_y): de qual coluna o jogador esta indo
:param (destino_x): para qual linha o jogador quer ir
:param (destino_y): para qual coluna o jogador que ir 
:param (estado): estado atual do tabuleiro
:return: True se movimento de jogador for valido
"""
def movimento_valido(jogador, origem_x, origem_y, destino_x, destino_y, estado):
#TODO avaliar ganho de desempenho ao deixar de usar celulas_vazias() e passar a usar apenas o argumento estado. Se eh que faz sentido usar celulas_vazias()
    try: #! TESTE
        #*RATO
        if jogador == COMP:
            #Checa se eh a primeira jogada de um rato
            primeira_jogada = False
            if origem_x == 1:
                primeira_jogada = True


            #NAO deixa o rato se mover pra tras
            if destino_x < origem_x:
                #print("IF1")
                return False
            #NAO deixa o rato se mover na diagonal SEM capturar o gato
            elif ((destino_x == (origem_x + 1)) and (destino_y == origem_y -1 or destino_y == origem_y + 1)) and estado[destino_x][destino_y] != HUMANO:
                #print("IF2")
                return False
            elif (origem_y != destino_y) and estado[destino_x][destino_y] != HUMANO:
                #print("IF20")
                return False
            #NAO deixa o rato se mover mais do que uma casa SEM ser sua primeira jogada
            elif primeira_jogada == False and destino_x > origem_x + 1 or destino_y > origem_y + 1:
                #print("IF3")
                return False
            #NAO deixa o rato se mover na horizontal
            elif destino_x == origem_x and destino_y != origem_y:
                #print("IF4")
                return False


            #Movimentos validos para a primeira jogada de um rato
            if primeira_jogada == True:
                #Rato quer se mover uma ou duas celulas a frente que esteja vazia
                if (destino_x - origem_x == 2 or destino_x - origem_x == 1) and [destino_x, destino_y] in celulas_vazias(estado):
                    #print("IF5")
                    return True
                #*Rato quer se mover na diagonal para CAPTURAR um gato
                elif (destino_y == origem_y -1 or destino_y == origem_y + 1) and estado[destino_x][destino_y] == HUMANO: #! destino x < 3
                    #print("IF6")
                    return True
                else:
                    #print("IF7")
                    return False
            
            #Nao eh a primeira jogada de um rato
            else:
                #Rato quer se mover uma celula para frente que esta vazia 
                if destino_x == (origem_x + 1) and [destino_x, destino_y] in celulas_vazias(estado):
                    #print("IF8")
                    return True
                #* Rato captura o gato
                elif (destino_y == origem_y -1 or destino_y == origem_y + 1) and estado[destino_x][destino_y] == HUMANO: #! destino x < 3
                    #print("IF9")
                    return True
                else:
                    #print("IF10")
                    return False
        #*GATO
        else:
            if origem_x != destino_x and origem_y != destino_y: #ANTIGO -> if (origem_x and origem_y) != (destino_x and destino_y):
                #print("IF11")
                return False
            else:
                #print("IF12")
                return True
    except IndexError:
        pass
""" ---------------------------------------------------------- """

"""
Executa o movimento no tabuleiro. Identifica o jogador e checa o retorno de movimento_valido(), que eh True se o movimento for valido e False caso contrario.
Se True, realiza o movimento corretamente.
:param (jogador): o jogador da vez
:param (origem_x): de qual linha o jogador esta indo
:param (origem_y): de qual coluna o jogador esta indo
:param (destino_x): para qual linha o jogador esta indo
:param (destino_y): para qual coluna o jogador esta indo
:param (estado): estado atual do tabuleiro
:return: estado atual do tabuleiro, apos realizacao de um execucao de um movimento
"""
def exec_movimento(jogador, origem_x, origem_y, destino_x, destino_y, estado=tabuleiro):

    #*RATO
    if jogador == COMP:
        print("IF2")
        #Apos validar o movimento, realiza-o
        if movimento_valido(jogador, origem_x, origem_y, destino_x, destino_y, estado):
            print("IF3")
            estado[origem_x][origem_y] = 0
            estado[destino_x][destino_y] = COMP
            return
        
    #*GATO
    else:
        print("IF5")
        #Testa se o movimento eh valido antes de realiza-lo
        if movimento_valido(jogador, origem_x, origem_y, destino_x, destino_y, estado):
            print("IF6")

            #*Movimento Vertical
            if destino_y == origem_y:
                print("IF7")

                #Verifica se o movimento eh frontal ou traseiro
                if origem_x > destino_x:
                    flag_frente = True
                else:
                    flag_frente = False

                #*FRONTAL
                if flag_frente == True:
                    #Percorre o caminho a ser feito pelo gato
                    for i in range(origem_x, destino_x, -1):
                        if estado[i][destino_y] == 1:   #*Existe um rato no caminho, substituir o primeiro rato encontrado pelo gato
                            estado[i][destino_y] = -1
                            estado[origem_x][origem_y] = 0
                            return
                        flag_frente = False

                #*TRASEIRO
                else:
                    #Percorre o caminho a ser feito pelo gato
                    for i in range(origem_x, destino_x):
                        if estado[i][destino_y] == 1:   #*Existe um rato no caminho, subsituir o primeiro rato encontrato pelo gato
                            estado[i][destino_y] = -1
                            estado[origem_x][origem_y] = 0
                            return

                #*Nao existe rato no caminho
                estado[destino_x][destino_y] = -1
                estado[origem_x][origem_y] = 0
                return

            #*Movimento Horizontal
            else:
                #Verifica se o movimento eh para esquerda ou direita
                if origem_y < destino_y:
                    flag_direita = True
                else:
                    flag_direita = False
                
                #*Direita
                if flag_direita == True:
                    #Percorre o caminho a ser feito pelo gato
                    for i in range(origem_y, destino_y): 
                        if estado[destino_x][i] == 1:   #*Existe um rato no caminho, subsituir o primeiro rato encontrato pelo gato
                            estado[destino_x][i] = -1
                            estado[origem_x][origem_y] = 0
                            return
                
                #*Esquerda
                else:
                    #Percorre o caminho a ser feito pelo gato
                    for i in range(origem_y, destino_y, -1):
                        if estado[destino_x][i] == 1:   #*Existe um rato no caminho, subsituir o primeiro rato encontrato pelo gato
                            estado[destino_x][i] = -1
                            estado[origem_x][origem_y] = 0
                            return
                
                #*Nao existe rato no caminho
                estado[destino_x][destino_y] = -1
                estado[origem_x][origem_y] = 0
                return

        #*Movimento Errado ou Algo Inesperado
        else:
            print("IF13")
            return print("movimento invalido ou algo inesperado")
""" ---------------------------------------------------------- """
"""retorna uma lista de tuplas com as posicoes dos ratos"""
#! FUNCAO NOVA
def posicoes_ratos(estado):
    posicoes = []
    for i in range(len(estado)):
        for j in range(len(estado[i])):
            if estado[i][j] == 1:
                posicoes.append((i, j))
    return posicoes
""" ---------------------------------------------------------- """
"""retorna a posicao atual do gato"""
#! FUNCAO NOVA
def encontra_gato(estado):
    for i, linha in enumerate(estado):
        if HUMANO in linha:
            j = linha.index(HUMANO)
            return i, j #! POSSIVEL PROBLEMA (TUPLA IMUTAVEL)
    return False
""" ---------------------------------------------------------- """
"""retorna o numero de ratos presentes em estado"""
#! FUNCAO NOVA
def numero_ratos(estado):
    numero_ratos = 0
    for linha in estado:
        for elemento in linha:
            if elemento == COMP:
                numero_ratos += 1
    return numero_ratos
""" ---------------------------------------------------------- """
#! FUNCAO NOVA
#TODO checar se realmente eh necessario, e onde (SEGUINDO IDEIA...)
def desfaz_movimento(jogador, origem_x, origem_y, destino_x, destino_y, estado_temp):
    estado_temp[origem_x][origem_y] = 0
    estado_temp[destino_x][destino_y] = 0
    
    if jogador == COMP:
        estado_temp[origem_x][origem_y] = COMP
    else:
        estado_temp[origem_x][origem_y] = HUMANO
""" ---------------------------------------------------------- """
#! FUNCAO NOVA
"""recebe um jogador, sua origem e o estado do tabuleiro e retorna uma lista de tuplas com as possiveis jogadas partindo desta origem"""
def jogadas_possiveis(jogador, origem_x, origem_y, estado):
    possible_plays = []
    if jogador == COMP:
        #Rato se move uma casa pra frente
        if movimento_valido(COMP, origem_x, origem_y, origem_x+1, origem_y, estado):
            possible_plays.append((origem_x+1, origem_y))
        #Rato se move duas casas pra frente
        if movimento_valido(COMP, origem_x, origem_y, origem_x+2, origem_y, estado):
            possible_plays.append((origem_x+2, origem_y))
        #Rato come o gato na diagonal direita
        if movimento_valido(COMP, origem_x, origem_y, origem_x+1, origem_y+1, estado):
            possible_plays.append((origem_x+1, origem_y+1))
        #Rato come o gato na diagonal esquerda
        if movimento_valido(COMP, origem_x, origem_y, origem_x+1, origem_y-1, estado):
            possible_plays.append((origem_x+1, origem_y-1))
    
    elif jogador == HUMANO:
        for i in range(0, 8):
            #Gato se move na vertical para frente
            if movimento_valido(HUMANO, origem_x, origem_y, origem_x-i, origem_y, estado):
                if origem_x-i >= 0 and origem_x-i <= 7:
                    possible_plays.append((origem_x-i, origem_y))
            #Gato se move na vertical para tras
            if movimento_valido(HUMANO, origem_x, origem_y, origem_x+i, origem_y, estado):
                if origem_x+i >= 0 and origem_x+i <= 7:
                    possible_plays.append((origem_x+i, origem_y))
            #Gato se move na horizontal para a direita
            if movimento_valido(HUMANO, origem_x, origem_y, origem_x, origem_y+i, estado):
                if origem_y+i >= 0 and origem_y+i <= 7:
                    possible_plays.append((origem_x, origem_y+i))
            #Gato se move na horizontal para a esquerda
            if movimento_valido(HUMANO, origem_x, origem_y, origem_x, origem_y-i, estado):
                if origem_y-i >= 0 and origem_y-i <= 7:
                    possible_plays.append((origem_x, origem_y-i))
            else:
                continue

    #Remove jogada onde jogador nao se move
    remover = (origem_x, origem_y)
    aux_lista = [tupla for tupla in possible_plays if tupla != remover]

    #Retorna falso se nao existge nenhuma jogada possivel para jogador
    #if not possible_plays:
    #    return False
    
    possiveis_jogadas =  list(set(aux_lista))   #remove elementos iguais da lista, deixando apenas unicos
    return possiveis_jogadas
""" ---------------------------------------------------------- """

"""
Função da IA que escolhe o melhor movimento
:param (estado): estado atual do tabuleiro
:param (profundidade): índice do nó na árvore (0 <= profundidade <= 9),
mas nunca será nove neste caso (veja a função iavez())
:param (jogador): um HUMANO ou um Computador
:return: uma lista com [melhor linha, melhor coluna, melhor placar]
"""
def minimax(estado_temp, profundidade, jogador):
#TODO fazer a funcao jogadas_possiveis, obter uma lista de jogadas possiveis para jogador e iterar sobre cada jogada, ao final o minimax iria retornar qual foi a melhor jogada (recursao)

    if jogador == COMP:
        melhor = [-1, -1, -infinity]
    else:
        melhor = [-1, -1, +infinity]

    if profundidade == 0 or fim_jogo(estado_temp):
        placar = avaliacao(estado_temp)
        return [-1, -1, placar]

    #Recompensa a jogada onde o rato come o gato
    if jogador == COMP:
        if not encontra_gato(estado_temp):
            if placar[2] > melhor[2]:
                return melhor
    #Recompensa a jogada onde um gato come o ultimo rato
    else:
        if not posicoes_ratos(estado_temp):
            if placar[2] > melhor[2]:
                return melhor
    
    #Obtem um rato
    if jogador == 1:
        for rato in posicoes_ratos(estado_temp):
            origem_x = rato[0]
            origem_y = rato[1]
            #break #! remover o break resulta em ratos fazendo melhores jogadas mas demorando para comer o gato
    #Obtem um gato
    else:
        origem_x = encontra_gato(estado_temp)[0]
        origem_y = encontra_gato(estado_temp)[1]

    try:
        for jogadas in jogadas_possiveis(jogador, origem_x, origem_y, estado_temp):

            destino_x = jogadas[0]
            destino_y = jogadas[1]
            
            exec_movimento(jogador, origem_x, origem_y, destino_x, destino_y, estado_temp)
            
            placar = minimax(estado_temp, profundidade-1, -jogador)

            placar[0] = destino_x
            placar[1] = destino_y

            if jogador == COMP:
                if placar[2] > melhor[2]:
                    melhor = placar
            else:
                if placar[2] < melhor[2]:
                    melhor = placar
    except TypeError:
        pass
    
    global origem_x_global
    global origem_y_global
    origem_x_global = origem_x
    origem_y_global = origem_y
    return melhor


    #! obtem um rato
    #! obtem todas as jogadas possiveis para este rato:
    #! for teste in jogadas_possiveis(jogador, origem_x, origem_y, estado_temp)     itera sobre estas jogadas
    #!      destino_x & destino_y = jogadas_possiveis[0][0], [0][1]
    #!      exec_movimento()
    #!      se gato morto ou fim de jogo:
    #!          retorna melhor jogada
    #!      placar = minimax()
    #!      placar[0] & [1] = destinos
    #!      
    #!      ...    

""" ---------------------------------------------------------- """

"""
Limpa o console para SO Windows
"""
def limpa_console():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')
""" ---------------------------------------------------------- """

"""
Imprime o tabuleiro no console
:param. (estado): estado atual do tabuleiro
"""
def exibe_tabuleiro(estado=tabuleiro):
    print('----------------')
    for row in estado:
        print('\n----------------')
        for cell in row:
            if cell == +1:
                print('|', COMP, '|', end='')
            elif cell == -1:
                print('|', HUMANO, '|', end='')
            else:
                print('|', ' ', '|', end='')
    print('\n----------------')
""" ---------------------------------------------------------- """

"""
Chama a função minimax se a profundidade < 9, #! falso pro jogo de gato e rato
ou escolhe uma coordenada aleatória.
:param (comp_escolha): Computador escolhe X ou O
:param (humano_escolha): HUMANO escolhe X ou O
:return:
"""
def IA_vez():
    profundidade = len(celulas_vazias(tabuleiro))   #! possivel alteracao importante a ser feita aq
    if profundidade == 0 or fim_jogo(tabuleiro):
        return

    #cria uma copia do estado atual para passar para o minimax
    estado_temp = copy.deepcopy(tabuleiro)

    #limpa_console()
    print('Vez do Computador (RATO)') 
    exibe_tabuleiro(tabuleiro)

    #TODO entender oque essa condicao signfica. pro jogo da velha, acredito q profundidade == 9 represente a primeira jogada da IA
    #! IMPORTANTE
    #TODO consertar isso -> sempre que chamar IA_vez() vai pegar um dos movimentos abaixo, mas em dado momento do jogo, os movimentos abaixo nao serao mais validos
    #Pega um movimento aleatorio qualquer de inicio
    origem_x = 1
    origem_y = choice([0, 1, 2, 5, 6, 7])
    destino_x = choice([2, 3])
    destino_y = choice([0, 1, 2, 5, 6, 7])
    if profundidade == 32: #! ANTES 32
        #Testa ate achar um movimento valido
        while not movimento_valido(COMP, origem_x, origem_y, destino_x, destino_y, tabuleiro): #!TODO deve dar pra ganhar desemepnho aqui
            origem_x = 1
            origem_y = choice([0, 1, 2, 5, 6, 7])
            destino_x = choice([2, 3])
            destino_y = choice([0, 1, 2, 5, 6, 7])
        print("IA_VEZ")
        exec_movimento(COMP, origem_x, origem_y, destino_x, destino_y, tabuleiro) #!
    else:
        move = minimax(estado_temp, profundidade, COMP)
        destino_x, destino_y = move[0], move[1]
        exec_movimento(COMP, origem_x_global, origem_y_global, destino_x, destino_y, tabuleiro) #!

        return
    time.sleep(1)
""" ---------------------------------------------------------- """

def HUMANO_vez(): #! estado=tabuleiro ?
    """
    O HUMANO joga escolhendo um movimento válido
    :param comp_escolha: Computador escolhe X ou O
    :param humano_escolha: HUMANO escolhe X ou O
    :return:
    """
    profundidade = len(celulas_vazias(tabuleiro))
    if profundidade == 0 or fim_jogo(tabuleiro):
        return

    #limpa_console()
    print('Vez do HUMANO (GATO)')
    exibe_tabuleiro(tabuleiro)
    tenta_movimento = False
    while(tenta_movimento == False):
        origem_x = int(input('Informe DE ONDE no eixo X voce quer mover:   '))
        origem_y = int(input('Informe DE ONDE no eixo Y voce quer mover:   '))
        destino_x = int(input('Informe PARA ONDE no eixo X voce quer se mover:   '))
        destino_y = int(input('Informe PARA ONDE no eixo Y voce quer se mover:   '))

        tenta_movimento = movimento_valido(HUMANO, origem_x, origem_y, destino_x, destino_y, tabuleiro)

        if tenta_movimento == False:
            print('Movimento Invalido, Tente Novamente:')
        else:
            print("...EXECUTANDO MOVIMENTO...")
            exec_movimento(HUMANO, origem_x, origem_y, destino_x, destino_y)
            #exibe_tabuleiro(tabuleiro)
            #quit()

""" ---------------------------------------------------------- """

"""
Funcao Principal que chama todas funcoes
"""
def main():

    #limpa_console()
    humano = HUMANO #GATO
    comp = COMP     #RATO

    # Laço principal do jogo
    while not fim_jogo(tabuleiro):
        HUMANO_vez()
        IA_vez()

    # Mensagem de Final de jogo
    if vitoria(tabuleiro, HUMANO):
        #limpa_console()
        print('Vez do HUMANO (GATO)')
        exibe_tabuleiro(tabuleiro)
        print('Você Venceu!')
    elif vitoria(tabuleiro, COMP):
        #limpa_console()
        print('Vez do COMPUTADOR (RATO)')
        exibe_tabuleiro(tabuleiro)
        print('Você Perdeu!')
    else:
        #limpa_console()
        exibe_tabuleiro(tabuleiro)
        print('Empate (ou erro)!')

    exit()

if __name__ == '__main__':
    #print(len(celulas_vazias(tabuleiro)))
    main()