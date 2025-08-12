# Resolvedor de 8-Puzzle com Lógica Proposicional (SAT)

Este projeto é uma implementação de um resolvedor para o clássico quebra-cabeça 8-puzzle, desenvolvido como atividade para a disciplina de Lógica para Computação.

A solução utiliza o poder dos resolvedores de Satisfatibilidade Booleana (SAT) para modelar o problema, suas regras e transições de estado. O objetivo é, a partir de um estado inicial, encontrar a sequência ótima de movimentos para alcançar o estado final ordenado.

## O Problema: 8-Puzzle

O 8-puzzle é um quebra-cabeça deslizante que consiste em uma grade 3x3 com 8 peças numeradas (de 1 a 8) e um espaço vazio. O objetivo é reorganizar as peças, movendo-as adjacente ao espaço vazio, até que a ordem numérica seja alcançada.

## Resultado Final

O programa não apenas resolve o quebra-cabeça, mas também gera uma visualização completa da sequência de movimentos, desde o estado inicial até a solução.

## Tecnologias Utilizadas

*   **Linguagem:** Python 3
*   **Resolvedor SAT:** [PySAT](https://github.com/pysathq/pysat) - Uma biblioteca Python para prototipagem e desenvolvimento de algoritmos baseados em SAT.
*   **Visualização:** Matplotlib - Para a geração da imagem com a sequência da solução.

## Como Executar o Projeto

### Pré-requisitos

- Python 3.
- Git (para clonar o repositório).
- As bibliotecas Python necessárias.

### 1. Clone o Repositório

Abra seu terminal e clone este repositório para sua máquina local:
```bash
git clone https://github.com/alinevitoriaw/solver-8puzzle-sat.git
cd solver-8puzzle-sat
