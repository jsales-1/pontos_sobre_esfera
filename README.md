# Otimização Conformacional de Pontos Sobre Esferas

**## Autor**: José David Alves Sales  
**## Orientador**: Dr. José Mario Martínez Pérez  

Este repositório contém o código utilizado para a otimização de pontos sobre uma esfera, com o objetivo de formar sólidos de Platão. O processo envolve a distribuição de pontos na superfície esférica de maneira que maximize a uniformidade das distâncias entre eles. A otimização é realizada com a utilização de pesos ponderados e a função objetivo é minimizada por um algoritmo quasi-Newton.

## Objetivo

O principal objetivo deste projeto é explorar a otimização de pontos sobre a esfera para gerar poliedros regulares, como os sólidos de Platão (tetraedro, cubo, octaedro, dodecaedro e icosaedro), e analisar como diferentes parâmetros influenciam a formação dessas estruturas geométricas.

## Metodologia

A otimização é realizada com a seguinte abordagem:

1. **Geração de Configurações Iniciais**: São geradas posições aleatórias de pontos na esfera, com diferentes números de classes e pontos por classe.
2. **Conversão de Coordenadas**: As coordenadas esféricas são convertidas para coordenadas cartesianas para calcular as distâncias entre os pontos.
3. **Função Objetivo**: A função objetivo minimiza a soma das distâncias ponderadas entre todos os pares de pontos, de acordo com as classes atribuídas a cada ponto.
4. **Otimização**: O algoritmo L-BFGS-B é utilizado para ajustar iterativamente as coordenadas esféricas, minimizando a função objetivo.
5. **Exportação dos Resultados**: Após a otimização, os pontos são exportados para o formato STL, permitindo a visualização tridimensional dos poliedros gerados.

## Implementação

O processo foi implementado em Python, utilizando as bibliotecas:
- `numpy`: Para operações matemáticas e manipulação de matrizes.
- `scipy`: Para a realização da otimização e cálculos de distâncias.
- `stl`: Para manipulação e exportação de modelos em formato STL.

## Parâmetros de Teste

Foram realizados testes variando o número de pontos e classes, com o objetivo de identificar configurações que gerassem os sólidos de Platão de maneira eficiente. As duas abordagens de teste envolvem:
1. A variação do número de pontos de acordo com múltiplos de 4, com um número fixo de classes.
2. A variação com múltiplos de 2 e número de classes ajustado conforme a quantidade de pontos.

## Resultados

Os resultados indicaram que, ao otimizar a distribuição dos pontos, os sólidos de Platão surgem como soluções naturais em determinadas configurações. Poliedros como o tetraedro, cubo, octaedro, dodecaedro e icosaedro foram gerados e visualizados.

## Como Usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/jsales-1/pontos_sobre_esfera.git
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o código para otimizar os pontos e gerar o poliedro:
   ```bash
   python otimização.py
   ```

4. Visualize os resultados no formato STL gerado.

## Referências

- [Distribuição de Pontos sobre Esfera - School of Mathematics and Statistics](https://www.unsw.edu.au/science/our-schools/maths/our-school/spotlight-on-our-people/history-school/glimpses-mathematics-and-statistics/distributing-points-sphere)
- [Repositório Pontos Sobre Esfera](https://github.com/jsales-1/pontos_sobre_esfera)
- [Documentação do NumPy](https://numpy.org/doc/stable/)
- [Documentação do SciPy](https://docs.scipy.org/doc/scipy/)
- [Documentação do Python STL](https://python-stl.readthedocs.io/en/latest/)

---

Agora o README está ajustado com o nome do orientador incluído.
