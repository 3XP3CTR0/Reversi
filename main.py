import pygame
from game import criar_tabuleiro, jogada_valida, jogar, contar_pecas, tem_jogada_valida

# ---------------- CONFIGURAÇÕES ----------------

LARGURA = 640
ALTURA = 760
TAMANHO_CASA = LARGURA // 8

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 130, 0)
AMARELO = (255, 255, 0)
CINZA = (210, 210, 210)
AZUL = (100, 160, 255)

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Reversi")

relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 22)
fonte_grande = pygame.font.SysFont("arial", 34)

# ---------------- ESTADO DO JOGO ----------------

def resetar_jogo():
    global tab, jogador, fim_de_jogo
    tab = criar_tabuleiro()
    jogador = 1   # 1 = Branco | -1 = Preto
    fim_de_jogo = False

resetar_jogo()

# ---------------- BOTÃO ----------------

BOTAO_RECT = pygame.Rect(240, 720, 160, 30)

def desenhar_botao():
    pygame.draw.rect(tela, AZUL, BOTAO_RECT, border_radius=8)
    texto = fonte.render("Reiniciar", True, PRETO)
    tela.blit(
        texto,
        (BOTAO_RECT.centerx - texto.get_width() // 2,
         BOTAO_RECT.centery - texto.get_height() // 2)
    )

# ---------------- DESENHO ----------------

def desenhar_tabuleiro(tab):
    tela.fill(VERDE)

    for i in range(8):
        for j in range(8):
            pygame.draw.rect(
                tela,
                PRETO,
                (j*TAMANHO_CASA, i*TAMANHO_CASA, TAMANHO_CASA, TAMANHO_CASA),
                1
            )

            if tab[i][j] == 1:
                pygame.draw.circle(
                    tela,
                    BRANCO,
                    (j*TAMANHO_CASA + TAMANHO_CASA//2,
                     i*TAMANHO_CASA + TAMANHO_CASA//2),
                    TAMANHO_CASA//2 - 6
                )

            elif tab[i][j] == -1:
                pygame.draw.circle(
                    tela,
                    PRETO,
                    (j*TAMANHO_CASA + TAMANHO_CASA//2,
                     i*TAMANHO_CASA + TAMANHO_CASA//2),
                    TAMANHO_CASA//2 - 6
                )

            elif not fim_de_jogo and jogada_valida(tab, i, j, jogador):
                pygame.draw.circle(
                    tela,
                    AMARELO,
                    (j*TAMANHO_CASA + TAMANHO_CASA//2,
                     i*TAMANHO_CASA + TAMANHO_CASA//2),
                    5
                )

def desenhar_hud():
    x, o = contar_pecas(tab)

    pygame.draw.rect(tela, CINZA, (0, 640, 640, 80))

    placar = fonte.render(f"Branco: {x}    Preto: {o}", True, PRETO)
    tela.blit(placar, (20, 665))

    if not fim_de_jogo:
        texto_turno = "Vez: Cinza" if jogador == 1 else "Vez: Preto"
    else:
        if x > o:
            texto_turno = "Branco venceu!"
        elif o > x:
            texto_turno = "Preto venceu!"
        else:
            texto_turno = "Empate!"

    msg = fonte_grande.render(texto_turno, True, PRETO)
    tela.blit(msg, (360, 660))

    desenhar_botao()

# ---------------- LOOP PRINCIPAL ----------------

rodando = True

while rodando:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mx, my = event.pos

            # Clique no botão reiniciar
            if BOTAO_RECT.collidepoint(mx, my):
                resetar_jogo()

            # Clique no tabuleiro
            elif not fim_de_jogo and my < 640:

                if tem_jogada_valida(tab, jogador):

                    linha = my // TAMANHO_CASA
                    coluna = mx // TAMANHO_CASA

                    if jogar(tab, linha, coluna, jogador):
                        jogador *= -1

                if not tem_jogada_valida(tab, 1) and not tem_jogada_valida(tab, -1):
                    fim_de_jogo = True

    desenhar_tabuleiro(tab)
    desenhar_hud()

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
