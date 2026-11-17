"""
Derivados da NTA pública (National Transfer Accounts, ntaccounts.org) com o motor do AINU.Systems.

Fonte dos perfis: data/raw/nta_perfis_C_YL_S.csv (perfis por idade "Smooth Mean" de consumo C, renda do trabalho YL e poupança S; ver docs/nta_perfis_fonte.md).
Exceções: as linhas de consumo e renda do trabalho do Japão (2019, IPSS v3.0) e da Coreia do Sul (2024, KOSIS) vêm de fontes nacionais, sem a suavização do portal; ver docs/nta_perfis_fonte.md.
Os cortes etários vêm de src/config.py (composição de perfis) e a população por idade, do motor (UN WPP 2024, variante média). Nada daqui depende de arquivos
fora do repositório.

Funções:
  perfil(iso, var)                  -> (ano do perfil, vetor por idade simples 0..100), ou None se o país não tem perfil
  cfcc_por_coorte(iso, ano_pop)     -> participação (%) de Descendentes, Estruturadores e Ascendentes no consumo total (privado e público):
                                       perfil NTA x população da ONU do ano_pop, com os cortes vigentes.

Limites: perfil suavizado, de um ano que pode diferir do ano da população; a última idade do perfil (85+ ou 90+) é estendida às idades acima; consumo total, sem
separar privado e público. Os valores são estimativas (natureza EST).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from src.config import COMPOSICAO_PERFIL_POR_PAIS, cortes_por_composicao
from src.projecao import ANO_BASE, projetar

ARQUIVO = Path(__file__).resolve().parent.parent / "data" / "raw" / "nta_perfis_C_YL_S.csv"
NOME_NTA = {"ARG": "Argentina", "BRA": "Brazil", "CHN": "China", "FRA": "France", "IND": "India", "ITA": "Italy", "JPN": "Japan",
            "MEX": "Mexico", "NGA": "Nigeria", "KOR": "South Korea", "USA": "US"}


def _ler() -> dict:
    perfis = {}
    with open(ARQUIVO, encoding="utf-8") as fh:
        next(fh)
        for ln in fh:
            p = ln.rstrip("\n").split(",", 6)
            perfis[(p[0], p[1])] = (int(p[2]), np.array([float(x) for x in p[6].split(" ")]))
    return perfis


def perfil(iso: str, var: str = "C"):
    """(ano do perfil, vetor de 101 idades) ou None."""
    nome = NOME_NTA.get(iso)
    dados = _ler().get((nome, var)) if nome else None
    if dados is None:
        return None
    ano, v = dados
    out = np.empty(101)
    out[: len(v)] = v[:101]
    if len(v) < 101:
        out[len(v):] = v[-1]
    return ano, out


# Costa Rica: o perfil por idade do CCP-UCR (CNT_CR2013) não é redistribuído. Entram só os valores agregados do working paper v2.6 (Tabela 16: consumo total por coorte,
# cortes 0–22 / 23–60 / 61+, população da ONU de 2013), com o ano de população indicado.
CFCC_AGREGADO = {"CRI": {"pct": [31.5, 56.2, 12.3], "ano_perfil": 2013, "ano_pop": 2013, "cortes": (22, 61)}}


def cfcc_por_coorte(iso: str, ano_pop: int = 2025):
    """Participação (%) de [Descendentes, Estruturadores, Ascendentes] no consumo total, ou None se não houver perfil NTA.
    Costa Rica: valores agregados do paper (ano_pop = 2013, sem recalcular para outros anos)."""
    p = perfil(iso, "C")
    if p is None:
        return dict(CFCC_AGREGADO[iso]) if iso in CFCC_AGREGADO else None
    ano_perfil, c = p
    bm, tm = cortes_por_composicao(COMPOSICAO_PERFIL_POR_PAIS[iso])
    pop = projetar(iso).pop.sum(axis=0)[:, ano_pop - ANO_BASE]
    pesos = np.array([(c[: bm + 1] * pop[: bm + 1]).sum(), (c[bm + 1: tm] * pop[bm + 1: tm]).sum(), (c[tm:101] * pop[tm:101]).sum()])
    return {"pct": [float(100 * x / pesos.sum()) for x in pesos], "ano_perfil": ano_perfil, "ano_pop": ano_pop, "cortes": (bm, tm)}
