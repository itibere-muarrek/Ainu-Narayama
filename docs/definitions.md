# Definições Técnicas — AINU-Narayama (v8.0)

## 1. Introdução

Este documento é a receita técnica exata do projeto AINU-Narayama: contém as
fórmulas matemáticas usadas no cálculo do Índice de Narayama Sistêmico (N*) e
seus componentes, conforme definidos na tese de doutorado "Do Dilema de
Narayama ao Oicoceno Civilizacional" (`V1_EcoPol_062426_v8.0.docx`). Um único
exemplo (Brasil, dados reais da UN WPP 2024) percorre as seções 2 a 5 para
mostrar a mecânica completa do cálculo.

## 2. N* (Índice de Narayama Sistêmico)

```
N*(i,t) = NGII_puro(i,t) × Fator_Geracional(i,t)
```

Interpretação: capacidade de renovação geracional projetada ao final do
próximo ciclo de 25 anos.

Exemplo (Brasil, dados reais 2024):

- NGII_puro = 3,150
- Fator_Geracional = 0,691
- N* = 3,150 × 0,691 = **2,178** (zona "Expansão Forte" — ver nota da seção 3
  sobre o efeito de `Pop_Topo` pequeno em populações jovens, e a seção 8
  sobre a ausência de normalização na tese)

## 3. NGII_puro (Potência Geracional — Pilar 1)

```
NGII_puro = (Pop_Base / Pop_Topo) × (Nascimentos / Mortes)
```

Onde:

- Pop_Base = população da coorte formadora. Faixa etária por perfil
  (Tabela 14): **0–16** (A), **0–18** (B), **0–21** (C), **0–23** (D), **0–25** (E).
- Pop_Topo = população da coorte legatária/dependente. Faixa etária
  por perfil (Tabela 14): **44+** (A), **55+** (B), **60+** (C), **62+** (D), **65+** (E).
- Nascimentos = nascimentos no ano
- Mortes = mortes no ano

Interpretação: potência reprodutiva do país no momento atual.

Exemplo (Brasil — Perfil C, dados reais UN WPP 2024):

- Pop_Base (0–21) = 62,70 milhões
- Pop_Topo (60+) = 34,16 milhões
- Nascimentos = 2,57 milhões
- Mortes = 1,50 milhões
- NGII_puro = (62,70/34,16) × (2,57/1,50) = 1,835 × 1,715 = **3,150**

> **Decisão vigente** (atualizada em 2026-07-03): a tese define o NGII_puro
> de duas formas que não foram reconciliadas no texto — a Seção V.III
> (resumida) e o Anexo 1 (A1.2, "Formalização Matemática do Modelo",
> a seção mais formal) usam a fórmula de **2 componentes** acima, sem
> escolaridade; o Capítulo 5 (capítulo dedicado ao Pilar 1) usa uma
> versão de 3 componentes com um fator adicional de escolaridade. Como
> o Anexo 1 é a especificação formal e não inclui escolaridade, este
> projeto adotou a versão de 2 componentes (decisão de 2026-07-02).
>
> Pop_Base/Pop_Topo usam as faixas por perfil da **Tabela 14** (5 níveis —
> decisão de 2026-07-03, calibração país-a-país solicitada pelo usuário
> após o deploy inicial), não mais a Seção V.III (2 níveis, usada até
> 2026-07-02 — ver `FAIXAS_ETARIAS_POR_PERFIL_V3` em `src/config.py`,
> mantida como referência histórica). `Pop_Topo` continua sendo a
> coorte **idosa/legatária**, não provedora.
>
> A Tabela 14 **reduz, mas não elimina**, a inflação do NGII_puro em
> países jovens/alta fecundidade: RD Congo caiu de N*>41 (Seção V.III)
> para N*≈16 (Tabela 14); Arábia Saudita, Egito e Etiópia ainda ficam
> acima de N*=9. Isso é esperado — nenhuma das duas faixas etárias da
> tese resolve a ausência de normalização do N_Base (seção 8). Ver
> `FAIXAS_ETARIAS_POR_PERFIL_TABELA14` em `src/config.py`.

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
> coorte) usados pelo autor, que não são publicados no texto. Ver
> `test_calculo_brasil.py` na raiz do projeto para o cálculo com dados
> reais da UN WPP (N* = 2,334 — não comparável a nenhum dos quatro
> valores acima, ver seção 8 sobre a ausência de normalização).

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

## 8. Nota sobre a ausência de normalização do N*

A tese não especifica, em nenhuma seção (incluindo o Anexo 1, "Formalização
Matemática do Modelo" — a seção mais formal), nenhum passo de normalização,
limitação ou escala para o N_Base. A fórmula é publicada exatamente como:

```
N*(i,t) = N_Base(i,t) = NGII_puro(i,t) × Fator_Geracional(i,t)
```

sem divisão por constante de referência, sem raiz/log, sem limitar a uma
faixa (ex.: 0-2). As tabelas de interpretação (Tabela 4/Anexo 8, seção 7)
**presumem implicitamente** que N* fica numa faixa próxima de 1 — mas isso
não é garantido pela fórmula: para países jovens/alta fecundidade, onde
`Pop_Topo` é pequeno frente a `Pop_Base`, o NGII_puro cresce sem limite
matemático (ex.: com os cortes da Tabela 14 — seção 3 —, RD Congo, Arábia
Saudita, Egito e Etiópia produzem N* entre 9 e 16 com dados reais; com os
cortes da Seção V.III, usados até 2026-07-02, esses valores chegavam a
41 — ver `src/data_pipeline.py`). Isso é uma lacuna real do modelo
publicado, não um erro de implementação deste projeto: nenhuma das duas
faixas etárias que a tese oferece elimina o problema, só muda a magnitude.

Um documento de simulação de terceiros (produzido com ChatGPT/Grok, trazido
ao projeto em 2026-07-01) alegava uma "normalização para escala 0-2", mas a
verificação numérica linha a linha mostrou que o valor de "N*" publicado
nesse documento era, na prática, uma cópia do Fator_Alocativo estimado — não
uma normalização real do N_Base. Não há, portanto, nenhuma fonte confiável
(nem a tese, nem o documento externo) que defina como conter esses valores.

## 9. Roadmap Fase 2b — Versão Expandida (escolaridade)

Confirmado em 2026-07-02, a partir de um documento de simulação de terceiros
(ChatGPT/Grok, validado com pesquisadores) que — apesar de ter números não
reproduzíveis (ver seção 8) — trouxe uma clarificação metodológica útil sobre
a existência de **duas versões complementares** do N*, ambas legítimas:

- **Versão Básica (N\*\_Base)** — a que este projeto implementa hoje como
  indicador central (`calcular_ngii_puro`, 2 componentes, seção 3).
- **Versão Expandida (N\*\_Expandido)** — adiciona um terceiro fator de
  qualidade educacional, reservada para "análises de sensibilidade e estudos
  complementares" (não substitui a Básica).

Quando uma fonte real de escolaridade for integrada (candidatas: UNESCO
Institute for Statistics, World Bank Education Statistics — nenhuma delas
integrada ainda), a Versão Expandida deve ser implementada assim:

**1. Fórmula** (a acrescentar em `src/indices.py`, função nova, não alterar
`calcular_ngii_puro`):
```
NGII_puro_expandido = NGII_puro × (Taxa_Escolaridade_Efetiva_0-25 / Taxa_Escolaridade_Esperada)
N*_Expandido = NGII_puro_expandido × Fator_Geracional
```
Sugestão de assinatura:
```python
def calcular_ngii_puro_expandido(ngii_puro: float, taxa_escolaridade_efetiva: float, taxa_escolaridade_esperada: float) -> Optional[float]
```
(recebe o `ngii_puro` já calculado pela versão básica, não recalcula
Pop_Base/Pop_Topo/Nasc/Mort — evita duplicação de lógica.)

**2. Pipeline** (`src/data_pipeline.py`): adicionar colunas
`ngii_puro_expandido` e `n_base_expandido` **ao lado** de `ngii_puro` e
`n_base` no CSV de saída — não substituir. `executar_pipeline_completo()`
já está estruturado para adicionar colunas opcionais sem quebrar o schema
existente.

**3. Fonte de dados**: precisa de uma coluna `taxa_escolaridade` por país/ano
em `data/raw/` — provavelmente um novo arquivo (ex.: `data/raw/escolaridade.csv`)
com o mesmo padrão de `carregar_dados_un`/`carregar_dados_oecd` em
`src/data_loader.py` (função nova `carregar_dados_escolaridade`, mesma
convenção de retorno vazio + mensagem clara se o arquivo não existir).

**4. Apps**: `ainu.systems` (detalhado) deve mostrar as duas versões lado a
lado quando disponíveis; `narayama.live` (minimalista) continua mostrando só
a Versão Básica, consistente com o documento de terceiros ("a tese utiliza
prioritariamente a versão básica... reservando a expandida para... estudos
complementares").

**5. Não bloqueante**: esta fase não impede o funcionamento atual dos sites
— a Versão Básica já é o indicador central segundo a própria clarificação
metodológica trazida pelo usuário.

## 10. Referências

- Tese v8.0, `V1_EcoPol_062426_v8.0.docx`:
  - Seção V.II — Fórmula principal do N*
  - Seção V.III — Fator_Geracional (adotada); faixas etárias de Pop_Base/Pop_Topo
    por perfil, 2 níveis (usadas até 2026-07-02, não mais adotadas — ver seção 3);
    fórmula resumida (2 componentes) do NGII_puro (adotada, ver seção 3)
  - Seção V.III-bis — Fator_Alocativo e Farol Institucional
  - Capítulo 3 (3.2) — Limiares PEEC-PEA-PEC (convenção alternativa, não adotada)
  - Capítulo 5 — NGII_puro, versão alternativa de 3 componentes com
    escolaridade (não adotada — ver seção 3)
  - Anexo 1 (A1.2) — Formalização Matemática do Modelo; confirma a fórmula
    de 2 componentes do NGII_puro e a ausência de normalização (seção 8)
  - Tabela 4 / Anexo 8 — Zonas críticas do N* (convenção adotada)
  - Tabela 14 — Faixas etárias por Perfil Estrutural, 5 níveis (adotada em
    2026-07-03 — ver seção 3)
  - Anexo 9 — Protocolo de Falseabilidade (7 testes)
- Documento de terceiros "Aqui está a simulação completa atualizada com os 7
  países destaque..." (ChatGPT/Grok, validado com pesquisadores, trazido em
  2026-07-01/02): números não reproduzíveis (seção 8), mas útil para a
  clarificação metodológica da seção 9 (Versão Básica vs. Expandida)
