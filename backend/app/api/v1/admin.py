from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database import get_db
from app.models import Usuario, LogAuditoria, TipoUsuario, StatusUsuario
from app.schemas import Usuario as UsuarioSchema, UsuarioAprovacao, LogAuditoria as LogSchema
from app.security import get_current_admin
from agente.scheduler import tarefa_coleta_semanal
import asyncio

router = APIRouter(prefix="/admin", tags=["administração"])


@router.get("/usuarios", response_model=List[UsuarioSchema])
async def listar_usuarios(
    status: StatusUsuario = None,
    tipo: TipoUsuario = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)
):
    """Lista todos os usuários (ADMIN only)"""

    query = db.query(Usuario)

    if status:
        query = query.filter(Usuario.status == status)

    if tipo:
        query = query.filter(Usuario.tipo_usuario == tipo)

    return query.all()


@router.put("/usuarios/{usuario_id}", response_model=UsuarioSchema)
async def atualizar_usuario(
    usuario_id: int,
    aprovacao: UsuarioAprovacao,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)
):
    """Aprova, rejeita ou promove um usuário (ADMIN only)"""

    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    # Não permitir editar a si mesmo
    if usuario.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não pode editar a si mesmo"
        )

    usuario.status = aprovacao.status

    if aprovacao.tipo_usuario:
        usuario.tipo_usuario = aprovacao.tipo_usuario

    # Log de auditoria
    log = LogAuditoria(
        usuario_id=current_user.id,
        acao=f"ATUALIZOU_USUARIO_STATUS_{aprovacao.status.value}",
        tabela="usuarios",
        registro_id=usuario.id,
        depois={
            "status": usuario.status.value,
            "tipo_usuario": usuario.tipo_usuario.value
        }
    )

    db.add(log)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario


@router.get("/logs", response_model=List[LogSchema])
async def listar_logs(
    usuario_id: int = None,
    acao: str = None,
    tabela: str = None,
    limite: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)
):
    """Lista logs de auditoria com filtros (ADMIN only)"""

    query = db.query(LogAuditoria)

    if usuario_id:
        query = query.filter(LogAuditoria.usuario_id == usuario_id)

    if acao:
        query = query.filter(LogAuditoria.acao.contains(acao))

    if tabela:
        query = query.filter(LogAuditoria.tabela == tabela)

    return query.order_by(LogAuditoria.criado_em.desc()).limit(limite).all()


@router.get("/logs/{log_id}", response_model=LogSchema)
async def obter_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)
):
    """Obtém detalhes de um log específico"""

    log = db.query(LogAuditoria).filter(LogAuditoria.id == log_id).first()

    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log não encontrado"
        )

    return log


@router.get("/estatisticas", response_model=Dict[str, Any])
async def obter_estatisticas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)
):
    """Retorna estatísticas do sistema (ADMIN only)"""

    total_usuarios = db.query(Usuario).count()
    usuarios_ativos = db.query(Usuario).filter(Usuario.status == StatusUsuario.ATIVO).count()
    usuarios_pendentes = db.query(Usuario).filter(Usuario.status == StatusUsuario.NAO_APROVADO).count()
    total_logs = db.query(LogAuditoria).count()

    return {
        "total_usuarios": total_usuarios,
        "usuarios_ativos": usuarios_ativos,
        "usuarios_pendentes": usuarios_pendentes,
        "usuarios_rejeitados": total_usuarios - usuarios_ativos - usuarios_pendentes,
        "total_logs_auditoria": total_logs,
        "admins": db.query(Usuario).filter(Usuario.tipo_usuario == TipoUsuario.ADMIN).count(),
        "co_admins": db.query(Usuario).filter(Usuario.tipo_usuario == TipoUsuario.CO_ADMIN).count()
    }


@router.post("/coleta-manual", response_model=Dict[str, Any])
async def disparar_coleta_manual(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)
):
    """
    Dispara manualmente a coleta semanal (ADMIN only).

    Útil para testes e coletas fora do agendamento automático.
    """

    try:
        # Log de auditoria
        log = LogAuditoria(
            usuario_id=current_user.id,
            acao="COLETA_MANUAL_DISPARADA",
            tabela="agente",
            registro_id=0,
            depois={"timestamp": "trigger manual"}
        )
        db.add(log)
        db.commit()

        # Dispara coleta em background
        asyncio.create_task(tarefa_coleta_semanal())

        return {
            "status": "coleta iniciada",
            "mensagem": "Coleta semanal manual disparada com sucesso",
            "usuario_id": current_user.id,
            "timestamp": str(__import__("datetime").datetime.now())
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao disparar coleta: {str(e)}"
        )
