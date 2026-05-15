# AINU-Narayama Backend v3.1.0

API REST para o Sistema de Medição Socioeconômica AINU-Narayama.

## 🚀 Quick Start

### Pré-requisitos
- Python 3.11+
- PostgreSQL 15+
- pip

### Instalação Local

```bash
# 1. Clonar repositório
git clone <repo-url>
cd backend

# 2. Criar virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Copiar arquivo .env
cp .env.example .env
# Editar .env com suas credenciais

# 5. Rodar migrations (cria tabelas)
python -c "from app.database import init_db; init_db()"

# 6. Iniciar servidor
python main.py
```

Acesso:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Com Docker Compose

```bash
docker-compose up -d

# Logs
docker-compose logs -f backend
```

## 📊 Endpoints Principais

### Autenticação
```
POST   /api/v1/auth/register        # Registrar novo usuário
POST   /api/v1/auth/login           # Login
POST   /api/v1/auth/refresh-token   # Renovar access token
GET    /api/v1/auth/me              # Dados do usuário autenticado
```

### Países
```
GET    /api/v1/paises               # Listar países
GET    /api/v1/paises/{id}          # Detalhe país
POST   /api/v1/paises               # Criar país (ADMIN)
PUT    /api/v1/paises/{id}          # Atualizar país (ADMIN)
PUT    /api/v1/paises/{id}/perfil   # Atualizar perfis (CO-ADMIN/ADMIN)
DELETE /api/v1/paises/{id}          # Deletar país (ADMIN)
```

### Cálculos
```
POST   /api/v1/calculo/n-star       # Calcular N*
POST   /api/v1/calculo/ies          # Calcular IES
GET    /api/v1/calculo/indices/{id} # Obter índices salvos
```

### Simulações
```
POST   /api/v1/simulacoes                    # Criar simulação
GET    /api/v1/simulacoes/usuario            # Minhas simulações
GET    /api/v1/simulacoes/{id}               # Detalhe simulação
PUT    /api/v1/simulacoes/{id}               # Atualizar simulação
DELETE /api/v1/simulacoes/{id}               # Deletar simulação
```

### Administração
```
GET    /api/v1/admin/usuarios               # Listar usuários (ADMIN)
PUT    /api/v1/admin/usuarios/{id}          # Aprovar/Rejeitar usuário (ADMIN)
GET    /api/v1/admin/logs                   # Logs de auditoria (ADMIN)
GET    /api/v1/admin/estatisticas           # Estatísticas do sistema (ADMIN)
```

## 🔐 Autenticação

A API usa JWT (JSON Web Tokens) com Bearer authentication.

### Exemplo de Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "senha": "senha123"
  }'
```

Resposta:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Usando o Token
```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer {access_token}"
```

## 📋 Tipos de Usuário

1. **VISITANTE** (padrão)
   - Status: NAO_APROVADO (até admin aprovar)
   - Acesso: Apenas "Sobre", "FAQ", "Contato"

2. **VISITANTE APROVADO**
   - Status: ATIVO (após aprovação admin)
   - Acesso: Simuladores, Dashboard, Download de dados

3. **CO-ADMIN**
   - Pode gerenciar países e editar perfis
   - Pode aprovar novos usuários

4. **ADMIN** (Itiberê)
   - Acesso total ao sistema
   - Gerencia usuários, países, logs

## 🧪 Testes

```bash
# Rodar todos os testes
pytest

# Rodar testes específicos
pytest tests/test_auth.py
pytest tests/test_calculos.py -v

# Com cobertura
pytest --cov=app tests/
```

## 📈 Agente Automático

O agente coleta e calcula índices automaticamente:

**Schedule:** Sexta-feira 14:00 (horário de São Paulo)  
**Equivalente:** Sábado 00:00 (horário de Nagano)

### Fases:
1. **Pré-coleta** - Validação de configurações
2. **Coleta** - Dados da UN WPP, World Bank
3. **Transformação** - Normalização e validação
4. **Cálculo** - N* e IES para 29 países
5. **Persistência** - Salva no BD
6. **Notificação** - Email ao admin

### Ativar Scheduler
```python
from agente.scheduler import iniciar_scheduler

iniciar_scheduler()  # Inicia background scheduler
```

## 🗄️ Banco de Dados

### Tabelas
1. **usuarios** - 14 colunas
2. **paises** - 20 colunas
3. **dados_brutos_paises** - 20 colunas
4. **indices_calculados** - 18 colunas
5. **simulacoes_clientes** - 15 colunas
6. **log_auditoria** - 8 colunas

### Conexão
```python
from app.database import SessionLocal

db = SessionLocal()
# ... usar db
db.close()
```

## 📝 Exemplos de Uso

### 1. Registrar Usuário
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@example.com",
    "senha": "senha123456",
    "mes_ano_nasc": "01/1990",
    "cidade": "São Paulo"
  }'
```

### 2. Criar País (ADMIN)
```bash
curl -X POST http://localhost:8000/api/v1/paises \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Brasil",
    "codigo_iso": "BRA",
    "regiao": "América Latina",
    "perfil_a": 30,
    "perfil_b": 25,
    "perfil_c": 20,
    "perfil_d": 15,
    "perfil_e": 10
  }'
```

### 3. Calcular N*
```bash
curl -X POST http://localhost:8000/api/v1/calculo/n-star \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "pais_id": 1,
    "dados_override": {
      "pop_base_mi": 215.0,
      "tfr_2024": 1.45
    }
  }'
```

## ⚙️ Variáveis de Ambiente

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/ainu
SECRET_KEY=minimo-32-caracteres-para-jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
ADMIN_EMAIL=narayama.live@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=sua-app-password
FRONTEND_URL=https://narayama.live
BACKEND_URL=https://ainu.systems
ENVIRONMENT=development  # ou production
```

## 🚢 Deploy no Railway

```bash
# 1. Instalar Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Deploy
cd backend
railway up
```

## 📞 Suporte

- **Pesquisador:** Itiberê L G C Muarrek (USP)
- **Email:** narayama.live@gmail.com
- **Tese:** Economia Política

## 📄 Licença

Todos os direitos reservados ao pesquisador.
