# 📡 Exemplos de Uso da API - Agente Coletor

Guia prático com exemplos de curl para testar o agente coletor.

## 1. Autenticação

### Login (obter token JWT)

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "seu-email@example.com",
    "password": "sua-senha"
  }'
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**Salve o token:** `export TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."`

---

## 2. Disparar Coleta Manual

### POST /admin/coleta-manual

Dispara a coleta semanal manualmente (útil para testes).

```bash
curl -X POST http://localhost:8000/api/v1/admin/coleta-manual \
  -H "Authorization: Bearer $TOKEN"
```

**Resposta:**
```json
{
  "status": "coleta iniciada",
  "mensagem": "Coleta semanal manual disparada com sucesso",
  "usuario_id": 1,
  "timestamp": "2026-05-15T16:45:30.123456"
}
```

---

## 3. Monitoramento em Tempo Real

### Acompanhar logs durante a coleta

```bash
# Terminal 1: Inicia servidor
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2: Acompanha logs
tail -f logs/agente.log
```

**Você verá:**
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

---

## 4. Consultar Resultados

### GET /paises - Listar todos os países

```bash
curl http://localhost:8000/api/v1/paises \
  -H "Authorization: Bearer $TOKEN"
```

**Resposta:**
```json
[
  {
    "id": 1,
    "nome": "Brasil",
    "codigo_iso": "BRA",
    "populacao": 215000000,
    ...
  },
  ...
]
```

### GET /paises/{codigo_iso}/indices - Obter índices de um país

```bash
curl http://localhost:8000/api/v1/paises/BRA/indices \
  -H "Authorization: Bearer $TOKEN"
```

**Resposta:**
```json
{
  "pais": "Brasil",
  "codigo_iso": "BRA",
  "n_estrela": 1.025,
  "status_n": "EQUILIBRIO",
  "ies": 0.847,
  "status_ies": "CRITICO",
  "nih": 0.65,
  "ncii": 0.78,
  "nsii": 0.72,
  "data_calculo": "2026-05-15"
}
```

---

## 5. Consultar Estatísticas (ADMIN)

### GET /admin/estatisticas

```bash
curl http://localhost:8000/api/v1/admin/estatisticas \
  -H "Authorization: Bearer $TOKEN"
```

**Resposta:**
```json
{
  "total_usuarios": 5,
  "usuarios_ativos": 4,
  "usuarios_pendentes": 1,
  "usuarios_rejeitados": 0,
  "total_logs_auditoria": 245,
  "admins": 2,
  "co_admins": 1
}
```

---

## 6. Consultar Logs de Auditoria (ADMIN)

### GET /admin/logs

```bash
curl "http://localhost:8000/api/v1/admin/logs?limite=10" \
  -H "Authorization: Bearer $TOKEN"
```

**Filtrar por ação:**
```bash
curl "http://localhost:8000/api/v1/admin/logs?acao=COLETA&limite=10" \
  -H "Authorization: Bearer $TOKEN"
```

**Resposta:**
```json
[
  {
    "id": 1,
    "usuario_id": 1,
    "acao": "COLETA_MANUAL_DISPARADA",
    "tabela": "agente",
    "registro_id": 0,
    "criado_em": "2026-05-15T16:45:30.123456",
    "depois": {
      "timestamp": "trigger manual"
    }
  }
]
```

---

## 7. Cenários de Teste

### Teste A: Coleta Rápida (Fallback)

```bash
# Dispara coleta manualmente
# Deve completar em segundos (usando dados fallback)

curl -X POST http://localhost:8000/api/v1/admin/coleta-manual \
  -H "Authorization: Bearer $TOKEN"

# Acompanha logs
tail -f logs/agente.log

# Esperado: 7 fases concluídas em poucos segundos
```

### Teste B: Verificar Validação

```bash
# Após coleta, procure por "RESULTADO VALIDAÇÃO"

grep "RESULTADO VALIDAÇÃO" logs/agente.log

# Esperado:
# ====================================================
# RESULTADO VALIDAÇÃO FALSEABILIDADE
#   Passou: ✅
#   Avisos: 0
#   Erros: 0
# ====================================================
```

### Teste C: Verificar Persistência

```bash
# Conecte ao banco de dados
psql -U ainu_user -d ainu_db

# Listar últimos índices calculados
SELECT 
  p.nome,
  ic.n_estrela,
  ic.status_n,
  ic.ies,
  ic.data_calculo
FROM indices_calculados ic
JOIN paises p ON ic.pais_id = p.id
ORDER BY ic.data_calculo DESC
LIMIT 10;
```

### Teste D: Verificar Email (Desenvolvimento)

```bash
# Em desenvolvimento, emails são simulados nos logs

grep "EMAIL SIMULADO" logs/agente.log

# Esperado:
# [EMAIL SIMULADO] Para: narayama.live@gmail.com
# [EMAIL SIMULADO] Assunto: AINU: Coleta Semanal Concluída com Sucesso
# [EMAIL SIMULADO] Dados: {'total_paises': 29, ...}
```

---

## 8. Troubleshooting via API

### Erro: Unauthorized (401)

```bash
# Token expirado ou inválido
# Faça login novamente para obter novo token
```

### Erro: Forbidden (403)

```bash
# Seu usuário não é ADMIN
# Contacte um administrador para elevar privilégios
```

### Erro: Internal Server Error (500)

```bash
# Verifique os logs
tail -f logs/agente.log

# Procure por "ERROR"
grep ERROR logs/agente.log
```

---

## 9. Automação com Shell Script

Salve em `test_coleta.sh`:

```bash
#!/bin/bash

# Configuração
API="http://localhost:8000/api/v1"
EMAIL="seu-email@example.com"
PASSWORD="sua-senha"

echo "1️⃣ Autenticando..."
TOKEN=$(curl -s -X POST $API/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}" \
  | jq -r '.access_token')

echo "2️⃣ Disparando coleta..."
curl -s -X POST $API/admin/coleta-manual \
  -H "Authorization: Bearer $TOKEN"

echo "3️⃣ Acompanhando logs..."
sleep 2
tail -20 logs/agente.log

echo "✅ Teste concluído"
```

Execute:
```bash
chmod +x test_coleta.sh
./test_coleta.sh
```

---

## 10. Integração com Postman

1. **Criar Coleção:** "AINU Agente Coletor"

2. **Adicionar Variável Global:**
   - Nome: `TOKEN`
   - Valor: (deixe vazio, será preenchido após login)

3. **Request 1: Login**
   - Método: `POST`
   - URL: `{{base_url}}/auth/login`
   - Body (JSON):
     ```json
     {
       "email": "seu-email@example.com",
       "password": "sua-senha"
     }
     ```
   - Script (pós-teste):
     ```javascript
     var jsonData = pm.response.json();
     pm.globals.set("TOKEN", jsonData.access_token);
     ```

4. **Request 2: Coleta Manual**
   - Método: `POST`
   - URL: `{{base_url}}/admin/coleta-manual`
   - Header: `Authorization: Bearer {{TOKEN}}`

5. **Request 3: Estatísticas**
   - Método: `GET`
   - URL: `{{base_url}}/admin/estatisticas`
   - Header: `Authorization: Bearer {{TOKEN}}`

---

**Pronto para testar! 🚀**

Qualquer dúvida: narayama.live@gmail.com
