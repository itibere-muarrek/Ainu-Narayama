"""
ainu.systems — Contas Nacionais por Nascimentos (Diretório de países), beta.

Página só para usuários logados. Mostra as fichas dos 11 países do AINU.Systems com as mesmas páginas da prévia do Diretório
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

try:
    import gerar_fichas as G
    G.EMBED = True
    G.carregar()
    ok = True
except Exception:  # dados ausentes: avisa e não quebra
    ok = False

t = G.T[lang if lang in G.T else "pt"] if ok else {"titulo": "Contas Nacionais por Nascimentos", "x_sem": "Os dados do Diretório ainda não foram liberados neste ambiente."}
st.title(t["titulo"])
st.caption(ts("dados_abertos_nota", lang))
if not ok:
    st.warning(t["x_sem"])
    st.stop()
st.caption(t["x_nota_app"])
if lang != "pt":
    st.caption(t["aviso_texto_pt"])

aba1, aba2 = st.tabs([t["tabela"], t["x_ficha"]])
with aba1:
    mostrar_html(G.html_indice(lang), 1500)
with aba2:
    iso = st.selectbox(t["x_pais"], ISO, format_func=lambda c: nome_pais(c, lang))
    mostrar_html(G.html_ficha(iso, lang), 2400)
