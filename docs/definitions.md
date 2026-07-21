# Definições Técnicas — AINU-Narayama (v9.2)

## 1. Introdução

Este documento é a receita técnica exata do projeto AINU-Narayama: contém as
fórmulas matemáticas usadas no cálculo do Índice de Narayama Sistêmico (N*) e
seus componentes, conforme definidos na tese de doutorado "Do Dilema de
Narayama ao Oicoceno Civilizacional". Fonte atual: `V1_EcoPol_070726_v9_2.docx`
— versão consolidada que incorpora, no corpo do próprio documento (Seção
9-A.1 a 9-A.9), todas as correções e extensões antes registradas separadamente
nas revisões v9.0/v9.1 e nos registros técnicos deste repositório (composição
ponderada de perfis, Protocolo de Falseabilidade quantitativo, normalização
do N* por raiz quadrada, e P_2.1/P_eq/P_tendência — ver seção 10 abaixo para
a citação exata de cada seção). As fórmulas centrais e a estrutura das seções
1-8 vêm de `V1_EcoPol_062426_v8.0.docx`, inalteradas na v9.2. Um único exemplo
(Brasil, dados reais da UN WPP 2024) percorre as seções 2 a 5 para mostrar a
mecânica completa do cálculo.

## 2. N* (Índice de Narayama Sistêmico)

```
N*(i,t) = NGII_puro(i,t) × Fator_Geracional(i,t)
```

Interpretação: capacidade de renovação geracional projetada ao final do
próximo ciclo de 25 anos.

Exemplo (Brasil, dados reais 2024):

- NGII_puro = 2,949
- Fator_Geracional = 0,691
- N* = 2,949 × 0,691 = **2,039** (zona "Expansão Forte" — ver nota da seção 3
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

Essas faixas são por perfil-letra. **O corte efetivo de cada país** é a
média ponderada dessas faixas pela composição do país entre 2-3 perfis
adjacentes — ver a nota de 2026-07-04 abaixo e
[`COMPOSICAO_PERFIL_POR_PAIS`](../src/config.py) para a tabela completa
dos 28 países (não duplicada aqui para não ter uma segunda fonte que pode
ficar desatualizada).

Interpretação: potência reprodutiva do país no momento atual.

Exemplo (Brasil — composição 30% B / 40% C / 30% D, dados reais UN WPP 2024):

- Pop_Base (0–21) = 62,70 milhões
- Pop_Topo (59+) = 36,49 milhões
- Nascimentos = 2,57 milhões
- Mortes = 1,50 milhões
- NGII_puro = (62,70/36,49) × (2,57/1,50) = 1,718 × 1,717 = **2,949**

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
> para N*≈16 (Tabela 14, perfil único); Arábia Saudita, Egito e Etiópia
> ainda ficam acima de N*=9. Isso é esperado — nenhuma das duas faixas
> etárias da tese resolve a ausência de normalização do N_Base
> (seção 8). Ver `FAIXAS_ETARIAS_POR_PERFIL_TABELA14` em `src/config.py`.

> **Correção (2026-07-04): país não é um perfil único, é uma composição
> ponderada.** Até esta data, este projeto atribuía UM perfil (A-E) a
> cada país (ex.: "Brasil = Perfil C"). Isso estava errado: a **Seção
> 5.2** do docx v8.0 — verificada diretamente e confirmada país a país
> com o autor — classifica cada um dos 28 países como uma composição
> ponderada de 2-3 perfis adjacentes (ex.: Brasil = 30% B + 40% C + 30%
> D; Japão = 60% D + 40% E). Isso também corrige uma afirmação anterior,
> incorreta, de que nenhum país é Perfil E.
>
> A partir de 2026-07-04, `Pop_Base`/`Pop_Topo` de cada país são a média
> ponderada dos cortes por perfil (pesos = fração de composição),
> arredondada ao inteiro mais próximo (round-half-up — só afeta Irã,
> Arábia Saudita e Polônia, os únicos três países cuja média cai
> exatamente em ",5"). Exemplo do Brasil: `pop_base_max` =
> round(0,30×18 + 0,40×21 + 0,30×23) = round(20,7) = 21 (inalterado);
> `pop_topo_min` = round(0,30×55 + 0,40×60 + 0,30×62) = round(59,1) = 59
> (antes 60). Países de perfil puro (Chile, Suécia, Austrália — 100% C)
> não mudam. Japão é o primeiro país a efetivamente usar os cortes do
> Perfil E (antes um valor morto na tabela, nunca lido por nenhum país).
>
> Ver `COMPOSICAO_PERFIL_POR_PAIS` em `src/config.py` para a composição
> completa dos 28 países e `scripts/build_un_wpp_raw.py` para o script
> (novo, reprodutível) que reconstruiu `data/raw/un_wpp.csv` com os
> cortes recalibrados.

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

## 6. Protocolo de Falseabilidade

> **Atualização (2026-07-07): versão quantitativa, v9.0.** A tese v9.0
> (`V1_EcoPol_070726_v9.0.docx`) reescreveu por completo o Anexo 9. Os 7
> testes qualitativos da v8.0 (mantidos abaixo como "versão anterior")
> foram substituídos por uma fórmula fechada de 4 ajustes multiplicativos,
> calibrados país a país e aprovados pelo usuário com um pesquisador
> colaborador da Unicamp:
>
> ```
> NGII_Puro = NGII_Bruto × (1-migratorio) × (1-inercia) × (1-politicas) × (1-subregistro)
> ```
>
> Critério de aceitação da v9.0: redução total composta entre 25% e 45%.
> Os 4 ajustes, por país, estão em
> [`AJUSTES_FALSEABILIDADE_POR_PAIS`](../src/config.py); a fórmula está em
> [`aplicar_falseabilidade_quantitativa`](../src/falseability.py) e já
> alimenta o pipeline (`src/data_pipeline.py`) — deixou de ser lacuna.
>
> Exemplo (Brasil, 2024): NGII_Bruto = 2,9493 → ajustes
> (migratório 12%, inércia 15%, políticas 6%, sub-registro 4%) → NGII_Puro
> = 1,9908 (redução real de 32,5%).
>
> **Nota de correção**: a primeira versão da tabela de calibração que o
> usuário forneceu tinha os percentuais certos, mas o NGII_Puro final
> publicado batia com a soma simples dos 4 percentuais, não com a fórmula
> multiplicativa declarada no texto. A aritmética foi corrigida antes de
> incorporar aqui — os 28 países recalculados corretamente continuam
> dentro do critério de aceitação (25%-45%) da v9.0.
>
> **Automação parcial (2026-07-13)**: `scripts/build_migracao_raw.py`
> coleta automaticamente, via UN International Migrant Stock 2024, um
> **proxy** do ajuste migratório — % da população total que é imigrante
> (estoque), não "% de nascimentos de mães imigrantes nos últimos 10
> anos" (a definição exata acima). Grava em `data/raw/migracao_un.csv`;
> não substitui `AJUSTES_FALSEABILIDADE_POR_PAIS` automaticamente — usar
> esse dado pra recalibrar é decisão do usuário, não do script. Os
> ajustes de inércia demográfica e sub-registro/mortalidade seguem sem
> automação (IHME exige conta; políticas natalistas não são dado
> estruturado — ver `docs/infraestrutura.md`, seção 2.1).

### Versão anterior (v8.0, substituída) — 7 testes qualitativos

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

Mantido como referência histórica em
[`aplicar_protocolo_falseabilidade`](../src/falseability.py) — não é mais
a versão usada pelo pipeline.

## 7. Limiares Críticos (PEEC–PEA–PEC)

A tese define estes limiares de duas formas que se contradizem entre si (ver
Seção 3.2/Tabela 3 vs. Tabela 4/Anexo 8). Este projeto adota a convenção da
**Tabela 4 / Anexo 8** ("nova fórmula"), na qual N* alto é melhor. Desde
2026-07-09 (ver seção 8), o N* publicado é normalizado (`sqrt(N_Base)`) —
os limiares abaixo aparecem nas duas escalas:

| Zona | Faixa de N_Base (bruto) | Faixa de N* (normalizado) | Farol |
|---|---|---|---|
| Expansão Forte | N_Base > 1,10 | N* > 1,0488 | +/n |
| Equilíbrio Sustentável (PEA) | 0,80 ≤ N_Base ≤ 1,10 | 0,8944 ≤ N* ≤ 1,0488 | +/n |
| Tensão Acelerada | 0,50 ≤ N_Base < 0,80 | 0,7071 ≤ N* < 0,8944 | − |
| Colapso de Narayama (PEC) | N_Base < 0,50 | N* < 0,7071 | − |

As duas colunas classificam exatamente os mesmos países nas mesmas zonas —
a raiz quadrada é estritamente monotônica, então não muda nenhuma
classificação, só a régua usada pra lê-la. `classificar_zona_n_base`
continua operando sobre o N_Base bruto (menos superfície de código); os
limiares normalizados (`LIMIARES_SIMPLES_NORMALIZADOS` em `src/config.py`)
servem só pra colorir a tabela na escala exibida.

**PEEC** (Ponto de Esgotamento por Excesso de Contingente) não é um limiar de
N* nesta convenção — é diagnosticado diretamente pela TFR: TFR > 2,8 indica
contingente juvenil crescendo mais rápido do que a capacidade do sistema de
educá-lo e integrá-lo economicamente (ex.: Nigéria, Etiópia).

Implementado em [`classificar_zona_n_base`](../src/indices.py).

## 8. Normalização do N* (raiz quadrada, decisão de 2026-07-09)

A tese não especifica, em nenhuma seção (incluindo o Anexo 1, "Formalização
Matemática do Modelo" — a seção mais formal), nenhum passo de normalização,
limitação ou escala para o N_Base. A fórmula é publicada exatamente como:

```
N_Base(i,t) = NGII_puro(i,t) × Fator_Geracional(i,t)
```

sem divisão por constante de referência, sem raiz/log, sem limitar a uma
faixa. Mesmo após a composição ponderada de perfis (seção 3) e o Protocolo
de Falseabilidade quantitativo (seção 6, v9.0) — que juntos reduzem, mas
não eliminam, o problema —, RD Congo, Arábia Saudita, Etiópia, Egito e
Nigéria continuavam com N_Base entre ~6,6 e ~11,6, sem plausibilidade
física (o usuário observou, em 2026-07-06, que nenhum país deveria passar
de ~6 ou ficar abaixo de ~0,3).

**Três métodos foram comparados com os dados reais dos 28 países** antes de
decidir:

| Método | RD Congo (maior) | Coreia do Sul (menor) | Problema |
|---|---|---|---|
| Truncamento (`min(6, max(0.3, N_Base))`) | 6,00 | 0,30 | Empata 5 países no teto e 3 no piso — perde diferenciação real |
| Divisão pela mediana da amostra | 10,15 | 0,12 | Não limita nada — o problema original persiste |
| **Raiz quadrada** (`sqrt(N_Base)`) — escolhida | **3,41** | **0,37** | Nenhum — ver abaixo |

A raiz quadrada foi escolhida por preservar a ordenação total dos 28 países
(sem nenhum empate), não exigir nenhuma constante arbitrária, e manter
N_Base=1 como ponto fixo (`sqrt(1)=1`). **Diferente de outras lacunas
documentadas neste projeto, esta normalização está sendo formalizada pelo
próprio autor como parte da tese — não é uma extensão só do projeto.**

```
N*(i,t) = sqrt(N_Base(i,t))
```

Implementado em [`normalizar_n_base`](../src/indices.py). Os limiares de
zona recalculados na escala normalizada estão na seção 7. `N_Base` (bruto)
continua disponível ao lado de `N*` em `data/processed/n_index_2024.csv` e
na tabela do ainu.systems, para transparência.

Um documento de simulação de terceiros (produzido com ChatGPT/Grok, trazido
ao projeto em 2026-07-01) alegava uma "normalização para escala 0-2", mas a
verificação numérica linha a linha mostrou que o valor de "N*" publicado
nesse documento era, na prática, uma cópia do Fator_Alocativo estimado — não
uma normalização real do N_Base. Não influenciou a decisão acima.

### 8-A. Série histórica do N* (quinquenal, decisão de 2026-07-15)

O gráfico "Evolução do N*" do ainu.systems usa uma série **quinquenal**
(1990, 1995, 2000, ..., 2020, 2024 — último intervalo de só 4 anos pra manter
2024 como âncora, mesmo ano do snapshot em `n_index_2024.csv`), não anual.
Decisão explícita do autor: **"quinquenal para começar e vamos refinando
após validações"** — ponto de partida deliberadamente grosseiro, não uma
limitação técnica: a mesma cadeia de cálculo (NGII_Bruto → NGII_Puro →
N_Base → N*) roda pra cada ano independentemente, então passar pra anual no
futuro é só trocar a lista de anos em
[`ANOS_ALVO_HISTORICO`](../src/config.py) — nenhuma mudança de arquitetura,
script ou schema de arquivo é necessária.

Fonte: [`scripts/build_historico_raw.py`](../scripts/build_historico_raw.py)
(dados brutos, `data/raw/un_wpp_historico.csv`) e
[`executar_pipeline_historico`](../src/data_pipeline.py) (cálculo,
`data/processed/n_index_historico.csv`). O Protocolo de Falseabilidade
(seção 6) é aplicado com os mesmos ajustes de hoje (`AJUSTES_FALSEABILIDADE_POR_PAIS`,
por país, não por ano) retroativamente a cada ano da série — os ajustes não
têm calibração histórica própria, é uma simplificação consciente do mesmo
tipo já assumido para o Fator_Alocativo (seção 5).

### 8-B. P_2.1 e P_eq — população de convergência e de equilíbrio (2026-07-16)

Formalização original do autor (documento "tabela geracional -
formula.docx", 2026-07-16), incorporada à Tabela Geracional (seção
9-A.7) dos dois sites. Define três conceitos além do N*:

- **População Endógena, P_E(t)**: `P_E(t+1) = P_E(t) + B_E(t) - D_E(t)`
  — evolução da população só por nascimentos e óbitos, sem termo de
  migração.
- **P_2.1 (Estado de Convergência)**: `P_2.1 = P_E(t_c)`, onde `t_c`
  é o instante em que a TFR atinge 2,1 (nível de reposição) pela
  primeira vez. A população nesse momento, mas com a estrutura etária
  ainda não estabilizada.
- **P_eq (Estado de Equilíbrio)**: `P_eq = P_E(t_c + 25)` — a
  população ~1 geração depois de `t_c`, mantendo TFR=2,1 durante todo
  o período. O tamanho populacional sustentável real (a inércia
  etária já se dissipou).

Também define **P_obs(t) = P_E(t) + P_X(t)**, onde `P_X` é a
população decorrente de processos exógenos (migração). O Framework
Narayama (o índice em si) usa só `P_E`; o AINU (a infraestrutura
computacional) pode simular cenários sobre `P_X` sem alterar a
definição do indicador — separa mensuração de análise de cenários.

**Implementação v1 (2026-07-16, `t_c` = 2024, instantâneo) — abandonada**:
a primeira versão usava a variante oficial "Instant replacement zero
migration" da UN WPP 2024 Revision, que assume TFR=2,1 já a partir de
2024. Auditoria do autor em 2026-07-18 encontrou que essa premissa
produz números sem sentido pra países de fecundidade baixa persistente:
China e Coreia do Sul apareciam com `P_eq` **maior** que a população
atual, apesar de TFR real muito abaixo de 2,1 (China ~0,9-1,0; Coreia
~0,7) — o salto instantâneo ignora a trajetória real desses países.

**Tentativa 2 (mesma auditoria) — também abandonada**: usar direto a
trajetória real da ONU (variante "Zero migration", fecundidade "Medium"
+ migração zero, sem nenhum salto) pra achar o `t_c` real (ano em que a
TFR de cada país cruza 2,1). Resultado: **nenhum dos 20 países com TFR
hoje abaixo de 2,1 — dos 28 do projeto, incluindo os 7 destaque do
narayama.live — cruza TFR=2,1 até 2100**, o fim do horizonte de
projeção da ONU. O dado real e puro da ONU não cobre esse cenário pra
praticamente nenhum país do projeto.

**Implementação atual (v2, 2026-07-18) — cenário PROPOSTO de
recuperação em 25+25 anos**: decisão do autor. Em vez de um dado direto
da ONU (que não cobre o cenário) ou um salto instantâneo (irreal),
simula-se um cenário próprio: todo país — esteja hoje acima ou abaixo
de 2,1 — segue um plano de convergência **linear** até TFR=2,1 ao longo
de 25 anos (`t_c = 2049`), e depois mantém TFR=2,1 por mais 25 anos
(`t_c + 25 = 2074`). Convergir nos dois sentidos (não só recuperar quem
está abaixo de 2,1, mas também países hoje acima, como Nigéria) é
coerente com o enquadramento da tese: PEC (colapso, TFR baixa) e PEEC
(saturação, TFR alta) são os dois extremos, PEA (TFR ~2,1) é o meio — o
mesmo plano de convergência serve pros dois lados.

A única parte "proposta" (não um dado direto da ONU) é a trajetória de
TFR (`TFR_ramp(t)`, interpolação linear de `TFR_real(2024)` até 2,1 em
`t_c`, depois constante). Nascimentos e óbitos usados na simulação SÃO
reais — vêm da variante "Zero migration" da própria ONU (colunas
`Births`/`Deaths`/`TFR` anuais, presentes em
`WPP2024_Demographic_Indicators_OtherVariants.csv.gz`). Nascimentos são
escalados pela razão `TFR_ramp(t) / TFR_real(t)` a cada ano — a
aproximação padrão quando não se tem fecundidade específica por idade
(que este projeto não tem — exigiria tábua de mortalidade e fecundidade
por idade). Óbitos ficam com o valor real da ONU (não dependem do
cenário de fecundidade no curto/médio prazo). **Simplificação explícita**:
não é um modelo de coorte por idade, é uma escala do total de
nascimentos — mesmo nível de aproximação já usado em outras partes do
projeto (ex.: normalização do N* por raiz quadrada, seção 5.2). Ver
[`scripts/build_convergencia_raw.py`](../scripts/build_convergencia_raw.py).

**Limitação explícita, documentada nos cards da Tabela Geracional**: não
é uma previsão nem um dado direto da ONU — é um cenário proposto de
política de recuperação/convergência, simulado sobre componentes reais
da ONU (nascimentos, óbitos, TFR), não população inventada.

**Correção de interpretação — "o problema dos dois números" (mesma
auditoria, 2026-07-18)**: a v2 original comparava, nos cards,
"população hoje (2024) → P_eq (2074)". O autor identificou que essa
comparação mistura dois efeitos distintos e não deveria ser somada num
único número: a **inércia etária própria do país** (que sozinha já pode
fazer a população crescer por décadas, mesmo sem nenhuma mudança de
política — caso do Brasil: TFR real ~1,6, mas a população real da ONU
[variante "Zero migration", sem rampa nenhuma] cresce até ~2043 antes de
começar a cair, por causa da base grande de mulheres em idade fértil
herdada de décadas de fecundidade mais alta) e o **efeito do cenário de
recuperação proposto**. Comparar "hoje" com "daqui a 50 anos sob um
cenário ideal" confunde os dois — dá a impressão de que todo o ganho
populacional veio da política, quando parte (às vezes a maior parte, ver
Brasil) já aconteceria de qualquer forma.

Correção: introduzido **P_tendência**, a população no MESMO ano final
(`t_c + 25 = 2074`), mas seguindo a trajetória real da ONU sem nenhuma
rampa/política (variante "Zero migration" pura). Os cards agora mostram
`P_tendência → P_eq` — ambos no ano 2074, isolando o efeito da política
de recuperação da simples passagem do tempo. Coluna `p_tendencia` em
`data/raw/convergencia_un.csv`. Resultado, pós-correção: pra todo país
com TFR real hoje abaixo de 2,1 (a maioria dos 28, incluindo os 7
destaque do narayama.live), `P_eq > P_tendência` — a recuperação de
fecundidade dá uma população maior que não fazer nada; pra países hoje
acima de 2,1 (Nigéria, Etiópia, RD Congo...), `P_eq < P_tendência` — a
convergência PARA BAIXO até 2,1 reduz o crescimento que aconteceria sem
intervenção. Ambos os casos são esperados e coerentes com o
enquadramento PEC/PEEC/PEA da tese.

**Resolvido**: o item "T_2.1 gradual" que ficava em aberto desde
2026-07-16 — essa implementação (v2) já é o cenário gradual, só que como
convergência proposta por nós em 25 anos, não uma variante pronta da
ONU (nenhuma cobre esse caso, ver "Tentativa 2" acima). **Em aberto pra
uma iteração futura**: um modelo de coorte por idade completo
(fecundidade específica por idade + tábua de mortalidade), que
substituiria a aproximação por escala de nascimentos por algo mais
preciso — projeto bem maior, fora de escopo por ora.

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
  - Anexo 9 — Protocolo de Falseabilidade (7 testes, substituído — ver v9.0 abaixo)
- Tese v9.0, `V1_EcoPol_070726_v9.0.docx` (trazida em 2026-07-07):
  comparação estrutural completa contra a v8.0 confirmou que todas as
  fórmulas centrais, cortes etários e a composição dos 28 países (Seção
  5.2/Anexo 5) são idênticas entre as duas versões — a v9.0 não substitui
  a v8.0 como fonte geral. A única mudança material é:
  - Anexo 9 — Protocolo de Falseabilidade reescrito: fórmula quantitativa
    de 4 ajustes multiplicativos (adotada, ver seção 6), substituindo os
    7 testes qualitativos da v8.0
- Tese v9.2, `V1_EcoPol_070726_v9_2.docx` (trazida em 2026-07-21) —
  **fonte atual/consolidada**, substitui a citação separada de v8.0/v9.0/v9.1
  como "fonte geral": incorpora, na própria Seção 9-A (9-A.1 a 9-A.9), tudo
  que antes só existia como registro técnico neste repositório —
  - 9-A.1 — Composição ponderada de perfis (Seção 5.2, corrigida)
  - 9-A.2 — Protocolo de Falseabilidade quantitativo, calibração testada e
    aprovada com pesquisador da Unicamp (mesmo conteúdo da v9.0 acima, agora
    com a calibração final)
  - 9-A.3 — Normalização do N* via raiz quadrada (N\* = √N_Base), com os 5
    limiares refinados em 12/07/2026: PEC < 0,71; Tensão Acelerada
    0,71-0,90; PEA 0,90-1,40; Tensão Populacional 1,40-2,00; PEEC ≥ 2,00
    — mesmos valores usados em `src/config.py` (`LIMIARES_5_ZONAS_NORMALIZADOS`)
  - 9-A.9 — P_conv/P_eq/P_tendência: formaliza o cenário de recuperação em
    25+25 anos e a correção "problema dos dois números" (commit 696630d),
    com o mesmo conteúdo de docs/registro_correcao_p_eq_2026-07-18.docx
  - As fórmulas centrais (Seções 1-8 deste documento) permanecem inalteradas
    desde a v8.0 — a v9.2 não as reescreve, só consolida as extensões acima
    no corpo do texto em vez de mantê-las como adendo separado
- Documento de terceiros "Aqui está a simulação completa atualizada com os 7
  países destaque..." (ChatGPT/Grok, validado com pesquisadores, trazido em
  2026-07-01/02): números não reproduzíveis (seção 8), mas útil para a
  clarificação metodológica da seção 9 (Versão Básica vs. Expandida)
