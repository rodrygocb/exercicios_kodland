import pygame
import random

# Inicializa o pygame
pygame.init()

# Define o tamanho da janela e cria a tela do jogo
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo Simples com PyGame")

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

# Variáveis do Jogo
tamanho_jogador = 50
pos_jogador = [LARGURA // 2, ALTURA - 2 * tamanho_jogador]
tamanho_inimigo = 50
pos_inimigo = [random.randint(0, LARGURA - tamanho_inimigo), 0]
lista_inimigos = [pos_inimigo]

VELOCIDADE = 10
relogio = pygame.time.Clock()

jogo_terminado = False
pontuacao = 0

# Definir funções para a mecânica do jogo
def soltar_inimigos(lista_inimigos):
    delay = random.random()
    if len(lista_inimigos) < 10 and delay < 0.1:
        x_pos = random.randint(0, LARGURA - tamanho_inimigo)
        y_pos = 0
        lista_inimigos.append([x_pos, y_pos])

def desenhar_inimigos(lista_inimigos):
    for pos_inimigo in lista_inimigos:
        pygame.draw.rect(tela, VERMELHO, (pos_inimigo[0], pos_inimigo[1], tamanho_inimigo, tamanho_inimigo))

def atualizar_posicao_inimigos(lista_inimigos, pontuacao):
    for idx, pos_inimigo in enumerate(lista_inimigos):
        if pos_inimigo[1] >= 0 and pos_inimigo[1] < ALTURA:
            pos_inimigo[1] += VELOCIDADE
        else:
            lista_inimigos.pop(idx)
            pontuacao += 1
    return pontuacao

def detectar_colisao(pos_jogador, pos_inimigo):
    j_x, j_y = pos_jogador
    i_x, i_y = pos_inimigo

    if (i_x >= j_x and i_x < (j_x + tamanho_jogador)) or (j_x >= i_x and j_x < (i_x + tamanho_inimigo)):
        if (i_y >= j_y and i_y < (j_y + tamanho_jogador)) or (j_y >= i_y and j_y < (i_y + tamanho_inimigo)):
            return True
    return False

def verificar_colisoes(lista_inimigos, pos_jogador):
    for pos_inimigo in lista_inimigos:
        if detectar_colisao(pos_jogador, pos_inimigo):
            return True
    return False

def movimento_jogador(teclas, pos_jogador):
    if teclas[pygame.K_LEFT] and pos_jogador[0] > 0:
        pos_jogador[0] -= 10
    if teclas[pygame.K_RIGHT] and pos_jogador[0] < LARGURA - tamanho_jogador:
        pos_jogador[0] += 10

# Loop principal do jogo
while not jogo_terminado:
    tela.fill(BRANCO)

    # Captura os eventos do jogo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo_terminado = True

    teclas = pygame.key.get_pressed()
    movimento_jogador(teclas, pos_jogador)

    soltar_inimigos(lista_inimigos)
    pontuacao = atualizar_posicao_inimigos(lista_inimigos, pontuacao)

    if verificar_colisoes(lista_inimigos, pos_jogador):
        jogo_terminado = True

    desenhar_inimigos(lista_inimigos)

    # Desenhar o jogador
    pygame.draw.rect(tela, AZUL, (pos_jogador[0], pos_jogador[1], tamanho_jogador, tamanho_jogador))

    # Atualizar a tela
    pygame.display.update()

    relogio.tick(30)

pygame.quit()
