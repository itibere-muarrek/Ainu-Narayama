# 📊 Resumo Técnico - Agente Coletor AINU

## Visão Geral

Sistema automático de coleta, processamento e validação de dados socioeconômicos de 29 países, executado semanalmente com 7 fases de processamento.

## Stack Tecnológico

```
Backend:     FastAPI + Uvicorn
Scheduler:   APScheduler 3.10.4
Database:    PostgreSQL 13+
HTTP:        requests 2.31.0
ORM:         SQLAlchemy 2.0.25
Config:      python-dotenv 1.0.0
Email:       smtplib (built-in)
Async:       asyncio
```

## Arquitetura

### Modular

```
agente/
├── scheduler.py          # Orquestrador (entry point)
├── coleta/              # Fonte de dados
├── transformacao/       # Normalização
├── calculo/            # Índices
├── validacao/          # 4 testes (NOVO)
├── persistencia/       # PostgreSQL
└── notificacao/        # Email
```

Cada módulo é independente e testável isoladamente.

### Fluxo de Dados

```
[APScheduler Trigger]
        ↓
[scheduler.tarefa_coleta_semanal()]
        ↓
[Fase 1: Pré-Coleta]
        ↓
[Fase 2: Coleta Paralela]
    ├─ 29 países (5 simultâneos)
    ├─ Múltiplas fontes (UN WPP, World Bank, IBGE, etc)
    └─ Fallback strategy (3 fontes)
        ↓
[Fase 3: Transformação]
    ├─ Validação de completude
    ├─ Validação de ranges
    └─ Tratamento de outliers
        ↓
[Fase 4: Cálculo]
    ├─ NGII, N*, IES, NIH, NCII, NSII, L
    └─ Classificação de status
        ↓
[Fase 5: Validação] ← NOVO
    ├─ TRR (Rarefação Residual)
    ├─ TSP (Sinal Penalização)
    ├─ TCE (Coerência Estrutural)
    └─ TCD (Consistência Dados)
        ↓
[Fase 6: Persistência]
    ├─ dados_brutos_paises
    ├─ indices_calculados
    └─ log_auditoria
        ↓
[Fase 7: Notificação]
    └─ Email HTML para admin
```

## Fórmulas Implementadas

### NGII (Natural Growth Index)

```
NGII = (Pop_Base / Pop_Topo) × (Nascimentos / Mortes)
```

### N* (Farol Index)

```
Fator = TFR_2024 / TFR_1999
N* = NGII × Fator

Classificação:
  PROMISSOR  → N* > 1.3
  EQUILÍBRIO → 0.9 ≤ N* ≤ 1.3
  CRÍTICO    → 0.5 ≤ N* < 0.9
  COLAPSO    → N* < 0.5
```

### IES (Índice Equilíbrio Sistêmico)

```
NIH = 1 − (0.35·T + 0.25·U + 0.20·M + 0.20·I)
NCII = (VA / Emprego) × (Salários / VA)
NSII = 0.45·A_ext_epi + 0.55·NIH
L = 0.4·RET + 0.3·COMP + 0.3·SYM
IES = L × ∛(NGII × NCII × NSII)
```

## 4 Testes de Falseabilidade

### TRR - Teste Rarefação Residual

```python
def teste_trr(ngii_bruto, ngii_puro):
    diff = abs(ngii_puro - ngii_bruto) / ngii_bruto
    return diff < 0.15  # 15% tolerance
```

**Valida:** Diferença entre cálculos < 15%

### TSP - Teste Sinal Penalização

```python
def teste_tsp(ngii):
    return ngii > 0.5  # NGII mínimo
```

**Valida:** Razão demográfica adequada

### TCE - Teste Coerência Estrutural

```python
def teste_tce(pop_base, pop_topo, tfr, nasc_mortes):
    checks = [
        pop_base > 0,
        pop_topo > 0,
        tfr >= 0.5 and tfr <= 9.0,
        nasc > 0,
        mortes > 0
    ]
    return all(checks)
```

**Valida:** Dados demográficos coerentes

### TCD - Teste Consistência Dados

```python
def teste_tcd(va, emprego, salarios):
    checks = [
        0.001 < (va/emprego) < 100,
        salarios <= va
    ]
    return all(checks)
```

**Valida:** Dados econômicos convergem

## Banco de Dados

### Tabelas Principais

#### dados_brutos_paises

```sql
- pais_id (FK)
- data_coleta
- pop_base_mi, pop_topo_mi
- nascimentos_mi, mortes_mi
- tfr_2024, tfr_1999
- va_bruto, emprego_total, salarios_totais
- yale_epi_score
- t_ultraprocessados, u_agrotoxicos, m_medicalizado, i_inflamacao
- ret_retorno_local, comp_competitividade, sym_simbolismo
- confiabilidade, metodo
```

#### indices_calculados

```sql
- pais_id (FK)
- data_calculo
- ngii_bruto, ngii_puro, fator_geracional
- n_estrela, status_n
- nih, l_glocalizado, a_ext_epi
- ncii, nsii
- ies, status_ies
```

#### log_auditoria

```sql
- usuario_id (FK)
- acao (ex: COLETA_MANUAL_DISPARADA)
- tabela, registro_id
- antes, depois (JSON)
- criado_em
```

## API REST

### Endpoints Principais

#### Coleta Manual (ADMIN)

```
POST /api/v1/admin/coleta-manual
Authorization: Bearer <token>

Response:
{
  "status": "coleta iniciada",
  "mensagem": "...",
  "usuario_id": 1,
  "timestamp": "2026-05-15T16:45:30.123456"
}
```

#### Consultar Países

```
GET /api/v1/paises
Authorization: Bearer <token>

Response:
[{
  "id": 1,
  "nome": "Brasil",
  "codigo_iso": "BRA",
  ...
}]
```

#### Consultar Índices

```
GET /api/v1/paises/{codigo_iso}/indices
Authorization: Bearer <token>

Response:
{
  "pais": "Brasil",
  "n_estrela": 1.025,
  "status_n": "EQUILIBRIO",
  "ies": 0.847,
  ...
}
```

## Agendamento

### Cron Expression

```
day_of_week=4   (Friday, 0=Monday)
hour=14         (14:00)
minute=0
timezone='America/Sao_Paulo'

Equivalente: Sábado 00:00 Asia/Tokyo
```

### APScheduler Config

```python
trigger = CronTrigger(
    hour=14,
    minute=0,
    day_of_week=4,
    timezone='America/Sao_Paulo'
)

scheduler.add_job(
    tarefa_coleta_semanal,
    trigger=trigger,
    id='coleta_semanal_ainu',
    name='Coleta Semanal AINU'
)
```

## Performance

### Tempos Esperados

```
Fase 1 (Pré-Coleta):       ~30 minutos
Fase 2 (Coleta):           ~3h 30m (5 paralelos)
Fase 3 (Transformação):    ~1 hora
Fase 4 (Cálculo):          ~1 hora
Fase 5 (Validação):        ~1 hora
Fase 6 (Persistência):     ~1 hora
Fase 7 (Notificação):      ~1 hora
───────────────────────────────────
TOTAL:                      ~8 horas
```

### Otimizações

- **Coleta Paralela:** 5 países simultâneos (ThreadPoolExecutor)
- **Fallback Strategy:** 3 tentativas por país (redundância)
- **Batch Insert:** Dados salvos em batch no PostgreSQL
- **Caching:** Dados anteriores como fallback

## Monitoramento

### Logs

```
logs/agente.log

Padrão:
[TIMESTAMP] [LEVEL] [MODULE] Mensagem

Exemplo:
2026-05-15 16:45:30,123 INFO agente.scheduler === INÍCIO COLETA SEMANAL ===
2026-05-15 16:45:31,456 INFO agente.coleta ✓ Coletados dados de 29 países
```

### Métricas

Contadores de status N* após cada coleta:
- PROMISSORES (N* > 1.3)
- EQUILÍBRIO (0.9 ≤ N* ≤ 1.3)
- CRÍTICOS (0.5 ≤ N* < 0.9)
- COLAPSO (N* < 0.5)

## Segurança

### Autenticação

- JWT Bearer Token
- Admin-only endpoints
- Log de auditoria completo

### Validação de Dados

- Range validation (TFR, Pop, etc)
- Tipo validation (float, int, str)
- Completude validation (campos obrigatórios)

### Email

- Credenciais em variáveis de ambiente
- SMTP TLS
- Desenvolvimento: simulado em logs

## Deployment

### Desenvolvimento

```bash
python -m uvicorn app.main:app --reload
```

### Produção

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]
```

## Configuração

### Variáveis de Ambiente (.env)

```
DATABASE_URL=postgresql://...
ADMIN_EMAIL=narayama.live@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=...
SMTP_PASSWORD=...
SCHEDULER_TIMEZONE=America/Sao_Paulo
ENVIRONMENT=development
SECRET_KEY=...
```

## Extensibilidade

### Adicionar Novo Teste de Validação

```python
# Em agente/validacao/testes_falseabilidade.py

def _teste_novo(self, indices):
    """Novo teste de validação"""
    # Implementar lógica
    return {
        "passou": bool,
        "motivo": str,
        "detalhe": str
    }
```

### Adicionar Nova Fonte de Coleta

```python
# Em agente/coleta/coleta_nova_fonte.py

def coletar_nova_fonte(pais_iso):
    """Coleta de nova fonte"""
    # Implementar lógica
    return dados_dict
```

## Referências

- APScheduler: https://apscheduler.readthedocs.io/
- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- PostgreSQL: https://www.postgresql.org/docs/

---

**Última atualização:** 15 de Maio de 2026
