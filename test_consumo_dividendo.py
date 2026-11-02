"""
Testes de src/consumo_dividendo.py (escala do Dividendo, crianças adicionais, cenários).
Sem dependência de pytest: `python test_consumo_dividendo.py`. Os testes que leem
data/diretorio/publicavel/simulacoes.json são pulados se o arquivo não existe (ele fica fora do git).
"""

from src.consumo_dividendo import (
    ARQUIVO,
    carregar,
    cenarios,
    custo_dividendo,
    empregos_liquidos,
    horizontes_do_cenario,
    incremento,
    razao_gasto_familia,
    razao_programa,
)


def test_custo_dividendo_e_proporcional():
    assert custo_dividendo(10, 0.75) == 0.75
    assert abs(custo_dividendo(25, 0.75) - 1.875) < 1e-12
    assert abs(custo_dividendo(50, 0.75) - 3.75) < 1e-12
    assert custo_dividendo(0, 0.75) == 0
    assert custo_dividendo(10, None) is None
    assert custo_dividendo(-1, 0.75) is None


def test_razoes():
    assert abs(razao_programa(0.75, 0.87) - 0.862) < 1e-3
    assert razao_programa(0.75, None) is None
    assert razao_programa(0.75, 0) is None
    assert abs(razao_gasto_familia(0.75, 1.43) - 0.524) < 1e-3
    assert razao_gasto_familia(None, 1.43) is None


def test_incremento_linear():
    assert incremento(1000, 0.251) == 251
    assert incremento(0, 0.251) == 0
    assert incremento(1000, None) is None


def test_empregos_liquidos_reproduz_os_tres_pontos():
    b, l50, l100 = 0.251, 0.133, 0.0155
    assert empregos_liquidos(b, l50, l100, 0) == b
    assert abs(empregos_liquidos(b, l50, l100, 50) - l50) < 1e-12
    assert abs(empregos_liquidos(b, l50, l100, 100) - l100) < 1e-12
    meio = empregos_liquidos(b, l50, l100, 25)
    assert l50 < meio < b
    assert empregos_liquidos(b, l50, l100, 101) is None
    assert empregos_liquidos(None, l50, l100, 10) is None


def test_cenarios_e_horizontes():
    hs = [
        {"cenario": "S3", "ano": 2040}, {"cenario": "S1", "ano": 2030}, {"cenario": "S3", "ano": 2030},
    ]
    assert cenarios(hs) == ["S3", "S1"]
    assert [h["ano"] for h in horizontes_do_cenario(hs, "S3")] == [2030, 2040]


def test_dados_do_diretorio_reproduzem_a_planilha():
    dados = carregar()
    if dados is None:
        print("   (simulacoes.json ausente: teste pulado)")
        return
    assert len(dados["paises"]) == 11
    for iso, p in dados["paises"].items():
        assert p["natureza_dividendo"] == "SIM"
        if p["dividendo_10pct_pib"] is not None:
            # os 25% e 50% da planilha são o dobro e meio e o quíntuplo do valor dos 10%
            assert abs(custo_dividendo(50, p["dividendo_10pct_pib"]) - 5 * p["dividendo_10pct_pib"]) < 1e-9
        assert len(p["horizontes"]) == 12 or iso == "NGA" and p["horizontes"], iso
    ita = dados["paises"]["ITA"]
    assert abs(razao_programa(ita["dividendo_10pct_pib"], ita["programa"]["pct_pib"]) - 0.86) < 0.01     # 0,9× no Paper 3
    assert dados["paises"]["IND"]["programa"]["pct_pib"] is None                                       # nível L2: retido
    assert dados["paises"]["NGA"]["dividendo_10pct_pib"] is None


if __name__ == "__main__":
    for nome, f in list(globals().items()):
        if nome.startswith("test_") and callable(f):
            f()
            print("ok", nome)
