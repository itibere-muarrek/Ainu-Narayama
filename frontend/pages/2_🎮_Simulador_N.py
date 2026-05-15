import streamlit as st
import os
from dotenv import load_dotenv

from services.auth import auth_manager
from services.api_client import AIAClient
from components.ainu_theme import header_ainu, sidebar_ainu, alert
from components.simulador_n import simulador_n_interativo

load_dotenv()
st.set_page_config(page_title="Simulador N* - AINU", page_icon="🎮", layout="wide")

BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")

# Check auth
if not auth_manager.esta_autenticado() or not auth_manager.esta_aprovado():
    st.error("❌ Acesso negado. Faça login com conta aprovada.")
    st.stop()

api_client = AIAClient(BACKEND_URL, auth_manager.obter_token())

# Layout
header_ainu()
sidebar_ainu(auth_manager)

st.markdown("## 🎮 Simulador N* (Índice Geracional)")
st.caption("Explore cenários demográficos e veja impactos no índice de gerações")

# Carregar países
paises = api_client.get_paises()

if not paises:
    alert("erro", "Não foi possível carregar dados")
    st.stop()

# Simulador
simulador_n_interativo(paises, api_client)
