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
    assert ano == 2024 and len(c) == 101 and c[0] > 0   # KOSIS (série oficial 2010–2024), e não o 2019 antigo do portal NTA
    assert perfil("CRI", "C") is None and cfcc_por_coorte("PRY") is None  # sem perfil NTA público no repositório
    for iso, esperado in (("KOR", [21.0, 54.3, 24.8]), ("ITA", [17.4, 48.2, 34.5])):
        r = cfcc_por_coorte(iso)
        assert abs(sum(r["pct"]) - 100) < 1e-6 and r["cortes"] == (22, 61)
        assert all(abs(a - b) < 0.2 for a, b in zip(r["pct"], esperado)), (iso, r["pct"])


def test_costa_rica_tem_so_valores_agregados():
    assert perfil("CRI", "C") is None                       # o perfil por idade do CCP-UCR não está no repositório
    r = cfcc_por_coorte("CRI")
    assert r["pct"] == [31.5, 56.2, 12.3] and abs(sum(r["pct"]) - 100) < 1e-9 and r["cortes"] == (22, 61) and r["ano_pop"] == 2013


def test_perfil_do_japao_2019_do_ipss():
    """Japão: consumo e renda do trabalho de 2019 (IPSS v3.0). A janela de superávit (renda > consumo) fica a 1 ano dos cortes 24/63."""
    ano_c, c = perfil("JPN", "C")
    ano_y, yl = perfil("JPN", "YL")
    assert ano_c == ano_y == 2019 and len(c) == len(yl) == 101
    assert abs(c[40] - 2427200) < 1 and abs(yl[40] - 4199700) < 1       # 242,72 e 419,97 (10 mil ienes) da tabela do IPSS
    sup = [i for i in range(101) if c[i] - yl[i] < 0]
    assert (sup[0], sup[-1]) == (24, 61), (sup[0], sup[-1])
    r = cfcc_por_coorte("JPN")
    assert abs(sum(r["pct"]) - 100) < 1e-6 and r["ano_perfil"] == 2019


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
    assert cf["fonte"].startswith("KOSIS") and "2024" in cf["fonte"]
    for bloco, chave in coortes_motor.NOTA_ESPECIFICA:
        reg = k[bloco][chave]
        assert reg.get("lacuna") and reg["nota"] == coortes_motor.NOTA_ESPECIFICA[(bloco, chave)], (bloco, chave)


def test_ficha_do_japao_usa_o_perfil_2019_do_ipss():
    cf = FICHAS["JPN"]["consumo"]["cfcc_total_pct_desc_estr_asc"]
    assert cf["fonte"].startswith("IPSS") and "2019" in cf["fonte"] and abs(sum(cf["valor"]) - 100) < 0.2 and not cf.get("lacuna")
    assert all(abs(a - b) < 0.2 for a, b in zip(cf["valor"], cfcc_por_coorte("JPN")["pct"]))


def test_ajuste_das_fichas_e_idempotente():
    for iso, ficha in FICHAS.items():
        assert coortes_motor.aplicar(copy.deepcopy(ficha)) is False, iso


if __name__ == "__main__":
    for nome, fn in list(globals().items()):
        if nome.startswith("test_") and callable(fn):
            fn()
            print("ok ", nome)
