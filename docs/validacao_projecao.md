# Validação do motor de projeção por coorte

Gerado por `scripts/validar_projecao.py`.

## V1 — Calibração dos nascimentos c(t)

c(t) = nascimentos oficiais / (ASFR da ONU × mulheres da ONU). Perto de 1 = o modelo de fecundidade por idade é consistente com o total oficial.

| País | c mín | c máx |
|---|---|---|
| NGA | 0.9998 | 1.0003 |
| ETH | 0.9996 | 1.0005 |
| COD | 1.0001 | 1.0002 |
| VNM | 1.0002 | 1.0007 |
| IND | 1.0001 | 1.0005 |
| IDN | 1.0000 | 1.0002 |
| IRN | 0.9983 | 1.0004 |
| SAU | 0.9920 | 0.9942 |
| MAR | 1.0011 | 1.0021 |
| EGY | 0.9992 | 1.0004 |
| THA | 0.9994 | 1.0004 |
| MEX | 1.0006 | 1.0007 |
| POL | 0.9998 | 1.0098 |
| BRA | 1.0001 | 1.0009 |
| USA | 0.9972 | 0.9986 |
| CHN | 0.9999 | 1.0003 |
| FRA | 0.9996 | 1.0000 |
| ARG | 0.9999 | 1.0000 |
| CHL | 0.9977 | 1.0000 |
| SWE | 0.9970 | 0.9994 |
| GBR | 0.9950 | 1.0005 |
| AUS | 0.9957 | 0.9967 |
| ZAF | 0.9971 | 0.9982 |
| JPN | 1.0005 | 1.0013 |
| DEU | 0.9993 | 1.0058 |
| ITA | 1.0002 | 1.0014 |
| KOR | 1.0006 | 1.0033 |
| RUS | 0.9976 | 1.0023 |

**Maior desvio de 1 em todos os países e anos: 0.98%.**

## V2 — Migração líquida residual vs NetMigrations (ONU)

Soma, sobre idades e sexos, do resíduo M(a,t) vs saldo migratório da ONU (milhares/ano), média 2025-2074. **Não é teste independente para a idade 0:** a fração de mortalidade infantil W_INFANTIL = 0.25 foi calibrada (grade 0,15–0,75) para minimizar justamente esta diferença.

| País | resíduo médio | ONU médio | diferença |
|---|---|---|---|
| NGA | 25 | 41 | -16 |
| ETH | 40 | 34 | 6 |
| COD | -38 | -45 | 7 |
| VNM | -29 | -32 | 3 |
| IND | -352 | -382 | 30 |
| IDN | -41 | -48 | 7 |
| IRN | -23 | -27 | 4 |
| SAU | 32 | 35 | -3 |
| MAR | -73 | -76 | 3 |
| EGY | -18 | -22 | 4 |
| THA | 57 | 58 | -1 |
| MEX | -94 | -98 | 4 |
| POL | -12 | -11 | -2 |
| BRA | -56 | -59 | 3 |
| USA | 1,231 | 1,258 | -27 |
| CHN | -164 | -184 | 20 |
| FRA | 102 | 104 | -2 |
| ARG | 1 | 1 | 1 |
| CHL | 20 | 20 | 0 |
| SWE | 32 | 33 | -0 |
| GBR | 219 | 221 | -2 |
| AUS | 160 | 165 | -4 |
| ZAF | 170 | 173 | -4 |
| JPN | 112 | 113 | -0 |
| DEU | 150 | 154 | -4 |
| ITA | 47 | 46 | 0 |
| KOR | 20 | 19 | 1 |
| RUS | 292 | 303 | -11 |

**Mediana do desvio absoluto: 3.3 mil/ano; máximo: 30 mil/ano (IND).** Antes do ajuste infantil o máximo era 124 mil/ano (NGA), concentrado na idade 1: os óbitos de idade 0 do ano-calendário incluem recém-nascidos que ainda não existiam em 1º de julho, e a coorte presente em julho enfrenta só uma fração dessa mortalidade. O resíduo é aplicado em número absoluto e igual no cenário e na base, então tende a afetar mais o nível do que a diferença entre os dois.

## V3 — N* de 2024: motor vs pipeline de produção

| País | N* produção | N* motor | dif. relativa |
|---|---|---|---|
| NGA | 2.5796 | 2.5796 | -0.00% |
| ETH | 2.9995 | 2.9995 | -0.00% |
| COD | 3.4082 | 3.4082 | -0.00% |
| VNM | 1.4793 | 1.4792 | -0.01% |
| IND | 1.3676 | 1.3676 | -0.00% |
| IDN | 1.4487 | 1.4487 | -0.00% |
| IRN | 1.6574 | 1.6574 | +0.00% |
| SAU | 3.0514 | 3.0524 | +0.03% |
| MAR | 1.6604 | 1.6603 | -0.01% |
| EGY | 2.6123 | 2.6123 | -0.00% |
| THA | 0.5531 | 0.5531 | -0.01% |
| MEX | 1.6711 | 1.6711 | -0.00% |
| POL | 0.6231 | 0.6231 | -0.01% |
| BRA | 1.1731 | 1.1731 | +0.00% |
| USA | 0.9609 | 0.9609 | +0.00% |
| CHN | 0.5928 | 0.5928 | -0.00% |
| FRA | 0.7515 | 0.7516 | +0.01% |
| ARG | 1.0649 | 1.0649 | -0.00% |
| CHL | 0.8126 | 0.8125 | -0.01% |
| SWE | 0.7859 | 0.7860 | +0.01% |
| GBR | 0.8025 | 0.8024 | -0.01% |
| AUS | 1.0750 | 1.0750 | -0.00% |
| ZAF | 1.6604 | 1.6604 | -0.00% |
| JPN | 0.4258 | 0.4258 | -0.00% |
| DEU | 0.6301 | 0.6301 | -0.00% |
| ITA | 0.4944 | 0.4944 | -0.00% |
| KOR | 0.3666 | 0.3665 | -0.02% |
| RUS | 0.7869 | 0.7869 | +0.00% |

**Maior diferença relativa: 0.03%.**

## V4 — Sem migração vs variante "Zero migration" da ONU (população 2074, milhares)

Teste independente: nenhum parâmetro do motor foi ajustado a este dado.

| País | ONU Zero migration | motor (migração=0) | dif. relativa |
|---|---|---|---|
| NGA | 427,445 | 429,079 | +0.38% |
| ETH | 293,505 | 293,509 | +0.00% |
| COD | 337,903 | 337,473 | -0.13% |
| VNM | 106,524 | 106,326 | -0.19% |
| IND | 1,711,822 | 1,709,225 | -0.15% |
| IDN | 323,528 | 323,059 | -0.14% |
| IRN | 96,326 | 96,375 | +0.05% |
| SAU | 45,032 | 45,489 | +1.02% |
| MAR | 48,098 | 47,925 | -0.36% |
| EGY | 192,001 | 191,923 | -0.04% |
| THA | 50,380 | 50,521 | +0.28% |
| MEX | 153,009 | 152,768 | -0.16% |
| POL | 26,988 | 26,803 | -0.69% |
| BRA | 200,273 | 199,937 | -0.17% |
| USA | 310,120 | 312,762 | +0.85% |
| CHN | 964,226 | 963,291 | -0.10% |
| FRA | 58,376 | 58,667 | +0.50% |
| ARG | 45,272 | 45,256 | -0.03% |
| CHL | 16,375 | 16,434 | +0.36% |
| SWE | 8,954 | 9,040 | +0.97% |
| GBR | 58,858 | 59,492 | +1.08% |
| AUS | 25,535 | 25,820 | +1.12% |
| ZAF | 73,993 | 74,264 | +0.37% |
| JPN | 77,750 | 78,142 | +0.50% |
| DEU | 60,931 | 61,224 | +0.48% |
| ITA | 37,827 | 38,008 | +0.48% |
| KOR | 30,255 | 30,364 | +0.36% |
| RUS | 105,684 | 106,098 | +0.39% |

**Mediana do desvio absoluto: 0.36%; máximo: 1.12%.**

## V5 e V6 — TFR→2,1 (rampa de 25 anos), sem migração: motor vs P_eq do projeto

O P_eq atual (narayama.live) usa um método mais simples: escala o total de nascimentos pela razão entre TFRs e mantém os óbitos da ONU, sem modelar a estrutura etária das mulheres. **V5** compara com o motor de coorte completo; **V6** repete o motor com as mulheres do cenário-base como exposição (efeito de eco desligado), para testar a hipótese de que a diferença vem do eco.

| País | P_eq do projeto (mi) | V5 motor (mi) | V5 dif. | V6 sem eco (mi) | V6 dif. |
|---|---|---|---|---|---|
| NGA | 397.3 | 395.1 | -0.56% | 401.3 | +1.01% |
| ETH | 279.2 | 275.9 | -1.16% | 279.2 | -0.01% |
| COD | 259.9 | 250.0 | -3.82% | 265.2 | +2.02% |
| VNM | 116.5 | 118.7 | +1.95% | 115.6 | -0.70% |
| IND | 1,870.0 | 1,899.8 | +1.59% | 1,858.0 | -0.64% |
| IDN | 348.2 | 352.4 | +1.19% | 346.2 | -0.58% |
| IRN | 107.2 | 109.4 | +2.08% | 106.7 | -0.51% |
| SAU | 48.0 | 48.8 | +1.70% | 48.2 | +0.45% |
| MAR | 51.5 | 52.0 | +0.91% | 51.1 | -0.74% |
| EGY | 191.7 | 190.5 | -0.64% | 191.3 | -0.21% |
| THA | 59.6 | 62.3 | +4.47% | 59.5 | -0.15% |
| MEX | 169.3 | 173.7 | +2.64% | 168.2 | -0.62% |
| POL | 31.1 | 31.9 | +2.29% | 30.8 | -0.95% |
| BRA | 226.8 | 232.2 | +2.40% | 225.2 | -0.70% |
| USA | 342.3 | 352.1 | +2.85% | 344.5 | +0.64% |
| CHN | 1,153.6 | 1,201.2 | +4.12% | 1,148.0 | -0.49% |
| FRA | 64.1 | 65.7 | +2.38% | 64.4 | +0.41% |
| ARG | 51.3 | 52.6 | +2.61% | 51.1 | -0.38% |
| CHL | 19.6 | 20.3 | +3.68% | 19.6 | -0.09% |
| SWE | 10.0 | 10.4 | +3.37% | 10.1 | +0.85% |
| GBR | 66.2 | 68.5 | +3.52% | 66.9 | +0.95% |
| AUS | 28.1 | 28.9 | +2.83% | 28.4 | +0.83% |
| ZAF | 79.3 | 80.5 | +1.55% | 79.1 | -0.14% |
| JPN | 89.4 | 92.5 | +3.41% | 90.0 | +0.63% |
| DEU | 68.1 | 69.9 | +2.61% | 68.5 | +0.51% |
| ITA | 43.6 | 45.3 | +3.75% | 43.8 | +0.47% |
| KOR | 36.8 | 38.4 | +4.47% | 36.8 | -0.04% |
| RUS | 119.6 | 123.5 | +3.27% | 120.1 | +0.40% |

**V5 (com eco): mediana 2.61%, máximo 4.47%. V6 (sem eco): mediana 0.54%, máximo 2.02%.**

**Leitura:** desligar o eco aproxima o motor do método antigo (a mediana do desvio cai mais da metade), o que **confirma** que a diferença vem do efeito de eco: no método novo os nascimentos de hoje mudam o número de mulheres em idade fértil 25 anos depois. O método antigo não captura isso (subestima o efeito quando a TFR sobe de um nível baixo; superestima quando cai de um nível alto). O motor de coorte é o mais completo, mas o P_eq público do narayama.live **não foi alterado**: trocar de método muda números publicados e é decisão do autor.
