from typing import Dict, Any


def calcular_nih(
    t_ultraprocessados: float,
    u_agrotoxicos: float,
    m_medicalizado: float,
    i_inflamacao: float
) -> Dict[str, Any]:
    """
    Calcula o índice NIH (Nutrient Impact Health).

    Fórmula:
    NIH = 1 − (0.35·T + 0.25·U + 0.20·M + 0.20·I)

    Onde:
    - T = Taxa de Ultraprocessados (0-1)
    - U = Taxa de Agrotóxicos (0-1)
    - M = Taxa Medicalizada (0-1)
    - I = Taxa de Inflamação (0-1)

    Retorna:
    - nih: float (0-1)
    """

    # Normalizar percentuais para 0-1 se necessário
    if t_ultraprocessados > 1:
        t_ultraprocessados = t_ultraprocessados / 100
    if u_agrotoxicos > 1:
        u_agrotoxicos = u_agrotoxicos / 100
    if m_medicalizado > 1:
        m_medicalizado = m_medicalizado / 100
    if i_inflamacao > 1:
        i_inflamacao = i_inflamacao / 100

    # Validação
    if not all(0 <= v <= 1 for v in [t_ultraprocessados, u_agrotoxicos, m_medicalizado, i_inflamacao]):
        raise ValueError("Valores devem estar entre 0 e 1 (ou 0-100%)")

    # Cálculo NIH
    nih = 1 - (0.35 * t_ultraprocessados + 0.25 * u_agrotoxicos + 0.20 * m_medicalizado + 0.20 * i_inflamacao)
    nih = max(0, min(1, nih))  # Garante resultado entre 0 e 1

    return {
        "nih": round(nih, 4),
        "t_ultraprocessados": round(t_ultraprocessados, 4),
        "u_agrotoxicos": round(u_agrotoxicos, 4),
        "m_medicalizado": round(m_medicalizado, 4),
        "i_inflamacao": round(i_inflamacao, 4)
    }
