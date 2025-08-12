from pysat.formula import CNF, IDPool
from pysat.solvers import Glucose3
from itertools import combinations
from utilitarios import imprimir_tabuleiro
from visualizador import desenhar_sequencia_solucao

class Resolvedor8PuzzleSAT:
    def __init__(self, estado_inicial, estado_final):
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
        self.tamanho = len(estado_inicial)
        self.num_pecas = self.tamanho**2
        self.vpool = IDPool()

    def var_posicao(self, tempo, linha, coluna, valor):
        return self.vpool.id(('P', tempo, linha, coluna, valor))

    def var_acao(self, tempo, peca_movida):
        return self.vpool.id(('A', tempo, peca_movida))

    def criar_regras_de_estado(self, formula, tempo):
        for linha in range(self.tamanho):
            for coluna in range(self.tamanho):
                formula.append([self.var_posicao(tempo, linha, coluna, val) for val in range(self.num_pecas)])
                for v1, v2 in combinations(range(self.num_pecas), 2):
                    formula.append([-self.var_posicao(tempo, linha, coluna, v1), -self.var_posicao(tempo, linha, coluna, v2)])

        for valor in range(self.num_pecas):
            formula.append([self.var_posicao(tempo, l, c, valor) for l in range(self.tamanho) for c in range(self.tamanho)])
            for (l1, c1), (l2, c2) in combinations([(l, c) for l in range(self.tamanho) for c in range(self.tamanho)], 2):
                formula.append([-self.var_posicao(tempo, l1, c1, valor), -self.var_posicao(tempo, l2, c2, valor)])

    def criar_regras_de_acao(self, formula, tempo):
        pecas_moviveis = range(1, self.num_pecas)
        formula.append([self.var_acao(tempo, peca) for peca in pecas_moviveis])
        for p1, p2 in combinations(pecas_moviveis, 2):
            formula.append([-self.var_acao(tempo, p1), -self.var_acao(tempo, p2)])

        if tempo > 0:
            for peca in pecas_moviveis:
                formula.append([-self.var_acao(tempo - 1, peca), -self.var_acao(tempo, peca)])

    def criar_regras_de_transicao(self, formula, tempo):
        for peca_movida in range(1, self.num_pecas):
            acao_var = self.var_acao(tempo, peca_movida)
            
            for l1 in range(self.tamanho):
                for c1 in range(self.tamanho):
                    vizinhos = []
                    if l1 > 0: vizinhos.append((l1 - 1, c1))
                    if l1 < self.tamanho - 1: vizinhos.append((l1 + 1, c1))
                    if c1 > 0: vizinhos.append((l1, c1 - 1))
                    if c1 < self.tamanho - 1: vizinhos.append((l1, c1 + 1))

                    for l2, c2 in vizinhos:
                        pos_peca_t = self.var_posicao(tempo, l1, c1, peca_movida)
                        pos_vazio_t = self.var_posicao(tempo, l2, c2, 0)
                        
                        pos_peca_t1 = self.var_posicao(tempo + 1, l2, c2, peca_movida)
                        pos_vazio_t1 = self.var_posicao(tempo + 1, l1, c1, 0)
                        
                        formula.append([-acao_var, -pos_peca_t, -pos_vazio_t, pos_peca_t1])
                        formula.append([-acao_var, -pos_peca_t, -pos_vazio_t, pos_vazio_t1])

        for peca_a_manter in range(1, self.num_pecas):
            for peca_da_acao in range(1, self.num_pecas):
                if peca_a_manter != peca_da_acao:
                    acao_var = self.var_acao(tempo, peca_da_acao)
                    for l in range(self.tamanho):
                        for c in range(self.tamanho):
                            pos_t = self.var_posicao(tempo, l, c, peca_a_manter)
                            pos_t1 = self.var_posicao(tempo + 1, l, c, peca_a_manter)
                            formula.append([-acao_var, -pos_t, pos_t1])

    def resolver(self, max_passos=30):
        for num_passos in range(max_passos + 1):
            print(f"Tentando encontrar solução com {num_passos} passo(s)...")
            
            formula = CNF()
            
            for linha in range(self.tamanho):
                for coluna in range(self.tamanho):
                    valor = self.estado_inicial[linha][coluna]
                    formula.append([self.var_posicao(0, linha, coluna, valor)])

            for tempo in range(num_passos):
                self.criar_regras_de_estado(formula, tempo)
                self.criar_regras_de_acao(formula, tempo)
                self.criar_regras_de_transicao(formula, tempo)
            
            self.criar_regras_de_estado(formula, num_passos)

            for linha in range(self.tamanho):
                for coluna in range(self.tamanho):
                    valor = self.estado_final[linha][coluna]
                    formula.append([self.var_posicao(num_passos, linha, coluna, valor)])

            with Glucose3(bootstrap_with=formula.clauses) as solver:
                if solver.solve():
                    print(f"\nSolução encontrada em {num_passos} passos!")
                    modelo = solver.get_model()
                    self.imprimir_solucao(modelo, num_passos)
                    return modelo
        
        print(f"Não foi possível encontrar uma solução em até {max_passos} passos.")
        return None

    def imprimir_solucao(self, modelo, num_passos):
        vars_verdadeiras = [self.vpool.obj(var) for var in modelo if var > 0 and self.vpool.obj(var)]
        acoes_executadas = sorted([var for var in vars_verdadeiras if var[0] == 'A'], key=lambda x: x[1])
        
        print("\nSequência de Ações:")
        for acao in acoes_executadas:
            _, passo_tempo, peca_movida = acao
            print(f"Passo {passo_tempo + 1}: Mover peça {peca_movida}")

        print("\nEvolução do Tabuleiro:")
        sequencia_tabuleiros = []
        for tempo in range(num_passos + 1):
            print(f"\n--- Tempo {tempo} ---")
            tabuleiro = [[-1] * self.tamanho for _ in range(self.tamanho)]
            posicoes_verdadeiras = [var for var in vars_verdadeiras if var[0] == 'P' and var[1] == tempo]
            for pos in posicoes_verdadeiras:
                _, _, linha, coluna, valor = pos
                tabuleiro[linha][coluna] = valor
            sequencia_tabuleiros.append(tabuleiro)
            imprimir_tabuleiro(tabuleiro)
            
        try:
            desenhar_sequencia_solucao(sequencia_tabuleiros, num_passos, acoes_executadas)
        except Exception as e:
            print(f"\nNão foi possível gerar a visualização gráfica. Erro: {e}")