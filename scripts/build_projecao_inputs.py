"""
Constrói data/processed/projecao_inputs.npz — insumos compactos do motor de
projeção por coorte (src/projecao.py) para os 28 países da amostra.

Por que um arquivo em data/processed (e não data/raw): data/raw/* não vai pro
git (os dumps da UN têm ~60-300 MB), então o Render não enxerga. Este script
filtra só os 28 países e só o que o motor usa (alguns MB), e o resultado é
versionado.

Fontes (UN WPP 2024, variante Medium, cache em data/raw/_cache):
  proj.csv.gz               população por idade simples e sexo, 1º de julho, 2024-2100
  deaths_proj.csv.gz        óbitos por idade simples e sexo, ano-calendário, 2024-2100
  fertility_age5.csv.gz     ASFR por grupo quinquenal da mãe, ano-calendário
  demographic_indicators    TFR, nascimentos, razão de sexo ao nascer (1950-2101)

Convenção temporal (verificada numericamente: soma da população por idade ==
TPopulation1July): estoques são de 1º de julho do ano t; fluxos (nascimentos,
óbitos) são do ano-calendário t, centrados no mesmo 1º de julho.

Pressuposto do cenário "tendência da ONU" (pedido do autor em 2026-10-09: a
simulação altera APENAS a TFR; todo o resto segue a tendência verificada):
  - taxa de mortalidade por idade/sexo/ano m = óbitos/população (da ONU);
  - migração líquida em número absoluto por idade/sexo/ano, obtida como
    resíduo da projeção média da ONU (o que sobra após aplicar a mortalidade).
    O resíduo é derivado em src/projecao.py (não armazenado aqui), com a
    mesma função de sobrevivência que o motor usa.

Uso: python scripts/build_projecao_inputs.py
"""

import gzip
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import DATA_PROCESSED_DIR, DATA_RAW_DIR, PAISES

CACHE = DATA_RAW_DIR / "_cache"
SAIDA = DATA_PROCESSED_DIR / "projecao_inputs.npz"
ANOS = np.arange(2024, 2101)  # 77 anos, 1º jul. (estoque) / ano-calendário (fluxo)
IDADES = np.arange(0, 101)  # 0..100+ (aberto)
CODIGOS = list(PAISES.keys())


def _ler_gz(nome, usecols, filtro_iso=True):
    partes = []
    with gzip.open(CACHE / nome, "rt", encoding="utf-8-sig") as f:
        for chunk in pd.read_csv(f, usecols=usecols, chunksize=500_000, low_memory=False):
            if filtro_iso:
                chunk = chunk[chunk["ISO3_code"].isin(CODIGOS)]
            if "Variant" in chunk.columns:
                chunk = chunk[chunk["Variant"] == "Medium"]
            if len(chunk):
                partes.append(chunk)
    return pd.concat(partes, ignore_index=True)


def _matriz(df, col_h, col_m, codigo):
    """DataFrame de um país -> array [sexo(0=H,1=M), idade, ano]."""
    d = df[df["ISO3_code"] == codigo]
    arr = np.zeros((2, len(IDADES), len(ANOS)))
    ia = d["AgeGrpStart"].to_numpy(dtype=int)
    it = (d["Time"].to_numpy(dtype=int) - ANOS[0])
    ok = (it >= 0) & (it < len(ANOS)) & (ia >= 0) & (ia <= 100)
    arr[0, ia[ok], it[ok]] = pd.to_numeric(d[col_h], errors="coerce").to_numpy()[ok]
    arr[1, ia[ok], it[ok]] = pd.to_numeric(d[col_m], errors="coerce").to_numpy()[ok]
    return arr


def construir() -> dict:
    print("[ler] população por idade...")
    pop = _ler_gz("proj.csv.gz", ["ISO3_code", "Variant", "Time", "AgeGrpStart", "PopMale", "PopFemale"])
    print("[ler] óbitos por idade...")
    mor = _ler_gz("deaths_proj.csv.gz", ["ISO3_code", "Variant", "Time", "AgeGrpStart", "DeathMale", "DeathFemale"])
    print("[ler] fecundidade por idade...")
    fec = _ler_gz("fertility_age5.csv.gz", ["ISO3_code", "Variant", "Time", "AgeGrpStart", "ASFR"])
    print("[ler] indicadores demográficos...")
    ind = _ler_gz(
        "demographic_indicators.csv.gz",
        ["ISO3_code", "Variant", "Time", "TFR", "Births", "SRB", "Deaths"],
    )

    grupos = sorted(fec["AgeGrpStart"].unique().tolist())
    print("grupos de fecundidade:", grupos)
    out = {
        "anos": ANOS,
        "idades": IDADES,
        "grupos_fecundidade": np.array(grupos, dtype=int),
        "codigos": np.array(CODIGOS),
    }
    anos_ind = np.arange(1950, 2102)
    for cod in CODIGOS:
        P = _matriz(pop, "PopMale", "PopFemale", cod)  # milhares, 1º jul.
        D = _matriz(mor, "DeathMale", "DeathFemale", cod)  # milhares, ano-calendário
        with np.errstate(divide="ignore", invalid="ignore"):
            m = np.where(P > 0, D / P, 0.0)  # taxa central de mortalidade
        T = len(ANOS)
        # fecundidade (ASFR por 1000 mulheres), grupos x ano
        f = fec[fec["ISO3_code"] == cod]
        asfr = np.zeros((len(grupos), T))
        for gi, g in enumerate(grupos):
            fg = f[f["AgeGrpStart"] == g]
            idx = fg["Time"].to_numpy(dtype=int) - ANOS[0]
            ok = (idx >= 0) & (idx < T)
            asfr[gi, idx[ok]] = fg["ASFR"].to_numpy()[ok]

        i = ind[ind["ISO3_code"] == cod].set_index("Time").reindex(anos_ind)
        out[f"{cod}_pop"] = P
        out[f"{cod}_m"] = m
        out[f"{cod}_asfr"] = asfr
        out[f"{cod}_tfr_ind"] = i["TFR"].to_numpy(dtype=float)  # 1950-2101
        out[f"{cod}_births_ind"] = i["Births"].to_numpy(dtype=float)  # milhares
        out[f"{cod}_deaths_ind"] = i["Deaths"].to_numpy(dtype=float)
        out[f"{cod}_srb"] = i["SRB"].to_numpy(dtype=float)
    out["anos_indicadores"] = anos_ind
    return out


if __name__ == "__main__":
    dados = construir()
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(SAIDA, **dados)
    print(f"[ok] {SAIDA} ({SAIDA.stat().st_size / 1e6:.2f} MB, {len(CODIGOS)} países)")
