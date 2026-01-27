# game.py
# Lógica do jogo Reversi

def criar_tabuleiro():
    tab = [[0]*8 for _ in range(8)]
    tab[3][3] = -1
    tab[3][4] = 1
    tab[4][3] = 1
    tab[4][4] = -1
    return tab

DIRECOES = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

def jogada_valida(tab, linha, coluna, jogador):
    if tab[linha][coluna] != 0:
        return False

    adversario = -jogador
    for dl, dc in DIRECOES:
        l = linha + dl
        c = coluna + dc
        encontrou_adversario = False

        while 0 <= l < 8 and 0 <= c < 8 and tab[l][c] == adversario:
            encontrou_adversario = True
            l += dl
            c += dc

        if encontrou_adversario and 0 <= l < 8 and 0 <= c < 8 and tab[l][c] == jogador:
            return True
    return False

def jogar(tab, linha, coluna, jogador):
    if not jogada_valida(tab, linha, coluna, jogador):
        return False

    tab[linha][coluna] = jogador
    adversario = -jogador

    for dl, dc in DIRECOES:
        l = linha + dl
        c = coluna + dc
        caminho = []

        while 0 <= l < 8 and 0 <= c < 8 and tab[l][c] == adversario:
            caminho.append((l, c))
            l += dl
            c += dc

        if caminho and 0 <= l < 8 and 0 <= c < 8 and tab[l][c] == jogador:
            for pos in caminho:
                tab[pos[0]][pos[1]] = jogador
    return True

def tem_jogada_valida(tab, jogador):
    for i in range(8):
        for j in range(8):
            if jogada_valida(tab, i, j, jogador):
                return True
    return False

def contar_pecas(tab):
    x = sum(l.count(1) for l in tab)
    o = sum(l.count(-1) for l in tab)
    return x, o
