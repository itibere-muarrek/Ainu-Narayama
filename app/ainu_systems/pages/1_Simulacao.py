"""
ainu.systems — Simulação geracional (beta).

Página separada, só para usuários logados. A única alavanca é a TFR; todo o
resto segue a tendência da projeção média da UN WPP 2024. Motor e validação:
src/projecao.py e docs/validacao_projecao.md.
"""

import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from src.auth import exigir_login
from src.config import (
    COMPOSICAO_PERFIL_POR_PAIS,
    CORES_5_ZONAS,
    LIMIARES_5_ZONAS_NORMALIZADOS,
    PAISES_DESTAQUE_NARAYAMA_LIVE,
    PAISES_EXEMPLO_ZONAS_NARAYAMA_LIVE,
    cortes_por_composicao,
)
from src.i18n import nome_pais, nome_zona, seletor_idioma
from src.i18n_simulacao import numeros_validacao, ts
from src.projecao import ANO_BASE, simular, tfr_onu

st.set_page_config(page_title="ainu.systems — Simulação", layout="wide")
lang = seletor_idioma()
exigir_login(lambda k: ts(k, lang))

HORIZONTE = 2074
# 11 países do panorama (8 destaque + 3 exemplos). Ampliar para os 28 é só
# editar esta lista: os insumos de data/processed/projecao_inputs.npz já cobrem todos.
PAISES_SIMULACAO = sorted(
    PAISES_DESTAQUE_NARAYAMA_LIVE + PAISES_EXEMPLO_ZONAS_NARAYAMA_LIVE,
    key=lambda c: nome_pais(c, lang),
)
LIM_PEA = LIMIARES_5_ZONAS_NORMALIZADOS["tensao_acelerada"]  # 0,90: piso do PEA

st.title(ts("sim_titulo", lang))
st.markdown(ts("sim_intro", lang))
st.info(ts("sim_aviso", lang))

# ---------------------------------------------------------------------------
# Controles
# ---------------------------------------------------------------------------

col1, col2 = st.columns([1, 2])
with col1:
    pais = st.selectbox(ts("sim_pais", lang), PAISES_SIMULACAO, format_func=lambda c: nome_pais(c, lang))
tfr_hoje = float(tfr_onu(pais)[0])
with col2:
    tfr_alvo = st.slider(
        ts("sim_tfr_alvo", lang),
        min_value=0.8, max_value=3.2, value=2.1, step=0.05,
        help=f"{ts('sim_tfr_atual', lang)}: {tfr_hoje:.2f}",
    )
st.caption(f"{ts('sim_tfr_atual', lang)}: **{tfr_hoje:.2f}**")

# composição de perfis (padrão da config; ajustável à mão)
composicao = dict(COMPOSICAO_PERFIL_POR_PAIS[pais])
with st.expander(ts("sim_avancado", lang)):
    st.markdown(ts("sim_avancado_ajuda", lang))
    cols = st.columns(5)
    pesos = {}
    for i, perfil in enumerate("ABCDE"):
        with cols[i]:
            pesos[perfil] = st.number_input(
                ts("sim_peso", lang, p=perfil),
                min_value=0.0, max_value=1.0, step=0.05,
                value=float(composicao.get(perfil, 0.0)),
                key=f"peso_{pais}_{perfil}",
            )
    ativos = {p: w for p, w in pesos.items() if w > 0}
    soma = sum(ativos.values())
    motivo = None
    if abs(soma - 1.0) > 1e-6:
        motivo = ts("sim_comp_soma", lang, s=soma)
    elif len(ativos) > 3:
        motivo = ts("sim_comp_max3", lang)
    if motivo:
        st.warning(ts("sim_comp_invalida", lang, motivo=motivo))
    else:
        composicao = ativos
    b, tp = cortes_por_composicao(composicao)
    st.caption(ts("sim_cortes", lang, b=b, t=tp))

# ---------------------------------------------------------------------------
# Simulação (cache por país/alvo/composição)
# ---------------------------------------------------------------------------


@st.cache_data(show_spinner=False)
def _rodar(pais: str, alvo: float, comp_itens: tuple):
    return simular(pais, alvo, composicao=dict(comp_itens), horizonte=HORIZONTE)


r = _rodar(pais, round(tfr_alvo, 4), tuple(sorted(composicao.items())))
n = r["horizonte_idx"]
anos = r["cenario"].anos[:n]
pop_c = r["cenario"].pop_total[:n] / 1000.0
pop_b = r["base"].pop_total[:n] / 1000.0
nc = r["n_cenario"]["n_estrela"][:n]
nb = r["n_base"]["n_estrela"][:n]
rotulo_c = ts("sim_cenario", lang, alvo=tfr_alvo)
rotulo_b = ts("sim_base", lang)
COR_C, COR_B = "#1f77b4", "#7f7f7f"

# ---------------------------------------------------------------------------
# Resumo (2024, 2049, 2074)
# ---------------------------------------------------------------------------

st.subheader(ts("sim_resumo", lang))
for ano in (ANO_BASE + 25, HORIZONTE):
    k = ano - ANO_BASE
    zc = r["n_cenario"]["zona"][k]
    zb = r["n_base"]["zona"][k]
    c1, c2, c3 = st.columns(3)
    c1.metric(
        ts("sim_pop_ano", lang, ano=ano), f"{pop_c[k]:,.1f}",
        f"{pop_c[k] - pop_b[k]:+,.1f} vs {rotulo_b}",
    )
    c2.metric(ts("sim_n_ano", lang, ano=ano), f"{nc[k]:.2f}", f"{nc[k] - nb[k]:+.2f} vs {rotulo_b}")
    c3.metric(
        ts("sim_zona_ano", lang, ano=ano),
        nome_zona(zc, lang) if zc else "—",
        f"{rotulo_b}: {nome_zona(zb, lang) if zb else '—'}",
        delta_color="off",
    )

# ---------------------------------------------------------------------------
# Pontos de virada
# ---------------------------------------------------------------------------

st.subheader(ts("sim_virada_titulo", lang))
st.caption(ts("sim_virada_nota", lang))


def _fmt(ano, estado_se_none):
    return str(ano) if ano is not None else estado_se_none


def _linhas_virada(res, serie_n, virada):
    cut = r["horizonte_idx"]
    saldo = (res.nascimentos - res.obitos)[:cut]
    pt = res.pop_total[:cut]
    nn = serie_n["n_estrela"][:cut]
    if saldo.min() >= 0:
        s_none = ts("sim_v_sempre_pos", lang)
    elif saldo.max() < 0:
        s_none = ts("sim_v_sempre_neg", lang)
    elif saldo[0] >= 0:
        s_none = ts("sim_v_pos_depois_neg", lang, ano=int(res.anos[int(np.argmax(saldo < 0))]))
    else:
        s_none = ts("sim_v_nao", lang)
    p_none = ts("sim_v_cresce", lang) if pt[-1] > pt[0] and virada["pico_populacao"] is None else (
        ts("sim_v_cai", lang) if virada["pico_populacao"] is None else ts("sim_v_nao", lang))
    f_none = ts("sim_v_nao", lang)
    if nn[0] >= LIM_PEA:
        n_none = (ts("sim_v_n_ja", lang) if nn.min() >= LIM_PEA
                  else ts("sim_v_n_ja_cai", lang, ano=int(res.anos[int(np.argmax(nn < LIM_PEA))])))
    else:
        n_none = ts("sim_v_n_nunca", lang)
    return [
        _fmt(virada["saldo_natural_positivo"], s_none),
        _fmt(virada["pico_populacao"], p_none),
        _fmt(virada["fim_da_queda"], f_none),
        _fmt(virada["n_estrela_cruza_pea"], n_none),
    ]


itens = [ts("sim_v_saldo", lang), ts("sim_v_pico", lang), ts("sim_v_fim_queda", lang), ts("sim_v_n", lang)]
col_c = _linhas_virada(r["cenario"], r["n_cenario"], r["virada_cenario"])
col_b = _linhas_virada(r["base"], r["n_base"], r["virada_base"])
st.table({ts("sim_col_item", lang): itens, rotulo_c: col_c, rotulo_b: col_b})

# ---------------------------------------------------------------------------
# Gráficos
# ---------------------------------------------------------------------------

g1, g2 = st.columns(2)
with g1:
    st.markdown(f"**{ts('sim_pop_titulo', lang)}**")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=anos, y=pop_b, name=rotulo_b, line=dict(color=COR_B, dash="dash")))
    fig.add_trace(go.Scatter(x=anos, y=pop_c, name=rotulo_c, line=dict(color=COR_C, width=3)))
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10), xaxis_title=ts("sim_ano", lang),
                      legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, use_container_width=True)
with g2:
    st.markdown(f"**{ts('sim_n_titulo', lang)}**")
    fig = go.Figure()
    # faixas das 5 zonas (limiares normalizados da tese)
    lim = LIMIARES_5_ZONAS_NORMALIZADOS
    teto = max(2.4, float(np.nanmax([nc.max(), nb.max()])) * 1.08)
    faixas = [
        (0, lim["pec"], "Colapso de Narayama (PEC)"),
        (lim["pec"], lim["tensao_acelerada"], "Tensão Acelerada"),
        (lim["tensao_acelerada"], lim["pea"], "Ponto de Equilíbrio Autossustentável (PEA)"),
        (lim["pea"], lim["tensao_populacional"], "Tensão Populacional"),
        (lim["tensao_populacional"], teto, "Saturação por Excesso de Contingente (PEEC)"),
    ]
    for y0, y1, zona in faixas:
        fig.add_hrect(y0=y0, y1=y1, fillcolor=CORES_5_ZONAS[zona], opacity=0.55, line_width=0,
                      annotation_text=nome_zona(zona, lang).split(" (")[0], annotation_position="top left",
                      annotation_font_size=10)
    fig.add_trace(go.Scatter(x=anos, y=nb, name=rotulo_b, line=dict(color=COR_B, dash="dash")))
    fig.add_trace(go.Scatter(x=anos, y=nc, name=rotulo_c, line=dict(color=COR_C, width=3)))
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10), xaxis_title=ts("sim_ano", lang),
                      yaxis=dict(range=[0, teto]), legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, use_container_width=True)

g3, g4 = st.columns(2)
with g3:
    st.markdown(f"**{ts('sim_nasc_obitos', lang)}**")
    fig = go.Figure()
    for res, rot, cor, dash in ((r["base"], rotulo_b, COR_B, "dash"), (r["cenario"], rotulo_c, COR_C, "solid")):
        fig.add_trace(go.Scatter(x=anos, y=res.nascimentos[:n] / 1000, name=f"{ts('sim_nascimentos', lang)} — {rot}",
                                 line=dict(color=cor, dash=dash)))
    fig.add_trace(go.Scatter(x=anos, y=r["cenario"].obitos[:n] / 1000, name=f"{ts('sim_obitos', lang)} — {rotulo_c}",
                             line=dict(color="#d62728", width=2)))
    fig.add_trace(go.Scatter(x=anos, y=r["base"].obitos[:n] / 1000, name=f"{ts('sim_obitos', lang)} — {rotulo_b}",
                             line=dict(color="#d62728", dash="dash", width=1)))
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10), xaxis_title=ts("sim_ano", lang),
                      legend=dict(orientation="h", y=-0.35))
    st.plotly_chart(fig, use_container_width=True)
with g4:
    st.markdown(f"**{ts('sim_piramide_titulo', lang)}**")
    ano_est = st.select_slider(ts("sim_piramide_ano", lang), options=[ANO_BASE, ANO_BASE + 25, HORIZONTE],
                               value=HORIZONTE)
    k = ano_est - ANO_BASE
    idades = np.arange(0, 101)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=idades, y=r["base"].pop[:, :, k].sum(axis=0), name=rotulo_b,
                             line=dict(color=COR_B, dash="dash")))
    fig.add_trace(go.Scatter(x=idades, y=r["cenario"].pop[:, :, k].sum(axis=0), name=rotulo_c,
                             line=dict(color=COR_C, width=3)))
    b_max, t_min = r["n_cenario"]["cortes"]
    fig.add_vrect(x0=0, x1=b_max + 0.5, fillcolor="#2ca02c", opacity=0.08, line_width=0,
                  annotation_text="Pop_Base", annotation_position="top left")
    fig.add_vrect(x0=t_min - 0.5, x1=100, fillcolor="#9467bd", opacity=0.08, line_width=0,
                  annotation_text="Pop_Topo", annotation_position="top right")
    fig.update_layout(height=330, margin=dict(l=10, r=10, t=10, b=10), xaxis_title=ts("sim_idade", lang),
                      yaxis_title=ts("sim_milhares", lang), legend=dict(orientation="h", y=-0.3))
    st.plotly_chart(fig, use_container_width=True)

with st.expander(ts("sim_metodo_titulo", lang)):
    st.markdown(ts("sim_metodo", lang, **numeros_validacao(lang)))
