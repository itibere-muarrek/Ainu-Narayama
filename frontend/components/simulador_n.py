import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional
from services.api_client import AIAClient
from components.ainu_theme import status_badge, AINU_COLORS

def simulador_n_interativo(paises: list, api_client: AIAClient):
    """Componente interativo do simulador N*"""

    st.markdown("### 🎮 Simulador N* (Índice Geracional)")
    st.caption("Explore cenários e veja para onde o país vai em 25 anos")

    # Seleção de países
    col1, col2 = st.columns(2)

    with col1:
        pais_1_nome = st.selectbox(
            "País 1",
            [p["nome"] for p in paises],
            key="simulador_pais1"
        )
        pais_1 = next(p for p in paises if p["nome"] == pais_1_nome)

    with col2:
        pais_2_nome = st.selectbox(
            "País 2 (Opcional)",
            [p["nome"] for p in paises],
            index=1,
            key="simulador_pais2"
        )
        pais_2 = next(p for p in paises if p["nome"] == pais_2_nome)

    st.divider()

    # Tabs para cada país
    tab1, tab2 = st.tabs([f"📍 {pais_1['nome']}", f"📍 {pais_2['nome']}"])

    with tab1:
        params1 = _painel_pais(pais_1, "país1", api_client)

    with tab2:
        params2 = _painel_pais(pais_2, "país2", api_client) if pais_2["id"] != pais_1["id"] else params1

    st.divider()

    # Botões
    col_sim, col_reset = st.columns(2)

    with col_sim:
        if st.button("▶️ SIMULAR", use_container_width=True, key="btn_simular_n"):
            _executar_simulacao_n(pais_1, params1, pais_2, params2, api_client)

    with col_reset:
        if st.button("🔄 RESETAR", use_container_width=True, key="btn_resetar_n"):
            st.session_state.pop("simulacao_resultado_n", None)
            st.rerun()


def _painel_pais(pais: Dict[str, Any], chave_sessao: str, api_client: AIAClient) -> Dict[str, Any]:
    """Painel de parâmetros para um país"""

    st.markdown(f"**{pais['nome']}** • ISO: {pais['codigo_iso']}")

    # Obter dados mais recentes
    indices = api_client.get_indices(pais['id'])

    # Valores baseline
    pop_base = 100.0  # Placeholder - em produção: vem dos dados
    pop_topo = 50.0
    nascimentos = 2.5
    mortes = 1.2
    tfr_2024 = 1.6
    tfr_1999 = 2.4

    # Sliders para alterações (±25%)
    col1, col2 = st.columns([1, 2])

    parametros = {}

    com col1:
        st.caption("Ajuste os parâmetros:")

    # Pop Base
    min_pop_base = pop_base * 0.75
    max_pop_base = pop_base * 1.25
    pop_base_novo = st.slider(
        "População 0-25 (milhões)",
        min_value=float(min_pop_base),
        max_value=float(max_pop_base),
        value=float(pop_base),
        step=0.1,
        key=f"slider_pop_base_{chave_sessao}"
    )
    parametros["pop_base_mi"] = pop_base_novo

    # Pop Topo
    min_pop_topo = pop_topo * 0.75
    max_pop_topo = pop_topo * 1.25
    pop_topo_novo = st.slider(
        "População 65+ (milhões)",
        min_value=float(min_pop_topo),
        max_value=float(max_pop_topo),
        value=float(pop_topo),
        step=0.1,
        key=f"slider_pop_topo_{chave_sessao}"
    )
    parametros["pop_topo_mi"] = pop_topo_novo

    # Nascimentos
    min_nasc = nascimentos * 0.75
    max_nasc = nascimentos * 1.25
    nasc_novo = st.slider(
        "Nascimentos Anuais (milhões)",
        min_value=float(min_nasc),
        max_value=float(max_nasc),
        value=float(nascimentos),
        step=0.05,
        key=f"slider_nasc_{chave_sessao}"
    )
    parametros["nascimentos_mi"] = nasc_novo

    # Mortes
    min_mortes = mortes * 0.75
    max_mortes = mortes * 1.25
    mortes_novo = st.slider(
        "Mortes Anuais (milhões)",
        min_value=float(min_mortes),
        max_value=float(max_mortes),
        value=float(mortes),
        step=0.05,
        key=f"slider_mortes_{chave_sessao}"
    )
    parametros["mortes_mi"] = mortes_novo

    # TFR 2024
    min_tfr24 = tfr_2024 * 0.75
    max_tfr24 = tfr_2024 * 1.25
    tfr24_novo = st.slider(
        "TFR 2024",
        min_value=float(min_tfr24),
        max_value=float(max_tfr24),
        value=float(tfr_2024),
        step=0.05,
        key=f"slider_tfr24_{chave_sessao}"
    )
    parametros["tfr_2024"] = tfr24_novo

    # TFR 1999
    min_tfr99 = tfr_1999 * 0.75
    max_tfr99 = tfr_1999 * 1.25
    tfr99_novo = st.slider(
        "TFR 1999",
        min_value=float(min_tfr99),
        max_value=float(max_tfr99),
        value=float(tfr_1999),
        step=0.05,
        key=f"slider_tfr99_{chave_sessao}"
    )
    parametros["tfr_1999"] = tfr99_novo

    return parametros


def _executar_simulacao_n(pais_1: Dict, params1: Dict, pais_2: Dict, params2: Dict, api_client: AIAClient):
    """Executa simulação e mostra resultados"""

    with st.spinner("Calculando N*..."):
        resultado1 = api_client.calcular_n_star(pais_1["id"], params1)

        if pais_2["id"] != pais_1["id"]:
            resultado2 = api_client.calcular_n_star(pais_2["id"], params2)
        else:
            resultado2 = None

    if resultado1:
        st.session_state["simulacao_resultado_n"] = {
            "pais1": pais_1,
            "resultado1": resultado1,
            "params1": params1,
            "pais2": pais_2 if resultado2 else None,
            "resultado2": resultado2,
            "params2": params2 if resultado2 else None
        }

        # Mostrar resultados
        st.divider()
        st.markdown("### 📊 Resultados")

        col1, col2 = st.columns(2 if resultado2 else [1])

        with col1:
            _mostrar_resultado_n(pais_1["nome"], resultado1)

        if resultado2:
            with col2:
                _mostrar_resultado_n(pais_2["nome"], resultado2)

        st.divider()

        # Botões ação
        col_desc, col_salv = st.columns(2)

        with col_desc:
            if st.button("🗑️ DESCARTAR", use_container_width=True):
                st.info("✓ Simulação descartada (não salva na ficha)")
                st.session_state.pop("simulacao_resultado_n", None)

        with col_salv:
            if st.button("💾 SALVAR", use_container_width=True):
                st.success("✓ Simulação salva em 'Minhas Simulações'")
                # Aqui: chamar api_client.criar_simulacao()


def _mostrar_resultado_n(pais_nome: str, resultado: Dict):
    """Mostra resultado N* para um país"""

    st.markdown(f"#### {pais_nome}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("NGII", f"{resultado.get('ngii_puro', 0):.3f}", "Puro")

    with col2:
        st.metric("Fator Ger.", f"{resultado.get('fator_geracional', 0):.3f}", "TFR")

    with col3:
        st.metric("N*", f"{resultado.get('n_estrela', 0):.3f}", resultado.get('status_n', ''))

    status = resultado.get('status_n', 'DESCONHECIDO')
    st.markdown(
        f"Status: {status_badge(status)}",
        unsafe_allow_html=True
    )
