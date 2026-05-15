from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from app.config import get_settings
from app.models import Usuario
from app.database import get_db
from sqlalchemy.orm import Session

settings = get_settings()

# Contexto para hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de segurança
security = HTTPBearer()


def hash_password(password: str) -> str:
    """Criptografa a senha usando bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha coincide com o hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria um JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Cria um JWT refresh token com expiração de 7 dias"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """Verifica e decodifica um JWT token, retorna o email do usuário"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """Dependência para obter o usuário autenticado a partir do token"""
    token = credentials.credentials
    email = verify_token(token)

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return usuario


async def get_current_admin(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """Dependência para verificar se o usuário é ADMIN"""
    from app.models import TipoUsuario

    if current_user.tipo_usuario != TipoUsuario.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a ADMIN"
        )
    return current_user


async def get_current_co_admin_or_admin(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """Dependência para verificar se o usuário é CO-ADMIN ou ADMIN"""
    from app.models import TipoUsuario

    if current_user.tipo_usuario not in [TipoUsuario.CO_ADMIN, TipoUsuario.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a CO-ADMIN e ADMIN"
        )
    return current_user


async def get_current_active_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """Dependência para verificar se o usuário está ativo (aprovado)"""
    from app.models import StatusUsuario

    if current_user.status != StatusUsuario.ATIVO:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não aprovado ou rejeitado"
        )
    return current_user
