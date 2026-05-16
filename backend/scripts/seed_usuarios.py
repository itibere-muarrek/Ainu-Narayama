import sys
import os
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))

from app.database import SessionLocal, init_db
from app.models import Usuario
from app.routers.auth import get_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_usuarios():
    init_db()
    db = SessionLocal()

    usuarios_padrao = [
        {
            "email": "imuarrek@gmail.com",
            "nome": "Admin AINU",
            "senha": "Nara2026!",
            "is_admin": True,
            "aprovado": True,
        },
        {
            "email": "VISITOR1",
            "nome": "Visitante 1",
            "senha": "Vis123",
            "is_admin": False,
            "aprovado": True,
        },
        {
            "email": "VISITOR2",
            "nome": "Visitante 2",
            "senha": "Vis456",
            "is_admin": False,
            "aprovado": True,
        },
    ]

    for user_data in usuarios_padrao:
        usuario_existente = db.query(Usuario).filter(
            Usuario.email == user_data["email"]
        ).first()

        if not usuario_existente:
            novo_usuario = Usuario(
                email=user_data["email"],
                nome=user_data["nome"],
                senha_hash=get_password_hash(user_data["senha"]),
                is_admin=user_data["is_admin"],
                aprovado=user_data["aprovado"],
            )
            db.add(novo_usuario)
            logger.info(f"✓ Usuário criado: {user_data['email']}")
        else:
            logger.info(f"✓ Usuário já existe: {user_data['email']}")

    db.commit()
    db.close()
    logger.info("\n✅ Seed de usuários concluído!")


if __name__ == "__main__":
    seed_usuarios()
