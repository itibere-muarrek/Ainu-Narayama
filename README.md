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

Ainda não implementado (Fase 2). O motor de cálculo já existe em
`src/indices.py` e `src/falseability.py`, mas a orquestração
completa (ler `data/raw/`, aplicar o Protocolo de Falseabilidade,
calcular N* para os 28 países e gravar em `data/processed/`) ainda
não foi construída.

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
- Fase 2: CHR + NIH
- Fase 3: EIS + IES
- Fase 4: IVAT e simulações OLG
- Fase 5: Agentes computacionais

## Referências
- Tese v8.0: /docs/
- UN WPP: https://population.un.org/wpp/
- OECD SOCX: https://stats.oecd.org/
- Streamlit: https://docs.streamlit.io/

---
Criado: 29 de junho de 2026
Versão: 1.0 (MVP)
