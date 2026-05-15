import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

from components.auth import redirecionar_se_nao_logado
from services.api_client import AIAClient
from components.ainu_theme import stat_box, status_badge, tabela_formatada, alert

# PROTEÇÃO: Esta deve ser a primeira linha de páginas autenticadas!
redirecionar_se_nao_logado()

# Config
load_dotenv()
st.set_page_config(page_title="Dashboard - AINU", page_icon="📊", layout="wide")

BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")
api_client = AIAClient(BACKEND_URL, st.session_state.get('jwt_token'))

st.markdown(f"## 📊 Dashboard")
user_name = st.session_state.get("user_data", {}).get("nome", "Usuário")
st.caption(f"Olá {user_name}! Visão geral dos 29 países.")

# Carregar países
paises = api_client.get_paises()

if not paises:
    alert("erro", "Não foi possível carregar os dados dos países")
    st.stop()

# Stats gerais
st.markdown("### 📈 Resumo Geral")

# Calcular estatísticas
promissores = 0
equilibrio = 0
criticos = 0
colapso = 0

for pais in paises:
    indices = api_client.get_indices(pais["id"])
    if indices:
        status = indices.get("status_n", "")
        if status == "PROMISSOR":
            promissores += 1
        elif status == "EQUILIBRIO":
            equilibrio += 1
        elif status == "CRITICO":
            criticos += 1
        elif status == "COLAPSO":
            colapso += 1

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Países", len(paises))

with col2:
    st.metric("🟢 Promissores", promissores)

with col3:
    st.metric("🔵 Equilíbrio", equilibrio)

with col4:
    st.metric("🟠 Críticos", criticos)

with col5:
    st.metric("🔴 Colapso", colapso)

st.divider()

# ===== ÍNDICE N* =====

st.markdown("### 📈 Índice N* (Geracional)")

col_select, col_filter = st.columns([2, 1])

with col_select:
    pais_selecionado = st.selectbox(
        "Selecione um país para detalhes",
        [p["nome"] for p in paises],
        key="select_pais_n"
    )

with col_filter:
    filtro_status = st.multiselect(
        "Filtrar por status",
        ["PROMISSOR", "EQUILIBRIO", "CRITICO", "COLAPSO"],
        default=["PROMISSOR", "EQUILIBRIO"],
        key="filter_status_n"
    )

# Pegar país selecionado
pais_sel = next(p for p in paises if p["nome"] == pais_selecionado)
indices_sel = api_client.get_indices(pais_sel["id"])

if indices_sel:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("N*", f"{indices_sel.get('n_estrela', 0):.3f}")

    with col2:
        st.metric("NGII", f"{indices_sel.get('ngii_puro', 0):.3f}")

    with col3:
        st.metric("Fator Geracional", f"{indices_sel.get('fator_geracional', 0):.3f}")

    with col4:
        status = indices_sel.get('status_n', '-')
        st.markdown(f"**Status**: {status_badge(status)}", unsafe_allow_html=True)

# Tabela com 6 países
st.markdown("#### Primeiros 6 Países")

dados_n = []
for pais in paises[:6]:
    indices = api_client.get_indices(pais["id"])
    if indices:
        dados_n.append({
            "País": pais["nome"],
            "ISO": pais["codigo_iso"],
            "N*": f"{indices.get('n_estrela', 0):.3f}",
            "NGII": f"{indices.get('ngii_puro', 0):.3f}",
            "Status": indices.get('status_n', '-')
        })

if dados_n:
    df_n = pd.DataFrame(dados_n)
    tabela_formatada(df_n, status_col="Status")

if st.button("📋 Ver os 29 Países", key="btn_ver_todos_n"):
    # Expandir e mostrar todos
    dados_todos = []
    for pais in paises:
        indices = api_client.get_indices(pais["id"])
        if indices:
            dados_todos.append({
                "País": pais["nome"],
                "ISO": pais["codigo_iso"],
                "Região": pais.get("regiao", "-"),
                "N*": f"{indices.get('n_estrela', 0):.3f}",
                "NGII": f"{indices.get('ngii_puro', 0):.3f}",
                "Fator Ger.": f"{indices.get('fator_geracional', 0):.3f}",
                "Status": indices.get('status_n', '-')
            })

    if dados_todos:
        df_todos = pd.DataFrame(dados_todos)
        st.dataframe(df_todos, use_container_width=True, hide_index=True)

st.divider()

# ===== ÍNDICE IES =====

st.markdown("### ⚖️ Índice IES (Estabilidade Sistêmica)")

col_select2, col_filter2 = st.columns([2, 1])

with col_select2:
    pais_selecionado2 = st.selectbox(
        "Selecione um país para detalhes",
        [p["nome"] for p in paises],
        key="select_pais_ies",
        index=1
    )

with col_filter2:
    filtro_status2 = st.multiselect(
        "Filtrar por status",
        ["ESTAVEL", "TRANSICAO", "CRITICO"],
        default=["ESTAVEL", "TRANSICAO"],
        key="filter_status_ies"
    )

# Pegar país selecionado
pais_sel2 = next(p for p in paises if p["nome"] == pais_selecionado2)
indices_sel2 = api_client.get_indices(pais_sel2["id"])

if indices_sel2:
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("IES", f"{indices_sel2.get('ies', 0):.3f}")

    with col2:
        st.metric("L", f"{indices_sel2.get('l_glocalizado', 0):.3f}")

    with col3:
        st.metric("NCII", f"{indices_sel2.get('ncii', 0):.3f}")

    with col4:
        st.metric("NSII", f"{indices_sel2.get('nsii', 0):.3f}")

    with col5:
        st.metric("NIH", f"{indices_sel2.get('nih', 0):.3f}")

# Tabela IES
st.markdown("#### Primeiros 6 Países")

dados_ies = []
for pais in paises[:6]:
    indices = api_client.get_indices(pais["id"])
    if indices:
        dados_ies.append({
            "País": pais["nome"],
            "L": f"{indices.get('l_glocalizado', 0):.3f}",
            "NCII": f"{indices.get('ncii', 0):.3f}",
            "NSII": f"{indices.get('nsii', 0):.3f}",
            "IES": f"{indices.get('ies', 0):.3f}",
            "Status": indices.get('status_ies', '-')
        })

if dados_ies:
    df_ies = pd.DataFrame(dados_ies)
    tabela_formatada(df_ies, status_col="Status")

if st.button("📋 Ver os 29 Países", key="btn_ver_todos_ies"):
    dados_todos_ies = []
    for pais in paises:
        indices = api_client.get_indices(pais["id"])
        if indices:
            dados_todos_ies.append({
                "País": pais["nome"],
                "ISO": pais["codigo_iso"],
                "L": f"{indices.get('l_glocalizado', 0):.3f}",
                "NCII": f"{indices.get('ncii', 0):.3f}",
                "NSII": f"{indices.get('nsii', 0):.3f}",
                "IES": f"{indices.get('ies', 0):.3f}",
                "Status": indices.get('status_ies', '-')
            })

    if dados_todos_ies:
        df_todos_ies = pd.DataFrame(dados_todos_ies)
        st.dataframe(df_todos_ies, use_container_width=True, hide_index=True)
