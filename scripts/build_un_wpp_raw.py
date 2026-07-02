"""
Reconstrói data/raw/un_wpp.csv (colunas pop_base/pop_topo) a partir dos
dados de população por idade simples da UN World Population Prospects
2024 Revision.

Por que este script existe: até 2026-07-04 esse passo era feito ad hoc em
scripts de scratchpad de sessão, que não ficavam salvos no repositório —
cada recalibração de corte etário exigia refazer o download/processamento
do zero, sem nada reprodutível. Este script substitui isso.

Fonte: population.un.org/wpp/downloads — CSVs "Population by Single Age",
variante "Medium":
  WPP2024_PopulationBySingleAgeSex_Medium_1950-2023.csv.gz (cobre 1999)
  WPP2024_PopulationBySingleAgeSex_Medium_2024-2100.csv.gz (cobre 2024)

A API do UN WPP Data Portal (population.un.org/dataportalapi) foi avaliada
como alternativa mais leve, mas seu endpoint de dados retorna 401
(exige token Bearer não documentado publicamente) — descartada em favor do
download direto dos CSVs bulk, testado e funcional em 2026-07-04.

Os cortes etários (pop_base_max/pop_topo_min) usados vêm de
src.config.PAISES (nunca hardcoded aqui) — refletem a composição ponderada
de perfis da Seção 5.2 (ver COMPOSICAO_PERFIL_POR_PAIS em src/config.py).

pop_total, nascimentos, mortes e tfr NÃO dependem do corte etário — são
preservados do data/raw/un_wpp.csv existente, não recalculados aqui.

Uso:
    python scripts/build_un_wpp_raw.py [--output CAMINHO]

Sem --output, escreve em data/raw/un_wpp_new.csv (não sobrescreve o
arquivo em produção automaticamente — diferencie manualmente antes de
substituir data/raw/un_wpp.csv).
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

URLS = {
    "hist": (
        "https://population.un.org/wpp/assets/Excel%20Files/"
        "1_Indicator%20(Standard)/CSV_FILES/"
        "WPP2024_PopulationBySingleAgeSex_Medium_1950-2023.csv.gz"
    ),
    "proj": (
        "https://population.un.org/wpp/assets/Excel%20Files/"
        "1_Indicator%20(Standard)/CSV_FILES/"
        "WPP2024_PopulationBySingleAgeSex_Medium_2024-2100.csv.gz"
    ),
}

ANOS = {"hist": 1999, "proj": 2024}
CODIGOS_ISO3 = list(PAISES.keys())
USECOLS = ["ISO3_code", "Variant", "Time", "AgeGrpStart", "PopTotal"]


def _baixar_se_necessario(nome: str, url: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    destino = CACHE_DIR / f"{nome}.csv.gz"
    if destino.exists():
        print(f"[cache] {destino.name} já existe, pulando download.")
        return destino
    print(f"[download] {url}")
    with urllib.request.urlopen(url) as resp, open(destino, "wb") as f:
        shutil.copyfileobj(resp, f)
    print(f"[download] salvo em {destino} ({destino.stat().st_size / 1e6:.1f} MB)")
    return destino


def _extrair_populacao_por_idade(caminho_gz: Path, ano: int) -> pd.DataFrame:
    """Lê o CSV gzipado em chunks, filtrando só os 28 países e o ano alvo."""
    partes = []
    with gzip.open(caminho_gz, "rt", encoding="utf-8-sig") as f:
        for chunk in pd.read_csv(f, usecols=USECOLS, chunksize=500_000, low_memory=False):
            filtrado = chunk[
                chunk["ISO3_code"].isin(CODIGOS_ISO3)
                & (chunk["Time"] == ano)
                & (chunk["Variant"] == "Medium")
            ]
            if len(filtrado):
                partes.append(filtrado)
    if not partes:
        raise RuntimeError(f"Nenhuma linha encontrada para o ano {ano} em {caminho_gz.name}")
    return pd.concat(partes, ignore_index=True)


def _pop_base_topo(populacao_idade: pd.DataFrame, codigo: str) -> tuple:
    """Soma população (em milhões) de 0..pop_base_max e pop_topo_min..100+."""
    pais_info = PAISES[codigo]
    base_max = pais_info["pop_base_max"]
    topo_min = pais_info["pop_topo_min"]

    dados_pais = populacao_idade[populacao_idade["ISO3_code"] == codigo]
    pop_base = dados_pais[dados_pais["AgeGrpStart"] <= base_max]["PopTotal"].sum() / 1000
    pop_topo = dados_pais[dados_pais["AgeGrpStart"] >= topo_min]["PopTotal"].sum() / 1000
    return round(pop_base, 4), round(pop_topo, 4)


def construir(caminho_saida: Path) -> pd.DataFrame:
    caminho_hist = _baixar_se_necessario("hist", URLS["hist"])
    caminho_proj = _baixar_se_necessario("proj", URLS["proj"])

    pop_1999 = _extrair_populacao_por_idade(caminho_hist, ANOS["hist"])
    pop_2024 = _extrair_populacao_por_idade(caminho_proj, ANOS["proj"])

    atual = pd.read_csv(DATA_RAW_DIR / "un_wpp.csv")

    linhas = []
    for _, linha_atual in atual.iterrows():
        codigo = linha_atual["pais_codigo"]
        ano = int(linha_atual["ano"])
        populacao_idade = pop_1999 if ano == ANOS["hist"] else pop_2024
        pop_base, pop_topo = _pop_base_topo(populacao_idade, codigo)
        linhas.append(
            {
                "pais_codigo": codigo,
                "ano": ano,
                "pop_total": linha_atual["pop_total"],
                "pop_base": pop_base,
                "pop_topo": pop_topo,
                "nascimentos": linha_atual["nascimentos"],
                "mortes": linha_atual["mortes"],
                "tfr": linha_atual["tfr"],
            }
        )

    resultado = pd.DataFrame(linhas)
    resultado.to_csv(caminho_saida, index=False)
    print(f"[ok] {len(resultado)} linhas escritas em {caminho_saida}")
    return resultado


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DATA_RAW_DIR / "un_wpp_new.csv",
        help="Caminho de saída (padrão: data/raw/un_wpp_new.csv, não sobrescreve o arquivo em produção)",
    )
    args = parser.parse_args()
    construir(args.output)
