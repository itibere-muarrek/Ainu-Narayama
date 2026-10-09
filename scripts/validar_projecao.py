"""
Validação do motor de projeção por coorte (src/projecao.py).

Com a TFR da própria ONU o modelo reproduz a projeção média por construção;
por isso este script mede o que NÃO é trivial:

  V1  Calibração c(t) dos nascimentos (modelo ASFR×mulheres vs total oficial).
  V2  Migração líquida residual (soma sobre as idades) vs NetMigrations da ONU
      — mede se o "resíduo" é de fato migração (e não viés do método).
  V3  N* de 2024 recalculado pelo motor vs data/processed/n_index_2024.csv
      (integração com o pipeline de produção).
  V4  Cenário sem migração vs variante "Zero migration" da ONU (pop. 2074).
  V5  Cenário TFR→2,1 sem migração vs P_eq do projeto
      (data/raw/convergencia_un.csv; método antigo = escala de nascimentos).

Uso: python scripts/validar_projecao.py   (precisa dos caches em data/raw/_cache)
Escreve docs/validacao_projecao.md.
"""

import gzip
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import DATA_PROCESSED_DIR, DATA_RAW_DIR, PAISES
from src.projecao import (
    _derivados,
    _insumos,
    calibracao,
    n_estrela_serie,
    projetar,
    trajetoria_tfr,
)

CACHE = DATA_RAW_DIR / "_cache"
CODIGOS = list(PAISES.keys())


def _indicadores(variantes=None):
    cols = ["ISO3_code", "Variant", "Time", "TPopulation1July", "NetMigrations"]
    partes = []
    arq = "demographic_indicators.csv.gz" if variantes is None else "other_variants.csv.gz"
    with gzip.open(CACHE / arq, "rt", encoding="utf-8-sig") as f:
        for ch in pd.read_csv(f, usecols=cols, chunksize=500_000, low_memory=False):
            ch = ch[ch["ISO3_code"].isin(CODIGOS)]
            if variantes:
                ch = ch[ch["Variant"].isin(variantes)]
            partes.append(ch)
    return pd.concat(partes, ignore_index=True)


def main() -> str:
    ins = _insumos()
    anos = ins["anos"]
    L = []

    ind = _indicadores()
    ind = ind[ind["Variant"] == "Medium"]

    # V1 ---------------------------------------------------------------
    L.append("## V1 — Calibração dos nascimentos c(t)\n")
    L.append("c(t) = nascimentos oficiais / (ASFR da ONU × mulheres da ONU). Perto de 1 = o modelo de fecundidade por idade é consistente com o total oficial.\n")
    L.append("| País | c mín | c máx |\n|---|---|---|")
    pior = 0.0
    for c in CODIGOS:
        cal = calibracao(c)
        pior = max(pior, float(np.abs(cal - 1).max()))
        L.append(f"| {c} | {cal.min():.4f} | {cal.max():.4f} |")
    L.append(f"\n**Maior desvio de 1 em todos os países e anos: {pior:.2%}.**\n")

    # V2 ---------------------------------------------------------------
    L.append("## V2 — Migração líquida residual vs NetMigrations (ONU)\n")
    L.append("Soma, sobre idades e sexos, do resíduo M(a,t) vs saldo migratório da ONU (milhares/ano), média 2025-2074. Se o resíduo fosse só viés do método, não acompanharia a migração.\n")
    L.append("| País | resíduo médio | ONU médio | diferença |\n|---|---|---|---|")
    for c in CODIGOS:
        M = _derivados(c)[1][:, :, 1:51].sum(axis=(0, 1)).mean()
        d = ind[(ind["ISO3_code"] == c) & (ind["Time"].between(2025, 2074))]["NetMigrations"].mean()
        L.append(f"| {c} | {M:,.0f} | {d:,.0f} | {M - d:,.0f} |")
    L.append(
        "\n**Leitura:** na maioria dos países o resíduo acompanha o saldo oficial da ONU de perto "
        "(diferença de poucas dezenas de milhares por ano ou menos), o que indica que ele é de fato "
        "migração. Divergências maiores (NGA, IND, COD: 75–125 mil/ano) **não foram investigadas**. "
        "Hipótese não testada: nesses países de população jovem e fecundidade alta, a aproximação do "
        "passo anual nas idades 0–4 pesa mais. O resíduo é aplicado em número absoluto e igual no "
        "cenário e na base, então tende a afetar mais o nível do que a diferença entre os dois.\n"
    )

    # V3 ---------------------------------------------------------------
    L.append("## V3 — N* de 2024: motor vs pipeline de produção\n")
    ref = pd.read_csv(DATA_PROCESSED_DIR / "n_index_2024.csv").set_index("codigo")
    L.append("| País | N* produção | N* motor | dif. relativa |\n|---|---|---|---|")
    max_dif = 0.0
    for c in CODIGOS:
        if c not in ref.index:
            continue
        s = n_estrela_serie(projetar(c))
        v = float(s["n_estrela"][0])
        r = float(ref.loc[c, "n_estrela"])
        max_dif = max(max_dif, abs(v / r - 1))
        L.append(f"| {c} | {r:.4f} | {v:.4f} | {v / r - 1:+.2%} |")
    L.append(f"\n**Maior diferença relativa: {max_dif:.2%}.**\n")

    # V4 ---------------------------------------------------------------
    L.append("## V4 — Sem migração vs variante \"Zero migration\" da ONU (população 2074, milhares)\n")
    zm = _indicadores(variantes=["Zero migration"])
    zm = zm[zm["Time"] == 2074].set_index("ISO3_code")["TPopulation1July"]
    L.append("| País | ONU Zero migration | motor (migração=0) | dif. relativa |\n|---|---|---|---|")
    dif4 = []
    for c in CODIGOS:
        if c not in zm.index:
            continue
        v = projetar(c, migracao="zero").pop_total[2074 - 2024]
        dif4.append(abs(v / zm[c] - 1))
        L.append(f"| {c} | {zm[c]:,.0f} | {v:,.0f} | {v / zm[c] - 1:+.2%} |")
    if dif4:
        L.append(f"\n**Mediana do desvio absoluto: {np.median(dif4):.2%}; máximo: {max(dif4):.2%}.**\n")

    # V5 ---------------------------------------------------------------
    conv_path = DATA_RAW_DIR / "convergencia_un.csv"
    if conv_path.exists():
        L.append("## V5 — TFR→2,1 (rampa 25 anos), sem migração: motor de coorte vs P_eq do projeto\n")
        L.append("O P_eq atual (narayama.live) usa um método mais simples (escala de nascimentos); aqui comparamos os dois métodos. Esperam-se diferenças pequenas, não nulas.\n")
        conv = pd.read_csv(conv_path).set_index("pais_codigo")
        L.append("| País | P_eq do projeto (mi) | motor (mi) | dif. relativa |\n|---|---|---|---|")
        dif5 = []
        for c in CODIGOS:
            if c not in conv.index:
                continue
            res = projetar(c, trajetoria_tfr(c, 2.1), migracao="zero")
            v = res.pop_total[2074 - 2024] / 1000.0
            r = float(conv.loc[c, "p_eq"])
            dif5.append(abs(v / r - 1))
            L.append(f"| {c} | {r:,.1f} | {v:,.1f} | {v / r - 1:+.2%} |")
        if dif5:
            L.append(f"\n**Mediana do desvio absoluto: {np.median(dif5):.2%}; máximo: {max(dif5):.2%}.**\n")
            L.append(
                "**Leitura:** o motor de coorte dá populações maiores que o método antigo na maioria dos "
                "países (e menores em NGA, COD, ETH, EGY). Hipótese não testada isoladamente: o método "
                "antigo escala o total de nascimentos sem modelar a estrutura etária das mulheres (efeito "
                "de eco de coortes grandes ou pequenas) e mantém os óbitos fixos. Se a diferença importar "
                "para o narayama.live, vale decidir se o P_eq público passa a usar este motor.\n"
            )

    texto = "# Validação do motor de projeção por coorte\n\nGerado por `scripts/validar_projecao.py`.\n\n" + "\n".join(L)
    saida = Path(__file__).resolve().parent.parent / "docs" / "validacao_projecao.md"
    saida.write_text(texto, encoding="utf-8")
    return texto


if __name__ == "__main__":
    main()
    print("ok -> docs/validacao_projecao.md")
