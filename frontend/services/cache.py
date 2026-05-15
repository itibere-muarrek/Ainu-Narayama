import streamlit as st
from datetime import datetime, timedelta
from typing import Any, Optional, Callable
import hashlib

class CacheManager:
    """Gerencia cache em st.session_state com expiração"""

    def __init__(self, ttl_seconds: int = 300):
        """
        Inicializa cache manager.

        Args:
            ttl_seconds: Time-to-live padrão em segundos (5 min default)
        """
        self.ttl_seconds = ttl_seconds
        self.cache_key = "_ainu_cache"

    def _obter_cache(self) -> dict:
        """Obtém dicionário de cache da sessão"""
        if self.cache_key not in st.session_state:
            st.session_state[self.cache_key] = {}
        return st.session_state[self.cache_key]

    def _gerar_chave(self, funcao: str, args: tuple, kwargs: dict) -> str:
        """Gera chave única para cache"""
        chave_str = f"{funcao}:{args}:{sorted(kwargs.items())}"
        return hashlib.md5(chave_str.encode()).hexdigest()

    def get(self, chave: str) -> Optional[Any]:
        """Obtém valor do cache se ainda válido"""
        cache = self._obter_cache()
        if chave not in cache:
            return None

        item = cache[chave]
        if datetime.now() > item["expira_em"]:
            del cache[chave]
            return None

        return item["valor"]

    def set(self, chave: str, valor: Any, ttl: Optional[int] = None) -> None:
        """Salva valor no cache com expiração"""
        cache = self._obter_cache()
        ttl = ttl or self.ttl_seconds
        cache[chave] = {
            "valor": valor,
            "expira_em": datetime.now() + timedelta(seconds=ttl)
        }

    def limpar(self) -> None:
        """Limpa todo o cache"""
        if self.cache_key in st.session_state:
            st.session_state[self.cache_key] = {}

    def limpar_chave(self, chave: str) -> None:
        """Limpa uma chave específica"""
        cache = self._obter_cache()
        if chave in cache:
            del cache[chave]


# Instâncias globais de cache
cache_manager = CacheManager(ttl_seconds=300)  # 5 minutos
paises_cache = CacheManager(ttl_seconds=600)   # 10 minutos
