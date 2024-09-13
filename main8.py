import pygame
import random
import time

# Inicializa o pygame
pygame.init()

# Define o tamanho da janela e cria a tela do jogo
LARGURA, ALTURA = 1000, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cascão vs Chuva - PyGame")

# Carregar imagens
imagem_fundo = pygame.image.load('imagens/fundo.jpg')
imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))  # Redimensiona o fundo para o tamanho da tela

imagens_personagens = [
    pygame.image.load('imagens/personagem1.png'),
    pygame.image.load('imagens/personagem2.png'),
    pygame.image.load('imagens/personagem3.png'),
    pygame.image.load('imagens/personagem4.png')
]

imagens_inimigos = [
    pygame.image.load('imagens/inimigo1.png'),
    pygame.image.load('imagens/inimigo2.png'),
    pygame.image.load('imagens/inimigo3.png'),
    pygame.image.load('imagens/inimigo4.png')
]

# Redimensionar imagens se necessário
tamanho_personagem = 50
tamanho_inimigo = 50

for i in range(4):
    imagens_personagens[i] = pygame.transform.scale(imagens_personagens[i], (tamanho_personagem, tamanho_personagem))
    imagens_inimigos[i] = pygame.transform.scale(imagens_inimigos[i], (tamanho_inimigo, tamanho_inimigo))

# Variáveis do Jogo
pos_personagem = [LARGURA // 2, ALTURA - 2 * tamanho_personagem]
lista_inimigos = []
VELOCIDADE = 10
relogio = pygame.time.Clock()

jogo_terminado = False
pontuacao = 0
vidas = 3
tempo_pausa = 1  # Tempo de pausa em segundos
inicio_tempo = time.time()  # Marca o início do jogo

# Inicializa variáveis de imagem de personagem e inimigo
imagem_personagem = imagens_personagens[0]
imagem_inimigo = imagens_inimigos[0]


# Função para desenhar o texto na tela
def desenhar_texto(texto, fonte, cor, superficie, pos_x, pos_y):
    texto_superficie = fonte.render(texto, True, cor)
    texto_rect = texto_superficie.get_rect(center=(pos_x, pos_y))
    superficie.blit(texto_superficie, texto_rect)


# Função para exibir o menu de seleção de personagens
def exibir_menu_selecao():
    global imagem_personagem, imagem_inimigo
    fonte_menu = pygame.font.SysFont(None, 55)
    selecionado = 0
    trocando = True

    while True:
        tela.blit(imagem_fundo, (0, 0))  # Desenha o fundo

        for i, imagem in enumerate(imagens_personagens):
            x_pos = LARGURA // 5 * (i + 1) - tamanho_personagem // 2
            y_pos = ALTURA // 2 - tamanho_personagem // 2 + 175  # Ajuste esta linha para mover os personagens para baixo
            tela.blit(imagem, (x_pos, y_pos))
            if i == selecionado:
                pygame.draw.rect(tela, (255, 0, 0),
                                 (x_pos - 10, y_pos - 10, tamanho_personagem + 20, tamanho_personagem + 20),
                                 2)  # Desenha uma borda vermelha ao redor da seleção

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    selecionado = (selecionado - 1) % 4
                elif evento.key == pygame.K_RIGHT:
                    selecionado = (selecionado + 1) % 4
                elif evento.key == pygame.K_RETURN:
                    imagem_personagem = imagens_personagens[selecionado]
                    imagem_inimigo = imagens_inimigos[selecionado]
                    return


# Função para soltar inimigos
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


def detectar_colisao(pos_personagem, pos_inimigo):
    p_x, p_y = pos_personagem
    i_x, i_y = pos_inimigo

    if (i_x >= p_x and i_x < (p_x + tamanho_personagem)) or (p_x >= i_x and p_x < (i_x + tamanho_inimigo)):
        if (i_y >= p_y and i_y < (p_y + tamanho_personagem)) or (p_y >= i_y and p_y < (i_y + tamanho_inimigo)):
            return True
    return False


def verificar_colisoes(lista_inimigos, pos_personagem):
    for pos_inimigo in lista_inimigos:
        if detectar_colisao(pos_personagem, pos_inimigo):
            return pos_inimigo  # Retorna o inimigo que colidiu
    return None


def movimento_personagem(teclas, pos_personagem):
    if teclas[pygame.K_LEFT] and pos_personagem[0] > 0:
        pos_personagem[0] -= 10
    if teclas[pygame.K_RIGHT] and pos_personagem[0] < LARGURA - tamanho_personagem:
        pos_personagem[0] += 10


# Fonte para o texto
fonte = pygame.font.SysFont(None, 55)

# Exibir o menu de seleção de personagens
exibir_menu_selecao()

# Loop principal do jogo
inimigos_atingidos = set()  # Conjunto para rastrear inimigos que já causaram dano
while not jogo_terminado:
    tela.blit(imagem_fundo, (0, 0))  # Desenha o fundo

    # Captura os eventos do jogo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo_terminado = True

    teclas = pygame.key.get_pressed()
    movimento_personagem(teclas, pos_personagem)

    soltar_inimigos(lista_inimigos)
    pontuacao = atualizar_posicao_inimigos(lista_inimigos, pontuacao)

    inimigo_colidido = verificar_colisoes(lista_inimigos, pos_personagem)
    if inimigo_colidido and id(inimigo_colidido) not in inimigos_atingidos:
        vidas -= 1
        inimigos_atingidos.add(id(inimigo_colidido))  # Marca o inimigo como já causador de dano
        if vidas <= 0:
            jogo_terminado = True
        else:
            # Pausa o jogo por um curto período
            tela.fill((255, 0, 0))  # Tela de pausa em vermelho
            desenhar_texto(f'Vida Perdida! Vidas Restantes: {vidas}', fonte, (255, 255, 255), tela, LARGURA // 2,
                           ALTURA // 2)
            pygame.display.update()
            time.sleep(tempo_pausa)
            tela.blit(imagem_fundo, (0, 0))  # Desenha o fundo novamente para limpar a tela de pausa

    desenhar_inimigos(lista_inimigos)

    # Desenhar o personagem
    tela.blit(imagem_personagem, (pos_personagem[0], pos_personagem[1]))

    # Mostrar a pontuação e vidas
    desenhar_texto(f'Pontuação: {pontuacao}', fonte, (0, 0, 0), tela, LARGURA // 2, 30)
    desenhar_texto(f'Vidas: {vidas}', fonte, (0, 0, 0), tela, LARGURA // 2, 70)

    # Atualizar a tela
    pygame.display.update()

    relogio.tick(30)

# Calcular o tempo de jogo
tempo_jogo = int(time.time() - inicio_tempo)

# Tela de fim de jogo
tela.blit(imagem_fundo, (0, 0))  # Desenha o fundo
desenhar_texto('Fim de Jogo', fonte, (255, 0, 0), tela, LARGURA // 2, ALTURA // 3)
desenhar_texto(f'Pontuação Final: {pontuacao}', fonte, (255, 255, 255), tela, LARGURA // 2, ALTURA // 2)
desenhar_texto(f'Tempo de Jogo: {tempo_jogo} segundos', fonte, (255, 255, 255), tela, LARGURA // 2, ALTURA // 1.5)
pygame.display.update()
time.sleep(5)  # Mostra a tela final por 5 segundos

pygame.quit()
