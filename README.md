# 🌍 AINU-Narayama v4.0

**Sistema Integrado de Medição da Sustentabilidade Intergeracional**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-blue.svg)
![Status](https://img.shields.io/badge/status-production-brightgreen.svg)

---

## 🎯 O que é AINU?

**AINU** (Índice Integrado de Sustentabilidade Intergeracional) é um sistema de medição em tempo real que avalia a capacidade de 29 países sustentarem suas populações ao longo das gerações.

Combina dados de:
- 📊 **Demografia** (população, natalidade, fecundidade)
- 💰 **Economia** (VA, emprego, salários)
- 🌱 **Sustentabilidade** (índices ambientais)
- 🏥 **Saúde** (esperança de vida, mortalidade)
- 🔬 **Inovação** (capacidade tecnológica)

## ✨ Características

### 🤖 Agente Coletor Automático
- ✅ Roda **todo sábado 00:00 (Nagano)** = Sexta 14:00 (São Paulo)
- ✅ Coleta de **29 países** em paralelo
- ✅ **7 fases** de processamento
- ✅ **4 testes** de falseabilidade
- ✅ **Fallback strategy** (3 fontes)
- ✅ Email automático de notificação

### 📈 Índices Calculados
- **N*** (Índice Farol) — Capacidade de crescimento sustentável
- **IES** (Índice Equilíbrio Sistêmico) — Saúde do sistema como um todo
- **NIH** (Natural Health Index) — Qualidade de vida
- **NCII** (Natural Capital Index) — Economia sustentável
- **NSII** (Natural System Index) — Estabilidade ambiental
- **L** (Glocal Index) — Capacidade local de inovação

### 🔐 Segurança & Confiabilidade
- JWT authentication
- ADMIN-only endpoints
- Log de auditoria completo
- Validação de dados em 4 camadas

---

## 📦 Stack Tecnológico

### Backend
- **FastAPI** 0.104+ — API REST moderna
- **SQLAlchemy** 2.0.25 — ORM
- **PostgreSQL** 13+ — Banco de dados
- **APScheduler** 3.10.4 — Agendamento automático
- **Python** 3.11+

### Frontend
- **React** 18+ — UI moderna
- **TypeScript** — Type safety
- **Tailwind CSS** — Design

### DevOps
- **Railway** — Deployment
- **Docker** — Containerização
- **Gunicorn** — Production server

---

## 🚀 Quick Start

### 1. Clone o Repositório
```bash
git clone https://github.com/itibere-muarrek/Ainu-Narayama.git
cd Ainu-Narayama
```

### 2. Configure Backend
```bash
cd backend

# Crie variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais

# Instale dependências
pip install -r requirements.txt

# Inicie servidor
python -m uvicorn app.main:app --reload
```

### 3. Configure Frontend
```bash
cd frontend

# Instale dependências
npm install

# Inicie dev server
npm start
```

### 4. Acesse
- **API:** http://localhost:8000
- **Frontend:** http://localhost:3000
- **Docs:** http://localhost:8000/docs (Swagger)

---

## 📚 Documentação

### Agente Coletor (Recomendado começar por aqui)

1. **[QUICKSTART_AGENTE.md](QUICKSTART_AGENTE.md)** — 5 minutos
   - Setup rápido
   - Teste imediato
   - Troubleshooting básico

2. **[backend/agente/README.md](backend/agente/README.md)** — Documentação técnica
   - Detalhes das 7 fases
   - Configuração completa
   - Monitoramento avançado

3. **[RESUMO_TECNICO.md](RESUMO_TECNICO.md)** — Arquitetura
   - Fórmulas e cálculos
   - 4 testes de falseabilidade
   - Schema do banco de dados

4. **[EXEMPLOS_API.md](EXEMPLOS_API.md)** — Testes
   - Exemplos com curl
   - Integração com Postman
   - Cenários de teste

5. **[INDICE_DOCUMENTACAO.md](INDICE_DOCUMENTACAO.md)** — Navegação
   - Guia por perfil (Dev, Arquiteto, QA, DevOps)
   - Índice de tópicos

---

## 🔄 7 Fases do Agente Coletor

```
FASE 1: Pré-Coleta (30 min)
   └─ Validação de ambiente

FASE 2: Coleta Paralela (3h 30m)
   ├─ 29 países, 5 simultâneos
   ├─ UN WPP, World Bank, IBGE, INEGI, FAO, WHO
   └─ Fallback strategy (3 fontes)

FASE 3: Transformação (1h)
   ├─ Normalização
   └─ Validação de ranges

FASE 4: Cálculo (1h)
   ├─ N*, IES, NIH, NCII, NSII, L
   └─ Classificação de status

FASE 5: Validação (1h) ← NOVO
   ├─ TRR (Rarefação Residual)
   ├─ TSP (Sinal Penalização)
   ├─ TCE (Coerência Estrutural)
   └─ TCD (Consistência Dados)

FASE 6: Persistência (1h)
   └─ PostgreSQL + Auditoria

FASE 7: Notificação (1h)
   └─ Email HTML

TOTAL: ~8 horas automáticas
```

---

## 🧪 Testes de Falseabilidade

### TRR - Teste Rarefação Residual
```
Se |NGII_Puro - NGII_Bruto| / NGII_Bruto > 15% → MAQUIAGEM
```

### TSP - Teste Sinal Penalização
```
Se NGII < 0.5 → ESTRUTURADOR PENALIZADO
```

### TCE - Teste Coerência Estrutural
```
Validar: Pop > 0, TFR ∈ [0.5, 9.0], Nasc > 0, Mortes > 0
```

### TCD - Teste Consistência Dados
```
Validar: VA/Emprego ∈ [0.001, 100], Salários ≤ VA
```

---

## 📊 Exemplo de Resultado

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
  "validacao": {
    "trr": "PASSOU",
    "tsp": "PASSOU",
    "tce": "PASSOU",
    "tcd": "PASSOU"
  }
}
```

---

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```bash
# Banco de Dados
DATABASE_URL=postgresql://user:pass@localhost:5432/ainu_db

# JWT
SECRET_KEY=seu-secret-super-seguro-aqui

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=seu-app-password
ADMIN_EMAIL=narayama.live@gmail.com

# Scheduler
SCHEDULER_TIMEZONE=America/Sao_Paulo

# Ambiente
ENVIRONMENT=development
```

Copie `.env.example` para `.env` e edite.

---

## 🚢 Deployment na Railway

### 1. Conecte seu GitHub
```bash
railway link
```

### 2. Crie serviços
```bash
railway service add postgresql
railway service add python
```

### 3. Deploy automático
- Cada push em `main` redeploya automaticamente
- Variáveis de ambiente configuradas no Railway

### 4. Acesse
```
https://seu-projeto.railway.app
```

---

## 📈 Classificação de N*

| Status | Range | Significado |
|--------|-------|-------------|
| 🟢 PROMISSOR | N* > 1.3 | Crescimento sustentável |
| 🟡 EQUILÍBRIO | 0.9 ≤ N* ≤ 1.3 | Estável |
| 🟠 CRÍTICO | 0.5 ≤ N* < 0.9 | Sob pressão |
| 🔴 COLAPSO | N* < 0.5 | Insustentável |

---

## 🐛 Troubleshooting

### "Coleta não inicia"
```bash
tail -f logs/agente.log
# Procure por ERROR
```

### "Email não envia"
- Em desenvolvimento: `grep "EMAIL SIMULADO" logs/agente.log`
- Em produção: verifique `SMTP_PASSWORD` em `.env`

### "Banco de dados não conecta"
```bash
psql -U usuario -d ainu_db
# Teste conexão
```

---

## 📞 Contato & Suporte

- **Email:** narayama.live@gmail.com
- **GitHub:** [Ainu-Narayama](https://github.com/itibere-muarrek/Ainu-Narayama)
- **API Docs:** http://localhost:8000/docs

---

## 📝 Estrutura do Projeto

```
Ainu-Narayama/
├── backend/
│   ├── agente/                    (Coletor automático)
│   │   ├── scheduler.py
│   │   ├── coleta/
│   │   ├── transformacao/
│   │   ├── calculo/
│   │   ├── validacao/            ← NOVO (4 testes)
│   │   ├── persistencia/
│   │   ├── notificacao/
│   │   └── README.md
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── config.py
│   │   └── api/v1/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── docs/
│   ├── QUICKSTART_AGENTE.md
│   ├── RESUMO_TECNICO.md
│   ├── EXEMPLOS_API.md
│   └── INDICE_DOCUMENTACAO.md
├── .gitignore
└── README.md                     (este arquivo)
```

---

## 📄 Licença

Este projeto está sob licença **MIT**. Veja [LICENSE](LICENSE) para detalhes.

---

## 🙏 Créditos

Desenvolvido com ❤️ para sustentabilidade intergeracional.

**Última atualização:** 15 de Maio de 2026  
**Versão:** 4.0

---

## 🎯 Roadmap

- [ ] Integração com UN WPP API
- [ ] Dashboard de visualização
- [ ] Alertas em tempo real (Slack, PagerDuty)
- [ ] Exportação de relatórios (PDF, Excel)
- [ ] Simulações de cenários
- [ ] Mobile app

---

**Pronto para começar?** → Leia [QUICKSTART_AGENTE.md](QUICKSTART_AGENTE.md) 🚀
