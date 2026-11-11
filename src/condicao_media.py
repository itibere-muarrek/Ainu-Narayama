"""
Condição média em TFT de reposição (exploratório) — cálculo por país.

Usa o motor de projeção (src/projecao.py): a única alavanca é a TFT; mortalidade e migração seguem a projeção média da UN
WPP 2024. Para cada país compara a Tendência (TFT da ONU) com uma Meta (TFT -> alvo em `anos_rampa` anos e mantida), nos
ciclos de 25 anos (2024, 2049, 2074, 2099), e devolve, por país/cenário/ano:

  N*                 N*_Obs da trajetória (função da TFT e da estrutura etária: serve como checagem de coerência do
                     índice, não como evidência de sustentabilidade);
  A_E                razão Ascendentes / Estruturadores (cortes etários do país, Pop_Topo e Pop_Base do N*);
  E_80               Estruturadores por pessoa de 80+ (cuidador POTENCIAL, não cuidador efetivo);
  pop, D, E, A       populações em milhões.

Cenário ≠ previsão. Hipótese H8 do plano do Paper 3 (v5.4): resultado exploratório, limiares ainda não pré-registrados.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import COMPOSICAO_PERFIL_POR_PAIS, PAISES, cortes_por_composicao
from src.projecao import ANO_BASE, n_estrela_serie, projetar, trajetoria_tfr

ANOS_CICLO = (2024, 2049, 2074, 2099)


def _linhas(pais: str, cenario: str, res, serie_n: dict) -> list[dict]:
    base_max, topo_min = cortes_por_composicao(COMPOSICAO_PERFIL_POR_PAIS[pais])
    tot = res.pop.sum(axis=0)  # [idade, ano], em milhares
    out = []
    for ano in ANOS_CICLO:
        k = ano - ANO_BASE
        d = tot[: base_max + 1, k].sum()
        e = tot[base_max + 1 : topo_min, k].sum()
        a = tot[topo_min:, k].sum()
        o80 = tot[80:, k].sum()
        out.append(
            {
                "pais": pais,
                "cenario": cenario,
                "ano": ano,
                "tfr": float(res.tfr[k]),
                "n_estrela": float(serie_n["n_estrela"][k]),
                "zona": serie_n["zona"][k],
                "pop": float(tot[:, k].sum() / 1000),
                "D": float(d / 1000),
                "E": float(e / 1000),
                "A": float(a / 1000),
                "A_E": float(a / e) if e > 0 else np.nan,
                "E_80": float(e / o80) if o80 > 0 else np.nan,
            }
        )
    return out


def tabela_condicao(paises: list[str] | None = None, alvo: float = 2.1, anos_rampa: int = 25) -> pd.DataFrame:
    """Uma linha por país × cenário ("tendencia" | "meta") × ano de ciclo."""
    paises = paises or list(PAISES.keys())
    linhas: list[dict] = []
    for p in paises:
        base = projetar(p)
        meta = projetar(p, trajetoria_tfr(p, alvo, anos_rampa))
        linhas += _linhas(p, "tendencia", base, n_estrela_serie(base))
        linhas += _linhas(p, "meta", meta, n_estrela_serie(meta))
    return pd.DataFrame(linhas)


def resumo_2099(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por país: N* e razões em 2024 e em 2099, Tendência × Meta, e a zona da Meta em 2099."""
    t24 = df[(df.cenario == "tendencia") & (df.ano == 2024)].set_index("pais")
    t99 = df[(df.cenario == "tendencia") & (df.ano == 2099)].set_index("pais")
    m99 = df[(df.cenario == "meta") & (df.ano == 2099)].set_index("pais")
    m74 = df[(df.cenario == "meta") & (df.ano == 2074)].set_index("pais")
    return pd.DataFrame(
        {
            "n_2024": t24["n_estrela"],
            "n_2099_tendencia": t99["n_estrela"],
            "n_2099_meta": m99["n_estrela"],
            "zona_2099_meta": m99["zona"],
            "a_e_2024": t24["A_E"],
            "a_e_2074_meta": m74["A_E"],
            "a_e_2099_meta": m99["A_E"],
            "a_e_2099_tendencia": t99["A_E"],
            "e80_2024": t24["E_80"],
            "e80_2099_meta": m99["E_80"],
            "e80_2099_tendencia": t99["E_80"],
        }
    ).reset_index(names="pais")
