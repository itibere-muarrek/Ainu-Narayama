"""
ainu.systems — Condição média em TFT de reposição (exploratório).

Página só para usuários logados. Compara a Tendência da ONU com uma Meta (TFT -> alvo, padrão 2,1) nos ciclos de 25 anos,
com N*, razão Ascendentes/Estruturador e Estruturadores por pessoa de 80+. Cálculo em src/condicao_media.py (motor
src/projecao.py). Hipótese H8 do plano do Paper 3 (v5.4). Cenário condicional, não previsão.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from src.auth import exigir_login
from src.condicao_media import resumo_2099, tabela_condicao
from src.config import CORES_5_ZONAS, LIMIARES_5_ZONAS_NORMALIZADOS, PAISES
from src.i18n import nome_pais, nome_zona, seletor_idioma
from src.i18n_condicao import tcm
from src.i18n_simulacao import ts

st.set_page_config(page_title="ainu.systems — Condição média", layout="wide")
lang = seletor_idioma()
exigir_login(lambda k: ts(k, lang))

VIRGULA = lang in {"pt", "es", "fr", "it", "fi"}
COR_C, COR_B = "#1f77b4", "#7f7f7f"
PAISES_PAPER3 = ["NGA", "MEX", "IND", "BRA", "ARG", "USA", "FRA", "CHN", "ITA", "JPN", "KOR"]

st.title(tcm("cm_titulo", lang))
if tcm("cm_nota_idioma", lang):
    st.caption(tcm("cm_nota_idioma", lang))
st.markdown(tcm("cm_intro", lang))
st.warning(tcm("cm_aviso", lang))

c1, c2 = st.columns(2)
with c1:
    alvo = st.slider(tcm("cm_alvo", lang), min_value=1.6, max_value=2.6, value=2.1, step=0.05)
with c2:
    rampa = st.select_slider(tcm("cm_rampa", lang), options=[10, 15, 25, 40], value=25)


@st.cache_data(show_spinner=False)
def _calcular(alvo_: float, rampa_: int) -> pd.DataFrame:
    return tabela_condicao(alvo=alvo_, anos_rampa=rampa_)


with st.spinner(tcm("cm_calculando", lang)):
    df = _calcular(round(alvo, 4), int(rampa))
res = resumo_2099(df)


def num(x, casas=2):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    s = f"{x:.{casas}f}"
    return s.replace(".", ",") if VIRGULA else s


# ---------------------------------------------------------------------------
# 1. Tabela-resumo
# ---------------------------------------------------------------------------
st.subheader(tcm("cm_tab_titulo", lang))
st.caption(tcm("cm_tab_nota", lang))

COLS = [
    ("n_2024", "cm_col_n24", 2), ("n_2099_tendencia", "cm_col_n99t", 2), ("n_2099_meta", "cm_col_n99m", 2),
    ("zona_2099_meta", "cm_col_zona", None),
    ("a_e_2024", "cm_col_ae24", 2), ("a_e_2074_meta", "cm_col_ae74", 2), ("a_e_2099_meta", "cm_col_ae99m", 2),
    ("a_e_2099_tendencia", "cm_col_ae99t", 2),
    ("e80_2024", "cm_col_e24", 1), ("e80_2099_meta", "cm_col_e99m", 1), ("e80_2099_tendencia", "cm_col_e99t", 1),
]
linhas = []
for _, r in res.sort_values("n_2024", ascending=False).iterrows():
    linha = {tcm("cm_col_pais", lang): nome_pais(r["pais"], lang) + (" *" if r["pais"] in PAISES_PAPER3 else "")}
    for col, chave, casas in COLS:
        if casas is None:
            linha[tcm(chave, lang)] = nome_zona(r[col], lang).split(" (")[0] if r[col] else "—"
        else:
            linha[tcm(chave, lang)] = num(r[col], casas)
    linhas.append(linha)


def _mediana(sub: pd.DataFrame, rotulo: str) -> dict:
    linha = {tcm("cm_col_pais", lang): rotulo}
    for col, chave, casas in COLS:
        linha[tcm(chave, lang)] = "—" if casas is None else num(float(np.nanmedian(sub[col])), casas)
    return linha


linhas.append(_mediana(res, tcm("cm_mediana", lang)))
linhas.append(_mediana(res[res.pais != "NGA"], tcm("cm_mediana_sn", lang)))
st.dataframe(pd.DataFrame(linhas), use_container_width=True, hide_index=True)
st.caption("(\\*) " + tcm("cm_p3", lang))

st.download_button(
    tcm("cm_baixar", lang),
    df.to_csv(index=False).encode("utf-8-sig"),
    file_name=f"condicao_media_tfr{alvo:.2f}_rampa{rampa}.csv",
    mime="text/csv",
)

# ---------------------------------------------------------------------------
# 2. Gráficos
# ---------------------------------------------------------------------------
st.subheader(tcm("cm_graf_titulo", lang))
sel = st.multiselect(
    tcm("cm_graf_paises", lang),
    options=sorted(PAISES.keys(), key=lambda c: nome_pais(c, lang)),
    default=["ITA", "KOR", "MEX"],
    format_func=lambda c: nome_pais(c, lang),
)

g1, g2 = st.columns(2)
with g1:
    st.markdown(f"**{tcm('cm_graf_ae', lang)}**")
    fig = go.Figure()
    for p in sel:
        for cen, dash in (("tendencia", "dash"), ("meta", "solid")):
            d = df[(df.pais == p) & (df.cenario == cen)]
            fig.add_trace(go.Scatter(
                x=d.ano, y=d.A_E, mode="lines+markers", line=dict(dash=dash),
                name=f"{nome_pais(p, lang)} — {tcm('cm_meta' if cen == 'meta' else 'cm_tendencia', lang)}",
            ))
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10), xaxis_title=tcm("cm_ano", lang),
                      legend=dict(orientation="h", y=-0.3))
    st.plotly_chart(fig, use_container_width=True)
with g2:
    st.markdown(f"**{tcm('cm_graf_n', lang)}**")
    fig = go.Figure()
    lim = LIMIARES_5_ZONAS_NORMALIZADOS
    teto = max(2.4, float(df[df.pais.isin(sel or ["ITA"])].n_estrela.max()) * 1.08)
    faixas = [
        (0, lim["pec"], "Colapso de Narayama (PEC)"),
        (lim["pec"], lim["tensao_acelerada"], "Tensão Acelerada"),
        (lim["tensao_acelerada"], lim["pea"], "Ponto de Equilíbrio Autossustentável (PEA)"),
        (lim["pea"], lim["tensao_populacional"], "Tensão Populacional"),
        (lim["tensao_populacional"], teto, "Saturação por Excesso de Contingente (PEEC)"),
    ]
    for y0, y1, zona in faixas:
        fig.add_hrect(y0=y0, y1=y1, fillcolor=CORES_5_ZONAS[zona], opacity=0.5, line_width=0,
                      annotation_text=nome_zona(zona, lang).split(" (")[0], annotation_position="top left",
                      annotation_font_size=10)
    for p in sel:
        for cen, dash in (("tendencia", "dash"), ("meta", "solid")):
            d = df[(df.pais == p) & (df.cenario == cen)]
            fig.add_trace(go.Scatter(
                x=d.ano, y=d.n_estrela, mode="lines+markers", line=dict(dash=dash),
                name=f"{nome_pais(p, lang)} — {tcm('cm_meta' if cen == 'meta' else 'cm_tendencia', lang)}",
            ))
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10), xaxis_title=tcm("cm_ano", lang),
                      yaxis=dict(range=[0, teto]), legend=dict(orientation="h", y=-0.3))
    st.plotly_chart(fig, use_container_width=True)

st.subheader(tcm("cm_ler_titulo", lang))
st.markdown(tcm("cm_ler", lang))
st.caption(tcm("cm_fonte", lang))
