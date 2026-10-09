"""
Motor de projeção por coorte (idade simples × sexo) — base da página de
simulação do ainu.systems.

Pedido do autor (2026-10-09): a simulação altera APENAS a TFR; mortalidade e
migração seguem a tendência verificada (projeção média da UN WPP 2024). O
cenário-padrão é o da tese (Seção 8-B): a TFR converge linearmente ao alvo em
25 anos e se mantém por mais 25 (2 ciclos geracionais, horizonte 2074).

Método (componentes de coorte, passo anual de 1º jul. a 1º jul.):
  - sobreviventes:   P(a+1,t+1) = P(a,t)·S(a,t) + M(a+1,t+1),  S = exp(-média de m na diagonal)
      m = taxa central de mortalidade da ONU; M = migração líquida absoluta,
      obtida como resíduo da projeção média da ONU (ver
      scripts/build_projecao_inputs.py). Idade 100+ é aberta.
  - nascimentos:     B(t) = c(t) · Σ_g ASFR_g(t)·r(t)/1000 · Mulheres_g(t)
      r(t) = TFR_cenário(t)/TFR_ONU(t) (preserva o padrão etário de
      fecundidade da ONU); c(t) = B_ONU(t)/B_modelo_ONU(t) é a calibração
      ao total de nascimentos oficial (deve ficar perto de 1 — ver validação).
  - idade 0:         P(0,t+1) = g(t)·0,5·(B(t)+B(t+1)), g calibrado na ONU.

Com a TFR da própria ONU, o modelo reproduz a projeção média da ONU por
construção (população por idade, nascimentos e óbitos). O que NÃO é trivial —
e é verificado em scripts/validar_projecao.py — é: (1) a calibração c(t)
perto de 1; (2) o N* de 2024 bater com data/processed/n_index_2024.csv; (3) o
cenário sem migração bater com a variante "Zero migration" da ONU.

Cenário ≠ previsão: o resultado é um exercício condicional (se a TFR fizer tal
trajetória, mantido tudo mais na tendência da ONU).
"""

from __future__ import annotations

import functools
from dataclasses import dataclass
from typing import Optional

import numpy as np

from src.config import (
    AJUSTES_FALSEABILIDADE_POR_PAIS,
    COMPOSICAO_PERFIL_POR_PAIS,
    DATA_PROCESSED_DIR,
    cortes_por_composicao,
)
from src.indices import (
    calcular_fator_geracional,
    calcular_n_base,
    calcular_ngii_puro,
    classificar_zona_5,
    normalizar_n_base,
)
from src.falseability import aplicar_falseabilidade_quantitativa

ARQUIVO_INSUMOS = DATA_PROCESSED_DIR / "projecao_inputs.npz"
CICLO = 25
ANO_BASE = 2024


@functools.lru_cache(maxsize=1)
def _insumos() -> dict:
    with np.load(ARQUIVO_INSUMOS) as z:
        return {k: z[k] for k in z.files}


@dataclass
class Resultado:
    pais: str
    anos: np.ndarray  # ano de cada coluna (2024..2100)
    pop: np.ndarray  # [sexo, idade, ano], milhares, 1º jul.
    nascimentos: np.ndarray  # milhares, ano-calendário
    obitos: np.ndarray  # milhares, ano-calendário
    tfr: np.ndarray  # TFR do cenário, por ano
    tfr_onu: np.ndarray  # TFR da ONU (variante média), por ano
    migracao: str

    @property
    def pop_total(self) -> np.ndarray:
        return self.pop.sum(axis=(0, 1))


def _fator_sobrevivencia(m: np.ndarray) -> np.ndarray:
    """Fator de sobrevivência do passo 1º jul. t -> t+1, por sexo/idade: mortalidade
    média ao longo da diagonal de Lexis (idade a em t -> a+1 em t+1). Formato
    [sexo, idade, t], t = 0..T-2. Idade 100+ permanece em 100+."""
    S = np.empty((m.shape[0], m.shape[1], m.shape[2] - 1))
    S[:, :100, :] = np.exp(-0.5 * (m[:, :100, :-1] + m[:, 1:101, 1:]))
    S[:, 100, :] = np.exp(-0.5 * (m[:, 100, :-1] + m[:, 100, 1:]))
    return S


@functools.lru_cache(maxsize=None)
def _derivados(pais: str):
    """(S, M): sobrevivência por passo e migração líquida residual (absoluta,
    indexada pelo ano de DESTINO) que faz o modelo reproduzir a projeção média
    da ONU. M absorve migração real + o erro de aproximação do passo anual."""
    ins = _insumos()
    P, m = ins[f"{pais}_pop"], ins[f"{pais}_m"]
    S = _fator_sobrevivencia(m)
    T = P.shape[2]
    M = np.zeros_like(P)
    for t in range(T - 1):
        for s in (0, 1):
            sobrev = np.zeros(P.shape[1])
            sobrev[1:100] = P[s, 0:99, t] * S[s, 0:99, t]
            sobrev[100] = P[s, 99, t] * S[s, 99, t] + P[s, 100, t] * S[s, 100, t]
            M[s, 1:, t + 1] = P[s, 1:, t + 1] - sobrev[1:]
    return S, M


def _idx_ano(ins: dict, ano: int) -> int:
    return int(ano - ins["anos_indicadores"][0])


def tfr_onu(pais: str) -> np.ndarray:
    """TFR da ONU (variante média) para 2024..2100."""
    ins = _insumos()
    i0 = _idx_ano(ins, ANO_BASE)
    return ins[f"{pais}_tfr_ind"][i0 : i0 + len(ins["anos"])]


def tfr_historico(pais: str, ano: int) -> float:
    """TFR da ONU em qualquer ano de 1950 a 2101."""
    ins = _insumos()
    return float(ins[f"{pais}_tfr_ind"][_idx_ano(ins, ano)])


def trajetoria_tfr(pais: str, alvo: float, anos_rampa: int = CICLO, ano_inicio: int = ANO_BASE) -> np.ndarray:
    """TFR do cenário (2024..2100): ONU até ano_inicio, rampa linear até `alvo`
    em `anos_rampa` anos, depois constante no alvo (Seção 8-B da tese)."""
    ins = _insumos()
    anos = ins["anos"]
    base = tfr_onu(pais)
    tfr0 = float(base[ano_inicio - anos[0]])
    out = base.copy()
    for k, ano in enumerate(anos):
        if ano <= ano_inicio:
            continue
        frac = min(1.0, (ano - ano_inicio) / float(anos_rampa))
        out[k] = tfr0 + (alvo - tfr0) * frac
    return out


def calibracao(pais: str) -> np.ndarray:
    """c(t) = nascimentos oficiais da ONU / nascimentos modelados (ASFR da ONU
    × mulheres da ONU), 2024..2100. Perto de 1 => o modelo de fecundidade por
    idade é consistente com o total oficial; a distância de 1 mede o quanto a
    calibração está "consertando" o modelo."""
    ins = _insumos()
    T = len(ins["anos"])
    i0 = _idx_ano(ins, ANO_BASE)
    b_ind = ins[f"{pais}_births_ind"][i0 : i0 + T]
    asfr, grupos, P0 = ins[f"{pais}_asfr"], ins["grupos_fecundidade"], ins[f"{pais}_pop"]
    b_modelo = np.array(
        [(asfr[:, t] / 1000.0 * np.array([P0[1, g : g + 5, t].sum() for g in grupos])).sum() for t in range(T)]
    )
    return np.where(b_modelo > 0, b_ind / b_modelo, 1.0)


def projetar(pais: str, tfr_cenario: Optional[np.ndarray] = None, migracao: str = "un") -> Resultado:
    """Projeta 2024-2100. `tfr_cenario=None` => cenário-base (TFR da ONU).
    `migracao`: "un" (padrão, tendência da ONU) ou "zero" (só p/ validação)."""
    ins = _insumos()
    anos = ins["anos"]
    T = len(anos)
    P0 = ins[f"{pais}_pop"]
    m = ins[f"{pais}_m"]
    S, M_un = _derivados(pais)
    M = M_un if migracao == "un" else np.zeros_like(P0)
    asfr = ins[f"{pais}_asfr"]  # [grupo, ano], por 1000
    grupos = ins["grupos_fecundidade"]
    i0 = _idx_ano(ins, ANO_BASE)
    tfr_ind = ins[f"{pais}_tfr_ind"][i0 : i0 + T]
    b_ind = ins[f"{pais}_births_ind"][i0 : i0 + T]  # milhares

    tfr_c = tfr_ind.copy() if tfr_cenario is None else np.asarray(tfr_cenario, dtype=float)
    razao = np.where(tfr_ind > 0, tfr_c / tfr_ind, 1.0)

    def mulheres_grupo(pf: np.ndarray) -> np.ndarray:
        return np.array([pf[g : g + 5].sum() for g in grupos])

    cal = calibracao(pais)
    # fração masculina e fator g(t) da idade 0 (ONU)
    pop0_tot = P0[:, 0, :].sum(axis=0)
    frac_h = np.where(pop0_tot > 0, P0[0, 0, :] / pop0_tot, 0.512)
    b_passo_onu = 0.5 * (b_ind[:-1] + b_ind[1:])
    g = np.where(b_passo_onu > 0, pop0_tot[1:] / b_passo_onu, 1.0)

    def nascimentos(t: int, pf: np.ndarray) -> float:
        return float(cal[t] * (asfr[:, t] * razao[t] / 1000.0 * mulheres_grupo(pf)).sum())

    P = P0[:, :, 0].copy()
    pop = np.zeros_like(P0)
    pop[:, :, 0] = P
    B = np.zeros(T)
    D = np.zeros(T)
    B[0] = nascimentos(0, P[1])
    D[0] = (P * m[:, :, 0]).sum()
    for t in range(T - 1):
        Pn = np.zeros_like(P)
        for s in (0, 1):
            Pn[s, 1:100] = P[s, 0:99] * S[s, 0:99, t]
            Pn[s, 100] = P[s, 99] * S[s, 99, t] + P[s, 100] * S[s, 100, t]
        Pn[:, 1:] += M[:, 1:, t + 1]
        np.clip(Pn, 0.0, None, out=Pn)
        B[t + 1] = nascimentos(t + 1, Pn[1])
        nasc_passo = g[t] * 0.5 * (B[t] + B[t + 1])
        Pn[0, 0] = nasc_passo * frac_h[t + 1]
        Pn[1, 0] = nasc_passo * (1.0 - frac_h[t + 1])
        P = Pn
        pop[:, :, t + 1] = P
        D[t + 1] = (P * m[:, :, t + 1]).sum()
    return Resultado(pais, anos, pop, B, D, tfr_c, tfr_ind, migracao)


# ---------------------------------------------------------------------------
# N* ao longo da trajetória (mesma cadeia da tese: NGII_bruto -> NGII_puro ->
# N_Base -> N*), com os cortes etários recalculados na hora a partir da
# composição de perfis (editável à mão em src/config.py).
# ---------------------------------------------------------------------------

def n_estrela_serie(res: Resultado, composicao: Optional[dict] = None) -> dict:
    """Série anual do N* e seus componentes para o resultado de `projetar`.

    Ajustes de falseabilidade: constantes por país, calibradas para 2024 — a
    mesma simplificação já assumida na série histórica (docs/definitions.md,
    seção 8-A). Fator_Geracional(t) = TFR(t)/TFR(t-25): usa a TFR da ONU para
    anos < 2024 e a do cenário a partir de 2024.
    """
    ins = _insumos()
    composicao = composicao or COMPOSICAO_PERFIL_POR_PAIS[res.pais]
    base_max, topo_min = cortes_por_composicao(composicao)
    ajustes = AJUSTES_FALSEABILIDADE_POR_PAIS[res.pais]
    anos = res.anos
    tot = res.pop.sum(axis=0)  # [idade, ano]
    pop_base = tot[0 : base_max + 1, :].sum(axis=0) / 1000.0  # milhões
    pop_topo = tot[topo_min:, :].sum(axis=0) / 1000.0
    n_est, n_base_l, ngii_b, ngii_p, fg_l = [], [], [], [], []
    for k, ano in enumerate(anos):
        bruto = calcular_ngii_puro(pop_base[k], pop_topo[k], res.nascimentos[k] / 1000.0, res.obitos[k] / 1000.0)
        puro = aplicar_falseabilidade_quantitativa(bruto, ajustes) if bruto is not None else None
        ano_ant = ano - CICLO
        tfr_ant = res.tfr[ano_ant - anos[0]] if ano_ant >= anos[0] else tfr_historico(res.pais, ano_ant)
        fg = calcular_fator_geracional(res.tfr[k], tfr_ant)
        nb = calcular_n_base(puro, fg)
        n_est.append(normalizar_n_base(nb) if nb is not None else np.nan)
        n_base_l.append(nb if nb is not None else np.nan)
        ngii_b.append(bruto if bruto is not None else np.nan)
        ngii_p.append(puro if puro is not None else np.nan)
        fg_l.append(fg if fg is not None else np.nan)
    return {
        "anos": anos,
        "n_estrela": np.array(n_est),
        "n_base": np.array(n_base_l),
        "ngii_bruto": np.array(ngii_b),
        "ngii_puro": np.array(ngii_p),
        "fator_geracional": np.array(fg_l),
        "pop_base": pop_base,
        "pop_topo": pop_topo,
        "cortes": (base_max, topo_min),
        "zona": [classificar_zona_5(x) if not np.isnan(x) else None for x in np.array(n_base_l)],
    }


# ---------------------------------------------------------------------------
# Pontos de virada (todos calculados; a página mostra os três)
# ---------------------------------------------------------------------------

def pontos_de_virada(res: Resultado, serie_n: dict, limiar_n: float = 0.90) -> dict:
    """Três leituras de "virada", sempre dentro do horizonte projetado:
      1. saldo natural (nascimentos - óbitos) passa de negativo a positivo;
      2. população total: ano do pico (se depois cai) e ano em que a queda
         termina (mínimo, se depois volta a crescer);
      3. N* cruza `limiar_n` (0,90 = piso do PEA) de baixo para cima.
    Cada item é o ano, ou None se não ocorre no horizonte."""
    anos = res.anos
    saldo = res.nascimentos - res.obitos
    v1 = next((int(anos[k]) for k in range(1, len(anos)) if saldo[k - 1] < 0 <= saldo[k]), None)
    pt = res.pop_total
    k_max, k_min = int(np.argmax(pt)), int(np.argmin(pt))
    pico = int(anos[k_max]) if 0 < k_max < len(anos) - 1 else None
    fim_queda = int(anos[k_min]) if 0 < k_min < len(anos) - 1 else None
    n = serie_n["n_estrela"]
    v3 = next((int(anos[k]) for k in range(1, len(anos)) if n[k - 1] < limiar_n <= n[k]), None)
    return {"saldo_natural_positivo": v1, "pico_populacao": pico, "fim_da_queda": fim_queda, "n_estrela_cruza_pea": v3}


def simular(pais: str, tfr_alvo: float, anos_rampa: int = CICLO, composicao: Optional[dict] = None, horizonte: int = 2074) -> dict:
    """Atalho para a página: cenário (TFR -> alvo) e base (tendência ONU)."""
    cen = projetar(pais, trajetoria_tfr(pais, tfr_alvo, anos_rampa))
    bas = projetar(pais)
    n_cen, n_bas = n_estrela_serie(cen, composicao), n_estrela_serie(bas, composicao)
    corte = int(horizonte - ANO_BASE) + 1
    return {
        "cenario": cen,
        "base": bas,
        "n_cenario": n_cen,
        "n_base": n_bas,
        "horizonte_idx": corte,
        "virada_cenario": pontos_de_virada(_cortar(cen, corte), _cortar_n(n_cen, corte)),
        "virada_base": pontos_de_virada(_cortar(bas, corte), _cortar_n(n_bas, corte)),
    }


def _cortar(res: Resultado, n: int) -> Resultado:
    return Resultado(res.pais, res.anos[:n], res.pop[:, :, :n], res.nascimentos[:n], res.obitos[:n], res.tfr[:n], res.tfr_onu[:n], res.migracao)


def _cortar_n(serie: dict, n: int) -> dict:
    return {**serie, "anos": serie["anos"][:n], "n_estrela": serie["n_estrela"][:n]}
