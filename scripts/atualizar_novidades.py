"""
Bloco "Última atualização / Novo:" abaixo do logo das duas landings (ainu.systems e narayama.live), em 9 idiomas.

Como usar: ao publicar uma mudança, edite DATA_SITE e ITENS abaixo (uma lista curta e objetiva por site, em todos os
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

# data por site: cada um só muda de data quando muda de fato
DATA_SITE = {"ainu-systems": date(2026, 11, 11), "narayama-live": date(2026, 11, 11)}
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


def data_fmt(lang: str, site: str) -> str:
    d = DATA_SITE[site]
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
            "Costa Rica no panorama (agora 12 países, igual ao narayama.live); card da Coreia do Sul corrigido para 0,48.",
            "Costa Rica no panorama (agora 12 países, igual ao narayama.live); card da Coreia do Sul corrigido para 0,48.",
            "Itália (C50/D50 → C30/D70) e Coreia do Sul (C80/D20 → C50/D50): perfis revistos pela regra de TFT por fonte; N*_Obs 2024 da Coreia 0,456 → 0,484 (Itália inalterado).",
            "Costa Rica: perfil estrutural passou de C100 para C50/D50 (julgamento do autor); N*_Obs 2024 de 1,25 para 1,32, ainda na zona de equilíbrio.",
            "Mais 2 países incluídos (Costa Rica e Paraguai): o índice N* agora cobre 30 países.",
            "Página “Condição média” (colaboradores): fecundidade a 2,1 contra a tendência da ONU, de 2024 a 2099.",
            "A simulação por coorte inclui Costa Rica e Paraguai.",
        ],
        "en": [
            "Costa Rica added to the overview (now 12 countries, same as narayama.live); South Korea’s card corrected to 0.48.",
            "Costa Rica added to the overview (now 12 countries, same as narayama.live); South Korea’s card corrected to 0.48.",
            "Italy (C50/D50 → C30/D70) and South Korea (C80/D20 → C50/D50): profiles revised by the fertility-by-source rule; Korea’s 2024 N*_Obs 0.456 → 0.484 (Italy unchanged).",
            "Costa Rica: structural profile changed from C100 to C50/D50 (author’s judgment); 2024 N*_Obs from 1.25 to 1.32, still in the equilibrium zone.",
            "2 more countries added (Costa Rica and Paraguay): the N* index now covers 30 countries.",
            "New “Average condition” page (collaborators): fertility at 2.1 vs. the UN trend, 2024–2099.",
            "The cohort simulation now includes Costa Rica and Paraguay.",
        ],
        "es": [
            "Costa Rica en el panorama (ahora 12 países, igual que narayama.live); tarjeta de Corea del Sur corregida a 0,48.",
            "Costa Rica en el panorama (ahora 12 países, igual que narayama.live); tarjeta de Corea del Sur corregida a 0,48.",
            "Italia (C50/D50 → C30/D70) y Corea del Sur (C80/D20 → C50/D50): perfiles revisados con la regla de TFR por fuente; N*_Obs 2024 de Corea 0,456 → 0,484 (Italia sin cambios).",
            "Costa Rica: el perfil estructural pasó de C100 a C50/D50 (juicio del autor); N*_Obs 2024 de 1,25 a 1,32, aún en la zona de equilibrio.",
            "2 países más incluidos (Costa Rica y Paraguay): el índice N* ahora cubre 30 países.",
            "Nueva página «Condición media» (colaboradores): fecundidad de 2,1 frente a la tendencia de la ONU, de 2024 a 2099.",
            "La simulación por cohortes incluye Costa Rica y Paraguay.",
        ],
        "fr": [
            "Costa Rica ajouté au panorama (désormais 12 pays, comme narayama.live) ; carte de la Corée du Sud corrigée à 0,48.",
            "Costa Rica ajouté au panorama (désormais 12 pays, comme narayama.live) ; carte de la Corée du Sud corrigée à 0,48.",
            "Italie (C50/D50 → C30/D70) et Corée du Sud (C80/D20 → C50/D50) : profils révisés selon la règle de TFR par source ; N*_Obs 2024 de la Corée 0,456 → 0,484 (Italie inchangée).",
            "Costa Rica : le profil structurel passe de C100 à C50/D50 (jugement de l’auteur) ; N*_Obs 2024 de 1,25 à 1,32, toujours en zone d’équilibre.",
            "2 pays de plus inclus (Costa Rica et Paraguay) : l’indice N* couvre désormais 30 pays.",
            "Nouvelle page « Condition moyenne » (collaborateurs) : fécondité à 2,1 contre la tendance de l’ONU, de 2024 à 2099.",
            "La simulation par cohortes inclut le Costa Rica et le Paraguay.",
        ],
        "ko": [
            "코스타리카가 개요에 추가되었습니다(narayama.live와 같은 12개국); 한국 카드는 0.48로 수정되었습니다.",
            "코스타리카가 개요에 추가되었습니다(narayama.live와 같은 12개국); 한국 카드는 0.48로 수정되었습니다.",
            "이탈리아(C50/D50 → C30/D70)와 한국(C80/D20 → C50/D50): 출처별 TFR 규칙으로 프로파일 수정; 한국 2024년 N*_Obs 0.456 → 0.484(이탈리아 변동 없음).",
            "코스타리카: 구조 프로파일을 C100에서 C50/D50으로 변경(저자 판단); 2024년 N*_Obs 1.25 → 1.32, 여전히 균형 구간.",
            "국가 2개 추가(코스타리카, 파라과이): N* 지수가 이제 30개국을 다룹니다.",
            "새 페이지 ‘평균 조건’(협력자용): 출산율 2.1과 유엔 추세 비교, 2024–2099년.",
            "코호트 시뮬레이션에 코스타리카와 파라과이가 포함됩니다.",
        ],
        "it": [
            "Costa Rica nel quadro (ora 12 paesi, come narayama.live); scheda della Corea del Sud corretta a 0,48.",
            "Costa Rica nel quadro (ora 12 paesi, come narayama.live); scheda della Corea del Sud corretta a 0,48.",
            "Italia (C50/D50 → C30/D70) e Corea del Sud (C80/D20 → C50/D50): profili rivisti con la regola del TFR per fonte; N*_Obs 2024 della Corea 0,456 → 0,484 (Italia invariata).",
            "Costa Rica: il profilo strutturale passa da C100 a C50/D50 (giudizio dell’autore); N*_Obs 2024 da 1,25 a 1,32, ancora nella zona di equilibrio.",
            "2 paesi in più inclusi (Costa Rica e Paraguay): l’indice N* copre ora 30 paesi.",
            "Nuova pagina «Condizione media» (collaboratori): fecondità a 2,1 contro la tendenza dell’ONU, dal 2024 al 2099.",
            "La simulazione per coorti include Costa Rica e Paraguay.",
        ],
        "zh": [
            "哥斯达黎加加入概览（现为 12 个国家，与 narayama.live 一致）；韩国卡片更正为 0.48。",
            "哥斯达黎加加入概览（现为 12 个国家，与 narayama.live 一致）；韩国卡片更正为 0.48。",
            "意大利（C50/D50 → C30/D70）和韩国（C80/D20 → C50/D50）：按分来源生育率规则修订类型；韩国 2024 年 N*_Obs 0.456 → 0.484（意大利不变）。",
            "哥斯达黎加：结构类型由 C100 改为 C50/D50（作者判断）；2024 年 N*_Obs 由 1.25 变为 1.32，仍处于均衡区。",
            "新增 2 个国家（哥斯达黎加和巴拉圭）：N* 指数现涵盖 30 个国家。",
            "新页面“平均状况”（合作者）：生育率 2.1 与联合国趋势对比，2024–2099 年。",
            "分队列模拟已包含哥斯达黎加和巴拉圭。",
        ],
        "ja": [
            "コスタリカを概況に追加（narayama.liveと同じ12か国）。韓国のカードを0.48に修正。",
            "コスタリカを概況に追加（narayama.liveと同じ12か国）。韓国のカードを0.48に修正。",
            "イタリア（C50/D50 → C30/D70）と韓国（C80/D20 → C50/D50）：出典別TFR規則でプロファイルを見直し。韓国の2024年N*_Obsは0.456→0.484（イタリアは変更なし）。",
            "コスタリカ：構造プロファイルをC100からC50/D50に変更（著者判断）。2024年のN*_Obsは1.25から1.32で、均衡ゾーンのまま。",
            "2か国を追加（コスタリカとパラグアイ）：N* 指数は30か国になりました。",
            "新ページ「平均的条件」（協力者向け）：出生率 2.1 と国連トレンドの比較（2024〜2099年）。",
            "コホート別シミュレーションにコスタリカとパラグアイを追加。",
        ],
        "fi": [
            "Costa Rica lisätty yleiskuvaan (nyt 12 maata, kuten narayama.livessa); Etelä-Korean kortti korjattu arvoon 0,48.",
            "Costa Rica lisätty yleiskuvaan (nyt 12 maata, kuten narayama.livessa); Etelä-Korean kortti korjattu arvoon 0,48.",
            "Italia (C50/D50 → C30/D70) ja Etelä-Korea (C80/D20 → C50/D50): profiilit tarkistettu lähdekohtaisella TFR-säännöllä; Korean N*_Obs 2024 0,456 → 0,484 (Italia ennallaan).",
            "Costa Rica: rakenneprofiili muutettu C100:sta C50/D50:ksi (kirjoittajan arvio); N*_Obs 2024 1,25 → 1,32, edelleen tasapainovyöhykkeellä.",
            "Mukaan 2 uutta maata (Costa Rica ja Paraguay): N*-indeksi kattaa nyt 30 maata.",
            "Uusi sivu ”Keskimääräinen tila” (yhteistyökumppaneille): hedelmällisyys 2,1:ssä verrattuna YK:n trendiin, 2024–2099.",
            "Kohorttisimulaatio sisältää nyt Costa Rican ja Paraguayn.",
        ],
    },
    "narayama-live": {
        "pt": [
            "Costa Rica incluída no painel (agora 12 países): N*_Obs 2024 de 1,32, em equilíbrio.",
            "Coreia do Sul: perfil estrutural revisto de C80/D20 para C50/D50 (regra de TFT por fonte); N*_Obs 2024 de 0,456 para 0,484, ainda em PEC. Os demais países ficam como estavam.",
            "Paraguai entrou no ainu.systems (fora deste painel).",
        ],
        "en": [
            "Costa Rica added to the panel (now 12 countries): 2024 N*_Obs of 1.32, in the equilibrium zone.",
            "South Korea: structural profile revised from C80/D20 to C50/D50 (fertility-by-source rule); 2024 N*_Obs from 0.456 to 0.484, still PEC. The other countries are unchanged.",
            "Paraguay was added to ainu.systems (outside this panel).",
        ],
        "es": [
            "Costa Rica incluida en el panel (ahora 12 países): N*_Obs 2024 de 1,32, en equilibrio.",
            "Corea del Sur: perfil estructural revisado de C80/D20 a C50/D50 (regla de TFR por fuente); N*_Obs 2024 de 0,456 a 0,484, aún PEC. Los demás países no cambian.",
            "Paraguay se añadió a ainu.systems (fuera de este panel).",
        ],
        "fr": [
            "Costa Rica ajouté au panneau (désormais 12 pays) : N*_Obs 2024 de 1,32, en zone d’équilibre.",
            "Corée du Sud : profil structurel révisé de C80/D20 à C50/D50 (règle de TFR par source) ; N*_Obs 2024 de 0,456 à 0,484, toujours PEC. Les autres pays sont inchangés.",
            "Le Paraguay a été ajouté à ainu.systems (hors de ce panneau).",
        ],
        "ko": [
            "코스타리카가 패널에 추가되었습니다(이제 12개국): 2024년 N*_Obs 1.32, 균형 구간.",
            "한국: 구조 프로파일을 C80/D20에서 C50/D50으로 수정(출처별 TFR 규칙); 2024년 N*_Obs 0.456 → 0.484, 여전히 PEC. 다른 국가는 그대로입니다.",
            "파라과이는 ainu.systems에 추가되었습니다(이 패널에는 포함되지 않음).",
        ],
        "it": [
            "Costa Rica aggiunta al pannello (ora 12 paesi): N*_Obs 2024 di 1,32, in zona di equilibrio.",
            "Corea del Sud: profilo strutturale rivisto da C80/D20 a C50/D50 (regola del TFR per fonte); N*_Obs 2024 da 0,456 a 0,484, ancora PEC. Gli altri paesi restano invariati.",
            "Il Paraguay è stato aggiunto a ainu.systems (fuori da questo pannello).",
        ],
        "zh": [
            "哥斯达黎加已加入面板（现为 12 个国家）：2024 年 N*_Obs 为 1.32，处于均衡区。",
            "韩国：结构类型由 C80/D20 修订为 C50/D50（分来源生育率规则）；2024 年 N*_Obs 由 0.456 变为 0.484，仍为 PEC。其他国家不变。",
            "巴拉圭已加入 ainu.systems（不在此面板内）。",
        ],
        "ja": [
            "コスタリカをパネルに追加（12か国に）：2024年のN*_Obsは1.32で、均衡ゾーン。",
            "韓国：構造プロファイルをC80/D20からC50/D50に見直し（出典別TFR規則）。2024年のN*_Obsは0.456から0.484で、PECのまま。他の国は変更なし。",
            "パラグアイはainu.systemsに追加されました（このパネルには含まれません）。",
        ],
        "fi": [
            "Costa Rica lisätty paneeliin (nyt 12 maata): N*_Obs 2024 1,32, tasapainovyöhykkeellä.",
            "Etelä-Korea: rakenneprofiili tarkistettu C80/D20:sta C50/D50:ksi (lähdekohtainen TFR-sääntö); N*_Obs 2024 0,456 → 0,484, edelleen PEC. Muut maat ennallaan.",
            "Paraguay lisättiin ainu.systems-sivustoon (tämän paneelin ulkopuolella).",
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
        f'      <p class="nov-data" data-i18n="nov_ultima">{ULTIMA["pt"]}{data_fmt("pt", site)}</p>\n'
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
            ("nov_ultima", ULTIMA[lang] + data_fmt(lang, site)),
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

    # sitemap.xml: a data de modificação acompanha a data das novidades
    mapa = caminho.parent / "sitemap.xml"
    if mapa.exists():
        x = mapa.read_bytes().decode("utf-8")
        x = re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{DATA_SITE[site].isoformat()}</lastmod>", x)
        mapa.write_bytes(x.encode("utf-8"))
    print("ok", site, caminho.relative_to(RAIZ))


if __name__ == "__main__":
    for site, caminho in PAGINAS.items():
        aplicar(site, caminho)
