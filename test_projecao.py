"""
Testes do motor de projeção por coorte (src/projecao.py) e do hash de senhas
(src/senha.py). Sem dependência de pytest: `python test_projecao.py`.

Os testes de ordem de grandeza contra a ONU (calibração, N* de 2024, variante
"Zero migration") ficam em scripts/validar_projecao.py, que precisa dos dumps
da ONU em data/raw/_cache; estes aqui rodam só com o que está no repositório.
"""

import numpy as np
import pandas as pd

from src.config import DATA_PROCESSED_DIR, PAISES_DESTAQUE_NARAYAMA_LIVE, PAISES_EXEMPLO_ZONAS_NARAYAMA_LIVE
from src.projecao import n_estrela_serie, projetar, simular, tfr_onu, trajetoria_tfr
from src.senha import gerar_hash, verificar_hash

ONZE = PAISES_DESTAQUE_NARAYAMA_LIVE + PAISES_EXEMPLO_ZONAS_NARAYAMA_LIVE


def test_cenario_com_tfr_da_onu_e_o_cenario_base():
    for p in ("BRA", "JPN", "NGA"):
        base = projetar(p)
        igual = projetar(p, tfr_onu(p))
        assert np.allclose(base.pop, igual.pop)


def test_trajetoria_tfr_rampa_e_patamar():
    tfr = trajetoria_tfr("BRA", 2.1)
    assert abs(tfr[0] - tfr_onu("BRA")[0]) < 1e-12  # 2024 = ONU
    assert abs(tfr[25] - 2.1) < 1e-12  # chega ao alvo em 25 anos
    assert np.allclose(tfr[25:51], 2.1)  # e mantém por mais 25
    meio = tfr[12]
    assert min(tfr[0], 2.1) < meio < max(tfr[0], 2.1)  # rampa linear entre os dois


def test_mais_fecundidade_mais_populacao_em_2074():
    for p in ("BRA", "JPN", "ITA", "KOR"):
        baixo = projetar(p, trajetoria_tfr(p, 1.5)).pop_total[50]
        alto = projetar(p, trajetoria_tfr(p, 2.5)).pop_total[50]
        assert alto > baixo


def test_populacao_nao_negativa_e_idades_validas():
    for p in ONZE:
        r = projetar(p, trajetoria_tfr(p, 0.8))
        assert (r.pop >= 0).all()
        assert r.pop.shape[:2] == (2, 101)


def test_n_estrela_2024_bate_com_producao():
    ref = pd.read_csv(DATA_PROCESSED_DIR / "n_index_2024.csv").set_index("codigo")
    for p in ONZE:
        v = float(n_estrela_serie(projetar(p))["n_estrela"][0])
        assert abs(v / ref.loc[p, "n_estrela"] - 1) < 0.001, p  # 0,1%


def test_composicao_de_perfis_ajustavel_a_mao():
    # Mudar a composição muda só os cortes (e, portanto, o N*), nunca a projeção.
    r = projetar("BRA")
    a = n_estrela_serie(r, {"C": 1.0})
    b = n_estrela_serie(r, {"B": 0.3, "C": 0.4, "D": 0.3})
    assert a["cortes"] != b["cortes"]
    assert a["n_estrela"][0] != b["n_estrela"][0]


def test_simular_devolve_pontos_de_virada():
    s = simular("JPN", 2.1)
    assert set(s["virada_cenario"]) == {"saldo_natural_positivo", "pico_populacao", "fim_da_queda", "n_estrela_cruza_pea"}
    assert s["horizonte_idx"] == 51  # 2024..2074


def test_hash_de_senha():
    h = gerar_hash("uma-senha-longa-123")
    assert verificar_hash("uma-senha-longa-123", h)
    assert not verificar_hash("outra", h)
    assert not verificar_hash("x", "lixo")
    assert gerar_hash("a") != gerar_hash("a")  # sal individual


def test_textos_da_simulacao_completos_e_consistentes():
    import string

    from src.i18n import IDIOMAS
    from src.i18n_simulacao import TX_SIM, numeros_validacao, ts

    fm = string.Formatter()
    for chave, v in TX_SIM.items():
        ref = {f for _, f, _, _ in fm.parse(v["pt"]) if f}
        for lang in IDIOMAS:
            assert lang in v, (chave, lang)
            assert {f for _, f, _, _ in fm.parse(v[lang]) if f} == ref, (chave, lang)
    for lang in IDIOMAS:  # o texto do método formata com os números da validação
        assert "{" not in ts("sim_metodo", lang, **numeros_validacao(lang))


def test_validacao_publicada_dentro_dos_limites():
    import json
    from pathlib import Path

    v = json.loads((Path(__file__).parent / "docs" / "validacao_projecao.json").read_text(encoding="utf-8"))
    assert v["v3_max_dif"] < 0.001  # N* 2024 do motor vs produção
    assert v["v1_max_desvio"] < 0.02  # calibração dos nascimentos
    assert v["v4_max"] < 0.03  # sem migração vs ONU Zero migration
    assert v["v6_mediana"] < v["v5_mediana"] / 2  # o eco explica a diferença vs P_eq antigo


if __name__ == "__main__":
    testes = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in testes:
        t()
        print("ok ", t.__name__)
    print(f"{len(testes)} testes passaram")
