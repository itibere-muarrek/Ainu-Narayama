# AINU-Narayama Frontend v3.1.0

Interface web Streamlit para o Sistema de Medição Socioeconômica AINU-Narayama.

## 🚀 Quick Start

### Pré-requisitos
- Python 3.11+
- Backend AINU rodando (http://localhost:8000)
- pip

### Instalação Local

```bash
# 1. Ir para pasta frontend
cd frontend

# 2. Criar virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Copiar arquivo .env
cp .env.example .env
# Editar .env se backend não está em localhost:8000

# 5. Rodar Streamlit
streamlit run main.py
```

Acesso: http://localhost:8501

### Com Docker Compose

```bash
docker-compose up -d

# Logs
docker-compose logs -f frontend
```

Acesso: http://localhost:8501

## 📄 Páginas

1. **🏠 Home** - Página pública de entrada
   - Informações sobre AINU
   - Login/Cadastro
   - Países destaque

2. **📊 Dashboard** - Visão geral dos 29 países
   - Tabelas N* e IES
   - Filtros por status
   - Estatísticas gerais

3. **🎮 Simulador N*** - Simulador de cenários demográficos
   - Ajuste de ±25% em macrovariáveis
   - Cálculo em tempo real
   - Análise de agente IA

4. **🎮 Simulador IES** - Simulador de estabilidade sistêmica
   - 4 dimensões interativas
   - Gráfico RADAR 4D
   - Simulações comparativas

5. **📖 Metodologia** - Documentação técnica
   - Explicação de fórmulas
   - Fontes de dados
   - Referências

6. **ℹ️ Sobre** - Informações do projeto
   - Missão AINU
   - Pesquisador
   - 29 países

7. **❓ FAQ** - Perguntas frequentes
   - Como usar
   - Índices
   - Simuladores

8. **📧 Contato** - Formulário de contato
   - Envio de mensagens
   - Feedback rápido

## 🔐 Autenticação

### Fluxo
1. **Home → Cadastre-se** → Preencher dados → Admin aprova
2. **Home → Login** → Email + Senha → Acesso ao Dashboard/Simuladores
3. **Token JWT** → Armazenado em `st.session_state`
4. **Logout** → Botão na sidebar

### Roles
- 👤 **VISITANTE** (não aprovado): Apenas Home
- 👤 **VISITANTE APROVADO**: Acesso completo
- 🔐 **CO-ADMIN**: Gerenciar países
- 👨‍💼 **ADMIN**: Acesso total

## 🎨 Tema AINU

**Cores:**
- Azul Profundo: `#0A1F3D`
- Dourado: `#D4AF37`
- Terracota: `#C85A54`
- Creme: `#F8F4ED`

**Componentes:**
- `header_ainu()` - Cabeçalho
- `sidebar_ainu()` - Sidebar
- `stat_box()` - Caixa de estatística
- `card()` - Card informativo
- `status_badge()` - Badge de status
- `footer_ainu()` - Rodapé

## 📊 Integração com Backend

### Endpoints Usados
```
POST   /api/v1/auth/register          # Registro
POST   /api/v1/auth/login             # Login
GET    /api/v1/auth/me                # Dados usuário
GET    /api/v1/paises                 # Listar países
POST   /api/v1/calculo/n-star         # Calcular N*
POST   /api/v1/calculo/ies            # Calcular IES
GET    /api/v1/calculo/indices/{id}   # Obter índices
POST   /api/v1/simulacoes             # Criar simulação
GET    /api/v1/simulacoes/usuario     # Minhas simulações
```

### Cliente API
```python
from services.api_client import AIAClient

api = AIAClient("http://localhost:8000/api/v1", token)
paises = api.get_paises()
resultado = api.calcular_n_star(pais_id, params)
```

## 🔧 Variáveis de Ambiente

```env
BACKEND_API_URL=http://localhost:8000/api/v1
STREAMLIT_CLIENT_THEME_BASE=light
LOG_LEVEL=INFO
ADMIN_EMAIL=narayama.live@gmail.com
```

## 📦 Estrutura

```
frontend/
├── main.py                 # Entry point (Home)
├── pages/                  # 8 páginas Streamlit
├── components/
│   ├── ainu_theme.py      # Tema visual
│   ├── simulador_n.py     # Componente N*
│   └── simulador_ies.py   # Componente IES
├── services/
│   ├── api_client.py      # Cliente HTTP
│   ├── auth.py            # Autenticação JWT
│   └── cache.py           # Cache em session
├── .streamlit/
│   └── config.toml        # Config Streamlit
└── requirements.txt
```

## 🚢 Deploy no Railway

```bash
# Login Railway
railway login

# Deploy
railway up
```

Variáveis de ambiente no Railway:
- `BACKEND_API_URL`: https://seu-backend.railway.app/api/v1

## 🧪 Testes Locais

```bash
# Verificar syntax
python -m py_compile main.py pages/*.py

# Rodar com recarregamento
streamlit run main.py --logger.level=debug
```

## 📞 Suporte

- Email: narayama.live@gmail.com
- GitHub: [AINU-Narayama](https://github.com/itiberre/ainu-narayama)

## 📄 Licença

© 2024 Itiberê L G C Muarrek (USP)
Todos os direitos reservados.
