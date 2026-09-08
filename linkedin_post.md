Jogo da Velha: 1 milhao de partidas provaram por que aleatorio nunca vence otimizado.

Implementei em Python dois algoritmos para Jogo da Velha — um "ingenuo" (jogadas aleatorias) e um "fera" (minimax, busca exaustiva de todo o espaco). E entao coloquei eles para jogar 1.000.000 de partidas.

Resultados:
• ingenuo vs ingenuo: 43.7% vitorias, 12.7% empates — puro caos
• ingenuo vs fera: ingenuo NUNCA ganha. Zero. Nada.
• fera vs ingenuo: fera vence 99.5% das vezes
• fera vs fera: 100% empate — dois otimos se anulam

O fera calcula todas as jogadas possiveis, avaliando vitoria, derrota e empate com profundidade. Contra ele, o aleatorio nao tem nenhuma chance.

Projeto funcional em Python puro — funcoes puras, tabuleiros imutaveis, sem frameworks.

Quer testar contra o fera? Clone o repo e rode:
python main.py play fera          # voce joga O (o fera comeca)
python main.py play fera --first  # voce joga X (voce comeca)

Boa sorte. Voce vai precisar.

github.com/DavyAndrade/tic-tac-toe-python

#Python #InteligenciaArtificial #Minimax #JogosDeTabuleiro #EngenhariaDeSoftware #Algoritmos #ProgramacaoFuncional
