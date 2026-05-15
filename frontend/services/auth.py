import streamlit as st
import jwt
from datetime import datetime
from typing import Optional, Dict, Any
import os

class AuthManager:
    """Gerencia autenticação e tokens JWT localmente"""

    def __init__(self):
        self.token_key = "token"
        self.user_key = "user"
        self.refresh_token_key = "refresh_token"

    def salvar_token(self, token: str, refresh_token: str, user_data: Dict[str, Any]) -> None:
        """Salva tokens e dados do usuário na sessão"""
        st.session_state[self.token_key] = token
        st.session_state[self.refresh_token_key] = refresh_token
        st.session_state[self.user_key] = user_data

    def obter_token(self) -> Optional[str]:
        """Retorna token atual"""
        return st.session_state.get(self.token_key)

    def obter_usuario(self) -> Optional[Dict[str, Any]]:
        """Retorna dados do usuário autenticado"""
        return st.session_state.get(self.user_key)

    def esta_autenticado(self) -> bool:
        """Verifica se usuário está autenticado"""
        return self.obter_token() is not None

    def esta_aprovado(self) -> bool:
        """Verifica se usuário está APROVADO (status = ATIVO)"""
        user = self.obter_usuario()
        if not user:
            return False
        return user.get("status") == "ATIVO"

    def e_admin(self) -> bool:
        """Verifica se usuário é ADMIN"""
        user = self.obter_usuario()
        if not user:
            return False
        return user.get("tipo_usuario") == "ADMIN"

    def e_co_admin(self) -> bool:
        """Verifica se usuário é CO-ADMIN"""
        user = self.obter_usuario()
        if not user:
            return False
        return user.get("tipo_usuario") == "CO-ADMIN"

    def e_co_admin_ou_admin(self) -> bool:
        """Verifica se é CO-ADMIN ou ADMIN"""
        return self.e_co_admin() or self.e_admin()

    def logout(self) -> None:
        """Remove tokens e dados do usuário"""
        if self.token_key in st.session_state:
            del st.session_state[self.token_key]
        if self.refresh_token_key in st.session_state:
            del st.session_state[self.refresh_token_key]
        if self.user_key in st.session_state:
            del st.session_state[self.user_key]

    def nome_usuario(self) -> str:
        """Retorna nome do usuário ou 'Visitante'"""
        user = self.obter_usuario()
        return user.get("nome", "Visitante") if user else "Visitante"

    def email_usuario(self) -> Optional[str]:
        """Retorna email do usuário"""
        user = self.obter_usuario()
        return user.get("email") if user else None

    def verificar_token_expirado(self) -> bool:
        """Verifica se token JWT expirou"""
        token = self.obter_token()
        if not token:
            return True

        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            exp = payload.get("exp")
            if exp:
                return datetime.fromtimestamp(exp) < datetime.now()
        except:
            pass

        return False


# Instância global
auth_manager = AuthManager()
