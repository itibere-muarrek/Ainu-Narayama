"""
Testes de src/condicao_media.py e da inclusão de Costa Rica e Paraguai (2026-11-10).
Rodar da raiz do repositório:  python test_condicao_media.py
"""

import pandas as pd

from src.condicao_media import ANOS_CICLO, resumo_2099, tabela_condicao
from src.config import DATA_PROCESSED_DIR, PAISES


def test_cri_pry_no_cadastro_e_no_n_index():
    assert {"CRI", "PRY"} <= set(PAISES) and len(PAISES) == 30
    n = pd.read_csv(DATA_PROCESSED_DIR / "n_index_2024.csv").set_index("codigo")
    assert len(n) == 30
    assert abs(n.loc["CRI", "n_estrela"] - 1.3229) < 1e-3 and abs(n.loc["PRY", "n_estrela"] - 2.4001) < 1e-3
    assert pd.isna(n.loc["CRI", "n_estrela_mig"])  # sem ajustes de cenário: não inventados


def test_28_paises_originais_nao_mudaram():
    n = pd.read_csv(DATA_PROCESSED_DIR / "n_index_2024.csv").set_index("codigo")
    assert abs(n.loc["ITA", "n_estrela"] - 0.608) < 1e-3 and abs(n.loc["KOR", "n_estrela"] - 0.456) < 1e-3


def test_tabela_condicao_formato_e_valores_conhecidos():
    df = tabela_condicao(["ITA", "KOR"])
    assert set(df.ano) == set(ANOS_CICLO) and set(df.cenario) == {"tendencia", "meta"}
    assert len(df) == 2 * 2 * len(ANOS_CICLO)
    r = resumo_2099(df).set_index("pais")
    # valores da exploração de 2026-11-10 (TFT -> 2,1 em 25 anos, mantida)
    assert abs(r.loc["ITA", "n_2099_meta"] - 1.01) < 0.01 and abs(r.loc["ITA", "a_e_2099_meta"] - 0.72) < 0.01
    assert abs(r.loc["KOR", "a_e_2099_tendencia"] - 1.45) < 0.01
    # a Meta não piora a razão Ascendentes/Estruturador em 2099 nesses países de TFT baixa
    assert (r["a_e_2099_meta"] < r["a_e_2099_tendencia"]).all()
    # 2024 é igual nos dois cenários (a rampa começa depois)
    d24 = df[df.ano == 2024].pivot_table(index="pais", columns="cenario", values="A_E")
    assert (d24["tendencia"] - d24["meta"]).abs().max() < 1e-9


def test_traducoes_da_pagina_completas():
    """Os 9 idiomas têm todas as chaves; o asterisco do N* segue escapado; a nota de tradução só falta em PT."""
    from src.i18n import IDIOMAS
    from src.i18n_condicao import TX, tcm

    for chave, entrada in TX.items():
        faltam = [lg for lg in IDIOMAS if lg not in entrada]
        assert not faltam, f"{chave}: sem {faltam}"
    for lg in IDIOMAS:
        for chave in ("cm_aviso", "cm_graf_n"):
            texto = tcm(chave, lg)
            assert "N*" not in texto.replace("N\\*", ""), f"{chave}/{lg}: asterisco do N* sem escape"
        assert (tcm("cm_nota_idioma", lg) == "") == (lg == "pt"), lg
        assert tcm("cm_ler", lg).count("\n") == 3, f"cm_ler/{lg}: devem ser 4 itens"
        assert "CRI = C50/D50" in tcm("cm_aviso", lg) and "2026-11-10" in tcm("cm_aviso", lg)


if __name__ == "__main__":
    for nome, fn in list(globals().items()):
        if nome.startswith("test_") and callable(fn):
            fn()
            print("ok ", nome)
