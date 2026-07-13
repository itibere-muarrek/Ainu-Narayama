"""
Configurações centrais do projeto AINU-Narayama.

Contém o cadastro dos 28 países cobertos pela tese v8.0 (Anexo 5),
os limiares críticos do Índice de Narayama Sistêmico (N*) e os
caminhos padrão de dados usados pelo restante do pipeline.

Fonte: V1_EcoPol_062426_v8.0.docx (tese de doutorado, Cap. 3, V.III,
Capítulo 5, Anexo 5, Anexo 8, Tabela 4, Tabela 14).
"""

import math
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

# Limiares na escala normalizada (N* = sqrt(N_Base), decisão de
# 2026-07-09 — ver src.indices.normalizar_n_base). Derivados
# dinamicamente de LIMIARES_SIMPLES, nunca hardcoded 2ª vez, pra não
# ficarem dessincronizados. A classificação de zona em si continua
# usando os limiares brutos (a raiz é monotônica, dá a mesma zona) —
# estes aqui servem só pra UI colorir a tabela já na escala exibida.
LIMIARES_SIMPLES_NORMALIZADOS = {k: math.sqrt(v) for k, v in LIMIARES_SIMPLES.items()}

# ---------------------------------------------------------------------------
# Classificação de 5 zonas (revisão do autor, 12/07/2026)
# ---------------------------------------------------------------------------
# A tese passou a definir PEEC como limiar de N* (antes era diagnosticado
# só por TFR — ver LIMIAR_PEEC_TFR acima, mantido por compatibilidade).
# Os 4 limiares em N_Base abaixo (0,50/0,81/1,96/4,00) correspondem
# exatamente às raízes quadradas de N* = 0,71/0,90/1,40/2,00 — 3 deles
# (0,81=0,9²; 1,96=1,4²; 4,00=2,0²) são quadrados perfeitos; o quarto
# (0,50) é o limiar original PEC/Tensão Acelerada da Tabela 4/Anexo 8,
# inalterado (sua raiz, 0,7071, foi só arredondada para 0,71 na escala
# nova — não é quadrado perfeito, ao contrário do que uma nota do autor
# na tese afirma).
#
# classificar_zona_n_base (4 zonas, Tabela 4/Anexo 8) permanece intacta
# como referência histórica — não é mais a usada pelo pipeline.

LIMIARES_5_ZONAS = {
    "pec": 0.50,
    "tensao_acelerada": 0.81,
    "pea": 1.96,
    "tensao_populacional": 4.00,
}

LIMIARES_5_ZONAS_NORMALIZADOS = {k: math.sqrt(v) for k, v in LIMIARES_5_ZONAS.items()}

# Cores exatas da legenda da tese (Seção 9-A.7).
CORES_5_ZONAS = {
    "Colapso de Narayama (PEC)": "#f5c2c7",  # vermelho
    "Tensão Acelerada": "#ffdba8",  # laranja
    "Equilíbrio Sustentável (PEA)": "#cfe2ff",  # azul
    "Tensão Populacional": "#fff3cd",  # amarelo-claro
    "Saturação por Overbirths (PEEC)": "#ffd60a",  # amarelo forte
}

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
# Fórmulas (Anexo 1, A1.2 — NGII_puro com 2 componentes)
# ---------------------------------------------------------------------------

FORMULAS = {
    "ngii_puro": "NGII_puro = (Pop_Base / Pop_Topo) x (Nascimentos / Mortes)",
    "componente_1": "Razao Geracional = Pop_Base / Pop_Topo (faixa etaria varia por perfil, ver FAIXAS_ETARIAS_POR_PERFIL_TABELA14)",
    "componente_2": "Vitalidade = Nascimentos / Mortes",
    "fator_geracional": "Fator_Geracional = TFR_atual / TFR_25_anos_atras",
    "n_base": "N* = N_Base = NGII_puro x Fator_Geracional",
    "fator_alocativo": "Fator_Alocativo = NTA(0-25) / NTA(65+)",
    "nota": (
        "Decisao vigente (atualizada em 2026-07-03): NGII_puro usa a "
        "formula de 2 componentes do Anexo 1 / Secao V.III, sem o "
        "terceiro fator de escolaridade do Capitulo 5 (removido). "
        "Pop_Base/Pop_Topo usam as faixas etarias por perfil da Tabela "
        "14 (5 niveis, mais granular que a Secao V.III — ver "
        "FAIXAS_ETARIAS_POR_PERFIL_TABELA14 abaixo). O Anexo 1 nao "
        "especifica nenhum passo de normalizacao do N_Base — valores "
        "altos em paises jovens/alta fecundidade sao uma consequencia "
        "matematica da formula tal como publicada (ver docs/definitions.md)."
    ),
}

# ---------------------------------------------------------------------------
# Faixas etárias por Perfil Estrutural — Tabela 14 (decisão vigente)
# ---------------------------------------------------------------------------
# A tese define as faixas de Pop_Base/Pop_Topo por perfil de duas
# formas diferentes (V.III, com 2 níveis, vs. Tabela 14, com 5
# níveis, mais granular — ver docs/definitions.md). Decisão
# confirmada em 2026-07-03: usar a Tabela 14 (5 níveis) para todos os
# 28 países, calibrando os cortes etários por perfil individualmente
# em vez da faixa binária da Seção V.III (A/B vs. C/D/E). A fórmula
# do NGII_puro usa a versão de 2 componentes do Anexo 1 (2026-07-02)
# — o terceiro fator de escolaridade do Capítulo 5 continua removido.
#
# pop_base_max: idade máxima da coorte formadora (Prometidos/Ativo Primário)
# pop_topo_min: idade mínima da coorte legatária (dependente idosa)
# Nenhum dos 28 países do Anexo 5 é classificado como Perfil E.

FAIXAS_ETARIAS_POR_PERFIL_TABELA14 = {
    "A": {"pop_base_max": 16, "pop_topo_min": 44, "tfr_min": 4.0, "tfr_max": None},
    "B": {"pop_base_max": 18, "pop_topo_min": 55, "tfr_min": 2.1, "tfr_max": 4.0},
    "C": {"pop_base_max": 21, "pop_topo_min": 60, "tfr_min": 1.2, "tfr_max": 2.1},
    "D": {"pop_base_max": 23, "pop_topo_min": 62, "tfr_min": None, "tfr_max": 1.3},
    "E": {"pop_base_max": 25, "pop_topo_min": 65, "tfr_min": None, "tfr_max": 1.3},
}

# ---------------------------------------------------------------------------
# Faixas etárias por Perfil Estrutural — Seção V.III (referência, não usada)
# ---------------------------------------------------------------------------
# Versão anterior, de 2 níveis (A/B vs. C/D/E), usada até 2026-07-02.
# Mantida aqui só como referência/histórico.
# Seção V.III: "Pop_Base = coorte 0–25 (Perfis A/B) ou 0–21 (Perfis
# C/D/E); Pop_Topo = coorte 55+ (Perfis A/B) ou 61+ (Perfis C/D/E)".

FAIXAS_ETARIAS_POR_PERFIL_V3 = {
    "A": {"pop_base_max": 25, "pop_topo_min": 55},
    "B": {"pop_base_max": 25, "pop_topo_min": 55},
    "C": {"pop_base_max": 21, "pop_topo_min": 61},
    "D": {"pop_base_max": 21, "pop_topo_min": 61},
    "E": {"pop_base_max": 21, "pop_topo_min": 61},
}

# ---------------------------------------------------------------------------
# Composição de perfis por país — Seção 5.2 (decisão de 2026-07-04)
# ---------------------------------------------------------------------------
# CORREÇÃO: até 2026-07-03 este arquivo atribuía UM único perfil (A-E) a
# cada país. Isso estava errado — a Seção 5.2 do docx v8.0 (verificada
# diretamente, e confirmada país a país com o usuário) classifica cada um
# dos 28 países como uma COMPOSIÇÃO PONDERADA de 2-3 perfis adjacentes
# (ex.: Brasil = 30% B + 40% C + 30% D — não "Perfil C" puro). Isso também
# corrige a afirmação (antes nesta seção) de que nenhum país é Perfil E:
# Japão usa 40% Perfil E.
#
# pop_base_max/pop_topo_min de cada país (ver _cortes_ponderados) são a
# média ponderada dos cortes de FAIXAS_ETARIAS_POR_PERFIL_TABELA14 pelos
# pesos abaixo, arredondada ao inteiro mais próximo (round-half-up, não o
# banker's rounding padrão do Python — só muda o resultado de IRN, SAU e
# POL, os três únicos países cuja média cai exatamente em ",5").

COMPOSICAO_PERFIL_POR_PAIS = {
    "NGA": {"A": 0.35, "B": 0.40, "C": 0.25},
    "ETH": {"A": 0.40, "B": 0.40, "C": 0.20},
    "COD": {"A": 0.60, "B": 0.40},
    "VNM": {"B": 0.80, "C": 0.20},
    "IND": {"B": 1.00},
    "IDN": {"B": 1.00},
    "IRN": {"B": 0.70, "C": 0.30},
    "SAU": {"B": 0.70, "C": 0.30},
    "MAR": {"B": 1.00},
    "THA": {"B": 0.80, "C": 0.20},
    "MEX": {"B": 0.40, "C": 0.60},
    "EGY": {"B": 0.80, "C": 0.20},
    "POL": {"B": 0.30, "C": 0.70},
    "BRA": {"B": 0.30, "C": 0.40, "D": 0.30},
    "USA": {"C": 0.20, "D": 0.80},
    "CHN": {"B": 0.25, "C": 0.60, "D": 0.15},
    "FRA": {"C": 0.80, "D": 0.20},
    "ARG": {"C": 0.85, "D": 0.15},
    "CHL": {"C": 1.00},
    "SWE": {"C": 1.00},
    "GBR": {"C": 0.80, "D": 0.20},
    "AUS": {"C": 1.00},
    "ZAF": {"B": 0.80, "C": 0.20},
    "JPN": {"D": 0.60, "E": 0.40},
    "DEU": {"C": 0.20, "D": 0.80},
    "ITA": {"C": 0.50, "D": 0.50},
    "KOR": {"C": 0.80, "D": 0.20},
    "RUS": {"C": 0.30, "D": 0.70},
}

for _codigo, _composicao in COMPOSICAO_PERFIL_POR_PAIS.items():
    assert abs(sum(_composicao.values()) - 1.0) < 1e-9, (
        f"composição de {_codigo} não soma 1.0: {_composicao}"
    )
del _codigo, _composicao


def _cortes_ponderados(composicao: dict) -> tuple:
    """Média ponderada dos cortes por perfil, arredondada (round-half-up)."""
    base_max = sum(
        peso * FAIXAS_ETARIAS_POR_PERFIL_TABELA14[perfil]["pop_base_max"]
        for perfil, peso in composicao.items()
    )
    topo_min = sum(
        peso * FAIXAS_ETARIAS_POR_PERFIL_TABELA14[perfil]["pop_topo_min"]
        for perfil, peso in composicao.items()
    )
    return math.floor(base_max + 0.5), math.floor(topo_min + 0.5)


def _rotulo_composicao(composicao: dict) -> str:
    ordem = "ABCDE"
    partes = [f"{p}{round(composicao[p] * 100):g}" for p in ordem if p in composicao]
    return "/".join(partes)


# ---------------------------------------------------------------------------
# Cadastro dos 28 países (Anexo 5 / Seção 5.2, dados 2024)
# ---------------------------------------------------------------------------
# pop_base_min/max e pop_topo_min/max: derivados da composição do país em
# COMPOSICAO_PERFIL_POR_PAIS via _cortes_ponderados (ver seção acima).
#
# faixa_etaria_farol_min/max: faixa etária da coorte usada no cálculo
# de NTA(65+) para o Fator_Alocativo (Seção V.III-bis). É fixa em
# 65-150 para todos os países/perfis — a fórmula do farol usa
# explicitamente "NTA(65+)", não uma faixa que varia por perfil.

_FAROL_FAIXA_PADRAO = {"faixa_etaria_farol_min": 65, "faixa_etaria_farol_max": 150}


def _pais(nome: str, regiao: str, codigo: str) -> dict:
    composicao = COMPOSICAO_PERFIL_POR_PAIS[codigo]
    pop_base_max, pop_topo_min = _cortes_ponderados(composicao)
    return {
        "nome": nome,
        "regiao": regiao,
        "perfil": _rotulo_composicao(composicao),
        "pop_base_min": 0,
        "pop_base_max": pop_base_max,
        "pop_topo_min": pop_topo_min,
        "pop_topo_max": 150,
        **_FAROL_FAIXA_PADRAO,
    }


PAISES = {
    "NGA": _pais("Nigéria", "África Subsaariana", "NGA"),
    "ETH": _pais("Etiópia", "África Subsaariana", "ETH"),
    "COD": _pais("República Democrática do Congo", "África Subsaariana", "COD"),

    "VNM": _pais("Vietnã", "Ásia Sudeste", "VNM"),
    "IND": _pais("Índia", "Ásia Meridional", "IND"),
    "IDN": _pais("Indonésia", "Ásia Sudeste", "IDN"),
    "IRN": _pais("Irã", "Oriente Médio", "IRN"),
    "SAU": _pais("Arábia Saudita", "Oriente Médio", "SAU"),
    "MAR": _pais("Marrocos", "África do Norte", "MAR"),
    "EGY": _pais("Egito", "África do Norte", "EGY"),

    "THA": _pais("Tailândia", "Ásia Sudeste", "THA"),
    "MEX": _pais("México", "América do Norte", "MEX"),
    "POL": _pais("Polônia", "Europa Oriental", "POL"),
    "BRA": _pais("Brasil", "América do Sul", "BRA"),
    "USA": _pais("Estados Unidos", "América do Norte", "USA"),
    "CHN": _pais("China", "Ásia Oriental", "CHN"),
    "FRA": _pais("França", "Europa Ocidental", "FRA"),
    "ARG": _pais("Argentina", "América do Sul", "ARG"),
    "CHL": _pais("Chile", "América do Sul", "CHL"),
    "SWE": _pais("Suécia", "Europa Ocidental", "SWE"),
    "GBR": _pais("Reino Unido", "Europa Ocidental", "GBR"),
    "AUS": _pais("Austrália", "Oceania", "AUS"),
    "ZAF": _pais("África do Sul", "África Subsaariana", "ZAF"),

    "JPN": _pais("Japão", "Ásia Oriental", "JPN"),
    "DEU": _pais("Alemanha", "Europa Ocidental", "DEU"),
    "ITA": _pais("Itália", "Europa Ocidental", "ITA"),
    "KOR": _pais("Coreia do Sul", "Ásia Oriental", "KOR"),
    "RUS": _pais("Rússia", "Eurásia", "RUS"),
}

# ---------------------------------------------------------------------------
# Protocolo de Falseabilidade quantitativo — Anexo 9 (v9.0, 2026-07-07)
# ---------------------------------------------------------------------------
# A v9.0 da tese (V1_EcoPol_070726_v9.0.docx) reescreveu o Anexo 9: os 7
# testes qualitativos da v8.0 (ver src/falseability.py,
# aplicar_protocolo_falseabilidade — mantida como referência histórica)
# foram substituídos por uma fórmula quantitativa de 4 ajustes
# multiplicativos, calibrados país a país e aprovados pelo usuário com um
# pesquisador colaborador da Unicamp:
#
#   NGII_Puro = NGII_Bruto × (1-migratorio) × (1-inercia) × (1-politicas) × (1-subregistro)
#
# Critério de aceitação da v9.0: redução total composta entre 25% e 45%.
# Os percentuais abaixo foram fornecidos pelo usuário; a fórmula de
# aplicação (multiplicativa, não aditiva) foi corrigida por este projeto
# antes de incorporar — a primeira versão da tabela tinha os percentuais
# certos mas o resultado final publicado batia com uma soma simples dos
# percentuais, não com a fórmula multiplicativa declarada.

AJUSTES_FALSEABILIDADE_POR_PAIS = {
    "SAU": {"migratorio": 0.22, "inercia": 0.12, "politicas": 0.12, "subregistro": 0.06},
    "ETH": {"migratorio": 0.11, "inercia": 0.18, "politicas": 0.07, "subregistro": 0.17},
    "COD": {"migratorio": 0.10, "inercia": 0.16, "politicas": 0.05, "subregistro": 0.23},
    "NGA": {"migratorio": 0.09, "inercia": 0.15, "politicas": 0.06, "subregistro": 0.19},
    "EGY": {"migratorio": 0.08, "inercia": 0.14, "politicas": 0.09, "subregistro": 0.11},
    "MEX": {"migratorio": 0.14, "inercia": 0.11, "politicas": 0.06, "subregistro": 0.08},
    "MAR": {"migratorio": 0.11, "inercia": 0.12, "politicas": 0.07, "subregistro": 0.09},
    "IRN": {"migratorio": 0.09, "inercia": 0.13, "politicas": 0.10, "subregistro": 0.08},
    "ZAF": {"migratorio": 0.15, "inercia": 0.11, "politicas": 0.07, "subregistro": 0.12},
    "IND": {"migratorio": 0.06, "inercia": 0.18, "politicas": 0.08, "subregistro": 0.10},
    "IDN": {"migratorio": 0.07, "inercia": 0.16, "politicas": 0.07, "subregistro": 0.09},
    "VNM": {"migratorio": 0.06, "inercia": 0.15, "politicas": 0.08, "subregistro": 0.07},
    "BRA": {"migratorio": 0.12, "inercia": 0.15, "politicas": 0.06, "subregistro": 0.04},
    "ARG": {"migratorio": 0.10, "inercia": 0.12, "politicas": 0.05, "subregistro": 0.04},
    "AUS": {"migratorio": 0.25, "inercia": 0.06, "politicas": 0.04, "subregistro": 0.03},
    "CHL": {"migratorio": 0.13, "inercia": 0.10, "politicas": 0.07, "subregistro": 0.05},
    "USA": {"migratorio": 0.18, "inercia": 0.08, "politicas": 0.04, "subregistro": 0.03},
    "GBR": {"migratorio": 0.17, "inercia": 0.08, "politicas": 0.06, "subregistro": 0.04},
    "SWE": {"migratorio": 0.22, "inercia": 0.07, "politicas": 0.05, "subregistro": 0.03},
    "FRA": {"migratorio": 0.15, "inercia": 0.09, "politicas": 0.08, "subregistro": 0.04},
    "CHN": {"migratorio": 0.09, "inercia": 0.14, "politicas": 0.12, "subregistro": 0.06},
    "RUS": {"migratorio": 0.12, "inercia": 0.14, "politicas": 0.06, "subregistro": 0.09},
    "THA": {"migratorio": 0.10, "inercia": 0.13, "politicas": 0.08, "subregistro": 0.07},
    "POL": {"migratorio": 0.08, "inercia": 0.12, "politicas": 0.05, "subregistro": 0.06},
    "DEU": {"migratorio": 0.14, "inercia": 0.12, "politicas": 0.05, "subregistro": 0.06},
    "KOR": {"migratorio": 0.07, "inercia": 0.16, "politicas": 0.05, "subregistro": 0.13},
    "ITA": {"migratorio": 0.11, "inercia": 0.15, "politicas": 0.06, "subregistro": 0.07},
    "JPN": {"migratorio": 0.08, "inercia": 0.18, "politicas": 0.04, "subregistro": 0.13},
}

for _codigo, _ajustes in AJUSTES_FALSEABILIDADE_POR_PAIS.items():
    assert all(0 <= v < 1 for v in _ajustes.values()), f"ajuste fora de [0,1) em {_codigo}: {_ajustes}"
    _reducao_total = 1 - (
        (1 - _ajustes["migratorio"])
        * (1 - _ajustes["inercia"])
        * (1 - _ajustes["politicas"])
        * (1 - _ajustes["subregistro"])
    )
    assert 0.25 <= _reducao_total <= 0.45, (
        f"redução total de {_codigo} ({_reducao_total:.1%}) fora do critério de aceitação da v9.0 (25%-45%)"
    )
del _codigo, _ajustes, _reducao_total

# ---------------------------------------------------------------------------
# Plataformas (Anexo 14 — Glossário Técnico, "AINU")
# ---------------------------------------------------------------------------
# narayama.live: interface pública minimalista, mostra só os países
# destaque abaixo (confirmado pelo autor da tese em 2026-07-01).
# ainu.systems: plataforma restrita a pesquisadores e formuladores de
# política, com cálculos detalhados, simulações e calibração para os
# 28 países da amostra (ver app/ainu_systems/ e app/narayama_live/).

PAISES_DESTAQUE_NARAYAMA_LIVE = ["ARG", "BRA", "CHN", "KOR", "USA", "ITA", "JPN"]
