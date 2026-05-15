import streamlit as st
import os
from dotenv import load_dotenv

from services.auth import auth_manager
from services.api_client import AIAClient
from services.cache import paises_cache
from components.ainu_theme import (
    topbar_ainu, header_ainu, sidebar_ainu, card, stat_box, alert, footer_ainu,
    AINU_COLORS
)

# Config
load_dotenv()
st.set_page_config(
    page_title="AINU-Narayama",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")
api_client = AIAClient(BACKEND_URL, auth_manager.obter_token())


# ===== LAYOUT =====

topbar_ainu(auth_manager)
header_ainu()
sidebar_ainu(auth_manager)

# ===== HOME PÚBLICA =====

if not auth_manager.esta_autenticado():
    # HERO SECTION
    st.markdown(
        f"""
        <div style='
            background: linear-gradient(135deg, {AINU_COLORS['azul_profundo']} 0%, {AINU_COLORS['terracota']} 100%);
            padding: 4rem 2rem;
            border-radius: 1rem;
            color: white;
            text-align: center;
            margin: 2rem 0;
        '>
            <h1 style='font-size: 2.5rem; margin: 0 0 1rem 0;'>Índice de Narayama Sistêmico</h1>
            <p style='font-size: 1.1rem; margin: 0 0 2rem 0;'>Medindo equilíbrio socioeconômico de 29 países</p>
            <p style='font-size: 0.95rem; margin: 0;'>Ferramenta de análise para pesquisa em Economia Política</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Login / Registro
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔐 Já tem conta? Faça Login", use_container_width=True, key="btn_login"):
            st.session_state["show_login"] = True

    with col2:
        if st.button("📝 Não tem conta? Cadastre-se", use_container_width=True, key="btn_register"):
            st.session_state["show_register"] = True

    st.divider()

    # MODALS
    if st.session_state.get("show_login"):
        _modal_login(api_client)

    if st.session_state.get("show_register"):
        _modal_registro(api_client)

    # SEÇÃO 1: O QUE É AINU?
    st.markdown("### 🌿 O que é AINU?")

    col1, col2, col3 = st.columns(3)

    with col1:
        card(
            "Filosofia Sistêmica",
            "AINU mede o equilíbrio entre gerações, estruturas econômicas e sustentabilidade nutricional de uma nação.",
            "🎯",
            "azul_profundo"
        )

    with col2:
        card(
            "Dados Confiáveis",
            "Integramos dados de UN WPP, World Bank, Yale EPI e fontes nacionais para 29 países.",
            "📊",
            "dourado"
        )

    with col3:
        card(
            "Simulações Interativas",
            "Explore cenários futuros ajustando variáveis e veja como as mudanças afetam índices.",
            "🎮",
            "terracota"
        )

    st.divider()

    # SEÇÃO 2: 6 PAÍSES DESTAQUE
    st.markdown("### 🌍 Países Destaque")

    paises = api_client.get_paises()
    if paises:
        # Selecionar 6 países padrão
        destaque = ["Brasil", "Vietnã", "México", "Japão", "China", "Estados Unidos"]
        paises_selecionados = [p for p in paises if p["nome"] in destaque][:6]

        cols = st.columns(min(3, len(paises_selecionados)))

        for idx, pais in enumerate(paises_selecionados):
            with cols[idx % 3]:
                indices = api_client.get_indices(pais["id"])
                n_star = indices.get("n_estrela", "N/A") if indices else "N/A"
                status_n = indices.get("status_n", "-") if indices else "-"

                st.markdown(
                    f"""
                    <div style='
                        background: {AINU_COLORS['branco']};
                        padding: 1.5rem;
                        border-radius: 0.8rem;
                        border-top: 3px solid {AINU_COLORS['dourado']};
                        text-align: center;
                    '>
                        <h3 style='color: {AINU_COLORS['azul_profundo']}; margin: 0 0 1rem 0;'>{pais["nome"]}</h3>
                        <p style='color: {AINU_COLORS['cinza_claro']}; margin: 0;'>ISO: {pais["codigo_iso"]}</p>
                        <h2 style='color: {AINU_COLORS['dourado']}; margin: 1rem 0 0 0;'>{n_star}</h2>
                        <p style='margin: 0; color: {AINU_COLORS['terracota']}; font-weight: bold;'>{status_n}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        alert("aviso", "Conectando ao servidor...")

    st.divider()
    footer_ainu()

# ===== HOME AUTENTICADA =====

else:
    st.markdown(f"### 👋 Olá, {auth_manager.nome_usuario()}!")

    if auth_manager.esta_aprovado():
        st.success("✓ Sua conta foi aprovada! Acesso total ao sistema.")

        # Stats
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            stat_box("Países", "29", "", "🌍")

        with col2:
            stat_box("N*", "Calculado", "", "📈")

        with col3:
            stat_box("IES", "Calculado", "", "⚖️")

        with col4:
            stat_box("Simulações", "Disponível", "", "🎮")

        st.divider()

        st.markdown("### 📚 Explore o Sistema")
        st.caption("Use o menu lateral para acessar Dashboard, Simuladores e Documentação")

    else:
        alert(
            "aviso",
            f"👤 Sua conta está em revisão. Admin notificará quando aprovada. ({auth_manager.obter_usuario().get('status', 'DESCONHECIDO')})"
        )

        # Mostrar apenas info básicas
        col1, col2 = st.columns(2)

        with col1:
            st.info("📖 Leia sobre AINU em 'Sobre'")

        with col2:
            st.info("❓ Perguntas? Veja 'FAQ'")


# ===== FUNCTIONS =====

def _modal_login(api_client: AIAClient):
    """Modal de login"""
    st.markdown("### 🔐 Login")

    email = st.text_input("Email", key="login_email")
    senha = st.text_input("Senha", type="password", key="login_senha")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Entrar", use_container_width=True, key="btn_login_submit"):
            if email and senha:
                resultado = api_client.login(email, senha)
                if resultado:
                    usuario = api_client.me()
                    if usuario:
                        auth_manager.salvar_token(
                            resultado["access_token"],
                            resultado["refresh_token"],
                            usuario
                        )
                        st.success("✓ Login realizado!")
                        st.session_state["show_login"] = False
                        st.rerun()
            else:
                st.error("Preencha email e senha")

    with col2:
        if st.button("Cancelar", use_container_width=True):
            st.session_state["show_login"] = False
            st.rerun()


def _modal_registro(api_client: AIAClient):
    """Modal de registro"""
    st.markdown("### 📝 Cadastro")

    nome = st.text_input("Nome Completo", key="reg_nome")
    email = st.text_input("Email", key="reg_email")
    senha = st.text_input("Senha (mín. 8 caracteres)", type="password", key="reg_senha")
    instituicao = st.text_input("Instituição (opcional)", key="reg_inst")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Registrar", use_container_width=True, key="btn_reg_submit"):
            if nome and email and len(senha) >= 8:
                resultado = api_client.registrar(nome, email, senha, instituicao)
                if resultado:
                    st.success("✓ Cadastro realizado! Aguarde aprovação do admin.")
                    st.session_state["show_register"] = False
                    st.rerun()
            else:
                st.error("Preencha nome, email e senha (mín. 8 chars)")

    with col2:
        if st.button("Cancelar", use_container_width=True):
            st.session_state["show_register"] = False
            st.rerun()
