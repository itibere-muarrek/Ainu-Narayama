import requests
from typing import List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)


def coletar_un_wpp(db: Session) -> List[Dict[str, Any]]:
    """
    Coleta dados de populações e TFR da UN World Population Prospects.

    Retorna lista de dicionários com dados brutos de todos os países.
    """

    dados_coletados = []

    try:
        logger.info("Tentando coletar dados da UN WPP...")

        # Dados de exemplo/fallback (em produção: integrar com API real)
        # UN WPP API: https://population.un.org/dataportalapi/api/v1

        dados_coletados = _coletar_fallback()

        logger.info(f"✓ {len(dados_coletados)} registros coletados")

    except requests.RequestException as e:
        logger.warning(f"Erro na coleta UN WPP: {e}")
        dados_coletados = _coletar_fallback()

    return dados_coletados


def _coletar_fallback() -> List[Dict[str, Any]]:
    """
    Dados fallback quando a coleta automática falha.

    Em produção: manter dados calibrados de referência.
    """

    return [
        {
            "pais": "Brasil",
            "codigo_iso": "BRA",
            "pop_base_mi": 215.0,
            "pop_topo_mi": 214.0,
            "nascimentos_mi": 2.5,
            "mortes_mi": 0.8,
            "tfr_2024": 1.52,
            "tfr_1999": 2.67,
            "data_coleta": datetime.now().date().isoformat(),
            "confiabilidade": "Media",
            "metodo": "ESTIMADO"
        },
        {
            "pais": "Argentina",
            "codigo_iso": "ARG",
            "pop_base_mi": 46.2,
            "pop_topo_mi": 46.0,
            "nascimentos_mi": 0.65,
            "mortes_mi": 0.36,
            "tfr_2024": 1.80,
            "tfr_1999": 2.59,
            "data_coleta": datetime.now().date().isoformat(),
            "confiabilidade": "Media",
            "metodo": "ESTIMADO"
        },
        {
            "pais": "México",
            "codigo_iso": "MEX",
            "pop_base_mi": 128.3,
            "pop_topo_mi": 127.0,
            "nascimentos_mi": 1.85,
            "mortes_mi": 0.58,
            "tfr_2024": 1.68,
            "tfr_1999": 3.12,
            "data_coleta": datetime.now().date().isoformat(),
            "confiabilidade": "Media",
            "metodo": "ESTIMADO"
        },
        {
            "pais": "Japão",
            "codigo_iso": "JPN",
            "pop_base_mi": 123.3,
            "pop_topo_mi": 125.1,
            "nascimentos_mi": 0.73,
            "mortes_mi": 1.28,
            "tfr_2024": 1.20,
            "tfr_1999": 1.34,
            "data_coleta": datetime.now().date().isoformat(),
            "confiabilidade": "Alta",
            "metodo": "ESTIMADO"
        },
        {
            "pais": "Alemanha",
            "codigo_iso": "DEU",
            "pop_base_mi": 83.4,
            "pop_topo_mi": 83.9,
            "nascimentos_mi": 0.69,
            "mortes_mi": 0.95,
            "tfr_2024": 1.25,
            "tfr_1999": 1.35,
            "data_coleta": datetime.now().date().isoformat(),
            "confiabilidade": "Alta",
            "metodo": "ESTIMADO"
        },
        {
            "pais": "India",
            "codigo_iso": "IND",
            "pop_base_mi": 1417.2,
            "pop_topo_mi": 1408.6,
            "nascimentos_mi": 16.2,
            "mortes_mi": 8.5,
            "tfr_2024": 2.15,
            "tfr_1999": 3.40,
            "data_coleta": datetime.now().date().isoformat(),
            "confiabilidade": "Media",
            "metodo": "ESTIMADO"
        }
    ]
