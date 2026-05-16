# AINU.SYSTEMS v3.1.0

**Agente Inteligente Narayama de Uniformização**

Sistema de análise demográfica com inteligência artificial para compreender a saúde e sustentabilidade de populações em 29 países.

[![Status](https://img.shields.io/badge/status-production-brightgreen)](https://narayama.live)
[![Version](https://img.shields.io/badge/version-3.1.0-blue)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 🌍 O que é AINU?

AINU analisa dados demográficos usando dois índices principais:

- **N\* (Índice Narayama)**: Mede capacidade regenerativa de populações
- **IES (Índice Equilíbrio Sistêmico)**: Mede sustentabilidade do sistema

Homenageia o filme clássico de Shohei Imamura que explora temas de ciclo de vida, morte e sustentabilidade.

---

## 🚀 Quick Start

### Pré-requisitos
- Docker & Docker Compose
- Git
- Python 3.11+ (para desenvolvimento local)

### 1. Clonar repositório
```bash
git clone https://github.com/imuarrek/ainu-narayama.git
cd ainu-narayama
```

### 2. Configurar variáveis de ambiente
```bash
cp .env.example .env
# Edite .env com suas configurações
```

### 3. Iniciar com Docker
```bash
docker-compose up -d
```

### 4. Popular banco de dados
```bash
docker exec ainu_backend python -m scripts.seed_usuarios
```

### 5. Acessar aplicação
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000/docs
- **Login**: 
  - Email: `imuarrek@gmail.com`
  - Senha: `Nara2026!`

---

## 📊 Recursos

### Dashboard
- Visualização de 29 países
- KPIs e métricas globais
- Filtros e ordenação
- Gráficos interativos com Plotly

### Simuladores
- **Simulador N\***: Teste cenários de capacidade regenerativa
- **Simulador IES**: Teste cenários de sustentabilidade
- Ajustes de parâmetros (±25%)
- Comparação antes/depois em tempo real

### Histórico & Projeções
- Dados de 1999 a 2024 (25 anos)
- Projeções de 2024 a 2034 (10 anos)
- Análise de tendências
- Pontos de transição críticos

### Autenticação
- Registro de usuários
- Aprovação por administrador
- JWT tokens (24h)
- Senhas com bcrypt

### Painel Admin
- Gerenciar usuários pendentes
- Aprovar/rejeitar cadastros
- Visualizar logs
- Status do sistema

---

## 🏗️ Arquitetura

```
ainu-narayama/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app
│   │   ├── models.py         # SQLAlchemy ORM
│   │   ├── database.py       # PostgreSQL connection
│   │   └── routers/
│   │       ├── auth.py       # Autenticação JWT
│   │       ├── paises.py     # APIs de países
│   │       └── admin.py      # APIs administrativas
│   ├── agente/
│   │   └── scheduler.py      # Agente 7 fases
│   ├── scripts/
│   │   └── seed_usuarios.py  # Populate DB
│   └── requirements.txt
│
├── frontend/
│   ├── main.py               # Home + Login
│   ├── pages/
│   │   ├── 1_Dashboard.py
│   │   ├── 2_Simulador_N.py
│   │   ├── 3_Simulador_IES.py
│   │   ├── 4_Historico.py
│   │   ├── 5_Projecoes.py
│   │   ├── 6_Metodologia.py
│   │   ├── 7_Sobre.py
│   │   ├── 8_FAQ.py
│   │   ├── 9_Contato.py
│   │   └── 10_Admin.py
│   ├── data/
│   │   └── paises_narayama.json
│   └── requirements.txt
│
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── .env.example
├── .gitignore
└── README.md
```

### Stack Tecnológico

**Backend**
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- PostgreSQL 15
- APScheduler (Agente)
- Python-Jose (JWT)
- Passlib (Bcrypt)

**Frontend**
- Streamlit 1.28.1
- Plotly (Gráficos)
- Pandas (Dados)
- Requests (API)

**Deployment**
- Docker & Docker Compose
- Railway (Recomendado)
- PostgreSQL Cloud

---

## 📐 Fórmulas

### N\* (Índice Narayama)
```
N* = NGII_Puro × Fator_Geracional

Onde:
  NGII_Puro = (pop_base / pop_topo) × (nasc / mortes)
  Fator_Geracional = tfr_atual / tfr_1999
```

**Status:**
- N* > 1.3 = 🟢 PROMISSOR
- 0.9-1.3 = 🔵 EQUILÍBRIO  
- 0.5-0.9 = 🟠 CRÍTICO
- N* < 0.5 = 🔴 COLAPSO

### IES (Índice Equilíbrio Sistêmico)
```
IES = L × ∛(NGII × NCII × NSII)

Onde:
  NIH = max(0.35, min(0.85, 1 − (0.35·T + 0.25·U + 0.20·M + 0.20·I)))
  NSII = 0.45·A_ext + 0.55·NIH
```

**Status:**
- IES > 0.8 = 🟢 SAUDÁVEL
- 0.6-0.8 = 🔵 ESTÁVEL
- 0.4-0.6 = 🟡 FRÁGIL
- IES < 0.4 = 🔴 CRÍTICO

---

## 🤖 Agente Coletor (7 Fases)

Executa automaticamente toda **sexta-feira às 14:00 (São Paulo)**:

1. **PRÉ-COLETA**: Validações e preparação
2. **COLETA PARALELA**: UN WPP, World Bank, Yale EPI
3. **TRANSFORMAÇÃO**: Normalização de dados
4. **CÁLCULO**: N*, IES, NIH, NSII
5. **VALIDAÇÃO**: 4 testes de falsificabilidade (TRR, TSP, TCE, TCD)
6. **PERSISTÊNCIA**: Salvando em PostgreSQL
7. **NOTIFICAÇÃO**: Email para admin

---

## 👥 Usuários Pré-configurados

| Email | Senha | Tipo | Status |
|---|---|---|---|
| imuarrek@gmail.com | Nara2026! | Admin | ✅ Aprovado |
| VISITOR1 | Vis123 | Usuário | ✅ Aprovado |
| VISITOR2 | Vis456 | Usuário | ✅ Aprovado |

---

## 🛠️ Desenvolvimento Local

### Sem Docker
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Frontend (novo terminal)
cd frontend
pip install -r requirements.txt
streamlit run main.py
```

### Com SQLite (rápido para testes)
```bash
# Edite backend/.env
DATABASE_URL=sqlite:///./test.db
```

---

## 📚 Países Analisados (29)

**África**: Nigeria, Ethiopia, DRCongo, Egypt, Kenya

**Ásia**: India, Indonesia, Vietnam, Iran, China, Thailand, Pakistan, Bangladesh, Japan, South Korea, Saudi Arabia

**Europa**: Poland, Germany, France, Spain, Russia

**Américas**: Brazil, Mexico, United States, Argentina, Canada

**Oceania**: Australia

---

## 🔐 Segurança

- ✅ HTTPS em produção
- ✅ JWT tokens (24h)
- ✅ Bcrypt password hashing
- ✅ SQL Injection protection (SQLAlchemy ORM)
- ✅ CORS configurado
- ✅ Validação de entrada (Pydantic)
- ✅ Rate limiting recomendado (nginx)
- ✅ Backup automático de banco de dados

---

## 📖 Documentação

- **Metodologia**: Veja página "Metodologia" no app
- **FAQ**: Veja página "FAQ"
- **API Docs**: http://localhost:8000/docs (Swagger UI)

---

## 🚀 Deploy em Railway

1. Conecte seu repositório GitHub
2. Configure variáveis de ambiente
3. Deploy automático em push
4. PostgreSQL fornecido por Railway

Veja [RAILWAY.md](RAILWAY.md) para instruções detalhadas.

---

## 📈 Estatísticas

- **Países**: 29
- **Anos de histórico**: 25 (1999-2024)
- **Anos de projeção**: 10 (2024-2034)
- **Indicadores por país**: 15+
- **Testes de validação**: 4
- **Fases do agente**: 7

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit mudanças (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📞 Suporte

- 📧 **Email**: narayama.live@gmail.com
- 🌐 **Website**: https://narayama.live
- 📚 **Documentação**: Veja abas do app
- ❓ **FAQ**: Página "FAQ" no app

---

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes

---

## 🎬 Inspiração

Homenageia o filme **"Narayama Bushiko"** (A Balada de Narayama) de Shohei Imamura,
que explora temas de envelhecimento, morte e sustentabilidade populacional.

---

## 🙏 Agradecimentos

- Anthropic Claude por desenvolvimento
- UN WPP por dados populacionais
- World Bank por indicadores econômicos
- Yale EPI por dados ambientais
- Shohei Imamura pela inspiração

---

**AINU.SYSTEMS v3.1.0** | Lançado em 2024 | Última atualização: 2024-05-16

```
╔═══════════════════════════════════════════════════════════════════════╗
║                    AINU.SYSTEMS v3.1.0 - ONLINE                      ║
║            Agente Inteligente Narayama de Uniformização               ║
║                   https://narayama.live                              ║
╚═══════════════════════════════════════════════════════════════════════╝
```
