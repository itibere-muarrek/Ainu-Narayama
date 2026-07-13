"""
Constrói data/raw/migracao_un.csv com o percentual de população
imigrante (estoque de migrantes internacionais / população total) por
país, a partir da UN International Migrant Stock 2024.

Por que este script existe: é o primeiro passo do "bot de coleta de
dados" (2026-07-13) — automatizar as fontes que já têm dado público
sem login, começando pelo ajuste "migratório" do Protocolo de
Falseabilidade quantitativo (ver src.config.AJUSTES_FALSEABILIDADE_POR_PAIS).

IMPORTANTE — isto é um PROXY, não a métrica exata: a definição do
ajuste migratório em docs/definitions.md (seção 6) é "% de nascimentos
de mães imigrantes nos últimos 10 anos" — um dado bem mais específico
do que "% da população total que é imigrante" (o que a UN Migrant
Stock mede). Não existe fonte pública estruturada para a métrica exata
nos 28 países; este script traz o proxy mais próximo disponível sem
necessidade de conta/login. Decisão de usar este proxy pra recalibrar
AJUSTES_FALSEABILIDADE_POR_PAIS fica com o usuário — este script só
coleta o dado, não substitui nada automaticamente.

Fonte: UN Population Division, International Migrant Stock 2024
(population.un.org/development/desa/pd) — arquivo "by sex and
destination", Tabela 3 ("International migrant stock as a percentage
of the total population by sex and by region, country or area of
destination, 1990-2024"). O servidor exige um User-Agent de navegador
(requisições sem esse cabeçalho retornam 403).

O "Location code" da planilha é o código numérico ISO 3166-1 (ex.:
Brasil=76, Japão=392) — mapeado aqui para os códigos ISO3 usados no
projeto (BRA, JPN etc.).

Uso:
    python scripts/build_migracao_raw.py [--output CAMINHO]

Sem --output, escreve em data/raw/migracao_un.csv.
"""

import argparse
import shutil
import sys
import urllib.request
from pathlib import Path

import openpyxl
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import DATA_RAW_DIR, PAISES

CACHE_DIR = DATA_RAW_DIR / "_cache"

URL_MIGRANT_STOCK = (
    "https://www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/"
    "files/undesa_pd_2024_ims_stock_by_sex_and_destination.xlsx"
)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

ANO = 2024
COLUNA_ANO_2024 = 12  # índice 0-based na Tabela 3: 0=Index,1=Nome,2=Coverage,3=DataType,4=LocationCode,5..12=1990..2024

# Código numérico ISO 3166-1 por país (chave = "Location code" da planilha).
CODIGO_ISO_NUMERICO = {
    "NGA": 566, "ETH": 231, "COD": 180, "VNM": 704, "IND": 356, "IDN": 360,
    "IRN": 364, "SAU": 682, "MAR": 504, "EGY": 818, "THA": 764, "MEX": 484,
    "POL": 616, "BRA": 76, "USA": 840, "CHN": 156, "FRA": 250, "ARG": 32,
    "CHL": 152, "SWE": 752, "GBR": 826, "AUS": 36, "ZAF": 710, "JPN": 392,
    "DEU": 276, "ITA": 380, "KOR": 410, "RUS": 643,
}


def _baixar_se_necessario() -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    destino = CACHE_DIR / "migrant_stock_destination_2024.xlsx"
    if destino.exists():
        print(f"[cache] {destino.name} já existe, pulando download.")
        return destino

    print(f"[download] {URL_MIGRANT_STOCK}")
    req = urllib.request.Request(URL_MIGRANT_STOCK, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as resp, open(destino, "wb") as f:
        shutil.copyfileobj(resp, f)
    print(f"[download] salvo em {destino} ({destino.stat().st_size / 1e3:.0f} KB)")
    return destino


def construir(caminho_saida: Path) -> pd.DataFrame:
    caminho_xlsx = _baixar_se_necessario()

    wb = openpyxl.load_workbook(caminho_xlsx, read_only=True, data_only=True)
    ws = wb["Table 3"]

    numerico_para_codigo = {v: k for k, v in CODIGO_ISO_NUMERICO.items()}
    encontrados = {}
    for row in ws.iter_rows(min_row=12, values_only=True):
        location_code = row[4]
        if location_code in numerico_para_codigo:
            codigo = numerico_para_codigo[location_code]
            encontrados[codigo] = row[COLUNA_ANO_2024]

    faltando = set(CODIGO_ISO_NUMERICO) - set(encontrados)
    if faltando:
        raise RuntimeError(f"Países não encontrados na planilha: {sorted(faltando)}")

    linhas = [
        {"pais_codigo": codigo, "ano": ANO, "proporcao_migrantes_pct": round(pct, 4)}
        for codigo, pct in sorted(encontrados.items())
    ]
    resultado = pd.DataFrame(linhas)
    resultado.to_csv(caminho_saida, index=False)
    print(f"[ok] {len(resultado)} linhas escritas em {caminho_saida}")
    return resultado


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DATA_RAW_DIR / "migracao_un.csv",
        help="Caminho de saída (padrão: data/raw/migracao_un.csv)",
    )
    args = parser.parse_args()
    construir(args.output)
