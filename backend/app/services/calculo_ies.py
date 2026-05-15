from typing import Dict, Any
from app.services.calculo_nih import calcular_nih


def calcular_l(
    ret_retorno_local: float,
    comp_competitividade: float,
    sym_simbolismo: float
) -> float:
    """
    Calcula o componente L (Glocalizado).

    Fórmula:
    L = 0.4·RET + 0.3·COMP + 0.3·SYM

    Onde todos os valores devem estar entre 0-1 (ou 0-100%).
    """

    # Normalizar se necessário
    if ret_retorno_local > 1:
        ret_retorno_local = ret_retorno_local / 100
    if comp_competitividade > 1:
        comp_competitividade = comp_competitividade / 100
    if sym_simbolismo > 1:
        sym_simbolismo = sym_simbolismo / 100

    if not all(0 <= v <= 1 for v in [ret_retorno_local, comp_competitividade, sym_simbolismo]):
        raise ValueError("L: Valores devem estar entre 0 e 1")

    l = 0.4 * ret_retorno_local + 0.3 * comp_competitividade + 0.3 * sym_simbolismo
    return round(l, 4)


def calcular_ncii(
    va_bruto: float,
    emprego_total: float,
    salarios_totais: float
) -> float:
    """
    Calcula o índice NCII (Competitive Comparative Institutional Index).

    Fórmula:
    NCII = (VA / Emprego) × (Salários / VA)

    Onde:
    - VA = Valor Agregado
    - Emprego = Total de emprego
    - Salários = Total de salários
    """

    if emprego_total == 0 or va_bruto == 0:
        raise ValueError("VA_Bruto e Emprego_Total não podem ser zero")

    produtividade = va_bruto / emprego_total
    participacao_salarial = salarios_totais / va_bruto if va_bruto != 0 else 0

    ncii = produtividade * participacao_salarial
    return round(ncii, 4)


def calcular_nsii(
    a_ext_epi: float,
    nih: float
) -> float:
    """
    Calcula o índice NSII (Nutritional Systemic Impact Index).

    Fórmula:
    NSII = 0.45·A_ext + 0.55·NIH

    Onde:
    - A_ext = Yale EPI Score normalizado (0-1)
    - NIH = Índice calculado anteriormente
    """

    if not all(0 <= v <= 1 for v in [a_ext_epi, nih]):
        raise ValueError("A_ext_epi e NIH devem estar entre 0 e 1")

    nsii = 0.45 * a_ext_epi + 0.55 * nih
    return round(nsii, 4)


def calcular_ies(
    ngii_puro: float,
    ncii: float,
    nsii: float,
    l: float
) -> Dict[str, Any]:
    """
    Calcula o índice IES (Índice de Estabilidade Sistêmica).

    Fórmula:
    IES = L × ∛(NGII × NCII × NSII)

    Onde:
    - L = Componente Glocalizado
    - NGII = Net Generational Impact Index
    - NCII = Competitive Comparative Institutional Index
    - NSII = Nutritional Systemic Impact Index

    Retorna dicionário com IES e status.
    """

    if any(v < 0 for v in [ngii_puro, ncii, nsii, l]):
        raise ValueError("Valores negativos não permitidos")

    # Cálculo: raiz cúbica do produto
    produto = ngii_puro * ncii * nsii
    raiz_cubica = produto ** (1/3) if produto >= 0 else 0

    ies = l * raiz_cubica
    ies = round(ies, 4)

    # Status IES
    if ies >= 1.0:
        status_ies = "ESTAVEL"
    elif ies >= 0.5:
        status_ies = "TRANSICAO"
    else:
        status_ies = "CRITICO"

    return {
        "ies": ies,
        "l": round(l, 4),
        "ncii": round(ncii, 4),
        "nsii": round(nsii, 4),
        "raiz_cubica": round(raiz_cubica, 4),
        "status_ies": status_ies
    }


def calcular_ies_completo(
    ngii_puro: float,
    va_bruto: float,
    emprego_total: float,
    salarios_totais: float,
    ret_retorno_local: float,
    comp_competitividade: float,
    sym_simbolismo: float,
    yale_epi_score: float,
    t_ultraprocessados: float,
    u_agrotoxicos: float,
    m_medicalizado: float,
    i_inflamacao: float
) -> Dict[str, Any]:
    """
    Cálculo completo do IES com todos os componentes.
    """

    # Calcular L
    l = calcular_l(ret_retorno_local, comp_competitividade, sym_simbolismo)

    # Calcular NCII
    ncii = calcular_ncii(va_bruto, emprego_total, salarios_totais)

    # Calcular NIH
    nih_data = calcular_nih(t_ultraprocessados, u_agrotoxicos, m_medicalizado, i_inflamacao)
    nih = nih_data["nih"]

    # Normalizar Yale EPI Score para 0-1
    a_ext_epi = yale_epi_score / 100 if yale_epi_score > 1 else yale_epi_score

    # Calcular NSII
    nsii = calcular_nsii(a_ext_epi, nih)

    # Calcular IES final
    resultado = calcular_ies(ngii_puro, ncii, nsii, l)

    # Adicionar componentes
    resultado.update({
        "nih": nih,
        "a_ext_epi": round(a_ext_epi, 4),
        "yale_epi_score": round(yale_epi_score, 4)
    })

    return resultado
