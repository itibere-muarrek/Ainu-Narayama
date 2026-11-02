"""
ainu.systems — Dados verificáveis do Diretório Contas Nacionais por Nascimentos, beta.

Página só para usuários logados. Lista de todos os dados com fonte externa (identificador, série, período, verificação) e
link para conferir no original, mais os números conferidos contra a fonte e o rodapé de referências de método.
Mesma página da prévia do Diretório (scripts/diretorio/gerar_fichas.py, modo embutido).
"""

import sys
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "scripts" / "diretorio"))

from src.auth import exigir_login
from src.i18n import seletor_idioma
from src.i18n_simulacao import ts

def mostrar_html(h: str, altura: int) -> None:
    """HTML gerado por nós (dados do Diretório) num iframe: st.iframe nas versões novas do Streamlit, components.html nas antigas."""
    if hasattr(st, "iframe"):
        st.iframe(h, height=altura)
    else:
        import streamlit.components.v1 as components
        components.html(h, height=altura, scrolling=True)


st.set_page_config(page_title="ainu.systems — Dados verificáveis", layout="wide")
lang = seletor_idioma()
exigir_login(lambda k: ts(k, lang))

TX = {
    "pt": {"t": "Dados verificáveis", "sem": "Os dados do Diretório ainda não foram liberados neste ambiente.",
           "idioma": "Esta página está em português e inglês; os outros idiomas mostram português."},
    "en": {"t": "Verifiable data", "sem": "The Directory data has not been released in this environment.",
           "idioma": "This page is in Portuguese and English; other languages show Portuguese."},
}
tx = TX["en" if lang == "en" else "pt"]

try:
    import gerar_fichas as G
    G.EMBED = True
    G.carregar()
    ok = True
except Exception:
    ok = False

st.title(tx["t"])
if not ok:
    st.warning(tx["sem"])
    st.stop()
if lang not in ("pt", "en"):
    st.caption(tx["idioma"])
mostrar_html(G.html_dados(lang), 2600)
