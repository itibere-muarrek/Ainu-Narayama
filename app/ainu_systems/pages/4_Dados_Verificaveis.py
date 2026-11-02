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

try:
    import gerar_fichas as G
    G.EMBED = True
    G.carregar()
    ok = True
except Exception:
    ok = False

t = G.T[lang if lang in G.T else "pt"] if ok else {"d_titulo": "Dados verificáveis", "x_sem": "Os dados do Diretório ainda não foram liberados neste ambiente."}
st.title(t["d_titulo"])
if not ok:
    st.warning(t["x_sem"])
    st.stop()
if lang != "pt":
    st.caption(t["aviso_texto_pt"])
mostrar_html(G.html_dados(lang), 2600)
