"""
Configurações centrais do projeto AINU-Narayama.

Contém o cadastro dos 28 países cobertos pela tese v8.0 (Anexo 5),
os limiares críticos do Índice de Narayama Sistêmico (N*) e os
caminhos padrão de dados usados pelo restante do pipeline.

Fonte: V1_EcoPol_062426_v8.0.docx (tese de doutorado, Cap. 3, V.III,
Capítulo 5, Anexo 5, Anexo 8, Tabela 4, Tabela 14).
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Caminhos de diretórios
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"
DOCS_DIR = BASE_DIR / "docs"

PATHS = {
    "DIR_DATA_RAW": str(DATA_RAW_DIR),
    "DIR_DATA_PROCESSED": str(DATA_PROCESSED_DIR),
    "DIR_DOCS": str(DOCS_DIR),
    "DIR_NOTEBOOKS": str(BASE_DIR / "notebooks"),
    "FILE_PAISES_PERFIL": str(DOCS_DIR / "paises_perfil.csv"),
    "FILE_DEFINITIONS": str(DOCS_DIR / "definitions.md"),
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

LOGGING_CONFIG = {
    "LOG_LEVEL": "INFO",
    "LOG_FILE": "ainu.log",
    "LOG_FORMAT": "%(asctime)s - %(levelname)s - %(message)s",
}

# ---------------------------------------------------------------------------
# Limiares críticos do N* (Índice de Narayama Sistêmico)
# ---------------------------------------------------------------------------
# A tese contém duas convenções de escala para o N* que não foram
# reconciliadas entre si (ver docs/definitions.md, seção "Nota sobre
# inconsistência interna da tese"). Este projeto adota a convenção da
# Tabela 4 / Anexo 8 ("nova fórmula"), na qual N* alto = melhor.
#
# PEEC (Ponto de Esgotamento por Excesso de Contingente) NÃO é um
# limiar de N_Base nesta convenção: é uma condição diagnosticada
# diretamente pela TFR (Cap. 3.2.1), sinalizada quando TFR > 2,8.
# Por isso fica fora de ZONAS_CRITICAS/LIMIARES_SIMPLES (que são
# limiares de N*) e é tratado à parte, como LIMIAR_PEEC_TFR.

ZONAS_CRITICAS = {
    "expansao_forte": {"min": 1.10, "max": float("inf")},
    "equilibrio_sustentavel": {"min": 0.80, "max": 1.10},  # também chamado PEA
    "tensao_acelerada": {"min": 0.50, "max": 0.80},
    "colapso_narayama": {"min": float("-inf"), "max": 0.50},  # também chamado PEC
}

LIMIARES_SIMPLES = {
    "expansao_forte": 1.10,
    "pea": 0.80,  # Ponto de Equilíbrio Absoluto (limite inferior da zona)
    "pec": 0.50,  # Ponto de Entropia Crônica (limite inferior da zona)
}

LIMIAR_PEEC_TFR = 2.8  # diagnosticado por TFR, não por N*

# Constantes equivalentes a LIMIARES_SIMPLES, mantidas porque
# src/indices.py e src/falseability.py já as importam por nome.
LIMIAR_EXPANSAO_FORTE = LIMIARES_SIMPLES["expansao_forte"]
LIMIAR_PEA_INFERIOR = LIMIARES_SIMPLES["pea"]
LIMIAR_TENSAO_INFERIOR = LIMIARES_SIMPLES["pec"]

# ---------------------------------------------------------------------------
# Farol do Fator_Alocativo (Seção V.III-bis)
# ---------------------------------------------------------------------------

FATOR_ALOCATIVO_LIMIARES = {
    "superior": 1.05,  # Farol + (prioridade ao futuro)
    "inferior": 0.95,  # Farol - (gerontocracia); entre os dois: Farol n
}

FAROL_INTERPRETACAO = {
    "positivo": "+",  # Fator_Alocativo > 1.05: investe mais no futuro
    "neutro": "n",  # 0.95 <= Fator_Alocativo <= 1.05: equilíbrio
    "negativo": "-",  # Fator_Alocativo < 0.95: investe mais nos idosos
}

# Constantes equivalentes a FATOR_ALOCATIVO_LIMIARES, mantidas porque
# src/indices.py e src/falseability.py já as importam por nome.
FATOR_ALOCATIVO_SUPERIOR = FATOR_ALOCATIVO_LIMIARES["superior"]
FATOR_ALOCATIVO_INFERIOR = FATOR_ALOCATIVO_LIMIARES["inferior"]

# ---------------------------------------------------------------------------
# Fórmulas (Capítulo 5 — NGII_puro com 3 componentes)
# ---------------------------------------------------------------------------

FORMULAS = {
    "ngii_puro": (
        "NGII_puro = (Pop_Base / Pop_Topo) x (Nascimentos / Mortes) "
        "x (Taxa_Escolaridade_0-25 / Taxa_Esperada)"
    ),
    "componente_1": "Razao Geracional = Pop_Base / Pop_Topo (0-25 / 25-65)",
    "componente_2": "Vitalidade = Nascimentos / Mortes",
    "componente_3": "Educacao = Taxa_Escolaridade_0-25 / Taxa_Esperada",
    "fator_geracional": "Fator_Geracional = TFR_atual / TFR_25_anos_atras",
    "n_base": "N* = N_Base = NGII_puro x Fator_Geracional",
    "fator_alocativo": "Fator_Alocativo = NTA(0-25) / NTA(65+)",
    "nota": (
        "Pop_Base e Pop_Topo sao faixas etarias, nao geracoes. "
        "Pop_Topo = provedores atuais (25-65), nao idosos (55+/65+). "
        "Fixo para todos os perfis (Capitulo 5), sem variacao por perfil."
    ),
}

# ---------------------------------------------------------------------------
# Faixas etárias por Perfil Estrutural (Tabela 14)
# ---------------------------------------------------------------------------
# pop_base_max: idade máxima da coorte formadora (Prometidos/Ativo Primário)
# pop_topo_min: idade mínima da coorte legatária (dependente idosa)
#
# IMPORTANTE: a fórmula de NGII_puro implementada em src/indices.py
# segue o Capítulo 5 da tese, que usa Pop_Base = 0-25 e
# Pop_Topo = 25-65 (coorte PROVEDORA atual) de forma fixa, sem
# variação por perfil. As faixas abaixo (coorte Legatária/idosa, que
# a tese usa em outra definição de Pop_Topo na Seção V.III — ver
# docs/definitions.md) NÃO são usadas por calcular_ngii_puro(); estão
# aqui reservadas para uso futuro (ex.: cálculo de NTA(65+) para o
# Fator_Alocativo, Fase 2+).
# Nota: nenhum dos 28 países do Anexo 5 é classificado como Perfil E;
# a faixa é mantida pois consta na Tabela 14.

FAIXAS_ETARIAS_POR_PERFIL = {
    "A": {"pop_base_max": 16, "pop_topo_min": 44, "tfr_min": 4.0, "tfr_max": None},
    "B": {"pop_base_max": 18, "pop_topo_min": 55, "tfr_min": 2.1, "tfr_max": 4.0},
    "C": {"pop_base_max": 21, "pop_topo_min": 60, "tfr_min": 1.2, "tfr_max": 2.1},
    "D": {"pop_base_max": 23, "pop_topo_min": 62, "tfr_min": None, "tfr_max": 1.3},
    "E": {"pop_base_max": 25, "pop_topo_min": 65, "tfr_min": None, "tfr_max": 1.3},
}

# ---------------------------------------------------------------------------
# Cadastro dos 28 países (Anexo 5, dados 2024)
# ---------------------------------------------------------------------------
# perfil: A, B, C ou D, atribuído país a país conforme a faixa de TFR
# da Tabela 14 (a tese agrupa alguns países em rótulos de transição,
# ex. "B→C"; aqui cada país recebe a letra única cuja faixa de TFR o
# contém). Nenhum país do Anexo 5 é classificado como Perfil E.
#
# pop_base_min/max e pop_topo_min/max: fixos para todos os perfis,
# conforme a fórmula do Capítulo 5 (Pop_Base=0-25, Pop_Topo=25-65 —
# coorte PROVEDORA atual, não idosa).
#
# faixa_etaria_farol_min/max: faixa etária da coorte usada no cálculo
# de NTA(65+) para o Fator_Alocativo (Seção V.III-bis). É fixa em
# 65-150 para todos os países/perfis — a fórmula do farol usa
# explicitamente "NTA(65+)", não uma faixa que varia por perfil.

_POP_BASE_TOPO_PADRAO = {
    "pop_base_min": 0,
    "pop_base_max": 25,
    "pop_topo_min": 25,
    "pop_topo_max": 65,
    "faixa_etaria_farol_min": 65,
    "faixa_etaria_farol_max": 150,
}


def _pais(nome: str, regiao: str, perfil: str) -> dict:
    return {"nome": nome, "regiao": regiao, "perfil": perfil, **_POP_BASE_TOPO_PADRAO}


PAISES = {
    "NGA": _pais("Nigéria", "África Subsaariana", "A"),
    "ETH": _pais("Etiópia", "África Subsaariana", "A"),
    "COD": _pais("República Democrática do Congo", "África Subsaariana", "A"),

    "VNM": _pais("Vietnã", "Ásia Sudeste", "B"),
    "IND": _pais("Índia", "Ásia Meridional", "B"),
    "IDN": _pais("Indonésia", "Ásia Sudeste", "B"),
    "IRN": _pais("Irã", "Oriente Médio", "B"),
    "SAU": _pais("Arábia Saudita", "Oriente Médio", "B"),
    "MAR": _pais("Marrocos", "África do Norte", "B"),
    "EGY": _pais("Egito", "África do Norte", "B"),

    "THA": _pais("Tailândia", "Ásia Sudeste", "C"),
    "MEX": _pais("México", "América do Norte", "C"),
    "POL": _pais("Polônia", "Europa Oriental", "C"),
    "BRA": _pais("Brasil", "América do Sul", "C"),
    "USA": _pais("Estados Unidos", "América do Norte", "C"),
    "CHN": _pais("China", "Ásia Oriental", "C"),
    "FRA": _pais("França", "Europa Ocidental", "C"),
    "ARG": _pais("Argentina", "América do Sul", "C"),
    "CHL": _pais("Chile", "América do Sul", "C"),
    "SWE": _pais("Suécia", "Europa Ocidental", "C"),
    "GBR": _pais("Reino Unido", "Europa Ocidental", "C"),
    "AUS": _pais("Austrália", "Oceania", "C"),
    "ZAF": _pais("África do Sul", "África Subsaariana", "C"),

    "JPN": _pais("Japão", "Ásia Oriental", "D"),
    "DEU": _pais("Alemanha", "Europa Ocidental", "D"),
    "ITA": _pais("Itália", "Europa Ocidental", "D"),
    "KOR": _pais("Coreia do Sul", "Ásia Oriental", "D"),
    "RUS": _pais("Rússia", "Eurásia", "D"),
}

# ---------------------------------------------------------------------------
# Plataformas (Anexo 14 — Glossário Técnico, "AINU")
# ---------------------------------------------------------------------------
# narayama.live: interface pública minimalista, mostra só os países
# destaque abaixo (confirmado pelo autor da tese em 2026-07-01).
# ainu.systems: plataforma restrita a pesquisadores e formuladores de
# política, com cálculos detalhados, simulações e calibração para os
# 28 países da amostra (ver app/ainu_systems/ e app/narayama_live/).

PAISES_DESTAQUE_NARAYAMA_LIVE = ["ARG", "BRA", "CHN", "KOR", "USA", "ITA", "JPN"]
