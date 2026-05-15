import streamlit as st
import os
from dotenv import load_dotenv

from components.ainu_theme import AINU_COLORS, expandir_secao

load_dotenv()
st.set_page_config(page_title="Metodologia - AINU", page_icon="📖", layout="wide")

st.markdown("## 📖 Metodologia AINU")
st.caption("Documentação técnica dos índices e fórmulas")

st.divider()

# Índice N*
st.markdown("### 📈 Índice N* (Net Generational Impact)")

expandir_secao(
    "O que é N*?",
    """
    O Índice N* mede o **impacto geracional líquido** de um país.

    Considera:
    - **População base** (0-25 anos): força de trabalho futura
    - **População topo** (65+ anos): demanda de cuidados
    - **Nascimentos/Mortes anuais**: fluxo geracional
    - **TFR (Taxa de Fecundidade)**: comparação 2024 vs 1999

    **Interpretação:**
    - 🟢 **N* ≥ 1.5**: PROMISSOR - crescimento geracional sustentável
    - 🔵 **N* 1.0-1.5**: EQUILÍBRIO - substituição geracional estável
    - 🟠 **N* 0.5-1.0**: CRÍTICO - contração geracional
    - 🔴 **N* < 0.5**: COLAPSO - envelhecimento severo
    """,
    "❓"
)

st.markdown("**Fórmula:**")
st.latex(r"N^* = \text{NGII}_{puro} = \left(\frac{\text{Pop}_{base}}{\text{Pop}_{topo}}\right) \times \left(\frac{\text{Nascimentos}}{\text{Mortes}}\right) \times \frac{\text{TFR}_{2024}}{\text{TFR}_{1999}}")

st.divider()

# Índice IES
st.markdown("### ⚖️ Índice IES (Stabilidade Econômica Integrada)")

expandir_secao(
    "O que é IES?",
    """
    O Índice IES mede a **estabilidade sistêmica** integrada de 4 dimensões:

    1. **NGII** (Geracional): Dinâmica demográfica
    2. **NCII** (Econômica): Produtividade e distribuição salarial
    3. **NSII** (Nutricional): Saúde e bem-estar alimentar
    4. **L** (Glocalizada): Equilíbrio local-global

    **Status IES:**
    - 🟢 **IES ≥ 1.0**: ESTÁVEL - sistema sustentável
    - 🔵 **IES 0.5-1.0**: TRANSIÇÃO - inflexão possível
    - 🔴 **IES < 0.5**: CRÍTICO - intervenção necessária
    """,
    "❓"
)

st.markdown("**Fórmula:**")
st.latex(r"IES = L \times \sqrt[3]{\text{NGII} \times \text{NCII} \times \text{NSII}}")

st.divider()

# Componentes
st.markdown("### 🔧 Componentes da Fórmula")

expandir_secao(
    "NCII (Competitividade Econômica)",
    """
    $$\\text{NCII} = \\left(\\frac{VA}{Emprego}\\right) \\times \\left(\\frac{Salários}{VA}\\right)$$

    - **VA**: Valor Agregado (PIB)
    - **Emprego**: Total de empregos
    - **Salários**: Total de salários
    - Mede produtividade × distribuição
    """,
    "💼"
)

expandir_secao(
    "NSII (Saúde Nutricional)",
    """
    $$\\text{NSII} = 0.45 \\times A_{ext} + 0.55 \\times NIH$$

    - **A_ext**: Yale EPI Score (meio ambiente)
    - **NIH**: Índice de Saúde Nutricional

    Onde:
    $$NIH = 1 - (0.35T + 0.25U + 0.20M + 0.20I)$$

    - T: Taxa de ultraprocessados
    - U: Taxa de agrotóxicos
    - M: Taxa medicalizada
    - I: Taxa de inflamação
    """,
    "🥗"
)

expandir_secao(
    "L (Glocalização)",
    """
    $$L = 0.4 \\times RET + 0.3 \\times COMP + 0.3 \\times SYM$$

    - **RET**: Retorno Local (fluxos financeiros)
    - **COMP**: Competitividade Regional
    - **SYM**: Simbolismo (identidade sistêmica)
    """,
    "🌍"
)

st.divider()

# Dados
st.markdown("### 📊 Fontes de Dados")

st.markdown("""
- **UN WPP** (United Nations World Population Prospects): População, nascimentos, mortes, TFR
- **World Bank**: VA Bruto, emprego, salários
- **Yale EPI** (Environmental Performance Index): Qualidade ambiental
- **Fontes Nacionais**: Dados adicionais e validação

**Atualização:** Coletada automaticamente toda sexta-feira 14:00 (SP)
""")

st.divider()

st.markdown("### 📚 Referências")

st.markdown("""
- Muarrek, I. L. G. C. (2024). *Economia Política do Equilíbrio Sistêmico*. USP.
- UN DESA, World Population Prospects 2024
- World Bank Open Data
- Yale Center for Environmental Law & Policy
""")
