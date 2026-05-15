import streamlit as st
import os
from dotenv import load_dotenv

from components.ainu_theme import header_ainu, sidebar_ainu, alert, AINU_COLORS
from services.auth import auth_manager

load_dotenv()
st.set_page_config(page_title="Contato - AINU", page_icon="📧", layout="wide")

header_ainu()
sidebar_ainu(auth_manager)

st.markdown("## 📧 Fale Conosco")
st.caption("Envie mensagens, críticas ou sugestões para o pesquisador")

st.divider()

# Formulário
st.markdown("### 📝 Formulário de Contato")

col1, col2 = st.columns([2, 1])

with col1:
    nome = st.text_input(
        "Seu Nome",
        value=auth_manager.nome_usuario() if auth_manager.esta_autenticado() else ""
    )

    email = st.text_input(
        "Seu Email",
        value=auth_manager.email_usuario() if auth_manager.esta_autenticado() else ""
    )

with col2:
    assunto = st.selectbox(
        "Assunto",
        [
            "Dúvida",
            "Sugestão de melhoria",
            "Bug/Erro",
            "Pesquisa/Colaboração",
            "Outro"
        ]
    )

mensagem = st.text_area(
    "Sua Mensagem",
    height=200,
    placeholder="Digite aqui sua mensagem..."
)

col_submit, col_clear = st.columns(2)

with col_submit:
    if st.button("📨 ENVIAR", use_container_width=True):
        if nome and email and mensagem:
            # Simular envio (em produção: integrar com API)
            st.success("""
            ✓ Mensagem enviada com sucesso!

            O pesquisador receberá seu contato e responderá em breve.
            Obrigado por sua contribuição!
            """)
        else:
            st.error("❌ Preencha todos os campos obrigatórios")

with col_clear:
    if st.button("🔄 LIMPAR", use_container_width=True):
        st.rerun()

st.divider()

# Informações de contato
st.markdown("### 📞 Informações Diretas")

st.markdown(f"""
**Pesquisador:**
Itiberê L G C Muarrek

**Email:**
narayama.live@gmail.com

**Instituição:**
Universidade de São Paulo (USP)
Programa de Pós-Graduação em Economia Política

**Horário de Resposta:**
Segunda-feira a Sexta-feira, 09:00-17:00 (Brasília)

---

**Redes Sociais e Links:**
- 🌐 Website: https://narayama.live
- 📚 Pesquisa: https://usp.br/
""")

st.divider()

# Feedback rápido
st.markdown("### 👍 Feedback Rápido")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("👍 Gostei!", use_container_width=True):
        st.balloons()
        st.success("Obrigado pelo feedback positivo!")

with col2:
    if st.button("😐 Neutro", use_container_width=True):
        st.info("Seu feedback nos ajuda a melhorar!")

with col3:
    if st.button("👎 Posso melhorar", use_container_width=True):
        st.warning("Use o formulário acima para detalhar melhorias!")

st.divider()

# FAQ rápido
st.markdown("### ❓ Respostas Rápidas")

st.markdown("""
**P: Quanto tempo leva para responder?**
R: Geralmente 24-48 horas úteis.

**P: Posso sugerir novos países?**
R: Sim! Envie a solicitação com contexto da pesquisa.

**P: Como cito este trabalho?**
R: Use: Muarrek, I. L. G. C. (2024). AINU-Narayama v3.1.0.

**P: Posso usar os dados comercialmente?**
R: Não recomendado. Para uso comercial, entre em contato.
""")
