"""Testes F1–F9 do PQDF-N* (EcoPol V1_1, Anexo 9-B) que é possível executar com os dados do repositório.

Executa F1 (reprodutibilidade), F4 (robustez classificatória) e a parte numérica de F5 (peso de cada ajuste); registra por que
os demais (F2, F3, F6, F7, F8, F9) NÃO foram executados. Nada aqui foi pré-registrado: as sensibilidades de F4 foram definidas
junto com a execução e isso consta no resultado. Grava docs/testes_pqdf_n_estrela.json e .md.

Uso: python scripts/testes_pqdf.py
"""
from __future__ import annotations

import json
import math
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from src.config import (  # noqa: E402
    AJUSTES_FALSEABILIDADE_POR_PAIS as AJ,
    CENARIOS_PQDF,
    COMPOSICAO_PERFIL_POR_PAIS,
    cortes_por_composicao,
)
from src.data_pipeline import executar_pipeline_completo  # noqa: E402
from src.indices import classificar_zona_5  # noqa: E402

ANO = 2024
raw = pd.read_csv(RAIZ / "data" / "raw" / "un_wpp.csv").set_index(["pais_codigo", "ano"])
snap = pd.read_csv(RAIZ / "data" / "processed" / "n_index_2024.csv").set_index("codigo")
paises = list(snap.index)
res: dict = {"data": date.today().isoformat(), "ano_referencia": ANO, "aviso": (
    "Sensibilidades de F4 e leitura de F5 definidas junto com a execução, não pré-registradas: valem como diagnóstico, "
    "não como confirmação nem refutação formal. Resultados de F1–F9 não executados constam como tal.")}

# ---------------------------------------------------------------- F1 reprodutibilidade
# Recalculo independente (sem src.*) a partir da tabela data/raw/un_wpp.csv, comparado ao pipeline sem arredondamento e ao CSV.
maior_dif_pipeline, maior_dif_csv = 0.0, 0.0
for c in paises:
    a, b = raw.loc[(c, ANO)], raw.loc[(c, ANO - 25)]
    ngii = (a.pop_base / a.pop_topo) * (a.nascimentos / a.mortes)
    n_obs = math.sqrt(ngii * (a.tfr / b.tfr))
    maior_dif_csv = max(maior_dif_csv, abs(n_obs - snap.loc[c, "n_estrela"]))
n1 = executar_pipeline_completo(ANO).set_index("codigo")
n2 = executar_pipeline_completo(ANO).set_index("codigo")
maior_dif_pipeline = float((n1.n_estrela - n2.n_estrela).abs().max())
res["F1"] = {
    "teste": "Reprodutibilidade",
    "criterio": "diferença numérica > 1e-8 ou artefato não reconstruível",
    "dif_max_duas_execucoes": maior_dif_pipeline,
    "dif_max_recalculo_independente_vs_csv": maior_dif_csv,
    "tolerancia_do_csv": "5e-5 (o CSV publica 4 casas decimais)",
    "resultado": "passa" if maior_dif_pipeline <= 1e-8 and maior_dif_csv <= 5e-5 else "falha",
    "limite": "Parte da tabela data/raw/un_wpp.csv (derivada do WPP 2024); não refaz o download dos arquivos de ~200 MB da ONU.",
}

# ---------------------------------------------------------------- F4 robustez classificatória
z = np.load(RAIZ / "data" / "processed" / "projecao_inputs.npz", allow_pickle=True)
anos_npz = list(z["anos"])
codigos_npz = [str(x) for x in z["codigos"]]


def n_com_cortes(c: str, deslocamento: int) -> float | None:
    """N*_Obs com os cortes etários do país deslocados em `deslocamento` anos (Pop_Base e Pop_Topo)."""
    pop = z[f"{c}_pop"].sum(axis=0)  # [idade, ano]
    k = anos_npz.index(ANO)
    base_max, topo_min = cortes_por_composicao(COMPOSICAO_PERFIL_POR_PAIS[c])
    base = pop[0 : base_max + deslocamento + 1, k].sum()
    topo = pop[topo_min + deslocamento :, k].sum()
    a = raw.loc[(c, ANO)]
    return math.sqrt((base / topo) * (a.nascimentos / a.mortes) * snap.loc[c, "fator_geracional"])


sens: dict[str, dict] = {}
base_obs = snap["n_estrela"]
zona_obs = snap["status"]


def avaliar(nome: str, serie: pd.Series) -> None:
    zonas = serie.map(lambda n: classificar_zona_5(n * n))
    sens[nome] = {
        "spearman": round(float(base_obs.rank().corr(serie.rank())), 4),  # Spearman = Pearson dos postos
        "concordancia_de_zonas": round(float((zonas == zona_obs).mean()), 4),
        "paises_que_mudam_de_zona": sorted(zonas.index[zonas != zona_obs].tolist()),
    }


for d in (-1, 1):
    avaliar(f"cortes etários {d:+d} ano", pd.Series({c: n_com_cortes(c, d) for c in paises}))
for suf, chave in CENARIOS_PQDF.items():
    avaliar(f"cenário {chave} (N*_{suf})", snap[f"n_estrela_{suf}"])
avaliar("calibração histórica combinada (N*_cal)", snap["n_estrela_cal"])

fica_ok = {
    k: v["spearman"] >= 0.85 and v["concordancia_de_zonas"] >= 0.80 for k, v in sens.items()
}
res["F4"] = {
    "teste": "Robustez classificatória",
    "criterio": "Spearman < 0,85 ou concordância de zonas < 80% nas sensibilidades definidas",
    "sensibilidades": sens,
    "atende_o_criterio": fica_ok,
    "resultado": "passa em todas" if all(fica_ok.values()) else "falha em: " + "; ".join(k for k, v in fica_ok.items() if not v),
    "decisao_prevista_pelo_protocolo": "Publicar zonas como provisórias." if not all(fica_ok.values()) else "—",
}

# ---------------------------------------------------------------- F5 (parte numérica)
reducao = {}
for suf, chave in CENARIOS_PQDF.items():
    reducao[chave] = {
        "paises_que_mudam_de_zona": int((snap[f"n_estrela_{suf}"].map(lambda n: classificar_zona_5(n * n)) != zona_obs).sum()),
        "reducao_mediana_do_N*_%": round(float(((1 - snap[f"n_estrela_{suf}"] / base_obs) * 100).median()), 2),
    }
res["F5"] = {
    "teste": "Migração e inércia",
    "criterio": "mudanças extensas de zona, ou ajuste de inércia redundante com Pop_Base/Pop_Topo (o protocolo não fixa limiar numérico)",
    "por_ajuste_isolado": reducao,
    "resultado": "indeterminado",
    "motivo": "O limiar de 'extensas' não está definido e o teste de redundância da inércia exige o estimador do ajuste (modelo com e sem "
              "o tamanho da coorte reprodutiva), que o repositório não tem: os ajustes são valores calibrados, não estimados.",
}

# ---------------------------------------------------------------- não executados
res["nao_executados"] = {
    "F2": "Validade convergente: exige especificações pré-registradas e medidas demográficas externas definidas; não há registro prévio.",
    "F3": "Valor incremental: exige variável-alvo e previsão fora da amostra com benchmarks (TFR, razão de dependência); não definidos.",
    "F6": "Políticas e conjuntura: exige desenho de efeito causal (diferença-em-diferenças etc.) por política; não há estimativas.",
    "F7": "NTAI/Farol: o Farol depende do Fator_Alocativo (NTA), ainda não integrado.",
    "F8": "IES/EIS: o índice não está implementado neste repositório.",
    "F9": "Replicação externa: precisa de equipe independente; não é executável pelo autor nem por este sistema.",
}

(RAIZ / "docs" / "testes_pqdf_n_estrela.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")

md = [f"# Testes F1–F9 do PQDF-N* — execução de {res['data']}", "", f"> {res['aviso']}", "",
      "| Teste | Situação | Resultado |", "|---|---|---|",
      f"| F1 Reprodutibilidade | executado | {res['F1']['resultado']} (dif. entre execuções {maior_dif_pipeline:.1e}; recálculo independente × CSV {maior_dif_csv:.1e}) |",
      f"| F4 Robustez classificatória | executado | {res['F4']['resultado']} |",
      "| F5 Migração e inércia | parcial | indeterminado (ver motivo) |"]
for k, v in res["nao_executados"].items():
    md.append(f"| {k} | não executado | {v} |")
md += ["", "## F4 — sensibilidades", "", "| Sensibilidade | Spearman | Concordância de zonas | Países que mudam de zona |", "|---|---|---|---|"]
for k, v in sens.items():
    md.append(f"| {k} | {v['spearman']:.3f} | {v['concordancia_de_zonas']*100:.0f}% | {', '.join(v['paises_que_mudam_de_zona']) or '—'} |")
md += ["", f"Decisão prevista pelo protocolo quando F4 falha: {res['F4']['decisao_prevista_pelo_protocolo']}", "",
       "## F5 — cada ajuste isolado", "", "| Ajuste | Países que mudam de zona | Redução mediana do N* |", "|---|---|---|"]
for k, v in reducao.items():
    md.append(f"| {k} | {v['paises_que_mudam_de_zona']} | {v['reducao_mediana_do_N*_%']}% |")
md += ["", f"Motivo da indeterminação: {res['F5']['motivo']}", ""]
(RAIZ / "docs" / "testes_pqdf_n_estrela.md").write_text("\n".join(md), encoding="utf-8")
print("\n".join(md))
