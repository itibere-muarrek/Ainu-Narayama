import streamlit as st
from components.ainu_theme import header_ainu, card, AINU_COLORS
from components.auth import fazer_login, fazer_cadastro


def mostrar_home_publico():
    """
    Home para usuários NÃO LOGADOS
    """

    header_ainu()

    # HERO SECTION
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            f"""
            <div style='text-align: center; padding: 40px;'>
                <h1 style='color: {AINU_COLORS["dourado"]}; font-size: 3rem;'>
                    ÍNDICE DE NARAYAMA SISTÊMICO
                </h1>
                <p style='color: {AINU_COLORS["azul_profundo"]}; font-size: 1.3rem;'>
                    Medindo o equilíbrio socioeconômico de 29 países
                </p>
                <hr style='border: 1px solid {AINU_COLORS["terracota"]};'>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # BOTÕES DE LOGIN/CADASTRO (POSICIONADOS CORRETAMENTE!)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔐 JÁ TEM CONTA? FAÇA LOGIN", use_container_width=True, key="btn_login_home"):
            st.session_state.show_login_modal = True

    with col2:
        if st.button("📝 NÃO TEM CONTA? CADASTRE-SE", use_container_width=True, key="btn_signup_home"):
            st.session_state.show_signup_modal = True

    st.divider()

    # MODAL LOGIN
    if st.session_state.get("show_login_modal", False):
        mostrar_modal_login()

    # MODAL CADASTRO
    if st.session_state.get("show_signup_modal", False):
        mostrar_modal_cadastro()

    # SEÇÃO: O QUE É AINU?
    st.markdown("### 🌿 O que é AINU?")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div style='background: {AINU_COLORS["creme"]}; padding: 20px; border-radius: 10px; border-left: 4px solid {AINU_COLORS["dourado"]};'>
                <h4 style='color: {AINU_COLORS["dourado"]}; margin-top: 0;'>🎯 Filosofia Sistêmica</h4>
                <p style='color: {AINU_COLORS["azul_profundo"]};'>AINU mede o equilíbrio entre gerações, estruturas econômicas e sustentabilidade.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div style='background: {AINU_COLORS["creme"]}; padding: 20px; border-radius: 10px; border-left: 4px solid {AINU_COLORS["azul_claro"]};'>
                <h4 style='color: {AINU_COLORS["azul_claro"]}; margin-top: 0;'>📊 Dados Confiáveis</h4>
                <p style='color: {AINU_COLORS["azul_profundo"]};'>Coletamos de UN WPP, World Bank, Yale EPI e fontes nacionais.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div style='background: {AINU_COLORS["creme"]}; padding: 20px; border-radius: 10px; border-left: 4px solid {AINU_COLORS["verde"]};'>
                <h4 style='color: {AINU_COLORS["verde"]}; margin-top: 0;'>🎮 Simulações</h4>
                <p style='color: {AINU_COLORS["azul_profundo"]};'>Explore cenários futuros e veja como mudam os índices.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # SEÇÃO: 6 PAÍSES DESTAQUE
    st.markdown("### 📊 Países em Destaque")
    cols = st.columns(3)
    destaque = [
        ("Brasil", "🇧🇷", "0.695", "EQUILÍBRIO"),
        ("Vietnã", "🇻🇳", "1.37", "PROMISSOR"),
        ("Japão", "🇯🇵", "0.584", "CRÍTICO"),
    ]

    for i, (pais, emoji, n_star, status) in enumerate(destaque):
        with cols[i]:
            st.metric(f"{emoji} {pais}", f"N* = {n_star}", status)


def mostrar_modal_login():
    """Modal de login"""
    with st.form("login_form"):
        st.subheader("🔐 Fazer Login")

        email = st.text_input("📧 Email:", key="login_email")
        senha = st.text_input("🔑 Senha:", type="password", key="login_senha")

        col1, col2 = st.columns(2)

        with col1:
            if st.form_submit_button("Entrar", use_container_width=True):
                if email and senha:
                    fazer_login(email, senha)
                    st.session_state.show_login_modal = False
                else:
                    st.error("❌ Preencha email e senha!")

        with col2:
            if st.form_submit_button("Cancelar", use_container_width=True):
                st.session_state.show_login_modal = False
                st.rerun()


def mostrar_modal_cadastro():
    """Modal de cadastro"""
    with st.form("signup_form"):
        st.subheader("📝 Cadastre-se")

        nome = st.text_input("👤 Nome completo:", key="signup_nome")
        email = st.text_input("📧 Email:", key="signup_email")
        senha = st.text_input("🔑 Senha:", type="password", key="signup_senha")
        instituicao = st.text_input("🏢 Instituição/Empresa:", key="signup_inst", value="")

        col1, col2 = st.columns(2)

        with col1:
            if st.form_submit_button("Criar Conta", use_container_width=True):
                if nome and email and senha:
                    if fazer_cadastro(nome, email, senha, instituicao):
                        st.session_state.show_signup_modal = False
                        st.rerun()
                else:
                    st.error("❌ Preencha nome, email e senha!")

        with col2:
            if st.form_submit_button("Cancelar", use_container_width=True):
                st.session_state.show_signup_modal = False
                st.rerun()
