import streamlit as st
import os
from dotenv import load_dotenv

from components.ainu_theme import header_ainu, sidebar_ainu, expandir_secao
from services.auth import auth_manager

load_dotenv()
st.set_page_config(page_title="FAQ - AINU", page_icon="❓", layout="wide")

header_ainu()
sidebar_ainu(auth_manager)

st.markdown("## ❓ Perguntas Frequentes")

st.divider()

st.markdown("### 🔐 Acesso e Autenticação")

expandir_secao(
    "Como me registrar?",
    """
    1. Na Home, clique em **"Cadastre-se"**
    2. Preencha: Nome, Email, Senha (mín. 8 caracteres), Instituição
    3. Clique em **"Registrar"**
    4. Aguarde aprovação do admin (via email)
    5. Após aprovação, faça login
    """,
    "📝"
)

expandir_secao(
    "Esqueci minha senha. O que fazer?",
    """
    Na página de login, clique em **"Recuperar Senha"** e insira seu email.
    Você receberá um link de recuperação no email cadastrado.
    """,
    "🔑"
)

expandir_secao(
    "Minha conta está pendente. Quanto tempo leva para aprovação?",
    """
    O admin revisa cadastros regularmente. Normalmente, aprovações ocorrem
    em até 24 horas. Verifique seu email para notificação de aprovação.
    """,
    "⏳"
)

st.divider()

st.markdown("### 📊 Sobre os Índices")

expandir_secao(
    "Como N* é calculado?",
    """
    **N* = NGII × Fator Geracional**

    Onde:
    - **NGII** = (Pop_Base / Pop_Topo) × (Nascimentos / Mortes)
    - **Fator_Ger** = TFR_2024 / TFR_1999

    Compara **dinâmica geracional atual com 25 anos atrás**.
    """,
    "📐"
)

expandir_secao(
    "Como IES é calculado?",
    """
    **IES = L × ∛(NGII × NCII × NSII)**

    Integra 4 dimensões:
    - **NGII**: Dinâmica geracional
    - **NCII**: Competitividade econômica
    - **NSII**: Saúde nutricional
    - **L**: Glocalização

    Resultado entre 0 e 2+. Maior = mais sustentável.
    """,
    "📐"
)

expandir_secao(
    "Qual é a diferença entre PROMISSOR, EQUILÍBRIO, CRÍTICO e COLAPSO?",
    """
    Baseado no **N* (Índice Geracional)**:

    - 🟢 **PROMISSOR** (N* ≥ 1.5): País em crescimento geracional
    - 🔵 **EQUILÍBRIO** (1.0-1.5): Substituição de gerações estável
    - 🟠 **CRÍTICO** (0.5-1.0): Primeira sinais de contração
    - 🔴 **COLAPSO** (< 0.5): Envelhecimento severo

    Cada status sugere diferentes políticas.
    """,
    "📊"
)

st.divider()

st.markdown("### 🎮 Usando os Simuladores")

expandir_secao(
    "Como funciona o Simulador N*?",
    """
    1. Selecione até **2 países**
    2. Use **sliders** para ajustar variáveis (±25%):
       - População base e topo
       - Nascimentos e mortes
       - TFR 2024 e 1999
    3. Veja cálculos em tempo real
    4. Clique **"SIMULAR"** para análise completa
    5. Escolha **"SALVAR"** ou **"DESCARTAR"**
    """,
    "🎮"
)

expandir_secao(
    "Como funciona o Simulador IES?",
    """
    Similar ao N*, mas explora 4 dimensões:

    **Econômica (NCII)**: VA, Emprego, Salários
    **Glocalizada (L)**: Retorno Local, Competitividade, Simbolismo
    **Nutricional (NSII)**: Yale EPI, Ultraprocessados, Agrotóxicos, Medicalização
    **Saúde (NIH)**: Consequências para bem-estar

    Resultado visualizado em **RADAR 4D** interativo.
    """,
    "🎮"
)

expandir_secao(
    "Qual é a diferença entre SALVAR e DESCARTAR?",
    """
    - **DESCARTAR**: Simulação não é salva na ficha (apenas para exploração rápida)
    - **SALVAR**: Simulação é armazenada em "Minhas Simulações" para referência futura

    Ambas são registradas nos logs de auditoria.
    """,
    "💾"
)

st.divider()

st.markdown("### 📈 Dados e Atualizações")

expandir_secao(
    "De onde vêm os dados?",
    """
    - **UN WPP** (World Population Prospects): População, TFR, nascimentos, mortes
    - **World Bank**: Valor Agregado, emprego, salários
    - **Yale EPI**: Qualidade ambiental e saúde
    - **Fontes Nacionais**: Dados específicos dos 29 países

    Todos são **dados públicos e validados**.
    """,
    "📚"
)

expandir_secao(
    "Com que frequência os dados são atualizados?",
    """
    Os dados são coletados e recalculados **automaticamente** toda sexta-feira
    às 14:00 horário de São Paulo (equivalente a sábado 00:00 Nagano).

    Você será notificado de atualizações importantes via email.
    """,
    "🔄"
)

expandir_secao(
    "Os dados são públicos? Posso usar em pesquisa?",
    """
    **Sim!** AINU agrega dados públicos de fontes reconhecidas internacionalmente.

    Para uso em publicações, recomenda-se:
    1. Citar as fontes originais (UN, World Bank, Yale, etc)
    2. Referenciar AINU-Narayama v3.1.0
    3. Contatar pesquisador: narayama.live@gmail.com
    """,
    "📄"
)

st.divider()

st.markdown("### 🔗 Suporte")

st.info("""
**Mais dúvidas?**

📧 **Email**: narayama.live@gmail.com
📖 **Metodologia**: Veja página dedicada para detalhes técnicos
🌐 **AINU.SYSTEMS**: https://narayama.live
""")
