"""
ainu.systems — Consumo por coorte e Dividendo Intergeracional (beta).

Página separada, só para usuários logados. Escala números do Paper 3 exportados pelo Diretório
(data/diretorio/publicavel/simulacoes.json); não roda modelo novo. Cálculos em src/consumo_dividendo.py.
"""

import sys
from pathlib import Path

import streamlit as st
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from src.auth import exigir_login
from src.consumo_dividendo import (
    carregar,
    cenarios,
    custo_dividendo,
    empregos_liquidos,
    horizontes_do_cenario,
    incremento,
    razao_gasto_familia,
    razao_programa,
)
from src.i18n import nome_pais, seletor_idioma
from src.i18n_consumo import tc
from src.i18n_simulacao import ts

st.set_page_config(page_title="ainu.systems — Consumo e Dividendo", layout="wide")
lang = seletor_idioma()
exigir_login(lambda k: ts(k, lang))

VIRGULA = lang in {"pt", "es", "fr", "it", "fi"}


def fmt(x, casas: int = 2) -> str:
    s = f"{x:,.{casas}f}"
    return s.translate(str.maketrans(",.", ".,")) if VIRGULA else s


def pct_txt(v: float) -> str:
    """Porcentagem sem zeros à direita (0,0095; 0,87; 1,11)."""
    s = f"{v:g}"
    return s.replace(".", ",") if VIRGULA else s


st.title(tc("c_titulo", lang))
st.markdown(tc("c_intro", lang))
st.caption(tc("c_naturezas", lang))
if lang not in ("pt", "en"):
    st.caption(tc("c_nota_idioma", "en"))

dados = carregar()
if dados is None:
    st.warning(tc("c_sem_dados", lang))
    st.stop()

paises = dados["paises"]
iso = st.selectbox(tc("c_pais", lang), sorted(paises, key=lambda c: nome_pais(c, lang)), format_func=lambda c: nome_pais(c, lang))
p = paises[iso]

# ---------------------------------------------------------------------------
# 1. Dividendo
# ---------------------------------------------------------------------------

st.header(tc("c_div_titulo", lang))
st.markdown(tc("c_div_ajuda", lang))
base10 = p["dividendo_10pct_pib"]
if base10 is None:
    st.info(tc("c_div_nd", lang))
else:
    x = st.slider(tc("c_div_slider", lang), min_value=0, max_value=50, value=10, step=1)
    custo = custo_dividendo(x, base10)
    c1, c2, c3 = st.columns(3)
    c1.metric(tc("c_div_custo", lang), f"{fmt(custo)}%", help="SIM")

    prog = p["programa"]
    r_prog = razao_programa(custo, prog.get("pct_pib"))
    if r_prog is None:
        c2.metric(tc("c_div_prog", lang), "—")
        c2.caption(tc("c_div_prog_nd", lang))
    else:
        c2.metric(tc("c_div_prog", lang), tc("c_vezes", lang, x=fmt(r_prog, 1)), help="SIM")
        c2.caption(tc("c_div_prog_nome", lang, nome=prog["nome"], pct=f"{pct_txt(prog['pct_pib'])}%", ano=prog["ano"]))
        if prog.get("ressalva"):
            c2.caption(tc("c_div_prog_ressalva", lang))

    fam = p["gasto_publico_familia"]
    r_fam = razao_gasto_familia(custo, fam["pct_pib"] if fam else None)
    if r_fam is None:
        c3.metric(tc("c_div_fam", lang), "—")
        c3.caption(tc("c_div_fam_nd", lang))
    else:
        c3.metric(tc("c_div_fam", lang), f"{fmt(100 * r_fam, 0)}%", help="SIM")
        c3.caption(tc("c_div_fam_nome", lang, pct=f"{fmt(fam['pct_pib'])}%", ano=fam["ano"]))
    if p.get("base_consumo_descendentes"):
        st.caption(tc("c_div_base", lang, base=p["base_consumo_descendentes"]))

# ---------------------------------------------------------------------------
# 2. Criança adicional
# ---------------------------------------------------------------------------

st.header(tc("c_inc_titulo", lang))
st.markdown(tc("c_inc_ajuda", lang))
inc = p["incremento_crianca"]
if not inc.get("disponivel"):
    st.info(tc("c_inc_nd", lang, motivo=inc.get("motivo") or tc("c_inc_motivo_default", lang)))
else:
    cn, cd = st.columns(2)
    with cn:
        n = st.number_input(tc("c_inc_n", lang), min_value=0, max_value=50_000_000, value=1000, step=1000)
    with cd:
        desloc = st.slider(tc("c_inc_desloc", lang), min_value=0, max_value=100, value=0, step=5)
    un_c, un_v = inc["unidade_consumo"], inc["unidade_vad"]
    emp_b = inc["empregos_brutos_por_crianca"]["mediana"]
    emp_l = empregos_liquidos(emp_b, inc["empregos_liquidos_50"], inc["empregos_liquidos_100"], desloc)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(tc("c_inc_consumo", lang, un=un_c), fmt(incremento(n, inc["cfcc_por_crianca_ano"]), 0), help="EST")
    m2.metric(tc("c_inc_vad", lang, un=un_v), fmt(incremento(n, inc["vad_por_crianca_ano"]["mediana"]), 0), help="EST")
    m3.metric(tc("c_inc_emp_bruto", lang), fmt(incremento(n, emp_b), 0), help="EST")
    m4.metric(tc("c_inc_emp_liq", lang), fmt(incremento(n, emp_l), 0), help="EST")
    st.caption(tc("c_inc_nota", lang))
    st.caption(inc.get("aviso", ""))

# ---------------------------------------------------------------------------
# 3. Cenários de fecundidade
# ---------------------------------------------------------------------------

st.header(tc("c_cen_titulo", lang))
st.markdown(tc("c_cen_ajuda", lang))
hs = p["horizontes"]
if hs:
    cen = st.selectbox(tc("c_cen_escolha", lang), cenarios(hs))
    linhas = horizontes_do_cenario(hs, cen)
    tabela = {
        tc("c_cen_horizonte", lang): [h["horizonte"] for h in linhas],
        tc("c_cen_ano", lang): [h["ano"] for h in linhas],
        tc("c_cen_tft", lang): [fmt(h["tft"]) for h in linhas],
        tc("c_cen_desc", lang): [fmt(h["delta_desc_pct"], 1) for h in linhas],
        tc("c_cen_estr", lang): [fmt(h["delta_estr_pct"], 1) for h in linhas],
        tc("c_cen_asc", lang): [fmt(h["delta_asc_pct"], 1) for h in linhas],
        tc("c_cen_cfcc", lang): [fmt(h["delta_cfcc_total_pct"], 1) for h in linhas],
        tc("c_cen_pub", lang): [fmt(h["delta_consumo_publico_pct"], 1) for h in linhas],
    }
    st.table(tabela)
    st.caption(tc("c_cen_nota", lang))

st.divider()
with st.expander(f"{tc('c_fontes_titulo', lang)} ({len(p.get('fontes', []))})", expanded=False):
    st.caption(tc("c_fontes_nota", lang))
    for f in p.get("fontes", []):
        host = urlsplit(f["url"]).netloc.removeprefix("www.")
        ids = f", {', '.join(sorted(set(f['ids']))[:2])}" if f.get("ids") else ""
        st.markdown(f"- [{f['nome']}]({f['url']}) <small>({host}{ids})</small>", unsafe_allow_html=True)
st.caption(tc("c_rodape", lang))
