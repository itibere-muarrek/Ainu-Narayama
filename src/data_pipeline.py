"""
Orquestração do cálculo de N* para os 28 países.

Lê data/raw/un_wpp.csv (via src.data_loader) e grava data/processed/n_index_{ano}.csv. Valor publicado = N*_Obs (PQDF-N*,
camada A): NGII_Obs = (Pop_Base/Pop_Topo) × (Nascimentos/Mortes), N_Base = NGII_Obs × Fator_Geracional, N* = √N_Base, sem
nenhum ajuste. Junto vêm, só como referência, os cenários unitários (n_estrela_mig/ine/pol/sub) — ver
docs/definitions.md, seção 6.

Pop_Base/Pop_Topo: cada país usa o corte etário da média ponderada de sua composição de perfis
(src.config.COMPOSICAO_PERFIL_POR_PAIS), já agregada em data/raw/un_wpp.csv por scripts/build_un_wpp_raw.py.

A zona (`status`) é classificada com src.indices.classificar_zona_5 a partir do N_Base (a raiz é monotônica). Fator_Alocativo e
farol ficam vazios: dependem de National Transfer Accounts ainda não integradas.

Fonte de dados: UN World Population Prospects 2024 (population.un.org/wpp), variante média, idade simples.
"""

from pathlib import Path
from typing import Optional

import pandas as pd

from src.config import (
    AJUSTES_FALSEABILIDADE_POR_PAIS,
    CENARIOS_PQDF,
    ANOS_ALVO_HISTORICO,
    DATA_PROCESSED_DIR,
    DATA_RAW_DIR,
    PAISES,
)
from src.data_loader import carregar_dados_un
from src.indices import (
    calcular_fator_geracional,
    calcular_n_base,
    calcular_ngii_obs,
    classificar_zona_5,
    normalizar_n_base,
)

CICLO_GERACIONAL_ANOS = 25


def _arred(v):
    return round(v, 4) if v is not None else None


def _linha_n(linha, tfr_ano_base, codigo: str) -> dict:
    """Cadeia do N* de um país/ano. Valor publicado = N*_Obs (PQDF-N*, camada A, sem ajustes);
    n_estrela_<mig|ine|pol|sub> = cenários unitários."""
    ngii_obs = calcular_ngii_obs(
        pop_base=linha["pop_base"], pop_topo=linha["pop_topo"], nascimentos=linha["nascimentos"], mortes=linha["mortes"]
    )
    fg = calcular_fator_geracional(tfr_atual=linha["tfr"], tfr_25_anos_atras=tfr_ano_base)
    n_base = calcular_n_base(ngii_obs, fg)
    ajustes = AJUSTES_FALSEABILIDADE_POR_PAIS[codigo]
    out = {
        "codigo": codigo,
        "n_base": _arred(n_base),
        "n_estrela": _arred(normalizar_n_base(n_base)),
        "ngii_obs": _arred(ngii_obs),
        "fator_geracional": _arred(fg),
        "status": classificar_zona_5(n_base),
    }
    for sufixo, chave in CENARIOS_PQDF.items():
        nb_k = calcular_n_base(ngii_obs * (1 - ajustes[chave]) if ngii_obs is not None else None, fg)
        out[f"n_estrela_{sufixo}"] = _arred(normalizar_n_base(nb_k))
    return out


def executar_pipeline_completo(ano: int, caminho_un: Optional[Path] = None) -> pd.DataFrame:
    """
    Calcula o N*_Obs (NGII_Obs x Fator_Geracional, raiz quadrada) para os 28
    países da amostra, usando dados da UN WPP para `ano` e `ano - 25`.

    Args:
        ano: Ano de referência (ex.: 2024). Requer que data/raw/un_wpp.csv
            tenha linhas para este ano e para `ano - 25`.
        caminho_un: Caminho alternativo do CSV UN WPP (opcional, usa
            data/raw/un_wpp.csv por padrão).

    Returns:
        DataFrame com uma linha por país (só os países com dados em
        ambos os anos), colunas: codigo, n_base, n_estrela, farol,
        ngii_obs, fator_geracional, fator_alocativo, status, populacao
        (valor publicado = N*_Obs, PQDF-N*) e, como referência, os
        cenários unitários n_estrela_mig/ine/pol/sub. `farol` e `fator_alocativo` ficam
        None nesta fase. Também grava o resultado em
        data/processed/n_index_{ano}.csv.
    """
    caminho_un = caminho_un or (DATA_RAW_DIR / "un_wpp.csv")
    df = carregar_dados_un(caminho_un)

    ano_base = ano - CICLO_GERACIONAL_ANOS
    df_ano = df[df["ano"] == ano].set_index("pais_codigo")
    df_base = df[df["ano"] == ano_base].set_index("pais_codigo")

    resultados = []
    for codigo in PAISES:
        if codigo not in df_ano.index or codigo not in df_base.index:
            continue
        if codigo not in AJUSTES_FALSEABILIDADE_POR_PAIS:
            continue

        linha = df_ano.loc[codigo]

        linha_n = _linha_n(linha, df_base.loc[codigo, "tfr"], codigo)
        resultados.append({**linha_n, "farol": None, "fator_alocativo": None, "populacao": round(linha["pop_total"], 3)})

    ordem = ["codigo", "n_base", "n_estrela", "farol", "ngii_obs", "fator_geracional", "fator_alocativo", "status", "populacao"]
    resultado_df = pd.DataFrame(resultados).sort_values("codigo").reset_index(drop=True)
    resultado_df = resultado_df[ordem + [c for c in resultado_df.columns if c not in ordem]]

    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    caminho_saida = DATA_PROCESSED_DIR / f"n_index_{ano}.csv"
    resultado_df.to_csv(caminho_saida, index=False)

    return resultado_df


def executar_pipeline_historico(
    anos: Optional[list] = None,
    caminho_historico: Optional[Path] = None,
) -> pd.DataFrame:
    """
    Calcula N* pra uma série de anos (série histórica, Fase 2+ —
    decisão do autor de 2026-07-15: começar quinquenal, refinar pra
    anual depois de validações), usando
    data/raw/un_wpp_historico.csv (ver scripts/build_historico_raw.py).

    Mesma cadeia de cálculo de `executar_pipeline_completo`, repetida
    pra cada ano de `anos`: NGII_Obs ->
    N_Base -> N* (normalizado). Cada ano usa seu próprio ano-25 pra
    calcular o Fator_Geracional — o CSV de origem precisa ter uma
    linha de TFR pra esse ano-25 (não precisa ter pop_base/pop_topo:
    só a coluna tfr é lida do ano-25, ver linha `tfr_25_anos_atras`
    abaixo).

    Args:
        anos: Lista de anos-alvo (opcional, usa
            src.config.ANOS_ALVO_HISTORICO por padrão — hoje
            [1990, 1995, ..., 2024]).
        caminho_historico: Caminho alternativo do CSV (opcional, usa
            data/raw/un_wpp_historico.csv por padrão).

    Returns:
        DataFrame com uma linha por (país, ano), colunas: codigo, ano,
        n_base, n_estrela (N*_Obs). Também grava o resultado em
        data/processed/n_index_historico.csv.
    """
    anos = anos or ANOS_ALVO_HISTORICO
    caminho_historico = caminho_historico or (DATA_RAW_DIR / "un_wpp_historico.csv")
    df = carregar_dados_un(caminho_historico)

    resultados = []
    for ano in anos:
        ano_base = ano - CICLO_GERACIONAL_ANOS
        df_ano = df[df["ano"] == ano].set_index("pais_codigo")
        df_base = df[df["ano"] == ano_base].set_index("pais_codigo")

        for codigo in PAISES:
            if codigo not in df_ano.index or codigo not in df_base.index:
                continue
            if codigo not in AJUSTES_FALSEABILIDADE_POR_PAIS:
                continue

            linha = df_ano.loc[codigo]
            if pd.isna(linha["pop_base"]) or pd.isna(linha["pop_topo"]):
                continue

            linha_n = _linha_n(linha, df_base.loc[codigo, "tfr"], codigo)
            resultados.append({"codigo": codigo, "ano": ano, **{k: linha_n[k] for k in ("n_base", "n_estrela")}})

    resultado_df = pd.DataFrame(resultados).sort_values(["codigo", "ano"]).reset_index(drop=True)

    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    caminho_saida = DATA_PROCESSED_DIR / "n_index_historico.csv"
    resultado_df.to_csv(caminho_saida, index=False)

    return resultado_df
