import streamlit as st
from typing import Optional, Dict, Any

# Cores AINU
AINU_COLORS = {
    "azul_profundo": "#0A1F3D",
    "dourado": "#D4AF37",
    "terracota": "#C85A54",
    "creme": "#F8F4ED",
    "branco": "#FFFFFF",
    "cinza_claro": "#E8E8E8",
    "verde": "#2ECC71",
    "laranja": "#F39C12",
    "vermelho": "#E74C3C",
    "azul_claro": "#3498DB"
}

# Status colors
STATUS_COLORS = {
    "PROMISSOR": AINU_COLORS["verde"],
    "EQUILIBRIO": AINU_COLORS["azul_claro"],
    "CRITICO": AINU_COLORS["laranja"],
    "COLAPSO": AINU_COLORS["vermelho"]
}


def header_ainu():
    """Cabeçalho AINU com logo e título"""
    col1, col2 = st.columns([1, 4])

    with col1:
        st.markdown(
            f"<h1 style='color: {AINU_COLORS['dourado']}; font-size: 2.5rem; margin: 0;'>🌍</h1>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style='padding-top: 0.5rem;'>
                <h1 style='color: {AINU_COLORS['azul_profundo']}; margin: 0; font-size: 2rem;'>AINU.SYSTEMS</h1>
                <p style='color: {AINU_COLORS['terracota']}; margin: 0; font-size: 0.9rem;'>Índice de Narayama Sistêmico</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()


def sidebar_ainu(auth_manager):
    """Sidebar com identidade AINU"""
    with st.sidebar:
        st.markdown(
            f"<p style='text-align: center; color: {AINU_COLORS['dourado']}; font-weight: bold;'>🌿 AINU v3.1.0</p>",
            unsafe_allow_html=True
        )
        st.divider()

        if auth_manager.esta_autenticado():
            st.markdown(
                f"<p style='color: {AINU_COLORS['azul_profundo']};'>👤 {auth_manager.nome_usuario()}</p>",
                unsafe_allow_html=True
            )
            st.caption(f"📧 {auth_manager.email_usuario()}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🚪 Logout", use_container_width=True):
                    auth_manager.logout()
                    st.rerun()

            st.divider()

        st.markdown(
            f"<p style='color: {AINU_COLORS['cinza_claro']}; font-size: 0.8rem;'>"
            "© 2024 Itiberê L G C Muarrek (USP)<br>"
            "Tese: Economia Política<br>"
            "narayama.live@gmail.com"
            "</p>",
            unsafe_allow_html=True,
            unsafe_allow_html=True
        )


def status_badge(status: str, size: str = "md") -> str:
    """Badge com status (HTML)"""
    color = STATUS_COLORS.get(status, AINU_COLORS["cinza_claro"])

    sizes = {
        "sm": ("0.7rem", "0.5rem 1rem"),
        "md": ("0.85rem", "0.6rem 1.2rem"),
        "lg": ("1rem", "0.8rem 1.5rem")
    }

    font_size, padding = sizes.get(size, sizes["md"])

    return f"""
    <span style='
        background-color: {color};
        color: white;
        padding: {padding};
        border-radius: 0.5rem;
        font-size: {font_size};
        font-weight: bold;
        display: inline-block;
    '>{status}</span>
    """


def stat_box(titulo: str, valor: str, unidade: str = "", icon: str = "📊"):
    """Caixa de estatística"""
    st.markdown(
        f"""
        <div style='
            background: linear-gradient(135deg, {AINU_COLORS['creme']} 0%, {AINU_COLORS['branco']} 100%);
            padding: 1.5rem;
            border-radius: 1rem;
            border-left: 4px solid {AINU_COLORS['dourado']};
        '>
            <p style='color: {AINU_COLORS['cinza_claro']}; margin: 0; font-size: 0.85rem;'>{icon} {titulo}</p>
            <h2 style='color: {AINU_COLORS['azul_profundo']}; margin: 0.5rem 0 0 0;'>{valor} <span style='font-size: 0.7em; color: {AINU_COLORS['terracota']};'>{unidade}</span></h2>
        </div>
        """,
        unsafe_allow_html=True
    )


def card(titulo: str, conteudo: str, icon: str = "📌", cor: str = "azul_profundo"):
    """Card informativo"""
    cor_hex = AINU_COLORS.get(cor, AINU_COLORS["azul_profundo"])

    st.markdown(
        f"""
        <div style='
            background: {AINU_COLORS['branco']};
            padding: 1.5rem;
            border-radius: 0.8rem;
            border-top: 3px solid {cor_hex};
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        '>
            <h3 style='color: {cor_hex}; margin-top: 0;'>{icon} {titulo}</h3>
            <p style='color: {AINU_COLORS['azul_profundo']}; line-height: 1.6;'>{conteudo}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def alert(tipo: str, mensagem: str):
    """Alerta customizado"""
    cores = {
        "info": {"bg": "#E3F2FD", "border": AINU_COLORS["azul_claro"], "icon": "ℹ️"},
        "sucesso": {"bg": "#E8F5E9", "border": AINU_COLORS["verde"], "icon": "✓"},
        "aviso": {"bg": "#FFF3E0", "border": AINU_COLORS["laranja"], "icon": "⚠️"},
        "erro": {"bg": "#FFEBEE", "border": AINU_COLORS["vermelho"], "icon": "✕"}
    }

    config = cores.get(tipo, cores["info"])

    st.markdown(
        f"""
        <div style='
            background: {config["bg"]};
            border-left: 4px solid {config["border"]};
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        '>
            <p style='margin: 0; color: {config["border"]}; font-weight: bold;'>{config["icon"]} {mensagem}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def footer_ainu():
    """Footer AINU"""
    st.divider()
    st.markdown(
        f"""
        <div style='text-align: center; padding: 2rem 1rem; color: {AINU_COLORS['cinza_claro']}; font-size: 0.85rem;'>
            <p style='margin: 0.5rem 0;'><strong>AINU-Narayama v3.1.0</strong></p>
            <p style='margin: 0.5rem 0;'>Sistema de Medição Socioeconômica para 29 Países</p>
            <p style='margin: 1rem 0 0 0; font-size: 0.75rem;'>
                © 2024 Itiberê L G C Muarrek (USP) | Tese: Economia Política<br>
                📧 narayama.live@gmail.com
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def tabela_formatada(df, status_col: Optional[str] = None):
    """Mostra dataframe com formatação AINU"""
    # Aplicar formatação de status se coluna informada
    if status_col and status_col in df.columns:
        # Adicionar badges de status
        df[status_col] = df[status_col].apply(
            lambda x: f"🟢 {x}" if x == "PROMISSOR"
            else f"🔵 {x}" if x == "EQUILIBRIO"
            else f"🟠 {x}" if x == "CRITICO"
            else f"🔴 {x}" if x == "COLAPSO"
            else x
        )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            status_col: st.column_config.TextColumn(width="small") if status_col else None
        }
    )


def expandir_secao(titulo: str, conteudo: str, aberto: bool = False):
    """Seção expansível"""
    with st.expander(titulo, expanded=aberto):
        st.markdown(conteudo)
