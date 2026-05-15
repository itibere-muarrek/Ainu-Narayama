from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Pais, Usuario
from app.schemas import Pais as PaisSchema, PaisCreate, PerfilUpdate
from app.security import get_current_user, get_current_co_admin_or_admin, get_current_admin

router = APIRouter(prefix="/paises", tags=["países"])


@router.get("", response_model=List[PaisSchema])
async def listar_paises(
    ativo: bool = True,
    regiao: str = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista todos os países (filtros opcionais)"""

    query = db.query(Pais)

    if ativo is not None:
        query = query.filter(Pais.ativo == ativo)

    if regiao:
        query = query.filter(Pais.regiao == regiao)

    return query.all()


@router.get("/{pais_id}", response_model=PaisSchema)
async def obter_pais(
    pais_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtém detalhes de um país específico"""

    pais = db.query(Pais).filter(Pais.id == pais_id).first()
    if not pais:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="País não encontrado"
        )

    return pais


@router.post("", response_model=PaisSchema, status_code=status.HTTP_201_CREATED)
async def criar_pais(
    pais: PaisCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)
):
    """Cria um novo país (ADMIN only)"""

    # Validar perfis (soma deve ser 100)
    soma_perfis = pais.perfil_a + pais.perfil_b + pais.perfil_c + pais.perfil_d + pais.perfil_e
    if abs(soma_perfis - 100) > 0.01:  # tolerância de 0.01%
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Soma dos perfis deve ser 100. Atual: {soma_perfis}"
        )

    # Verificar duplicatas
    if db.query(Pais).filter(Pais.nome == pais.nome).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="País com este nome já existe"
        )

    if db.query(Pais).filter(Pais.codigo_iso == pais.codigo_iso).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="País com este código ISO já existe"
        )

    if pais.identidade_sistematica:
        if db.query(Pais).filter(Pais.identidade_sistematica == pais.identidade_sistematica).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Identidade Sistêmica duplicada"
            )

    # Criar país
    novo_pais = Pais(**pais.model_dump())
    novo_pais.total_perfis = soma_perfis

    db.add(novo_pais)
    db.commit()
    db.refresh(novo_pais)

    return novo_pais


@router.put("/{pais_id}", response_model=PaisSchema)
async def atualizar_pais(
    pais_id: int,
    pais_update: PaisCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)
):
    """Atualiza dados de um país (ADMIN only)"""

    db_pais = db.query(Pais).filter(Pais.id == pais_id).first()
    if not db_pais:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="País não encontrado"
        )

    # Validar perfis
    soma_perfis = (
        pais_update.perfil_a + pais_update.perfil_b +
        pais_update.perfil_c + pais_update.perfil_d + pais_update.perfil_e
    )
    if abs(soma_perfis - 100) > 0.01:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Soma dos perfis deve ser 100. Atual: {soma_perfis}"
        )

    # Atualizar campos
    for campo, valor in pais_update.model_dump(exclude_unset=True).items():
        setattr(db_pais, campo, valor)

    db_pais.total_perfis = soma_perfis

    db.commit()
    db.refresh(db_pais)

    return db_pais


@router.put("/{pais_id}/perfil", response_model=PaisSchema)
async def atualizar_perfil(
    pais_id: int,
    perfil: PerfilUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_co_admin_or_admin)
):
    """Atualiza apenas os perfis A-E de um país (CO-ADMIN e ADMIN)"""

    db_pais = db.query(Pais).filter(Pais.id == pais_id).first()
    if not db_pais:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="País não encontrado"
        )

    # Validar soma = 100%
    soma = perfil.perfil_a + perfil.perfil_b + perfil.perfil_c + perfil.perfil_d + perfil.perfil_e
    if abs(soma - 100) > 0.01:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Soma dos perfis deve ser 100. Atual: {soma}"
        )

    # Atualizar
    db_pais.perfil_a = perfil.perfil_a
    db_pais.perfil_b = perfil.perfil_b
    db_pais.perfil_c = perfil.perfil_c
    db_pais.perfil_d = perfil.perfil_d
    db_pais.perfil_e = perfil.perfil_e
    db_pais.total_perfis = soma

    if perfil.pop_prometidos is not None:
        db_pais.pop_prometidos = perfil.pop_prometidos
    if perfil.pop_estruturadores is not None:
        db_pais.pop_estruturadores = perfil.pop_estruturadores
    if perfil.pop_legatarios is not None:
        db_pais.pop_legatarios = perfil.pop_legatarios

    db.commit()
    db.refresh(db_pais)

    return db_pais


@router.delete("/{pais_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_pais(
    pais_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)
):
    """Deleta um país (ADMIN only)"""

    db_pais = db.query(Pais).filter(Pais.id == pais_id).first()
    if not db_pais:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="País não encontrado"
        )

    db.delete(db_pais)
    db.commit()

    return None
