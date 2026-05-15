from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey, Enum, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum
from datetime import datetime


class TipoUsuario(str, enum.Enum):
    VISITANTE = "VISITANTE"
    CO_ADMIN = "CO-ADMIN"
    ADMIN = "ADMIN"


class StatusUsuario(str, enum.Enum):
    NAO_APROVADO = "NAO_APROVADO"
    ATIVO = "ATIVO"
    REJEITADO = "REJEITADO"


class StatusN(str, enum.Enum):
    PROMISSOR = "PROMISSOR"
    EQUILIBRIO = "EQUILIBRIO"
    CRITICO = "CRITICO"
    COLAPSO = "COLAPSO"


class Confiabilidade(str, enum.Enum):
    ALTA = "Alta"
    MEDIA = "Media"
    BAIXA = "Baixa"


class Metodo(str, enum.Enum):
    COLETADO = "COLETADO"
    CALIBRADO = "CALIBRADO"
    ESTIMADO = "ESTIMADO"


class TipoSimulacao(str, enum.Enum):
    N_STAR = "N_STAR"
    IES = "IES"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha_hash = Column(String, nullable=False)
    mes_ano_nasc = Column(String, nullable=True)  # MM/YYYY
    tipo_usuario = Column(Enum(TipoUsuario), default=TipoUsuario.VISITANTE)
    status = Column(Enum(StatusUsuario), default=StatusUsuario.NAO_APROVADO)
    instituicao = Column(String, nullable=True)
    empresa = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    criado_em = Column(DateTime, server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    simulacoes = relationship("SimulacaoCliente", back_populates="usuario")
    logs_auditoria = relationship("LogAuditoria", back_populates="usuario")


class Pais(Base):
    __tablename__ = "paises"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False, index=True)
    codigo_iso = Column(String(3), unique=True, nullable=False, index=True)
    regiao = Column(String, nullable=False)
    perfil = Column(String, nullable=True)  # ex: B30-C40-D30
    perfil_a = Column(Float, default=0.0)
    perfil_b = Column(Float, default=0.0)
    perfil_c = Column(Float, default=0.0)
    perfil_d = Column(Float, default=0.0)
    perfil_e = Column(Float, default=0.0)
    total_perfis = Column(Float, default=100.0)
    pop_prometidos = Column(Float, default=0.0)  # %
    pop_estruturadores = Column(Float, default=0.0)  # %
    pop_legatarios = Column(Float, default=0.0)  # %
    tfr_atual = Column(Float, nullable=True)
    tfr_25_anos_atras = Column(Float, nullable=True)
    identidade_sistematica = Column(String, unique=True, nullable=True)  # ex: PCD55
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    dados_brutos = relationship("DadosBrutosPais", back_populates="pais")
    indices = relationship("IndicesCalculados", back_populates="pais")


class DadosBrutosPais(Base):
    __tablename__ = "dados_brutos_paises"

    id = Column(Integer, primary_key=True, index=True)
    pais_id = Column(Integer, ForeignKey("paises.id"), nullable=False, index=True)
    data_coleta = Column(Date, nullable=False)
    pop_base_mi = Column(Float, nullable=True)  # Milhões
    pop_topo_mi = Column(Float, nullable=True)  # Milhões
    nascimentos_mi = Column(Float, nullable=True)  # Milhões
    mortes_mi = Column(Float, nullable=True)  # Milhões
    tfr_2024 = Column(Float, nullable=True)
    tfr_1999 = Column(Float, nullable=True)
    va_bruto = Column(Float, nullable=True)
    emprego_total = Column(Float, nullable=True)
    salarios_totais = Column(Float, nullable=True)
    yale_epi_score = Column(Float, nullable=True)
    t_ultraprocessados = Column(Float, nullable=True)  # %
    u_agrotoxicos = Column(Float, nullable=True)  # %
    m_medicalizado = Column(Float, nullable=True)  # %
    i_inflamacao = Column(Float, nullable=True)  # %
    ret_retorno_local = Column(Float, nullable=True)
    comp_competitividade = Column(Float, nullable=True)
    sym_simbolismo = Column(Float, nullable=True)
    confiabilidade = Column(Enum(Confiabilidade), default=Confiabilidade.MEDIA)
    necessita_atualizacao = Column(Boolean, default=False)
    metodo = Column(Enum(Metodo), default=Metodo.ESTIMADO)
    criado_em = Column(DateTime, server_default=func.now(), nullable=False)

    pais = relationship("Pais", back_populates="dados_brutos")


class IndicesCalculados(Base):
    __tablename__ = "indices_calculados"

    id = Column(Integer, primary_key=True, index=True)
    pais_id = Column(Integer, ForeignKey("paises.id"), nullable=False, index=True)
    data_calculo = Column(Date, nullable=False)
    ngii_bruto = Column(Float, nullable=True)
    ngii_puro = Column(Float, nullable=True)
    fator_geracional = Column(Float, nullable=True)
    n_estrela = Column(Float, nullable=True)
    status_n = Column(Enum(StatusN), nullable=True)
    nih = Column(Float, nullable=True)
    l_glocalizado = Column(Float, nullable=True)
    a_ext_epi = Column(Float, nullable=True)
    ncii = Column(Float, nullable=True)
    nsii = Column(Float, nullable=True)
    ies = Column(Float, nullable=True)
    status_ies = Column(String, nullable=True)
    analise_agente = Column(Text, nullable=True)
    criado_em = Column(DateTime, server_default=func.now(), nullable=False)

    pais = relationship("Pais", back_populates="indices")


class SimulacaoCliente(Base):
    __tablename__ = "simulacoes_clientes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    tipo = Column(Enum(TipoSimulacao), nullable=False)
    pais_1_id = Column(Integer, ForeignKey("paises.id"), nullable=False)
    pais_2_id = Column(Integer, ForeignKey("paises.id"), nullable=True)
    parametros_pais_1 = Column(JSON, nullable=False)  # variáveis modificadas
    parametros_pais_2 = Column(JSON, nullable=True)
    resultado_pais_1 = Column(JSON, nullable=False)  # resultado final
    resultado_pais_2 = Column(JSON, nullable=True)
    analise_agente_pais_1 = Column(Text, nullable=True)
    analise_agente_pais_2 = Column(Text, nullable=True)
    salvo_em_ficha = Column(Boolean, default=False)
    versao = Column(Integer, default=1)
    criado_em = Column(DateTime, server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    usuario = relationship("Usuario", back_populates="simulacoes")


class LogAuditoria(Base):
    __tablename__ = "log_auditoria"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    acao = Column(String, nullable=False)  # ex: EDITOU_PAIS, BAIXOU_SIMULACAO
    tabela = Column(String, nullable=False)
    registro_id = Column(Integer, nullable=True)
    antes = Column(JSON, nullable=True)
    depois = Column(JSON, nullable=True)
    criado_em = Column(DateTime, server_default=func.now(), nullable=False)

    usuario = relationship("Usuario", back_populates="logs_auditoria")
