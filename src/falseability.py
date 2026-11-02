"""
Calibração histórica do autor sobre o NGII observado (referência, nunca o valor publicado).

O valor publicado é o N*_Obs (PQDF-N*, camada A), sem ajustes — ver src.data_pipeline. Esta função aplica os quatro ajustes
multiplicativos de src.config.AJUSTES_FALSEABILIDADE_POR_PAIS e alimenta as colunas *_cal e os cenários unitários
(n_estrela_mig/ine/pol/sub):

    NGII_cal = NGII_Obs × (1-migratorio) × (1-inercia) × (1-politicas) × (1-subregistro)

Os valores dos ajustes são calibração do autor, sem fonte automatizável (docs/definitions.md, seção 6).
"""

from typing import Dict


def aplicar_falseabilidade_quantitativa(ngii_bruto: float, ajustes: Dict[str, float]) -> float:
    """
    Aplica a calibração histórica do autor (4 ajustes multiplicativos) ao NGII observado.

    Transforma o NGII_Obs (razão demográfica calculada diretamente de
    Pop_Base/Pop_Topo/Nascimentos/Mortes, sem nenhum ajuste) em NGII_cal,
    mediante desconto multiplicativo composto — não a soma simples dos
    percentuais.

    Fórmula:
        NGII_cal = NGII_Obs × (1-migratorio) × (1-inercia) × (1-politicas) × (1-subregistro)

    Args:
        ngii_bruto: NGII calculado sem ajustes de falseabilidade
            (resultado de calcular_ngii_puro() em src/indices.py).
        ajustes: dict com as chaves "migratorio", "inercia", "politicas",
            "subregistro" (frações entre 0 e 1) — ver
            src.config.AJUSTES_FALSEABILIDADE_POR_PAIS para os valores
            calibrados dos 28 países.

    Returns:
        NGII_cal (adimensional).

    Exemplo (Brasil, dados reais 2024 pós-recalibração de perfis):
        >>> aplicar_falseabilidade_quantitativa(
        ...     2.9493,
        ...     {"migratorio": 0.12, "inercia": 0.15, "politicas": 0.06, "subregistro": 0.04},
        ... )
        1.9907633433599998
    """
    return (
        ngii_bruto
        * (1 - ajustes["migratorio"])
        * (1 - ajustes["inercia"])
        * (1 - ajustes["politicas"])
        * (1 - ajustes["subregistro"])
    )
