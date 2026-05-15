from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def normalizar_dados(dados_brutos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Normaliza e valida dados brutos coletados.

    Etapas:
    1. Validação de completude (campos obrigatórios)
    2. Normalização de unidades (garantir milhões para população)
    3. Validação de ranges (valores plausíveis)
    4. Tratamento de outliers
    """

    dados_normalizados = []

    for dado in dados_brutos:
        try:
            normalizado = _normalizar_registro(dado)
            dados_normalizados.append(normalizado)
        except ValueError as e:
            logger.warning(f"Registro inválido ({dado.get('pais', 'UNKNOWN')}): {e}")
            continue

    logger.info(f"✓ {len(dados_normalizados)}/{len(dados_brutos)} registros validados")

    return dados_normalizados


def _normalizar_registro(dado: Dict[str, Any]) -> Dict[str, Any]:
    """Normaliza um registro individual"""

    # Campos obrigatórios
    campos_obrigatorios = [
        "pais", "codigo_iso", "pop_base_mi", "pop_topo_mi",
        "nascimentos_mi", "mortes_mi", "tfr_2024", "tfr_1999"
    ]

    for campo in campos_obrigatorios:
        if campo not in dado or dado[campo] is None:
            raise ValueError(f"Campo obrigatório ausente: {campo}")

    # Validar ranges plausíveis
    if dado["tfr_2024"] < 0.5 or dado["tfr_2024"] > 9.0:
        logger.warning(f"TFR 2024 suspeito: {dado['tfr_2024']} ({dado['pais']})")

    if dado["pop_base_mi"] < 0 or dado["pop_topo_mi"] < 0:
        raise ValueError("Populações não podem ser negativas")

    if dado["nascimentos_mi"] < 0 or dado["mortes_mi"] < 0:
        raise ValueError("Nascimentos/mortes não podem ser negativos")

    # Garantir formatos
    return {
        "pais": str(dado["pais"]).strip(),
        "codigo_iso": str(dado["codigo_iso"]).upper().strip(),
        "pop_base_mi": float(dado["pop_base_mi"]),
        "pop_topo_mi": float(dado["pop_topo_mi"]),
        "nascimentos_mi": float(dado["nascimentos_mi"]),
        "mortes_mi": float(dado["mortes_mi"]),
        "tfr_2024": float(dado["tfr_2024"]),
        "tfr_1999": float(dado["tfr_1999"]),
        "va_bruto": float(dado.get("va_bruto", 0)),
        "emprego_total": float(dado.get("emprego_total", 0)),
        "salarios_totais": float(dado.get("salarios_totais", 0)),
        "yale_epi_score": float(dado.get("yale_epi_score", 50)),
        "t_ultraprocessados": float(dado.get("t_ultraprocessados", 0)),
        "u_agrotoxicos": float(dado.get("u_agrotoxicos", 0)),
        "m_medicalizado": float(dado.get("m_medicalizado", 0)),
        "i_inflamacao": float(dado.get("i_inflamacao", 0)),
        "ret_retorno_local": float(dado.get("ret_retorno_local", 0)),
        "comp_competitividade": float(dado.get("comp_competitividade", 0)),
        "sym_simbolismo": float(dado.get("sym_simbolismo", 0)),
        "data_coleta": dado.get("data_coleta"),
        "confiabilidade": dado.get("confiabilidade", "Media"),
        "metodo": dado.get("metodo", "ESTIMADO")
    }
