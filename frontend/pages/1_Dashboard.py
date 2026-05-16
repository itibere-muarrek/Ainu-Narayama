import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.markdown("# 📊 Dashboard Global - 29 Países")

token = st.session_state.get("token")
if not token:
    st.error("❌ Você precisa estar logado para acessar esta página.")
    st.stop()


def carregar_paises():
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/v1/paises/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error("❌ Erro ao carregar países")
            return []
    except Exception as e:
        st.error(f"❌ Erro de conexão: {str(e)}")
        return []


paises = carregar_paises()

if paises:
    df = pd.DataFrame(paises)

    # KPIs
    col1, col2, col3, col4, col5 = st.columns(5)

    promissores = len([p for p in paises if p.get("status_n") == "PROMISSOR"])
    criticos = len([p for p in paises if p.get("status_n") == "CRÍTICO"])
    colapso = len([p for p in paises if p.get("status_n") == "COLAPSO"])
    equilibrio = len([p for p in paises if p.get("status_n") == "EQUILÍBRIO"])

    with col1:
        st.metric("🟢 Promissores", promissores)
    with col2:
        st.metric("🔵 Equilíbrio", equilibrio)
    with col3:
        st.metric("🟠 Críticos", criticos)
    with col4:
        st.metric("🔴 Colapso", colapso)
    with col5:
        st.metric("🌍 Total", len(paises))

    st.markdown("---")

    # Filtro
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.multiselect(
            "Filtrar por Status N*:",
            ["PROMISSOR", "EQUILÍBRIO", "CRÍTICO", "COLAPSO"],
            default=["PROMISSOR", "EQUILÍBRIO", "CRÍTICO", "COLAPSO"]
        )

    with col2:
        ordem = st.selectbox("Ordenar por:", ["N* (decrescente)", "IES (decrescente)", "País (A-Z)"])

    df_filtrado = df[df["status_n"].isin(status_filter)].copy()

    if ordem == "N* (decrescente)":
        df_filtrado = df_filtrado.sort_values("n_star", ascending=False)
    elif ordem == "IES (decrescente)":
        df_filtrado = df_filtrado.sort_values("ies", ascending=False)
    else:
        df_filtrado = df_filtrado.sort_values("pais", ascending=True)

    # Tabela
    st.markdown("### 📋 Tabela de Países")
    colunas_exibir = ["pais", "n_star", "status_n", "ies", "status_ies", "tfr_atual", "tfr_1999"]
    st.dataframe(
        df_filtrado[colunas_exibir],
        use_container_width=True,
        hide_index=True,
        column_config={
            "pais": st.column_config.TextColumn("País", width="medium"),
            "n_star": st.column_config.NumberColumn("N*", format="%.3f", width="small"),
            "status_n": st.column_config.TextColumn("Status N*", width="medium"),
            "ies": st.column_config.NumberColumn("IES", format="%.3f", width="small"),
            "status_ies": st.column_config.TextColumn("Status IES", width="medium"),
            "tfr_atual": st.column_config.NumberColumn("TFR Atual", format="%.2f", width="small"),
            "tfr_1999": st.column_config.NumberColumn("TFR 1999", format="%.2f", width="small"),
        }
    )

    st.markdown("---")

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        fig_n = px.scatter(
            df_filtrado,
            x="tfr_atual",
            y="n_star",
            color="status_n",
            hover_name="pais",
            title="N* vs TFR Atual",
            color_discrete_map={
                "PROMISSOR": "#00CC96",
                "EQUILÍBRIO": "#636EFA",
                "CRÍTICO": "#FFA15A",
                "COLAPSO": "#EF553B"
            }
        )
        st.plotly_chart(fig_n, use_container_width=True)

    with col2:
        fig_ies = px.scatter(
            df_filtrado,
            x="L",
            y="ies",
            color="status_ies",
            hover_name="pais",
            title="IES vs Fator L",
            color_discrete_map={
                "SAUDÁVEL": "#00CC96",
                "ESTÁVEL": "#636EFA",
                "FRÁGIL": "#FFA15A",
                "CRÍTICO": "#EF553B"
            }
        )
        st.plotly_chart(fig_ies, use_container_width=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        status_counts = df_filtrado["status_n"].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Distribuição Status N*",
            color_discrete_map={
                "PROMISSOR": "#00CC96",
                "EQUILÍBRIO": "#636EFA",
                "CRÍTICO": "#FFA15A",
                "COLAPSO": "#EF553B"
            }
        )
        st.plotly_chart(fig_status, use_container_width=True)

    with col2:
        ies_counts = df_filtrado["status_ies"].value_counts()
        fig_ies_dist = px.pie(
            values=ies_counts.values,
            names=ies_counts.index,
            title="Distribuição Status IES",
            color_discrete_map={
                "SAUDÁVEL": "#00CC96",
                "ESTÁVEL": "#636EFA",
                "FRÁGIL": "#FFA15A",
                "CRÍTICO": "#EF553B"
            }
        )
        st.plotly_chart(fig_ies_dist, use_container_width=True)

else:
    st.warning("⚠️ Nenhum dado disponível")
