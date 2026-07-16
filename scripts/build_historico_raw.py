"""
Constrói data/raw/un_wpp_historico.csv — série quinquenal de 1990 a
2024, decisão do autor de 2026-07-15 ("quinquenal para começar e
vamos refinando após validações"), para alimentar
data/processed/n_index_historico.csv (gráfico "Evolução do N*" do
ainu.systems).

Fontes (arquivos bulk da UN WPP 2024 Revision, os dois primeiros já
usados por scripts/build_un_wpp_raw.py — reaproveita o cache, sem
download extra pros anos que já estavam cobertos):
  - WPP2024_PopulationBySingleAgeSex_Medium_1950-2023.csv.gz
    (pop_base/pop_topo, anos até 2023)
  - WPP2024_PopulationBySingleAgeSex_Medium_2024-2100.csv.gz
    (idem, 2024 em diante)
  - WPP2024_Demographic_Indicators_Medium.csv.gz (pop_total,
    nascimentos, mortes, tfr — um único arquivo cobre 1950-2100,
    não precisa split histórico/projeção como o de idade simples;
    valores brutos vêm em milhares — este script já converte pra
    milhões, mesma unidade usada em data/raw/un_wpp.csv)

Anos-alvo (pontos exibidos no gráfico): 1990, 1995, 2000, 2005, 2010,
2015, 2020, 2024 — último intervalo de só 4 anos pra manter 2024
como âncora (mesmo ano do snapshot em n_index_2024.csv).

Anos extras (só para TFR, usados como "ano-25" no Fator_Geracional —
ver src.data_pipeline.executar_pipeline_historico —, nunca como
ano-alvo do próprio índice): 1965, 1970, 1975, 1980, 1985, 1999
(1990 e 1995 já são anos-alvo, não duplicados). Nessas linhas,
pop_base/pop_topo ficam vazias (NaN): o pipeline só lê a coluna tfr
do ano-25, nunca pop_base/pop_topo/nascimentos/mortes dele. Mesmo
assim, pop_total/nascimentos/mortes são preenchidos pra essas linhas
porque vêm do mesmo arquivo de indicadores, sem custo extra de
coleta — útil pra quem for auditar o dado bruto depois.

Uso:
    python scripts/build_historico_raw.py [--output CAMINHO]

Sem --output, escreve em data/raw/un_wpp_historico.csv.
"""

import argparse
import gzip
import shutil
import sys
import urllib.request
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import ANOS_ALVO_HISTORICO, DATA_RAW_DIR, PAISES

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
    "demographic_indicators": (
        "https://population.un.org/wpp/assets/Excel%20Files/"
        "1_Indicator%20(Standard)/CSV_FILES/"
        "WPP2024_Demographic_Indicators_Medium.csv.gz"
    ),
}

ANOS_ALVO = ANOS_ALVO_HISTORICO
ANOS_TFR_EXTRA = sorted({ano - 25 for ano in ANOS_ALVO} - set(ANOS_ALVO))
ANOS_TODOS = sorted(set(ANOS_ALVO) | set(ANOS_TFR_EXTRA))

CODIGOS_ISO3 = list(PAISES.keys())
USECOLS_IDADE = ["ISO3_code", "Variant", "Time", "AgeGrpStart", "PopTotal"]
USECOLS_INDICADORES = ["ISO3_code", "Variant", "Time", "TPopulation1July", "Births", "Deaths", "TFR"]


def _baixar_se_necessario(nome: str, url: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    destino = CACHE_DIR / f"{nome}.csv.gz"
    if destino.exists():
        print(f"[cache] {destino.name} já existe, pulando download.")
        return destino
    print(f"[download] {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(destino, "wb") as f:
        shutil.copyfileobj(resp, f)
    print(f"[download] salvo em {destino} ({destino.stat().st_size / 1e6:.1f} MB)")
    return destino


def _extrair_populacao_por_idade(caminho_gz: Path, anos: list) -> pd.DataFrame:
    """Lê o CSV gzipado em chunks, filtrando só os 28 países e os anos-alvo."""
    if not anos:
        return pd.DataFrame(columns=USECOLS_IDADE)
    partes = []
    with gzip.open(caminho_gz, "rt", encoding="utf-8-sig") as f:
        for chunk in pd.read_csv(f, usecols=USECOLS_IDADE, chunksize=500_000, low_memory=False):
            filtrado = chunk[
                chunk["ISO3_code"].isin(CODIGOS_ISO3)
                & chunk["Time"].isin(anos)
                & (chunk["Variant"] == "Medium")
            ]
            if len(filtrado):
                partes.append(filtrado)
    if not partes:
        return pd.DataFrame(columns=USECOLS_IDADE)
    return pd.concat(partes, ignore_index=True)


def _pop_base_topo(populacao_idade: pd.DataFrame, codigo: str, ano: int):
    """Soma população (em milhões) de 0..pop_base_max e pop_topo_min..100+."""
    pais_info = PAISES[codigo]
    base_max = pais_info["pop_base_max"]
    topo_min = pais_info["pop_topo_min"]

    dados = populacao_idade[(populacao_idade["ISO3_code"] == codigo) & (populacao_idade["Time"] == ano)]
    if dados.empty:
        return None, None
    pop_base = dados[dados["AgeGrpStart"] <= base_max]["PopTotal"].sum() / 1000
    pop_topo = dados[dados["AgeGrpStart"] >= topo_min]["PopTotal"].sum() / 1000
    return round(pop_base, 4), round(pop_topo, 4)


def _extrair_indicadores(caminho_gz: Path, anos: list) -> pd.DataFrame:
    """Lê o CSV gzipado de indicadores demográficos, filtrando países/anos."""
    partes = []
    with gzip.open(caminho_gz, "rt", encoding="utf-8-sig") as f:
        for chunk in pd.read_csv(f, usecols=USECOLS_INDICADORES, chunksize=500_000, low_memory=False):
            filtrado = chunk[
                chunk["ISO3_code"].isin(CODIGOS_ISO3)
                & chunk["Time"].isin(anos)
                & (chunk["Variant"] == "Medium")
            ]
            if len(filtrado):
                partes.append(filtrado)
    if not partes:
        raise RuntimeError(f"Nenhuma linha de indicadores encontrada para os anos {anos}")
    return pd.concat(partes, ignore_index=True)


def construir(caminho_saida: Path) -> pd.DataFrame:
    caminho_hist = _baixar_se_necessario("hist", URLS["hist"])
    caminho_proj = _baixar_se_necessario("proj", URLS["proj"])
    caminho_indicadores = _baixar_se_necessario("demographic_indicators", URLS["demographic_indicators"])

    anos_hist = [a for a in ANOS_ALVO if a <= 2023]
    anos_proj = [a for a in ANOS_ALVO if a >= 2024]

    pop_idade_hist = _extrair_populacao_por_idade(caminho_hist, anos_hist)
    pop_idade_proj = _extrair_populacao_por_idade(caminho_proj, anos_proj)

    indicadores = _extrair_indicadores(caminho_indicadores, ANOS_TODOS)

    linhas = []
    for codigo in CODIGOS_ISO3:
        for ano in ANOS_TODOS:
            linha_ind = indicadores[(indicadores["ISO3_code"] == codigo) & (indicadores["Time"] == ano)]
            if linha_ind.empty:
                print(f"[aviso] sem indicadores para {codigo} em {ano}, pulando linha.")
                continue
            linha_ind = linha_ind.iloc[0]

            pop_base = pop_topo = None
            if ano in ANOS_ALVO:
                fonte_idade = pop_idade_hist if ano <= 2023 else pop_idade_proj
                pop_base, pop_topo = _pop_base_topo(fonte_idade, codigo, ano)

            linhas.append(
                {
                    "pais_codigo": codigo,
                    "ano": ano,
                    "pop_total": round(linha_ind["TPopulation1July"] / 1000, 4),
                    "pop_base": pop_base,
                    "pop_topo": pop_topo,
                    "nascimentos": round(linha_ind["Births"] / 1000, 4),
                    "mortes": round(linha_ind["Deaths"] / 1000, 4),
                    "tfr": round(linha_ind["TFR"], 4),
                }
            )

    resultado = pd.DataFrame(linhas).sort_values(["pais_codigo", "ano"]).reset_index(drop=True)
    resultado.to_csv(caminho_saida, index=False)
    print(f"[ok] {len(resultado)} linhas escritas em {caminho_saida}")
    return resultado


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DATA_RAW_DIR / "un_wpp_historico.csv",
        help="Caminho de saída (padrão: data/raw/un_wpp_historico.csv)",
    )
    args = parser.parse_args()
    construir(args.output)
