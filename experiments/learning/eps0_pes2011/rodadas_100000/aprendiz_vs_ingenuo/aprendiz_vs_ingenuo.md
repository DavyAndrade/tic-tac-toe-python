# Experimento: aprendiz vs ingenuo (100.000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `ingenuo`
- Semente: 42
- Rodadas: 100.000
- Recompensa: vitoria +20, empate +1, derrota -1
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/eps0_pes2011/rodadas_100000/aprendiz_vs_ingenuo/`

## Resultado acumulado

| Partida | J1 | V | J2 |
|---------|----|---|----|
| 100.000 | 73.234 | 14.078 | 12.688 |

**Identico byte a byte ao `eps0_pes1011` (+10/+1/−1)** — mesmas 73.234V /
14.078E / 12.688D, mesmos 220 estados, mesma distribuicao de 2a jogada
({2:37.625, 4:24.812, 6:25.182, 8:12.381}), mesma abertura.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 220 | — |

Mesmas chaves e mesmas acoes do q_table de10/1/−1; apenas os valores diferem
(escalonados pelo dobro da vitoria).

## Grafico

`progress.svg` — series `J1 (Aprendiz)` / `V` / `J2 (Ingenuo)` por partida.

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Plano como todos: 73,2% de vitorias, 87,3% sem derrota — identico ao 10/1/−1
em100k e ao perfil do 500k (73,7%/87,6%).

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Nenhuma — mesma curva do 10/1/−1.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. ~12.700 derrotas, ate o fim.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
Dobrar a vitoria (10→20) nao muda NADA na politica: o argmax das medias de Q
preserva a mesma ordem dos pares (estado, celula) nesta mistura de resultados,
entao a trajetoria inteira se repete. Escala de vitoria e parametro
invariante aqui — so pesos que mudam a ORDEM relativa entre linhas (empate 0,
derrota −5) tem efeito.
