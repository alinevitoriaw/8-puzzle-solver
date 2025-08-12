# main.py

from solver import Resolvedor8PuzzleSAT
from utilitarios import imprimir_tabuleiro, gerar_estado_inicial_solucionavel

if __name__ == "__main__":
    print("*** SOLVER de 8-Puzzle com PySAT ***")

    ESTADO_FINAL = [
        [6, 4, 7],
        [8, 5, 0],
        [3, 2, 1]
    ]

    estado_a_resolver = gerar_estado_inicial_solucionavel(ESTADO_FINAL, num_movimentos=20)

    print("\nEstado Inicial:")
    imprimir_tabuleiro(estado_a_resolver)
    
    print("\nEstado Final:")
    imprimir_tabuleiro(ESTADO_FINAL)
    
    instancia_solver = Resolvedor8PuzzleSAT(estado_a_resolver, ESTADO_FINAL)
    
    instancia_solver.resolver()

    print("\n*** Fim da Execução ***")