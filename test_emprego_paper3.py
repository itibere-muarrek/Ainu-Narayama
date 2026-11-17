"""
Testes de src/emprego_paper3.py contra os números do working paper "O emprego que nascerá" (v2.6).
Rodar da raiz do repositório:  python test_emprego_paper3.py

A Itália reproduz o paper (perfil NTA 2008 do portal, no repositório). A Coreia do Sul usa agora o perfil KOSIS 2024, então difere do paper (NTA 2019 antiga);
o teste fixa o valor atual como regressão e confere a razão de consumo do paper (1,14) separadamente. A Costa Rica vem de parâmetros agregados
(o perfil do CCP-UCR não é redistribuído): confere-se que a aproximação fica perto do valor do paper com perfil por idade.
"""

from src import emprego_paper3 as E


def test_empregos_por_crianca_batem_com_o_paper():
    assert abs(E.emprego_por_crianca("ITA")["j0"] - 0.186) < 0.002           # paper: 0,186
    assert abs(E.emprego_por_crianca("KOR", razao=E.RAZAO_KOR_PAPER_V2_6)["j0"] - 0.300) < 0.002   # paper: 0,300 (razão 1,14)
    assert abs(E.emprego_por_crianca("CRI")["j0"] - 0.202) < 0.002           # paper: 0,202
    j = E.emprego_por_crianca("ITA", deslocamento=0.5)
    assert abs(j["j"] - 0.5 * j["j0"]) < 1e-12
    assert E.emprego_por_crianca("ITA", deslocamento=1.0)["j"] == 0.0


def test_ciclo_do_casal():
    c = E.ciclo_casal(0.25, filhos=2, iso="ITA")
    assert abs(c["j_casal"] - 0.5) < 1e-12 and abs(c["r_exato"] - 38 / 23) < 1e-12
    assert 1.3 < c["ciclo_exato"] < 1.34 and abs(c["ciclo_r2"] - 1.5) < 1e-12


def test_curva_j_da_italia_reproduz_o_paper():
    s = E.curva_j("ITA")                                                   # paper: -10,3% em 2059; volta a superar a Tendência em 2078
    assert abs(s.fundo_pct - (-10.29)) < 0.05 and s.ano_fundo == 2059 and s.ano_cruza == 2078
    c = E.curva_j("ITA", retorno=E.PARAMETROS["ITA"]["retorno_demanda"])   # paper: -5,1% em 2055; 2069
    assert abs(c.fundo_pct - (-5.06)) < 0.05 and c.ano_fundo == 2055 and c.ano_cruza == 2069


def test_curva_j_da_coreia_com_o_perfil_kosis_2024():
    s = E.curva_j("KOR")                    # regressão com o perfil KOSIS 2024 (o paper v2.6, com a NTA 2019 antiga, dá -19,7% em 2059)
    assert abs(s.fundo_pct - (-20.88)) < 0.1 and s.ano_fundo == 2060 and s.ano_cruza == 2081
    assert -19.7 > s.fundo_pct > -22                                        # mais fundo que o paper, mas da mesma ordem


def test_costa_rica_agregada_fica_perto_do_paper():
    s = E.curva_j("CRI")                    # paper (perfil por idade): -8,79% em 2057; 2075
    assert abs(s.fundo_pct - (-8.787)) < 0.6 and abs(s.ano_fundo - 2057) <= 1 and abs(s.ano_cruza - 2075) <= 1
    c = E.curva_j("CRI", retorno=E.PARAMETROS["CRI"]["retorno_demanda"])    # paper: -4,73% em 2054; 2067
    assert abs(c.fundo_pct - (-4.731)) < 0.6 and abs(c.ano_fundo - 2054) <= 1 and abs(c.ano_cruza - 2067) <= 1


def test_propriedades_gerais():
    sem, com = E.curva_j("ITA"), E.curva_j("ITA", retorno=0.452)
    assert (com.pct >= sem.pct - 1e-9).all()                                # o retorno da demanda só reduz o custo
    alto = E.curva_j("ITA", tfr_alvo=2.1, retorno=1.0)                      # retorno total: só o efeito bruto (Estruturadores a mais)
    assert abs(alto.pct - alto.ganho_bruto).max() < 1e-9


if __name__ == "__main__":
    for nome, fn in list(globals().items()):
        if nome.startswith("test_") and callable(fn):
            fn()
            print("ok ", nome)
