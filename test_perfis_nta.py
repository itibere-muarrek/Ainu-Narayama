"""
Testes da página pública "Perfis NTA por idade de 21 países" (scripts/gerar_perfis_nta.py), 2026-11-18.
Rodar da raiz do repositório:  python test_perfis_nta.py
"""

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "scripts"))

import gerar_perfis_nta as g
from src.i18n import nome_pais
from src.nta_derivados import cfcc_por_coorte

PAGINA = g.PAGINA


def test_vinte_e_um_paises_com_valores_coerentes():
    ls = g.calcular()
    assert [l["iso"] for l in ls] == g.PAISES and len(ls) == 21
    for l in ls:
        assert abs(sum(l["cfcc_pct"]) - 100) < 0.2 and all(x > 0 for x in l["cfcc_pct"]), l["iso"]
        assert l["cfcc_pct"] == [round(x, 1) for x in cfcc_por_coorte(l["iso"])["pct"]], l["iso"]
        assert l["superavit"][0] < l["superavit"][1] and len(l["curvas_norm"]["C"]) == len(l["curvas_norm"]["YL"]) == 91
        assert 0.3 < max(l["curvas_norm"]["YL"]) < 3, l["iso"]                # curvas divididas pela média de YL aos 30–49


def test_pagina_gerada_esta_em_dia_e_traz_a_atribuicao():
    html = (PAGINA / "index.html").read_text(encoding="utf-8")
    assert html == g.pagina(g.calcular()), "rode scripts/gerar_perfis_nta.py"
    for iso in g.PAISES:
        assert nome_pais(iso, "pt") in html and nome_pais(iso, "en") in html, iso
    for trecho in ("Denisenko", "Adjei", "Lee, R.; Mason, A.", "ntaccounts.org", "IPSS", "KOSIS", "estimativas", "estimates", "Costa Rica"):
        assert trecho in html, trecho
    assert 'data-lang="pt"' in html and 'data-lang="en"' in html and html.count("<svg") == 42


def test_json_derivado_e_pdfs():
    d = json.loads((PAGINA / "perfis_nta_derivados.json").read_text(encoding="utf-8"))
    assert len(d["paises"]) == 21 and all("curvas_norm" not in p for p in d["paises"])
    assert {p["iso"] for p in d["paises"]} == set(g.PAISES)
    for lang in ("pt", "en"):
        pdf = PAGINA / f"perfis-nta-apresentacao-{lang}.pdf"
        assert pdf.exists() and 100_000 < pdf.stat().st_size < 3_000_000 and pdf.read_bytes()[:4] == b"%PDF"


def test_sitemap_inclui_a_pagina():
    assert "https://ainu.systems/perfis-nta/" in (RAIZ / "landing" / "ainu-systems" / "sitemap.xml").read_text(encoding="utf-8")


if __name__ == "__main__":
    for nome, fn in list(globals().items()):
        if nome.startswith("test_") and callable(fn):
            fn()
            print("ok ", nome)
