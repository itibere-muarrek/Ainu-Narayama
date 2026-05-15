import streamlit as st
import os
from dotenv import load_dotenv

from components.auth import redirecionar_se_nao_logado
from services.api_client import AIAClient
from components.ainu_theme import alert
from components.simulador_ies import simulador_ies_interativo

# PROTEÇÃO: Esta deve ser a primeira linha de páginas autenticadas!
redirecionar_se_nao_logado()

load_dotenv()
st.set_page_config(page_title="Simulador IES - AINU", page_icon="🎮", layout="wide")

BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")
api_client = AIAClient(BACKEND_URL, st.session_state.get('jwt_token'))

st.markdown("## 🎮 Simulador IES (Estabilidade Sistêmica)")
st.caption("Explore mudanças estruturais e seu impacto no equilíbrio 4D")

paises = api_client.get_paises()

if not paises:
    alert("erro", "Erro ao carregar dados")
    st.stop()

simulador_ies_interativo(paises, api_client)
