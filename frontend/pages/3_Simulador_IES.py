import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Simulador IES", page_icon="⚖️", layout="wide")

st.markdown("# ⚖️ Simulador IES (Índice Equilíbrio Sistêmico)")

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


def calcular_nih(T, U, M, I):
    return max(0.35, min(0.85, 1 - (0.35*T + 0.25*U + 0.20*M + 0.20*I)))


def calcular_nsii(L, A_ext, NIH):
    return 0.45*A_ext + 0.55*NIH


def calcular_ies(L, NGII, NCII, NSII):
    return L * (NGII * NCII * NSII) ** (1/3)


def get_status_ies(ies):
    if ies > 0.8:
        return "🟢 SAUDÁVEL"
    elif 0.6 <= ies <= 0.8:
        return "🔵 ESTÁVEL"
    elif 0.4 <= ies < 0.6:
        return "🟡 FRÁGIL"
    else:
        return "🔴 CRÍTICO"


paises = carregar_paises()

if paises:
    pais_nomes = [p["pais"] for p in paises]
    pais_selecionado = st.selectbox("Selecione um país:", pais_nomes)

    pais_data = next((p for p in paises if p["pais"] == pais_selecionado), None)

    if pais_data:
        st.markdown(f"## {pais_selecionado}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("IES Original", f"{pais_data['ies']:.3f}", delta=get_status_ies(pais_data['ies']))

        with col2:
            st.metric("Status", get_status_ies(pais_data['ies']))

        with col3:
            st.metric("L (Fator)", f"{pais_data['L']:.2f}")

        st.markdown("---")

        st.markdown("### Ajuste os Parâmetros (±25%)")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**L (Fator de Ligação)**")
            L_original = pais_data["L"]
            L_min = L_original * 0.75
            L_max = L_original * 1.25
            L = st.slider(
                "L",
                min_value=L_min,
                max_value=L_max,
                value=L_original,
                label_visibility="collapsed"
            )

            st.markdown("**A_ext (Amplitude Extensão)**")
            A_ext_original = pais_data["A_ext"]
            A_ext_min = A_ext_original * 0.75
            A_ext_max = A_ext_original * 1.25
            A_ext = st.slider(
                "A_ext",
                min_value=A_ext_min,
                max_value=A_ext_max,
                value=A_ext_original,
                label_visibility="collapsed"
            )

            st.markdown("**T (Taxa Limitante)**")
            T_original = pais_data["T"]
            T_min = T_original * 0.75
            T_max = T_original * 1.25
            T = st.slider(
                "T",
                min_value=T_min,
                max_value=T_max,
                value=T_original,
                label_visibility="collapsed"
            )

            st.markdown("**U (Fator Instabilidade)**")
            U_original = pais_data["U"]
            U_min = U_original * 0.75
            U_max = U_original * 1.25
            U = st.slider(
                "U",
                min_value=U_min,
                max_value=U_max,
                value=U_original,
                label_visibility="collapsed"
            )

        with col2:
            st.markdown("**M (Fator Mobilidade)**")
            M_original = pais_data["M"]
            M_min = M_original * 0.75
            M_max = M_original * 1.25
            M = st.slider(
                "M",
                min_value=M_min,
                max_value=M_max,
                value=M_original,
                label_visibility="collapsed"
            )

            st.markdown("**I (Fator Inércia)**")
            I_original = pais_data["I"]
            I_min = I_original * 0.75
            I_max = I_original * 1.25
            I = st.slider(
                "I",
                min_value=I_min,
                max_value=I_max,
                value=I_original,
                label_visibility="collapsed"
            )

            st.markdown("**NCII (Índice Capacidade)**")
            NCII_original = pais_data["ncii"]
            NCII_min = NCII_original * 0.75
            NCII_max = NCII_original * 1.25
            NCII = st.slider(
                "NCII",
                min_value=NCII_min,
                max_value=NCII_max,
                value=NCII_original,
                label_visibility="collapsed"
            )

            st.markdown("**NGII (Índice Geração)**")
            NGII = (pais_data["pop_base"] / pais_data["pop_topo"])

        st.markdown("---")

        NIH = calcular_nih(T, U, M, I)
        NSII = calcular_nsii(L, A_ext, NIH)
        ies_simulado = calcular_ies(L, NGII, NCII, NSII)

        status_simulado = get_status_ies(ies_simulado)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("IES Simulado", f"{ies_simulado:.3f}")

        with col2:
            st.metric("Status Simulado", status_simulado)

        with col3:
            diferenca = ies_simulado - pais_data["ies"]
            pct_diferenca = (diferenca / pais_data["ies"]) * 100 if pais_data["ies"] != 0 else 0
            st.metric("Variação", f"{diferenca:+.3f}", delta=f"{pct_diferenca:+.1f}%")

        with col4:
            st.metric("NIH Calculado", f"{NIH:.3f}")

        st.markdown("---")

        st.markdown("### Fórmulas")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**IES (Índice Equilíbrio Sistêmico)**")
            st.code("""
IES = L × ∛(NGII × NCII × NSII)

NIH = 1 − (0.35·T + 0.25·U + 0.20·M + 0.20·I)
      [piso 0.35, teto 0.85]

NSII = 0.45·A_ext + 0.55·NIH
            """)

        with col2:
            st.markdown("**Interpretação**")
            st.info("""
- **IES > 0.8**: 🟢 SAUDÁVEL (sistema robusto)
- **0.6 ≤ IES ≤ 0.8**: 🔵 ESTÁVEL (sistema balanceado)
- **0.4 ≤ IES < 0.6**: 🟡 FRÁGIL (risco moderado)
- **IES < 0.4**: 🔴 CRÍTICO (sistema instável)
            """)

        st.markdown("---")

        fig = px.bar(
            x=["Original", "Simulado"],
            y=[pais_data["ies"], ies_simulado],
            title="IES - Comparação Original vs Simulado",
            labels={"y": "IES", "x": "Cenário"},
            color=["#636EFA", "#EF553B"],
            text=[f"{pais_data['ies']:.3f}", f"{ies_simulado:.3f}"]
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

else:
    st.error("⚠️ Erro ao carregar dados")
