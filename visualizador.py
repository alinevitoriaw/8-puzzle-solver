import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Tuple, Optional


class VisualizadorPuzzle:
    def __init__(self, tamanho_celula: float = 2.5, arquivo_saida: str = "solucao_8_puzzle.png"):
        self.tamanho_celula = tamanho_celula
        self.arquivo_saida = arquivo_saida
        
        self.cores = {
            'celula_numerada': '#f0f0f0',
            'celula_vazia': '#cccccc',
            'borda': 'black',
            'texto': '#333333'
        }
        
        self.estilos = {
            'largura_borda': 2,
            'tamanho_fonte': 16,
            'peso_fonte': 'bold',
            'espacamento': 1.5
        }

    def _configurar_eixo(self, eixo, tamanho_tabuleiro: int) -> None:
        eixo.set_xlim(0, tamanho_tabuleiro)
        eixo.set_ylim(0, tamanho_tabuleiro)
        eixo.set_aspect('equal')
        eixo.set_xticks([])
        eixo.set_yticks([])
        eixo.invert_yaxis()

    def _desenhar_celula(self, eixo, linha: int, coluna: int, valor: int) -> None:
        cor_fundo = self.cores['celula_numerada'] if valor != 0 else self.cores['celula_vazia']
        
        retangulo = patches.Rectangle(
            (coluna, linha), 1, 1,
            linewidth=self.estilos['largura_borda'],
            edgecolor=self.cores['borda'],
            facecolor=cor_fundo
        )
        eixo.add_patch(retangulo)

        if valor != 0:
            eixo.text(
                coluna + 0.5, linha + 0.5, str(valor),
                ha='center', va='center',
                fontsize=self.estilos['tamanho_fonte'],
                weight=self.estilos['peso_fonte'],
                color=self.cores['texto']
            )

    def _desenhar_tabuleiro(self, eixo, tabuleiro: List[List[int]]) -> None:
        tamanho = len(tabuleiro)
        for linha in range(tamanho):
            for coluna in range(tamanho):
                valor = tabuleiro[linha][coluna]
                self._desenhar_celula(eixo, linha, coluna, valor)

    def _obter_acao_por_passo(self, acoes_executadas: List[Tuple], passo: int) -> Optional[str]:
        for acao in acoes_executadas:
            if len(acao) >= 3 and acao[1] == passo - 1:
                return f"Mover peça {acao[2]}"
        return "Ação desconhecida"

    def _definir_titulo(self, eixo, indice: int, acoes_executadas: List[Tuple]) -> None:
        if indice == 0:
            eixo.set_title("Estado Inicial", fontsize=12, pad=10)
        else:
            acao = self._obter_acao_por_passo(acoes_executadas, indice)
            eixo.set_title(f"Passo {indice}\n({acao})", fontsize=12, pad=10)

    def desenhar_sequencia_solucao(self, sequencia_de_tabuleiros: List[List[List[int]]], 
                                 num_passos: int, acoes_executadas: List[Tuple]) -> None:
        if not sequencia_de_tabuleiros:
            raise ValueError("Sequência de tabuleiros não pode estar vazia")
        
        num_plots = num_passos + 1
        largura_figura = num_plots * self.tamanho_celula
        
        fig, eixos = plt.subplots(1, num_plots, figsize=(largura_figura, 3))
        
        if num_plots == 1:
            eixos = [eixos]
        
        tamanho_tabuleiro = len(sequencia_de_tabuleiros[0])
        
        for i, tabuleiro in enumerate(sequencia_de_tabuleiros):
            eixo_atual = eixos[i]
            
            self._configurar_eixo(eixo_atual, tamanho_tabuleiro)
            self._desenhar_tabuleiro(eixo_atual, tabuleiro)
            self._definir_titulo(eixo_atual, i, acoes_executadas)
        
        fig.tight_layout(pad=self.estilos['espacamento'])
        plt.savefig(self.arquivo_saida, dpi=150, bbox_inches='tight')
        print(f"\nVisualização da solução salva em '{self.arquivo_saida}'")
        plt.close(fig)


def desenhar_sequencia_solucao(sequencia_de_tabuleiros: List[List[List[int]]], 
                              num_passos: int, acoes_executadas: List[Tuple]) -> None:
    visualizador = VisualizadorPuzzle()
    visualizador.desenhar_sequencia_solucao(sequencia_de_tabuleiros, num_passos, acoes_executadas)