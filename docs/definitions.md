# Definições Técnicas — AINU-Narayama (v8.0)

## 1. Introdução

Este documento é a receita técnica exata do projeto AINU-Narayama: contém as
fórmulas matemáticas usadas no cálculo do Índice de Narayama Sistêmico (N*) e
seus componentes, conforme definidos na tese de doutorado "Do Dilema de
Narayama ao Oicoceno Civilizacional" (`V1_EcoPol_062426_v8.0.docx`). Um único
exemplo (Brasil, dados reais da UN WPP 2024 — exceto escolaridade, ainda
neutra/placeholder) percorre as seções 2 a 5 para mostrar a mecânica completa
do cálculo.

## 2. N* (Índice de Narayama Sistêmico)

```
N*(i,t) = NGII_puro(i,t) × Fator_Geracional(i,t)
```

Interpretação: capacidade de renovação geracional projetada ao final do
próximo ciclo de 25 anos.

Exemplo (Brasil, dados reais 2024):

- NGII_puro = 3,377
- Fator_Geracional = 0,691
- N* = 3,377 × 0,691 = **2,334** (zona "Expansão Forte" — ver nota da seção 3
  sobre o efeito de `Pop_Topo` pequeno em populações jovens)

## 3. NGII_puro (Potência Geracional — Pilar 1)

```
NGII_puro = (Pop_Base / Pop_Topo) × (Nascimentos / Mortes) × (Taxa_Escolaridade_0-25 / Taxa_Esperada)
```

Onde:

- Pop_Base = população da coorte formadora. Faixa etária por perfil
  (Seção V.III): **0–25 anos** para Perfis A/B, **0–21 anos** para
  Perfis C/D/E.
- Pop_Topo = população da coorte legatária/dependente. Faixa etária
  por perfil (Seção V.III): **55+** para Perfis A/B, **61+** para
  Perfis C/D/E.
- Nascimentos = nascimentos no ano
- Mortes = mortes no ano
- Taxa_Escolaridade_0-25 = taxa observada de educação completa (CHR + educação formal) na coorte 0-25
- Taxa_Esperada = taxa de escolaridade de referência para o perfil/contexto do país

Interpretação: potência reprodutiva do país no momento atual, ajustada pela
qualidade da formação da coorte que vai substituir os provedores de hoje.

Exemplo (Brasil — Perfil C, dados reais UN WPP 2024):

- Pop_Base (0–21) = 62,70 milhões
- Pop_Topo (61+) = 31,88 milhões
- Nascimentos = 2,57 milhões
- Mortes = 1,50 milhões
- Taxa_Escolaridade_0-25 = 1,0 (neutro — fonte real ainda não integrada, ver seção 8)
- Taxa_Esperada = 1,0 (idem)
- NGII_puro = (62,70/31,88) × (2,57/1,50) × (1,0/1,0) = 1,967 × 1,715 = **3,377**

> **Decisão híbrida** (confirmada em 2026-07-01): a tese define
> Pop_Base/Pop_Topo de duas formas que não foram reconciliadas no
> texto — o Capítulo 5 usa uma faixa fixa (0-25/25-65, "provedores
> atuais") para todos os perfis; a Seção V.III usa faixas que variam
> por perfil (0-25/55+ para A/B, **0-21/61+ para C/D/E**), com
> `Pop_Topo` = coorte **idosa**, não provedora. Este projeto adota as
> faixas por perfil da Seção V.III, mantendo o terceiro fator
> (escolaridade) do Capítulo 5. Isso **infla bastante o NGII_puro de
> países jovens/alta fecundidade** (ex.: RD Congo, Etiópia, Nigéria
> chegam a N* > 17 nesta fase), porque `Pop_Topo` (55+/61+) é um
> denominador muito pequeno nessas populações — um efeito mecânico da
> fórmula, não uma medida calibrada. Ver `FAIXAS_ETARIAS_POR_PERFIL_V3`
> em `src/config.py`.

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

Exemplo (Brasil, dados reais):

- TFR 2024 = 1,6143
- TFR 1999 = 2,3353
- Fator_Geracional = 1,6143 / 2,3353 = **0,691** (deterioração)

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
  - Seção V.III — Fator_Geracional; faixas etárias de Pop_Base/Pop_Topo por
    perfil (adotadas neste projeto — ver seção 3); versão resumida (2
    componentes) do NGII_puro (não adotada, ver seção 3)
  - Seção V.III-bis — Fator_Alocativo e Farol Institucional
  - Capítulo 3 (3.2) — Limiares PEEC-PEA-PEC (convenção alternativa, não adotada)
  - Capítulo 5 — NGII_puro, estrutura de 3 componentes com escolaridade
    (adotada neste projeto, combinada com as faixas etárias da Seção V.III)
  - Tabela 4 / Anexo 8 — Zonas críticas do N* (convenção adotada)
  - Tabela 14 — Faixas etárias por Perfil Estrutural (referência, não adotada — ver seção 3)
  - Anexo 9 — Protocolo de Falseabilidade (7 testes)
