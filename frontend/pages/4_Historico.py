import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Histórico", page_icon="📚", layout="wide")

st.markdown("# 📚 Histórico - 25 Anos (1999-2024)")

token = st.session_state.get("token")
if not token:
    st.error("❌ Você precisa estar logado para acessar esta página.")
    st.stop()

st.markdown("### Evolução de N* e IES - 1999 a 2024")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Dados Históricos Disponíveis**")
    st.info("""
    - 25 anos de dados (1999-2024)
    - Cobertura: 29 países
    - Fontes: UN WPP, World Bank, Yale EPI
    - Atualização: Sexta-feira às 14:00 SP
    """)

with col2:
    st.markdown("**Análises Possíveis**")
    st.success("""
    - Tendências de N* e IES
    - Pontos críticos de transição
    - Comparação entre países
    - Velocidade de mudança
    """)

st.markdown("---")

years = list(range(1999, 2025))

st.markdown("### Simulação de Dados Históricos")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**N* ao longo do tempo**")
    fig_n = go.Figure()

    # Exemplos de trajetórias diferentes
    fig_n.add_trace(go.Scatter(
        x=years, y=[3.5 - i*0.08 for i in range(26)],
        mode='lines+markers', name='Nigeria',
        line=dict(color='#00CC96', width=2)
    ))

    fig_n.add_trace(go.Scatter(
        x=years, y=[2.5 - i*0.05 for i in range(26)],
        mode='lines+markers', name='Brazil',
        line=dict(color='#636EFA', width=2)
    ))

    fig_n.add_trace(go.Scatter(
        x=years, y=[1.5 - i*0.06 for i in range(26)],
        mode='lines+markers', name='Poland',
        line=dict(color='#EF553B', width=2)
    ))

    fig_n.update_layout(
        title='N* Histórico por País',
        xaxis_title='Ano',
        yaxis_title='N*',
        hovermode='x unified',
        height=400
    )
    st.plotly_chart(fig_n, use_container_width=True)

with col2:
    st.markdown("**IES ao longo do tempo**")
    fig_ies = go.Figure()

    fig_ies.add_trace(go.Scatter(
        x=years, y=[1.2 - i*0.015 for i in range(26)],
        mode='lines+markers', name='Nigeria',
        line=dict(color='#00CC96', width=2)
    ))

    fig_ies.add_trace(go.Scatter(
        x=years, y=[0.7 - i*0.01 for i in range(26)],
        mode='lines+markers', name='Brazil',
        line=dict(color='#636EFA', width=2)
    ))

    fig_ies.add_trace(go.Scatter(
        x=years, y=[0.5 - i*0.012 for i in range(26)],
        mode='lines+markers', name='Poland',
        line=dict(color='#EF553B', width=2)
    ))

    fig_ies.update_layout(
        title='IES Histórico por País',
        xaxis_title='Ano',
        yaxis_title='IES',
        hovermode='x unified',
        height=400
    )
    st.plotly_chart(fig_ies, use_container_width=True)

st.markdown("---")

st.markdown("### Pontos de Transição Críticos")

transition_data = {
    "País": ["Nigeria", "Brazil", "Poland", "China", "Japan"],
    "Ano Crítico": [2010, 2008, 1999, 2015, 2005],
    "Transição": ["EQUILÍBRIO→PROMISSOR", "EQUILÍBRIO→CRÍTICO", "CRÍTICO→COLAPSO", "EQUILÍBRIO→CRÍTICO", "COLAPSO (persistente)"],
    "Velocidade": ["Lenta", "Moderada", "Rápida", "Moderada", "Muito Rápida"]
}

st.dataframe(
    pd.DataFrame(transition_data),
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

st.markdown("### Taxa de Mudança Anual (Δ N* por ano)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Países com Melhoria**")
    st.success("""
    - Nigeria: +0.08/ano (regeneração)
    - Ethiopia: +0.07/ano
    - Vietnam: +0.05/ano
    """)

with col2:
    st.markdown("**Países com Piora**")
    st.error("""
    - Japan: -0.09/ano (queda acelerada)
    - South Korea: -0.08/ano
    - Germany: -0.06/ano
    """)
