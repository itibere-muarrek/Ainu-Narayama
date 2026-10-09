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

Soma, sobre idades e sexos, do resíduo M(a,t) vs saldo migratório da ONU (milhares/ano), média 2025-2074. Se o resíduo fosse só viés do método, não acompanharia a migração.

| País | resíduo médio | ONU médio | diferença |
|---|---|---|---|
| NGA | 165 | 41 | 124 |
| ETH | 61 | 34 | 27 |
| COD | 30 | -45 | 75 |
| VNM | -26 | -32 | 6 |
| IND | -282 | -382 | 100 |
| IDN | -29 | -48 | 19 |
| IRN | -21 | -27 | 5 |
| SAU | 32 | 35 | -2 |
| MAR | -72 | -76 | 4 |
| EGY | -12 | -22 | 9 |
| THA | 57 | 58 | -0 |
| MEX | -92 | -98 | 7 |
| POL | -12 | -11 | -1 |
| BRA | -52 | -59 | 7 |
| USA | 1,234 | 1,258 | -24 |
| CHN | -157 | -184 | 27 |
| FRA | 103 | 104 | -1 |
| ARG | 2 | 1 | 1 |
| CHL | 20 | 20 | 0 |
| SWE | 32 | 33 | -0 |
| GBR | 219 | 221 | -1 |
| AUS | 161 | 165 | -4 |
| ZAF | 175 | 173 | 1 |
| JPN | 112 | 113 | -0 |
| DEU | 150 | 154 | -3 |
| ITA | 47 | 46 | 1 |
| KOR | 20 | 19 | 1 |
| RUS | 292 | 303 | -10 |

**Leitura:** na maioria dos países o resíduo acompanha o saldo oficial da ONU de perto (diferença de poucas dezenas de milhares por ano ou menos), o que indica que ele é de fato migração. Divergências maiores (NGA, IND, COD: 75–125 mil/ano) **não foram investigadas**. Hipótese não testada: nesses países de população jovem e fecundidade alta, a aproximação do passo anual nas idades 0–4 pesa mais. O resíduo é aplicado em número absoluto e igual no cenário e na base, então tende a afetar mais o nível do que a diferença entre os dois.

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

| País | ONU Zero migration | motor (migração=0) | dif. relativa |
|---|---|---|---|
| NGA | 427,445 | 419,974 | -1.75% |
| ETH | 293,505 | 291,929 | -0.54% |
| COD | 337,903 | 332,352 | -1.64% |
| VNM | 106,524 | 106,091 | -0.41% |
| IND | 1,711,822 | 1,703,835 | -0.47% |
| IDN | 323,528 | 322,215 | -0.41% |
| IRN | 96,326 | 96,275 | -0.05% |
| SAU | 45,032 | 45,455 | +0.94% |
| MAR | 48,098 | 47,837 | -0.54% |
| EGY | 192,001 | 191,500 | -0.26% |
| THA | 50,380 | 50,480 | +0.20% |
| MEX | 153,009 | 152,549 | -0.30% |
| POL | 26,988 | 26,794 | -0.72% |
| BRA | 200,273 | 199,652 | -0.31% |
| USA | 310,120 | 312,565 | +0.79% |
| CHN | 964,226 | 962,816 | -0.15% |
| FRA | 58,376 | 58,641 | +0.45% |
| ARG | 45,272 | 45,205 | -0.15% |
| CHL | 16,375 | 16,426 | +0.31% |
| SWE | 8,954 | 9,038 | +0.94% |
| GBR | 58,858 | 59,467 | +1.03% |
| AUS | 25,535 | 25,811 | +1.08% |
| ZAF | 73,993 | 73,929 | -0.09% |
| JPN | 77,750 | 78,127 | +0.48% |
| DEU | 60,931 | 61,205 | +0.45% |
| ITA | 37,827 | 38,000 | +0.46% |
| KOR | 30,255 | 30,359 | +0.34% |
| RUS | 105,684 | 106,053 | +0.35% |

**Mediana do desvio absoluto: 0.45%; máximo: 1.75%.**

## V5 — TFR→2,1 (rampa 25 anos), sem migração: motor de coorte vs P_eq do projeto

O P_eq atual (narayama.live) usa um método mais simples (escala de nascimentos); aqui comparamos os dois métodos. Esperam-se diferenças pequenas, não nulas.

| País | P_eq do projeto (mi) | motor (mi) | dif. relativa |
|---|---|---|---|
| NGA | 397.3 | 387.0 | -2.59% |
| ETH | 279.2 | 274.5 | -1.69% |
| COD | 259.9 | 246.6 | -5.13% |
| VNM | 116.5 | 118.5 | +1.70% |
| IND | 1,870.0 | 1,893.3 | +1.25% |
| IDN | 348.2 | 351.4 | +0.91% |
| IRN | 107.2 | 109.3 | +1.96% |
| SAU | 48.0 | 48.8 | +1.61% |
| MAR | 51.5 | 51.9 | +0.71% |
| EGY | 191.7 | 190.0 | -0.86% |
| THA | 59.6 | 62.2 | +4.36% |
| MEX | 169.3 | 173.5 | +2.48% |
| POL | 31.1 | 31.8 | +2.25% |
| BRA | 226.8 | 231.8 | +2.23% |
| USA | 342.3 | 351.8 | +2.78% |
| CHN | 1,153.6 | 1,200.4 | +4.05% |
| FRA | 64.1 | 65.6 | +2.33% |
| ARG | 51.3 | 52.5 | +2.48% |
| CHL | 19.6 | 20.3 | +3.61% |
| SWE | 10.0 | 10.4 | +3.34% |
| GBR | 66.2 | 68.5 | +3.46% |
| AUS | 28.1 | 28.9 | +2.79% |
| ZAF | 79.3 | 80.1 | +1.07% |
| JPN | 89.4 | 92.4 | +3.38% |
| DEU | 68.1 | 69.9 | +2.57% |
| ITA | 43.6 | 45.3 | +3.72% |
| KOR | 36.8 | 38.4 | +4.44% |
| RUS | 119.6 | 123.4 | +3.22% |

**Mediana do desvio absoluto: 2.52%; máximo: 5.13%.**

**Leitura:** o motor de coorte dá populações maiores que o método antigo na maioria dos países (e menores em NGA, COD, ETH, EGY). Hipótese não testada isoladamente: o método antigo escala o total de nascimentos sem modelar a estrutura etária das mulheres (efeito de eco de coortes grandes ou pequenas) e mantém os óbitos fixos. Se a diferença importar para o narayama.live, vale decidir se o P_eq público passa a usar este motor.
