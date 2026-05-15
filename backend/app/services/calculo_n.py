from typing import Dict, Any, Optional
from app.models import StatusN


def calcular_n_star(
    pop_base_mi: float,
    pop_topo_mi: float,
    nascimentos_mi: float,
    mortes_mi: float,
    tfr_2024: float,
    tfr_1999: float
) -> Dict[str, Any]:
    """
    Calcula o índice N* (N-Estrela) com seus componentes.

    Fórmulas:
    - NGII_Bruto = (Pop_Base / Pop_Topo) × (Nasc / Mortes)
    - Fator_Geracional = TFR_2024 / TFR_1999
    - NGII_Puro = NGII_Bruto × Fator_Geracional
    - N* = NGII_Puro (resultado final)

    Retorna dicionário com:
    - ngii_bruto
    - ngii_puro
    - fator_geracional
    - n_estrela
    - status_n (PROMISSOR, EQUILIBRIO, CRITICO, COLAPSO)
    """

    # Validação básica
    if pop_topo_mi == 0 or mortes_mi == 0 or tfr_1999 == 0:
        raise ValueError("Divisor não pode ser zero (Pop_Topo, Mortes, TFR_1999)")

    if any(v < 0 for v in [pop_base_mi, pop_topo_mi, nascimentos_mi, mortes_mi, tfr_2024, tfr_1999]):
        raise ValueError("Valores negativos não permitidos")

    # Cálculos
    ngii_bruto = (pop_base_mi / pop_topo_mi) * (nascimentos_mi / mortes_mi)
    fator_geracional = tfr_2024 / tfr_1999
    ngii_puro = ngii_bruto * fator_geracional
    n_estrela = ngii_puro

    # Status baseado em valor de N*
    if n_estrela >= 1.5:
        status_n = StatusN.PROMISSOR
    elif n_estrela >= 1.0:
        status_n = StatusN.EQUILIBRIO
    elif n_estrela >= 0.5:
        status_n = StatusN.CRITICO
    else:
        status_n = StatusN.COLAPSO

    return {
        "ngii_bruto": round(ngii_bruto, 4),
        "ngii_puro": round(ngii_puro, 4),
        "fator_geracional": round(fator_geracional, 4),
        "n_estrela": round(n_estrela, 4),
        "status_n": status_n.value
    }


def validar_n_star(n_estrela: float) -> str:
    """Valida e retorna o status do N*"""
    if n_estrela >= 1.5:
        return "PROMISSOR"
    elif n_estrela >= 1.0:
        return "EQUILIBRIO"
    elif n_estrela >= 0.5:
        return "CRITICO"
    else:
        return "COLAPSO"
