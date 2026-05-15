from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models import Pais
from app.services.calculo_n import calcular_n_star
from app.services.calculo_ies import calcular_ies_completo
import logging

logger = logging.getLogger(__name__)


def calcular_todos_indices(
    dados_processados: List[Dict[str, Any]],
    db: Session
) -> List[Dict[str, Any]]:
    """
    Calcula índices N* e IES para todos os países.

    Retorna lista de dicionários com índices calculados.
    """

    indices_calculados = []

    for dado in dados_processados:
        try:
            # Obter país do BD
            pais = db.query(Pais).filter(
                Pais.codigo_iso == dado["codigo_iso"]
            ).first()

            if not pais:
                logger.warning(f"País não encontrado no BD: {dado['pais']}")
                continue

            # Calcular N*
            n_star = calcular_n_star(
                pop_base_mi=dado["pop_base_mi"],
                pop_topo_mi=dado["pop_topo_mi"],
                nascimentos_mi=dado["nascimentos_mi"],
                mortes_mi=dado["mortes_mi"],
                tfr_2024=dado["tfr_2024"],
                tfr_1999=dado["tfr_1999"]
            )

            # Calcular IES
            ies = calcular_ies_completo(
                ngii_puro=n_star["ngii_puro"],
                va_bruto=dado["va_bruto"],
                emprego_total=dado["emprego_total"],
                salarios_totais=dado["salarios_totais"],
                ret_retorno_local=dado["ret_retorno_local"],
                comp_competitividade=dado["comp_competitividade"],
                sym_simbolismo=dado["sym_simbolismo"],
                yale_epi_score=dado["yale_epi_score"],
                t_ultraprocessados=dado["t_ultraprocessados"],
                u_agrotoxicos=dado["u_agrotoxicos"],
                m_medicalizado=dado["m_medicalizado"],
                i_inflamacao=dado["i_inflamacao"]
            )

            # Compilar resultado
            resultado = {
                "pais_id": pais.id,
                "pais_nome": pais.nome,
                "codigo_iso": dado["codigo_iso"],
                "data_coleta": dado["data_coleta"],
                "confiabilidade": dado["confiabilidade"],
                "metodo": dado["metodo"],
                # Dados brutos
                "pop_base_mi": dado["pop_base_mi"],
                "pop_topo_mi": dado["pop_topo_mi"],
                "nascimentos_mi": dado["nascimentos_mi"],
                "mortes_mi": dado["mortes_mi"],
                "tfr_2024": dado["tfr_2024"],
                "tfr_1999": dado["tfr_1999"],
                "va_bruto": dado["va_bruto"],
                "emprego_total": dado["emprego_total"],
                "salarios_totais": dado["salarios_totais"],
                "yale_epi_score": dado["yale_epi_score"],
                "t_ultraprocessados": dado["t_ultraprocessados"],
                "u_agrotoxicos": dado["u_agrotoxicos"],
                "m_medicalizado": dado["m_medicalizado"],
                "i_inflamacao": dado["i_inflamacao"],
                "ret_retorno_local": dado["ret_retorno_local"],
                "comp_competitividade": dado["comp_competitividade"],
                "sym_simbolismo": dado["sym_simbolismo"],
                # Índices calculados
                "ngii_bruto": n_star["ngii_bruto"],
                "ngii_puro": n_star["ngii_puro"],
                "fator_geracional": n_star["fator_geracional"],
                "n_estrela": n_star["n_estrela"],
                "status_n": n_star["status_n"],
                "nih": ies.get("nih"),
                "l_glocalizado": ies.get("l"),
                "a_ext_epi": ies.get("a_ext_epi"),
                "ncii": ies.get("ncii"),
                "nsii": ies.get("nsii"),
                "ies": ies.get("ies"),
                "status_ies": ies.get("status_ies")
            }

            indices_calculados.append(resultado)
            logger.info(f"  ✓ {pais.nome}: N*={n_star['n_estrela']:.3f}, IES={ies.get('ies', 0):.3f}")

        except Exception as e:
            logger.error(f"Erro ao calcular índices para {dado.get('pais', 'UNKNOWN')}: {e}")
            continue

    return indices_calculados
