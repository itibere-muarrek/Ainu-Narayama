import streamlit as st
from services.api_client import AIAClient
import os


def verificar_autenticacao(token):
    """
    Verifica se JWT token é válido

    Returns:
        True: Token válido
        False: Token inválido ou expirado
    """
    if token is None:
        return False

    try:
        BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")
        api = AIAClient(BACKEND_URL, token)
        user = api.me()
        return user is not None
    except:
        return False


def redirecionar_se_nao_logado():
    """
    Se NÃO estiver logado, redireciona para HOME

    USE ESTA FUNÇÃO NA PRIMEIRA LINHA DE CADA PÁGINA PROTEGIDA!
    """
    token = st.session_state.get('jwt_token', None)

    if token is None:
        st.warning("⚠️ Você precisa fazer login para acessar esta página!")
        st.switch_page("pages/0_🏠_Home.py")

    if not verificar_autenticacao(token):
        st.error("❌ Sessão expirada. Faça login novamente.")
        st.session_state.jwt_token = None
        st.session_state.user_data = None
        st.switch_page("pages/0_🏠_Home.py")


def fazer_login(email, senha):
    """
    Tenta fazer login no backend

    POST /api/v1/auth/login
    """
    BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")
    api = AIAClient(BACKEND_URL)

    resultado = api.login(email, senha)

    if resultado:
        st.session_state.jwt_token = resultado.get("access_token")
        # Buscar dados do usuário
        api_autenticado = AIAClient(BACKEND_URL, resultado.get("access_token"))
        user = api_autenticado.me()
        st.session_state.user_data = user
        st.success("✅ Login realizado com sucesso!")
        st.rerun()
    else:
        st.error("❌ Erro ao fazer login. Verifique email e senha.")


def fazer_cadastro(nome, email, senha, instituicao=""):
    """
    Tenta registrar novo usuário

    POST /api/v1/auth/register
    """
    BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")
    api = AIAClient(BACKEND_URL)

    resultado = api.registrar(nome, email, senha, instituicao)

    if resultado:
        st.success("✅ Cadastro realizado! Aguarde aprovação do admin e faça login.")
        return True
    else:
        st.error("❌ Erro ao registrar. Tente novamente.")
        return False


def fazer_logout():
    """
    Faz logout (limpa JWT token)
    """
    st.session_state.jwt_token = None
    st.session_state.user_data = None
    st.rerun()
