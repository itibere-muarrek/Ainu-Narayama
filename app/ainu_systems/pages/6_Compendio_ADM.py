"""
ainu.systems — Compêndio técnico (restrito ao administrador).

O CONTEÚDO NÃO ESTÁ NO REPOSITÓRIO (que é público). A página lê o arquivo de:
  1. a variável AINU_COMPENDIO_ARQUIVO (caminho), se existir;
  2. /etc/secrets/COMPENDIO_AINU_SYSTEMS.md (Secret File do Render);
  3. docs/privado/COMPENDIO_AINU_SYSTEMS.md (cópia local, ignorada pelo git).
Só vê quem entrou como administrador: AINU_ADMIN (padrão: o login antigo, AINU_LEGACY_USER / AinuOriginal@@).
No modo de senha única (sem logins individuais) quem tem a senha é o administrador.
Os demais usuários não veem nada além de um aviso de acesso restrito.
"""

import os
import sys
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(RAIZ))

from src.auth import exigir_login, _LOGIN_SENHA_ANTIGA
from src.i18n import seletor_idioma
from src.i18n_simulacao import ts

st.set_page_config(page_title="ainu.systems — Compêndio (ADM)", layout="wide")
lang = seletor_idioma()
usuario = exigir_login(lambda k: ts(k, lang))

admin = os.environ.get("AINU_ADMIN") or os.environ.get("AINU_LEGACY_USER", _LOGIN_SENHA_ANTIGA)
if usuario is not None and usuario != admin:
    st.title("Compêndio técnico")
    st.warning("Acesso restrito ao administrador.")
    st.stop()

NOME = "COMPENDIO_AINU_SYSTEMS"
candidatos = [
    Path(os.environ["AINU_COMPENDIO_ARQUIVO"]) if os.environ.get("AINU_COMPENDIO_ARQUIVO") else None,
    Path("/etc/secrets") / f"{NOME}.md",
    RAIZ / "docs" / "privado" / f"{NOME}.md",
]
arquivo = next((p for p in candidatos if p and p.is_file()), None)
if arquivo is None:
    st.title("Compêndio técnico")
    st.info(
        "O arquivo do compêndio não está neste ambiente. No Render: Environment → Secret Files → "
        f"nome `{NOME}.md`. Localmente: `docs/privado/{NOME}.md`."
    )
    st.stop()

st.caption("Restrito ao administrador. Conteúdo fora do repositório público.")
docx = arquivo.with_suffix(".docx")
if docx.is_file():
    st.download_button("Baixar .docx", docx.read_bytes(), file_name=docx.name,
                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
st.markdown(arquivo.read_text(encoding="utf-8"))
