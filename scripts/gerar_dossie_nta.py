"""
Gera o PDF curto de apresentação dos perfis NTA de 20 países (PT e EN), a partir dos mesmos números da página pública
(scripts/gerar_perfis_nta.py): resumo, curvas por idade, parcela das coortes, janela de superávit, fontes e atribuição.

Saídas:  landing/ainu-systems/perfis-nta/perfis-nta-apresentacao-pt.pdf  e  ...-en.pdf
Rodar da raiz do repositório:  python scripts/gerar_dossie_nta.py
Depende de PyMuPDF (pymupdf), só para este PDF.
"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

import pymupdf

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "scripts"))

import gerar_perfis_nta as g  # noqa: E402
from src.i18n import nome_pais  # noqa: E402

SAIDA = g.PAGINA


def svg_grade(linhas: list[dict], lang: str) -> bytes:
    """Grade 4 x 5 de curvas, com estilos embutidos (o SVG da página usa CSS externo)."""
    cw, ch, cols = 240, 168, 4
    rows = (len(linhas) + cols - 1) // cols
    W, H = cols * cw, rows * ch
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">', f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    for i, l in enumerate(linhas):
        ox, oy = (i % cols) * cw, (i // cols) * ch
        interno = g.svg(l)
        interno = interno.replace('class="grade"', 'stroke="#E3ECF3" stroke-width="0.6"').replace('class="eixo"', 'font-size="7" fill="#6E92A8" font-family="Helvetica"')
        interno = interno.replace('class="corte"', 'stroke="#9AAFC0" stroke-width="0.8" stroke-dasharray="3 2"')
        interno = interno.replace('class="curvaC"', 'fill="none" stroke="#1B6CA8" stroke-width="1.5"').replace('class="curvaY"', 'fill="none" stroke="#C0392B" stroke-width="1.5"')
        interno = re.sub(r"^<svg[^>]*>", "", interno).replace("</svg>", "")
        interno = f'<g transform="translate({ox},{oy + 16})">{interno}</g>'
        s.append(f'<text x="{ox + 8}" y="{oy + 12}" font-size="10" font-family="Helvetica" font-weight="bold" fill="#0D1B2A">{nome_pais(l["iso"], lang)} <tspan font-weight="normal" fill="#6E92A8" font-size="8">{l["ano_c_yl"]}</tspan></text>')
        s.append(interno)
    s.append("</svg>")
    return "".join(s).encode("utf-8")


def svg_barras(linhas: list[dict], lang: str) -> bytes:
    ls = sorted(linhas, key=lambda z: -z["cfcc_pct"][2])
    lh, W = 17, 620
    H = len(ls) * lh + 6
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">', f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    x0, larg = 120, W - 130
    for i, l in enumerate(ls):
        y = 3 + i * lh
        s.append(f'<text x="4" y="{y + 12}" font-size="10" font-family="Helvetica" fill="#0D1B2A">{nome_pais(l["iso"], lang)}</text>')
        x = x0
        for v, cor in zip(l["cfcc_pct"], ("#2E86C1", "#173F2A", "#B9770E")):
            w = larg * v / 100
            s.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="14" fill="{cor}"/><text x="{x + w / 2:.1f}" y="{y + 11}" font-size="8" font-family="Helvetica" fill="#ffffff" text-anchor="middle">{v:.0f}</text>')
            x += w
    s.append("</svg>")
    return "".join(s).encode("utf-8")


def png(svg_bytes: bytes, destino: Path, dpi: int = 170) -> None:
    doc = pymupdf.open(stream=svg_bytes, filetype="svg")
    doc[0].get_pixmap(dpi=dpi).save(str(destino))


TEXTO = {
    "pt": {
        "t": "Perfis NTA por idade de 20 países", "sub": "Apresentação dos dados ampliados · AINU.Systems · 18 de novembro de 2026",
        "resumo_h": "O que foi acrescentado",
        "resumo": ["Perfis por idade de consumo (C), renda do trabalho (YL) e, quando existe, poupança (S) de <b>20 países</b>: os 11 que já estavam no repositório e <b>9 novos</b> do portal National Transfer Accounts (Rússia, Suécia, Tailândia, Austrália, Polônia, África do Sul, Indonésia, Alemanha e Chile), no último ano de cada um.",
                   "Para cada país, estimamos a <b>parcela de cada coorte</b> (Descendentes, Estruturadores e Ascendentes) no consumo total e a <b>janela do ciclo de vida</b> em que a renda do trabalho supera o consumo, comparada aos cortes etários que o AINU.Systems usa.",
                   "Tudo é reprodutível: código, testes e dados estão no repositório público; a página interativa traz as curvas, as tabelas e os arquivos para conferência."],
        "links_h": "Para verificar",
        "links": [("Página com curvas e tabelas", "https://ainu.systems/perfis-nta/"), ("Perfis (CSV)", g.URL_CSV), ("Fontes, atribuição e licenças", g.URL_FONTES), ("Termos de dados de terceiros", g.URL_TERCEIROS),
                  ("Paper 3 (texto integral, Zenodo)", "https://doi.org/10.5281/zenodo.24326808")],
        "curvas_h": "Curvas por idade", "curvas_p": "Consumo (azul) e renda do trabalho (vermelho), cada um dividido pela média da renda do trabalho de 30 a 49 anos do próprio país. Linhas tracejadas: cortes dos coortes.",
        "coortes_h": "Parcela de cada coorte no consumo (%)", "coortes_p": "Azul: Descendentes; verde: Estruturadores; ocre: Ascendentes. Perfil NTA × população da ONU de 2025, com os cortes etários de cada país.",
        "janela_h": "Janela de superávit do ciclo de vida", "janela_cab": ["País", "Cortes D/A", "Desc. %", "Estr. %", "Asc. %", "Superávit", "Início−D", "Fim−A"],
        "janela_n": "Hipótese de trabalho: o ciclo de vida só vira superávit alguns anos depois do corte dos Descendentes e termina perto do corte dos Ascendentes. Cuidado: a janela bruta depende do nível relativo das curvas (México 2014: razão agregada de 0,46, janela de 45–46 anos; os dados conferem com o portal).",
        "fontes_h": "Fontes, atribuição e limites",
        "fontes": ["National Transfer Accounts Project, ntaccounts.org (acessado em novembro de 2026), tipo \"Smooth Mean\". Uso comparativo: Lee, R.; Mason, A. (eds.) (2011), <i>Population Aging and the Generational Economy</i>, Edward Elgar.",
                   "Japão: IPSS (ano fiscal 2019, v3.0). Coreia do Sul: KOSIS, tabela DT_1NTA2003 (2024). Equipes nacionais indicadas pelo portal: Rússia, M. Denisenko e V. Kozlov; Suécia, N. Adjei, T. Lindh e G. Öberg.",
                   "Valores arredondados a 5 algarismos significativos, em moeda local nominal. Perfis suavizados de um ano que pode diferir do ano da população; a última idade do perfil é estendida às idades acima; consumo total (privado e público). As parcelas e janelas são <b>estimativas exploratórias</b> do AINU.Systems, sem revisão por pares.",
                   "Os 9 países novos foram incluídos em 18/11/2026 com a atribuição que o portal pede; correções ou pedidos de retirada são bem-vindos (issues no repositório)."],
        "rod": "Itiberê L. G. C. Muarrek · AINU.Systems Research (pesquisa independente)",
    },
    "en": {
        "t": "NTA age profiles of 20 countries", "sub": "Presentation of the expanded data · AINU.Systems · 18 November 2026",
        "resumo_h": "What was added",
        "resumo": ["Age profiles of consumption (C), labor income (YL) and, where available, saving (S) for <b>20 countries</b>: the 11 already in the repository and <b>9 new</b> ones from the National Transfer Accounts portal (Russia, Sweden, Thailand, Australia, Poland, South Africa, Indonesia, Germany and Chile), in each country's latest year.",
                   "For each country we estimate <b>each cohort's share</b> (Descendants, Structurers and Ascendants) of total consumption and the <b>life-cycle window</b> in which labor income exceeds consumption, compared with the age cut-offs AINU.Systems uses.",
                   "Everything is reproducible: code, tests and data are in the public repository; the interactive page offers the curves, tables and files for verification."],
        "links_h": "To verify",
        "links": [("Page with curves and tables", "https://ainu.systems/perfis-nta/"), ("Profiles (CSV)", g.URL_CSV), ("Sources, attribution and licenses", g.URL_FONTES), ("Third-party data terms", g.URL_TERCEIROS),
                  ("Paper 3 (full text, Zenodo)", "https://doi.org/10.5281/zenodo.24326808")],
        "curvas_h": "Age curves", "curvas_p": "Consumption (blue) and labor income (red), each divided by the country's mean labor income at ages 30–49. Dashed lines: cohort cut-offs.",
        "coortes_h": "Each cohort's share of consumption (%)", "coortes_p": "Blue: Descendants; green: Structurers; ochre: Ascendants. NTA profile × 2025 UN population, with each country's age cut-offs.",
        "janela_h": "Life-cycle surplus window", "janela_cab": ["Country", "Cuts D/A", "Desc. %", "Struct. %", "Asc. %", "Surplus", "Start−D", "End−A"],
        "janela_n": "Working hypothesis: the life cycle turns to surplus a few years after the Descendants cut-off and ends near the Ascendants cut-off. Caution: the raw window depends on the relative level of the curves (Mexico 2014: aggregate ratio of 0.46, window of ages 45–46; the data match the portal).",
        "fontes_h": "Sources, attribution and limits",
        "fontes": ["National Transfer Accounts Project, ntaccounts.org (accessed November 2026), type \"Smooth Mean\". For comparative use: Lee, R.; Mason, A. (eds.) (2011), <i>Population Aging and the Generational Economy</i>, Edward Elgar.",
                   "Japan: IPSS (fiscal year 2019, v3.0). South Korea: KOSIS, table DT_1NTA2003 (2024). National teams listed by the portal: Russia, M. Denisenko and V. Kozlov; Sweden, N. Adjei, T. Lindh and G. Öberg.",
                   "Values rounded to 5 significant digits, in nominal local currency. Smoothed profiles of one year that may differ from the population year; the last age of the profile is extended to older ages; total consumption (private and public). Shares and windows are <b>exploratory estimates</b> by AINU.Systems, not peer reviewed.",
                   "The 9 new countries were added on 18 Nov 2026 with the attribution the portal requests; corrections or removal requests are welcome (issues in the repository)."],
        "rod": "Itiberê L. G. C. Muarrek · AINU.Systems Research (independent research)",
    },
}


def html(lang: str, linhas: list[dict], pasta: Path) -> str:
    t = TEXTO[lang]
    css = ("body{font-family:sans-serif;font-size:10pt;color:#0D1B2A} h1{font-size:20pt;color:#173F2A;margin:0 0 2pt} h2{font-size:12.5pt;color:#1B6CA8;margin:12pt 0 3pt} "
           "p{margin:3pt 0} .sub{color:#6E92A8;font-size:9.5pt} li{margin:2pt 0} th{background-color:#173F2A;color:#ffffff;font-size:8.5pt;text-align:left} td{font-size:8.5pt} "
           ".rod{color:#6E92A8;font-size:8pt;margin-top:10pt}")
    res = "".join(f"<li>{x}</li>" for x in t["resumo"])
    lk = "".join(f'<li><a href="{u}">{n}</a><br><span class="sub">{u}</span></li>' for n, u in t["links"])
    tab = "<table width='100%' cellpadding='2'><tr>" + "".join(f"<th>{h}</th>" for h in t["janela_cab"]) + "</tr>"
    for l in sorted(linhas, key=lambda z: -z["cfcc_pct"][2]):
        d, e, a = l["cfcc_pct"]
        tab += (f"<tr><td>{nome_pais(l['iso'], lang)}</td><td>{l['corte_descendentes_ate']}/{l['corte_ascendentes_desde']}</td><td>{g.num(d, lang)}</td><td>{g.num(e, lang)}</td><td>{g.num(a, lang)}</td>"
                f"<td>{l['superavit'][0]}–{l['superavit'][1]}</td><td>{l['inicio_menos_corte_desc']:+d}</td><td>{l['fim_menos_corte_asc']:+d}</td></tr>")
    tab += "</table>"
    fo = "".join(f"<li>{x}</li>" for x in t["fontes"])
    return (f"<html><head><style>{css}</style></head><body><h1>{t['t']}</h1><p class='sub'>{t['sub']}</p>"
            f"<h2>{t['resumo_h']}</h2><ul>{res}</ul><h2>{t['links_h']}</h2><ul>{lk}</ul>"
            f"<h2>{t['curvas_h']}</h2><p>{t['curvas_p']}</p><p><img src='grade_{lang}.png' width='520'></p>"
            f"<h2>{t['coortes_h']}</h2><p>{t['coortes_p']}</p><p><img src='barras_{lang}.png' width='500'></p>"
            f"<h2>{t['janela_h']}</h2>{tab}<p>{t['janela_n']}</p>"
            f"<h2>{t['fontes_h']}</h2><ul>{fo}</ul><p class='rod'>{t['rod']}</p></body></html>")


def main() -> None:
    linhas = g.calcular()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        pasta = Path(tmp)
        for lang in ("pt", "en"):
            png(svg_grade(linhas, lang), pasta / f"grade_{lang}.png")
            png(svg_barras(linhas, lang), pasta / f"barras_{lang}.png")
            destino = SAIDA / f"perfis-nta-apresentacao-{lang}.pdf"
            story = pymupdf.Story(html=html(lang, linhas, pasta), archive=pymupdf.Archive(str(pasta)))
            bruto = pasta / f"bruto_{lang}.pdf"
            w = pymupdf.DocumentWriter(str(bruto))
            mediabox = pymupdf.paper_rect("a4")
            where = mediabox + (40, 40, -40, -40)
            more = True
            while more:
                dev = w.begin_page(mediabox)
                more, _ = story.place(where)
                story.draw(dev)
                w.end_page()
            w.close()
            doc = pymupdf.open(str(bruto))
            doc.subset_fonts()
            doc.save(str(destino), garbage=4, deflate=True, clean=True)
            doc.close()
            print("ok:", destino, f"({destino.stat().st_size // 1024} KB)", "páginas:", len(pymupdf.open(str(destino))))


if __name__ == "__main__":
    main()
