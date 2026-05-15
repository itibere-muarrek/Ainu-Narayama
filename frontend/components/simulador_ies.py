import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, Optional
from services.api_client import AIAClient
from components.ainu_theme import status_badge, AINU_COLORS

def simulador_ies_interativo(paises: list, api_client: AIAClient):
    """Componente interativo do simulador IES"""

    st.markdown("### 🎮 Simulador IES (Estabilidade Sistêmica)")
    st.caption("Explore como mudanças estruturais afetam o equilíbrio")

    # Seleção de países
    col1, col2 = st.columns(2)

    with col1:
        pais_1_nome = st.selectbox(
            "País 1",
            [p["nome"] for p in paises],
            key="simulador_ies_pais1"
        )
        pais_1 = next(p for p in paises if p["nome"] == pais_1_nome)

    with col2:
        pais_2_nome = st.selectbox(
            "País 2 (Opcional)",
            [p["nome"] for p in paises],
            index=1,
            key="simulador_ies_pais2"
        )
        pais_2 = next(p for p in paises if p["nome"] == pais_2_nome)

    st.divider()

    # Tabs para cada país
    tab1, tab2 = st.tabs([f"📍 {pais_1['nome']}", f"📍 {pais_2['nome']}"])

    with tab1:
        params1 = _painel_pais_ies(pais_1, "país1_ies", api_client)

    with tab2:
        params2 = _painel_pais_ies(pais_2, "país2_ies", api_client) if pais_2["id"] != pais_1["id"] else params1

    st.divider()

    # Botões
    col_sim, col_reset = st.columns(2)

    with col_sim:
        if st.button("▶️ SIMULAR", use_container_width=True, key="btn_simular_ies"):
            _executar_simulacao_ies(pais_1, params1, pais_2, params2, api_client)

    with col_reset:
        if st.button("🔄 RESETAR", use_container_width=True, key="btn_resetar_ies"):
            st.session_state.pop("simulacao_resultado_ies", None)
            st.rerun()


def _painel_pais_ies(pais: Dict[str, Any], chave_sessao: str, api_client: AIAClient) -> Dict[str, Any]:
    """Painel de parâmetros IES para um país"""

    st.markdown(f"**{pais['nome']}** • ISO: {pais['codigo_iso']}")

    # Valores baseline (placeholders)
    va_bruto = 1000.0
    emprego = 50.0
    salarios = 500.0
    ret_local = 0.6
    comp = 0.5
    sym = 0.7
    yale = 60.0
    ultra = 0.35
    agro = 0.25
    medic = 0.20
    infla = 0.15

    parametros = {}

    # 4 isonomias
    st.markdown("**Dimensão Econômica (NCII)**")
    col1, col2, col3 = st.columns(3)

    with col1:
        min_va = va_bruto * 0.75
        max_va = va_bruto * 1.25
        va_novo = st.slider(
            "VA Bruto",
            float(min_va), float(max_va), float(va_bruto),
            key=f"slider_va_{chave_sessao}"
        )
        parametros["va_bruto"] = va_novo

    with col2:
        min_emp = emprego * 0.75
        max_emp = emprego * 1.25
        emp_novo = st.slider(
            "Emprego Total",
            float(min_emp), float(max_emp), float(emprego),
            key=f"slider_emp_{chave_sessao}"
        )
        parametros["emprego_total"] = emp_novo

    with col3:
        min_sal = salarios * 0.75
        max_sal = salarios * 1.25
        sal_novo = st.slider(
            "Salários Totais",
            float(min_sal), float(max_sal), float(salarios),
            key=f"slider_sal_{chave_sessao}"
        )
        parametros["salarios_totais"] = sal_novo

    st.markdown("**Dimensão Glocalizada (L)**")
    col1, col2, col3 = st.columns(3)

    with col1:
        min_ret = ret_local * 0.75
        max_ret = ret_local * 1.25
        ret_novo = st.slider(
            "Retorno Local",
            float(min_ret), float(max_ret), float(ret_local),
            key=f"slider_ret_{chave_sessao}"
        )
        parametros["ret_retorno_local"] = ret_novo

    with col2:
        min_comp = comp * 0.75
        max_comp = comp * 1.25
        comp_novo = st.slider(
            "Competitividade",
            float(min_comp), float(max_comp), float(comp),
            key=f"slider_comp_{chave_sessao}"
        )
        parametros["comp_competitividade"] = comp_novo

    with col3:
        min_sym = sym * 0.75
        max_sym = sym * 1.25
        sym_novo = st.slider(
            "Simbolismo",
            float(min_sym), float(max_sym), float(sym),
            key=f"slider_sym_{chave_sessao}"
        )
        parametros["sym_simbolismo"] = sym_novo

    st.markdown("**Dimensão Nutricional (NSII)**")
    col1, col2 = st.columns(2)

    with col1:
        min_yale = yale * 0.75
        max_yale = yale * 1.25
        yale_novo = st.slider(
            "Yale EPI Score",
            float(min_yale), float(max_yale), float(yale),
            key=f"slider_yale_{chave_sessao}"
        )
        parametros["yale_epi_score"] = yale_novo

    st.markdown("**Saúde Nutricional (NIH)**")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        min_ultra = ultra * 0.75
        max_ultra = ultra * 1.25
        ultra_novo = st.slider(
            "Ultraproc.",
            float(min_ultra), float(max_ultra), float(ultra),
            key=f"slider_ultra_{chave_sessao}"
        )
        parametros["t_ultraprocessados"] = ultra_novo

    with col2:
        min_agro = agro * 0.75
        max_agro = agro * 1.25
        agro_novo = st.slider(
            "Agrotóxicos",
            float(min_agro), float(max_agro), float(agro),
            key=f"slider_agro_{chave_sessao}"
        )
        parametros["u_agrotoxicos"] = agro_novo

    with col3:
        min_medic = medic * 0.75
        max_medic = medic * 1.25
        medic_novo = st.slider(
            "Medicalizado",
            float(min_medic), float(max_medic), float(medic),
            key=f"slider_medic_{chave_sessao}"
        )
        parametros["m_medicalizado"] = medic_novo

    with col4:
        min_infla = infla * 0.75
        max_infla = infla * 1.25
        infla_novo = st.slider(
            "Inflamação",
            float(min_infla), float(max_infla), float(infla),
            key=f"slider_infla_{chave_sessao}"
        )
        parametros["i_inflamacao"] = infla_novo

    return parametros


def _executar_simulacao_ies(pais_1: Dict, params1: Dict, pais_2: Dict, params2: Dict, api_client: AIAClient):
    """Executa simulação IES e mostra resultados"""

    with st.spinner("Calculando IES..."):
        resultado1 = api_client.calcular_ies(pais_1["id"], params1)

        if pais_2["id"] != pais_1["id"]:
            resultado2 = api_client.calcular_ies(pais_2["id"], params2)
        else:
            resultado2 = None

    if resultado1:
        st.session_state["simulacao_resultado_ies"] = {
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
            _mostrar_resultado_ies(pais_1["nome"], resultado1)
            # RADAR para país 1
            fig = criar_radar_ies(resultado1)
            st.plotly_chart(fig, use_container_width=True)

        if resultado2:
            with col2:
                _mostrar_resultado_ies(pais_2["nome"], resultado2)
                # RADAR para país 2
                fig = criar_radar_ies(resultado2)
                st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # Botões ação
        col_desc, col_salv = st.columns(2)

        with col_desc:
            if st.button("🗑️ DESCARTAR", use_container_width=True, key="btn_desc_ies"):
                st.info("✓ Simulação descartada")
                st.session_state.pop("simulacao_resultado_ies", None)

        with col_salv:
            if st.button("💾 SALVAR", use_container_width=True, key="btn_salv_ies"):
                st.success("✓ Simulação salva")


def _mostrar_resultado_ies(pais_nome: str, resultado: Dict):
    """Mostra resultado IES para um país"""

    st.markdown(f"#### {pais_nome}")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("IES", f"{resultado.get('ies', 0):.3f}", resultado.get('status_ies', ''))

    with col2:
        status = resultado.get('status_ies', 'DESCONHECIDO')
        st.markdown(
            f"Status: {status_badge(status)}",
            unsafe_allow_html=True
        )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("L", f"{resultado.get('l_glocalizado', 0):.3f}", "Gloc.")

    with col2:
        st.metric("NCII", f"{resultado.get('ncii', 0):.3f}", "Econ.")

    with col3:
        st.metric("NSII", f"{resultado.get('nsii', 0):.3f}", "Nutr.")

    with col4:
        st.metric("NIH", f"{resultado.get('nih', 0):.3f}", "Saúde")


def criar_radar_ies(resultado: Dict) -> go.Figure:
    """Cria gráfico RADAR 4D para IES"""

    categorias = ["NGII", "NCII", "NSII", "L"]

    # Normalizar valores para 0-1
    ngii = min(resultado.get('ngii_puro', 0.5) / 2, 1)  # Dividir por 2 para normalizar
    ncii = min(resultado.get('ncii', 0.5) / 2, 1)
    nsii = min(resultado.get('nsii', 0.5), 1)
    l_val = min(resultado.get('l_glocalizado', 0.5), 1)

    valores = [ngii, ncii, nsii, l_val]

    fig = go.Figure(data=go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        name='Seu Cenário',
        line=dict(color=AINU_COLORS['azul_claro']),
        fillcolor='rgba(52, 152, 219, 0.3)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickfont=dict(size=10)
            ),
            bgcolor='rgba(248, 244, 237, 0.5)'
        ),
        font=dict(size=12, color=AINU_COLORS['azul_profundo']),
        title="Índice IES - Análise 4D",
        showlegend=True,
        height=500,
        margin=dict(l=80, r=80, t=100, b=80)
    )

    return fig
