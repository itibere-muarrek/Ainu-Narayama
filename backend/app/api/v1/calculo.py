from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional, Dict, Any

from app.database import get_db
from app.models import Pais, DadosBrutosPais, IndicesCalculados, Usuario
from app.schemas import ResultadoNStar, ResultadoIES, ParametrosCalculo
from app.security import get_current_user, get_current_active_user
from app.services.calculo_n import calcular_n_star
from app.services.calculo_ies import calcular_ies_completo, calcular_l, calcular_ncii, calcular_nsii
from app.services.calculo_nih import calcular_nih

router = APIRouter(prefix="/calculo", tags=["cálculos"])


@router.post("/n-star", response_model=ResultadoNStar)
async def calculo_n_star(
    parametros: ParametrosCalculo,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Calcula N* (Net Generational Impact Index) para um país.

    Pode usar dados reais do BD ou parametros sobrescritados.
    """

    # Obter país
    pais = db.query(Pais).filter(Pais.id == parametros.pais_id).first()
    if not pais:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="País não encontrado"
        )

    # Obter dados mais recentes
    dados = db.query(DadosBrutosPais).filter(
        DadosBrutosPais.pais_id == parametros.pais_id
    ).order_by(DadosBrutosPais.data_coleta.desc()).first()

    if not dados:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dados brutos não encontrados para este país"
        )

    # Parâmetros de cálculo
    pop_base_mi = parametros.dados_override.get("pop_base_mi", dados.pop_base_mi or 0) if parametros.dados_override else (dados.pop_base_mi or 0)
    pop_topo_mi = parametros.dados_override.get("pop_topo_mi", dados.pop_topo_mi or 0) if parametros.dados_override else (dados.pop_topo_mi or 0)
    nascimentos_mi = parametros.dados_override.get("nascimentos_mi", dados.nascimentos_mi or 0) if parametros.dados_override else (dados.nascimentos_mi or 0)
    mortes_mi = parametros.dados_override.get("mortes_mi", dados.mortes_mi or 0) if parametros.dados_override else (dados.mortes_mi or 0)
    tfr_2024 = parametros.dados_override.get("tfr_2024", dados.tfr_2024 or 0) if parametros.dados_override else (dados.tfr_2024 or 0)
    tfr_1999 = parametros.dados_override.get("tfr_1999", dados.tfr_1999 or 0) if parametros.dados_override else (dados.tfr_1999 or 0)

    # Validações
    if any(v is None or v <= 0 for v in [pop_base_mi, pop_topo_mi, nascimentos_mi, mortes_mi, tfr_2024, tfr_1999]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dados insuficientes ou inválidos para cálculo de N*"
        )

    try:
        resultado = calcular_n_star(
            pop_base_mi=pop_base_mi,
            pop_topo_mi=pop_topo_mi,
            nascimentos_mi=nascimentos_mi,
            mortes_mi=mortes_mi,
            tfr_2024=tfr_2024,
            tfr_1999=tfr_1999
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    # Salvar resultado no BD
    indice = IndicesCalculados(
        pais_id=parametros.pais_id,
        data_calculo=date.today(),
        ngii_bruto=resultado["ngii_bruto"],
        ngii_puro=resultado["ngii_puro"],
        fator_geracional=resultado["fator_geracional"],
        n_estrela=resultado["n_estrela"],
        status_n=resultado["status_n"]
    )

    db.add(indice)
    db.commit()

    return ResultadoNStar(
        pais_id=parametros.pais_id,
        **resultado
    )


@router.post("/ies", response_model=ResultadoIES)
async def calculo_ies(
    parametros: ParametrosCalculo,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Calcula IES (Índice de Estabilidade Sistêmica) para um país.

    Pode usar dados reais do BD ou parâmetros sobrescritados.
    """

    # Obter país
    pais = db.query(Pais).filter(Pais.id == parametros.pais_id).first()
    if not pais:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="País não encontrado"
        )

    # Obter dados mais recentes
    dados = db.query(DadosBrutosPais).filter(
        DadosBrutosPais.pais_id == parametros.pais_id
    ).order_by(DadosBrutosPais.data_coleta.desc()).first()

    if not dados:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dados brutos não encontrados para este país"
        )

    # Obter N* mais recente
    indices = db.query(IndicesCalculados).filter(
        IndicesCalculados.pais_id == parametros.pais_id
    ).order_by(IndicesCalculados.data_calculo.desc()).first()

    if not indices or indices.ngii_puro is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="N* não calculado. Execute /calculo/n-star primeiro"
        )

    # Parâmetros
    override = parametros.dados_override or {}
    ngii_puro = indices.ngii_puro
    va_bruto = override.get("va_bruto", dados.va_bruto or 0)
    emprego_total = override.get("emprego_total", dados.emprego_total or 0)
    salarios_totais = override.get("salarios_totais", dados.salarios_totais or 0)
    ret_retorno_local = override.get("ret_retorno_local", dados.ret_retorno_local or 0)
    comp_competitividade = override.get("comp_competitividade", dados.comp_competitividade or 0)
    sym_simbolismo = override.get("sym_simbolismo", dados.sym_simbolismo or 0)
    yale_epi_score = override.get("yale_epi_score", dados.yale_epi_score or 0)
    t_ultraprocessados = override.get("t_ultraprocessados", dados.t_ultraprocessados or 0)
    u_agrotoxicos = override.get("u_agrotoxicos", dados.u_agrotoxicos or 0)
    m_medicalizado = override.get("m_medicalizado", dados.m_medicalizado or 0)
    i_inflamacao = override.get("i_inflamacao", dados.i_inflamacao or 0)

    try:
        resultado = calcular_ies_completo(
            ngii_puro=ngii_puro,
            va_bruto=va_bruto,
            emprego_total=emprego_total,
            salarios_totais=salarios_totais,
            ret_retorno_local=ret_retorno_local,
            comp_competitividade=comp_competitividade,
            sym_simbolismo=sym_simbolismo,
            yale_epi_score=yale_epi_score,
            t_ultraprocessados=t_ultraprocessados,
            u_agrotoxicos=u_agrotoxicos,
            m_medicalizado=m_medicalizado,
            i_inflamacao=i_inflamacao
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    # Salvar resultado
    indices.nih = resultado.get("nih")
    indices.l_glocalizado = resultado.get("l")
    indices.a_ext_epi = resultado.get("a_ext_epi")
    indices.ncii = resultado.get("ncii")
    indices.nsii = resultado.get("nsii")
    indices.ies = resultado.get("ies")
    indices.status_ies = resultado.get("status_ies")

    db.commit()

    return ResultadoIES(
        pais_id=parametros.pais_id,
        nih=resultado.get("nih"),
        l_glocalizado=resultado.get("l"),
        a_ext_epi=resultado.get("a_ext_epi"),
        ncii=resultado.get("ncii"),
        nsii=resultado.get("nsii"),
        ies=resultado.get("ies"),
        status_ies=resultado.get("status_ies")
    )


@router.get("/indices/{pais_id}", response_model=Dict[str, Any])
async def obter_indices(
    pais_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Retorna os índices calculados mais recentes de um país"""

    indices = db.query(IndicesCalculados).filter(
        IndicesCalculados.pais_id == pais_id
    ).order_by(IndicesCalculados.data_calculo.desc()).first()

    if not indices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum índice calculado para este país"
        )

    return {
        "id": indices.id,
        "pais_id": indices.pais_id,
        "data_calculo": indices.data_calculo.isoformat(),
        "n_estrela": indices.n_estrela,
        "status_n": indices.status_n,
        "ies": indices.ies,
        "status_ies": indices.status_ies,
        "ngii_bruto": indices.ngii_bruto,
        "ngii_puro": indices.ngii_puro,
        "fator_geracional": indices.fator_geracional,
        "nih": indices.nih,
        "l_glocalizado": indices.l_glocalizado,
        "a_ext_epi": indices.a_ext_epi,
        "ncii": indices.ncii,
        "nsii": indices.nsii
    }
