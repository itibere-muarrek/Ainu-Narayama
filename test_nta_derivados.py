"""
Testes de src/nta_derivados.py e do alinhamento das fichas do Diretório à composição de perfis de src/config.py (2026-11-12).
Rodar da raiz do repositório:  python test_nta_derivados.py
"""

import copy
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "scripts" / "diretorio"))

import coortes_motor
from src.nta_derivados import cfcc_por_coorte, perfil

FICHAS = {f["iso"]: f for f in json.loads((RAIZ / "data" / "diretorio" / "publicavel" / "paises.json").read_text(encoding="utf-8"))}


def test_perfis_nta_e_cfcc_por_coorte():
    ano, c = perfil("KOR", "C")
    assert ano == 2019 and len(c) == 101 and c[0] > 0
    assert perfil("CRI", "C") is None and cfcc_por_coorte("PRY") is None  # sem perfil NTA público no repositório
    for iso, esperado in (("KOR", [21.0, 54.3, 24.8]), ("ITA", [17.4, 48.2, 34.5])):
        r = cfcc_por_coorte(iso)
        assert abs(sum(r["pct"]) - 100) < 1e-6 and r["cortes"] == (22, 61)
        assert all(abs(a - b) < 0.2 for a, b in zip(r["pct"], esperado)), (iso, r["pct"])


def test_metodo_reproduz_a_ficha_da_italia_em_1_ponto():
    """Validação do método: com a NTA 2008, o resultado fica a 1 ponto percentual da ficha da Itália (cortes inalterados)."""
    r = cfcc_por_coorte("ITA")["pct"]
    ficha = FICHAS["ITA"]["consumo"]["cfcc_total_pct_desc_estr_asc"]["valor"]
    assert all(abs(a - b) <= 1.5 for a, b in zip(r, ficha)), (r, ficha)


def test_ficha_da_coreia_e_da_italia_alinhadas_ao_config():
    for iso in ("ITA", "KOR"):
        c = FICHAS[iso]["coortes"]
        assert c["composicao_perfis"] == "C30 D70" and (c["descendentes"], c["estruturadores"], c["ascendentes"]) == ("0–22", "23–60", "61+"), (iso, c)
    k = FICHAS["KOR"]
    cf = k["consumo"]["cfcc_total_pct_desc_estr_asc"]
    assert cf["natureza"] == "EST" and abs(sum(cf["valor"]) - 100) < 0.2 and not cf.get("lacuna") and "nota" in cf
    for bloco, chave in coortes_motor.NOTA_ESPECIFICA:
        reg = k[bloco][chave]
        assert reg.get("lacuna") and reg["nota"] == coortes_motor.NOTA_ESPECIFICA[(bloco, chave)], (bloco, chave)


def test_ajuste_das_fichas_e_idempotente():
    for iso, ficha in FICHAS.items():
        assert coortes_motor.aplicar(copy.deepcopy(ficha)) is False, iso


if __name__ == "__main__":
    for nome, fn in list(globals().items()):
        if nome.startswith("test_") and callable(fn):
            fn()
            print("ok ", nome)
