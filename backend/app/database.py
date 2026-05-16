from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv

load_dotenv()

# Tentar DATABASE_URL primeiro
DATABASE_URL = os.getenv("DATABASE_URL")

# Se não houver DATABASE_URL, tentar construir a partir de variáveis de serviço (Railway)
if not DATABASE_URL:
    pg_host = os.getenv("PGHOST")
    pg_port = os.getenv("PGPORT", "5432")
    pg_user = os.getenv("PGUSER")
    pg_password = os.getenv("PGPASSWORD")
    pg_database = os.getenv("PGDATABASE")

    if all([pg_host, pg_user, pg_password, pg_database]):
        DATABASE_URL = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"

# Fallback para SQLite se nenhuma configuração de PostgreSQL foi encontrada
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./test.db"

if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(DATABASE_URL, echo=False)
else:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from .models import Base
    Base.metadata.create_all(bind=engine)
