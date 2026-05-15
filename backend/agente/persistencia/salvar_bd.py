from typing import List, Dict, Any
from datetime import date
from sqlalchemy.orm import Session
from app.models import DadosBrutosPais, IndicesCalculados
import logging

logger = logging.getLogger(__name__)


def salvar_indices_bd(
    indices_calculados: List[Dict[str, Any]],
    db: Session
) -> None:
    """
    Salva os índices calculados no banco de dados.

    Cria registros em duas tabelas:
    1. dados_brutos_paises (dados coletados)
    2. indices_calculados (índices derivados)
    """

    registros_salvos = 0
    registros_erro = 0

    for indice in indices_calculados:
        try:
            # Salvar dados brutos
            dados_brutos = DadosBrutosPais(
                pais_id=indice["pais_id"],
                data_coleta=date.fromisoformat(indice["data_coleta"]) if isinstance(indice["data_coleta"], str) else indice["data_coleta"],
                pop_base_mi=indice["pop_base_mi"],
                pop_topo_mi=indice["pop_topo_mi"],
                nascimentos_mi=indice["nascimentos_mi"],
                mortes_mi=indice["mortes_mi"],
                tfr_2024=indice["tfr_2024"],
                tfr_1999=indice["tfr_1999"],
                va_bruto=indice["va_bruto"],
                emprego_total=indice["emprego_total"],
                salarios_totais=indice["salarios_totais"],
                yale_epi_score=indice["yale_epi_score"],
                t_ultraprocessados=indice["t_ultraprocessados"],
                u_agrotoxicos=indice["u_agrotoxicos"],
                m_medicalizado=indice["m_medicalizado"],
                i_inflamacao=indice["i_inflamacao"],
                ret_retorno_local=indice["ret_retorno_local"],
                comp_competitividade=indice["comp_competitividade"],
                sym_simbolismo=indice["sym_simbolismo"],
                confiabilidade=indice["confiabilidade"],
                metodo=indice["metodo"]
            )

            db.add(dados_brutos)
            db.flush()

            # Salvar índices calculados
            indices_calc = IndicesCalculados(
                pais_id=indice["pais_id"],
                data_calculo=date.fromisoformat(indice["data_coleta"]) if isinstance(indice["data_coleta"], str) else indice["data_coleta"],
                ngii_bruto=indice["ngii_bruto"],
                ngii_puro=indice["ngii_puro"],
                fator_geracional=indice["fator_geracional"],
                n_estrela=indice["n_estrela"],
                status_n=indice["status_n"],
                nih=indice["nih"],
                l_glocalizado=indice["l_glocalizado"],
                a_ext_epi=indice["a_ext_epi"],
                ncii=indice["ncii"],
                nsii=indice["nsii"],
                ies=indice["ies"],
                status_ies=indice["status_ies"]
            )

            db.add(indices_calc)

            registros_salvos += 1

        except Exception as e:
            logger.error(f"Erro ao salvar índices para {indice.get('pais_nome', 'UNKNOWN')}: {e}")
            registros_erro += 1
            continue

    try:
        db.commit()
        logger.info(f"✓ {registros_salvos} registros salvos com sucesso")

        if registros_erro > 0:
            logger.warning(f"⚠ {registros_erro} registros falharam")

    except Exception as e:
        logger.error(f"Erro no commit: {e}")
        db.rollback()
        raise
