import streamlit as st
import os
from dotenv import load_dotenv

from services.auth import auth_manager
from services.api_client import AIAClient
from components.ainu_theme import header_ainu, sidebar_ainu, alert
from components.simulador_ies import simulador_ies_interativo

load_dotenv()
st.set_page_config(page_title="Simulador IES - AINU", page_icon="🎮", layout="wide")

BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")

if not auth_manager.esta_autenticado() or not auth_manager.esta_aprovado():
    st.error("❌ Acesso negado.")
    st.stop()

api_client = AIAClient(BACKEND_URL, auth_manager.obter_token())

header_ainu()
sidebar_ainu(auth_manager)

st.markdown("## 🎮 Simulador IES (Estabilidade Sistêmica)")
st.caption("Explore mudanças estruturais e seu impacto no equilíbrio 4D")

paises = api_client.get_paises()

if not paises:
    alert("erro", "Erro ao carregar dados")
    st.stop()

simulador_ies_interativo(paises, api_client)
