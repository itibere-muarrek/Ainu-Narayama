import streamlit as st
import os
from dotenv import load_dotenv

from components.ainu_theme import topbar_ainu, header_ainu, sidebar_ainu, footer_ainu
from components.home_publico import mostrar_home_publico
from components.home_cliente import mostrar_home_cliente
from components.auth import fazer_logout

# Config
load_dotenv()
st.set_page_config(
    page_title="AINU-Narayama",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")

# ===== INICIALIZAR SESSION STATE =====
if "jwt_token" not in st.session_state:
    st.session_state.jwt_token = None
if "user_data" not in st.session_state:
    st.session_state.user_data = None
if "show_login_modal" not in st.session_state:
    st.session_state.show_login_modal = False
if "show_signup_modal" not in st.session_state:
    st.session_state.show_signup_modal = False


# ===== LAYOUT SUPERIOR =====

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    st.markdown(
        f"<h1 style='text-align: center; color: #D4AF37;'>🌍 AINU.SYSTEMS</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<p style='text-align: center; color: #C85A54; font-size: 0.9rem;'>Índice de Narayama Sistêmico</p>",
        unsafe_allow_html=True
    )

st.divider()

# ===== TOPBAR =====
col1, col2, col3 = st.columns([2, 3, 2])

with col1:
    st.markdown(
        f"<p style='color: #0A1F3D; font-size: 0.85rem; margin: 0;'>"
        "🌐 <b>PT</b> | EN | ES"
        "</p>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"<p style='color: #C85A54; font-size: 0.85rem; text-align: center; margin: 0;'>"
        "💬 Críticas são bem-vindas, colabore com o projeto."
        "</p>",
        unsafe_allow_html=True
    )

with col3:
    if st.session_state.get("jwt_token"):
        user_name = st.session_state.get("user_data", {}).get("nome", "Usuário")
        st.markdown(
            f"<p style='color: #0A1F3D; font-size: 0.85rem; text-align: right; margin: 0;'>"
            f"👤 Olá, {user_name}"
            "</p>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<p style='color: #E8E8E8; font-size: 0.85rem; text-align: right; margin: 0;'>"
            "👤 Visitante"
            "</p>",
            unsafe_allow_html=True
        )

st.divider()

# ===== CONTEÚDO PRINCIPAL =====

if not st.session_state.get("jwt_token"):
    # ===== HOME PÚBLICA =====
    mostrar_home_publico()

else:
    # ===== HOME AUTENTICADA =====
    mostrar_home_cliente(st.session_state.get("user_data", {}))

    # ===== SIDEBAR PARA USUÁRIOS LOGADOS =====
    with st.sidebar:
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚪 Logout", use_container_width=True):
                fazer_logout()

# ===== FOOTER =====
st.divider()
footer_ainu()
