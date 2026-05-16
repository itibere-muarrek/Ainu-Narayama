import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Projeções", page_icon="🔮", layout="wide")

st.markdown("# 🔮 Projeções - 10 Anos (2024-2034)")

token = st.session_state.get("token")
if not token:
    st.error("❌ Você precisa estar logado para acessar esta página.")
    st.stop()

st.markdown("### Cenários de Evolução de N* e IES")

col1, col2, col3 = st.columns(3)

with col1:
    cenario = st.selectbox(
        "Selecione cenário:",
        ["Otimista", "Base", "Pessimista"]
    )

with col2:
    pais_proj = st.selectbox(
        "País:",
        ["Nigeria", "Brazil", "Poland", "China", "Japan", "Todos"]
    )

with col3:
    metrica = st.selectbox(
        "Métrica:",
        ["N*", "IES", "Ambas"]
    )

st.markdown("---")

years = list(range(2024, 2035))

if cenario == "Otimista":
    st.markdown("### 📈 Cenário Otimista (Melhorias Globais)")
    col1, col2 = st.columns(2)

    with col1:
        fig_n = go.Figure()
        fig_n.add_trace(go.Scatter(
            x=years, y=[2.5 + i*0.15 for i in range(11)],
            mode='lines+markers', name='Nigeria',
            line=dict(color='#00CC96', width=3)
        ))
        fig_n.add_trace(go.Scatter(
            x=years, y=[1.8 + i*0.10 for i in range(11)],
            mode='lines+markers', name='Brazil',
            line=dict(color='#636EFA', width=3)
        ))
        fig_n.update_layout(title='N* Projetado (Otimista)', height=400)
        st.plotly_chart(fig_n, use_container_width=True)

    with col2:
        fig_ies = go.Figure()
        fig_ies.add_trace(go.Scatter(
            x=years, y=[1.0 + i*0.03 for i in range(11)],
            mode='lines+markers', name='Nigeria',
            line=dict(color='#00CC96', width=3)
        ))
        fig_ies.add_trace(go.Scatter(
            x=years, y=[0.8 + i*0.02 for i in range(11)],
            mode='lines+markers', name='Brazil',
            line=dict(color='#636EFA', width=3)
        ))
        fig_ies.update_layout(title='IES Projetado (Otimista)', height=400)
        st.plotly_chart(fig_ies, use_container_width=True)

elif cenario == "Base":
    st.markdown("### 📊 Cenário Base (Tendência Atual)")
    col1, col2 = st.columns(2)

    with col1:
        fig_n = go.Figure()
        fig_n.add_trace(go.Scatter(
            x=years, y=[2.5 for _ in range(11)],
            mode='lines+markers', name='Nigeria',
            line=dict(color='#00CC96', width=3)
        ))
        fig_n.add_trace(go.Scatter(
            x=years, y=[1.8 - i*0.08 for i in range(11)],
            mode='lines+markers', name='Brazil',
            line=dict(color='#636EFA', width=3)
        ))
        fig_n.add_trace(go.Scatter(
            x=years, y=[0.5 - i*0.05 for i in range(11)],
            mode='lines+markers', name='Poland',
            line=dict(color='#EF553B', width=3)
        ))
        fig_n.update_layout(title='N* Projetado (Base)', height=400)
        st.plotly_chart(fig_n, use_container_width=True)

    with col2:
        fig_ies = go.Figure()
        fig_ies.add_trace(go.Scatter(
            x=years, y=[1.0 for _ in range(11)],
            mode='lines+markers', name='Nigeria',
            line=dict(color='#00CC96', width=3)
        ))
        fig_ies.add_trace(go.Scatter(
            x=years, y=[0.8 - i*0.02 for i in range(11)],
            mode='lines+markers', name='Brazil',
            line=dict(color='#636EFA', width=3)
        ))
        fig_ies.add_trace(go.Scatter(
            x=years, y=[0.4 - i*0.03 for i in range(11)],
            mode='lines+markers', name='Poland',
            line=dict(color='#EF553B', width=3)
        ))
        fig_ies.update_layout(title='IES Projetado (Base)', height=400)
        st.plotly_chart(fig_ies, use_container_width=True)

else:
    st.markdown("### 📉 Cenário Pessimista (Aceleração de Crises)")
    col1, col2 = st.columns(2)

    with col1:
        fig_n = go.Figure()
        fig_n.add_trace(go.Scatter(
            x=years, y=[2.5 - i*0.2 for i in range(11)],
            mode='lines+markers', name='Nigeria',
            line=dict(color='#00CC96', width=3)
        ))
        fig_n.add_trace(go.Scatter(
            x=years, y=[1.8 - i*0.15 for i in range(11)],
            mode='lines+markers', name='Brazil',
            line=dict(color='#636EFA', width=3)
        ))
        fig_n.add_trace(go.Scatter(
            x=years, y=[0.3 - i*0.08 for i in range(11)],
            mode='lines+markers', name='Poland',
            line=dict(color='#EF553B', width=3)
        ))
        fig_n.update_layout(title='N* Projetado (Pessimista)', height=400)
        st.plotly_chart(fig_n, use_container_width=True)

    with col2:
        fig_ies = go.Figure()
        fig_ies.add_trace(go.Scatter(
            x=years, y=[0.9 - i*0.05 for i in range(11)],
            mode='lines+markers', name='Nigeria',
            line=dict(color='#00CC96', width=3)
        ))
        fig_ies.add_trace(go.Scatter(
            x=years, y=[0.7 - i*0.05 for i in range(11)],
            mode='lines+markers', name='Brazil',
            line=dict(color='#636EFA', width=3)
        ))
        fig_ies.add_trace(go.Scatter(
            x=years, y=[0.35 - i*0.05 for i in range(11)],
            mode='lines+markers', name='Poland',
            line=dict(color='#EF553B', width=3)
        ))
        fig_ies.update_layout(title='IES Projetado (Pessimista)', height=400)
        st.plotly_chart(fig_ies, use_container_width=True)

st.markdown("---")

st.markdown("### Previsões por Cenário")

previsoes = {
    "Cenário": ["Otimista", "Base", "Pessimista"],
    "N* Médio 2034": [3.2, 1.8, 0.8],
    "IES Médio 2034": [1.1, 0.75, 0.4],
    "Países Promissores": ["20-24", "12-16", "5-8"],
    "Países em Colapso": ["0-2", "6-9", "12-15"]
}

st.dataframe(
    pd.DataFrame(previsoes),
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

st.markdown("### Fatores de Incerteza")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Fatores Positivos**")
    st.success("""
    - Políticas de educação
    - Acesso a contraceptivos
    - Desenvolvimento econômico
    - Estabilidade política
    """)

with col2:
    st.markdown("**Fatores Negativos**")
    st.error("""
    - Mudanças climáticas
    - Conflitos geopolíticos
    - Crises econômicas
    - Migrações massivas
    """)
