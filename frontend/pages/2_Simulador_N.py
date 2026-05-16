import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Simulador N*", page_icon="🧮", layout="wide")

st.markdown("# 🧮 Simulador N* (Índice Narayama)")

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
            return []
    except:
        return []


def calcular_n_star(pop_base, pop_topo, nasc, mortes, tfr_atual, tfr_1999):
    NGII_Puro = (pop_base / pop_topo) * (nasc / mortes)
    Fator_Geracional = tfr_atual / tfr_1999
    n_star = NGII_Puro * Fator_Geracional
    return round(n_star, 3)


def get_status_n(n_star):
    if n_star > 1.3:
        return "🟢 PROMISSOR"
    elif 0.9 <= n_star <= 1.3:
        return "🔵 EQUILÍBRIO"
    elif 0.5 <= n_star < 0.9:
        return "🟠 CRÍTICO"
    else:
        return "🔴 COLAPSO"


paises = carregar_paises()

if paises:
    pais_nomes = [p["pais"] for p in paises]
    pais_selecionado = st.selectbox("Selecione um país:", pais_nomes)

    pais_data = next((p for p in paises if p["pais"] == pais_selecionado), None)

    if pais_data:
        st.markdown(f"## {pais_selecionado}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("N* Original", f"{pais_data['n_star']:.3f}", delta=get_status_n(pais_data['n_star']))

        with col2:
            st.metric("Status", get_status_n(pais_data['n_star']))

        with col3:
            st.metric("TFR Atual/1999", f"{pais_data['tfr_atual']:.2f} / {pais_data['tfr_1999']:.2f}")

        st.markdown("---")

        st.markdown("### Ajuste os Parâmetros (±25%)")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**População Base (milhões)**")
            pop_base_original = pais_data["pop_base"]
            pop_base_min = pop_base_original * 0.75
            pop_base_max = pop_base_original * 1.25
            pop_base = st.slider(
                "Pop Base",
                min_value=pop_base_min,
                max_value=pop_base_max,
                value=pop_base_original,
                label_visibility="collapsed"
            )

            st.markdown("**Nascimentos (milhões)**")
            nasc_original = pais_data["nasc"]
            nasc_min = nasc_original * 0.75
            nasc_max = nasc_original * 1.25
            nasc = st.slider(
                "Nascimentos",
                min_value=nasc_min,
                max_value=nasc_max,
                value=nasc_original,
                label_visibility="collapsed"
            )

            st.markdown("**TFR Atual**")
            tfr_atual_original = pais_data["tfr_atual"]
            tfr_atual_min = tfr_atual_original * 0.75
            tfr_atual_max = tfr_atual_original * 1.25
            tfr_atual = st.slider(
                "TFR Atual",
                min_value=tfr_atual_min,
                max_value=tfr_atual_max,
                value=tfr_atual_original,
                label_visibility="collapsed"
            )

        with col2:
            st.markdown("**População Topo (milhões)**")
            pop_topo_original = pais_data["pop_topo"]
            pop_topo_min = pop_topo_original * 0.75
            pop_topo_max = pop_topo_original * 1.25
            pop_topo = st.slider(
                "Pop Topo",
                min_value=pop_topo_min,
                max_value=pop_topo_max,
                value=pop_topo_original,
                label_visibility="collapsed"
            )

            st.markdown("**Mortes (milhões)**")
            mortes_original = pais_data["mortes"]
            mortes_min = mortes_original * 0.75
            mortes_max = mortes_original * 1.25
            mortes = st.slider(
                "Mortes",
                min_value=mortes_min,
                max_value=mortes_max,
                value=mortes_original,
                label_visibility="collapsed"
            )

            st.markdown("**TFR 1999**")
            tfr_1999_original = pais_data["tfr_1999"]
            tfr_1999_min = tfr_1999_original * 0.75
            tfr_1999_max = tfr_1999_original * 1.25
            tfr_1999 = st.slider(
                "TFR 1999",
                min_value=tfr_1999_min,
                max_value=tfr_1999_max,
                value=tfr_1999_original,
                label_visibility="collapsed"
            )

        st.markdown("---")

        n_star_simulado = calcular_n_star(pop_base, pop_topo, nasc, mortes, tfr_atual, tfr_1999)
        status_simulado = get_status_n(n_star_simulado)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("N* Simulado", f"{n_star_simulado:.3f}")

        with col2:
            st.metric("Status Simulado", status_simulado)

        with col3:
            diferenca = n_star_simulado - pais_data["n_star"]
            pct_diferenca = (diferenca / pais_data["n_star"]) * 100 if pais_data["n_star"] != 0 else 0
            st.metric("Variação", f"{diferenca:+.3f}", delta=f"{pct_diferenca:+.1f}%")

        with col4:
            if abs(n_star_simulado - pais_data["n_star"]) > 0.1:
                st.warning("⚠️ Mudança significativa")
            else:
                st.success("✓ Mudança pequena")

        st.markdown("---")

        st.markdown("### Comparação")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Fórmula de N***")
            st.code("""
N* = NGII_Puro × Fator_Geracional

NGII_Puro = (pop_base / pop_topo) × (nasc / mortes)
Fator_Geracional = tfr_atual / tfr_1999
            """)

        with col2:
            st.markdown("**Interpretação**")
            st.info("""
- **N* > 1.3**: 🟢 PROMISSOR (população crescente saudável)
- **0.9 ≤ N* ≤ 1.3**: 🔵 EQUILÍBRIO (população estável)
- **0.5 ≤ N* < 0.9**: 🟠 CRÍTICO (população em risco)
- **N* < 0.5**: 🔴 COLAPSO (população em declínio acelerado)
            """)

        fig = px.bar(
            x=["Original", "Simulado"],
            y=[pais_data["n_star"], n_star_simulado],
            title="N* - Comparação Original vs Simulado",
            labels={"y": "N*", "x": "Cenário"},
            color=["#636EFA", "#EF553B"],
            text=[f"{pais_data['n_star']:.3f}", f"{n_star_simulado:.3f}"]
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

else:
    st.error("⚠️ Erro ao carregar dados")
