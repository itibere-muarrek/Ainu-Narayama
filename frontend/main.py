import streamlit as st
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="AINU.SYSTEMS v3.1.0",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


def get_token():
    return st.session_state.get("token", None)


def set_token(token):
    st.session_state["token"] = token


def get_usuario():
    return st.session_state.get("usuario", None)


def set_usuario(usuario):
    st.session_state["usuario"] = usuario


def logout():
    st.session_state.clear()
    st.rerun()


def fazer_login(email: str, senha: str):
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/auth/login",
            json={"email": email, "senha": senha},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            set_token(data["access_token"])
            set_usuario(data["usuario"])
            st.success("✅ Login realizado com sucesso!")
            st.rerun()
        else:
            error = response.json().get("detail", "Erro ao fazer login")
            st.error(f"❌ {error}")
    except Exception as e:
        st.error(f"❌ Erro de conexão: {str(e)}")


def fazer_cadastro(nome: str, email: str, senha: str, confirma_senha: str):
    if senha != confirma_senha:
        st.error("❌ As senhas não coincidem!")
        return

    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/auth/registrar",
            json={"nome": nome, "email": email, "senha": senha},
            timeout=10
        )
        if response.status_code == 200:
            st.success("✅ Cadastro realizado! Aguarde aprovação do administrador.")
        else:
            error = response.json().get("detail", "Erro ao cadastrar")
            st.error(f"❌ {error}")
    except Exception as e:
        st.error(f"❌ Erro de conexão: {str(e)}")


def renderizar_home_publica():
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image("https://via.placeholder.com/300x100?text=AINU.SYSTEMS", use_column_width=True)

    st.markdown("""
    <h1 style="text-align: center; color: #667eea;">AINU.SYSTEMS v3.1.0</h1>
    <h3 style="text-align: center; color: #666;">Agente Inteligente Narayama de Uniformização</h3>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Cadastro"])

    with tab1:
        st.markdown("### Faça seu login")
        email = st.text_input("📧 Email", key="login_email")
        senha = st.text_input("🔑 Senha", type="password", key="login_senha")

        if st.button("Entrar", key="btn_login", use_container_width=True):
            if email and senha:
                fazer_login(email, senha)
            else:
                st.error("❌ Preencha todos os campos!")

    with tab2:
        st.markdown("### Crie sua conta")
        nome = st.text_input("👤 Nome completo", key="cadastro_nome")
        email = st.text_input("📧 Email", key="cadastro_email")
        senha = st.text_input("🔑 Senha", type="password", key="cadastro_senha")
        confirma_senha = st.text_input("🔑 Confirmar senha", type="password", key="cadastro_confirma")

        if st.button("Cadastrar", key="btn_cadastro", use_container_width=True):
            if nome and email and senha and confirma_senha:
                fazer_cadastro(nome, email, senha, confirma_senha)
            else:
                st.error("❌ Preencha todos os campos!")

    st.markdown("---")
    st.markdown("""
    ### Sobre AINU.SYSTEMS

    AINU é um sistema inteligente de análise demográfica que utiliza:
    - **N* (Índice Narayama)**: Mede a capacidade regenerativa de populações
    - **IES (Índice Equilíbrio Sistêmico)**: Avalia sustentabilidade sistêmica
    - **Validação em 4 testes**: TRR, TSP, TCE, TCD

    Analisa 29 países com dados de 1999 até 2034.
    """)


def renderizar_home_logada():
    usuario = get_usuario()

    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown(f"### 👋 Bem-vindo, {usuario['nome']}!")
    with col2:
        if st.button("🚪 Sair"):
            logout()

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Dashboard</h3>
            <p>Veja todos os 29 países</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🧮 Simuladores</h3>
            <p>Teste cenários N* e IES</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📈 Projeções</h3>
            <p>Veja 10 anos à frente</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>ℹ️ Metodologia</h3>
            <p>Entenda as fórmulas</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    ### Estatísticas Globais

    Acesse as páginas no menu lateral para:
    - 📊 **Dashboard**: Análise completa dos 29 países
    - 🧮 **Simuladores**: Ajuste parâmetros e veja mudanças em tempo real
    - 📈 **Histórico & Projeções**: Visualize tendências de 1999 a 2034
    - 📚 **Documentação**: Metodologia, FAQ e sobre
    - 💬 **Contato**: Envie mensagens direto para nós
    """)

    if usuario.get("is_admin"):
        st.markdown("---")
        st.markdown("### 👨‍💼 Painel Administrativo")
        st.info("Você tem acesso ao painel admin. Acesse via menu: 10_Admin")


def main():
    token = get_token()

    if token:
        renderizar_home_logada()
    else:
        renderizar_home_publica()


if __name__ == "__main__":
    main()
