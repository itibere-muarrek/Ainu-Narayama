"""
ainu.systems — Consumo e Dividendo: a realidade dos países.

Página só para usuários logados. Mostra o que é OBSERVADO em fontes oficiais: o consumo de cada país (Banco Mundial, WDI), o gasto
público em família (OCDE SOCX) e as transferências que cada país já paga às famílias com crianças. Nada aqui é estimativa,
projeção ou simulação; as suposições (custo do Dividendo, crianças adicionais, cenários) ficam na página Simulacao Dividendo.
Dados: data/diretorio/publicavel/realidade.json, gerado por scripts/diretorio/exportar_diretorio.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(RAIZ))

from src.auth import exigir_login
from src.i18n import nome_pais, seletor_idioma
from src.i18n_realidade import tr
from src.i18n_simulacao import ts

st.set_page_config(page_title="ainu.systems — Consumo e Dividendo", layout="wide")
lang = seletor_idioma()
exigir_login(lambda k: ts(k, lang))

ORDEM = ["ITA", "KOR", "JPN", "MEX", "ARG", "BRA", "USA", "IND", "NGA", "FRA", "CHN"]
VIRGULA = lang in {"pt", "es", "fr", "it", "fi"}


def fmt(x, casas: int = 1) -> str:
    s = f"{x:,.{casas}f}"
    return s.translate(str.maketrans(",.", ".,")) if VIRGULA else s


def pct(x: float) -> str:
    s = f"{x:g}"
    return s.replace(".", ",") if VIRGULA else s


def com_ano(v, casas: int = 1) -> str:
    """'57,6 (2025)' ou 'sem dado'."""
    if not v or v.get("valor") is None:
        return tr("r_nd", lang)
    return f"{fmt(v['valor'], casas)} ({v['ano']})"


def carregar():
    try:
        d = json.loads((RAIZ / "data" / "diretorio" / "publicavel" / "realidade.json").read_text(encoding="utf-8"))
        return d if isinstance(d.get("paises"), dict) else None
    except (OSError, ValueError):
        return None


dados = carregar()
st.title(tr("r_titulo", lang))
st.markdown(tr("r_intro", lang))
st.caption(tr("r_nota", lang))
if dados is None:
    st.warning(tr("r_sem", lang))
    st.stop()
paises = dados["paises"]

# ---------------------------------------------------------------------------
# Comparação entre países
# ---------------------------------------------------------------------------

st.header(tr("r_comp", lang))
linhas = []
for iso in ORDEM:
    p = paises[iso]
    w = p["wdi"]
    fam = p["gasto_publico_familia"]
    pr = p["programa"]
    if pr.get("pct_pib") is not None:
        prog = f"{'≈ ' if pr.get('ressalva') else ''}{pct(pr['pct_pib'])}: {pr['nome']} ({pr['ano']})"
    else:
        prog = tr("r_nd", lang)
    linhas.append({
        tr("r_pais", lang): nome_pais(iso, lang),
        tr("r_cons", lang): com_ano(w.get("consumo_familias_pib")),
        tr("r_gov", lang): com_ano(w.get("consumo_governo_pib")),
        tr("r_pc", lang): com_ano(w.get("consumo_familias_pc"), 0),
        tr("r_fam", lang): f"{fmt(fam['pct_pib'], 2)} ({fam['ano']})" if fam else tr("r_nd", lang),
        tr("r_prog", lang): prog,
    })
st.dataframe(linhas, hide_index=True, width="stretch")
series = dados.get("series", {})
if series:
    st.caption(" · ".join(f"[{v['codigo']}]({v['url']})" for v in series.values()))
st.caption(tr("r_fontes", lang))

# ---------------------------------------------------------------------------
# Transferências às famílias, país a país
# ---------------------------------------------------------------------------

st.header(tr("r_det", lang))
iso = st.selectbox(tr("r_pais", lang), ORDEM, format_func=lambda c: nome_pais(c, lang))
instr = paises[iso]["instrumentos"]
if lang != "pt":
    st.caption(tr("r_texto_pt", lang))
if not instr:
    st.info(tr("r_nenhum", lang))
for i in instr:
    with st.container(border=True):
        st.markdown(f"**{i['instrumento']}**")
        st.caption(i["tipo"])
        if i.get("valor"):
            st.markdown(f"**{tr('r_valor', lang)}.** {i['valor']}")
        if i.get("custo_fiscal"):
            st.markdown(f"**{tr('r_custo', lang)}.** {i['custo_fiscal']}")
