"""
ainu.systems — Emprego por criança e curva em J (Paper 3, exploratório).

Página só para usuários logados. Parte econômica do working paper "O emprego que nascerá": empregos brutos sustentados por uma criança adicional,
ciclo de um casal e curva em J da renda dos Estruturadores sob uma Meta de fecundidade. Cálculo em src/emprego_paper3.py (motor src/projecao.py),
validado contra as tabelas do paper (test_emprego_paper3.py). Método: ainu.systems/metodo-paper3. Cenário condicional, não previsão; empregos brutos
são tetos de demanda.
"""

import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from src import emprego_paper3 as E
from src.auth import exigir_login
from src.i18n import nome_pais, seletor_idioma
from src.i18n_simulacao import ts
from src.projecao import tfr_onu

PAISES = ["ITA", "KOR", "CRI"]
SITE = "https://ainu.systems/metodo-paper3/"
# valores do paper v2.6 (meta de 2,1 em 25 anos; sem retorno | com retorno da demanda): fundo %, ano do fundo, ano em que volta a superar a Tendência
PAPER = {"ITA": ((-10.3, 2059, 2078), (-5.1, 2055, 2069)), "KOR": ((-19.7, 2059, 2077), (-9.1, 2056, 2068)), "CRI": ((-8.8, 2057, 2075), (-4.7, 2054, 2067))}

TEXTOS = {
    "pt": {
        "titulo": "Emprego por criança e curva em J (Paper 3)",
        "intro": ("Parte econômica do working paper **O emprego que nascerá**: quantos empregos brutos uma criança adicional sustenta, o que isso significa para um casal "
                  "e como evolui a renda dos Estruturadores (23 a 60 anos) quando a fecundidade converge a uma Meta, com o custo de criar os filhos."),
        "aviso": ("Estudo **exploratório**. Os empregos são **tetos de demanda** (brutos, não líquidos) e o custo é um limite superior, cobrado integralmente aos "
                  "Estruturadores. Cenário condicional, **não previsão**. Método e fórmulas: " + SITE + " · valores do paper: " + SITE + "calculos/"),
        "pais": "País", "alvo": "TFT-alvo da Meta", "rampa": "Anos para chegar à meta", "desloc": "Deslocamento de outros gastos",
        "desloc_ajuda": "0% é o teto de demanda; com 50%, metade do emprego gerado deixa de existir por substituir outros gastos.",
        "filhos": "Número de filhos do casal", "retorno": "Retorno da demanda",
        "retorno_op": ["Sem retorno", "Teto do paper (o gasto com a criança vira renda de terceiros)"],
        "base": "Base do custo (Costa Rica)", "base_op": {"total": "Déficit total do ciclo de vida", "privado": "Só transferências privadas", "privado_publico": "Privadas mais a parcela pública"},
        "tfr_hoje": "TFT atual (ONU)",
        "h_emprego": "1. Empregos por criança adicional", "m_j0": "Empregos brutos por criança por ano (teto)", "m_j": "Com o deslocamento escolhido",
        "m_pc": "Consumo médio de um Descendente (US$ de 2019)", "m_inten": "Empregos por US$ milhão de consumo",
        "casal": "Um casal com {n} filhos sustenta cerca de **{jc:.2f}** posto de trabalho por ano pela demanda das crianças. O ciclo completo (fase dos pais, "
                 "{r:.2f} vez a dos filhos) chega a **{ce:.2f}** posto-ano (e a {c2:.2f} se a fase dos pais for tomada como o dobro). É posto-ano ao longo do ciclo, não empregos simultâneos, "
                 "e é uma ilustração contábil, não um resultado estimado.",
        "razao_kor": "Coreia do Sul: a razão de consumo (Descendente ÷ média) é **{r:.2f}** com o perfil KOSIS 2024; o paper v2.6, com a NTA 2019 antiga, usa 1,14 e obtém 0,30.",
        "h_j": "2. Curva em J da renda dos Estruturadores", "j_leg": "Diferença líquida entre a Meta e a Tendência (% da renda dos Estruturadores na Tendência)",
        "j_net": "Líquida do custo das crianças", "j_gross": "Só o efeito de haver mais Estruturadores", "ano": "Ano",
        "m_fundo": "Fundo da curva", "m_ano_fundo": "Ano do fundo", "m_cruza": "Volta a superar a Tendência em", "m_neg": "Anos de diferença negativa", "m_2074": "Em 2074", "m_2099": "Em 2099",
        "nunca": "não no horizonte",
        "cri_nota": ("Costa Rica: o perfil por idade do CCP-UCR não é redistribuído, então a curva usa parâmetros agregados (perfis planos). A aproximação fica a cerca de 0,4 ponto "
                     "percentual do vale do paper, que usa o perfil completo."),
        "paper_exp": "Valores do paper v2.6 (Meta de 2,1 em 25 anos)", "paper_cols": ["País", "Sem retorno: fundo (ano; volta em)", "Com retorno da demanda: fundo (ano; volta em)"],
        "limites": ("**Limites.** Valores médios, não marginais; empregos em pessoas ocupadas, com intensidade uniforme por seção; ICIO 2019 e perfis NTA suavizados; renda por idade constante "
                    "(sem produtividade); um único cenário, sem intervalo de incerteza. O custo cobrado aos Estruturadores é um limite superior, e o retorno da demanda também é um teto. "
                    "O gradiente de custo por número de filhos não é usado aqui porque falha como estimativa de gasto."),
        "fontes": "Fontes: ONU (WPP 2024), NTA (Itália 2008; Coreia do Sul 2024 pelo KOSIS), OCDE ICIO 2019 e ILOSTAT; Costa Rica: parâmetros derivados do CCP-UCR.",
    },
    "en": {
        "titulo": "Jobs per child and the J-curve (Paper 3)",
        "intro": ("The economic part of the working paper **The job that will be born**: how many gross jobs one additional child supports, what that means for a couple, "
                  "and how Structurers' income (ages 23 to 60) evolves when fertility converges to a Target, including the cost of raising the children."),
        "aviso": ("An **exploratory** study. Jobs are **demand ceilings** (gross, not net) and the cost is an upper bound, charged entirely to Structurers. A conditional scenario, "
                  "**not a forecast**. Method and formulas: " + SITE + " · the paper's values: " + SITE + "calculos/"),
        "pais": "Country", "alvo": "Target TFR", "rampa": "Years to reach the target", "desloc": "Displacement of other spending",
        "desloc_ajuda": "0% is the demand ceiling; at 50%, half of the jobs generated disappear because they displace other spending.",
        "filhos": "Number of children in the couple", "retorno": "Demand return",
        "retorno_op": ["No return", "Paper ceiling (spending on the child becomes third parties' income)"],
        "base": "Cost basis (Costa Rica)", "base_op": {"total": "Total life-cycle deficit", "privado": "Private transfers only", "privado_publico": "Private plus the public share"},
        "tfr_hoje": "Current TFR (UN)",
        "h_emprego": "1. Jobs per additional child", "m_j0": "Gross jobs per child per year (ceiling)", "m_j": "With the chosen displacement",
        "m_pc": "Average consumption of a Descendant (US$ of 2019)", "m_inten": "Jobs per US$ million of consumption",
        "casal": "A couple with {n} children supports about **{jc:.2f}** jobs per year through the children's demand. The full cycle (the parents' phase, "
                 "{r:.2f} times the children's) reaches **{ce:.2f}** job-years (and {c2:.2f} if the parents' phase is taken as twice as long). It is job-years over the cycle, not simultaneous jobs, "
                 "and an accounting illustration, not an estimated result.",
        "razao_kor": "South Korea: the consumption ratio (Descendant ÷ average) is **{r:.2f}** with the KOSIS 2024 profile; paper v2.6, with the earlier 2019 NTA, uses 1.14 and gets 0.30.",
        "h_j": "2. J-curve of Structurers' income", "j_leg": "Net difference between the Target and the Trend (% of Structurers' income under the Trend)",
        "j_net": "Net of the cost of children", "j_gross": "Only the effect of having more Structurers", "ano": "Year",
        "m_fundo": "Trough", "m_ano_fundo": "Year of the trough", "m_cruza": "Overtakes the Trend in", "m_neg": "Years of negative difference", "m_2074": "In 2074", "m_2099": "In 2099",
        "nunca": "not within the horizon",
        "cri_nota": ("Costa Rica: the age profile from CCP-UCR is not redistributed, so the curve uses aggregate parameters (flat profiles). The approximation lies about 0.4 percentage points "
                     "from the paper's trough, which uses the full profile."),
        "paper_exp": "Paper v2.6 values (Target of 2.1 in 25 years)", "paper_cols": ["Country", "No return: trough (year; overtakes in)", "With demand return: trough (year; overtakes in)"],
        "limites": ("**Limits.** Averages, not marginal values; jobs in employed persons, with uniform intensity by section; ICIO 2019 and smoothed NTA profiles; income by age held constant "
                    "(no productivity); a single scenario, with no uncertainty interval. The cost charged to Structurers is an upper bound, and the demand return is also a ceiling. "
                    "The cost gradient by number of children is not used here because it fails as an expenditure estimate."),
        "fontes": "Sources: UN (WPP 2024), NTA (Italy 2008; South Korea 2024 via KOSIS), OECD ICIO 2019 and ILOSTAT; Costa Rica: parameters derived from CCP-UCR.",
    },
}

st.set_page_config(page_title="ainu.systems — Paper 3", layout="wide")
lang = seletor_idioma()
exigir_login(lambda k: ts(k, lang))
L = TEXTOS["pt"] if lang == "pt" else TEXTOS["en"]

st.title(L["titulo"])
st.markdown(L["intro"])
st.info(L["aviso"])

c1, c2, c3 = st.columns([1, 2, 2])
with c1:
    pais = st.selectbox(L["pais"], PAISES, format_func=lambda c: nome_pais(c, lang))
with c2:
    alvo = st.slider(L["alvo"], min_value=0.8, max_value=3.2, value=2.1, step=0.05, help=f"{L['tfr_hoje']}: {float(tfr_onu(pais)[0]):.2f}")
with c3:
    rampa = st.slider(L["rampa"], min_value=10, max_value=40, value=25, step=1)
d1, d2, d3 = st.columns(3)
with d1:
    desloc = st.slider(L["desloc"], min_value=0, max_value=100, value=0, step=5, help=L["desloc_ajuda"], format="%d%%") / 100
with d2:
    filhos = st.slider(L["filhos"], min_value=1, max_value=4, value=2)
with d3:
    com_retorno = st.radio(L["retorno"], L["retorno_op"], index=0) == L["retorno_op"][1]
base = "total"
if pais == "CRI":
    base = st.selectbox(L["base"], list(L["base_op"]), format_func=lambda k: L["base_op"][k])
retorno = E.PARAMETROS[pais]["retorno_demanda"] if com_retorno else 0.0


@st.cache_data(show_spinner=False)
def _curva(iso: str, alvo_: float, rampa_: int, retorno_: float, base_: str):
    return E.curva_j(iso, alvo_, rampa_, retorno_, base_custo=base_)


# ---------------------------------------------------------------------------
# 1. Empregos por criança
# ---------------------------------------------------------------------------
st.subheader(L["h_emprego"])
j = E.emprego_por_crianca(pais, desloc)
ciclo = E.ciclo_casal(j["j"], filhos, pais)
m1, m2, m3, m4 = st.columns(4)
m1.metric(L["m_j0"], f"{j['j0']:.3f}")
m2.metric(L["m_j"], f"{j['j']:.3f}")
m3.metric(L["m_pc"], f"{j['consumo_medio_descendente_usd']:,.0f}")
m4.metric(L["m_inten"], f"{j['intensidade']:.1f}")
st.markdown(L["casal"].format(n=filhos, jc=ciclo["j_casal"], r=ciclo["r_exato"], ce=ciclo["ciclo_exato"], c2=ciclo["ciclo_r2"]))
if pais == "KOR":
    st.caption(L["razao_kor"].format(r=j["razao"]))

# ---------------------------------------------------------------------------
# 2. Curva em J
# ---------------------------------------------------------------------------
st.subheader(L["h_j"])
cv = _curva(pais, round(alvo, 4), int(rampa), float(retorno), base)
x = list(cv.anos)
fig = go.Figure()
fig.add_hline(y=0, line_color="#999999", line_width=1)
fig.add_trace(go.Scatter(x=x, y=cv.ganho_bruto, name=L["j_gross"], line=dict(color="#7f7f7f", dash="dash")))
fig.add_trace(go.Scatter(x=x, y=cv.pct, name=L["j_net"], line=dict(color="#1f77b4", width=3)))
fig.update_layout(height=420, margin=dict(l=10, r=10, t=10, b=10), xaxis_title=L["ano"], yaxis_title=L["j_leg"], legend=dict(orientation="h", y=-0.2))
st.plotly_chart(fig, use_container_width=True)
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric(L["m_fundo"], f"{cv.fundo_pct:.1f}%")
k2.metric(L["m_ano_fundo"], str(cv.ano_fundo))
k3.metric(L["m_cruza"], str(cv.ano_cruza) if cv.ano_cruza else L["nunca"])
k4.metric(L["m_neg"], str(cv.anos_negativos))
k5.metric(L["m_2074"], f"{cv.em(2074):+.1f}%")
k6.metric(L["m_2099"], f"{cv.em(2099):+.1f}%")
if pais == "CRI":
    st.caption(L["cri_nota"])

with st.expander(L["paper_exp"]):
    tab = {L["paper_cols"][0]: [nome_pais(i, lang) for i in PAISES],
           L["paper_cols"][1]: [f"{PAPER[i][0][0]:.1f}% ({PAPER[i][0][1]}; {PAPER[i][0][2]})" for i in PAISES],
           L["paper_cols"][2]: [f"{PAPER[i][1][0]:.1f}% ({PAPER[i][1][1]}; {PAPER[i][1][2]})" for i in PAISES]}
    st.table(tab)

st.markdown(L["limites"])
st.caption(L["fontes"])
