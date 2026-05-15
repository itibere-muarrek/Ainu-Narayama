# AINU Agente Coletor Automático

Sistema automático de coleta, processamento e cálculo de índices socioeconômicos de 29 países.

## 🚀 Visão Geral

O agente roda **automaticamente toda sexta-feira 14:00 (horário de São Paulo)** — equivalente a **sábado 00:00 (horário de Nagano)**.

### 7 Fases de Processamento

```
FASE 1: Pré-Coleta (validação de ambiente)
        ↓
FASE 2: Coleta Paralela (29 países, múltiplas fontes)
        ↓
FASE 3: Transformação (normalização e validação)
        ↓
FASE 4: Cálculo (N*, IES, NIH, NCII, NSII, L)
        ↓
FASE 5: Validação (4 testes de falseabilidade)
        ↓
FASE 6: Persistência (salva em PostgreSQL)
        ↓
FASE 7: Notificação (email para admin)
```

**Tempo total: ~8 horas de processamento automático**

## 📦 Estrutura

```
agente/
├── scheduler.py              # Orquestrador principal (APScheduler)
├── coleta/
│   ├── __init__.py
│   ├── coleta_un_wpp.py      # UN World Population Prospects
│   ├── coleta_world_bank.py  # World Bank WDI (skeleton)
│   ├── coleta_nacional.py    # IBGE, INEGI, etc (skeleton)
│   └── coleta_fallback.py    # Dados locais em caso de falha
│
├── transformacao/
│   ├── __init__.py
│   └── normalizar.py         # Média móvel, validação de ranges
│
├── calculo/
│   ├── __init__.py
│   └── calcular_indices.py   # N*, IES, NIH, NCII, NSII, L
│
├── validacao/
│   ├── __init__.py
│   └── testes_falseabilidade.py  # TRR, TSP, TCE, TCD
│
├── persistencia/
│   ├── __init__.py
│   └── salvar_bd.py          # Salva em PostgreSQL
│
├── notificacao/
│   ├── __init__.py
│   └── email_admin.py        # Notificação por email
│
└── README.md                 # Este arquivo
```

## 🔧 Configuração

### Variáveis de Ambiente (`.env`)

```bash
# Agendamento
SCHEDULER_TIMEZONE=America/Sao_Paulo  # ou Asia/Tokyo para Nagano

# Email SMTP (para notificações)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=seu-app-password
ADMIN_EMAIL=narayama.live@gmail.com

# Banco de dados
DATABASE_URL=postgresql://user:password@localhost:5432/ainu

# Ambiente
ENVIRONMENT=development  # ou production
```

### Dependências

```bash
pip install \
    apscheduler==3.10.4 \
    requests==2.31.0 \
    sqlalchemy==2.0.25 \
    python-dotenv==1.0.0 \
    fastapi==0.104.1 \
    uvicorn==0.24.0
```

## 🎯 Como Usar

### 1. Automático (Agendado)

O agente inicia automaticamente ao iniciar o servidor FastAPI:

```bash
# Em desenvolvimento
python -m uvicorn app.main:app --reload

# Em produção
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

**Próxima execução:** Próximo sábado (em Nagano) ou sexta 14h (em São Paulo)

Verificar próxima execução nos logs:

```
✓ Scheduler iniciado. Próxima execução: 2026-05-18 14:00:00 (America/Sao_Paulo)
```

### 2. Manual (Teste)

Chamar endpoint da API como ADMIN:

```bash
curl -X POST http://localhost:8000/api/v1/admin/coleta-manual \
  -H "Authorization: Bearer <seu-token-jwt>"
```

Resposta:

```json
{
  "status": "coleta iniciada",
  "mensagem": "Coleta semanal manual disparada com sucesso",
  "usuario_id": 1,
  "timestamp": "2026-05-15T16:45:30.123456"
}
```

## 📊 Detalhes das Fases

### Fase 1: Pré-Coleta

- Valida conectividade de rede
- Verifica status das APIs externas
- Carrega configuração (lista de 29 países)
- Log: "Iniciando coleta sábado 00:30 Nagano"

### Fase 2: Coleta Paralela

Coleta de **5 países simultâneos** para otimizar tempo:

**Por país coletamos:**

- **População:** Pop_Base, Pop_Topo (UN WPP)
- **Demografia:** Nascimentos, Mortes (IBGE, INEGI, etc)
- **Fecundidade:** TFR 1999, TFR 2024 (UN WPP)
- **Economia:** VA, Emprego, Salários (World Bank WDI)
- **Saúde:** Yale EPI Score (Yale Center for Environmental Law)
- **Nutrição:** T, U, M, I (FAO, WHO, IHME)
- **Inovação:** RET, COMP, SYM (Comtrade, Harvard Atlas)

**Estratégia de Fallback:**

1. Tenta Fonte Primária (5 min timeout)
2. Se falha → tenta Fonte Alternativa (5 min)
3. Se falha → tenta Fallback Local (5 min)
4. Se tudo falha → email admin + usa dado anterior

### Fase 3: Transformação

- Normaliza unidades (garantir milhões para população)
- Validação de completude (campos obrigatórios)
- Validação de ranges (valores plausíveis)
- Tratamento de outliers (±3 desvio padrão)
- Cálculo de média móvel (3 anos)

### Fase 4: Cálculo

Para cada país:

```python
# NGII (Natural Growth Index)
NGII_Puro = (Pop_Base / Pop_Topo) × (Nasc / Mortes)
Fator = TFR_2024 / TFR_1999
N* = NGII_Puro × Fator

# Saúde
NIH = 1 − (0.35·T + 0.25·U + 0.20·M + 0.20·I)

# Economia
NCII = (VA / Emprego) × (Salários / VA)

# Inovação
L = 0.4·RET + 0.3·COMP + 0.3·SYM

# Equilíbrio Sistêmico
IES = L × ∛(NGII × NCII × NIH)
```

**Classificação de N*:**

- **PROMISSOR:** N* > 1.3
- **EQUILÍBRIO:** 0.9 ≤ N* ≤ 1.3
- **CRÍTICO:** 0.5 ≤ N* < 0.9
- **COLAPSO:** N* < 0.5

### Fase 5: Validação (4 Testes de Falseabilidade)

#### TRR - Teste Rarefação Residual

**Valida:** Diferença entre NGII_Puro e NGII_Bruto < 15%

```
Se |NGII_Puro - NGII_Bruto| / NGII_Bruto > 15% → MAQUIAGEM
```

**Motivo:** Detecta manipulação ou erro de cálculo

#### TSP - Teste Sinal Penalização

**Valida:** Estruturadores conseguem sustentar Legatários?

```
Se NGII < 0.5 → ESTRUTURADOR PENALIZADO
```

**Motivo:** Razão demográfica desequilibrada

#### TCE - Teste Coerência Estrutural

**Valida:** Pop, TFR, Nasc, Mortes são coerentes?

```
- Pop > 0?
- TFR ∈ [0.5, 9.0]?
- Nasc > 0 e Mortes > 0?
- Razão Pop/Nasc ∈ [10, 1000]?
```

**Motivo:** Detecta dados impossíveis ou inverossímeis

#### TCD - Teste Consistência Dados

**Valida:** Diferentes fontes conversam entre si?

```
- VA/Emprego ∈ [0.001, 100]?
- Salários ≤ VA?
- Confiabilidade adequada?
```

**Motivo:** Detecta inconsistência entre fontes diferentes

**Resultado:** ✅ PASSOU (todos 4 testes) ou ⚠️ AVISOS (flags para revisão manual)

### Fase 6: Persistência

Salva 2 tabelas:

- `dados_brutos_paises` — dados coletados brutos
- `indices_calculados` — índices derivados

**Além disso:**

- Calcula contadores agregados (12 PROMISSORES, 10 EQUILÍBRIO, etc)
- Log completo de auditoria
- Marcação de timestamp

### Fase 7: Notificação

Email HTML para `narayama.live@gmail.com`

**Em desenvolvimento:** Simula email em logs  
**Em produção:** Envia via SMTP

```
Assunto: AINU: Coleta Semanal Concluída com Sucesso
Corpo:
  ├─ Status: ✅ SUCESSO
  ├─ Validação: ✅ PASSOU (4/4 testes)
  ├─ Total Países: 29
  ├─ Promissores: 12
  ├─ Equilíbrio: 10
  ├─ Críticos: 6
  └─ Colapso: 1
```

## 📈 Monitoramento

### Logs

Todos os eventos são registrados em `logs/agente.log`:

```bash
tail -f logs/agente.log
```

Procurar por marcadores:

```bash
# Início da coleta
grep "INÍCIO COLETA SEMANAL" logs/agente.log

# Sucesso
grep "7 FASES CONCLUÍDAS" logs/agente.log

# Erros
grep "ERROR" logs/agente.log
```

### Dashboard de Admin

Endpoint para status:

```bash
GET /api/v1/admin/estatisticas
```

Inclui contadores de coletas, testes e status geral.

## 🐛 Troubleshooting

### Coleta não inicia

```bash
# 1. Verificar se scheduler está rodando
ps aux | grep uvicorn

# 2. Verificar logs
tail -f logs/agente.log

# 3. Dispara coleta manual para testar
curl -X POST http://localhost:8000/api/v1/admin/coleta-manual \
  -H "Authorization: Bearer <token>"
```

### Erro de conexão com banco de dados

```bash
# 1. Verificar DATABASE_URL em .env
cat .env | grep DATABASE_URL

# 2. Testar conexão
python -c "from app.database import SessionLocal; db = SessionLocal(); print('OK')"

# 3. Rodar migrations se necessário
alembic upgrade head
```

### Email não envia

```bash
# 1. Verificar credenciais SMTP em .env
cat .env | grep SMTP

# 2. Em desenvolvimento, emails aparecem nos logs
grep "EMAIL SIMULADO" logs/agente.log

# 3. Verificar se app-password do Gmail está correto
# Gmail exige "App Passwords" em contas com 2FA
```

### Coleta incompleta ou avisos

```bash
# 1. Verificar logs de validação
grep -A 10 "RESULTADO VALIDAÇÃO" logs/agente.log

# 2. Revisar problemas identificados nos 4 testes
grep "⚠️" logs/agente.log

# 3. Contactar admin para revisão manual
```

## 🔄 Alternância de Timezone

Para rodar em **Nagano** em vez de São Paulo:

**scheduler.py, linha 105:**

```python
# De:
trigger = CronTrigger(hour=14, minute=0, day_of_week=4, timezone='America/Sao_Paulo')

# Para:
trigger = CronTrigger(hour=0, minute=0, day_of_week=5, timezone='Asia/Tokyo')
```

Equivalência:
- **São Paulo:** Sexta 14:00 UTC-3 = Sexta 17:00 UTC
- **Nagano:** Sábado 00:00 UTC+9 = Sexta 15:00 UTC ✓ (25h mais tarde)

## 📚 Referências

- MAPA_COLETA_DADOS_29_PAISES.md — Fontes de dados detalhadas
- ITEM_A_FORMULAS_COMPLETAS_ESTRUTURA_BD.md — Fórmulas e schema
- app/models.py — Schema do banco de dados
- app/config.py — Configuração da aplicação

## 📝 Changelog

- **v3.1.0** (2026-05-15) — Agente coletor implementado com 7 fases
  - ✅ Scheduler com APScheduler
  - ✅ Coleta paralela com fallback
  - ✅ 4 testes de falseabilidade
  - ✅ Integração com FastAPI
  - ✅ Email de notificação
  - ✅ Endpoint de coleta manual

## 📧 Suporte

Dúvidas ou problemas? Contacte: `narayama.live@gmail.com`
