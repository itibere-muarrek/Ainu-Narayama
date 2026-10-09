"""
Autenticação por usuário do ainu.systems (beta testers: Visitor1..Visitor6).

Configuração por variável de ambiente (no Render, nunca no repositório):

    AINU_USERS = {"Visitor1": "pbkdf2_sha256$<iter>$<salt_hex>$<hash_hex>", ...}

Os valores são HASHES (PBKDF2-SHA256 com sal individual), não senhas. Quem
gera os hashes é scripts/gerar_credenciais.py, que também grava as senhas em
texto num arquivo FORA do repositório, só para o administrador entregar a
cada pessoa por um canal separado.

Compatibilidade: se AINU_USERS não existir, vale o comportamento antigo (senha
única em AINU_SYSTEMS_PASSWORD; sem nenhuma das duas, acesso liberado com
aviso — só desenvolvimento local).

Limites honestos: é controle de acesso simples para poucas pessoas (sem
recuperação de senha, sem 2FA, sem bloqueio persistente entre sessões). Para
mais de ~10 usuários ou dados sensíveis, trocar por um provedor de identidade.
"""

from __future__ import annotations

import hmac
import json
import os
import time
from typing import Optional

import streamlit as st

from src.senha import gerar_hash, verificar_hash

_CHAVE_SESSAO = "ainu_usuario"
# Login que continua aceitando a senha única antiga (AINU_SYSTEMS_PASSWORD).
# O nome não é segredo; pode ser trocado pela variável AINU_LEGACY_USER.
_LOGIN_SENHA_ANTIGA = "AinuOriginal@@"


def ler_usuarios(bruto: Optional[str]):
    """Interpreta AINU_USERS. Devolve (usuarios, erro): (None, None) se a variável
    não existe; (None, "motivo") se existe mas está inválida; (dict, None) se ok.

    Tolera o erro mais comum de colagem: o JSON inteiro entre aspas (e com aspas
    internas escapadas), lendo-o uma segunda vez.
    """
    if bruto is None or not bruto.strip():
        return None, None
    try:
        dados = json.loads(bruto.strip())
        if isinstance(dados, str):  # colado entre aspas
            dados = json.loads(dados)
    except (json.JSONDecodeError, ValueError):
        return None, "não é um JSON válido (cole o conteúdo inteiro do arquivo, começando em { e terminando em })"
    if not isinstance(dados, dict) or not dados:
        return None, "não é um objeto {usuário: hash} (vazio ou de outro tipo)"
    if not all(isinstance(v, str) and v.startswith("pbkdf2_sha256$") for v in dados.values()):
        return None, "os valores não parecem hashes pbkdf2_sha256 (foram coladas senhas em vez de hashes?)"
    return dados, None


def _usuarios():
    return ler_usuarios(os.environ.get("AINU_USERS"))


def usuario_logado() -> Optional[str]:
    return st.session_state.get(_CHAVE_SESSAO)


def exigir_login(txt) -> Optional[str]:
    """Garante acesso; devolve o nome do usuário (ou None no modo senha única /
    desenvolvimento). Chama st.stop() se o acesso não foi concedido.

    `txt` é uma função texto(chave) já ligada ao idioma (ex.: lambda k: t(k, lang)).
    """
    usuarios, erro_config = _usuarios()
    if erro_config:
        # Variável existe mas está inválida: avisa claramente (em vez de ignorar em
        # silêncio) e segue no modo antigo, para não trancar o administrador.
        st.error(f"Configuração de logins (AINU_USERS) inválida: {erro_config}. Usando o modo de senha única.")

    if usuarios is None:  # modo antigo
        senha_esperada = os.environ.get("AINU_SYSTEMS_PASSWORD")
        if not senha_esperada:
            st.warning(txt("auth_nao_configurada"))
            return None
        if st.session_state.get("ainu_senha_unica_ok"):
            return None
        if not erro_config:
            st.caption("Modo senha única (AINU_USERS não definida neste serviço).")
        digitada = st.text_input(txt("senha_prompt"), type="password")
        if digitada and hmac.compare_digest(digitada, senha_esperada):
            st.session_state["ainu_senha_unica_ok"] = True
            st.rerun()
        if digitada:
            st.error(txt("senha_incorreta"))
        st.stop()

    if usuario_logado():
        with st.sidebar:
            st.caption(txt("login_logado_como").format(usuario=usuario_logado()))
            if st.button(txt("login_sair")):
                st.session_state.pop(_CHAVE_SESSAO, None)
                st.rerun()
        return usuario_logado()

    with st.form("ainu_login"):
        nome = st.text_input(txt("login_usuario"))
        senha = st.text_input(txt("senha_prompt"), type="password")
        enviado = st.form_submit_button(txt("login_entrar"))
    if enviado:
        nome = nome.strip()
        armazenado = usuarios.get(nome)
        # mesmo custo de cálculo se o usuário não existe (evita revelar quais existem)
        ok = verificar_hash(senha, armazenado or gerar_hash("x", 1000))
        if armazenado and ok:
            st.session_state[_CHAVE_SESSAO] = nome
            st.rerun()
        senha_antiga = os.environ.get("AINU_SYSTEMS_PASSWORD")
        login_antigo = os.environ.get("AINU_LEGACY_USER", _LOGIN_SENHA_ANTIGA)
        if senha_antiga and nome == login_antigo and hmac.compare_digest(senha, senha_antiga):
            st.session_state[_CHAVE_SESSAO] = nome
            st.rerun()
        time.sleep(1.0)
        st.error(txt("login_invalido"))
    st.stop()
