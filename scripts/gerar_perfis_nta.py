"""
Gera a página pública "Perfis NTA por idade de 21 países" (PT/EN) e o JSON com os valores derivados.

Saídas:
  landing/ainu-systems/perfis-nta/index.html
  landing/ainu-systems/perfis-nta/perfis_nta_derivados.json
  landing/ainu-systems/sitemap.xml (acrescenta a página, se ainda não estiver)

Entradas (todas no repositório): data/raw/nta_perfis_C_YL_S.csv, src/nta_derivados.py (perfil e cfcc_por_coorte), src/config.py (cortes por Perfil).
Os gráficos são SVG embutidos: curvas de consumo C(a) e renda do trabalho YL(a) divididas pela média da renda do trabalho de 30 a 49 anos
(prática usual da NTA, que torna as formas comparáveis entre moedas), com os cortes etários dos coortes marcados.

Rodar da raiz do repositório:  python scripts/gerar_perfis_nta.py
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import numpy as np

from src.config import COMPOSICAO_PERFIL_POR_PAIS, cortes_por_composicao
from src.i18n import nome_pais
from src.nta_derivados import cfcc_por_coorte, perfil

HOJE = date(2026, 11, 18)
PAGINA = RAIZ / "landing" / "ainu-systems" / "perfis-nta"
PAISES = ["ARG", "AUS", "BRA", "CHL", "CHN", "CRI", "DEU", "FRA", "IDN", "IND", "ITA", "JPN", "KOR", "MEX", "NGA", "POL", "RUS", "SWE", "THA", "USA", "ZAF"]
FONTE_NACIONAL = {"JPN": "IPSS (2019, v3.0)", "KOR": "KOSIS (2024)"}
EQUIPE = {"RUS": "M. Denisenko, V. Kozlov", "SWE": "N. Adjei, T. Lindh, G. Öberg", "CRI": "P. Jiménez-Fontana"}
URL_CSV = "https://github.com/itibere-muarrek/Ainu-Narayama/blob/main/data/raw/nta_perfis_C_YL_S.csv"
URL_FONTES = "https://github.com/itibere-muarrek/Ainu-Narayama/blob/main/docs/nta_perfis_fonte.md"
URL_TERCEIROS = "https://github.com/itibere-muarrek/Ainu-Narayama/blob/main/THIRD_PARTY_DATA.md"


def calcular() -> list[dict]:
    linhas = []
    for iso in PAISES:
        ano_c, c = perfil(iso, "C")
        ano_y, y = perfil(iso, "YL")
        ps = perfil(iso, "S")
        bm, tm = cortes_por_composicao(COMPOSICAO_PERFIL_POR_PAIS[iso])
        sup = [i for i in range(101) if y[i] > c[i]]
        cf = cfcc_por_coorte(iso)
        norm = y[30:50].mean()
        linhas.append({
            "iso": iso, "ano_c_yl": ano_c, "ano_poupanca": ps[0] if ps else None,
            "fonte": FONTE_NACIONAL.get(iso, "Portal NTA"), "equipe": EQUIPE.get(iso),
            "composicao_perfis": "/".join(f"{k}{round(v * 100)}" for k, v in sorted(COMPOSICAO_PERFIL_POR_PAIS[iso].items())),
            "corte_descendentes_ate": int(bm), "corte_ascendentes_desde": int(tm),
            "cfcc_pct": [round(x, 1) for x in cf["pct"]], "ano_populacao": cf["ano_pop"],
            "superavit": [sup[0], sup[-1]], "inicio_menos_corte_desc": sup[0] - int(bm), "fim_menos_corte_asc": sup[-1] - int(tm),
            "curvas_norm": {"C": [round(float(v / norm), 4) for v in c[:91]], "YL": [round(float(v / norm), 4) for v in y[:91]]},
        })
    return linhas


def svg(l: dict) -> str:
    W, H, ml, mr, mt, mb = 240, 150, 26, 6, 8, 20
    xmax, ymax = 90.0, 2.0
    px = lambda a: ml + (W - ml - mr) * a / xmax
    py = lambda v: mt + (H - mt - mb) * (1 - min(v, ymax) / ymax)
    def linha(v, cls):
        pts = " ".join(f"{px(i):.1f},{py(x):.1f}" for i, x in enumerate(v))
        return f'<polyline class="{cls}" points="{pts}"/>'
    g = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{l["iso"]}">']
    for yv in (0.5, 1.0, 1.5, 2.0):
        g.append(f'<line class="grade" x1="{ml}" x2="{W - mr}" y1="{py(yv):.1f}" y2="{py(yv):.1f}"/><text class="eixo" x="{ml - 3}" y="{py(yv) + 3:.1f}" text-anchor="end">{yv:g}</text>')
    for a in (0, 20, 40, 60, 80):
        g.append(f'<text class="eixo" x="{px(a):.1f}" y="{H - 6}" text-anchor="middle">{a}</text>')
    for corte in (l["corte_descendentes_ate"] + 0.5, l["corte_ascendentes_desde"] - 0.5):
        g.append(f'<line class="corte" x1="{px(corte):.1f}" x2="{px(corte):.1f}" y1="{mt}" y2="{H - mb}"/>')
    g.append(linha(l["curvas_norm"]["C"], "curvaC"))
    g.append(linha(l["curvas_norm"]["YL"], "curvaY"))
    g.append("</svg>")
    return "".join(g)


def num(x: float, lang: str, nd: int = 1) -> str:
    s = f"{x:.{nd}f}"
    return s.replace(".", ",") if lang == "pt" else s


def tabelas(linhas: list[dict]) -> dict:
    out = {}
    for lang in ("pt", "en"):
        cab_a = {"pt": ["País", "Ano (C e renda do trabalho)", "Poupança", "Fonte", "Equipe nacional indicada"],
                 "en": ["Country", "Year (C and labor income)", "Saving", "Source", "National team listed"]}[lang]
        a = "<table><thead><tr>" + "".join(f"<th>{h}</th>" for h in cab_a) + "</tr></thead><tbody>"
        for l in linhas:
            a += (f"<tr><td>{nome_pais(l['iso'], lang)}</td><td>{l['ano_c_yl']}</td><td>{l['ano_poupanca'] or '—'}</td>"
                  f"<td>{l['fonte']}</td><td>{l['equipe'] or '—'}</td></tr>")
        a += "</tbody></table>"
        cab_c = {"pt": ["País", "Cortes: Descendentes até / Ascendentes desde", "Descendentes %", "Estruturadores %", "Ascendentes %", "Idades com superávit (renda > consumo)", "Início − corte D", "Fim − corte A"],
                 "en": ["Country", "Cut-offs: Descendants up to / Ascendants from", "Descendants %", "Structurers %", "Ascendants %", "Ages with surplus (income > consumption)", "Start − D cut", "End − A cut"]}[lang]
        c = "<table><thead><tr>" + "".join(f"<th>{h}</th>" for h in cab_c) + "</tr></thead><tbody>"
        for l in sorted(linhas, key=lambda z: -z["cfcc_pct"][2]):
            d, e, asc = l["cfcc_pct"]
            c += (f"<tr><td>{nome_pais(l['iso'], lang)}</td><td>{l['corte_descendentes_ate']} / {l['corte_ascendentes_desde']}</td>"
                  f"<td>{num(d, lang)}</td><td>{num(e, lang)}</td><td>{num(asc, lang)}</td>"
                  f"<td>{l['superavit'][0]}–{l['superavit'][1]}</td><td>{l['inicio_menos_corte_desc']:+d}</td><td>{l['fim_menos_corte_asc']:+d}</td></tr>")
        c += "</tbody></table>"
        out[lang] = (a, c)
    return out


def barras(linhas: list[dict]) -> dict:
    out = {}
    for lang in ("pt", "en"):
        h = '<div class="barras">'
        for l in sorted(linhas, key=lambda z: -z["cfcc_pct"][2]):
            d, e, a = l["cfcc_pct"]
            h += (f'<div class="b-linha"><span class="b-nome">{nome_pais(l["iso"], lang)}</span><span class="b-trilho">'
                  f'<span class="b-d" style="width:{d}%">{num(d, lang, 0)}</span><span class="b-e" style="width:{e}%">{num(e, lang, 0)}</span>'
                  f'<span class="b-a" style="width:{a}%">{num(a, lang, 0)}</span></span></div>')
        out[lang] = h + "</div>"
    return out


def grade(linhas: list[dict]) -> dict:
    out = {}
    for lang in ("pt", "en"):
        h = '<div class="grade-g">'
        for l in linhas:
            h += (f'<figure><figcaption><strong>{nome_pais(l["iso"], lang)}</strong> <span>{l["ano_c_yl"]} · {l["composicao_perfis"]}</span></figcaption>'
                  f'{svg(l)}</figure>')
        out[lang] = h + "</div>"
    return out


CSS = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;1,500&family=JetBrains+Mono:wght@400;500&display=swap');
    :root { --ink:#0D1B2A; --ink-soft:#3D5166; --sky:#1B6CA8; --glow:#6E92A8; --paper:#F7F9FB; --divider:#D8E4EE; --white:#FFFFFF; --y:#C0392B;
            --f-body:'Inter', system-ui, sans-serif; --f-mono:'JetBrains Mono','Courier New',monospace; }
    * { box-sizing: border-box; }
    body { margin:0; font-family:var(--f-body); color:var(--ink); background:var(--paper); line-height:1.6; }
    nav { position:sticky; top:0; z-index:5; background:var(--white); border-bottom:1px solid var(--divider); display:flex; align-items:center; justify-content:space-between; padding:.7rem 1.2rem; }
    .nav-logo { font-family:var(--f-mono); letter-spacing:.14em; font-size:.8rem; color:var(--sky); text-decoration:none; }
    .nav-right a { font-size:.85rem; color:var(--ink-soft); text-decoration:none; margin-left:1rem; }
    .nav-right a:hover, .nav-right a.on { color:var(--sky); }
    .nav-right a.on { font-weight:600; }
    main { max-width:1060px; margin:0 auto; padding:2rem 1.2rem 4rem; }
    .eyebrow { font-family:var(--f-mono); font-size:.72rem; letter-spacing:.14em; text-transform:uppercase; color:var(--glow); margin:0; }
    h1 { font-size:clamp(1.7rem,4.5vw,2.4rem); line-height:1.2; margin:.4rem 0 .6rem; }
    h2 { font-size:1.3rem; margin:2.4rem 0 .4rem; padding-top:1.1rem; border-top:1px solid var(--divider); }
    p, li { color:var(--ink-soft); }
    .lead { font-size:1.05rem; color:var(--ink); }
    .aviso { background:#EAF2F9; border-left:4px solid var(--sky); padding:.8rem 1rem; border-radius:6px; margin:1.2rem 0; color:var(--ink); font-size:.95rem; }
    .tw { overflow-x:auto; margin:.6rem 0 1rem; }
    table { border-collapse:collapse; width:100%; font-size:.84rem; background:var(--white); }
    th, td { border:1px solid var(--divider); padding:.4rem .55rem; text-align:left; vertical-align:top; }
    th { background:#173F2A; color:#fff; font-weight:600; }
    tbody tr:nth-child(even) td { background:#F6F9FB; }
    .nota { font-size:.88rem; }
    a { color:var(--sky); }
    .down { display:inline-block; margin:.2rem .5rem .6rem 0; padding:.45rem .9rem; border:1px solid var(--sky); border-radius:6px; text-decoration:none; font-size:.88rem; }
    .grade-g { display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:.9rem; margin:.8rem 0; }
    figure { margin:0; background:var(--white); border:1px solid var(--divider); border-radius:8px; padding:.4rem .5rem .2rem; }
    figcaption { font-size:.8rem; color:var(--ink); } figcaption span { color:var(--glow); font-family:var(--f-mono); font-size:.7rem; margin-left:.3rem; }
    svg { width:100%; height:auto; display:block; }
    svg .grade { stroke:#E3ECF3; stroke-width:.6; } svg .eixo { font-size:7px; fill:#6E92A8; font-family:var(--f-mono); }
    svg .corte { stroke:#9AAFC0; stroke-width:.8; stroke-dasharray:3 2; }
    svg .curvaC { fill:none; stroke:var(--sky); stroke-width:1.5; } svg .curvaY { fill:none; stroke:var(--y); stroke-width:1.5; }
    .legenda { font-size:.85rem; color:var(--ink); } .legenda i { display:inline-block; width:1.4rem; height:3px; vertical-align:middle; margin:0 .3rem 0 .8rem; } .legenda i.c { background:var(--sky); } .legenda i.y { background:var(--y); } .legenda i.k { background:#9AAFC0; height:0; border-top:2px dashed #9AAFC0; }
    .barras { margin:.8rem 0; } .b-linha { display:flex; align-items:center; gap:.6rem; margin:.18rem 0; font-size:.82rem; }
    .b-nome { width:9.5rem; color:var(--ink); } .b-trilho { flex:1; display:flex; height:1.35rem; border-radius:4px; overflow:hidden; background:#E3ECF3; }
    .b-trilho span { color:#fff; font-size:.72rem; display:flex; align-items:center; justify-content:center; font-family:var(--f-mono); }
    .b-d { background:#2E86C1; } .b-e { background:#173F2A; } .b-a { background:#B9770E; }
    .leg2 span { display:inline-block; padding:.05rem .5rem; margin-right:.5rem; border-radius:3px; color:#fff; font-size:.78rem; } .leg2 .b-d { background:#2E86C1; } .leg2 .b-e { background:#173F2A; } .leg2 .b-a { background:#B9770E; }
    footer { max-width:1060px; margin:0 auto; padding:0 1.2rem 3rem; font-size:.85rem; color:var(--ink-soft); }
    [data-lang] { display:none; }
    html[lang="pt"] [data-lang="pt"], html[lang="en"] [data-lang="en"] { display:block; }
    html[lang="pt"] span[data-lang="pt"], html[lang="en"] span[data-lang="en"] { display:inline; }
"""

TEXTOS = {
    "pt": {
        "titulo": "Perfis NTA por idade de 21 países | AINU.Systems",
        "desc": "Consumo e renda do trabalho por idade de 21 países (National Transfer Accounts), parcela de cada coorte no consumo e janela de superávit do ciclo de vida. Estudo exploratório.",
        "eyebrow": "National Transfer Accounts · Perfis por idade",
        "h1": "Perfis NTA por idade de 21 países",
        "lead": "Consumo e renda do trabalho por idade de 21 países, vindos do portal National Transfer Accounts (e, para o Japão e a Coreia do Sul, das fontes nacionais), com a parcela de cada coorte (Descendentes, Estruturadores e Ascendentes) no consumo e a janela do ciclo de vida em que a renda do trabalho supera o consumo.",
        "aviso": "<strong>Estudo exploratório.</strong> Os perfis são os publicados pelas equipes nacionais, em moeda local nominal, com valores arredondados a 5 algarismos significativos. As parcelas por coorte e as janelas são <strong>estimativas</strong> do AINU.Systems (cortes etários por Perfil estrutural e população da ONU de 2025), sem revisão por pares.",
        "a_h": "A. Cobertura", "a_p": "Países, anos e fontes. Os 10 países incluídos em 18/11/2026 (Rússia, Suécia, Tailândia, Austrália, Polônia, África do Sul, Indonésia, Alemanha, Chile e Costa Rica) usam o último ano disponível no portal.",
        "b_h": "B. Curvas por idade", "b_p": "Consumo C(a) e renda do trabalho YL(a) divididos pela média da renda do trabalho de 30 a 49 anos de cada país (prática usual da NTA), para comparar as formas entre moedas. As linhas tracejadas mostram os cortes etários dos coortes usados pelo AINU.Systems. Eixo horizontal: idade; valores acima de 2 são cortados.",
        "leg": '<span class="legenda"><i class="c"></i>consumo C <i class="y"></i>renda do trabalho YL <i class="k"></i>cortes dos coortes</span>',
        "c_h": "C. Quem consome: parcela de cada coorte", "c_p": "Participação (%) no consumo total (privado e público) de Descendentes, Estruturadores e Ascendentes: perfil NTA × população da ONU de 2025, com os cortes etários de cada país.",
        "d_h": "D. Janela de superávit do ciclo de vida", "d_p": "Idades em que a renda do trabalho supera o consumo, e a distância dessa janela aos cortes dos coortes. Hipótese de trabalho: o ciclo de vida só vira superávit alguns anos depois do corte dos Descendentes e termina perto do corte dos Ascendentes.",
        "d_n": "<strong>Cuidado ao comparar países:</strong> a janela bruta depende do <em>nível</em> relativo das duas curvas, não só da forma. No México (2014), por exemplo, o consumo ficou muito próximo da renda do trabalho em todas as idades (razão agregada de 0,46), e a janela se reduz a 45–46 anos; os dados conferem com o portal.",
        "e_h": "E. Fontes, atribuição e limites",
        "e_li": [
            "<strong>Fonte:</strong> National Transfer Accounts Project, <a href='https://ntaccounts.org/' target='_blank' rel='noopener'>ntaccounts.org</a> (acessado em novembro de 2026), tipo \"Smooth Mean\". Para uso comparativo: Lee, R.; Mason, A. (eds.) (2011), <em>Population Aging and the Generational Economy</em>, Edward Elgar.",
            "<strong>Japão:</strong> consumo e renda do trabalho do IPSS (ano fiscal 2019, versão 3.0): National Institute of Population and Social Security Research (2025). <strong>Coreia do Sul:</strong> KOSIS, tabela DT_1NTA2003 (2024), por orientação da rede NTA.",
            "<strong>Equipes nacionais</strong> indicadas pelo portal: Rússia, M. Denisenko e V. Kozlov; Suécia, N. Adjei, T. Lindh e G. Öberg; Costa Rica, P. Jiménez-Fontana. Nos demais países o portal não indica a equipe no arquivo; citar o portal NTA.",
            "<strong>Limites:</strong> perfil suavizado de um ano que pode diferir do ano da população; a última idade do perfil (80, 85, 90, 95 ou 100 anos) é estendida às idades acima; consumo total, sem separar privado e público; moeda local nominal; estimativas, não observações.",
            "<strong>Costa Rica</strong> (2013): o perfil do portal, com a população da ONU de 2013 e cortes 0–22 / 23–60 / 61+, reproduz as participações do Paper 3 (31,5 / 56,2 / 12,3 %); a tabela acima usa a população de 2025, como nos demais países. Os arquivos originais do CCP-UCR não são redistribuídos.",
            "Correções ou pedidos de retirada de qualquer país: abra uma <em>issue</em> em <a href='https://github.com/itibere-muarrek/Ainu-Narayama/issues' target='_blank' rel='noopener'>github.com/itibere-muarrek/Ainu-Narayama</a>.",
        ],
        "down": "Dados e conferência",
        "d_csv": "Perfis (CSV, GitHub)", "d_json": "Valores derivados (JSON)", "d_fon": "Fontes e licenças", "d_pap": "Paper 3 (método)", "d_pdf": "Apresentação (PDF)",
        "nav_metodo": "Método do Paper 3",
        "rodape": f"Itiberê L. G. C. Muarrek · AINU.Systems Research (pesquisa independente) · Atualizado em {HOJE.day:02d}/{HOJE.month:02d}/{HOJE.year}.",
    },
    "en": {
        "titulo": "NTA age profiles of 21 countries | AINU.Systems",
        "desc": "Consumption and labor income by age for 21 countries (National Transfer Accounts), each cohort's share of consumption and the life-cycle surplus window. Exploratory study.",
        "eyebrow": "National Transfer Accounts · Age profiles",
        "h1": "NTA age profiles of 21 countries",
        "lead": "Consumption and labor income by age for 21 countries, from the National Transfer Accounts portal (and, for Japan and South Korea, from the national sources), with each cohort's share of consumption (Descendants, Structurers and Ascendants) and the life-cycle window in which labor income exceeds consumption.",
        "aviso": "<strong>Exploratory study.</strong> The profiles are those published by the national teams, in nominal local currency, with values rounded to 5 significant digits. The cohort shares and windows are AINU.Systems <strong>estimates</strong> (age cut-offs by structural Profile and 2025 UN population), not peer reviewed.",
        "a_h": "A. Coverage", "a_p": "Countries, years and sources. The 10 countries added on 18 Nov 2026 (Russia, Sweden, Thailand, Australia, Poland, South Africa, Indonesia, Germany, Chile and Costa Rica) use the latest year available in the portal.",
        "b_h": "B. Age curves", "b_p": "Consumption C(a) and labor income YL(a) divided by each country's mean labor income at ages 30–49 (the usual NTA practice), so shapes can be compared across currencies. Dashed lines show the cohort age cut-offs used by AINU.Systems. Horizontal axis: age; values above 2 are clipped.",
        "leg": '<span class="legenda"><i class="c"></i>consumption C <i class="y"></i>labor income YL <i class="k"></i>cohort cut-offs</span>',
        "c_h": "C. Who consumes: each cohort's share", "c_p": "Share (%) of total consumption (private and public) of Descendants, Structurers and Ascendants: NTA profile × 2025 UN population, with each country's age cut-offs.",
        "d_h": "D. Life-cycle surplus window", "d_p": "Ages at which labor income exceeds consumption, and the distance of that window from the cohort cut-offs. Working hypothesis: the life cycle turns to surplus a few years after the Descendants cut-off and ends near the Ascendants cut-off.",
        "d_n": "<strong>Caution when comparing countries:</strong> the raw window depends on the relative <em>level</em> of the two curves, not only on their shape. In Mexico (2014), for instance, consumption stayed very close to labor income at all ages (aggregate ratio of 0.46) and the window shrinks to ages 45–46; the data match the portal.",
        "e_h": "E. Sources, attribution and limits",
        "e_li": [
            "<strong>Source:</strong> National Transfer Accounts Project, <a href='https://ntaccounts.org/' target='_blank' rel='noopener'>ntaccounts.org</a> (accessed November 2026), type \"Smooth Mean\". For comparative use: Lee, R.; Mason, A. (eds.) (2011), <em>Population Aging and the Generational Economy</em>, Edward Elgar.",
            "<strong>Japan:</strong> consumption and labor income from IPSS (fiscal year 2019, version 3.0): National Institute of Population and Social Security Research (2025). <strong>South Korea:</strong> KOSIS, table DT_1NTA2003 (2024), as advised by the NTA network.",
            "<strong>National teams</strong> listed by the portal: Russia, M. Denisenko and V. Kozlov; Sweden, N. Adjei, T. Lindh and G. Öberg; Costa Rica, P. Jiménez-Fontana. For the other countries the portal file does not name the team; cite the NTA portal.",
            "<strong>Limits:</strong> smoothed profile of one year that may differ from the population year; the last age of the profile (80, 85, 90, 95 or 100) is extended to older ages; total consumption, private and public together; nominal local currency; estimates, not observations.",
            "<strong>Costa Rica</strong> (2013): the portal profile, with the 2013 UN population and cut-offs 0–22 / 23–60 / 61+, reproduces the shares in Paper 3 (31.5 / 56.2 / 12.3%); the table above uses the 2025 population, as for the other countries. The original CCP-UCR files are not redistributed.",
            "Corrections or removal requests for any country: open an issue at <a href='https://github.com/itibere-muarrek/Ainu-Narayama/issues' target='_blank' rel='noopener'>github.com/itibere-muarrek/Ainu-Narayama</a>.",
        ],
        "down": "Data and verification",
        "d_csv": "Profiles (CSV, GitHub)", "d_json": "Derived values (JSON)", "d_fon": "Sources and licenses", "d_pap": "Paper 3 (method)", "d_pdf": "Presentation (PDF)",
        "nav_metodo": "Paper 3 method",
        "rodape": f"Itiberê L. G. C. Muarrek · AINU.Systems Research (independent research) · Updated {HOJE.day} Nov {HOJE.year}.",
    },
}


def pagina(linhas: list[dict]) -> str:
    tb, gr, br = tabelas(linhas), grade(linhas), barras(linhas)
    partes = []
    for lang in ("pt", "en"):
        t = TEXTOS[lang]
        a, c = tb[lang]
        leg2 = {"pt": '<p class="leg2"><span class="b-d">Descendentes</span><span class="b-e">Estruturadores</span><span class="b-a">Ascendentes</span></p>',
                "en": '<p class="leg2"><span class="b-d">Descendants</span><span class="b-e">Structurers</span><span class="b-a">Ascendants</span></p>'}[lang]
        lis = "".join(f"<li>{x}</li>" for x in t["e_li"])
        partes.append(f"""<div data-lang="{lang}">
  <p class="eyebrow">{t['eyebrow']}</p>
  <h1>{t['h1']}</h1>
  <p class="lead">{t['lead']}</p>
  <div class="aviso">{t['aviso']}</div>
  <p><strong>{t['down']}:</strong> <a class="down" href="{URL_CSV}" target="_blank" rel="noopener">{t['d_csv']}</a><a class="down" href="perfis_nta_derivados.json" download>{t['d_json']}</a><a class="down" href="{URL_FONTES}" target="_blank" rel="noopener">{t['d_fon']}</a><a class="down" href="perfis-nta-apresentacao-{lang}.pdf" download>{t['d_pdf']}</a><a class="down" href="../metodo-paper3/">{t['d_pap']}</a></p>
  <h2>{t['a_h']}</h2><p>{t['a_p']}</p><div class="tw">{a}</div>
  <h2>{t['b_h']}</h2><p>{t['b_p']}</p><p>{t['leg']}</p>{gr[lang]}
  <h2>{t['c_h']}</h2><p>{t['c_p']}</p>{leg2}{br[lang]}
  <h2>{t['d_h']}</h2><p>{t['d_p']}</p><div class="tw">{c}</div><p class="nota">{t['d_n']}</p>
  <h2>{t['e_h']}</h2><ul>{lis}</ul>
</div>""")
    return f"""<!DOCTYPE html>
<html lang="pt">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{TEXTOS['pt']['titulo']}</title>
  <meta name="description" content="{TEXTOS['pt']['desc']}">
  <meta name="robots" content="index, follow">
  <link rel="icon" type="image/png" href="../Ainu.png">
  <link rel="canonical" href="https://ainu.systems/perfis-nta/">
  <style>{CSS}  </style>
</head>
<body>
<nav>
  <a class="nav-logo" href="../">AINU.SYSTEMS</a>
  <div class="nav-right">
    <a href="../metodo-paper3/"><span data-lang="pt">{TEXTOS['pt']['nav_metodo']}</span><span data-lang="en">{TEXTOS['en']['nav_metodo']}</span></a>
    <a id="lp" href="?lang=pt">PT</a><a id="le" href="?lang=en">EN</a>
  </div>
</nav>
<main>
{chr(10).join(partes)}
</main>
<footer>
  <p><span data-lang="pt">{TEXTOS['pt']['rodape']}</span><span data-lang="en">{TEXTOS['en']['rodape']}</span></p>
</footer>
<script>
(function () {{
  var pedido = new URLSearchParams(location.search).get('lang');
  var salvo = null; try {{ salvo = localStorage.getItem('ainu_lang'); }} catch (e) {{}}
  var nav = (navigator.language || 'pt').slice(0, 2);
  function normaliza(l) {{ return l === 'pt' ? 'pt' : (l ? 'en' : null); }}
  var lang = normaliza(pedido) || normaliza(salvo) || (nav === 'pt' ? 'pt' : 'en');
  document.documentElement.lang = lang;
  document.getElementById('l' + lang[0]).className = 'on';
  document.title = lang === 'pt' ? {json.dumps(TEXTOS['pt']['titulo'], ensure_ascii=False)} : {json.dumps(TEXTOS['en']['titulo'], ensure_ascii=False)};
}})();
</script>
</body>
</html>
"""


def main() -> None:
    linhas = calcular()
    PAGINA.mkdir(parents=True, exist_ok=True)
    (PAGINA / "index.html").write_text(pagina(linhas), encoding="utf-8")
    derivados = [{k: v for k, v in l.items() if k != "curvas_norm"} for l in linhas]
    (PAGINA / "perfis_nta_derivados.json").write_text(json.dumps(
        {"gerado_em": HOJE.isoformat(), "fonte": "National Transfer Accounts Project (ntaccounts.org); IPSS (Japão); KOSIS (Coreia do Sul)",
         "observacao": "Estimativas do AINU.Systems: cortes etários por Perfil e população da ONU de 2025; perfis em moeda local nominal, 5 algarismos significativos.",
         "paises": derivados}, ensure_ascii=False, indent=1), encoding="utf-8")
    mapa = RAIZ / "landing" / "ainu-systems" / "sitemap.xml"
    x = mapa.read_bytes().decode("utf-8")
    if "perfis-nta" not in x:
        nl = "\r\n" if "\r\n" in x else "\n"
        bloco = (f"  <url>{nl}    <loc>https://ainu.systems/perfis-nta/</loc>{nl}    <lastmod>{HOJE.isoformat()}</lastmod>{nl}"
                 f"    <changefreq>monthly</changefreq>{nl}    <priority>0.5</priority>{nl}  </url>{nl}")
        x = x.replace("</urlset>", bloco + "</urlset>")
        mapa.write_bytes(x.encode("utf-8"))
    print("ok:", PAGINA / "index.html", f"({(PAGINA / 'index.html').stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
