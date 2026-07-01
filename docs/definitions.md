# Definições Técnicas — AINU-Narayama (v8.0)

## 1. Introdução

Este documento é a receita técnica exata do projeto AINU-Narayama: contém as
fórmulas matemáticas usadas no cálculo do Índice de Narayama Sistêmico (N*) e
seus componentes, conforme definidos na tese de doutorado "Do Dilema de
Narayama ao Oicoceno Civilizacional" (`V1_EcoPol_062426_v8.0.docx`). Um único
exemplo ilustrativo (Brasil, valores fictícios) percorre as seções 2 a 5 para
mostrar a mecânica completa do cálculo.

## 2. N* (Índice de Narayama Sistêmico)

```
N*(i,t) = NGII_puro(i,t) × Fator_Geracional(i,t)
```

Interpretação: capacidade de renovação geracional projetada ao final do
próximo ciclo de 25 anos.

Exemplo (Brasil, ilustrativo):

- NGII_puro = 0,88
- Fator_Geracional = 0,67
- N* = 0,88 × 0,67 = **0,59**

## 3. NGII_puro (Potência Geracional — Pilar 1)

```
NGII_puro = (Pop_Base / Pop_Topo) × (Nascimentos / Mortes) × (Taxa_Escolaridade_0-25 / Taxa_Esperada)
```

Onde:

- Pop_Base = população 0–25 anos ("coortes futuras")
- Pop_Topo = população 25–65 anos ("provedores atuais" — **não** é a coorte idosa)
- Nascimentos = nascimentos no ano
- Mortes = mortes no ano
- Taxa_Escolaridade_0-25 = taxa observada de educação completa (CHR + educação formal) na coorte 0-25
- Taxa_Esperada = taxa de escolaridade de referência para o perfil/contexto do país

Interpretação: potência reprodutiva do país no momento atual, ajustada pela
qualidade da formação da coorte que vai substituir os provedores de hoje.

Exemplo (Brasil, ilustrativo):

- Pop_Base ≈ 65 milhões
- Pop_Topo ≈ 110 milhões
- Nascimentos ≈ 2,7 milhões
- Mortes ≈ 1,6 milhões
- Taxa_Escolaridade_0-25 ≈ 0,75
- Taxa_Esperada ≈ 0,85
- NGII_puro = (65/110) × (2,7/1,6) × (0,75/0,85) = 0,591 × 1,688 × 0,882 = **0,88**

> Esta é a fórmula de 3 componentes do Capítulo 5 da tese (a que inclui o
> ajuste por escolaridade). A tese também apresenta, na Seção V.III, uma
> versão resumida de 2 componentes com `Pop_Topo` = coorte idosa (55+/61+) em
> vez de provedora — as duas versões não foram reconciliadas no texto. Este
> projeto usa a do Capítulo 5.

Implementado em [`calcular_ngii_puro`](../src/indices.py).

## 4. Fator_Geracional

```
Fator_Geracional(i,t) = TFR(i,t) / TFR(i,t-25)
```

Onde:

- TFR(i,t) = Taxa de Fecundidade Total no ano corrente
- TFR(i,t-25) = Taxa de Fecundidade Total 25 anos antes

Interpretação: direção da trajetória reprodutiva (melhora ou piora frente à
geração anterior).

Valores:

- \> 1,0: melhora (fecundidade aumentou)
- = 1,0: estável (fecundidade igual)
- < 1,0: deterioração (fecundidade caiu)

Exemplo (Brasil, ilustrativo):

- TFR ano corrente = 1,60
- TFR 25 anos antes = 2,40
- Fator_Geracional = 1,60 / 2,40 = **0,67** (deterioração)

Implementado em [`calcular_fator_geracional`](../src/indices.py).

## 5. Fator_Alocativo e Farol Institucional

```
Fator_Alocativo = NTA(0-25) / NTA(65+)
```

Onde:

- NTA(0-25) = transferências líquidas para a coorte 0-25 (educação + saúde infantojuvenil + transferências privadas de famílias para filhos)
- NTA(65+) = transferências líquidas para a coorte 65+ (previdência + saúde geriátrica + transferências privadas de filhos para pais idosos)

Interpretação: a que geração a sociedade aloca mais recursos. **Não** é
componente do N_Base — é reportado separadamente como farol institucional.

Farol:

- `(+)` se Fator_Alocativo > 1,05 → investe mais no futuro
- `(n)` se 0,95 ≤ Fator_Alocativo ≤ 1,05 → equilíbrio
- `(−)` se Fator_Alocativo < 0,95 → investe mais no passado (gerontocracia)

Exemplo (Brasil, ilustrativo):

- NTA(0-25) = 11,7% do PIB
- NTA(65+) = 15% do PIB
- Fator_Alocativo = 11,7 / 15 = 0,78 → Farol **(−)**

Notação final publicada pela tese: `N*(i,t) = valor_numérico⁺/ⁿ/⁻` (ex.:
"Brasil 2024: N* = 0,72(-)").

> **Nota**: a tese publica **quatro valores diferentes** de N* para o
> Brasil 2024 em pontos distintos do texto, sem reconciliá-los: 0,45
> (Tabela 3, Seção 3.2), ~0,605 (implícito no Anexo 8), 0,695 (Anexo
> 12) e 0,72 (aqui, V.III-bis). Nenhum é reproduzível a partir das
> fórmulas deste documento sem os dados brutos exatos (população por
> coorte, escolaridade) usados pelo autor, que não são publicados no
> texto. Ver `test_calculo_brasil.py` na raiz do projeto para uma
> tentativa de validação com dados estimados e a divergência
> resultante.

Implementado em [`calcular_fator_alocativo`](../src/indices.py) e
[`classificar_farol_alocativo`](../src/indices.py).

## 6. Protocolo de Falseabilidade (resumo)

Antes de aceitar um NGII_Bruto como válido, 7 testes (Anexo 9) o "validam"
para obter o NGII_Puro, removendo distorções que mascaram a real trajetória
de sustentabilidade intergeracional:

```
NGII_Bruto -> Protocolo de Falseabilidade (7 Testes) -> NGII_Puro -> N*
```

1. **Migração**: o NGII permanece sustentável quando os fluxos migratórios são removidos? Diferença > 12–15% indica dependência estrutural da imigração.
2. **Estrutura Assistencial**: o crescimento populacional gera novos provedores ou novos dependentes? Se a base provedora (25-65) não cresce proporcionalmente, o NGII é ajustado para baixo.
3. **Conjuntura**: a deterioração já existia antes de um evento disruptivo (guerra, pandemia, crise)? Se antecede o evento em mais de 10 anos, o colapso é estrutural, não conjuntural.
4. **Natalismo Temporário**: um aumento de TFR persiste além de 10 anos após o fim de uma política natalista (bônus, subsídio, programa eleitoral)? Só mudanças persistentes contam.
5. **Inércia Etária**: o crescimento em nascimentos absolutos vem de renovação real ou de uma geração numerosa gerando filhos mesmo com razão filhos/mãe < 1?
6. **Substituição Civilizacional**: a população é estável porque se reproduz, ou porque é substituída por novos grupos com estrutura demográfica diferente? Diferença entre TFR oficial e TFR nativa estimada > 0,25 sinaliza substituição.
7. **Resistência a Choques**: o N* sinaliza deterioração estrutural pelo menos 5–10 anos antes de um evento visível (validação empírica com casos históricos: Ucrânia, Rússia, Irã, Síria, Japão, Alemanha, Coreia do Sul)?

Implementado em [`aplicar_protocolo_falseabilidade`](../src/falseability.py).

## 7. Limiares Críticos (PEEC–PEA–PEC)

A tese define estes limiares de duas formas que se contradizem entre si (ver
Seção 3.2/Tabela 3 vs. Tabela 4/Anexo 8). Este projeto adota a convenção da
**Tabela 4 / Anexo 8** ("nova fórmula"), na qual N* alto é melhor:

| Zona | Faixa de N* | Farol |
|---|---|---|
| Expansão Forte | N* > 1,10 | +/n |
| Equilíbrio Sustentável (PEA) | 0,80 ≤ N* ≤ 1,10 | +/n |
| Tensão Acelerada | 0,50 ≤ N* < 0,80 | − |
| Colapso de Narayama (PEC) | N* < 0,50 | − |

**PEEC** (Ponto de Esgotamento por Excesso de Contingente) não é um limiar de
N* nesta convenção — é diagnosticado diretamente pela TFR: TFR > 2,8 indica
contingente juvenil crescendo mais rápido do que a capacidade do sistema de
educá-lo e integrá-lo economicamente (ex.: Nigéria, Etiópia).

Implementado em [`classificar_zona_n_base`](../src/indices.py).

## 8. Referências

- Tese v8.0, `V1_EcoPol_062426_v8.0.docx`:
  - Seção V.II — Fórmula principal do N*
  - Seção V.III — Fator_Geracional; versão resumida (2 componentes) do NGII_puro
  - Seção V.III-bis — Fator_Alocativo e Farol Institucional
  - Capítulo 3 (3.2) — Limiares PEEC-PEA-PEC (convenção alternativa, não adotada)
  - Capítulo 5 — NGII_puro (3 componentes, adotado neste projeto)
  - Tabela 4 / Anexo 8 — Zonas críticas do N* (convenção adotada)
  - Tabela 14 — Faixas etárias por Perfil Estrutural
  - Anexo 9 — Protocolo de Falseabilidade (7 testes)
