from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from app.models import TipoUsuario, StatusUsuario, StatusN, Confiabilidade, Metodo, TipoSimulacao


# ===== USUARIO =====
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    mes_ano_nasc: Optional[str] = None
    instituicao: Optional[str] = None
    empresa: Optional[str] = None
    cidade: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=8)


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    mes_ano_nasc: Optional[str] = None
    instituicao: Optional[str] = None
    empresa: Optional[str] = None
    cidade: Optional[str] = None


class UsuarioAprovacao(BaseModel):
    status: StatusUsuario
    tipo_usuario: Optional[TipoUsuario] = None


class Usuario(UsuarioBase):
    id: int
    tipo_usuario: TipoUsuario
    status: StatusUsuario
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True


# ===== PAIS =====
class PaisBase(BaseModel):
    nome: str
    codigo_iso: str
    regiao: str
    identidade_sistematica: Optional[str] = None
    tfr_atual: Optional[float] = None
    tfr_25_anos_atras: Optional[float] = None
    ativo: bool = True


class PerfilUpdate(BaseModel):
    perfil_a: float = Field(..., ge=0, le=100)
    perfil_b: float = Field(..., ge=0, le=100)
    perfil_c: float = Field(..., ge=0, le=100)
    perfil_d: float = Field(..., ge=0, le=100)
    perfil_e: float = Field(..., ge=0, le=100)
    pop_prometidos: Optional[float] = None
    pop_estruturadores: Optional[float] = None
    pop_legatarios: Optional[float] = None


class PaisCreate(PaisBase):
    perfil_a: float = Field(default=0, ge=0, le=100)
    perfil_b: float = Field(default=0, ge=0, le=100)
    perfil_c: float = Field(default=0, ge=0, le=100)
    perfil_d: float = Field(default=0, ge=0, le=100)
    perfil_e: float = Field(default=0, ge=0, le=100)
    pop_prometidos: Optional[float] = None
    pop_estruturadores: Optional[float] = None
    pop_legatarios: Optional[float] = None


class Pais(PaisBase):
    id: int
    perfil_a: float
    perfil_b: float
    perfil_c: float
    perfil_d: float
    perfil_e: float
    total_perfis: float
    pop_prometidos: Optional[float]
    pop_estruturadores: Optional[float]
    pop_legatarios: Optional[float]
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True


# ===== DADOS BRUTOS =====
class DadosBrutosCreate(BaseModel):
    pais_id: int
    data_coleta: date
    pop_base_mi: Optional[float] = None
    pop_topo_mi: Optional[float] = None
    nascimentos_mi: Optional[float] = None
    mortes_mi: Optional[float] = None
    tfr_2024: Optional[float] = None
    tfr_1999: Optional[float] = None
    va_bruto: Optional[float] = None
    emprego_total: Optional[float] = None
    salarios_totais: Optional[float] = None
    yale_epi_score: Optional[float] = None
    t_ultraprocessados: Optional[float] = None
    u_agrotoxicos: Optional[float] = None
    m_medicalizado: Optional[float] = None
    i_inflamacao: Optional[float] = None
    ret_retorno_local: Optional[float] = None
    comp_competitividade: Optional[float] = None
    sym_simbolismo: Optional[float] = None
    confiabilidade: Optional[Confiabilidade] = Confiabilidade.MEDIA
    metodo: Optional[Metodo] = Metodo.ESTIMADO


class DadosBrutos(DadosBrutosCreate):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True


# ===== ÍNDICES CALCULADOS =====
class IndicesCalculadosCreate(BaseModel):
    pais_id: int
    ngii_bruto: Optional[float] = None
    ngii_puro: Optional[float] = None
    fator_geracional: Optional[float] = None
    n_estrela: Optional[float] = None
    status_n: Optional[StatusN] = None
    nih: Optional[float] = None
    l_glocalizado: Optional[float] = None
    a_ext_epi: Optional[float] = None
    ncii: Optional[float] = None
    nsii: Optional[float] = None
    ies: Optional[float] = None
    status_ies: Optional[str] = None
    analise_agente: Optional[str] = None


class IndicesCalculados(IndicesCalculadosCreate):
    id: int
    data_calculo: date
    criado_em: datetime

    class Config:
        from_attributes = True


# ===== SIMULAÇÕES =====
class SimulacaoCreate(BaseModel):
    tipo: TipoSimulacao
    pais_1_id: int
    pais_2_id: Optional[int] = None
    parametros_pais_1: Dict[str, Any]
    parametros_pais_2: Optional[Dict[str, Any]] = None


class SimulacaoUpdate(BaseModel):
    parametros_pais_1: Optional[Dict[str, Any]] = None
    parametros_pais_2: Optional[Dict[str, Any]] = None
    salvo_em_ficha: Optional[bool] = None


class Simulacao(BaseModel):
    id: int
    usuario_id: int
    tipo: TipoSimulacao
    pais_1_id: int
    pais_2_id: Optional[int]
    parametros_pais_1: Dict[str, Any]
    parametros_pais_2: Optional[Dict[str, Any]]
    resultado_pais_1: Dict[str, Any]
    resultado_pais_2: Optional[Dict[str, Any]]
    analise_agente_pais_1: Optional[str]
    analise_agente_pais_2: Optional[str]
    salvo_em_ficha: bool
    versao: int
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True


# ===== AUTENTICAÇÃO =====
class TokenData(BaseModel):
    sub: Optional[str] = None
    exp: Optional[datetime] = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


# ===== CÁLCULOS =====
class ParametrosCalculo(BaseModel):
    pais_id: int
    dados_override: Optional[Dict[str, Any]] = None


class ResultadoNStar(BaseModel):
    pais_id: int
    ngii_bruto: float
    ngii_puro: float
    fator_geracional: float
    n_estrela: float
    status_n: StatusN


class ResultadoIES(BaseModel):
    pais_id: int
    nih: float
    l_glocalizado: float
    a_ext_epi: float
    ncii: float
    nsii: float
    ies: float
    status_ies: str


# ===== LOG AUDITORIA =====
class LogAuditoriaCreate(BaseModel):
    acao: str
    tabela: str
    registro_id: Optional[int] = None
    antes: Optional[Dict[str, Any]] = None
    depois: Optional[Dict[str, Any]] = None


class LogAuditoria(LogAuditoriaCreate):
    id: int
    usuario_id: Optional[int]
    criado_em: datetime

    class Config:
        from_attributes = True
