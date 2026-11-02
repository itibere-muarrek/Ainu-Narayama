"""
ainu.systems — Contas Nacionais por Nascimentos (Diretório de países), beta.

Página só para usuários logados. Mostra as fichas dos 11 países do Paper 3 com as mesmas páginas da prévia do Diretório
(scripts/diretorio/gerar_fichas.py, modo embutido), a partir dos JSON de data/diretorio/publicavel/. Rodapé de fontes e
referências em cada ficha.
"""

import sys
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "scripts" / "diretorio"))

from src.auth import exigir_login
from src.i18n import nome_pais, seletor_idioma
from src.i18n_simulacao import ts

def mostrar_html(h: str, altura: int) -> None:
    """HTML gerado por nós (dados do Diretório) num iframe: st.iframe nas versões novas do Streamlit, components.html nas antigas."""
    if hasattr(st, "iframe"):
        st.iframe(h, height=altura)
    else:
        import streamlit.components.v1 as components
        components.html(h, height=altura, scrolling=True)


st.set_page_config(page_title="ainu.systems — Contas Nacionais por Nascimentos", layout="wide")
lang = seletor_idioma()
exigir_login(lambda k: ts(k, lang))

ISO = ["ITA", "KOR", "JPN", "MEX", "ARG", "BRA", "USA", "IND", "NGA", "FRA", "CHN"]
TX = {
    "pt": {"t": "Contas Nacionais por Nascimentos", "sem": "Os dados do Diretório ainda não foram liberados neste ambiente.", "tab1": "Comparação", "tab2": "Ficha do país", "pais": "País",
           "idioma": "Esta página está em português e inglês; os outros idiomas mostram português.", "ia": "",
           "dados": "Aqui constam só dados levantados em fontes e testados. A lista completa, com links para conferir cada fonte, está na página Dados Verificaveis. Estimativas, projeções e simulações são suposições para pesquisadores e ficam na página Consumo e Dividendo."},
    "en": {"t": "National Accounts by Births", "sem": "The Directory data has not been released in this environment.", "tab1": "Comparison", "tab2": "Country page", "pais": "Country",
           "idioma": "This page is in Portuguese and English; other languages show Portuguese.", "ia": "",
           "dados": "This page only has data gathered from sources and tested. The full list, with links to check each source, is on the Verifiable Data page. Estimates, projections and simulations are assumptions for researchers and are on the Consumption and Dividend page."},
}
tx = TX["en" if lang == "en" else "pt"]

try:
    import gerar_fichas as G
    G.EMBED = True
    G.carregar()
    ok = True
except Exception:  # dados ausentes: avisa e não quebra
    ok = False

st.title(tx["t"])
if not ok:
    st.warning(tx["sem"])
    st.stop()
if lang not in ("pt", "en"):
    st.caption(tx["idioma"])
st.caption(tx["dados"])

aba1, aba2 = st.tabs([tx["tab1"], tx["tab2"]])
with aba1:
    mostrar_html(G.html_indice(lang), 1500)
with aba2:
    iso = st.selectbox(tx["pais"], ISO, format_func=lambda c: nome_pais(c, lang))
    mostrar_html(G.html_ficha(iso, lang), 2400)
