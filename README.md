# AINU–Narayama: Observatório de Sustentabilidade Intergeracional

Cálculo do Índice de Narayama Sistêmico (N*) para 28 economias.

Baseado na tese "Do Dilema de Narayama ao Oicoceno Civilizacional" v8.0.

## Começar

### 1. Instalar dependências

```bash
pip install -r app/requirements.txt
```

### 2. Baixar dados
- UN WPP: https://population.un.org/wpp/ → salvar em data/raw/
- OECD: https://stats.oecd.org/ → salvar em data/raw/

### 3. Rodar pipeline

```python
from src.data_pipeline import executar_pipeline_completo
executar_pipeline_completo(2024)  # grava data/processed/n_index_2024.csv
```

Fase 2a (atual): usa só UN World Population Prospects (já commitado em
`data/raw/un_wpp.csv`, real, 28 países). Calcula NGII_puro e
Fator_Geracional (fórmula de 2 componentes, Anexo 1 — ver
docs/definitions.md). Ainda não calcula Fator_Alocativo/farol nem a
Versão Expandida com escolaridade (Fase 2b, ver docs/definitions.md
seção 9 — instruções já preparadas pra quando integrarmos essas fontes).

O Protocolo de Falseabilidade (`src/falseability.py`, 7 testes) existe
mas ainda não está plugado no pipeline automático — precisa de dados
históricos/série longa que a Fase 2a não cobre.

### 4. Rodar website

Duas plataformas separadas (ver docs/definitions.md):

```bash
# ainu.systems — restrita, dados detalhados dos 28 países
streamlit run app/ainu_systems/app.py
```
Acesse: http://localhost:8501

```bash
# narayama.live — pública, só os 7 países destaque
streamlit run app/narayama_live/app.py
```
Acesse: http://localhost:8501 (ou a porta seguinte livre, se as duas
estiverem rodando ao mesmo tempo)

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
(instala dependências, valida os 28 países e roda
`test_calculo_brasil.py`), como checagem antes do push chegar ao Render.

## Estrutura de Pastas
- `data/raw/` — Dados brutos (UN, OECD)
- `data/processed/` — Dados calculados (N*, etc)
- `src/` — Código principal (cálculos)
- `app/ainu_systems/` — Website restrito (Streamlit)
- `app/narayama_live/` — Website público (Streamlit)
- `docs/` — Documentação técnica

## Próximas Fases
- Fase 2a: ✅ pipeline UN WPP, N* (Versão Básica) pros 28 países
- Fase 2b: Fator_Alocativo real (NTA/OECD) + Versão Expandida com
  escolaridade real (UNESCO/World Bank) — instruções em
  docs/definitions.md, seção 9
- Fase 3: CHR + NIH
- Fase 4: EIS + IES
- Fase 5: IVAT e simulações OLG
- Fase 6: Agentes computacionais

## Referências
- Tese v8.0: /docs/
- UN WPP: https://population.un.org/wpp/
- OECD SOCX: https://stats.oecd.org/
- Streamlit: https://docs.streamlit.io/

---
Criado: 29 de junho de 2026
Versão: 1.0 (MVP)
