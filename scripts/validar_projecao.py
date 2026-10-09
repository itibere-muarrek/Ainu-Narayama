"""
Validação do motor de projeção por coorte (src/projecao.py).

Com a TFR da própria ONU o modelo reproduz a projeção média por construção;
por isso este script mede o que NÃO é trivial:

  V1  Calibração c(t) dos nascimentos (modelo ASFR×mulheres vs total oficial).
  V2  Migração líquida residual (soma sobre as idades) vs NetMigrations da ONU.
      ATENÇÃO: W_INFANTIL foi calibrado contra este mesmo dado, então V2 não é
      teste independente para a idade 0 (V4 é).
  V3  N* de 2024 recalculado pelo motor vs data/processed/n_index_2024.csv
      (integração com o pipeline de produção).
  V4  Cenário sem migração vs variante "Zero migration" da ONU (pop. 2074).
      Teste independente da calibração do passo anual.
  V5  Cenário TFR→2,1 sem migração vs P_eq do projeto
      (data/raw/convergencia_un.csv; método antigo = escala de nascimentos).
  V6  Teste da hipótese do "eco": o mesmo cenário de V5, mas com as mulheres do
      cenário-base como exposição à fecundidade (efeito de eco desligado).

Uso: python scripts/validar_projecao.py   (precisa dos caches em data/raw/_cache)
Escreve docs/validacao_projecao.md e docs/validacao_projecao.json (este último
alimenta os números exibidos na página de simulação).
"""

import gzip
import json
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import DATA_PROCESSED_DIR, DATA_RAW_DIR, PAISES
from src.projecao import (
    W_INFANTIL,
    _derivados,
    calibracao,
    n_estrela_serie,
    projetar,
    trajetoria_tfr,
)

CACHE = DATA_RAW_DIR / "_cache"
DOCS = Path(__file__).resolve().parent.parent / "docs"
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


def _pct(x: float) -> str:
    return f"{x:.2%}"


def main() -> str:
    L = []
    J = {"gerado_em": date.today().isoformat(), "w_infantil": W_INFANTIL}

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
    L.append(f"\n**Maior desvio de 1 em todos os países e anos: {_pct(pior)}.**\n")
    J["v1_max_desvio"] = pior

    # V2 ---------------------------------------------------------------
    L.append("## V2 — Migração líquida residual vs NetMigrations (ONU)\n")
    L.append(
        "Soma, sobre idades e sexos, do resíduo M(a,t) vs saldo migratório da ONU (milhares/ano), média "
        f"2025-2074. **Não é teste independente para a idade 0:** a fração de mortalidade infantil "
        f"W_INFANTIL = {W_INFANTIL} foi calibrada (grade 0,15–0,75) para minimizar justamente esta diferença.\n"
    )
    L.append("| País | resíduo médio | ONU médio | diferença |\n|---|---|---|---|")
    difs2 = {}
    for c in CODIGOS:
        M = _derivados(c)[1][:, :, 1:51].sum(axis=(0, 1)).mean()
        d = ind[(ind["ISO3_code"] == c) & (ind["Time"].between(2025, 2074))]["NetMigrations"].mean()
        difs2[c] = M - d
        L.append(f"| {c} | {M:,.0f} | {d:,.0f} | {M - d:,.0f} |")
    a2 = np.abs(np.array(list(difs2.values())))
    pior2 = max(difs2, key=lambda k: abs(difs2[k]))
    L.append(
        f"\n**Mediana do desvio absoluto: {np.median(a2):.1f} mil/ano; máximo: {a2.max():.0f} mil/ano ({pior2}).** "
        "Antes do ajuste infantil o máximo era 124 mil/ano (NGA), concentrado na idade 1: "
        "os óbitos de idade 0 do ano-calendário incluem recém-nascidos que ainda não existiam em "
        "1º de julho, e a coorte presente em julho enfrenta só uma fração dessa mortalidade. "
        "O resíduo é aplicado em número absoluto e igual no cenário e na base, então tende a "
        "afetar mais o nível do que a diferença entre os dois.\n"
    )
    J["v2_mediana_mil_ano"] = float(np.median(a2))
    J["v2_max_mil_ano"] = float(a2.max())

    # V3 ---------------------------------------------------------------
    L.append("## V3 — N* de 2024: motor vs pipeline de produção\n")
    ref = pd.read_csv(DATA_PROCESSED_DIR / "n_index_2024.csv").set_index("codigo")
    L.append("| País | N* produção | N* motor | dif. relativa |\n|---|---|---|---|")
    max_dif = 0.0
    for c in CODIGOS:
        if c not in ref.index:
            continue
        v = float(n_estrela_serie(projetar(c))["n_estrela"][0])
        r = float(ref.loc[c, "n_estrela"])
        max_dif = max(max_dif, abs(v / r - 1))
        L.append(f"| {c} | {r:.4f} | {v:.4f} | {v / r - 1:+.2%} |")
    L.append(f"\n**Maior diferença relativa: {_pct(max_dif)}.**\n")
    J["v3_max_dif"] = max_dif

    # V4 ---------------------------------------------------------------
    L.append("## V4 — Sem migração vs variante \"Zero migration\" da ONU (população 2074, milhares)\n")
    L.append("Teste independente: nenhum parâmetro do motor foi ajustado a este dado.\n")
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
    L.append(f"\n**Mediana do desvio absoluto: {_pct(np.median(dif4))}; máximo: {_pct(max(dif4))}.**\n")
    J["v4_mediana"], J["v4_max"] = float(np.median(dif4)), float(max(dif4))

    # V5 e V6 ----------------------------------------------------------
    conv_path = DATA_RAW_DIR / "convergencia_un.csv"
    if conv_path.exists():
        conv = pd.read_csv(conv_path).set_index("pais_codigo")
        L.append("## V5 e V6 — TFR→2,1 (rampa de 25 anos), sem migração: motor vs P_eq do projeto\n")
        L.append(
            "O P_eq atual (narayama.live) usa um método mais simples: escala o total de nascimentos pela razão "
            "entre TFRs e mantém os óbitos da ONU, sem modelar a estrutura etária das mulheres. "
            "**V5** compara com o motor de coorte completo; **V6** repete o motor com as mulheres do "
            "cenário-base como exposição (efeito de eco desligado), para testar a hipótese de que a "
            "diferença vem do eco.\n"
        )
        L.append("| País | P_eq do projeto (mi) | V5 motor (mi) | V5 dif. | V6 sem eco (mi) | V6 dif. |\n|---|---|---|---|---|---|")
        d5, d6 = [], []
        for c in CODIGOS:
            if c not in conv.index:
                continue
            base0 = projetar(c, migracao="zero")
            alvo = trajetoria_tfr(c, 2.1)
            v5 = projetar(c, alvo, migracao="zero").pop_total[50] / 1000.0
            v6 = projetar(c, alvo, migracao="zero", mulheres_ref=base0.pop[1]).pop_total[50] / 1000.0
            r = float(conv.loc[c, "p_eq"])
            d5.append(abs(v5 / r - 1))
            d6.append(abs(v6 / r - 1))
            L.append(f"| {c} | {r:,.1f} | {v5:,.1f} | {v5 / r - 1:+.2%} | {v6:,.1f} | {v6 / r - 1:+.2%} |")
        L.append(
            f"\n**V5 (com eco): mediana {_pct(np.median(d5))}, máximo {_pct(max(d5))}. "
            f"V6 (sem eco): mediana {_pct(np.median(d6))}, máximo {_pct(max(d6))}.**\n"
        )
        if np.median(d6) < np.median(d5) / 2:
            L.append(
                "**Leitura:** desligar o eco aproxima o motor do método antigo (a mediana do desvio cai "
                "mais da metade), o que **confirma** que a diferença vem do efeito de eco: no método "
                "novo os nascimentos de hoje mudam o número de mulheres em idade fértil 25 anos depois. "
                "O método antigo não captura isso (subestima o efeito quando a TFR sobe de um nível "
                "baixo; superestima quando cai de um nível alto). O motor de coorte é o mais completo, "
                "mas o P_eq público do narayama.live **não foi alterado**: trocar de método muda números "
                "publicados e é decisão do autor.\n"
            )
        else:
            L.append(
                "**Leitura:** desligar o eco **não** explica a maior parte da diferença, então a hipótese "
                "do eco não se sustenta sozinha; a origem da diferença segue em aberto.\n"
            )
        J["v5_mediana"], J["v5_max"] = float(np.median(d5)), float(max(d5))
        J["v6_mediana"], J["v6_max"] = float(np.median(d6)), float(max(d6))

    texto = "# Validação do motor de projeção por coorte\n\nGerado por `scripts/validar_projecao.py`.\n\n" + "\n".join(L)
    (DOCS / "validacao_projecao.md").write_text(texto, encoding="utf-8")
    (DOCS / "validacao_projecao.json").write_text(json.dumps(J, indent=1), encoding="utf-8")
    return texto


if __name__ == "__main__":
    main()
    print("ok -> docs/validacao_projecao.md e .json")
