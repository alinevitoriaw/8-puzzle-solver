import random

def gerar_estado_inicial_solucionavel(estado_final, num_movimentos=50):
    tabuleiro = [linha[:] for linha in estado_final]
    tamanho = len(tabuleiro)
    
    linha_vazia, col_vazia = -1, -1
    for i in range(tamanho):
        for j in range(tamanho):
            if tabuleiro[i][j] == 0:
                linha_vazia, col_vazia = i, j
                break
    
    ultimo_movimento = None
    for _ in range(num_movimentos):
        movimentos_possiveis = []
        if linha_vazia > 0 and ultimo_movimento != 'B':
            movimentos_possiveis.append('C')
        if linha_vazia < tamanho - 1 and ultimo_movimento != 'C':
            movimentos_possiveis.append('B')
        if col_vazia > 0 and ultimo_movimento != 'D':
            movimentos_possiveis.append('E')
        if col_vazia < tamanho - 1 and ultimo_movimento != 'E':
            movimentos_possiveis.append('D')
        
        if not movimentos_possiveis:
            continue
            
        movimento_escolhido = random.choice(movimentos_possiveis)
        
        if movimento_escolhido == 'C':
            tabuleiro[linha_vazia][col_vazia], tabuleiro[linha_vazia-1][col_vazia] = tabuleiro[linha_vazia-1][col_vazia], tabuleiro[linha_vazia][col_vazia]
            linha_vazia -= 1
            ultimo_movimento = 'C'
        elif movimento_escolhido == 'B':
            tabuleiro[linha_vazia][col_vazia], tabuleiro[linha_vazia+1][col_vazia] = tabuleiro[linha_vazia+1][col_vazia], tabuleiro[linha_vazia][col_vazia]
            linha_vazia += 1
            ultimo_movimento = 'B'
        elif movimento_escolhido == 'E':
            tabuleiro[linha_vazia][col_vazia], tabuleiro[linha_vazia][col_vazia-1] = tabuleiro[linha_vazia][col_vazia-1], tabuleiro[linha_vazia][col_vazia]
            col_vazia -= 1
            ultimo_movimento = 'E'
        elif movimento_escolhido == 'D':
            tabuleiro[linha_vazia][col_vazia], tabuleiro[linha_vazia][col_vazia+1] = tabuleiro[linha_vazia][col_vazia+1], tabuleiro[linha_vazia][col_vazia]
            col_vazia += 1
            ultimo_movimento = 'D'
            
    return tabuleiro

def imprimir_tabuleiro(tabuleiro):
    tamanho = len(tabuleiro)
    linha_horizontal = " ---" * tamanho
    print(linha_horizontal)
    for linha in tabuleiro:
        print(f"| {' | '.join(map(str, linha))} |".replace('0', ' '))
    print(linha_horizontal)