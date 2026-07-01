"""
Carregamento e validação de dados brutos do AINU-Narayama.

Lê os arquivos de origem (UN World Population Prospects e OECD
Social Expenditure Database) a partir de data/raw/ e prepara os
DataFrames usados pelo motor de cálculo em src/indices.py.

Nota: `pop_base` e `pop_topo` já vêm agregadas com o corte etário
correto por perfil do país (Seção V.III: Perfis A/B = 0-25/55+;
Perfis C/D/E = 0-21/61+ — ver src.config.FAIXAS_ETARIAS_POR_PERFIL_V3),
não uma faixa fixa — por isso os nomes das colunas não têm a idade
embutida. As colunas de escolaridade (`taxa_escolaridade_0_25`,
`taxa_escolaridade_esperada`), exigidas pela fórmula do NGII_puro
adotada (terceiro fator do Capítulo 5), foram colocadas na fonte
OECD por não serem cobertas pela UN WPP; isso é uma aproximação
prática desta Fase 1 e deve ser confirmado/ajustado quando a fonte de
dados real de escolaridade for definida (ex.: UNESCO, World Bank).
"""

from pathlib import Path
from typing import List, Tuple, Union

import pandas as pd

from src.config import DATA_RAW_DIR, PAISES

# Colunas mínimas esperadas em cada fonte de dados.
COLUNAS_UN_ESPERADAS = [
    "pais_codigo",
    "ano",
    "pop_total",
    "pop_base",
    "pop_topo",
    "nascimentos",
    "mortes",
    "tfr",
]

COLUNAS_OECD_ESPERADAS = [
    "pais_codigo",
    "ano",
    "gasto_educacao",
    "gasto_saude_infantil",
    "gasto_pensao",
    "gasto_saude_geriatrica",
    "taxa_escolaridade_0_25",
    "taxa_escolaridade_esperada",
]


def carregar_dados_un(arquivo_caminho: Union[str, Path]) -> pd.DataFrame:
    """
    Lê o CSV com dados demográficos da UN World Population Prospects (WPP).

    Colunas esperadas: pais_codigo, ano, pop_total, pop_base,
    pop_topo, nascimentos, mortes, tfr (pop_base/pop_topo já
    agregadas com o corte etário certo por perfil do país).

    Args:
        arquivo_caminho: Caminho do arquivo CSV.

    Returns:
        DataFrame pandas com os dados lidos. Se o arquivo não existir,
        imprime uma mensagem clara e retorna um DataFrame vazio com
        as colunas esperadas.
    """
    caminho = Path(arquivo_caminho)

    if not caminho.exists():
        print(f"Arquivo UN não encontrado em {caminho}")
        return pd.DataFrame(columns=COLUNAS_UN_ESPERADAS)

    try:
        return pd.read_csv(caminho)
    except Exception as erro:
        print(f"Erro ao ler arquivo UN em {caminho}: {erro}")
        return pd.DataFrame(columns=COLUNAS_UN_ESPERADAS)


def carregar_dados_oecd(arquivo_caminho: Union[str, Path]) -> pd.DataFrame:
    """
    Lê o CSV com dados de gasto social da OECD Social Expenditure Database (SOCX).

    Colunas esperadas: pais_codigo, ano, gasto_educacao,
    gasto_saude_infantil, gasto_pensao, gasto_saude_geriatrica,
    taxa_escolaridade_0_25, taxa_escolaridade_esperada.

    Args:
        arquivo_caminho: Caminho do arquivo CSV.

    Returns:
        DataFrame pandas com os dados lidos. Se o arquivo não existir,
        imprime uma mensagem clara e retorna um DataFrame vazio com
        as colunas esperadas.
    """
    caminho = Path(arquivo_caminho)

    if not caminho.exists():
        print(f"Arquivo OECD não encontrado em {caminho}")
        return pd.DataFrame(columns=COLUNAS_OECD_ESPERADAS)

    try:
        return pd.read_csv(caminho)
    except Exception as erro:
        print(f"Erro ao ler arquivo OECD em {caminho}: {erro}")
        return pd.DataFrame(columns=COLUNAS_OECD_ESPERADAS)


def validar_dados(df_un: pd.DataFrame, df_oecd: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Valida os DataFrames UN e OECD.

    Verifica: (1) colunas obrigatórias presentes, (2) ausência de
    valores nulos (NaN) nas colunas obrigatórias, (3) presença dos 28
    países da amostra (src.config.PAISES) em cada DataFrame.

    Args:
        df_un: DataFrame retornado por carregar_dados_un().
        df_oecd: DataFrame retornado por carregar_dados_oecd().

    Returns:
        Tupla (booleano_valido, lista_problemas). Exemplo:
        (True, []) ou (False, ["Faltam dados de Brasil em UN"]).
    """
    problemas: List[str] = []
    codigos_esperados = set(PAISES.keys())

    for nome, df, colunas in (
        ("UN", df_un, COLUNAS_UN_ESPERADAS),
        ("OECD", df_oecd, COLUNAS_OECD_ESPERADAS),
    ):
        colunas_faltantes = [c for c in colunas if c not in df.columns]
        if colunas_faltantes:
            problemas.append(f"Dados {nome}: colunas ausentes {colunas_faltantes}")
            continue

        if df[colunas].isna().any().any():
            linhas_com_nan = df[df[colunas].isna().any(axis=1)]
            problemas.append(f"Dados {nome}: valores ausentes (NaN) em {len(linhas_com_nan)} linha(s)")

        codigos_presentes = set(df["pais_codigo"].unique()) if "pais_codigo" in df.columns else set()
        codigos_faltantes = codigos_esperados - codigos_presentes
        for codigo in sorted(codigos_faltantes):
            problemas.append(f"Faltam dados de {PAISES[codigo]['nome']} ({codigo}) em {nome}")

    return (len(problemas) == 0, problemas)


def carregar_dados_completo():
    """
    Carrega e valida os dados UN WPP e OECD SOCX a partir de data/raw/.

    Usa data/raw/un_wpp.csv e data/raw/oecd_socx.csv como caminhos
    padrão (ver src.config.DATA_RAW_DIR).

    Returns:
        Tupla (df_un, df_oecd) se ambos os DataFrames forem válidos,
        ou None se houver qualquer problema de validação (a lista de
        problemas é impressa antes de retornar).
    """
    df_un = carregar_dados_un(DATA_RAW_DIR / "un_wpp.csv")
    df_oecd = carregar_dados_oecd(DATA_RAW_DIR / "oecd_socx.csv")

    valido, problemas = validar_dados(df_un, df_oecd)

    if not valido:
        print("Falha na validação dos dados:")
        for problema in problemas:
            print(f"  - {problema}")
        return None

    return (df_un, df_oecd)
