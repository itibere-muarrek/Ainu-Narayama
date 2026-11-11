"""
Bloco "Última atualização / Novo:" abaixo do logo das duas landings (ainu.systems e narayama.live), em 9 idiomas.

Como usar: ao publicar uma mudança, edite DATA e ITENS abaixo (uma lista curta e objetiva por site, em todos os
idiomas) e rode  python scripts/atualizar_novidades.py . O script reescreve só os trechos marcados com NOV nos dois
index.html (CSS, bloco HTML sob o logo e as chaves nov_* de cada idioma); é idempotente.

Regra de conteúdo: só o que é verdade na versão publicada; cada item uma linha; sem adjetivos.
Traduções feitas por IA, sem revisão nativa (como no resto das landings).
"""

import json
import re
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PAGINAS = {
    "ainu-systems": RAIZ / "landing" / "ainu-systems" / "index.html",
    "narayama-live": RAIZ / "landing" / "narayama-live" / "index.html",
}

DATA = date(2026, 11, 10)
IDIOMAS = ["pt", "en", "es", "fr", "ko", "it", "zh", "ja", "fi"]

# --------------------------------------------------------------------------- textos fixos
ULTIMA = {  # rótulo + separador; a data vem formatada abaixo
    "pt": "Última atualização: ", "en": "Last updated: ", "es": "Última actualización: ", "fr": "Dernière mise à jour : ",
    "ko": "최종 업데이트: ", "it": "Ultimo aggiornamento: ", "zh": "最近更新：", "ja": "最終更新：", "fi": "Viimeksi päivitetty: ",
}
ROTULO = {  # por site: "Novo:" quando há novidade própria; "Atualizado:" quando só houve reprocessamento
    "ainu-systems": {
        "pt": "Novo:", "en": "New:", "es": "Novedades:", "fr": "Nouveau :", "ko": "새 소식:", "it": "Novità:",
        "zh": "新增：", "ja": "新着：", "fi": "Uutta:",
    },
    "narayama-live": {
        "pt": "Atualizado:", "en": "Updated:", "es": "Actualizado:", "fr": "Mis à jour :", "ko": "업데이트:",
        "it": "Aggiornato:", "zh": "已更新：", "ja": "更新：", "fi": "Päivitetty:",
    },
}


def data_fmt(lang: str) -> str:
    d = DATA
    mes_en = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][d.month - 1]
    return {
        "pt": f"{d.day:02d}/{d.month:02d}/{d.year}", "es": f"{d.day:02d}/{d.month:02d}/{d.year}",
        "fr": f"{d.day:02d}/{d.month:02d}/{d.year}", "it": f"{d.day:02d}/{d.month:02d}/{d.year}",
        "en": f"{d.day} {mes_en} {d.year}", "fi": f"{d.day}.{d.month}.{d.year}",
        "ja": f"{d.year}年{d.month}月{d.day}日", "zh": f"{d.year}年{d.month}月{d.day}日",
        "ko": f"{d.year}년 {d.month}월 {d.day}일",
    }[lang]


# --------------------------------------------------------------------------- o que mudou (edite aqui)
ITENS = {
    "ainu-systems": {
        "pt": [
            "Costa Rica e Paraguai no índice N*: agora são 30 países.",
            "Página “Condição média” (colaboradores): fecundidade a 2,1 contra a tendência da ONU, de 2024 a 2099.",
            "A simulação por coorte inclui Costa Rica e Paraguai.",
        ],
        "en": [
            "Costa Rica and Paraguay added to the N* index: now 30 countries.",
            "New “Average condition” page (collaborators): fertility at 2.1 vs. the UN trend, 2024–2099.",
            "The cohort simulation now includes Costa Rica and Paraguay.",
        ],
        "es": [
            "Costa Rica y Paraguay en el índice N*: ahora son 30 países.",
            "Nueva página «Condición media» (colaboradores): fecundidad de 2,1 frente a la tendencia de la ONU, de 2024 a 2099.",
            "La simulación por cohortes incluye Costa Rica y Paraguay.",
        ],
        "fr": [
            "Costa Rica et Paraguay dans l’indice N* : 30 pays désormais.",
            "Nouvelle page « Condition moyenne » (collaborateurs) : fécondité à 2,1 contre la tendance de l’ONU, de 2024 à 2099.",
            "La simulation par cohortes inclut le Costa Rica et le Paraguay.",
        ],
        "ko": [
            "N* 지수에 코스타리카와 파라과이 추가: 이제 30개국입니다.",
            "새 페이지 ‘평균 조건’(협력자용): 출산율 2.1과 유엔 추세 비교, 2024–2099년.",
            "코호트 시뮬레이션에 코스타리카와 파라과이가 포함됩니다.",
        ],
        "it": [
            "Costa Rica e Paraguay nell’indice N*: ora sono 30 paesi.",
            "Nuova pagina «Condizione media» (collaboratori): fecondità a 2,1 contro la tendenza dell’ONU, dal 2024 al 2099.",
            "La simulazione per coorti include Costa Rica e Paraguay.",
        ],
        "zh": [
            "N* 指数新增哥斯达黎加和巴拉圭：现为 30 个国家。",
            "新页面“平均状况”（合作者）：生育率 2.1 与联合国趋势对比，2024–2099 年。",
            "分队列模拟已包含哥斯达黎加和巴拉圭。",
        ],
        "ja": [
            "N* 指数にコスタリカとパラグアイを追加：30か国になりました。",
            "新ページ「平均的条件」（協力者向け）：出生率 2.1 と国連トレンドの比較（2024〜2099年）。",
            "コホート別シミュレーションにコスタリカとパラグアイを追加。",
        ],
        "fi": [
            "Costa Rica ja Paraguay N*-indeksissä: nyt 30 maata.",
            "Uusi sivu ”Keskimääräinen tila” (yhteistyökumppaneille): hedelmällisyys 2,1:ssä verrattuna YK:n trendiin, 2024–2099.",
            "Kohorttisimulaatio sisältää nyt Costa Rican ja Paraguayn.",
        ],
    },
    "narayama-live": {
        "pt": [
            "Dados da ONU (WPP 2024) reprocessados: os 11 países desta página mantêm os mesmos valores de N*_Obs.",
            "Costa Rica e Paraguai entraram no ainu.systems (fora deste painel de 11 países).",
        ],
        "en": [
            "UN data (WPP 2024) reprocessed: the 11 countries on this page keep the same N*_Obs values.",
            "Costa Rica and Paraguay were added to ainu.systems (outside this 11-country panel).",
        ],
        "es": [
            "Datos de la ONU (WPP 2024) reprocesados: los 11 países de esta página mantienen los mismos valores de N*_Obs.",
            "Costa Rica y Paraguay se añadieron a ainu.systems (fuera de este panel de 11 países).",
        ],
        "fr": [
            "Données de l’ONU (WPP 2024) retraitées : les 11 pays de cette page gardent les mêmes valeurs de N*_Obs.",
            "Le Costa Rica et le Paraguay ont été ajoutés à ainu.systems (hors de ce panneau de 11 pays).",
        ],
        "ko": [
            "유엔 데이터(WPP 2024) 재처리: 이 페이지의 11개국 N*_Obs 값은 그대로입니다.",
            "코스타리카와 파라과이는 ainu.systems에 추가되었습니다(이 11개국 패널에는 포함되지 않음).",
        ],
        "it": [
            "Dati dell’ONU (WPP 2024) rielaborati: gli 11 paesi di questa pagina mantengono gli stessi valori di N*_Obs.",
            "Costa Rica e Paraguay sono stati aggiunti a ainu.systems (fuori da questo pannello di 11 paesi).",
        ],
        "zh": [
            "联合国数据（WPP 2024）已重新处理：本页 11 个国家的 N*_Obs 数值不变。",
            "哥斯达黎加和巴拉圭已加入 ainu.systems（不在本页的 11 国面板内）。",
        ],
        "ja": [
            "国連データ（WPP 2024）を再処理：このページの11か国の N*_Obs 値は変わりません。",
            "コスタリカとパラグアイは ainu.systems に追加されました（この11か国のパネルの対象外）。",
        ],
        "fi": [
            "YK:n tiedot (WPP 2024) käsitelty uudelleen: tämän sivun 11 maan N*_Obs-arvot pysyvät samoina.",
            "Costa Rica ja Paraguay lisättiin ainu.systems-sivustoon (tämän 11 maan paneelin ulkopuolella).",
        ],
    },
}

# --------------------------------------------------------------------------- CSS e HTML
CSS = """/* NOV-CSS-BEGIN */
    .novidades {
      margin: -1.2rem 0 1.9rem;
      max-width: 36rem;
      width: 100%;
      font-size: 0.82rem;
      line-height: 1.5;
      color: var(--ink-soft);
      text-align: left;
    }
    .novidades .nov-data {
      font-family: var(--f-mono);
      font-size: 0.7rem;
      letter-spacing: 0.08em;
      text-align: center;
      margin-bottom: 0.7rem;
    }
    .novidades .nov-rotulo { font-weight: 700; color: var(--sky); margin-bottom: 0.2rem; }
    .novidades .nov-lista { margin: 0; padding: 0 0 0 1.1rem; border-left: 2px solid var(--divider); list-style: none; }
    .novidades .nov-lista li { margin: 0.15rem 0 0.15rem 0.2rem; }
    .novidades .nov-lista li::before { content: "·"; color: var(--sky); font-weight: 700; margin-right: 0.45rem; margin-left: -0.9rem; }
    /* NOV-CSS-END */"""


def lista_html(itens):
    return "".join(f"<li>{i}</li>" for i in itens)


def bloco_html(site: str) -> str:
    return (
        "<!-- NOV-BEGIN -->\n"
        '    <div class="novidades">\n'
        f'      <p class="nov-data" data-i18n="nov_ultima">{ULTIMA["pt"]}{data_fmt("pt")}</p>\n'
        f'      <p class="nov-rotulo" data-i18n="nov_novo">{ROTULO[site]["pt"]}</p>\n'
        f'      <ul class="nov-lista" data-i18n="nov_lista">{lista_html(ITENS[site]["pt"])}</ul>\n'
        "    </div>\n"
        "    <!-- NOV-END -->"
    )


def chaves_idioma(site: str, lang: str, ident: str) -> str:
    j = lambda s: json.dumps(s, ensure_ascii=False)
    return "".join(
        f"{ident}{k}: {j(v)}, // NOV\n"
        for k, v in (
            ("nov_ultima", ULTIMA[lang] + data_fmt(lang)),
            ("nov_novo", ROTULO[site][lang]),
            ("nov_lista", lista_html(ITENS[site][lang])),
        )
    )


def aplicar(site: str, caminho: Path) -> None:
    bruto = caminho.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in bruto else "\n"
    s = bruto.replace("\r\n", "\n")

    # 1) limpa o que já foi inserido
    s = re.sub(r"[ \t]*/\* NOV-CSS-BEGIN \*/.*?/\* NOV-CSS-END \*/\n?", "", s, flags=re.S)
    s = re.sub(r"[ \t]*<!-- NOV-BEGIN -->.*?<!-- NOV-END -->\n?", "", s, flags=re.S)
    s = re.sub(r"^[ \t]*nov_\w+: .*// NOV\n", "", s, flags=re.M)

    # 2) CSS antes do primeiro </style>
    assert s.count("</style>") >= 1
    s = s.replace("</style>", CSS + "\n  </style>", 1)

    # 3) HTML logo depois da imagem do logo do hero
    m = re.search(r'(<img [^>]*class="hero-logo"[^>]*>\n)', s)
    assert m, f"{site}: logo do hero não encontrado"
    s = s[: m.end()] + "    " + bloco_html(site) + "\n" + s[m.end():]

    # 4) chaves em cada idioma
    for lang in IDIOMAS:
        m = re.search(rf"^(\s*){lang}: \{{\n", s, flags=re.M)
        assert m, f"{site}: bloco do idioma {lang} não encontrado"
        ident = m.group(1) + "  "
        s = s[: m.end()] + chaves_idioma(site, lang, ident) + s[m.end():]

    caminho.write_bytes(s.replace("\n", nl).encode("utf-8"))
    print("ok", site, caminho.relative_to(RAIZ))


if __name__ == "__main__":
    for site, caminho in PAGINAS.items():
        aplicar(site, caminho)
