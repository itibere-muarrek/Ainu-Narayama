from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.models import Usuario, TipoUsuario, StatusUsuario
from app.schemas import UsuarioCreate, Usuario as UsuarioSchema, LoginRequest, Token
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user,
    verify_token
)
from app.config import get_settings

router = APIRouter(prefix="/auth", tags=["autenticacao"])
settings = get_settings()


@router.post("/register", response_model=UsuarioSchema, status_code=status.HTTP_201_CREATED)
async def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra um novo usuário"""

    # Verificar se email já existe
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )

    # Criar novo usuário
    hash_senha = hash_password(usuario.senha)
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=hash_senha,
        mes_ano_nasc=usuario.mes_ano_nasc,
        instituicao=usuario.instituicao,
        empresa=usuario.empresa,
        cidade=usuario.cidade,
        tipo_usuario=TipoUsuario.VISITANTE,
        status=StatusUsuario.NAO_APROVADO
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


@router.post("/login", response_model=Token)
async def login(credenciais: LoginRequest, db: Session = Depends(get_db)):
    """Autentica usuário e retorna tokens"""

    # Buscar usuário
    usuario = db.query(Usuario).filter(Usuario.email == credenciais.email).first()
    if not usuario or not verify_password(credenciais.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Gerar tokens
    access_token = create_access_token(data={"sub": usuario.email})
    refresh_token = create_refresh_token(data={"sub": usuario.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh-token", response_model=Token)
async def refresh_token(token: str, db: Session = Depends(get_db)):
    """Renova o access token usando refresh token"""

    email = verify_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar se usuário existe
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    # Gerar novo access token
    new_access_token = create_access_token(data={"sub": usuario.email})

    return {
        "access_token": new_access_token,
        "refresh_token": token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(current_user: Usuario = Depends(get_current_user)):
    """Logout (client-side removal de tokens)"""
    return {"message": "Logout realizado com sucesso"}


@router.get("/me", response_model=UsuarioSchema)
async def get_me(current_user: Usuario = Depends(get_current_user)):
    """Retorna dados do usuário autenticado"""
    return current_user
