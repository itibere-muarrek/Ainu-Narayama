# Definições técnicas — AINU.Systems

Texto de referência do que o sistema calcula hoje. Cada fórmula aponta para o código que a implementa.
O texto de origem é a pesquisa independente "Do Dilema de Narayama ao Oicoceno Civilizacional" (V1_1, Anexo 9 — PQDF-N\*);
quando o código e o texto divergem, vale o texto, e a divergência é registrada na seção 9.

## 1. Cadeia de cálculo

```
NGII_Obs      = (Pop_Base / Pop_Topo) × (Nascimentos / Mortes)
N_Base        = NGII_Obs × Fator_Geracional
N*  (N*_Obs)  = √N_Base
```

O valor publicado é sempre o **N\*_Obs**: calculado direto das fontes oficiais, sem hipóteses contrafactuais
(PQDF-N\*, camada A). Os quatro ajustes do protocolo entram **só como cenários separados** (seção 6).

Exemplo (Brasil, 2024, UN WPP 2024): NGII_Obs = 2,9493; Fator_Geracional = 0,6913; N_Base = 2,0387; **N\*_Obs = 1,4278**.

Implementação: `src/indices.py` (`calcular_ngii_obs` calcula a razão do NGII, `calcular_n_base`, `normalizar_n_base`),
`src/data_pipeline.py` (`executar_pipeline_completo`, `executar_pipeline_historico`).

## 2. Entradas

- **UN World Population Prospects 2024**, variante média: população por idade simples, nascimentos, mortes, TFR
  (`scripts/build_un_wpp_raw.py`, saída em `data/raw/un_wpp*.csv`).
- **Pop_Base e Pop_Topo** vêm de uma composição ponderada de até 3 perfis estruturais A–E por país
  (`COMPOSICAO_PERFIL_POR_PAIS` em `src/config.py`; cortes etários por perfil: A 0–16/44+, B 0–18/55+, C 0–21/60+,
  D 0–23/62+, E 0–25/65+; média ponderada com arredondamento round-half-up).
- **Migração** (`scripts/build_migracao_raw.py`): estoque de migrantes da ONU, usado só como referência do cenário migratório.

## 3. NGII_Obs

Índice de Potência Geracional observado: razão entre a coorte formadora (Pop_Base) e a coorte ascendente (Pop_Topo),
multiplicada pela razão nascimentos/mortes. Sem ajuste algum.

## 4. Fator_Geracional

```
Fator_Geracional(i,t) = TFR(i,t) / TFR(i,t−25)
```

Acima de 1: a fecundidade melhorou frente à geração anterior; abaixo de 1: piorou. Implementado em `calcular_fator_geracional`.

## 5. Fator_Alocativo e farol institucional

```
Fator_Alocativo = NTA(0–25) / NTA(65+)       farol: (+) > 1,05 · (n) 0,95–1,05 · (−) < 0,95
```

Não faz parte do N_Base: é reportado à parte. **Pendente**: depende de National Transfer Accounts integradas aos 28 países;
até lá o farol aparece como "s/d" e nenhum valor provisório é publicado. Os perfis NTA de 11 países já levantados para o
Diretório (`data/diretorio/`) ainda não alimentam o Fator_Alocativo. Implementação pronta em `calcular_fator_alocativo`
e `classificar_farol_alocativo`.

## 6. PQDF-N\* (qualidade, decomposição e falseabilidade)

Camadas do protocolo (EcoPol V1_1, Anexo 9):

- **A — Observada:** NGII_Obs, N_Base e N\*_Obs, das fontes oficiais. É o valor publicado.
- **B — Corrigida:** correção documentada de completude registral. Não implementada (exige fonte e coeficiente por país).
- **C — Decomposta:** cenários separados para migração, inércia, políticas e conjuntura. Implementados como cenários
  unitários `N*_k = √(NGII_Obs × (1 − a_k) × Fator_Geracional)` (colunas `n_estrela_mig/ine/pol/sub`), com os valores de
  `AJUSTES_FALSEABILIDADE_POR_PAIS` em `src/config.py`. Esses valores são **dados pelo autor**, sem fonte automatizável;
  não são estimativas.
- **D — Estrutural:** exige evidência de nível A ou B. Não reportada.
- **E — Falsificável:** testes F1–F9. Execução e limites em [`testes_pqdf_n_estrela.md`](testes_pqdf_n_estrela.md).

Observação de método: no texto, o ajuste de sub-registro corrige o numerador (`B_corr = B_reg / c_B`); o código ainda o
trata como desconto multiplicativo no cenário `sub`. A diferença fica registrada até o ajuste ser reestimado.

## 7. Zonas

Classificação em 5 zonas, na escala do N\* (`classificar_zona_5` recebe o N_Base; a raiz é monotônica):

| Zona | N\* | N_Base |
|---|---|---|
| Colapso de Narayama (PEC) | < 0,71 | < 0,50 |
| Tensão Acelerada | 0,71–0,90 | 0,50–0,81 |
| Ponto de Equilíbrio Autossustentável (PEA) | 0,90–1,40 | 0,81–1,96 |
| Tensão Populacional | 1,40–2,00 | 1,96–4,00 |
| Saturação por Excesso de Contingente (PEEC) | ≥ 2,00 | ≥ 4,00 |

O PEEC também é diagnosticado por TFR > 2,8. **As zonas são provisórias** (teste F4, seção 6): a ordenação dos países é estável,
mas a zona de vários países muda com pequenas escolhas metodológicas.

## 8. Normalização, série histórica e convergência

- **Raiz quadrada** (decisão de 2026-07-09): preserva a ordenação, não usa constante arbitrária e mantém N_Base = 1 como ponto fixo.
- **Série histórica** (`n_index_historico.csv`): quinquenal, 1990–2024; para anual, trocar `ANOS_ALVO_HISTORICO` em `src/config.py`.
- **P_tendência e P_eq:** P_tendência é a população de 2074 seguindo a trajetória real da ONU; P_eq é um cenário **proposto** em que a TFR
  converge a 2,1 em rampa linear de 25 anos (2024–2049) e se mantém por mais 25 (2049–2074), variante "Zero migration". Os dois
  são comparados no mesmo ano. É cenário, não previsão.
- **Simulação por coorte:** `src/projecao.py`; método em [`simulacao.md`](simulacao.md), validação em [`validacao_projecao.md`](validacao_projecao.md).

## 9. Diferenças conhecidas entre código e texto

1. O N\*_Estrutural e a camada B do PQDF-N\* não estão implementados.
2. O ajuste de sub-registro (seção 6) e o proxy de migração (estoque de imigrantes, não nascimentos de mães imigrantes) diferem da definição do texto.
3. Testes F2, F3, F6, F7, F8 e F9 não foram executados; F5 é indeterminado. Ver o arquivo de testes.
4. O Fator_Alocativo e o farol não têm dado.
5. A composição de perfis é escolha do autor e fica fixa na simulação, mesmo quando a TFR muda muito.

## 10. Referências

- UN DESA, *World Population Prospects 2024* — population.un.org/wpp
- UN DESA, *International Migrant Stock 2024*
- Pesquisa independente "Do Dilema de Narayama ao Oicoceno Civilizacional" (V1_1), Anexo 9 (PQDF-N\*)
