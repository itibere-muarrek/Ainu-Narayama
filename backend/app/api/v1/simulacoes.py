from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database import get_db
from app.models import SimulacaoCliente, Usuario, Pais, DadosBrutosPais
from app.schemas import Simulacao, SimulacaoCreate, SimulacaoUpdate
from app.security import get_current_user, get_current_active_user
from app.services.calculo_n import calcular_n_star
from app.services.calculo_ies import calcular_ies_completo
from app.services.analise_agente import analisar_cenario

router = APIRouter(prefix="/simulacoes", tags=["simulações"])


def _executar_calculo(tipo: str, pais_id: int, parametros: Dict[str, Any], db: Session) -> Dict[str, Any]:
    """Helper para executar cálculo baseado no tipo"""

    # Obter dados do país
    dados = db.query(DadosBrutosPais).filter(
        DadosBrutosPais.pais_id == pais_id
    ).order_by(DadosBrutosPais.data_coleta.desc()).first()

    if not dados:
        raise ValueError("Dados não encontrados para este país")

    # Mesclar parametros com dados reais
    dados_completos = {
        "pop_base_mi": parametros.get("pop_base_mi", dados.pop_base_mi or 0),
        "pop_topo_mi": parametros.get("pop_topo_mi", dados.pop_topo_mi or 0),
        "nascimentos_mi": parametros.get("nascimentos_mi", dados.nascimentos_mi or 0),
        "mortes_mi": parametros.get("mortes_mi", dados.mortes_mi or 0),
        "tfr_2024": parametros.get("tfr_2024", dados.tfr_2024 or 0),
        "tfr_1999": parametros.get("tfr_1999", dados.tfr_1999 or 0),
        "va_bruto": parametros.get("va_bruto", dados.va_bruto or 0),
        "emprego_total": parametros.get("emprego_total", dados.emprego_total or 0),
        "salarios_totais": parametros.get("salarios_totais", dados.salarios_totais or 0),
        "ret_retorno_local": parametros.get("ret_retorno_local", dados.ret_retorno_local or 0),
        "comp_competitividade": parametros.get("comp_competitividade", dados.comp_competitividade or 0),
        "sym_simbolismo": parametros.get("sym_simbolismo", dados.sym_simbolismo or 0),
        "yale_epi_score": parametros.get("yale_epi_score", dados.yale_epi_score or 0),
        "t_ultraprocessados": parametros.get("t_ultraprocessados", dados.t_ultraprocessados or 0),
        "u_agrotoxicos": parametros.get("u_agrotoxicos", dados.u_agrotoxicos or 0),
        "m_medicalizado": parametros.get("m_medicalizado", dados.m_medicalizado or 0),
        "i_inflamacao": parametros.get("i_inflamacao", dados.i_inflamacao or 0)
    }

    if tipo == "N_STAR":
        resultado = calcular_n_star(
            pop_base_mi=dados_completos["pop_base_mi"],
            pop_topo_mi=dados_completos["pop_topo_mi"],
            nascimentos_mi=dados_completos["nascimentos_mi"],
            mortes_mi=dados_completos["mortes_mi"],
            tfr_2024=dados_completos["tfr_2024"],
            tfr_1999=dados_completos["tfr_1999"]
        )
    elif tipo == "IES":
        # Primeiro calcular N*
        n_star_resultado = calcular_n_star(
            pop_base_mi=dados_completos["pop_base_mi"],
            pop_topo_mi=dados_completos["pop_topo_mi"],
            nascimentos_mi=dados_completos["nascimentos_mi"],
            mortes_mi=dados_completos["mortes_mi"],
            tfr_2024=dados_completos["tfr_2024"],
            tfr_1999=dados_completos["tfr_1999"]
        )

        resultado = calcular_ies_completo(
            ngii_puro=n_star_resultado["ngii_puro"],
            va_bruto=dados_completos["va_bruto"],
            emprego_total=dados_completos["emprego_total"],
            salarios_totais=dados_completos["salarios_totais"],
            ret_retorno_local=dados_completos["ret_retorno_local"],
            comp_competitividade=dados_completos["comp_competitividade"],
            sym_simbolismo=dados_completos["sym_simbolismo"],
            yale_epi_score=dados_completos["yale_epi_score"],
            t_ultraprocessados=dados_completos["t_ultraprocessados"],
            u_agrotoxicos=dados_completos["u_agrotoxicos"],
            m_medicalizado=dados_completos["m_medicalizado"],
            i_inflamacao=dados_completos["i_inflamacao"]
        )
    else:
        raise ValueError(f"Tipo de simulação inválido: {tipo}")

    return {
        "resultado": resultado,
        "dados_usados": dados_completos
    }


@router.post("", response_model=Simulacao, status_code=status.HTTP_201_CREATED)
async def criar_simulacao(
    simulacao: SimulacaoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Cria e executa uma nova simulação"""

    # Validar países
    pais_1 = db.query(Pais).filter(Pais.id == simulacao.pais_1_id).first()
    if not pais_1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="País 1 não encontrado"
        )

    if simulacao.pais_2_id:
        pais_2 = db.query(Pais).filter(Pais.id == simulacao.pais_2_id).first()
        if not pais_2:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="País 2 não encontrado"
            )

    # Executar cálculo país 1
    try:
        calc_1 = _executar_calculo(
            simulacao.tipo.value,
            simulacao.pais_1_id,
            simulacao.parametros_pais_1,
            db
        )
        resultado_1 = calc_1["resultado"]
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro no cálculo país 1: {str(e)}"
        )

    # Executar cálculo país 2 se fornecido
    resultado_2 = None
    if simulacao.pais_2_id and simulacao.parametros_pais_2:
        try:
            calc_2 = _executar_calculo(
                simulacao.tipo.value,
                simulacao.pais_2_id,
                simulacao.parametros_pais_2,
                db
            )
            resultado_2 = calc_2["resultado"]
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro no cálculo país 2: {str(e)}"
            )

    # Gerar análises
    dados_orig_1 = db.query(DadosBrutosPais).filter(
        DadosBrutosPais.pais_id == simulacao.pais_1_id
    ).order_by(DadosBrutosPais.data_coleta.desc()).first()

    analise_1 = analisar_cenario(
        pais_1.nome,
        simulacao.tipo.value,
        {
            "pop_base_mi": dados_orig_1.pop_base_mi,
            "pop_topo_mi": dados_orig_1.pop_topo_mi,
            "nascimentos_mi": dados_orig_1.nascimentos_mi,
            "mortes_mi": dados_orig_1.mortes_mi,
            "tfr_2024": dados_orig_1.tfr_2024,
            "tfr_1999": dados_orig_1.tfr_1999
        },
        simulacao.parametros_pais_1,
        resultado_1
    )

    analise_2 = None
    if resultado_2:
        dados_orig_2 = db.query(DadosBrutosPais).filter(
            DadosBrutosPais.pais_id == simulacao.pais_2_id
        ).order_by(DadosBrutosPais.data_coleta.desc()).first()

        analise_2 = analisar_cenario(
            pais_2.nome,
            simulacao.tipo.value,
            {
                "pop_base_mi": dados_orig_2.pop_base_mi,
                "pop_topo_mi": dados_orig_2.pop_topo_mi,
                "nascimentos_mi": dados_orig_2.nascimentos_mi,
                "mortes_mi": dados_orig_2.mortes_mi,
                "tfr_2024": dados_orig_2.tfr_2024,
                "tfr_1999": dados_orig_2.tfr_1999
            },
            simulacao.parametros_pais_2,
            resultado_2
        )

    # Salvar simulação
    nova_sim = SimulacaoCliente(
        usuario_id=current_user.id,
        tipo=simulacao.tipo,
        pais_1_id=simulacao.pais_1_id,
        pais_2_id=simulacao.pais_2_id,
        parametros_pais_1=simulacao.parametros_pais_1,
        parametros_pais_2=simulacao.parametros_pais_2,
        resultado_pais_1=resultado_1,
        resultado_pais_2=resultado_2,
        analise_agente_pais_1=analise_1,
        analise_agente_pais_2=analise_2
    )

    db.add(nova_sim)
    db.commit()
    db.refresh(nova_sim)

    return nova_sim


@router.get("/usuario", response_model=List[Simulacao])
async def listar_minhas_simulacoes(
    salvo_em_ficha: bool = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista todas as simulações do usuário autenticado"""

    query = db.query(SimulacaoCliente).filter(SimulacaoCliente.usuario_id == current_user.id)

    if salvo_em_ficha is not None:
        query = query.filter(SimulacaoCliente.salvo_em_ficha == salvo_em_ficha)

    return query.order_by(SimulacaoCliente.criado_em.desc()).all()


@router.get("/{simulacao_id}", response_model=Simulacao)
async def obter_simulacao(
    simulacao_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtém detalhes de uma simulação específica"""

    simulacao = db.query(SimulacaoCliente).filter(SimulacaoCliente.id == simulacao_id).first()

    if not simulacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Simulação não encontrada"
        )

    # Verificar se o usuário tem acesso (é dono ou ADMIN)
    if simulacao.usuario_id != current_user.id and current_user.tipo_usuario.value != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )

    return simulacao


@router.put("/{simulacao_id}", response_model=Simulacao)
async def atualizar_simulacao(
    simulacao_id: int,
    updates: SimulacaoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Atualiza parâmetros ou status de uma simulação"""

    simulacao = db.query(SimulacaoCliente).filter(SimulacaoCliente.id == simulacao_id).first()

    if not simulacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Simulação não encontrada"
        )

    if simulacao.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas o dono pode atualizar"
        )

    if updates.parametros_pais_1:
        simulacao.parametros_pais_1 = updates.parametros_pais_1

    if updates.parametros_pais_2:
        simulacao.parametros_pais_2 = updates.parametros_pais_2

    if updates.salvo_em_ficha is not None:
        simulacao.salvo_em_ficha = updates.salvo_em_ficha

    simulacao.versao += 1

    db.commit()
    db.refresh(simulacao)

    return simulacao


@router.delete("/{simulacao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_simulacao(
    simulacao_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Deleta uma simulação"""

    simulacao = db.query(SimulacaoCliente).filter(SimulacaoCliente.id == simulacao_id).first()

    if not simulacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Simulação não encontrada"
        )

    if simulacao.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas o dono pode deletar"
        )

    db.delete(simulacao)
    db.commit()

    return None
