from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nome = Column(String(255), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    aprovado = Column(Boolean, default=False)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class IndiceCalculado(Base):
    __tablename__ = "indices_calculados"

    id = Column(Integer, primary_key=True, index=True)
    pais_id = Column(Integer, nullable=False)
    pais_nome = Column(String(255), nullable=False)
    n_star = Column(Float, nullable=False)
    status_n = Column(String(50), nullable=False)
    nih = Column(Float, nullable=False)
    nsii = Column(Float, nullable=False)
    ies = Column(Float, nullable=False)
    status_ies = Column(String(50), nullable=False)
    tfr_atual = Column(Float, nullable=False)
    tfr_1999 = Column(Float, nullable=False)

    # Testes de validação
    teste_trr = Column(Boolean, default=True)
    teste_tsp = Column(Boolean, default=True)
    teste_tce = Column(Boolean, default=True)
    teste_tcd = Column(Boolean, default=True)

    calculado_em = Column(DateTime, default=datetime.utcnow)


class Simulacao(Base):
    __tablename__ = "simulacoes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)
    tipo = Column(String(50), nullable=False)  # "n_star" ou "ies"
    pais_id = Column(Integer, nullable=False)
    pais_nome = Column(String(255), nullable=False)

    # Valores originais
    valor_original = Column(Float, nullable=False)
    status_original = Column(String(50), nullable=False)

    # Valores simulados
    parametros = Column(Text, nullable=False)  # JSON string
    valor_simulado = Column(Float, nullable=False)
    status_simulado = Column(String(50), nullable=False)

    criado_em = Column(DateTime, default=datetime.utcnow)


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False)
    mensagem = Column(Text, nullable=False)
    usuario_id = Column(Integer, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
