from math import inf as infinity
from random import choice
import platform
import time
from os import system
import copy

"""
Algoritmo MINIMAX para o Jogo do Gato e Ratos.
Alunos: Guilherme Lucas | Guilherme Kaio

A IA Joga com os Ratos. O Humano joga com o Gato.
A IA prioriza manter um alto numero de ratos adjacentes uns aos outros,
de maneira que cada um sirva de "escudo" para o outro, limitando a movimentacao do gato.
Ela mantem esta estrategia ate poder comer o gato ou chegar na linha de chegada.
"""

# Representando a variável que identifica cada jogador
# HUMANO = Gato
# COMP = Rato (Agente Inteligente)
# tabuleiro = matriz com os valores em cada posição (eixo x e y)
# indicando o jogador presente nessa posição.
# Começa com os ratos na linha 1, agrupados de tres em tres
# O gato na linha 7
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

#*Variaveis globais, utilizadas na funcao minimax e IA_vez
origem_x_global = 0
origem_y_global = 0
profundidade_global = 0 #Começa em 0 mas a cada jogada, a profundidade incrementa


def avaliacao(estado):
    """
    Funcao para avaliacao heuristica do estado. Normalmente chamada apenas no estado final do jogo
    :param (estado): Eh o estado atual do tabuleiro. Matriz de inteiros
    :return: +1 se COMP vence; -1 se HUMANO vence; 0 se der empate
    """
    if vitoria(estado, COMP):
        placar = +1
    elif vitoria(estado, HUMANO):
        placar = -1
    else:
        placar = 0

    return placar
""" ---------------------------------------------------------- """

def avaliacao_heuristica(estado):
    """
    Funcao de avaliacao heuristica do estado. Conta o numero de ratos adjacentes, fazendo com que a IA opte por jogadas que mantenham os ratos adjacentes uns aos outros.
    :param (estado): Eh o estado atual do tabuleiro. Matriz de inteiros
    :return: o numero de ratos adjacentes (int)
    """
    posicoes = posicoes_ratos(estado)
    adjacentes = []
    for i in range(len(posicoes)):
        for j in range(i+1, len(posicoes)):
            if abs(posicoes[i][0] - posicoes[j][0]) <= 1 and abs(posicoes[i][1] - posicoes[j][1]) <= 1:
                adjacentes.append((posicoes[i], posicoes[j]))
    return len(adjacentes)
""" ---------------------------------------------------------- """

def vitoria(estado, jogador):
    """
    Esta funcao testa se um jogador especifico vence. Possibilidades:
    *Gato (HUMANO) Vence:
    *    "if 1 not in tabuleiro"

    *Rato (COMP) Vence:
    *   "if -1 not in tabuleiro" or
    *   "if 1 in tabuleiro[7][0:7]" (se tem um rato na ultima linha)"
    :param (estado): Eh o estado atual do tabuleiro. Matriz de inteiros
    :param: (jogador): um HUMANO/GATO (-1) ou um COMPUTADOR/RATO (1)
    :return: True se JOGADOR vence ou False se JOGADOR perde
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

def fim_jogo(estado):
    """
    Testa se o fim de jogo foi alcancado de acordo com o estado atual. Utiliza a funcao vitoria()
    :param (estado): Eh o estado atual do tabuleiro. Matriz de inteiros
    :return: será fim de jogo caso ocorra vitória de um dos jogadores.
    """
    return vitoria(estado, HUMANO) or vitoria(estado, COMP)
""" ---------------------------------------------------------- """

#!OBS Certamente esta funcao poderia ser apagada, acredito que ela pode piorar o desempenho
#!      A alternativa seria alterar onde ela esta sendo usada (funcao movimento_valido()) para uma simples verificacao "se estado[x][y] == 0"
#!      No entanto, nao tive tempo de testar com esta alternativa

def celulas_vazias(estado):
    """
    Verifica celular vazias e insere na lista para informar posições
    ainda permitidas para próximas jogadas.
    :param (estado): Eh o estado atual do tabuleiro. Matriz de inteiros
    :return: Lista de celulas vazias
    """
    celulas = []
    for x, row in enumerate(estado):
        for y, cell in enumerate(row):
            if cell == 0: 
                celulas.append([x, y])
    return celulas
""" ---------------------------------------------------------- """

def movimento_valido(jogador, origem_x, origem_y, destino_x, destino_y, estado):
    """
    Testa se o movimento que JOGADOR quer fazer eh valido
    Um movimento é valido se:
    
    *RATO:
        *Nao se move mais de uma casa sem ser sua primeira jogada
        
        *Nao se move nas diagonais sem capturar o gato
        
        *Nao se move para tras ou para os lados
    
    *GATO:
        
        *Nao se move na diagonal
    
    :param (jogador): Espera-se 1 para o COMP e -1 para o HUMANO. Inteiro
    :param (origem_x): DE ONDE (eixo X) o jogador quer fazer o movimento 
    :param (origem_y): DE ONDE (eixo Y) o jogador quer fazer o movimento
    :param (destino_x): PARA ONDE (eixo X) o jogador quer se mover
    :param (destino_y): PARA ONDE (eixo Y) o jogador quer se mover
    :param (estado): Eh o estado atual do tabuleiro. Matriz de inteiros
    :return: True se o movimento for valido e False se o movimento for invalido
    """
    try:
        #*RATO
        if jogador == COMP:
            #Checa se eh a primeira jogada de um rato
            primeira_jogada = False
            if origem_x == 1:
                primeira_jogada = True

            #NAO deixa o rato se mover pra tras
            if destino_x < origem_x:
                return False
            
            #NAO deixa o rato se mover na diagonal SEM capturar o gato
            elif ((destino_x == (origem_x + 1)) and (destino_y == origem_y -1 or destino_y == origem_y + 1)) and estado[destino_x][destino_y] != HUMANO:
                return False
            
            elif (origem_y != destino_y) and estado[destino_x][destino_y] != HUMANO:
                return False
            
            #NAO deixa o rato se mover mais do que uma casa SEM ser sua primeira jogada
            elif primeira_jogada == False and destino_x > origem_x + 1 or destino_y > origem_y + 1:
                return False
            
            #NAO deixa o rato se mover na horizontal
            elif destino_x == origem_x and destino_y != origem_y:
                return False


            #Movimentos validos para a primeira jogada de um rato
            if primeira_jogada == True:
                #Rato quer se mover uma ou duas celulas a frente que esteja vazia
                if (destino_x - origem_x == 2 or destino_x - origem_x == 1) and [destino_x, destino_y] in celulas_vazias(estado):
                    return True
                
                #Rato quer se mover na diagonal para CAPTURAR um gato
                elif (destino_y == origem_y -1 or destino_y == origem_y + 1) and estado[destino_x][destino_y] == HUMANO: #! destino x < 3
                    return True
                else:
                    return False
            
            #Nao eh a primeira jogada de um rato
            else:
                #Rato quer se mover uma celula para frente que esta vazia 
                if destino_x == (origem_x + 1) and [destino_x, destino_y] in celulas_vazias(estado):
                    return True
                
                #Rato captura o gato
                elif (destino_y == origem_y -1 or destino_y == origem_y + 1) and estado[destino_x][destino_y] == HUMANO:
                    return True
                else:
                    
                    return False
        #*GATO
        else:
            #Nao deixa gato se mover na diagonal
            if origem_x != destino_x and origem_y != destino_y:
                return False
            else:
                return True
    except IndexError:
        pass
""" ---------------------------------------------------------- """

def exec_movimento(jogador, origem_x, origem_y, destino_x, destino_y, estado=tabuleiro):
    """
    Executa o movimento no tabuleiro. Identifica o jogador e checa o retorno de movimento_valido(), (True se for valido, False caso contrario)
    Se True, realiza o movimento CORRETAMENTE.
    :param (jogador): O jogador da vez. Inteiro
    :param (origem_x): DE ONDE (eixo X) o jogador esta se movimentando 
    :param (origem_y): DE ONDE (eixo Y) o jogador esta se movimentando 
    :param (destino_x): PARA ONDE (eixo X) o jogador esta se movimentando 
    :param (destino_y): PARA ONDE (eixo Y) o jogador esta se movimentando 
    :param (estado): Eh o estado atual do tabuleiro. Matriz de inteiros
    :return: Estado atual do tabuleiro, apos realizacao de uma execucao de um movimento. Matriz de Inteiros
    """
    #*RATO
    if jogador == COMP:
        #Apos validar o movimento, realiza-o
        if movimento_valido(jogador, origem_x, origem_y, destino_x, destino_y, estado):
            estado[origem_x][origem_y] = 0
            estado[destino_x][destino_y] = COMP
            return
        
    #*GATO
    else:
        #Testa se o movimento eh valido antes de realiza-lo
        if movimento_valido(jogador, origem_x, origem_y, destino_x, destino_y, estado):
            #*Movimento Vertical
            if destino_y == origem_y:
                #Verifica se o movimento eh frontal ou traseiro
                if origem_x > destino_x:
                    flag_frente = True
                else:
                    flag_frente = False

                #*FRONTAL
                if flag_frente == True:
                    #Percorre o caminho a ser feito pelo gato
                    for i in range(origem_x, destino_x, -1):
                        if estado[i][destino_y] == 1:   #*Existe um rato no caminho, substituir o PRIMEIRO rato encontrado pelo gato
                            estado[i][destino_y] = -1
                            estado[origem_x][origem_y] = 0
                            return
                        flag_frente = False

                #*TRASEIRO
                else:
                    #Percorre o caminho a ser feito pelo gato
                    for i in range(origem_x, destino_x):
                        if estado[i][destino_y] == 1:   #*Existe um rato no caminho, subsituir o PRIMEIRO rato encontrato pelo gato
                            estado[i][destino_y] = -1
                            estado[origem_x][origem_y] = 0
                            return

                #*Nao existe rato no caminho. Simplesmente substituir os valores
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
                        if estado[destino_x][i] == 1:   #*Existe um rato no caminho, subsituir o PRIMEIRO rato encontrato pelo gato
                            estado[destino_x][i] = -1
                            estado[origem_x][origem_y] = 0
                            return
                
                #*Esquerda
                else:
                    #Percorre o caminho a ser feito pelo gato
                    for i in range(origem_y, destino_y, -1):
                        if estado[destino_x][i] == 1:   #*Existe um rato no caminho, subsituir o PRIMEIRO rato encontrato pelo gato
                            estado[destino_x][i] = -1
                            estado[origem_x][origem_y] = 0
                            return
                
                #*Nao existe rato no caminho. Simplesmente substituir os valores
                estado[destino_x][destino_y] = -1
                estado[origem_x][origem_y] = 0
                return

        #*Movimento Errado ou Algo Inesperado
        else:
            return print("movimento invalido ou algo inesperado")
""" ---------------------------------------------------------- """

#! FUNCAO NOVA
def posicoes_ratos(estado):
    """
    Obtem uma lista de tuplas com as posicoes dos ratos presentes no tabuleiro
    :param (estado): Eh o estado atual do tabuleiro. Matriz de inteiros
    :return: Lista de tuplas com as posicoes dos ratos presentes em estado
    """
    posicoes = []
    for i in range(len(estado)):
        for j in range(len(estado[i])):
            if estado[i][j] == 1:
                posicoes.append((i, j))
    return posicoes
""" ---------------------------------------------------------- """

#! FUNCAO NOVA
def encontra_gato(estado):
    """
    Obtem a posicao atual do gato
    :param (estado): Eh o estado atual do tabuleiro. Matriz de inteiros
    :return: Tupla de inteiros representando a posicao do gato no estado. Eixo X e Y respectivamente. Ou False caso o gato tenha sido capturado
    """
    for i, linha in enumerate(estado):
        if HUMANO in linha:
            j = linha.index(HUMANO)
            return i, j
    return False
""" ---------------------------------------------------------- """

#! FUNCAO NOVA -- Possivel Heuristica para ambos jogadores
def numero_ratos(estado):
    """
    Obtem o numero de ratos presentes no tabuleiro
    :param (estado): Eh o estado atual do tabuleiro. Matriz de inteiros
    :return: Numero de ratos em estado. Inteiro
    """
    numero_ratos = 0
    for linha in estado:
        for elemento in linha:
            if elemento == COMP:
                numero_ratos += 1
    return numero_ratos
""" ---------------------------------------------------------- """

#! FUNCAO NAO UTILIZADA
#!      Decidi deixa-la aqui pois mesmo apos a entrega do trabalho pretendo continuar desenvolvendo.
#!      Seria utilizada no MINIMAX
def desfaz_movimento(jogador, origem_x, origem_y, destino_x, destino_y, estado_temp):
    """
    Desfaz um movimento, subsituindo os valores de acordo com jogador
    :param (jogador): O jogador que fez o movimento. Inteiro
    :param (origem_x): DE ONDE (eixo X) o jogador se moveu 
    :param (origem_y): DE ONDE (eixo Y) o jogador se moveu 
    :param (destino_x): PARA ONDE (eixo X) o jogador se moveu 
    :param (destino_y): PARA ONDE (eixo Y) o jogador se moveu 
    :param (estado_temp): Eh o estado atual do tabuleiro. Matriz de inteiros
    """
    estado_temp[origem_x][origem_y] = 0
    estado_temp[destino_x][destino_y] = 0
    if jogador == COMP:
        estado_temp[origem_x][origem_y] = COMP
    else:
        estado_temp[origem_x][origem_y] = HUMANO
""" ---------------------------------------------------------- """

#! FUNCAO NOVA
def jogadas_possiveis(jogador, origem_x, origem_y, estado):
    """
    Recebe um jogador, sua origem e o estado do tabuleiro e retorna uma lista de tuplas com as possiveis jogadas partindo desta origem
    :param (jogador): O jogador da vez. Inteiro, 1 ou -1
    :param (origem_x): DE ONDE (eixo X) o jogador quer/pode se mover
    :param (origem_y): DE ONDE (eixo Y) o jogador quer/pode se mover
    :param (estado): Eh o estado atual do tabuleiro. Matriz de inteiros
    :return: Lista de tuplas com as possiveis jogadas de jogador. As jogadas sao representadas por um destino x e y
    """

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
    
    possiveis_jogadas =  list(set(aux_lista))   #Remove elementos iguais da lista, deixando apenas unicos

    return possiveis_jogadas
""" ---------------------------------------------------------- """

#! OBS:
#!      Apesar de termos uma ideia bem clara do que queriamos fazer (linhas 12 a 15)
#!      e tambem termos desenvolvido duas heuristicas que certamente fariam tal estrategia funcionar
#!      nossa maior dificuldade foi saber como e onde chamar as funcoes de avaliacao heuristica (numero_de_ratos() e avaliacao_heuristica())
#!      ou seja, sua manipulacao dentro do MINIMAX
#!
#!      Acredito que se conseguissemos fazer com que as linhas 482 a 492 estivessem dentro do for logo abaixo
#!      a IA faria movimentos muito mais inteligentes. Apesar de identificar esta falha, nao conseguimos conserta-la a tempo
def minimax(estado_temp, profundidade, jogador):
    """
    Função da IA que escolhe o melhor movimento
    :param (estado): estado atual do tabuleiro. Matriz de inteiros
    :param (profundidade): Profundidade atual da "arvore". Incrementa a cada jogada feita em IA_vez() e Humano_vez()
    :param (jogador): Um HUMANO (-1) ou um Computador (1). Inteiro
    :return: uma lista com [melhor linha, melhor coluna, melhor placar]
    """

    #Variaveis globais
    global origem_x_global
    global origem_y_global
    global profundidade_global
    profundidade = profundidade_global

    if jogador == COMP:
        melhor = [-1, -1, -infinity]
    else:
        melhor = [-1, -1, +infinity]
    
    #Se o fim de jogo foi alcancado, chama a funcao de avaliacao padrao para identificar quem ganhou
    if fim_jogo(estado_temp):
        placar = avaliacao(estado_temp)
        return [-1, -1, placar]
    #Senao, chama funcao de avaliacao heuristica e atribui o valor para aval
    elif not fim_jogo(estado_temp):
        aval = avaliacao_heuristica(estado_temp)

    #"Heuristica" que prioriza a jogada onde o rato come o gato
    if jogador == COMP:
        if not encontra_gato(estado_temp):
            return [origem_x_global, origem_y_global, +infinity]

    #"Heuristica" que prioriza a jogada onde um gato come o ultimo rato
    else:
        if not posicoes_ratos(estado_temp):
            return [origem_x_global, origem_y_global, +infinity]
    
    # Obtem um rato
    if jogador == 1:
        for rato in posicoes_ratos(estado_temp):
            origem_x = rato[0]
            origem_y = rato[1]
            break  #! OBS: MANTER O BREAK RESULTA EM RATOS FAZENDO JOGADAS BEM MELHORES (de acordo com a heuristica). MAS PODEM DEMORAR UM POUCO PARA CAPTURAREM O GATO

    # Obtem o gato
    else:
        origem_x = encontra_gato(estado_temp)[0]
        origem_y = encontra_gato(estado_temp)[1]

    try:
        #Obtem todas as jogadas possiveis para jogador
        for jogadas in jogadas_possiveis(jogador, origem_x, origem_y, estado_temp):
            #Pegamos uma destas jogadas a cada iteracao
            destino_x = jogadas[0]
            destino_y = jogadas[1]
            
            exec_movimento(jogador, origem_x, origem_y, destino_x, destino_y, estado_temp)

            placar = minimax(estado_temp, profundidade+1, -jogador)

            #Atualiza os valores de placar apos as recursoes
            placar[0] = destino_x
            placar[1] = destino_y
            placar[2] = aval

            #Obtem valores das jogadas para MAX e MIN
            if jogador == COMP:
                if placar[2] > melhor[2]:
                    melhor = placar       #MAX
            else:
                if placar[2] < melhor[2]:
                    melhor = placar   #MIN
            
    except TypeError:
        pass
    
    #Obtemos qual foi a melhor jogada atraves das variaveis globais. Sera utilizada em IA_vez()
    origem_x_global = origem_x
    origem_y_global = origem_y
    return melhor
""" ---------------------------------------------------------- """

def limpa_console():
    """
    Limpa o console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')
""" ---------------------------------------------------------- """

# Define uma função chamada exibe_tabuleiro que recebe um argumento com um valor padrão de 'tabuleiro'
def exibe_tabuleiro(estado=tabuleiro):
    """
    Imprime o tabuleiro no console
    :param:(estado): estado atual do tabuleiro. Matriz de inteiros.
    """
    # Imprime três espaços em branco sem quebra de linha
    print('   ', end='')
    
    # Inicia um loop for que itera sobre o número de colunas do tabuleiro
    for i in range(len(estado[0])):
        
        # Imprime o número da coluna formatado como uma string com um espaço em branco antes e depois, sem quebra de linha
        print(' {}  '.format(i), end='')

    # Imprime uma nova linha
    print('\n  ', '---+' * (len(estado[0]) - 1), '---')

    # Inicia um loop for que itera sobre as linhas do tabuleiro e a posição (índice) de cada linha
    for i, row in enumerate(estado):

        # Imprime o número da linha formatado como uma string com um espaço em branco e uma barra vertical "|", sem quebra de linha
        print('{} |'.format(i), end='')

        # Inicia um loop for que itera sobre as células da linha atual
        for cell in row:

            # Se a célula atual contém +1, imprime o valor de COMP formatado como uma string dentro de barras verticais "|", sem quebra de linha
            if cell == +1:
                print(' {} |'.format(COMP), end='')

            # Se a célula atual contém -1, imprime o valor de HUMANO formatado como uma string dentro de barras verticais "|", sem quebra de linha
            elif cell == -1:
                print(' {} |'.format(HUMANO), end='')

            # Caso contrário, imprime três espaços em branco dentro de barras verticais "|", sem quebra de linha
            else:
                print('   |', end='')

        # Imprime uma nova linha com uma linha pontilhada que se estende até o final da linha
        print('\n  ', '---+' * (len(estado[0]) - 1), '---')
""" ---------------------------------------------------------- """


def IA_vez():
    """
    Chama a funcao minimax para escolher a melhor jogada. Incrementa a profundidade sempre que eh cahmada
    """

    global profundidade_global
    profundidade_global += 1

    #Cria uma copia do estado atual para passar para o minimax
    estado_temp = copy.deepcopy(tabuleiro)

    print('Vez do Computador (RATO)') 
    exibe_tabuleiro(tabuleiro)
    
    #Chama o minimax
    move = minimax(estado_temp, profundidade_global, COMP)
    destino_x, destino_y = move[0], move[1]
    
    #Executa melhor movimento obtido no minimax
    exec_movimento(COMP, origem_x_global, origem_y_global, destino_x, destino_y, tabuleiro) #!

    return
""" ---------------------------------------------------------- """

def HUMANO_vez():
    """
    O HUMANO joga escolhendo um movimento válido. Repete ate que escolha um movimento valido
    """

    print('Vez do HUMANO (GATO)')
    exibe_tabuleiro(tabuleiro)
    tenta_movimento = False
    while(tenta_movimento == False):
        origem_x = int(input('DE ONDE no eixo X voce quer mover?   '))
        origem_y = int(input('DE ONDE no eixo Y voce quer mover?   '))
        destino_x = int(input('PARA ONDE no eixo X voce quer se mover?   '))
        destino_y = int(input('PARA ONDE no eixo Y voce quer se mover?   '))

        tenta_movimento = movimento_valido(HUMANO, origem_x, origem_y, destino_x, destino_y, tabuleiro)

        if tenta_movimento == False:
            print('Movimento Invalido, Tente Novamente:')
        else:
            exec_movimento(HUMANO, origem_x, origem_y, destino_x, destino_y)

""" ---------------------------------------------------------- """

def main():
    """
    Funcao Principal que chama todas funcoes
    """

    # Laço principal do jogo
    while not fim_jogo(tabuleiro):
        HUMANO_vez()
        IA_vez()

    # Mensagem de Final de jogo
    if vitoria(tabuleiro, HUMANO):
        print('Vez do HUMANO (GATO)')
        exibe_tabuleiro(tabuleiro)
        print('Você Venceu!')
    elif vitoria(tabuleiro, COMP):
        print('Vez do COMPUTADOR (RATO)')
        exibe_tabuleiro(tabuleiro)
        print('Você Perdeu!')
    else:
        exibe_tabuleiro(tabuleiro)
        print('Empate (ou erro)!')

    exit()
""" ---------------------------------------------------------- """

if __name__ == '__main__':
    main()