# AINU–Narayama: Observatório de Sustentabilidade Intergeracional

Cálculo do Índice de Narayama Sistêmico (N*) para 28 economias.

Baseado na tese "Do Dilema de Narayama ao Oicoceno Civilizacional",
versão atual **v9.2** (2026-07-21) — consolida no corpo do documento
(Seção 9-A) tudo que antes ficava só nos registros técnicos deste
repositório: composição ponderada de perfis, Protocolo de
Falseabilidade quantitativo, normalização do N* por raiz quadrada e
P_2.1/P_eq/P_tendência. As fórmulas centrais vêm da v8.0, inalteradas
na v9.2 — ver `docs/definitions.md` para a citação exata de cada seção.

## Começar

### 1. Instalar dependências

```bash
pip install -r app/requirements.txt
```

### 2. Obter dados

```bash
python scripts/build_un_wpp_raw.py        # Pop_Base/Pop_Topo/Nasc/Mortes/TFR (UN WPP)
python scripts/build_migracao_raw.py      # proxy do ajuste migratório da falseabilidade (UN Migrant Stock)
python scripts/build_historico_raw.py     # série quinquenal 1990-2024 (UN WPP) — evolução do N*
python scripts/build_convergencia_raw.py  # P_2.1/P_eq (UN WPP, cenário Instant replacement) — Tabela Geracional
```

Os quatro scripts baixam da fonte oficial (com cache local em
`data/raw/_cache/`) e gravam em `data/raw/`. Já existe um workflow
agendado (`.github/workflows/atualizar_dados.yml`, mensal) que roda os
quatro automaticamente e abre um Pull Request se algo mudou — nunca
commita direto em `main` nem redesploya sozinho.

### 3. Rodar pipeline

```python
from src.data_pipeline import executar_pipeline_completo, executar_pipeline_historico
executar_pipeline_completo(2024)   # grava data/processed/n_index_2024.csv
executar_pipeline_historico()      # grava data/processed/n_index_historico.csv (quinquenal 1990-2024)
```

Cadeia de cálculo completa (ver `docs/definitions.md` para o
detalhamento de cada etapa):

1. **NGII_Bruto** = (Pop_Base/Pop_Topo) × (Nascimentos/Mortes), com
   Pop_Base/Pop_Topo por país como a composição ponderada de perfis da
   Seção 5.2 (não um perfil único — `src.config.COMPOSICAO_PERFIL_POR_PAIS`).
2. **NGII_Puro** = NGII_Bruto depurado pelo Protocolo de Falseabilidade
   quantitativo (4 ajustes multiplicativos, Anexo 9 v9.1 —
   `src.falseability.aplicar_falseabilidade_quantitativa`).
3. **N_Base** = NGII_Puro × Fator_Geracional.
4. **N\*** = raiz quadrada do N_Base (normalização, decisão de
   2026-07-09 — `src.indices.normalizar_n_base`).
5. **Zona** = uma das 5 zonas da Seção 9-A.3/9-A.7 (PEC, Tensão
   Acelerada, PEA, Tensão Populacional, PEEC —
   `src.indices.classificar_zona_5`).

`Fator_Alocativo`/farol institucional continuam pendentes (Fase 2b):
dependem de National Transfer Accounts, sem fonte pública estruturada
pros 28 países — ver `docs/definitions.md`, seção 5.

### 4. Rodar website

Duas plataformas separadas (ver docs/definitions.md):

```bash
# ainu.systems — restrita, dados detalhados dos 28 países + Tabela Geracional
streamlit run app/ainu_systems/app.py
```
Acesse: http://localhost:8501

```bash
# narayama.live — pública, só os 7 países destaque
streamlit run app/narayama_live/app.py
```
Acesse: http://localhost:8502 (ver `.claude/launch.json` — as duas
apps têm porta fixa pra rodar simultaneamente sem conflito)

O `ainu.systems` aceita a variável de ambiente `AINU_SYSTEMS_PASSWORD`
para restringir o acesso (sem ela, fica aberto com aviso — Fase 1).

## Deploy

Hospedado no [Render](https://render.com) (não Streamlit Cloud — o
plano gratuito do Streamlit Cloud não aceita domínio próprio,
só subdomínio `*.streamlit.app`; o Render aceita, com 2 domínios
customizados grátis no plano Hobby, o que cobre os dois apps).

`render.yaml` na raiz já define os dois serviços. Passos manuais
(feitos uma vez, no painel do Render):

1. Conectar o repositório GitHub no Render (New → Blueprint → aponta
   pro repositório) — ele lê o `render.yaml` e cria os dois serviços
   automaticamente.
2. Em **ainu-systems → Environment**, definir `AINU_SYSTEMS_PASSWORD`
   (o `render.yaml` já reserva a variável, mas o valor é secreto e
   não fica no repositório).
3. Em cada serviço → **Settings → Custom Domains**, adicionar
   `ainu.systems` (no serviço ainu-systems) e `narayama.live` (no
   serviço narayama-live). O Render mostra o registro DNS exato
   (A ou CNAME, depende do tipo de domínio) para criar no painel da
   Namecheap — seguir o que aparecer lá, os valores são específicos
   de cada serviço.

Depois disso, todo push para `main` redesploya os dois serviços
automaticamente — não precisa de workflow de deploy no GitHub
Actions. `.github/workflows/ci.yml` só roda os testes antes disso
(instala dependências, valida os 28 países, roda
`test_calculo_brasil.py` e checa a falseabilidade/normalização), como
checagem antes do push chegar ao Render.
`.github/workflows/atualizar_dados.yml` (mensal + manual) coleta dados
novos e abre PR se algo mudou (ver seção 2 acima) — também não
redesploya sozinho.

## Estrutura de Pastas
- `data/raw/` — Dados brutos (UN WPP, migração) — `_cache/` (gitignorado) guarda os downloads originais
- `data/processed/` — Dados calculados (N*, etc)
- `src/` — Código principal (cálculos)
- `scripts/` — Scripts de coleta de dados (reproduzíveis, usados pelo bot agendado)
- `app/ainu_systems/` — Website restrito (Streamlit)
- `app/narayama_live/` — Website público (Streamlit)
- `docs/` — Documentação técnica

## Estado atual (2026-07-21)

- ✅ Tese atualizada para **v9.2** (`V1_EcoPol_070726_v9_2.docx`,
  2026-07-21) — consolida no corpo do documento (Seção 9-A) tudo que
  antes só existia como registro técnico separado neste repositório.
  Citações de versão nos sites e no README atualizadas de v8.0 para
  v9.2 — ver `docs/definitions.md`, seção 10, para o detalhamento.
- ✅ Pipeline completo com dado real (UN WPP), 28 países, 5 zonas.
- ✅ Composição ponderada de perfis, Protocolo de Falseabilidade
  quantitativo e normalização do N* — as 3 mudanças metodológicas
  desta fase, documentadas em `docs/registro_mudancas_metodologicas_2026-07.docx`.
- ✅ Tabela Geracional (visualização em formato periódico), encabeçando
  os dois sites — 28 países no ainu.systems, 7 países destaque no
  narayama.live.
- ✅ P_2.1/P_eq (população de convergência e de equilíbrio, formalização
  do autor de 2026-07-16 — ver `docs/definitions.md`, seção 8-B) nos
  cards da Tabela Geracional. Corrigido em 2026-07-18 em duas etapas
  (auditoria do autor): (1) o cenário anterior, "Instant replacement
  zero migration" da UN WPP, mostrava aumento populacional pra países
  de TFR real baixíssima como China/Coreia do Sul — trocado por um
  cenário PROPOSTO de convergência linear em 25+25 anos (t_c=2049,
  t_c+25=2074), simulado sobre nascimentos/óbitos reais da UN WPP
  (variante "Zero migration") — fecha o item "T_2.1 gradual" que estava
  em aberto; (2) os cards comparavam "população hoje → P_eq", o que
  misturava inércia etária (que sozinha já faz a população crescer por
  décadas em países como o Brasil, mesmo sem mudança nenhuma) com o
  efeito da recuperação de fecundidade — corrigido pra comparar dois
  cenários no mesmo ano (`P_tendência (2074, sem mudança) → P_eq (2074,
  com recuperação)`), isolando o efeito da política.
- ✅ Seletor de idioma nos dois sites (2026-07-18, decisão do autor):
  barra superior, 9 idiomas — PT (padrão/fonte) + EN/ES/JA/KO/IT/FI/FR/ZH
  — ver `src/i18n.py`. Tradução PT→EN/ES/IT/FR feita com alta confiança;
  PT→JA/KO/FI/ZH feita com cuidado mas sem revisão nativa — recomendável
  revisão por falante nativo antes de divulgação ampla nesses 4 idiomas.
  Termos técnicos da tese (N*, PEC, PEEC, PEA, NGII, TFR, P_eq,
  P_tendência etc.) permanecem inalterados em todo idioma. Nomes de
  país/região traduzidos; códigos de "perfil" (ex.: A35/B40/C25) já são
  alfanuméricos, sem tradução.
- ✅ Bot agendado de coleta de dados (UN WPP + migração + série
  histórica + convergência), Fase 1.
- ✅ LICENSE (todos os direitos reservados) e legenda metodológica
  pública no narayama.live.
- ✅ Série histórica do N* (`n_index_historico.csv`), quinquenal
  1990-2024 — ponto de partida deliberadamente grosseiro, decisão do
  autor de 2026-07-15 ("quinquenal para começar e vamos refinando
  após validações"); migrar pra anual é só trocar
  `src.config.ANOS_ALVO_HISTORICO`, sem mudança de arquitetura.
- ⏳ Fator_Alocativo/NTA — sem fonte de dado real (gancho do convite ao
  Prof. Cássio Turra, Cedeplar/UFMG, National Transfer Accounts Project).
  ainda em decisão com o autor.

## Próximas Fases
- Fase 2b: Fator_Alocativo real (NTA) + Versão Expandida com
  escolaridade real (UNESCO/World Bank) — instruções em
  docs/definitions.md, seção 9
- Fase 3: CHR + NIH
- Fase 4: EIS + IES
- Fase 5: IVAT e simulações OLG
- Fase 6: Agentes computacionais

## Referências
- Tese v9.2 (consolidada; fórmulas centrais de v8.0): `docs/`
- UN WPP: https://population.un.org/wpp/
- UN International Migrant Stock: https://www.un.org/development/desa/pd/content/international-migrant-stock
- Streamlit: https://docs.streamlit.io/

## Licença

Este projeto está em fase de prototipagem e construção metodológica
(implementação computacional de uma tese de doutorado ainda em
andamento). Todos os direitos são reservados — ver `LICENSE`. Uso,
adaptação ou colaboração acadêmica requerem autorização prévia do
autor.

---
Criado: 29 de junho de 2026
Última atualização: 15 de julho de 2026
