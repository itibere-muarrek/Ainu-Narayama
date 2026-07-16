"""
Constrói data/raw/convergencia_un.csv — P_2.1 e P_eq (Tabela
Geracional, "tempo até estabilização populacional se a TFR convergir
a 2,1"), a partir do cenário oficial "Instant replacement zero
migration" da UN World Population Prospects 2024 Revision.

Origem da formalização: documento do autor "tabela geracional -
formula.docx" (2026-07-16), que define três conceitos:
  - P_E(t): população endógena (só nascimentos - óbitos, sem migração).
  - P_2.1 = P_E(t_c), onde t_c é o instante em que TFR(t_c) = 2,1 pela
    primeira vez — a população quando a fecundidade volta ao nível de
    reposição, mas a estrutura etária ainda não estabilizou.
  - P_eq = P_E(t_c + 25) — a população ~1 geração depois, mantendo
    TFR=2,1 o período todo. O tamanho populacional sustentável real.

Por que usar o cenário "Instant replacement zero migration" da UN WPP
em vez de projetar isso nós mesmos: essa variante já é exatamente
P_E com TFR fixada em ~2,1 (nível de reposição, tecnicamente NRR=1,
não travado no literal "2,1" mas equivalente) e migração líquida
zero — calculada pelos demógrafos da ONU com fecundidade por idade e
tábua de mortalidade reais, dado que este projeto não tem. Usar dado
real aqui, em vez de uma trajetória de nascimentos/óbitos inventada
por nós, é o mesmo princípio de rigor já aplicado em todo o resto do
pipeline (ver docs/definitions.md, seção 6 — Protocolo de
Falseabilidade).

Simplificação explícita, documentada em docs/definitions.md (seção
8-B): esse cenário assume que a TFR salta para o nível de reposição
IMEDIATAMENTE (T_2.1 = 0), não gradualmente — não é "quando a
sociedade realmente vai atingir TFR=2,1" (T_2.1 gradual/realista,
que dependeria de um cenário de convergência ainda não definido),
é "que tamanho a população teria SE a TFR já estivesse em reposição
hoje". Um piso demográfico ilustrativo, não uma previsão.

t_c = 2024 (ano-âncora do projeto, mesmo ano de n_index_2024.csv);
t_c + 25 = 2049.

Fonte: WPP2024_Demographic_Indicators_OtherVariants.csv.gz (mesma
pasta CSV_FILES da UN WPP usada pelos outros scripts de coleta —
esse arquivo cobre todas as variantes "especiais" da revisão 2024:
Instant replacement, Constant fertility, Momentum, Zero migration,
etc., não só a variante Medium).

Uso:
    python scripts/build_convergencia_raw.py [--output CAMINHO]

Sem --output, escreve em data/raw/convergencia_un.csv.
"""

import argparse
import gzip
import shutil
import sys
import urllib.request
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import DATA_RAW_DIR, PAISES

CACHE_DIR = DATA_RAW_DIR / "_cache"

URL_OUTRAS_VARIANTES = (
    "https://population.un.org/wpp/assets/Excel%20Files/"
    "1_Indicator%20(Standard)/CSV_FILES/"
    "WPP2024_Demographic_Indicators_OtherVariants.csv.gz"
)

VARIANTE = "Instant replacement zero migration"
ANO_CONVERGENCIA = 2024  # t_c (ano-âncora do projeto)
ANO_EQUILIBRIO = ANO_CONVERGENCIA + 25  # t_c + 25

CODIGOS_ISO3 = list(PAISES.keys())
USECOLS = ["ISO3_code", "Variant", "Time", "TPopulation1July", "TFR"]


def _baixar_se_necessario() -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    destino = CACHE_DIR / "other_variants.csv.gz"
    if destino.exists():
        print(f"[cache] {destino.name} já existe, pulando download.")
        return destino
    print(f"[download] {URL_OUTRAS_VARIANTES}")
    req = urllib.request.Request(URL_OUTRAS_VARIANTES, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(destino, "wb") as f:
        shutil.copyfileobj(resp, f)
    print(f"[download] salvo em {destino} ({destino.stat().st_size / 1e6:.1f} MB)")
    return destino


def construir(caminho_saida: Path) -> pd.DataFrame:
    caminho_gz = _baixar_se_necessario()

    partes = []
    with gzip.open(caminho_gz, "rt", encoding="utf-8-sig") as f:
        for chunk in pd.read_csv(f, usecols=USECOLS, chunksize=1_000_000, low_memory=False):
            filtrado = chunk[
                chunk["ISO3_code"].isin(CODIGOS_ISO3)
                & (chunk["Variant"] == VARIANTE)
                & chunk["Time"].isin([ANO_CONVERGENCIA, ANO_EQUILIBRIO])
            ]
            if len(filtrado):
                partes.append(filtrado)
    if not partes:
        raise RuntimeError(f"Nenhuma linha encontrada para a variante '{VARIANTE}'")
    dados = pd.concat(partes, ignore_index=True)

    linhas = []
    for codigo in CODIGOS_ISO3:
        linha_2_1 = dados[(dados["ISO3_code"] == codigo) & (dados["Time"] == ANO_CONVERGENCIA)]
        linha_eq = dados[(dados["ISO3_code"] == codigo) & (dados["Time"] == ANO_EQUILIBRIO)]
        if linha_2_1.empty or linha_eq.empty:
            print(f"[aviso] sem dado de convergência para {codigo}, pulando.")
            continue

        linhas.append(
            {
                "pais_codigo": codigo,
                "ano_2_1": ANO_CONVERGENCIA,
                "p_2_1": round(linha_2_1.iloc[0]["TPopulation1July"] / 1000, 4),
                "tfr_2_1": round(linha_2_1.iloc[0]["TFR"], 4),
                "ano_eq": ANO_EQUILIBRIO,
                "p_eq": round(linha_eq.iloc[0]["TPopulation1July"] / 1000, 4),
                "tfr_eq": round(linha_eq.iloc[0]["TFR"], 4),
            }
        )

    resultado = pd.DataFrame(linhas).sort_values("pais_codigo").reset_index(drop=True)
    resultado.to_csv(caminho_saida, index=False)
    print(f"[ok] {len(resultado)} linhas escritas em {caminho_saida}")
    return resultado


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DATA_RAW_DIR / "convergencia_un.csv",
        help="Caminho de saída (padrão: data/raw/convergencia_un.csv)",
    )
    args = parser.parse_args()
    construir(args.output)
