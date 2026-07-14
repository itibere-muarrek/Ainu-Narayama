# AINU–Narayama: Observatório de Sustentabilidade Intergeracional

Cálculo do Índice de Narayama Sistêmico (N*) para 28 economias.

Baseado na tese "Do Dilema de Narayama ao Oicoceno Civilizacional". As
fórmulas centrais, a composição de perfis dos 28 países e os limiares
de zona vêm da **v8.0**; o Protocolo de Falseabilidade quantitativo e
a normalização do N* vêm da revisão **v9.1** (2026-07) — ver
`docs/definitions.md` para a citação exata de cada seção.

## Começar

### 1. Instalar dependências

```bash
pip install -r app/requirements.txt
```

### 2. Obter dados

```bash
python scripts/build_un_wpp_raw.py      # Pop_Base/Pop_Topo/Nasc/Mortes/TFR (UN WPP)
python scripts/build_migracao_raw.py    # proxy do ajuste migratório da falseabilidade (UN Migrant Stock)
```

Os dois scripts baixam da fonte oficial (com cache local em
`data/raw/_cache/`) e gravam em `data/raw/`. Já existe um workflow
agendado (`.github/workflows/atualizar_dados.yml`, mensal) que roda os
dois automaticamente e abre um Pull Request se algo mudou — nunca
commita direto em `main` nem redesploya sozinho.

### 3. Rodar pipeline

```python
from src.data_pipeline import executar_pipeline_completo
executar_pipeline_completo(2024)  # grava data/processed/n_index_2024.csv
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

## Estado atual (2026-07-13)

- ✅ Pipeline completo com dado real (UN WPP), 28 países, 5 zonas.
- ✅ Composição ponderada de perfis, Protocolo de Falseabilidade
  quantitativo e normalização do N* — as 3 mudanças metodológicas
  desta fase, documentadas em `docs/registro_mudancas_metodologicas_2026-07.docx`.
- ✅ Tabela Geracional (visualização em formato periódico, ainu.systems).
- ✅ Bot agendado de coleta de dados (UN WPP + migração), Fase 1.
- ⏳ Fator_Alocativo/NTA — sem fonte de dado real (gancho do convite ao
  Prof. Cássio Turra, Cedeplar/UFMG, National Transfer Accounts Project).
- ⏳ Série histórica (`n_index_historico.csv`) ainda não gerada.

## Próximas Fases
- Fase 2b: Fator_Alocativo real (NTA) + Versão Expandida com
  escolaridade real (UNESCO/World Bank) — instruções em
  docs/definitions.md, seção 9
- Fase 3: CHR + NIH
- Fase 4: EIS + IES
- Fase 5: IVAT e simulações OLG
- Fase 6: Agentes computacionais

## Referências
- Tese v8.0/v9.1: `docs/`
- UN WPP: https://population.un.org/wpp/
- UN International Migrant Stock: https://www.un.org/development/desa/pd/content/international-migrant-stock
- Streamlit: https://docs.streamlit.io/

---
Criado: 29 de junho de 2026
Última atualização: 13 de julho de 2026
