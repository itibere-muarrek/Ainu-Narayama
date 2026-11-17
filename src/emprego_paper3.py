"""
Parte econômica do Paper 3 ("O emprego que nascerá"): empregos brutos por criança adicional, ciclo do casal, custo de um filho e curva em J.

Método e fórmulas: landing/ainu-systems/metodo-paper3 (página de método). Valores do paper: página de cálculos da mesma pasta.
Estudo exploratório; os empregos são tetos de demanda (brutos), e o custo é limite superior (integralmente a cargo dos Estruturadores).

Entradas
  - Perfis por idade de consumo C(a) e de renda do trabalho YL(a): Itália (NTA 2008, portal NTA) e Coreia do Sul (KOSIS 2024), via src/nta_derivados.py.
  - População por idade e cenários (Tendência da ONU e Meta): motor src/projecao.py.
  - Constantes derivadas da ICIO 2019 (OCDE) e do ILOSTAT, calculadas fora do repositório (os arquivos brutos não são redistribuídos): PARAMETROS.
  - Costa Rica: o perfil por idade vem do CCP-UCR e não é redistribuído; entra só por parâmetros agregados (razão custo/renda e razão de consumo), o que
    aproxima a curva em J com perfis planos (ver aproximacao_agregada).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np

from src.config import COMPOSICAO_PERFIL_POR_PAIS, cortes_por_composicao
from src.projecao import projetar, trajetoria_tfr

# Constantes derivadas (valores do paper v2.7; ver a página de cálculos). pc_medio_usd = consumo final por pessoa da ICIO 2019 (US$); inten = empregos
# por US$ milhão de consumo final (ICIO 2019 + ILOSTAT, direto e indireto, doméstico); razao_desc_media = consumo por pessoa de um Descendente dividido
# pelo consumo médio por pessoa (perfil NTA x população); retorno_demanda = parcela do custo de um filho que volta como renda de terceiros (teto).
PARAMETROS = {
    "ITA": {"pc_medio_usd": 22790.8176, "inten": 9.2560, "razao_desc_media": 0.8795, "ano_razao": 2008, "retorno_demanda": 0.452},
    "KOR": {"pc_medio_usd": 17447.1544, "inten": 15.0692, "razao_desc_media": None, "ano_razao": 2024, "retorno_demanda": 0.4615},   # razão: calculada com o perfil KOSIS 2024 (paper v2.7); o v2.6 usava 1,14 (NTA 2019 do portal) e retorno 0,471
    "CRI": {"pc_medio_usd": 9304.721, "inten": 25.7088, "razao_desc_media": 0.8457, "ano_razao": 2013, "retorno_demanda": 0.398,
            "custo_renda": {"total": 0.602, "privado": 0.410, "privado_publico": 0.551}},                                              # CNT_CR2013 (CCP-UCR), agregados
}
RAZAO_KOR_PAPER_V2_6 = 1.14


@dataclass
class CurvaJ:
    anos: np.ndarray
    pct: np.ndarray              # diferença líquida da renda dos Estruturadores, Meta menos Tendência, em % da renda na Tendência
    fundo_pct: float
    ano_fundo: int
    ano_cruza: Optional[int]     # primeiro ano a partir do qual a diferença fica sempre >= 0
    anos_negativos: int
    ganho_bruto: np.ndarray      # só o efeito de haver mais Estruturadores (sem o custo das crianças), em %

    def em(self, ano: int) -> float:
        return float(self.pct[list(self.anos).index(ano)])


def _perfis(iso: str, perfis=None):
    if perfis is not None:
        return perfis
    from src.nta_derivados import perfil

    c, y = perfil(iso, "C"), perfil(iso, "YL")
    return (c[1], y[1]) if c and y else None


def _cortes(iso: str):
    return cortes_por_composicao(COMPOSICAO_PERFIL_POR_PAIS[iso])


def tem_perfil_completo(iso: str) -> bool:
    return _perfis(iso) is not None


def razao_desc_media(iso: str, perfis=None) -> float:
    """Consumo por pessoa de um Descendente / consumo médio por pessoa. Itália e Costa Rica: valor do paper (população do ano do perfil).
    Coreia do Sul: calculada com o perfil KOSIS 2024 e a população de 2024 do motor."""
    p = PARAMETROS[iso]
    if p["razao_desc_media"] is not None and perfis is None:
        return float(p["razao_desc_media"])
    c, _ = _perfis(iso, perfis)
    bm, _ = _cortes(iso)
    pop = projetar(iso).pop.sum(axis=0)[:, 0]
    return float(((c[: bm + 1] * pop[: bm + 1]).sum() / pop[: bm + 1].sum()) / ((c * pop).sum() / pop.sum()))


def emprego_por_crianca(iso: str, deslocamento: float = 0.0, razao: Optional[float] = None) -> dict:
    """Empregos brutos sustentados por uma criança adicional por ano: J(0) = C̄_D x e / 1.000.000 e J(d) = (1 - d) x J(0)."""
    p = PARAMETROS[iso]
    r = razao_desc_media(iso) if razao is None else razao
    pc_desc = r * p["pc_medio_usd"]
    j0 = pc_desc * p["inten"] / 1e6
    return {"razao": r, "consumo_medio_descendente_usd": pc_desc, "intensidade": p["inten"], "j0": j0, "j": (1.0 - deslocamento) * j0}


def ciclo_casal(j0: float, filhos: int = 2, iso: str = "ITA") -> dict:
    """Ciclo completo de um casal (ilustração contábil, em posto-ano): J_casal = n x J(0); J_ciclo = J_casal x (1 + r), r = fase dos pais / fase dos filhos."""
    bm, tm = _cortes(iso)
    r_exato = (tm - (bm + 1)) / (bm + 1)
    j_casal = filhos * j0
    return {"j_casal": j_casal, "r_exato": r_exato, "ciclo_exato": j_casal * (1 + r_exato), "ciclo_r2": j_casal * (1 + 2.0)}


def _curva(rel: np.ndarray, anos: np.ndarray, ganho: np.ndarray) -> CurvaJ:
    i = int(np.argmin(rel))
    pos = [k for k in range(i, len(rel)) if (rel[k:] >= 0).all()]
    return CurvaJ(anos=anos, pct=rel, fundo_pct=float(rel[i]), ano_fundo=int(anos[i]), ano_cruza=int(anos[pos[0]]) if pos else None,
                  anos_negativos=int((rel < -1e-9).sum()), ganho_bruto=ganho)


def curva_j(iso: str, tfr_alvo: float = 2.1, rampa: int = 25, retorno: float = 0.0, perfis=None, base_custo: str = "total") -> CurvaJ:
    """Curva em J: [renda dos Estruturadores na Meta menos na Tendência] menos [custo das crianças adicionais de 0 a 22 anos], em % da renda na Tendência.
    retorno = parcela do custo que volta como renda de terceiros (0 = sem retorno; PARAMETROS[iso]["retorno_demanda"] = teto do paper).
    Itália e Coreia do Sul: com os perfis por idade. Costa Rica (sem perfil por idade no repositório): aproximação agregada com perfis planos.
    base_custo (só Costa Rica): "total" (déficit do ciclo de vida), "privado" ou "privado_publico"."""
    bm, tm = _cortes(iso)
    meta = projetar(iso, trajetoria_tfr(iso, tfr_alvo, rampa))
    tend = projetar(iso)
    pm, pt = meta.pop.sum(axis=0), tend.pop.sum(axis=0)
    anos = np.array(meta.anos)
    dp = pm - pt
    pf = _perfis(iso, perfis)
    if pf is not None:
        c, y = pf
        lcd = c - y
        d_yl = np.array([(y[bm + 1:tm] * dp[bm + 1:tm, k]).sum() for k in range(dp.shape[1])])
        yl_t = np.array([(y[bm + 1:tm] * pt[bm + 1:tm, k]).sum() for k in range(pt.shape[1])])
        custo = np.array([(lcd[:bm + 1] * dp[:bm + 1, k]).sum() for k in range(dp.shape[1])])
    else:
        rho = PARAMETROS[iso]["custo_renda"][base_custo]           # custo médio de um filho / renda média de um Estruturador
        d_yl = dp[bm + 1:tm].sum(axis=0)                           # renda por Estruturador = 1 (perfil plano)
        yl_t = pt[bm + 1:tm].sum(axis=0)
        custo = rho * dp[:bm + 1].sum(axis=0)
    rel = (d_yl - (1.0 - retorno) * custo) / yl_t * 100
    return _curva(rel, anos, d_yl / yl_t * 100)
