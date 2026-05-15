# 🚀 Quickstart - Agente Coletor AINU

Guia rápido para começar a usar o agente coletor automático.

## Pré-requisitos

- Python 3.11+
- PostgreSQL 13+
- pip/conda para gerenciar dependências

## 1. Setup Rápido (5 minutos)

### 1.1 Clone ou navegue ao projeto

```bash
cd C:\Users\LENOVO\Documents\Ainu.Narayama\backend
```

### 1.2 Instale dependências

```bash
pip install -r requirements.txt
```

### 1.3 Configure variáveis de ambiente

```bash
# Copie o exemplo
cp .env.example .env

# Edite .env com suas credenciais
# IMPORTANTE: Mude ADMIN_EMAIL, SMTP_PASSWORD, DATABASE_URL
```

### 1.4 Inicie o servidor

```bash
# Desenvolvimento
python -m uvicorn app.main:app --reload

# Produção
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

Você deve ver:

```
✓ Banco de dados inicializado
✓ Agente coletor semanal iniciado
✓ Scheduler iniciado. Próxima execução: 2026-05-18 14:00:00
```

## 2. Testar a Coleta (Agora)

### Via API

```bash
# 1. Obter token JWT (login como admin)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "seu-email@example.com", "password": "sua-senha"}'

# Salve o token retornado: {"access_token": "eyJ0eXAi..."}

# 2. Dispara coleta manual
curl -X POST http://localhost:8000/api/v1/admin/coleta-manual \
  -H "Authorization: Bearer eyJ0eXAi..."

# 3. Acompanhe nos logs
tail -f logs/agente.log
```

### Esperado

```
=== INÍCIO COLETA SEMANAL ===
Fase 1: Pré-coleta - validando configurações
Fase 2: Coletando dados...
  ✓ Coletados dados de 29 países
Fase 3: Normalizando e transformando dados...
  ✓ 29 registros processados
Fase 4: Calculando índices N* e IES...
  ✓ Brasil: N*=1.025, IES=0.847
  ✓ Argentina: N*=0.895, IES=0.782
  ...
Fase 5: Executando testes de falseabilidade...
  ✓ Validação concluída: PASSOU
Fase 6: Salvando no banco de dados...
  ✓ 29 registros salvos com sucesso
Fase 7: Enviando notificação ao admin...
  ✓ Email enviado para narayama.live@gmail.com
=== 7 FASES CONCLUÍDAS COM SUCESSO ===
```

## 3. Visualizar Resultados

### Via API

```bash
# Listar todos os países com seus índices
curl http://localhost:8000/api/v1/paises

# Obter índices de um país
curl http://localhost:8000/api/v1/paises/BR/indices
```

### Via Banco de Dados

```bash
psql -U ainu_user -d ainu_db

\dt  -- listar tabelas

SELECT 
  p.nome,
  ic.n_estrela,
  ic.status_n,
  ic.ies,
  ic.status_ies
FROM indices_calculados ic
JOIN paises p ON ic.pais_id = p.id
ORDER BY ic.data_calculo DESC
LIMIT 10;
```

## 4. Agendamento Automático

O agente roda automaticamente:

**SEXTA 14:00 (São Paulo) = SÁBADO 00:00 (Nagano)**

Para mudar o horário, edite `backend/agente/scheduler.py` linha ~120:

```python
# De:
trigger = CronTrigger(hour=14, minute=0, day_of_week=4, timezone='America/Sao_Paulo')

# Para (exemplo: segunda 09:00):
trigger = CronTrigger(hour=9, minute=0, day_of_week=0, timezone='America/Sao_Paulo')
```

## 5. Monitoramento

### Logs em Tempo Real

```bash
# Acompanhar coleta
tail -f logs/agente.log

# Filtrar erros
grep ERROR logs/agente.log

# Filtrar sucesso
grep "FASES CONCLUÍDAS" logs/agente.log
```

### Estatísticas de Admin

```bash
curl http://localhost:8000/api/v1/admin/estatisticas \
  -H "Authorization: Bearer <seu-token>"
```

## 6. Troubleshooting

### Erro: "Banco de dados não inicializado"

```bash
# Rode as migrations
python -m alembic upgrade head

# Crie dados iniciais
python scripts/seed_db.py
```

### Erro: "SMTP connection refused"

```bash
# Cheque credenciais em .env
cat .env | grep SMTP

# Em desenvolvimento, emails são simulados nos logs
grep "EMAIL SIMULADO" logs/agente.log
```

### Scheduler não dispara

```bash
# Verificar se está rodando
ps aux | grep uvicorn

# Forçar coleta manual (veja seção 2)
curl -X POST http://localhost:8000/api/v1/admin/coleta-manual ...

# Cheque timezone em .env
cat .env | grep SCHEDULER_TIMEZONE
```

## 7. Próximos Passos

- 📚 Leia `backend/agente/README.md` para documentação completa
- 🔧 Configure integração com World Bank e UN WPP em `backend/agente/coleta/`
- 📊 Personalize testes de falseabilidade em `backend/agente/validacao/`
- 🚀 Deploy em produção com Gunicorn + Nginx

## 📞 Suporte

Email: narayama.live@gmail.com  
Docs: http://localhost:8000/docs (Swagger)  
GitHub: (seu-repo)

---

**Pronto?** Dispara a coleta manual e acompanha nos logs! 🎯
