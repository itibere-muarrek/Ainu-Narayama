# Testes F1–F9 do PQDF-N* — execução de 2026-11-03

> Sensibilidades de F4 e leitura de F5 definidas junto com a execução, não pré-registradas: valem como diagnóstico, não como confirmação nem refutação formal. Resultados de F1–F9 não executados constam como tal.

| Teste | Situação | Resultado |
|---|---|---|
| F1 Reprodutibilidade | executado | passa (dif. entre execuções 0.0e+00; recálculo independente × CSV 4.7e-05) |
| F4 Robustez classificatória | executado | falha em: cortes etários -1 ano; cenário migratorio (N*_mig); cenário inercia (N*_ine); cenário politicas (N*_pol); cenário subregistro (N*_sub) |
| F5 Migração e inércia | parcial | indeterminado (ver motivo) |
| F2 | não executado | Validade convergente: exige especificações pré-registradas e medidas demográficas externas definidas; não há registro prévio. |
| F3 | não executado | Valor incremental: exige variável-alvo e previsão fora da amostra com benchmarks (TFR, razão de dependência); não definidos. |
| F6 | não executado | Políticas e conjuntura: exige desenho de efeito causal (diferença-em-diferenças etc.) por política; não há estimativas. |
| F7 | não executado | NTAI/Farol: o Farol depende do Fator_Alocativo (NTA), ainda não integrado. |
| F8 | não executado | IES/EIS: o índice não está implementado neste repositório. |
| F9 | não executado | Replicação externa: precisa de equipe independente; não é executável pelo autor nem por este sistema. |

## F4 — sensibilidades

| Sensibilidade | Spearman | Concordância de zonas | Países que mudam de zona |
|---|---|---|---|
| cortes etários -1 ano | 0.999 | 71% | BRA, CHN, FRA, IRN, MAR, MEX, POL, ZAF |
| cortes etários +1 ano | 0.999 | 96% | THA |
| cenário migratorio (N*_mig) | 0.996 | 64% | BRA, CHN, FRA, GBR, IRN, MAR, MEX, POL, SWE, ZAF |
| cenário inercia (N*_ine) | 0.994 | 71% | BRA, CHN, FRA, IRN, MAR, MEX, POL, ZAF |
| cenário politicas (N*_pol) | 0.998 | 79% | BRA, CHN, FRA, IRN, MAR, MEX |
| cenário subregistro (N*_sub) | 0.996 | 79% | BRA, FRA, IRN, MAR, MEX, ZAF |

Decisão prevista pelo protocolo quando F4 falha: Publicar zonas como provisórias.

## F5 — cada ajuste isolado

| Ajuste | Países que mudam de zona | Redução mediana do N* |
|---|---|---|
| migratorio | 10 | 5.66% |
| inercia | 8 | 6.72% |
| politicas | 6 | 3.05% |
| subregistro | 6 | 3.56% |

Motivo da indeterminação: O limiar de 'extensas' não está definido e o teste de redundância da inércia exige o estimador do ajuste (modelo com e sem o tamanho da coorte reprodutiva), que o repositório não tem: os ajustes são valores dados pelo autor, não estimados.
