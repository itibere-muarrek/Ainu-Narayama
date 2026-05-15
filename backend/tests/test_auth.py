import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import Usuario, TipoUsuario, StatusUsuario
from app.security import hash_password

# Database de teste
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
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

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_register_usuario():
    """Testa registro de novo usuário"""

    response = client.post(
        "/api/v1/auth/register",
        json={
            "nome": "João Silva",
            "email": "joao@example.com",
            "senha": "senha123456",
            "mes_ano_nasc": "01/1990",
            "cidade": "São Paulo"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "joao@example.com"
    assert data["tipo_usuario"] == "VISITANTE"
    assert data["status"] == "NAO_APROVADO"


def test_register_email_duplicado():
    """Testa erro ao registrar com email duplicado"""

    # Primeiro registro
    client.post(
        "/api/v1/auth/register",
        json={
            "nome": "João Silva",
            "email": "joao@example.com",
            "senha": "senha123456"
        }
    )

    # Tentativa de duplicata
    response = client.post(
        "/api/v1/auth/register",
        json={
            "nome": "Outro João",
            "email": "joao@example.com",
            "senha": "outrasenha"
        }
    )

    assert response.status_code == 400
    assert "já cadastrado" in response.json()["detail"]


def test_login_sucesso():
    """Testa login bem-sucedido"""

    # Registrar usuário
    client.post(
        "/api/v1/auth/register",
        json={
            "nome": "João Silva",
            "email": "joao@example.com",
            "senha": "senha123456"
        }
    )

    # Fazer login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "joao@example.com",
            "senha": "senha123456"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_senha_incorreta():
    """Testa erro com senha incorreta"""

    # Registrar
    client.post(
        "/api/v1/auth/register",
        json={
            "nome": "João Silva",
            "email": "joao@example.com",
            "senha": "senha123456"
        }
    )

    # Login com senha errada
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "joao@example.com",
            "senha": "senhaerrada"
        }
    )

    assert response.status_code == 401


def test_refresh_token():
    """Testa renovação de token"""

    # Registrar e fazer login
    client.post(
        "/api/v1/auth/register",
        json={
            "nome": "João Silva",
            "email": "joao@example.com",
            "senha": "senha123456"
        }
    )

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "joao@example.com",
            "senha": "senha123456"
        }
    )

    refresh_token = login_response.json()["refresh_token"]

    # Renovar token
    response = client.post(
        "/api/v1/auth/refresh-token",
        json={"token": refresh_token}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
