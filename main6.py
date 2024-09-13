import pygame
import random
import time

# Inicializa o pygame
pygame.init()

# Define o tamanho da janela e cria a tela do jogo
LARGURA, ALTURA = 1200, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo Simples com PyGame")

# Carregar imagens
imagem_personagens = [
    pygame.image.load(f'imagens/personagem{i}.png') for i in range(1, 5)
]
imagem_inimigos = [
    pygame.image.load(f'imagens/inimigo{i}.png') for i in range(1, 5)
]

# Redimensionar imagens se necessário
tamanho_personagem = 50
tamanho_inimigo = 50
imagem_personagens = [pygame.transform.scale(img, (tamanho_personagem, tamanho_personagem)) for img in
                      imagem_personagens]
imagem_inimigos = [pygame.transform.scale(img, (tamanho_inimigo, tamanho_inimigo)) for img in imagem_inimigos]

# Variáveis do Jogo
VELOCIDADE = 10
relogio = pygame.time.Clock()

# Função para desenhar o texto na tela
def desenhar_texto(texto, fonte, cor, superficie, pos_x, pos_y):
    texto_superficie = fonte.render(texto, True, cor)
    texto_rect = texto_superficie.get_rect(center=(pos_x, pos_y))
    superficie.blit(texto_superficie, texto_rect)

# Função para exibir a tela de seleção de personagem
def tela_selecao_personagem():
    selecionado = 0
    enquanto_rodando = True
    fonte = pygame.font.SysFont(None, 55)

    while enquanto_rodando:
        tela.fill((200, 200, 200))  # Cor de fundo da tela de seleção

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    selecionado = (selecionado - 1) % 4
                if evento.key == pygame.K_RIGHT:
                    selecionado = (selecionado + 1) % 4
                if evento.key == pygame.K_RETURN:
                    return selecionado  # Retorna o índice do personagem selecionado

        # Desenhar os personagens
        espacamento = 100
        for i, img in enumerate(imagem_personagens):
            pos_x = LARGURA // 2 + (i - 1.5) * espacamento
            pos_y = ALTURA // 2
            if i == selecionado:
                pygame.draw.rect(tela, (255, 0, 0), (pos_x - 60, pos_y - 60, 120, 120), 2)  # Destaca a seleção
            tela.blit(img, (pos_x - tamanho_personagem // 2, pos_y - tamanho_personagem // 2))

        desenhar_texto('Selecione seu personagem', fonte, (0, 0, 0), tela, LARGURA // 2, ALTURA // 4)
        desenhar_texto('Use as setas esquerda/direita e Enter para selecionar', fonte, (0, 0, 0), tela, LARGURA // 2, ALTURA // 4 + 50)

        pygame.display.update()

# Função para iniciar o jogo com o personagem e inimigo selecionados
def iniciar_jogo(personagem_idx):
    pos_jogador = [LARGURA // 2, ALTURA - 2 * tamanho_personagem]
    pos_inimigo = [random.randint(0, LARGURA - tamanho_inimigo), 0]
    lista_inimigos = [pos_inimigo]

    jogo_terminado = False
    pontuacao = 0
    vidas = 3
    tempo_pausa = 1  # Tempo de pausa em segundos
    inicio_tempo = time.time()  # Marca o início do jogo

    fonte = pygame.font.SysFont(None, 55)
    imagem_jogador = imagem_personagens[personagem_idx]
    imagem_inimigo = imagem_inimigos[personagem_idx]

    while not jogo_terminado:
        tela.fill((255, 255, 255))  # Preenche a tela com a cor branca

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_terminado = True

        teclas = pygame.key.get_pressed()
        movimento_jogador(teclas, pos_jogador)

        soltar_inimigos(lista_inimigos)
        pontuacao = atualizar_posicao_inimigos(lista_inimigos, pontuacao)

        inimigo_colidido = verificar_colisoes(lista_inimigos, pos_jogador)
        if inimigo_colidido:
            vidas -= 1
            if vidas <= 0:
                jogo_terminado = True
            else:
                tela.fill((255, 0, 0))  # Tela de pausa em vermelho
                desenhar_texto(f'Vida Perdida! Vidas Restantes: {vidas}', fonte, (255, 255, 255), tela, LARGURA // 2, ALTURA // 3)
                pygame.display.update()
                time.sleep(tempo_pausa)
                tela.fill((255, 255, 255))  # Limpa a tela de pausa

        desenhar_inimigos(lista_inimigos, imagem_inimigo)
        tela.blit(imagem_jogador, (pos_jogador[0], pos_jogador[1]))

        desenhar_texto(f'Pontuação: {pontuacao}', fonte, (0, 0, 0), tela, 10, 10)
        desenhar_texto(f'Vidas: {vidas}', fonte, (0, 0, 0), tela, LARGURA - 150, 10)

        pygame.display.update()
        relogio.tick(30)

    tempo_jogo = int(time.time() - inicio_tempo)
    tela.fill((0, 0, 0))
    desenhar_texto('Fim de Jogo', fonte, (255, 0, 0), tela, LARGURA // 2, ALTURA // 3)
    desenhar_texto(f'Pontuação Final: {pontuacao}', fonte, (255, 255, 255), tela, LARGURA // 2, ALTURA // 2)
    desenhar_texto(f'Tempo de Jogo: {tempo_jogo} segundos', fonte, (255, 255, 255), tela, LARGURA // 2, ALTURA // 1.5)
    pygame.display.update()
    time.sleep(5)

# Função para movimentar o jogador
def movimento_jogador(teclas, pos_jogador):
    if teclas[pygame.K_LEFT] and pos_jogador[0] > 0:
        pos_jogador[0] -= 10
    if teclas[pygame.K_RIGHT] and pos_jogador[0] < LARGURA - tamanho_personagem:
        pos_jogador[0] += 10

# Funções adicionais para o jogo
def soltar_inimigos(lista_inimigos):
    delay = random.random()
    if len(lista_inimigos) < 10 and delay < 0.1:
        x_pos = random.randint(0, LARGURA - tamanho_inimigo)
        y_pos = 0
        lista_inimigos.append([x_pos, y_pos])

def desenhar_inimigos(lista_inimigos, imagem_inimigo):
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

    if (i_x >= j_x and i_x < (j_x + tamanho_personagem)) or (j_x >= i_x and j_x < (i_x + tamanho_inimigo)):
        if (i_y >= j_y and i_y < (j_y + tamanho_personagem)) or (j_y >= i_y and j_y < (i_y + tamanho_inimigo)):
            return True
    return False

def verificar_colisoes(lista_inimigos, pos_jogador):
    for pos_inimigo in lista_inimigos:
        if detectar_colisao(pos_jogador, pos_inimigo):
            return pos_inimigo
    return None

# Função principal para o jogo
def main():
    while True:
        personagem_idx = tela_selecao_personagem()  # Tela de seleção de personagem
        iniciar_jogo(personagem_idx)  # Inicia o jogo com o personagem selecionado

# Inicia o jogo
main()
pygame.quit()
