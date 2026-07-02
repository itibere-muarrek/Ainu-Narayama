# Especificação Técnica de Infraestrutura — AINU-Narayama

> Snapshot em 2026-07-02, commit `26a33b5`. Este documento cobre **recursos,
> tecnologias e infraestrutura** (GitHub, Render, Namecheap, stack). Para
> fórmulas e metodologia do N*, ver [definitions.md](definitions.md).

## 1. Visão geral

Duas aplicações web (Streamlit) publicadas em domínio próprio, com dados
reais da UN World Population Prospects, hospedadas gratuitamente no Render e
com deploy automático a cada push no GitHub.

```
GitHub (código + dados pequenos)
   │  push para main
   ▼
Render (build + hospedagem, redeploy automático)
   │
   ├── ainu-systems  → ainu.systems     (plataforma restrita, 28 países)
   └── narayama-live → narayama.live    (plataforma pública, 7 países)
        │
        └── DNS gerenciado na Namecheap
```

## 2. GitHub

| Item | Valor |
|---|---|
| Repositório | `github.com/itibere-muarrek/Ainu-Narayama` |
| Branch de produção | `main` |
| Commit atual | `26a33b5` |
| Histórico anterior (v4.0, FastAPI/Railway, abandonado) | preservado na tag `archive/v4.0-railway` |
| CI | `.github/workflows/ci.yml` — roda a cada push/PR em `main`: instala dependências, valida os 28 países (`config.py` ↔ `paises_perfil.csv`), roda `test_calculo_brasil.py`. Não faz deploy (Render já redesploya sozinho). |

Não há workflow de deploy no GitHub Actions — nem Render nem (se algum dia
for usado) Streamlit Cloud precisam disso; ambos observam o repositório
diretamente.

## 3. Render (hospedagem)

Conta gratuita (sem cartão de crédito). Dois **Web Services** independentes,
criados via **Blueprint** a partir de [`render.yaml`](../render.yaml):

| Serviço | Domínio | Entry point | Runtime |
|---|---|---|---|
| `ainu-systems` | ainu.systems | `app/ainu_systems/app.py` | Python 3, Free |
| `narayama-live` | narayama.live | `app/narayama_live/app.py` | Python 3, Free |

**Build/start commands** (definidos no `render.yaml`, iguais nos dois):
```
buildCommand: pip install -r app/requirements.txt
startCommand: streamlit run app/<serviço>/app.py --server.port $PORT --server.address 0.0.0.0
```

**Variáveis de ambiente**:
- `AINU_SYSTEMS_PASSWORD` (só no serviço `ainu-systems`) — senha do gate de
  acesso da plataforma restrita. Definida direto no painel do Render, **não
  está no repositório** (`render.yaml` só reserva o nome com `sync: false`).

**Limites do plano gratuito**:
- 750h de instância/mês, **compartilhadas entre os dois serviços**.
- Cada serviço "dorme" após 15 min sem tráfego (não consome hora dormindo);
  primeiro acesso após dormir leva 30-60s pra acordar (cold start).
- Se exceder as 750h, o Render suspende até o mês seguinte — não cobra nada.
- Upgrade disponível a qualquer momento (plano Starter, ~US$7/mês/serviço)
  se quiser eliminar cold start e o teto de horas — não exige mudança de código.
- 2 domínios customizados grátis por workspace (Hobby) — exatamente o que os
  dois serviços usam.

**Deploy**: automático a cada push em `main`. Sem etapa manual depois da
configuração inicial (Fases 1-5 do plano de deploy, todas concluídas em
2026-07-02).

## 4. Namecheap (domínios e DNS)

Dois domínios, ambos gerenciados via **Advanced DNS** da própria Namecheap
(`Namecheap BasicDNS`):

| Domínio | Registros DNS | Observação |
|---|---|---|
| `ainu.systems` | CNAME `www` → `ainu-systems.onrender.com`; A `@` → `216.24.57.1` | Configuração direta, sem troca de nameservers |
| `narayama.live` | CNAME `www` → `narayama-live.onrender.com`; A `@` → `216.24.57.1` | Precisou trocar nameservers de `ns1-4.vercel-dns.com` (sobra de config. anterior) para `Namecheap BasicDNS` antes dos registros funcionarem |

SSL (Let's Encrypt) emitido automaticamente pelo Render após a validação do
DNS — sem ação manual além de criar os registros acima.

## 5. Stack de tecnologia

| Camada | Tecnologia | Versão mínima testada |
|---|---|---|
| Linguagem | Python | 3.13 |
| Interface web | Streamlit | ≥1.56.0 |
| Dados/cálculo | Pandas | ≥3.0.2 |
| Gráficos | Plotly | ≥6.7.0 |
| Serialização de dataframes | PyArrow | ≥24.0.0 |
| HTTP (reservado p/ Fase 2b) | Requests | ≥2.33.1 |

Todas as dependências em [`app/requirements.txt`](../app/requirements.txt),
usado tanto localmente quanto pelo `buildCommand` do Render.

## 6. Estrutura do repositório

```
Ainu.Narayama/
├── src/                        # motor de cálculo (sem dependência de Streamlit)
│   ├── config.py                 # 28 países, limiares, faixas etárias por perfil
│   ├── data_loader.py             # leitura/validação de CSVs brutos
│   ├── data_pipeline.py           # orquestra o cálculo de N* (Fase 2a: só UN WPP)
│   ├── indices.py                 # fórmulas: NGII_puro, Fator_Geracional, N*, Fator_Alocativo
│   └── falseability.py            # Protocolo de Falseabilidade (7 testes, Anexo 9)
├── app/
│   ├── ainu_systems/app.py      # plataforma restrita (28 países, gate de senha)
│   ├── narayama_live/app.py     # plataforma pública (7 países destaque)
│   └── requirements.txt
├── data/
│   ├── raw/un_wpp.csv           # painel real UN WPP (28 países, 1999+2024), commitado
│   └── processed/n_index_2024.csv  # saída do pipeline, commitado
├── docs/
│   ├── definitions.md           # fórmulas, decisões, inconsistências da tese, roadmap
│   ├── paises_perfil.csv        # referência dos 28 países (espelha src/config.py)
│   └── infraestrutura.md        # este documento
├── test_calculo_brasil.py       # script de sanidade manual
├── render.yaml                  # Blueprint dos 2 serviços
├── .github/workflows/ci.yml     # CI (não-deploy)
└── README.md                    # guia rápido de uso e deploy
```

`tests/` e `notebooks/` existem como estrutura reservada (Fase 1), ainda
vazios.

## 7. Dados e metodologia (resumo — detalhes em definitions.md)

| Fonte | Status | Uso |
|---|---|---|
| UN World Population Prospects 2024 | ✅ Integrada, dados reais (28 países, idade simples 1999+2024) | NGII_puro, Fator_Geracional |
| OECD Social Expenditure Database | ⏳ Planejada (Fase 2b) | Fator_Alocativo/farol — cobertura parcial (só ~15 dos 28 países são OCDE) |
| National Transfer Accounts (NTA) | ⏳ Planejada (Fase 2b) | Fator_Alocativo (fonte alternativa/complementar à OECD) |
| UNESCO / World Bank Education Stats | ⏳ Planejada (Fase 2b) | Versão Expandida do NGII_puro (fator de escolaridade) |

Fórmula vigente (Versão Básica, ver definitions.md seção 3):
```
NGII_puro = (Pop_Base / Pop_Topo) × (Nascimentos / Mortes)
N* = NGII_puro × Fator_Geracional
```
Sem normalização definida pela tese — valores altos em países jovens/alta
fecundidade são esperados (ver definitions.md, seção 8).

## 8. Segurança e segredos

- Único segredo do projeto: `AINU_SYSTEMS_PASSWORD`, mantido exclusivamente
  no painel do Render (variável de ambiente), nunca no repositório.
- `.gitignore` bloqueia `.env`, `data/raw/*` e `data/processed/*` por padrão,
  com exceção explícita pros dois arquivos pequenos e não-sensíveis já
  commitados (`un_wpp.csv`, `n_index_2024.csv`).
- Sem banco de dados, sem armazenamento de dados de usuário, sem
  autenticação de conta real (o gate de senha do `ainu-systems` é um
  placeholder de Fase 1, documentado como tal no próprio código).

## 9. Estado atual (2026-07-02)

- ✅ Fase 1 (estrutura) e Fase 2a (pipeline UN WPP) completas.
- ✅ Deploy completo: os dois domínios próprios no ar, HTTPS válido.
- ⏳ Fase 2b (Fator_Alocativo real + Versão Expandida com escolaridade) —
  não iniciada, instruções prontas em `definitions.md` seção 9.
- ⏳ Calibração de coortes país-a-país — planejada, ainda não iniciada.
