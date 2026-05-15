# 🚀 Deployment na Railway

Guia passo-a-passo para fazer deploy do AINU-Narayama na Railway.

## 📋 Pré-requisitos

- Conta no [Railway.app](https://railway.app)
- GitHub conectado (ou git push access)
- Variáveis de ambiente configuradas

## 🎯 Passo 1: Criar Projeto na Railway

### 1.1 Acesse Railway
```
https://railway.app/dashboard
```

### 1.2 Click em "New Project"

### 1.3 Selecione "Deploy from GitHub"

### 1.4 Conecte seu repositório
```
itibere-muarrek/Ainu-Narayama
```

## 🔧 Passo 2: Configurar Serviços

### 2.1 Criar PostgreSQL

```
Railway Dashboard → New → Database → PostgreSQL
```

Copie a `DATABASE_URL` gerada automaticamente.

### 2.2 Criar Backend (Python/FastAPI)

```
Railway Dashboard → New → GitHub Repo → Ainu-Narayama
```

**Configure:**
- **Root Directory:** `backend/`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:$PORT`

## 🔐 Passo 3: Configurar Variáveis de Ambiente

No Railway, vá a **Variables** e adicione:

```
ENVIRONMENT=production
DATABASE_URL=<copie do PostgreSQL>
SECRET_KEY=<gere com: openssl rand -hex 32>
ADMIN_EMAIL=narayama.live@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=seu-app-password
SCHEDULER_TIMEZONE=America/Sao_Paulo
```

### 🔑 Como gerar SECRET_KEY

```bash
openssl rand -hex 32
```

Ou no Python:

```python
import secrets
secrets.token_hex(32)
```

### 📧 SMTP com Gmail

1. Ative "App Passwords" no Gmail (se tiver 2FA)
2. Use a senha de app no `SMTP_PASSWORD`

**Ref:** https://support.google.com/accounts/answer/185833

## 📦 Passo 4: Deploy Automático

### 4.1 Conectar GitHub

Quando você der **push** em `main`:

```bash
git push origin main
```

Railway **faz deploy automaticamente** do `Dockerfile`:

```
backend/Dockerfile → gunicorn → uvicorn → FastAPI
```

### 4.2 Verificar Deploy

```
Railway Dashboard → Logs → View Build & Deploy Logs
```

Esperado:

```
✓ Build succeeded
✓ Deploy started
✓ 2024-05-15T00:00:00Z Application started
```

## 🌍 Passo 5: Acessar Aplicação

Após deploy bem-sucedido:

```
https://seu-projeto.up.railway.app
```

**API:** `https://seu-projeto.up.railway.app/api/v1/`  
**Docs:** `https://seu-projeto.up.railway.app/docs`  
**Health:** `https://seu-projeto.up.railway.app/health`

## ✅ Verificar Deployment

### Teste Health Check

```bash
curl https://seu-projeto.up.railway.app/health
```

Resposta esperada:

```json
{
  "status": "ok",
  "environment": "production"
}
```

### Teste Swagger Docs

```
https://seu-projeto.up.railway.app/docs
```

## 🔄 Agendador Automático

O scheduler começa **automaticamente** quando o app inicia:

```
✓ Banco de dados inicializado
✓ Agente coletor semanal iniciado
✓ Scheduler iniciado. Próxima execução: 2026-05-18 14:00:00
```

**Primeira coleta:** Próximo sábado 00:00 (Nagano) ou sexta 14:00 (São Paulo).

Para testar manualmente:

```bash
curl -X POST https://seu-projeto.up.railway.app/api/v1/admin/coleta-manual \
  -H "Authorization: Bearer <seu-token-jwt>"
```

## 📧 Email em Produção

O agente enviará emails reais para `narayama.live@gmail.com` após cada coleta:

```
Assunto: AINU: Coleta Semanal Concluída com Sucesso
Para: narayama.live@gmail.com
```

Verifique os logs:

```
Railway Logs → Grep "Email enviado"
```

## 🐛 Troubleshooting

### Erro: "Build failed"

```bash
# Verifique os logs no Railway
# Provavelmente: requirements.txt faltando ou versão Python incompatível

# Solução:
cd backend
pip freeze > requirements.txt
git push origin main
```

### Erro: "Database connection refused"

```bash
# Verifique:
# 1. DATABASE_URL está correto em Variables?
# 2. PostgreSQL está rodando?
# 3. Firewall está bloqueando?

# Em Railway Dashboard:
# → Postgres Service → View Logs
```

### Scheduler não inicia

```bash
# Logs:
Railway → Backend → Logs → Grep "Scheduler"

# Se ver erro, verifique:
# - SCHEDULER_TIMEZONE correto
# - APScheduler 3.10.4 em requirements.txt
```

### Email não envia

```bash
# Verifique em produção:
# SMTP_USER e SMTP_PASSWORD estão corretos?
# Gmail exige "App Password" (não senha comum)

# Logs:
Railway → Backend → Logs → Grep "Email"
```

## 📊 Monitoramento

### Ver Logs em Tempo Real

```
Railway Dashboard → Backend Service → Logs
```

Procure por:

```
✓ INÍCIO COLETA
✓ FIM COLETA
❌ ERROR
⚠️ WARNING
```

### Métricas

```
Railway Dashboard → Metrics
```

Monitore:

- **CPU Usage**
- **Memory Usage**
- **Network I/O**
- **Status Code Distribution**

## 🔄 Atualizações

Quando você fizer mudanças:

```bash
# Edite código
git add .
git commit -m "Update agente coletor"
git push origin main

# Railway faz deploy automaticamente!
```

## 💰 Custos na Railway

- **PostgreSQL:** $5/mês
- **Python App:** ~$5/mês (small)
- **Total:** ~$10/mês

(valores aproximados)

Verifique: Railway Dashboard → Pricing

## 📞 Suporte

- **Railway Docs:** https://docs.railway.app
- **Email:** narayama.live@gmail.com

---

**Pronto para deploy?** Siga os passos 1-5 acima! 🚀

Após deploy bem-sucedido, o agente coletor rodará automaticamente toda semana! 🎉
