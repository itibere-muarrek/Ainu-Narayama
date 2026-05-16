from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

from ..database import get_db
from ..models import Usuario, Log

load_dotenv()

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-secreta-muito-segura-32-caracteres-minimo")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", 24))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData(BaseModel):
    email: str


class UsuarioRegistro(BaseModel):
    nome: str
    email: EmailStr
    senha: str


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str


class UsuarioResponse(BaseModel):
    id: int
    email: str
    nome: str
    is_admin: bool
    aprovado: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    usuario: UsuarioResponse


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    usuario = db.query(Usuario).filter(Usuario.email == token_data.email).first()
    if usuario is None:
        raise credentials_exception
    return usuario


@router.post("/registrar", response_model=UsuarioResponse)
def registrar(usuario_data: UsuarioRegistro, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario_data.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já registrado")

    novo_usuario = Usuario(
        email=usuario_data.email,
        nome=usuario_data.nome,
        senha_hash=get_password_hash(usuario_data.senha),
        is_admin=False,
        aprovado=False,
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    db.add(Log(
        tipo="usuario_registrado",
        mensagem=f"Novo usuário registrado: {usuario_data.email}",
        usuario_id=novo_usuario.id
    ))
    db.commit()

    return novo_usuario


@router.post("/login", response_model=Token)
def login(usuario_login: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == usuario_login.email).first()

    if not usuario or not verify_password(usuario_login.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )

    if not usuario.aprovado:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário aguardando aprovação do administrador"
        )

    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": usuario.email},
        expires_delta=access_token_expires
    )

    db.add(Log(
        tipo="login",
        mensagem=f"Login realizado: {usuario_login.email}",
        usuario_id=usuario.id
    ))
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": usuario
    }


@router.get("/me", response_model=UsuarioResponse)
def get_me(token: str, db: Session = Depends(get_db)):
    usuario = get_current_user(token, db)
    return usuario
