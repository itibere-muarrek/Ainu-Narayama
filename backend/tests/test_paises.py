import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import Usuario, Pais, TipoUsuario, StatusUsuario
from app.security import hash_password

# Database de teste
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_paises.db"

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


@pytest.fixture
def admin_token():
    """Cria usuário admin e retorna token"""

    db = TestingSessionLocal()

    # Criar admin
    admin = Usuario(
        nome="Admin",
        email="admin@example.com",
        senha_hash=hash_password("admin123"),
        tipo_usuario=TipoUsuario.ADMIN,
        status=StatusUsuario.ATIVO
    )

    db.add(admin)
    db.commit()

    # Login e obter token
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@example.com",
            "senha": "admin123"
        }
    )

    token = response.json()["access_token"]
    db.close()

    return token


def test_criar_pais(admin_token):
    """Testa criação de país"""

    response = client.post(
        "/api/v1/paises",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "nome": "Brasil",
            "codigo_iso": "BRA",
            "regiao": "América Latina",
            "perfil_a": 30.0,
            "perfil_b": 25.0,
            "perfil_c": 20.0,
            "perfil_d": 15.0,
            "perfil_e": 10.0,
            "tfr_atual": 1.52,
            "tfr_25_anos_atras": 2.67,
            "identidade_sistematica": "BRA01"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Brasil"
    assert data["total_perfis"] == 100.0


def test_criar_pais_perfil_invalido(admin_token):
    """Testa erro ao criar país com perfis que não somam 100%"""

    response = client.post(
        "/api/v1/paises",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "nome": "Brasil",
            "codigo_iso": "BRA",
            "regiao": "América Latina",
            "perfil_a": 30.0,
            "perfil_b": 25.0,
            "perfil_c": 20.0,
            "perfil_d": 15.0,
            "perfil_e": 5.0  # Total = 95, não 100!
        }
    )

    assert response.status_code == 400
    assert "Soma dos perfis" in response.json()["detail"]


def test_listar_paises(admin_token):
    """Testa listagem de países"""

    # Criar país
    client.post(
        "/api/v1/paises",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "nome": "Brasil",
            "codigo_iso": "BRA",
            "regiao": "América Latina",
            "perfil_a": 30.0,
            "perfil_b": 25.0,
            "perfil_c": 20.0,
            "perfil_d": 15.0,
            "perfil_e": 10.0
        }
    )

    # Listar
    response = client.get(
        "/api/v1/paises",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["nome"] == "Brasil"


def test_obter_pais(admin_token):
    """Testa obtenção de detalhes de país"""

    # Criar
    create_response = client.post(
        "/api/v1/paises",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "nome": "Brasil",
            "codigo_iso": "BRA",
            "regiao": "América Latina",
            "perfil_a": 30.0,
            "perfil_b": 25.0,
            "perfil_c": 20.0,
            "perfil_d": 15.0,
            "perfil_e": 10.0
        }
    )

    pais_id = create_response.json()["id"]

    # Obter
    response = client.get(
        f"/api/v1/paises/{pais_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json()["nome"] == "Brasil"


def test_atualizar_pais(admin_token):
    """Testa atualização de país"""

    # Criar
    create_response = client.post(
        "/api/v1/paises",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "nome": "Brasil",
            "codigo_iso": "BRA",
            "regiao": "América Latina",
            "perfil_a": 30.0,
            "perfil_b": 25.0,
            "perfil_c": 20.0,
            "perfil_d": 15.0,
            "perfil_e": 10.0,
            "tfr_atual": 1.52
        }
    )

    pais_id = create_response.json()["id"]

    # Atualizar
    response = client.put(
        f"/api/v1/paises/{pais_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "nome": "Brasil",
            "codigo_iso": "BRA",
            "regiao": "América Latina",
            "perfil_a": 35.0,
            "perfil_b": 25.0,
            "perfil_c": 20.0,
            "perfil_d": 15.0,
            "perfil_e": 5.0,
            "tfr_atual": 1.45
        }
    )

    assert response.status_code == 200
    assert response.json()["perfil_a"] == 35.0
    assert response.json()["tfr_atual"] == 1.45


def test_deletar_pais(admin_token):
    """Testa exclusão de país"""

    # Criar
    create_response = client.post(
        "/api/v1/paises",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "nome": "Brasil",
            "codigo_iso": "BRA",
            "regiao": "América Latina",
            "perfil_a": 30.0,
            "perfil_b": 25.0,
            "perfil_c": 20.0,
            "perfil_d": 15.0,
            "perfil_e": 10.0
        }
    )

    pais_id = create_response.json()["id"]

    # Deletar
    response = client.delete(
        f"/api/v1/paises/{pais_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 204

    # Verificar se foi deletado
    get_response = client.get(
        f"/api/v1/paises/{pais_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert get_response.status_code == 404
