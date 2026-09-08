Jogo da Velha: o experimento que provou por que aleatorio nunca vence otimizado.

Implementei em Python dois algoritmos para Jogatina da Velha — um "ingenuo" (jogadas aleatorias) e um "fera" (minimax, busca exaustiva de todo o espaco). E entao coloquei mereka para jogar 1 milhao de partidas.

Resultados:
- ingenuo vs ingenuo: 43.7% vitorias, 12.7% empates
- ingenuo vs fera: ingenuo NUNCA ganha (0% vitorias)
- fera vs ingenuo: fera vence ~90% das vezes
- fera vs fera: 100% empate — dois otimos se anulam

O fera explora todas as jogadas possiveis, avaliando vitoria, derrota e empate com profundidade. Contra ele, o aleatorio nao tem chance.

Cenarios de jogo mostram a supremacia do algoritmo: em partida unica, fera fecha em 5 jogadas; ingenuo mal chega ao fim.

Projeto funcional em Python, puro — funcoes puras, tabuleiros imutaveis.

Quer testar contra o fera? Clone o repo, rode `python main.py play fera` e tente vencer. Boa sorte.

github.com/davy/TicTacToe

#Python #Minimax #InteligenciaArtificial #JogosDeTabuleiro #EngenhariaDeSoftware #DataScience #Algoritmos #ProgramacaoFuncional