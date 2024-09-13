import pygame
import random
import time  # Importa para usar o time.sleep()

# Inicializa o pygame
pygame.init()

# Define o tamanho da janela e cria a tela do jogo
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo Simples com PyGame")

# Carregar imagens
imagem_jogador = pygame.image.load('imagens/jogador.png')
imagem_inimigo = pygame.image.load('imagens/inimigo.png')

# Redimensionar imagens se necessário
tamanho_jogador = 50
imagem_jogador = pygame.transform.scale(imagem_jogador, (tamanho_jogador, tamanho_jogador))
tamanho_inimigo = 50
imagem_inimigo = pygame.transform.scale(imagem_inimigo, (tamanho_inimigo, tamanho_inimigo))

# Variáveis do Jogo
pos_jogador = [LARGURA // 2, ALTURA - 2 * tamanho_jogador]
pos_inimigo = [random.randint(0, LARGURA - tamanho_inimigo), 0]
lista_inimigos = [pos_inimigo]

VELOCIDADE = 10
relogio = pygame.time.Clock()

jogo_terminado = False
pontuacao = 0
vidas = 3
tempo_pausa = 1  # Tempo de pausa em segundos

# Função para desenhar o texto na tela
def desenhar_texto(texto, fonte, cor, superficie, pos_x, pos_y):
    texto_superficie = fonte.render(texto, True, cor)
    superficie.blit(texto_superficie, (pos_x, pos_y))

# Definir funções para a mecânica do jogo
def soltar_inimigos(lista_inimigos):
    delay = random.random()
    if len(lista_inimigos) < 10 and delay < 0.1:
        x_pos = random.randint(0, LARGURA - tamanho_inimigo)
        y_pos = 0
        lista_inimigos.append([x_pos, y_pos])

def desenhar_inimigos(lista_inimigos):
    for pos_inimigo in lista_inimigos:
        tela.blit(imagem_inimigo, (pos_inimigo[0], pos_inimigo[1]))

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
            return pos_inimigo  # Retorna o inimigo que colidiu
    return None

def movimento_jogador(teclas, pos_jogador):
    if teclas[pygame.K_LEFT] and pos_jogador[0] > 0:
        pos_jogador[0] -= 10
    if teclas[pygame.K_RIGHT] and pos_jogador[0] < LARGURA - tamanho_jogador:
        pos_jogador[0] += 10

# Fonte para o texto
fonte = pygame.font.SysFont(None, 55)

# Loop principal do jogo
inimigos_atingidos = set()  # Conjunto para rastrear inimigos que já causaram dano
while not jogo_terminado:
    tela.fill((255, 255, 255))  # Preenche a tela com a cor branca

    # Captura os eventos do jogo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo_terminado = True

    teclas = pygame.key.get_pressed()
    movimento_jogador(teclas, pos_jogador)

    soltar_inimigos(lista_inimigos)
    pontuacao = atualizar_posicao_inimigos(lista_inimigos, pontuacao)

    inimigo_colidido = verificar_colisoes(lista_inimigos, pos_jogador)
    if inimigo_colidido and id(inimigo_colidido) not in inimigos_atingidos:
        vidas -= 1
        inimigos_atingidos.add(id(inimigo_colidido))  # Marca o inimigo como já causador de dano
        if vidas <= 0:
            jogo_terminado = True
        else:
            # Pausa o jogo por um curto período
            tela.fill((255, 0, 0))  # Tela de pausa em vermelho
            desenhar_texto(f'Vida Perdida! Vidas Restantes: {vidas}', fonte, (255, 255, 255), tela, LARGURA // 4, ALTURA // 3)
            pygame.display.update()
            time.sleep(tempo_pausa)
            tela.fill((255, 255, 255))  # Limpa a tela de pausa

    desenhar_inimigos(lista_inimigos)

    # Desenhar o jogador
    tela.blit(imagem_jogador, (pos_jogador[0], pos_jogador[1]))

    # Mostrar a pontuação e vidas
    desenhar_texto(f'Pontuação: {pontuacao}', fonte, (0, 0, 0), tela, 10, 10)
    desenhar_texto(f'Vidas: {vidas}', fonte, (0, 0, 0), tela, LARGURA - 150, 10)

    # Atualizar a tela
    pygame.display.update()

    relogio.tick(30)

# Tela de fim de jogo
tela.fill((0, 0, 0))
desenhar_texto('Fim de Jogo', fonte, (255, 0, 0), tela, LARGURA // 3, ALTURA // 3)
desenhar_texto(f'Pontuação Final: {pontuacao}', fonte, (255, 255, 255), tela, LARGURA // 4, ALTURA // 2)
pygame.display.update()
time.sleep(3)

pygame.quit()
