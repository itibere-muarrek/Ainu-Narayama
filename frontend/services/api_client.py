import requests
import streamlit as st
from typing import Dict, Any, List, Optional
import json

class AIAClient:
    """Cliente para integração com API AINU-Narayama backend"""

    def __init__(self, base_url: str, token: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = 10

    def _headers(self) -> Dict[str, str]:
        """Retorna headers com autenticação"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _handle_error(self, response: requests.Response) -> None:
        """Trata erros HTTP"""
        if response.status_code == 401:
            st.error("❌ Sessão expirada. Faça login novamente.")
            if "token" in st.session_state:
                del st.session_state["token"]
        elif response.status_code == 403:
            st.error("❌ Acesso negado.")
        elif response.status_code == 404:
            st.error("❌ Recurso não encontrado.")
        else:
            try:
                error = response.json().get("detail", "Erro desconhecido")
            except:
                error = response.text
            st.error(f"❌ Erro: {error}")

    # ===== AUTENTICAÇÃO =====

    def registrar(self, nome: str, email: str, senha: str, instituicao: str = "") -> Dict[str, Any]:
        """Registra novo usuário"""
        url = f"{self.base_url}/auth/register"
        payload = {
            "nome": nome,
            "email": email,
            "senha": senha,
            "instituicao": instituicao
        }

        try:
            response = requests.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
            if response.status_code == 201:
                return response.json()
            else:
                self._handle_error(response)
                return None
        except requests.RequestException as e:
            st.error(f"❌ Erro de conexão: {e}")
            return None

    def login(self, email: str, senha: str) -> Dict[str, Any]:
        """Faz login e retorna tokens"""
        url = f"{self.base_url}/auth/login"
        payload = {"email": email, "senha": senha}

        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            else:
                self._handle_error(response)
                return None
        except requests.RequestException as e:
            st.error(f"❌ Erro de conexão: {e}")
            return None

    def me(self) -> Dict[str, Any]:
        """Retorna dados do usuário autenticado"""
        url = f"{self.base_url}/auth/me"

        try:
            response = requests.get(url, headers=self._headers(), timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            else:
                self._handle_error(response)
                return None
        except requests.RequestException as e:
            st.error(f"❌ Erro de conexão: {e}")
            return None

    # ===== PAÍSES =====

    def get_paises(self) -> List[Dict[str, Any]]:
        """Lista todos os países"""
        url = f"{self.base_url}/paises"

        try:
            response = requests.get(url, headers=self._headers(), timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            else:
                self._handle_error(response)
                return []
        except requests.RequestException as e:
            st.error(f"❌ Erro ao carregar países: {e}")
            return []

    def get_pais(self, pais_id: int) -> Optional[Dict[str, Any]]:
        """Obtém dados de um país específico"""
        url = f"{self.base_url}/paises/{pais_id}"

        try:
            response = requests.get(url, headers=self._headers(), timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            else:
                self._handle_error(response)
                return None
        except requests.RequestException as e:
            st.error(f"❌ Erro: {e}")
            return None

    # ===== CÁLCULOS =====

    def calcular_n_star(self, pais_id: int, dados_override: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Calcula N* para um país"""
        url = f"{self.base_url}/calculo/n-star"
        payload = {
            "pais_id": pais_id,
            "dados_override": dados_override
        }

        try:
            response = requests.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            else:
                self._handle_error(response)
                return None
        except requests.RequestException as e:
            st.error(f"❌ Erro no cálculo: {e}")
            return None

    def calcular_ies(self, pais_id: int, dados_override: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Calcula IES para um país"""
        url = f"{self.base_url}/calculo/ies"
        payload = {
            "pais_id": pais_id,
            "dados_override": dados_override
        }

        try:
            response = requests.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            else:
                self._handle_error(response)
                return None
        except requests.RequestException as e:
            st.error(f"❌ Erro no cálculo: {e}")
            return None

    def get_indices(self, pais_id: int) -> Optional[Dict[str, Any]]:
        """Obtém índices calculados de um país"""
        url = f"{self.base_url}/calculo/indices/{pais_id}"

        try:
            response = requests.get(url, headers=self._headers(), timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.RequestException:
            return None

    # ===== SIMULAÇÕES =====

    def criar_simulacao(self, tipo: str, pais_1_id: int, parametros_pais_1: Dict[str, Any],
                       pais_2_id: Optional[int] = None, parametros_pais_2: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Cria nova simulação"""
        url = f"{self.base_url}/simulacoes"
        payload = {
            "tipo": tipo,
            "pais_1_id": pais_1_id,
            "parametros_pais_1": parametros_pais_1,
            "pais_2_id": pais_2_id,
            "parametros_pais_2": parametros_pais_2
        }

        try:
            response = requests.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
            if response.status_code == 201:
                return response.json()
            else:
                self._handle_error(response)
                return None
        except requests.RequestException as e:
            st.error(f"❌ Erro ao criar simulação: {e}")
            return None

    def get_minhas_simulacoes(self, salvo_em_ficha: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Lista simulações do usuário"""
        url = f"{self.base_url}/simulacoes/usuario"
        params = {}
        if salvo_em_ficha is not None:
            params["salvo_em_ficha"] = salvo_em_ficha

        try:
            response = requests.get(url, headers=self._headers(), params=params, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except requests.RequestException:
            return []

    def atualizar_simulacao(self, simulacao_id: int, atualizacoes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Atualiza uma simulação"""
        url = f"{self.base_url}/simulacoes/{simulacao_id}"

        try:
            response = requests.put(url, json=atualizacoes, headers=self._headers(), timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            else:
                self._handle_error(response)
                return None
        except requests.RequestException as e:
            st.error(f"❌ Erro: {e}")
            return None

    def deletar_simulacao(self, simulacao_id: int) -> bool:
        """Deleta uma simulação"""
        url = f"{self.base_url}/simulacoes/{simulacao_id}"

        try:
            response = requests.delete(url, headers=self._headers(), timeout=self.timeout)
            if response.status_code == 204:
                st.success("✓ Simulação deletada!")
                return True
            else:
                self._handle_error(response)
                return False
        except requests.RequestException as e:
            st.error(f"❌ Erro: {e}")
            return False
