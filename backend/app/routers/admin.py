from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

from ..database import get_db
from ..models import Usuario, Log
from .auth import get_current_user

load_dotenv()

router = APIRouter()


class UsuarioAprovacaoResponse(BaseModel):
    id: int
    email: str
    nome: str
    criado_em: str

    class Config:
        from_attributes = True


class ContatoRequest(BaseModel):
    nome: str
    email: EmailStr
    assunto: str
    mensagem: str


class LogResponse(BaseModel):
    id: int
    tipo: str
    mensagem: str
    criado_em: str

    class Config:
        from_attributes = True


def is_admin(usuario: Usuario = Depends(get_current_user)):
    if not usuario.is_admin:
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return usuario


def send_email(destinatario: str, assunto: str, corpo: str):
    try:
        EMAIL = os.getenv("EMAIL_ADMIN", "narayama.live@gmail.com")
        SENHA = os.getenv("EMAIL_PASSWORD", "")

        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = destinatario
        msg["Subject"] = assunto

        msg.attach(MIMEText(corpo, "html"))

        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL, SENHA)
        servidor.send_message(msg)
        servidor.quit()
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False


@router.get("/usuarios-pendentes", response_model=List[UsuarioAprovacaoResponse])
def usuarios_pendentes(admin: Usuario = Depends(is_admin), db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).filter(Usuario.aprovado == False).all()
    return usuarios


@router.get("/usuarios-aprovados", response_model=List[UsuarioAprovacaoResponse])
def usuarios_aprovados(admin: Usuario = Depends(is_admin), db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).filter(Usuario.aprovado == True).all()
    return usuarios


@router.post("/aprovar/{usuario_id}")
def aprovar_usuario(usuario_id: int, admin: Usuario = Depends(is_admin), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    usuario.aprovado = True
    db.commit()

    send_email(
        usuario.email,
        "AINU.SYSTEMS - Cadastro Aprovado",
        f"<h2>Bem-vindo ao AINU.SYSTEMS!</h2><p>Seu cadastro foi aprovado. Você pode fazer login em: https://narayama.live</p>"
    )

    db.add(Log(
        tipo="usuario_aprovado",
        mensagem=f"Usuário aprovado: {usuario.email}",
        usuario_id=admin.id
    ))
    db.commit()

    return {"message": "Usuário aprovado com sucesso"}


@router.post("/rejeitar/{usuario_id}")
def rejeitar_usuario(usuario_id: int, admin: Usuario = Depends(is_admin), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.delete(usuario)
    db.commit()

    send_email(
        usuario.email,
        "AINU.SYSTEMS - Cadastro Rejeitado",
        "<h2>Cadastro Não Aprovado</h2><p>Seu cadastro foi rejeitado. Entre em contato conosco para mais informações.</p>"
    )

    db.add(Log(
        tipo="usuario_rejeitado",
        mensagem=f"Usuário rejeitado: {usuario.email}",
        usuario_id=admin.id
    ))
    db.commit()

    return {"message": "Usuário rejeitado"}


@router.post("/contato/enviar")
def enviar_contato(contato: ContatoRequest, db: Session = Depends(get_db)):
    EMAIL_ADMIN = os.getenv("EMAIL_ADMIN", "narayama.live@gmail.com")

    corpo = f"""
    <h2>Nova Mensagem de Contato</h2>
    <p><strong>Nome:</strong> {contato.nome}</p>
    <p><strong>Email:</strong> {contato.email}</p>
    <p><strong>Assunto:</strong> {contato.assunto}</p>
    <p><strong>Mensagem:</strong></p>
    <p>{contato.mensagem}</p>
    """

    send_email(EMAIL_ADMIN, f"AINU.SYSTEMS - {contato.assunto}", corpo)

    db.add(Log(
        tipo="contato",
        mensagem=f"Contato recebido de {contato.email}: {contato.assunto}",
    ))
    db.commit()

    return {"message": "Mensagem enviada com sucesso"}


@router.get("/logs", response_model=List[LogResponse])
def get_logs(admin: Usuario = Depends(is_admin), db: Session = Depends(get_db)):
    logs = db.query(Log).order_by(Log.criado_em.desc()).limit(100).all()
    return logs
