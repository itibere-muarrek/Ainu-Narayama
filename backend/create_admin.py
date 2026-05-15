import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Usuario, TipoUsuario, StatusUsuario
from app.security import hash_password
from app.config import get_settings

settings = get_settings()
engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()

# Verificar se admin já existe
admin_existente = db.query(Usuario).filter(Usuario.email == "imuarrek@admin.com").first()
if admin_existente:
    print("Admin já existe!")
    db.close()
    exit()

# Criar admin
admin = Usuario(
    nome="I Muarrek",
    email="imuarrek@admin.com",
    senha_hash=hash_password("Nara2051@@"),
    tipo_usuario=TipoUsuario.ADMIN,
    status=StatusUsuario.ATIVO
)

db.add(admin)
db.commit()
print("✅ Admin criado com sucesso!")
print(f"Email: imuarrek@admin.com")
print(f"Senha: Nara2051@@")
db.close()
