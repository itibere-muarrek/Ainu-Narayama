import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import Usuario, TipoUsuario, StatusUsuario
from app.security import hash_password

# Database URL para testes (SQLite em memória)
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db():
    """Cria um banco de dados limpo para cada teste"""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    """Cliente HTTP para testes"""
    from fastapi.testclient import TestClient
    return TestClient(app)


@pytest.fixture(scope="function")
def usuario_admin_db(db):
    """Cria um usuário admin no BD de teste"""
    admin = Usuario(
        nome="Admin Teste",
        email="admin@test.com",
        senha_hash=hash_password("admin123"),
        tipo_usuario=TipoUsuario.ADMIN,
        status=StatusUsuario.ATIVO
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


@pytest.fixture(scope="function")
def usuario_comum_db(db):
    """Cria um usuário comum (visitante) no BD de teste"""
    usuario = Usuario(
        nome="Usuário Teste",
        email="usuario@test.com",
        senha_hash=hash_password("usuario123"),
        tipo_usuario=TipoUsuario.VISITANTE,
        status=StatusUsuario.NAO_APROVADO
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@pytest.fixture(scope="function")
def usuario_admin_ativo_db(db):
    """Cria um usuário admin ATIVO no BD de teste"""
    admin = Usuario(
        nome="Admin Ativo",
        email="admin_ativo@test.com",
        senha_hash=hash_password("admin123"),
        tipo_usuario=TipoUsuario.ADMIN,
        status=StatusUsuario.ATIVO
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin
