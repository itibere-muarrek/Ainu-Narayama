import streamlit as st
import os
from dotenv import load_dotenv

from components.ainu_theme import card, AINU_COLORS

load_dotenv()
st.set_page_config(page_title="Sobre - AINU", page_icon="ℹ️", layout="wide")

st.markdown("## ℹ️ Sobre AINU-Narayama")

st.divider()

# Missão
st.markdown("### 🎯 Missão")

st.markdown("""
**AINU-Narayama** é um sistema de **medição socioeconômica** que fornece índices
científicos para comparar e analisar o **equilíbrio sistêmico** de 29 países.

Desenvolvido como parte de pesquisa em **Economia Política**, o AINU permite:

- 📊 Comparações internacionais estruturadas
- 🎮 Simulações interativas de cenários futuros
- 📈 Acompanhamento automático de indicadores
- 🔬 Análise baseada em dados confiáveis
""")

st.divider()

# Pesquisador
st.markdown("### 👤 Pesquisador")

st.markdown("""
**Itiberê L G C Muarrek**
- Instituição: Universidade de São Paulo (USP)
- Programa: Pós-Graduação em Economia Política
- Email: narayama.live@gmail.com
- Tese: *Economia Política do Equilíbrio Sistêmico*
""")

st.divider()

# Índices
st.markdown("### 📈 Índices Principais")

col1, col2, col3 = st.columns(3)

with col1:
    card(
        "N* (Geracional)",
        "Mede o impacto líquido entre gerações. Compara população base (0-25), topo (65+) e dinâmica de TFR.",
        "👶",
        "azul_profundo"
    )

with col2:
    card(
        "IES (Estabilidade)",
        "Integra 4 dimensões: geracional, econômica, nutricional e glocalizada para avaliar sustentabilidade.",
        "⚖️",
        "dourado"
    )

with col3:
    card(
        "NIH (Saúde)",
        "Índice de saúde nutricional que pondera ultraprocessados, agrotóxicos, medicalização e inflamação.",
        "🥗",
        "terracota"
    )

st.divider()

# 29 Países
st.markdown("### 🌍 29 Países em Análise")

st.markdown("""
A base de dados inclui 29 países distribuídos entre:

**América Latina (8):** Brasil, Argentina, México, Chile, Colômbia, Peru, Uruguai, Paraguai

**Europa (8):** Alemanha, França, Reino Unido, Itália, Espanha, Portugal, Holanda, Suécia

**Ásia (9):** China, Índia, Japão, Vietnã, Tailândia, Indonesia, Filipinas, Paquistão, Bangladesh

**Outros (4):** EUA, Canadá, Austrália, Africa do Sul
""")

st.divider()

# Stack técnico
st.markdown("### 🛠️ Tecnologia")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Backend**
    - Python 3.11
    - FastAPI
    - PostgreSQL
    - SQLAlchemy
    - APScheduler
    """)

with col2:
    st.markdown("""
    **Frontend**
    - Streamlit
    - Plotly
    - Pandas
    - JWT Auth
    """)

st.divider()

# Licença
st.markdown("### 📜 Licença e Copyright")

st.markdown(f"""
© 2024 **Itiberê L G C Muarrek**

Todos os direitos reservados ao pesquisador. AINU-Narayama é uma ferramenta
de pesquisa acadêmica em Economia Política.

**Contato:** narayama.live@gmail.com

---

**Aviso:** Os dados, índices e análises apresentadas nesta plataforma são
fornecidos para fins educacionais e de pesquisa. Recomenda-se validação
independente antes de uso em decisões críticas.
""")
