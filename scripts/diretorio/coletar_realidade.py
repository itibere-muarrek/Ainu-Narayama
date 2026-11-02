"""Coleta o consumo observado dos 11 países na API pública do Banco Mundial (WDI) e grava realidade_wdi.json.

Só leitura. Para cada país e indicador, pega o valor mais recente não vazio (parâmetro mrnev=1) e guarda o ano, o valor e o endereço
da série. Os valores são dado observado do Banco Mundial (compilação de fontes nacionais), sem nenhum cálculo nosso.

Uso: python scripts/diretorio/coletar_realidade.py
"""
from __future__ import annotations

import json
import urllib.request
from datetime import datetime
from pathlib import Path

from testar_links import UA

ISO = ["ITA", "KOR", "JPN", "MEX", "ARG", "BRA", "USA", "IND", "NGA", "FRA", "CHN"]
SERIES = {
    "consumo_familias_pib": ("NE.CON.PRVT.ZS", "Consumo final das famílias, % do PIB"),
    "consumo_governo_pib": ("NE.CON.GOVT.ZS", "Consumo final do governo geral, % do PIB"),
    "consumo_familias_pc": ("NE.CON.PRVT.PC.KD", "Consumo final das famílias per capita, US$ constantes de 2015"),
    "pib_pc": ("NY.GDP.PCAP.KD", "PIB per capita, US$ constantes de 2015"),
}


def buscar(iso: str, codigo: str):
    u = f"https://api.worldbank.org/v2/country/{iso}/indicator/{codigo}?format=json&mrnev=1&per_page=5"
    d = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=60).read())
    if len(d) > 1 and d[1] and d[1][0].get("value") is not None:
        return {"valor": d[1][0]["value"], "ano": int(d[1][0]["date"])}
    return None


def main():
    out = {"coletado_em": datetime.now().isoformat(timespec="seconds"), "fonte": "Banco Mundial, World Development Indicators (API pública)",
           "series": {k: {"codigo": c, "descricao": desc, "url": f"https://data.worldbank.org/indicator/{c}"} for k, (c, desc) in SERIES.items()}, "paises": {}}
    for iso in ISO:
        out["paises"][iso] = {k: buscar(iso, c) for k, (c, _) in SERIES.items()}
        print(iso, {k: (round(v["valor"], 1), v["ano"]) if v else None for k, v in out["paises"][iso].items()})
    (Path(__file__).with_name("realidade_wdi.json")).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
