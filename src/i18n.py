"""
Internacionalização (i18n) do AINU-Narayama — narayama.live e ainu.systems.

Seletor de idioma no topo da página (barra superior), 9 idiomas: PT
(padrão/fonte), EN, ES, JA, KO, IT, FI, FR, ZH. Decisão do autor,
2026-07-18: os dois sites recebem o seletor.

Convenção de tradução: termos técnicos definidos pela tese (N*, PEC,
PEEC, PEA, NGII_Bruto, NGII_puro, N_Base, Fator_Ger, Fator_Aloc, TFR,
P_eq, P_tendência, DDI, NTA) permanecem INALTERADOS em todos os
idiomas — são o vocabulário próprio do índice, não palavras comuns
(mesmo princípio de docs/feedback_significado_termos_da_tese.md: o
significado desses termos vem do texto da tese, a tradução não deve
reinterpretá-los). Só a prosa ao redor é traduzida.

Mecanismo: idioma persiste via query param `?lang=xx` (link
compartilhável, sem duplicar sessão) — ver `idioma_atual()` e
`seletor_idioma()`. Traduções ausentes caem em PT (nunca quebra,
nunca mostra a chave crua).

Qualidade: traduções PT->EN/ES/IT/FR feitas com alta confiança.
PT->JA/KO/FI/ZH feitas com cuidado, mas SEM revisão nativa — sinalizado
ao autor no registro técnico desta mudança; recomendável revisão por
falante nativo antes de divulgação ampla nesses 4 idiomas.
"""

from __future__ import annotations

import streamlit as st

IDIOMA_PADRAO = "pt"

IDIOMAS: dict[str, str] = {
    "pt": "Português",
    "en": "English",
    "es": "Español",
    "ja": "日本語",
    "ko": "한국어",
    "it": "Italiano",
    "fi": "Suomi",
    "fr": "Français",
    "zh": "中文",
}

# -----------------------------------------------------------------------
# Nomes dos países (28) — tradução padrão/geográfica, não interpretativa.
# -----------------------------------------------------------------------

NOMES_PAISES: dict[str, dict[str, str]] = {
    "ARG": {"pt": "Argentina", "en": "Argentina", "es": "Argentina", "ja": "アルゼンチン", "ko": "아르헨티나", "it": "Argentina", "fi": "Argentiina", "fr": "Argentine", "zh": "阿根廷"},
    "AUS": {"pt": "Austrália", "en": "Australia", "es": "Australia", "ja": "オーストラリア", "ko": "호주", "it": "Australia", "fi": "Australia", "fr": "Australie", "zh": "澳大利亚"},
    "BRA": {"pt": "Brasil", "en": "Brazil", "es": "Brasil", "ja": "ブラジル", "ko": "브라질", "it": "Brasile", "fi": "Brasilia", "fr": "Brésil", "zh": "巴西"},
    "CHL": {"pt": "Chile", "en": "Chile", "es": "Chile", "ja": "チリ", "ko": "칠레", "it": "Cile", "fi": "Chile", "fr": "Chili", "zh": "智利"},
    "CHN": {"pt": "China", "en": "China", "es": "China", "ja": "中国", "ko": "중국", "it": "Cina", "fi": "Kiina", "fr": "Chine", "zh": "中国"},
    "COD": {"pt": "República Democrática do Congo", "en": "Democratic Republic of the Congo", "es": "República Democrática del Congo", "ja": "コンゴ民主共和国", "ko": "콩고민주공화국", "it": "Repubblica Democratica del Congo", "fi": "Kongon demokraattinen tasavalta", "fr": "République démocratique du Congo", "zh": "刚果民主共和国"},
    "DEU": {"pt": "Alemanha", "en": "Germany", "es": "Alemania", "ja": "ドイツ", "ko": "독일", "it": "Germania", "fi": "Saksa", "fr": "Allemagne", "zh": "德国"},
    "EGY": {"pt": "Egito", "en": "Egypt", "es": "Egipto", "ja": "エジプト", "ko": "이집트", "it": "Egitto", "fi": "Egypti", "fr": "Égypte", "zh": "埃及"},
    "ETH": {"pt": "Etiópia", "en": "Ethiopia", "es": "Etiopía", "ja": "エチオピア", "ko": "에티오피아", "it": "Etiopia", "fi": "Etiopia", "fr": "Éthiopie", "zh": "埃塞俄比亚"},
    "FRA": {"pt": "França", "en": "France", "es": "Francia", "ja": "フランス", "ko": "프랑스", "it": "Francia", "fi": "Ranska", "fr": "France", "zh": "法国"},
    "GBR": {"pt": "Reino Unido", "en": "United Kingdom", "es": "Reino Unido", "ja": "イギリス", "ko": "영국", "it": "Regno Unito", "fi": "Yhdistynyt kuningaskunta", "fr": "Royaume-Uni", "zh": "英国"},
    "IDN": {"pt": "Indonésia", "en": "Indonesia", "es": "Indonesia", "ja": "インドネシア", "ko": "인도네시아", "it": "Indonesia", "fi": "Indonesia", "fr": "Indonésie", "zh": "印度尼西亚"},
    "IND": {"pt": "Índia", "en": "India", "es": "India", "ja": "インド", "ko": "인도", "it": "India", "fi": "Intia", "fr": "Inde", "zh": "印度"},
    "IRN": {"pt": "Irã", "en": "Iran", "es": "Irán", "ja": "イラン", "ko": "이란", "it": "Iran", "fi": "Iran", "fr": "Iran", "zh": "伊朗"},
    "ITA": {"pt": "Itália", "en": "Italy", "es": "Italia", "ja": "イタリア", "ko": "이탈리아", "it": "Italia", "fi": "Italia", "fr": "Italie", "zh": "意大利"},
    "JPN": {"pt": "Japão", "en": "Japan", "es": "Japón", "ja": "日本", "ko": "일본", "it": "Giappone", "fi": "Japani", "fr": "Japon", "zh": "日本"},
    "KOR": {"pt": "Coreia do Sul", "en": "South Korea", "es": "Corea del Sur", "ja": "韓国", "ko": "대한민국", "it": "Corea del Sud", "fi": "Etelä-Korea", "fr": "Corée du Sud", "zh": "韩国"},
    "MAR": {"pt": "Marrocos", "en": "Morocco", "es": "Marruecos", "ja": "モロッコ", "ko": "모로코", "it": "Marocco", "fi": "Marokko", "fr": "Maroc", "zh": "摩洛哥"},
    "MEX": {"pt": "México", "en": "Mexico", "es": "México", "ja": "メキシコ", "ko": "멕시코", "it": "Messico", "fi": "Meksiko", "fr": "Mexique", "zh": "墨西哥"},
    "NGA": {"pt": "Nigéria", "en": "Nigeria", "es": "Nigeria", "ja": "ナイジェリア", "ko": "나이지리아", "it": "Nigeria", "fi": "Nigeria", "fr": "Nigéria", "zh": "尼日利亚"},
    "POL": {"pt": "Polônia", "en": "Poland", "es": "Polonia", "ja": "ポーランド", "ko": "폴란드", "it": "Polonia", "fi": "Puola", "fr": "Pologne", "zh": "波兰"},
    "RUS": {"pt": "Rússia", "en": "Russia", "es": "Rusia", "ja": "ロシア", "ko": "러시아", "it": "Russia", "fi": "Venäjä", "fr": "Russie", "zh": "俄罗斯"},
    "SAU": {"pt": "Arábia Saudita", "en": "Saudi Arabia", "es": "Arabia Saudita", "ja": "サウジアラビア", "ko": "사우디아라비아", "it": "Arabia Saudita", "fi": "Saudi-Arabia", "fr": "Arabie saoudite", "zh": "沙特阿拉伯"},
    "SWE": {"pt": "Suécia", "en": "Sweden", "es": "Suecia", "ja": "スウェーデン", "ko": "스웨덴", "it": "Svezia", "fi": "Ruotsi", "fr": "Suède", "zh": "瑞典"},
    "THA": {"pt": "Tailândia", "en": "Thailand", "es": "Tailandia", "ja": "タイ", "ko": "태국", "it": "Tailandia", "fi": "Thaimaa", "fr": "Thaïlande", "zh": "泰国"},
    "USA": {"pt": "Estados Unidos", "en": "United States", "es": "Estados Unidos", "ja": "アメリカ合衆国", "ko": "미국", "it": "Stati Uniti", "fi": "Yhdysvallat", "fr": "États-Unis", "zh": "美国"},
    "VNM": {"pt": "Vietnã", "en": "Vietnam", "es": "Vietnam", "ja": "ベトナム", "ko": "베트남", "it": "Vietnam", "fi": "Vietnam", "fr": "Vietnam", "zh": "越南"},
    "ZAF": {"pt": "África do Sul", "en": "South Africa", "es": "Sudáfrica", "ja": "南アフリカ", "ko": "남아프리카공화국", "it": "Sudafrica", "fi": "Etelä-Afrikka", "fr": "Afrique du Sud", "zh": "南非"},
}

# -----------------------------------------------------------------------
# Zonas do N* (5) — acrônimo (PEC/PEEC/PEA) mantido em todo idioma: é o
# código próprio do índice, não uma sigla da língua portuguesa comum.
# -----------------------------------------------------------------------

ZONAS: dict[str, dict[str, str]] = {
    "Colapso de Narayama (PEC)": {
        "pt": "Colapso de Narayama (PEC)", "en": "Narayama Collapse (PEC)",
        "es": "Colapso de Narayama (PEC)", "ja": "ナラヤマ崩壊 (PEC)",
        "ko": "나라야마 붕괴 (PEC)", "it": "Collasso di Narayama (PEC)",
        "fi": "Narayama-romahdus (PEC)", "fr": "Effondrement de Narayama (PEC)",
        "zh": "楢山崩溃 (PEC)",
    },
    "Tensão Acelerada": {
        "pt": "Tensão Acelerada", "en": "Accelerated Tension",
        "es": "Tensión Acelerada", "ja": "加速的緊張", "ko": "가속 긴장",
        "it": "Tensione Accelerata", "fi": "Kiihtyvä jännite",
        "fr": "Tension accélérée", "zh": "加速紧张",
    },
    "Equilíbrio Sustentável (PEA)": {
        "pt": "Equilíbrio Sustentável (PEA)", "en": "Sustainable Equilibrium (PEA)",
        "es": "Equilibrio Sostenible (PEA)", "ja": "持続可能な均衡 (PEA)",
        "ko": "지속가능한 균형 (PEA)", "it": "Equilibrio Sostenibile (PEA)",
        "fi": "Kestävä tasapaino (PEA)", "fr": "Équilibre durable (PEA)",
        "zh": "可持续平衡 (PEA)",
    },
    "Tensão Populacional": {
        "pt": "Tensão Populacional", "en": "Population Tension",
        "es": "Tensión Poblacional", "ja": "人口的緊張", "ko": "인구 긴장",
        "it": "Tensione Demografica", "fi": "Väestöjännite",
        "fr": "Tension démographique", "zh": "人口紧张",
    },
    "Saturação por Overbirths (PEEC)": {
        "pt": "Saturação por Overbirths (PEEC)", "en": "Overbirth Saturation (PEEC)",
        "es": "Saturación por Overbirths (PEEC)", "ja": "オーバーバース飽和 (PEEC)",
        "ko": "과잉출생 포화 (PEEC)", "it": "Saturazione da Overbirths (PEEC)",
        "fi": "Ylisyntyvyyden kyllästymä (PEEC)", "fr": "Saturation par surnatalité (PEEC)",
        "zh": "过度生育饱和 (PEEC)",
    },
}

# -----------------------------------------------------------------------
# Regiões (12, filtro do ainu.systems) — os códigos de "perfil"
# (A35/B40/C25 etc.) já são alfanuméricos e não precisam de tradução.
# -----------------------------------------------------------------------

REGIOES: dict[str, dict[str, str]] = {
    "América do Norte": {"pt": "América do Norte", "en": "North America", "es": "América del Norte", "ja": "北米", "ko": "북아메리카", "it": "Nord America", "fi": "Pohjois-Amerikka", "fr": "Amérique du Nord", "zh": "北美洲"},
    "América do Sul": {"pt": "América do Sul", "en": "South America", "es": "América del Sur", "ja": "南米", "ko": "남아메리카", "it": "Sud America", "fi": "Etelä-Amerikka", "fr": "Amérique du Sud", "zh": "南美洲"},
    "Europa Ocidental": {"pt": "Europa Ocidental", "en": "Western Europe", "es": "Europa Occidental", "ja": "西ヨーロッパ", "ko": "서유럽", "it": "Europa Occidentale", "fi": "Länsi-Eurooppa", "fr": "Europe occidentale", "zh": "西欧"},
    "Europa Oriental": {"pt": "Europa Oriental", "en": "Eastern Europe", "es": "Europa Oriental", "ja": "東ヨーロッパ", "ko": "동유럽", "it": "Europa Orientale", "fi": "Itä-Eurooppa", "fr": "Europe orientale", "zh": "东欧"},
    "Eurásia": {"pt": "Eurásia", "en": "Eurasia", "es": "Eurasia", "ja": "ユーラシア", "ko": "유라시아", "it": "Eurasia", "fi": "Euraasia", "fr": "Eurasie", "zh": "欧亚大陆"},
    "Oceania": {"pt": "Oceania", "en": "Oceania", "es": "Oceanía", "ja": "オセアニア", "ko": "오세아니아", "it": "Oceania", "fi": "Oseania", "fr": "Océanie", "zh": "大洋洲"},
    "Oriente Médio": {"pt": "Oriente Médio", "en": "Middle East", "es": "Oriente Medio", "ja": "中東", "ko": "중동", "it": "Medio Oriente", "fi": "Lähi-itä", "fr": "Moyen-Orient", "zh": "中东"},
    "África Subsaariana": {"pt": "África Subsaariana", "en": "Sub-Saharan Africa", "es": "África Subsahariana", "ja": "サハラ以南アフリカ", "ko": "사하라 이남 아프리카", "it": "Africa Subsahariana", "fi": "Saharan eteläpuolinen Afrikka", "fr": "Afrique subsaharienne", "zh": "撒哈拉以南非洲"},
    "África do Norte": {"pt": "África do Norte", "en": "North Africa", "es": "África del Norte", "ja": "北アフリカ", "ko": "북아프리카", "it": "Africa del Nord", "fi": "Pohjois-Afrikka", "fr": "Afrique du Nord", "zh": "北非"},
    "Ásia Meridional": {"pt": "Ásia Meridional", "en": "South Asia", "es": "Asia Meridional", "ja": "南アジア", "ko": "남아시아", "it": "Asia Meridionale", "fi": "Etelä-Aasia", "fr": "Asie du Sud", "zh": "南亚"},
    "Ásia Oriental": {"pt": "Ásia Oriental", "en": "East Asia", "es": "Asia Oriental", "ja": "東アジア", "ko": "동아시아", "it": "Asia Orientale", "fi": "Itä-Aasia", "fr": "Asie de l'Est", "zh": "东亚"},
    "Ásia Sudeste": {"pt": "Ásia Sudeste", "en": "Southeast Asia", "es": "Sudeste Asiático", "ja": "東南アジア", "ko": "동남아시아", "it": "Sud-est asiatico", "fi": "Kaakkois-Aasia", "fr": "Asie du Sud-Est", "zh": "东南亚"},
}

# -----------------------------------------------------------------------
# Sufixo de milhões nos cards ("345mi" -> "345M" fora do PT — evita
# depender de unidades numéricas próprias do CJK, como 万/億).
# -----------------------------------------------------------------------

SUFIXO_MILHOES: dict[str, str] = {
    "pt": "mi", "en": "M", "es": "M", "ja": "M", "ko": "M",
    "it": "M", "fi": "M", "fr": "M", "zh": "M",
}

SEM_DADO: dict[str, str] = {
    "pt": "s/d", "en": "n/a", "es": "s/d", "ja": "N/A", "ko": "N/A",
    "it": "n/d", "fi": "N/A", "fr": "n/d", "zh": "N/A",
}

# -----------------------------------------------------------------------
# Textos da interface.
# -----------------------------------------------------------------------

T: dict[str, dict[str, str]] = {
    # --- Compartilhado entre os dois sites -----------------------------
    "n_star_header_destaque": {
        "pt": "N* — 7 Países Destaque (2024)", "en": "N* — 7 Featured Countries (2024)",
        "es": "N* — 7 Países Destacados (2024)", "ja": "N* — 注目7カ国（2024年）",
        "ko": "N* — 주요 7개국 (2024)", "it": "N* — 7 Paesi in Evidenza (2024)",
        "fi": "N* — 7 esiteltyä maata (2024)", "fr": "N* — 7 pays en vedette (2024)",
        "zh": "N* — 7个重点国家（2024年）",
    },
    "bar_chart_title": {
        "pt": "N* por país (2024)", "en": "N* by country (2024)",
        "es": "N* por país (2024)", "ja": "国別N*（2024年）", "ko": "국가별 N* (2024)",
        "it": "N* per paese (2024)", "fi": "N* maittain (2024)",
        "fr": "N* par pays (2024)", "zh": "各国N*（2024年）",
    },
    "tabela_geracional_header": {
        "pt": "Tabela Geracional de Narayama", "en": "Narayama Generational Table",
        "es": "Tabla Generacional de Narayama", "ja": "ナラヤマ世代表",
        "ko": "나라야마 세대 표", "it": "Tabella Generazionale di Narayama",
        "fi": "Narayaman sukupolvitaulukko", "fr": "Tableau générationnel de Narayama",
        "zh": "楢山世代表",
    },
    "indice_narayama_seta": {
        "pt": "Índice Narayama →", "en": "Narayama Index →", "es": "Índice Narayama →",
        "ja": "ナラヤマ指数 →", "ko": "나라야마 지수 →", "it": "Indice Narayama →",
        "fi": "Narayama-indeksi →", "fr": "Indice Narayama →", "zh": "楢山指数 →",
    },
    "col_pais": {
        "pt": "País", "en": "Country", "es": "País", "ja": "国", "ko": "국가",
        "it": "Paese", "fi": "Maa", "fr": "Pays", "zh": "国家",
    },
    "col_status": {
        "pt": "Status", "en": "Status", "es": "Estado", "ja": "状態", "ko": "상태",
        "it": "Stato", "fi": "Tila", "fr": "Statut", "zh": "状态",
    },

    # --- narayama.live ---------------------------------------------------
    "narayama_subtitulo": {
        "pt": "Termômetro do Índice de Narayama Sistêmico",
        "en": "Thermometer of the Systemic Narayama Index",
        "es": "Termómetro del Índice de Narayama Sistémico",
        "ja": "システミック・ナラヤマ指数の温度計",
        "ko": "체계적 나라야마 지수 온도계",
        "it": "Termometro dell'Indice di Narayama Sistemico",
        "fi": "Systeemisen Narayama-indeksin lämpömittari",
        "fr": "Thermomètre de l'indice de Narayama systémique",
        "zh": "系统性楢山指数温度计",
    },
    "narayama_intro": {
        "pt": "Acompanhe, de forma simples, a capacidade de renovação geracional de 7 países ao final de um ciclo de 25 anos — com base na tese de doutorado \"Do Dilema de Narayama ao Oicoceno Civilizacional\" (v9.2). Para análises detalhadas, simulações e calibração, veja [ainu.systems](https://ainu.systems).",
        "en": "Track, in simple terms, the generational renewal capacity of 7 countries at the end of a 25-year cycle — based on the doctoral thesis \"From Narayama's Dilemma to the Civilizational Oikocene\" (v9.2). For detailed analysis, simulations and calibration, see [ainu.systems](https://ainu.systems).",
        "es": "Siga, de forma simple, la capacidad de renovación generacional de 7 países al final de un ciclo de 25 años — según la tesis doctoral \"Del Dilema de Narayama al Oicoceno Civilizacional\" (v9.2). Para análisis detallados, simulaciones y calibración, vea [ainu.systems](https://ainu.systems).",
        "ja": "博士論文『ナラヤマのジレンマから文明的オイコセーンへ』（v9.2）に基づき、25年周期の終わりにおける7か国の世代更新能力をシンプルに追跡します。詳細な分析やシミュレーション、キャリブレーションについては[ainu.systems](https://ainu.systems)をご覧ください。",
        "ko": "박사 학위논문 『나라야마의 딜레마에서 문명적 오이코세까지』(v9.2)를 바탕으로, 25년 주기가 끝나는 시점의 7개국 세대 재생산 능력을 간단히 살펴봅니다. 자세한 분석, 시뮬레이션, 보정은 [ainu.systems](https://ainu.systems)에서 확인하세요.",
        "it": "Segui, in modo semplice, la capacità di rinnovamento generazionale di 7 paesi al termine di un ciclo di 25 anni — sulla base della tesi di dottorato \"Dal Dilemma di Narayama all'Oicocene Civilizzazionale\" (v9.2). Per analisi dettagliate, simulazioni e calibrazione, vedi [ainu.systems](https://ainu.systems).",
        "fi": "Seuraa yksinkertaisesti 7 maan sukupolvien uusiutumiskykyä 25 vuoden syklin lopussa — perustuen väitöskirjaan \"Narayaman dilemmasta sivilisaation Oikoseeniin\" (v9.2). Yksityiskohtaista analyysia, simulaatioita ja kalibrointia varten katso [ainu.systems](https://ainu.systems).",
        "fr": "Suivez, de façon simple, la capacité de renouvellement générationnel de 7 pays à la fin d'un cycle de 25 ans — d'après la thèse de doctorat \"Du Dilemme de Narayama à l'Oïcocène Civilisationnel\" (v9.2). Pour des analyses détaillées, des simulations et un calibrage, voir [ainu.systems](https://ainu.systems).",
        "zh": "基于博士论文《从楢山难题到文明世的宜居纪》(v9.2)，简明呈现7个国家在25年周期结束时的世代更新能力。详细分析、模拟与校准请见[ainu.systems](https://ainu.systems)。",
    },
    "narayama_info": {
        "pt": "**Como ler o N\\*:** não é uma nota de \"quanto maior, melhor\" — é um equilíbrio ao longo de 5 zonas. N\\* muito baixo indica **Colapso de Narayama (PEC)** (< 0,71): poucos nascimentos não repõem a geração legatária. Logo acima, **Tensão Acelerada** (0,71–0,90) já sinaliza risco antecipado de colapso. O ideal fica no meio da escala, faixa chamada de **Equilíbrio Sustentável (PEA)** (0,90–1,40). Logo acima disso, **Tensão Populacional** (1,40–2,00) já sinaliza risco antecipado de saturação. N\\* muito alto indica **Saturação por Overbirths (PEEC)** (≥ 2,00): crescimento populacional acelerado além da capacidade de absorção institucional. O farol institucional (+/n/-) ainda não aparece aqui: depende de dados de Contas de Transferências Nacionais (NTA) que este projeto ainda não tem — ver [ainu.systems](https://ainu.systems) para o detalhamento completo da metodologia.",
        "en": "**How to read N\\*:** it's not a \"higher is better\" score — it's a balance across 5 zones. A very low N\\* indicates **Narayama Collapse (PEC)** (< 0.71): too few births to replace the legacy generation. Just above that, **Accelerated Tension** (0.71-0.90) already signals an early warning of collapse. The ideal sits in the middle of the scale, a range called **Sustainable Equilibrium (PEA)** (0.90-1.40). Just above that, **Population Tension** (1.40-2.00) already signals an early warning of saturation. A very high N\\* indicates **Overbirth Saturation (PEEC)** (≥ 2.00): population growth accelerating beyond institutional absorption capacity. The institutional beacon (+/n/-) doesn't appear here yet: it depends on National Transfer Accounts (NTA) data this project doesn't have yet — see [ainu.systems](https://ainu.systems) for the full methodology.",
        "es": "**Cómo leer el N\\*:** no es una nota de \"cuanto más alto, mejor\" — es un equilibrio a lo largo de 5 zonas. Un N\\* muy bajo indica **Colapso de Narayama (PEC)** (< 0,71): pocos nacimientos no reponen a la generación legataria. Justo por encima, **Tensión Acelerada** (0,71–0,90) ya señala un riesgo temprano de colapso. Lo ideal está en el medio de la escala, franja llamada **Equilibrio Sostenible (PEA)** (0,90–1,40). Justo por encima de eso, **Tensión Poblacional** (1,40–2,00) ya señala un riesgo temprano de saturación. Un N\\* muy alto indica **Saturación por Overbirths (PEEC)** (≥ 2,00): crecimiento poblacional acelerado más allá de la capacidad de absorción institucional. El farol institucional (+/n/-) todavía no aparece aquí: depende de datos de Cuentas de Transferencias Nacionales (NTA) que este proyecto aún no tiene — ver [ainu.systems](https://ainu.systems) para el detalle completo de la metodología.",
        "ja": "**N\\*の読み方：** 「高いほど良い」という指標ではなく、5つのゾーンにわたるバランスを示します。N\\*が非常に低い場合は **ナラヤマ崩壊(PEC)** (0.71未満)を示します：出生数が少なすぎて先代世代を置き換えられません。そのすぐ上の **加速的緊張** (0.71-0.90)は、崩壊の早期警戒シグナルです。理想は尺度の中央、**持続可能な均衡(PEA)** (0.90-1.40)と呼ばれる範囲にあります。そのすぐ上の **人口的緊張** (1.40-2.00)は、飽和の早期警戒シグナルです。N\\*が非常に高い場合は **オーバーバース飽和(PEEC)** (2.00以上)を示します：人口増加が制度的な受容能力を超えて加速しています。制度的ビーコン（+/n/-）はまだここには表示されません：本プロジェクトがまだ保有していないNational Transfer Accounts（NTA）のデータに依存するためです — 詳しい方法論は[ainu.systems](https://ainu.systems)をご覧ください。",
        "ko": "**N\\* 읽는 법:** \"높을수록 좋다\"는 점수가 아니라 5개 구역에 걸친 균형을 나타냅니다. N\\*가 매우 낮으면 **나라야마 붕괴(PEC)** (0.71 미만)를 의미합니다: 출생아 수가 너무 적어 이전 세대를 대체하지 못합니다. 바로 위의 **가속 긴장** (0.71-0.90)은 이미 붕괴의 조기 경고 신호입니다. 이상적인 값은 척도의 중간, **지속가능한 균형(PEA)** (0.90-1.40)이라 불리는 구간에 있습니다. 바로 위의 **인구 긴장** (1.40-2.00)은 이미 포화의 조기 경고 신호입니다. N\\*가 매우 높으면 **과잉출생 포화(PEEC)** (2.00 이상)를 의미합니다: 인구 증가가 제도적 수용 능력을 넘어 가속화됩니다. 제도적 신호등(+/n/-)은 아직 여기에 표시되지 않습니다: 이 프로젝트가 아직 보유하지 않은 국민이전계정(NTA) 데이터에 의존하기 때문입니다 — 전체 방법론은 [ainu.systems](https://ainu.systems)를 참고하세요.",
        "it": "**Come leggere l'N\\*:** non è un punteggio \"più alto è meglio\" — è un equilibrio lungo 5 zone. Un N\\* molto basso indica **Collasso di Narayama (PEC)** (< 0,71): poche nascite non sostituiscono la generazione legataria. Subito sopra, **Tensione Accelerata** (0,71–0,90) segnala già un rischio precoce di collasso. L'ideale sta nel mezzo della scala, fascia chiamata **Equilibrio Sostenibile (PEA)** (0,90–1,40). Subito sopra questa, **Tensione Demografica** (1,40–2,00) segnala già un rischio precoce di saturazione. Un N\\* molto alto indica **Saturazione da Overbirths (PEEC)** (≥ 2,00): crescita demografica accelerata oltre la capacità di assorbimento istituzionale. Il faro istituzionale (+/n/-) non appare ancora qui: dipende dai dati dei National Transfer Accounts (NTA) che questo progetto non ha ancora — vedi [ainu.systems](https://ainu.systems) per il dettaglio completo della metodologia.",
        "fi": "**Miten N\\*:ää luetaan:** kyse ei ole \"mitä korkeampi, sitä parempi\" -pisteestä — vaan tasapainosta 5 vyöhykkeen välillä. Hyvin matala N\\* tarkoittaa **Narayama-romahdusta (PEC)** (< 0,71): liian vähän syntyvyyttä korvaamaan edellinen sukupolvi. Heti sen yläpuolella **kiihtyvä jännite** (0,71–0,90) merkitsee jo varhaista romahdusriskiä. Ihanne on asteikon keskellä, alueella nimeltä **kestävä tasapaino (PEA)** (0,90–1,40). Heti sen yläpuolella **väestöjännite** (1,40–2,00) merkitsee jo varhaista kyllästymisriskiä. Hyvin korkea N\\* tarkoittaa **ylisyntyvyyden kyllästymää (PEEC)** (≥ 2,00): väestönkasvu kiihtyy yli institutionaalisen vastaanottokyvyn. Institutionaalinen valo (+/n/-) ei näy vielä tässä: se riippuu National Transfer Accounts (NTA) -tiedoista, joita tällä projektilla ei vielä ole — katso [ainu.systems](https://ainu.systems) koko menetelmä.",
        "fr": "**Comment lire le N\\* :** ce n'est pas une note \"plus c'est haut, mieux c'est\" — c'est un équilibre sur 5 zones. Un N\\* très bas indique un **Effondrement de Narayama (PEC)** (< 0,71) : trop peu de naissances pour remplacer la génération léguée. Juste au-dessus, la **Tension accélérée** (0,71–0,90) signale déjà un risque précoce d'effondrement. L'idéal se situe au milieu de l'échelle, une plage appelée **Équilibre durable (PEA)** (0,90–1,40). Juste au-dessus, la **Tension démographique** (1,40–2,00) signale déjà un risque précoce de saturation. Un N\\* très élevé indique une **Saturation par surnatalité (PEEC)** (≥ 2,00) : croissance démographique accélérée au-delà de la capacité d'absorption institutionnelle. Le repère institutionnel (+/n/-) n'apparaît pas encore ici : il dépend des données des National Transfer Accounts (NTA), que ce projet n'a pas encore — voir [ainu.systems](https://ainu.systems) pour le détail complet de la méthodologie.",
        "zh": "**如何解读N\\*：** 这不是“越高越好”的分数，而是跨越5个区域的一种平衡。N\\*过低表示 **楢山崩溃(PEC)** (低于0.71)：出生人数过少，无法替代上一代人。紧邻其上的 **加速紧张** (0.71-0.90)已经是崩溃的早期预警信号。理想值位于量表中段，称为 **可持续平衡(PEA)** (0.90-1.40)区间。紧邻其上的 **人口紧张** (1.40-2.00)已经是饱和的早期预警信号。N\\*过高表示 **过度生育饱和(PEEC)** (2.00及以上)：人口增长速度超过了制度吸纳能力。制度信号灯（+/n/-）此处尚未显示：它依赖于本项目尚未获取的国民转移账户（NTA）数据 — 完整方法论请见[ainu.systems](https://ainu.systems)。",
    },
    "narayama_warning_sem_dado": {
        "pt": "Nenhum dado encontrado em `data/processed/n_index_2024.csv`. Este arquivo ainda não foi gerado pelo pipeline de cálculo (Fase 2).",
        "en": "No data found in `data/processed/n_index_2024.csv`. This file hasn't been generated by the calculation pipeline yet (Phase 2).",
        "es": "No se encontraron datos en `data/processed/n_index_2024.csv`. Este archivo aún no ha sido generado por el pipeline de cálculo (Fase 2).",
        "ja": "`data/processed/n_index_2024.csv` にデータが見つかりません。この計算パイプライン（フェーズ2）はまだ生成されていません。",
        "ko": "`data/processed/n_index_2024.csv`에서 데이터를 찾을 수 없습니다. 이 파일은 아직 계산 파이프라인(2단계)에서 생성되지 않았습니다.",
        "it": "Nessun dato trovato in `data/processed/n_index_2024.csv`. Questo file non è ancora stato generato dalla pipeline di calcolo (Fase 2).",
        "fi": "Tietoja ei löytynyt tiedostosta `data/processed/n_index_2024.csv`. Laskentaputki (vaihe 2) ei ole vielä luonut tätä tiedostoa.",
        "fr": "Aucune donnée trouvée dans `data/processed/n_index_2024.csv`. Ce fichier n'a pas encore été généré par le pipeline de calcul (Phase 2).",
        "zh": "在`data/processed/n_index_2024.csv`中未找到数据。计算流水线（第2阶段）尚未生成此文件。",
    },
    "narayama_caption_grade": {
        "pt": "Grade dos 7 países destaque por zona do Índice Narayama (Saturação/PEEC → Colapso/PEC), países ordenados por população atual dentro de cada zona. Farol institucional aparece como lacuna (`s/d`) — mesma explicação do quadro acima.",
        "en": "Grid of the 7 featured countries by Narayama Index zone (Overbirths/PEEC → Collapse/PEC), countries ordered by current population within each zone. The institutional beacon shows as a gap (`n/a`) — same explanation as the box above.",
        "es": "Cuadrícula de los 7 países destacados por zona del Índice Narayama (Saturación/PEEC → Colapso/PEC), países ordenados por población actual dentro de cada zona. El farol institucional aparece como laguna (`s/d`) — misma explicación del cuadro de arriba.",
        "ja": "ナラヤマ指数のゾーン別（オーバーバース飽和/PEEC → 崩壊/PEC）に注目7か国を並べたグリッドで、各ゾーン内は現在の人口順です。制度的ビーコンは欠落（N/A）として表示されます — 上記ボックスと同じ説明です。",
        "ko": "나라야마 지수 구역별(과잉출생/PEEC → 붕괴/PEC)로 정리한 주요 7개국 그리드이며, 각 구역 내에서는 현재 인구순으로 정렬됩니다. 제도적 신호등은 공백(N/A)으로 표시됩니다 — 위 상자와 동일한 설명입니다.",
        "it": "Griglia dei 7 paesi in evidenza per zona dell'Indice Narayama (Saturazione/PEEC → Collasso/PEC), paesi ordinati per popolazione attuale all'interno di ogni zona. Il faro istituzionale appare come lacuna (`n/d`) — stessa spiegazione del riquadro sopra.",
        "fi": "7 esitellyn maan ruudukko Narayama-indeksin vyöhykkeen mukaan (ylisyntyvyys/PEEC → romahdus/PEC), maat järjestetty nykyisen väestön mukaan kussakin vyöhykkeessä. Institutionaalinen valo näkyy aukkona (N/A) — sama selitys kuin yllä olevassa laatikossa.",
        "fr": "Grille des 7 pays en vedette par zone de l'indice de Narayama (Surnatalité/PEEC → Effondrement/PEC), pays classés par population actuelle au sein de chaque zone. Le repère institutionnel apparaît comme une lacune (`n/d`) — même explication que l'encadré ci-dessus.",
        "zh": "按楢山指数区域（过度生育/PEEC → 崩溃/PEC）排列的7个重点国家网格，各区域内按当前人口排序。制度信号灯显示为空缺（N/A）——说明同上方信息框。",
    },
    "farol_provisorio_caption": {
        "pt": "Nos 7 países também destacados no narayama.live, existe um valor de farol provisório herdado do modelo demográfico-TFR anterior à atualização do pipeline (Tabela 3.1.1 da tese) — mas a decisão foi não publicá-lo: não vem de fonte real de National Transfer Accounts (NTA). Por isso o farol aparece sempre como `s/d` nos cards, mesmo para esses 7 países.",
        "en": "For the 7 countries also featured on narayama.live, a provisional beacon value exists, inherited from the demographic-TFR model that predates the pipeline update (thesis Table 3.1.1) — but the decision was not to publish it: it doesn't come from a real National Transfer Accounts (NTA) source. That's why the beacon always shows as `n/a` on the cards, even for these 7 countries.",
        "es": "Para los 7 países también destacados en narayama.live, existe un valor de farol provisional heredado del modelo demográfico-TFR anterior a la actualización del pipeline (Tabla 3.1.1 de la tesis) — pero la decisión fue no publicarlo: no proviene de una fuente real de Cuentas de Transferencias Nacionales (NTA). Por eso el farol aparece siempre como `s/d` en las tarjetas, incluso para esos 7 países.",
        "ja": "narayama.liveでも注目されている7か国については、パイプライン更新前の人口統計-TFRモデルから引き継いだ暫定的なビーコン値が存在します（論文の表3.1.1）— しかし、それを公開しないという決定がなされました：実際のNational Transfer Accounts（NTA）のデータ源に基づくものではないためです。そのため、この7か国についても、カードのビーコンは常にN/Aと表示されます。",
        "ko": "narayama.live에서도 강조되는 7개국에 대해서는, 파이프라인 업데이트 이전의 인구통계-TFR 모델에서 물려받은 잠정적인 신호등 값이 존재합니다(논문 표 3.1.1) — 하지만 이를 공개하지 않기로 결정했습니다: 실제 국민이전계정(NTA) 출처에서 나온 것이 아니기 때문입니다. 그래서 이 7개국에 대해서도 카드의 신호등은 항상 N/A로 표시됩니다.",
        "it": "Per i 7 paesi anche in evidenza su narayama.live, esiste un valore di faro provvisorio ereditato dal modello demografico-TFR precedente all'aggiornamento della pipeline (Tabella 3.1.1 della tesi) — ma la decisione è stata di non pubblicarlo: non proviene da una fonte reale di National Transfer Accounts (NTA). Per questo il faro appare sempre come `n/d` nelle card, anche per questi 7 paesi.",
        "fi": "Myös narayama.liven 7 esitellylle maalle on olemassa väliaikainen valoarvo, joka on peritty putken päivitystä edeltävästä väestötieteellis-TFR-mallista (väitöskirjan taulukko 3.1.1) — mutta päätös oli olla julkaisematta sitä: se ei perustu todelliseen National Transfer Accounts (NTA) -lähteeseen. Siksi valo näkyy korteissa aina merkinnällä N/A, myös näiden 7 maan kohdalla.",
        "fr": "Pour les 7 pays également mis en avant sur narayama.live, il existe une valeur de repère provisoire héritée du modèle démographique-TFR antérieur à la mise à jour du pipeline (Tableau 3.1.1 de la thèse) — mais la décision a été de ne pas la publier : elle ne provient pas d'une source réelle de National Transfer Accounts (NTA). C'est pourquoi le repère apparaît toujours comme `n/d` sur les cartes, même pour ces 7 pays.",
        "zh": "在narayama.live同样重点展示的7个国家中，存在一个继承自流水线更新之前人口统计-TFR模型的临时信号灯数值（论文表3.1.1）——但决定是不公开它：因为它并非来自真实的国民转移账户（NTA）来源。因此，即使是这7个国家，卡片上的信号灯也始终显示为N/A。",
    },
    "caption_arrow_narayama": {
        "pt": "**A seta compara dois cenários no mesmo ano (2074), não hoje vs. futuro**: P_tendência → P_eq. **P_tendência**: população em 2074 se a fecundidade real de cada país seguir sem mudança (dado real UN WPP 2024, variante \"Zero migration\"). **P_eq**: população em 2074 num cenário PROPOSTO em que o país converge linearmente até TFR=2,1 ao longo de 25 anos (2024-2049) e mantém essa taxa por mais 25 anos (2049-2074) — sempre com migração zerada. Comparar as duas no mesmo ano isola o efeito da recuperação de fecundidade da simples inércia etária (que sozinha já pode fazer a população crescer por décadas, mesmo sem mudança nenhuma — caso do Brasil). **Não é uma previsão nem um dado direto da ONU**: os nascimentos usados na simulação de P_eq são reais, só escalados pela razão entre a TFR proposta e a TFR real projetada pela ONU, ano a ano — óbitos ficam com o valor real. Simplificação documentada, não um modelo de coorte por idade. Ver [ainu.systems](https://ainu.systems) para o detalhamento completo.",
        "en": "**The arrow compares two scenarios in the same year (2074), not today vs. the future**: P_tendência → P_eq. **P_tendência**: population in 2074 if each country's real fertility continues unchanged (real UN WPP 2024 data, \"Zero migration\" variant). **P_eq**: population in 2074 under a PROPOSED scenario where the country converges linearly to TFR=2.1 over 25 years (2024-2049) and holds that rate for 25 more years (2049-2074) — always with zero migration. Comparing both in the same year isolates the effect of fertility recovery from plain age inertia (which alone can already make a population grow for decades, even with no change at all — Brazil's case). **This is not a forecast nor direct UN data**: the births used in the P_eq simulation are real, only scaled by the ratio between the proposed TFR and the UN's real projected TFR, year by year — deaths keep their real value. A documented simplification, not an age-cohort model. See [ainu.systems](https://ainu.systems) for the full detail.",
        "es": "**La flecha compara dos escenarios en el mismo año (2074), no hoy vs. futuro**: P_tendencia → P_eq. **P_tendencia**: población en 2074 si la fecundidad real de cada país continúa sin cambios (dato real UN WPP 2024, variante \"Zero migration\"). **P_eq**: población en 2074 bajo un escenario PROPUESTO en que el país converge linealmente hasta TFR=2,1 a lo largo de 25 años (2024-2049) y mantiene esa tasa por 25 años más (2049-2074) — siempre con migración cero. Comparar ambas en el mismo año aísla el efecto de la recuperación de fecundidad de la simple inercia etaria (que por sí sola ya puede hacer crecer la población por décadas, aun sin cambio alguno — caso de Brasil). **No es una previsión ni un dato directo de la ONU**: los nacimientos usados en la simulación de P_eq son reales, solo escalados por la razón entre la TFR propuesta y la TFR real proyectada por la ONU, año a año — las defunciones mantienen el valor real. Simplificación documentada, no un modelo de cohorte por edad. Ver [ainu.systems](https://ainu.systems) para el detalle completo.",
        "ja": "**この矢印は同じ年（2074年）の2つのシナリオを比較するもので、今日対未来ではありません**：P_tendência → P_eq。**P_tendência**：各国の実際の出生力が変わらず続いた場合の2074年の人口（実際のUN WPP 2024データ、「Zero migration」バリアント）。**P_eq**：その国が25年間（2024-2049年）でTFR=2.1に線形収束し、その後さらに25年間（2049-2074年）そのTFRを維持するという、提案されたシナリオでの2074年の人口 — 常に移民ゼロ。同じ年で両者を比較することで、出生力回復の効果を単なる年齢構成の慣性（それだけでも何十年も人口を増加させうる — ブラジルの例）から切り離せます。**これは予測でも国連の直接データでもありません**：P_eqのシミュレーションに使われる出生数は実データで、提案TFRと国連の実際の予測TFRとの比率で年ごとに調整されているだけです — 死亡数は実際の値のままです。文書化された簡略化であり、年齢コーホートモデルではありません。詳細は[ainu.systems](https://ainu.systems)をご覧ください。",
        "ko": "**화살표는 오늘 대 미래가 아니라 같은 해(2074년)의 두 시나리오를 비교합니다**: P_tendência → P_eq. **P_tendência**: 각국의 실제 출산력이 변화 없이 지속될 경우 2074년의 인구(UN WPP 2024 실제 데이터, \"Zero migration\" 변형). **P_eq**: 해당 국가가 25년(2024-2049)에 걸쳐 TFR=2.1로 선형 수렴하고 이후 25년(2049-2074) 더 그 비율을 유지한다는 제안된 시나리오에서의 2074년 인구 — 항상 이주는 0으로 가정. 같은 해에 두 값을 비교하면 출산력 회복의 효과를 단순한 연령 관성(이것만으로도 아무 변화 없이 수십 년간 인구가 증가할 수 있음 — 브라질 사례)에서 분리할 수 있습니다. **이것은 예측도 유엔의 직접 데이터도 아닙니다**: P_eq 시뮬레이션에 사용된 출생아 수는 실제이며, 제안된 TFR과 유엔이 실제로 예측한 TFR의 비율로 매년 조정될 뿐입니다 — 사망자 수는 실제 값을 유지합니다. 문서화된 단순화이며 연령 코호트 모델이 아닙니다. 전체 내용은 [ainu.systems](https://ainu.systems)를 참고하세요.",
        "it": "**La freccia confronta due scenari nello stesso anno (2074), non oggi vs. futuro**: P_tendencia → P_eq. **P_tendencia**: popolazione nel 2074 se la fecondità reale di ogni paese continuasse invariata (dato reale UN WPP 2024, variante \"Zero migration\"). **P_eq**: popolazione nel 2074 in uno scenario PROPOSTO in cui il paese converge linearmente a TFR=2,1 nell'arco di 25 anni (2024-2049) e mantiene quel tasso per altri 25 anni (2049-2074) — sempre con migrazione zero. Confrontare i due nello stesso anno isola l'effetto del recupero della fecondità dalla semplice inerzia anagrafica (che da sola può già far crescere la popolazione per decenni, anche senza alcun cambiamento — caso del Brasile). **Non è una previsione né un dato diretto dell'ONU**: le nascite usate nella simulazione di P_eq sono reali, solo scalate dal rapporto tra la TFR proposta e la TFR reale proiettata dall'ONU, anno per anno — i decessi mantengono il valore reale. Semplificazione documentata, non un modello di coorte per età. Vedi [ainu.systems](https://ainu.systems) per il dettaglio completo.",
        "fi": "**Nuoli vertaa kahta skenaariota samana vuonna (2074), ei tätä päivää tulevaisuuteen**: P_tendencia → P_eq. **P_tendencia**: väestö vuonna 2074, jos kunkin maan todellinen hedelmällisyys jatkuu muuttumattomana (todellinen UN WPP 2024 -data, \"Zero migration\" -variantti). **P_eq**: väestö vuonna 2074 EHDOTETUSSA skenaariossa, jossa maa lähestyy lineaarisesti TFR=2,1:tä 25 vuoden aikana (2024-2049) ja pitää sen tason vielä 25 vuotta (2049-2074) — aina nollamuutolla. Kummankin vertaaminen samana vuonna erottaa hedelmällisyyden elpymisen vaikutuksen pelkästä ikärakenteen hitaudesta (joka yksinään voi jo kasvattaa väestöä vuosikymmeniä ilman mitään muutosta — Brasilian tapaus). **Tämä ei ole ennuste eikä suora YK-data**: P_eq-simulaatiossa käytetyt syntyvyysluvut ovat todellisia, vain skaalattu ehdotetun ja YK:n todella ennustaman TFR:n suhteella vuosittain — kuolleisuus säilyy todellisena. Dokumentoitu yksinkertaistus, ei ikäkohorttimalli. Katso [ainu.systems](https://ainu.systems) täydet tiedot.",
        "fr": "**La flèche compare deux scénarios la même année (2074), pas aujourd'hui contre le futur** : P_tendencia → P_eq. **P_tendencia** : population en 2074 si la fécondité réelle de chaque pays se poursuit sans changement (donnée réelle UN WPP 2024, variante \"Zero migration\"). **P_eq** : population en 2074 dans un scénario PROPOSÉ où le pays converge linéairement vers un TFR=2,1 sur 25 ans (2024-2049) puis maintient ce taux 25 années de plus (2049-2074) — toujours avec migration nulle. Comparer les deux la même année isole l'effet du redressement de la fécondité de la simple inertie d'âge (qui à elle seule peut déjà faire croître la population pendant des décennies, même sans aucun changement — cas du Brésil). **Ce n'est ni une prévision ni une donnée directe de l'ONU** : les naissances utilisées dans la simulation de P_eq sont réelles, seulement mises à l'échelle par le rapport entre le TFR proposé et le TFR réel projeté par l'ONU, année par année — les décès conservent leur valeur réelle. Simplification documentée, pas un modèle de cohorte par âge. Voir [ainu.systems](https://ainu.systems) pour le détail complet.",
        "zh": "**箭头比较的是同一年（2074年）的两种情景，而非今天与未来的对比**：P_tendência → P_eq。**P_tendência**：如果各国实际生育率保持不变，2074年的人口（联合国UN WPP 2024真实数据，\"Zero migration\"情景）。**P_eq**：在一个提议情景下2074年的人口——该国在25年内（2024-2049年）线性收敛至TFR=2.1，并在此后25年（2049-2074年）保持该水平——始终假设零迁移。在同一年比较两者，可以将生育率恢复的效果与单纯的年龄结构惯性（仅凭这一点就可能让人口在几十年内持续增长，即使毫无变化——巴西即是如此）区分开。**这不是预测，也不是联合国的直接数据**：P_eq模拟中使用的出生人数是真实的，只是按提议TFR与联合国实际预测TFR的比率逐年调整——死亡人数保持真实值。这是一种有文档记录的简化，而非按年龄分组的队列模型。完整细节见[ainu.systems](https://ainu.systems)。",
    },
    "footer_narayama": {
        "pt": "**Dados**: UN World Population Prospects  \n**Metodologia**: Tese \"Do Dilema de Narayama ao Oicoceno Civilizacional\" v9.2  \n**Análise detalhada**: [ainu.systems](https://ainu.systems)",
        "en": "**Data**: UN World Population Prospects  \n**Methodology**: Thesis \"From Narayama's Dilemma to the Civilizational Oikocene\" v9.2  \n**Detailed analysis**: [ainu.systems](https://ainu.systems)",
        "es": "**Datos**: UN World Population Prospects  \n**Metodología**: Tesis \"Del Dilema de Narayama al Oicoceno Civilizacional\" v9.2  \n**Análisis detallado**: [ainu.systems](https://ainu.systems)",
        "ja": "**データ**: UN World Population Prospects  \n**方法論**: 博士論文『ナラヤマのジレンマから文明的オイコセーンへ』v9.2  \n**詳細分析**: [ainu.systems](https://ainu.systems)",
        "ko": "**데이터**: UN World Population Prospects  \n**방법론**: 논문 『나라야마의 딜레마에서 문명적 오이코세까지』 v9.2  \n**상세 분석**: [ainu.systems](https://ainu.systems)",
        "it": "**Dati**: UN World Population Prospects  \n**Metodologia**: Tesi \"Dal Dilemma di Narayama all'Oicocene Civilizzazionale\" v9.2  \n**Analisi dettagliata**: [ainu.systems](https://ainu.systems)",
        "fi": "**Data**: UN World Population Prospects  \n**Menetelmä**: Väitöskirja \"Narayaman dilemmasta sivilisaation Oikoseeniin\" v9.2  \n**Yksityiskohtainen analyysi**: [ainu.systems](https://ainu.systems)",
        "fr": "**Données** : UN World Population Prospects  \n**Méthodologie** : Thèse \"Du Dilemme de Narayama à l'Oïcocène Civilisationnel\" v9.2  \n**Analyse détaillée** : [ainu.systems](https://ainu.systems)",
        "zh": "**数据**：UN World Population Prospects  \n**方法论**：论文《从楢山难题到文明世的宜居纪》v9.2  \n**详细分析**：[ainu.systems](https://ainu.systems)",
    },

    # --- ainu.systems ------------------------------------------------------
    "ainu_subtitulo": {
        "pt": "Plataforma restrita a pesquisadores e formuladores de política",
        "en": "Platform restricted to researchers and policymakers",
        "es": "Plataforma restringida a investigadores y formuladores de políticas",
        "ja": "研究者および政策立案者限定プラットフォーム",
        "ko": "연구자 및 정책 입안자 전용 플랫폼",
        "it": "Piattaforma riservata a ricercatori e responsabili politici",
        "fi": "Alusta rajattu tutkijoille ja päättäjille",
        "fr": "Plateforme réservée aux chercheurs et décideurs politiques",
        "zh": "面向研究人员与政策制定者的限制访问平台",
    },
    "ainu_intro": {
        "pt": "Cálculos detalhados do Índice de Narayama Sistêmico (N*) para os 28 países da amostra, com base na tese de doutorado \"Do Dilema de Narayama ao Oicoceno Civilizacional\" (v9.2). Para a visão pública e simplificada, veja [narayama.live](https://narayama.live).",
        "en": "Detailed calculations of the Systemic Narayama Index (N*) for the 28 countries in the sample, based on the doctoral thesis \"From Narayama's Dilemma to the Civilizational Oikocene\" (v9.2). For the public, simplified view, see [narayama.live](https://narayama.live).",
        "es": "Cálculos detallados del Índice de Narayama Sistémico (N*) para los 28 países de la muestra, según la tesis doctoral \"Del Dilema de Narayama al Oicoceno Civilizacional\" (v9.2). Para la vista pública y simplificada, vea [narayama.live](https://narayama.live).",
        "ja": "博士論文『ナラヤマのジレンマから文明的オイコセーンへ』（v9.2）に基づく、サンプル28か国のシステミック・ナラヤマ指数（N*）の詳細な計算です。公開・簡易版は[narayama.live](https://narayama.live)をご覧ください。",
        "ko": "박사 학위논문 『나라야마의 딜레마에서 문명적 오이코세까지』(v9.2)를 바탕으로 한 표본 28개국의 체계적 나라야마 지수(N*) 상세 계산입니다. 공개용 간략 버전은 [narayama.live](https://narayama.live)를 참고하세요.",
        "it": "Calcoli dettagliati dell'Indice di Narayama Sistemico (N*) per i 28 paesi del campione, sulla base della tesi di dottorato \"Dal Dilemma di Narayama all'Oicocene Civilizzazionale\" (v9.2). Per la vista pubblica e semplificata, vedi [narayama.live](https://narayama.live).",
        "fi": "Yksityiskohtaiset laskelmat systeemisestä Narayama-indeksistä (N*) otoksen 28 maalle, perustuen väitöskirjaan \"Narayaman dilemmasta sivilisaation Oikoseeniin\" (v9.2). Julkista, yksinkertaistettua näkymää varten katso [narayama.live](https://narayama.live).",
        "fr": "Calculs détaillés de l'indice de Narayama systémique (N*) pour les 28 pays de l'échantillon, d'après la thèse de doctorat \"Du Dilemme de Narayama à l'Oïcocène Civilisationnel\" (v9.2). Pour la vue publique simplifiée, voir [narayama.live](https://narayama.live).",
        "zh": "基于博士论文《从楢山难题到文明世的宜居纪》(v9.2)，对样本中28个国家的系统性楢山指数（N*）进行详细计算。公开简化版请见[narayama.live](https://narayama.live)。",
    },
    "auth_nao_configurada": {
        "pt": "Autenticação não configurada nesta instância (Fase 1 — placeholder). Defina a variável de ambiente `AINU_SYSTEMS_PASSWORD` para restringir o acesso.",
        "en": "Authentication not configured on this instance (Phase 1 — placeholder). Set the `AINU_SYSTEMS_PASSWORD` environment variable to restrict access.",
        "es": "Autenticación no configurada en esta instancia (Fase 1 — provisional). Defina la variable de entorno `AINU_SYSTEMS_PASSWORD` para restringir el acceso.",
        "ja": "このインスタンスでは認証が設定されていません（フェーズ1・プレースホルダー）。アクセスを制限するには環境変数`AINU_SYSTEMS_PASSWORD`を設定してください。",
        "ko": "이 인스턴스에는 인증이 설정되어 있지 않습니다(1단계 — 임시). 접근을 제한하려면 환경 변수 `AINU_SYSTEMS_PASSWORD`를 설정하세요.",
        "it": "Autenticazione non configurata in questa istanza (Fase 1 — segnaposto). Imposta la variabile d'ambiente `AINU_SYSTEMS_PASSWORD` per limitare l'accesso.",
        "fi": "Todennusta ei ole määritetty tässä instanssissa (vaihe 1 — paikkamerkki). Aseta ympäristömuuttuja `AINU_SYSTEMS_PASSWORD` rajoittaaksesi pääsyä.",
        "fr": "Authentification non configurée sur cette instance (Phase 1 — provisoire). Définissez la variable d'environnement `AINU_SYSTEMS_PASSWORD` pour restreindre l'accès.",
        "zh": "此实例尚未配置身份验证（第1阶段——占位）。请设置环境变量`AINU_SYSTEMS_PASSWORD`以限制访问。",
    },
    "senha_prompt": {
        "pt": "Senha de acesso (ainu.systems)", "en": "Access password (ainu.systems)",
        "es": "Contraseña de acceso (ainu.systems)", "ja": "アクセスパスワード（ainu.systems）",
        "ko": "접근 비밀번호 (ainu.systems)", "it": "Password di accesso (ainu.systems)",
        "fi": "Pääsysalasana (ainu.systems)", "fr": "Mot de passe d'accès (ainu.systems)",
        "zh": "访问密码（ainu.systems）",
    },
    "senha_incorreta": {
        "pt": "Senha incorreta.", "en": "Incorrect password.", "es": "Contraseña incorrecta.",
        "ja": "パスワードが正しくありません。", "ko": "비밀번호가 올바르지 않습니다.",
        "it": "Password errata.", "fi": "Väärä salasana.", "fr": "Mot de passe incorrect.",
        "zh": "密码错误。",
    },
    "ainu_warning_sem_dado": {
        "pt": "Nenhum dado encontrado em `data/processed/n_index_2024.csv`. Este arquivo ainda não foi gerado pelo pipeline de cálculo (Fase 2). As seções abaixo aparecem vazias até que os dados existam.",
        "en": "No data found in `data/processed/n_index_2024.csv`. This file hasn't been generated by the calculation pipeline yet (Phase 2). The sections below appear empty until the data exists.",
        "es": "No se encontraron datos en `data/processed/n_index_2024.csv`. Este archivo aún no ha sido generado por el pipeline de cálculo (Fase 2). Las secciones de abajo aparecen vacías hasta que existan los datos.",
        "ja": "`data/processed/n_index_2024.csv` にデータが見つかりません。この計算パイプライン（フェーズ2）はまだ生成されていません。データが存在するまで、以下のセクションは空のまま表示されます。",
        "ko": "`data/processed/n_index_2024.csv`에서 데이터를 찾을 수 없습니다. 이 파일은 아직 계산 파이프라인(2단계)에서 생성되지 않았습니다. 데이터가 존재할 때까지 아래 섹션은 비어 있게 표시됩니다.",
        "it": "Nessun dato trovato in `data/processed/n_index_2024.csv`. Questo file non è ancora stato generato dalla pipeline di calcolo (Fase 2). Le sezioni sottostanti appaiono vuote finché i dati non esistono.",
        "fi": "Tietoja ei löytynyt tiedostosta `data/processed/n_index_2024.csv`. Laskentaputki (vaihe 2) ei ole vielä luonut tätä tiedostoa. Alla olevat osiot näkyvät tyhjinä, kunnes data on olemassa.",
        "fr": "Aucune donnée trouvée dans `data/processed/n_index_2024.csv`. Ce fichier n'a pas encore été généré par le pipeline de calcul (Phase 2). Les sections ci-dessous apparaissent vides tant que les données n'existent pas.",
        "zh": "在`data/processed/n_index_2024.csv`中未找到数据。计算流水线（第2阶段）尚未生成此文件。数据生成之前，以下各部分将显示为空。",
    },
    "filtros_header": {
        "pt": "Filtros", "en": "Filters", "es": "Filtros", "ja": "フィルター", "ko": "필터",
        "it": "Filtri", "fi": "Suodattimet", "fr": "Filtres", "zh": "筛选条件",
    },
    "perfil_label": {
        "pt": "Perfil", "en": "Profile", "es": "Perfil", "ja": "プロファイル", "ko": "프로필",
        "it": "Profilo", "fi": "Profiili", "fr": "Profil", "zh": "类型",
    },
    "todos": {
        "pt": "Todos", "en": "All", "es": "Todos", "ja": "すべて", "ko": "전체",
        "it": "Tutti", "fi": "Kaikki", "fr": "Tous", "zh": "全部",
    },
    "regiao_label": {
        "pt": "Região", "en": "Region", "es": "Región", "ja": "地域", "ko": "지역",
        "it": "Regione", "fi": "Alue", "fr": "Région", "zh": "地区",
    },
    "todas": {
        "pt": "Todas", "en": "All", "es": "Todas", "ja": "すべて", "ko": "전체",
        "it": "Tutte", "fi": "Kaikki", "fr": "Toutes", "zh": "全部",
    },
    "buscar_pais_label": {
        "pt": "Buscar país", "en": "Search country", "es": "Buscar país", "ja": "国を検索",
        "ko": "국가 검색", "it": "Cerca paese", "fi": "Hae maata", "fr": "Rechercher un pays",
        "zh": "搜索国家",
    },
    "estatisticas_header": {
        "pt": "Estatísticas", "en": "Statistics", "es": "Estadísticas", "ja": "統計",
        "ko": "통계", "it": "Statistiche", "fi": "Tilastot", "fr": "Statistiques", "zh": "统计",
    },
    "paises_por_zona_label": {
        "pt": "**Países por zona de N\\*:**", "en": "**Countries by N\\* zone:**",
        "es": "**Países por zona de N\\*:**", "ja": "**N\\*ゾーン別の国数:**",
        "ko": "**N\\* 구역별 국가 수:**", "it": "**Paesi per zona di N\\*:**",
        "fi": "**Maat N\\*-vyöhykkeittäin:**", "fr": "**Pays par zone de N\\* :**",
        "zh": "**按N\\*区域划分的国家数：**",
    },
    "risco_peec_label": {
        "pt": "Risco PEEC (TFR > {limiar}): {valor}", "en": "PEEC risk (TFR > {limiar}): {valor}",
        "es": "Riesgo PEEC (TFR > {limiar}): {valor}", "ja": "PEECリスク（TFR > {limiar}）：{valor}",
        "ko": "PEEC 위험 (TFR > {limiar}): {valor}", "it": "Rischio PEEC (TFR > {limiar}): {valor}",
        "fi": "PEEC-riski (TFR > {limiar}): {valor}", "fr": "Risque PEEC (TFR > {limiar}) : {valor}",
        "zh": "PEEC风险（TFR > {limiar}）：{valor}",
    },
    "n_medio_perfil_label": {
        "pt": "**N\\* médio por perfil:**", "en": "**Average N\\* by profile:**",
        "es": "**N\\* promedio por perfil:**", "ja": "**プロファイル別平均N\\*:**",
        "ko": "**프로필별 평균 N\\*:**", "it": "**N\\* medio per profilo:**",
        "fi": "**Keskimääräinen N\\* profiileittain:**", "fr": "**N\\* moyen par profil :**",
        "zh": "**按类型划分的平均N\\*：**",
    },
    "fator_alocativo_medio_regiao_label": {
        "pt": "**Fator_Alocativo médio por região:**", "en": "**Average Fator_Alocativo by region:**",
        "es": "**Fator_Alocativo promedio por región:**", "ja": "**地域別平均Fator_Alocativo:**",
        "ko": "**지역별 평균 Fator_Alocativo:**", "it": "**Fator_Alocativo medio per regione:**",
        "fi": "**Keskimääräinen Fator_Alocativo alueittain:**", "fr": "**Fator_Alocativo moyen par région :**",
        "zh": "**按地区划分的平均Fator_Alocativo：**",
    },
    "sem_dados_carregados": {
        "pt": "Sem dados carregados.", "en": "No data loaded.", "es": "Sin datos cargados.",
        "ja": "データが読み込まれていません。", "ko": "로드된 데이터가 없습니다.",
        "it": "Nessun dato caricato.", "fi": "Ei ladattua dataa.", "fr": "Aucune donnée chargée.",
        "zh": "未加载数据。",
    },
    "tabela_principal_header": {
        "pt": "Tabela Principal — N* por País (2024)", "en": "Main Table — N* by Country (2024)",
        "es": "Tabla Principal — N* por País (2024)", "ja": "メインテーブル — 国別N*（2024年）",
        "ko": "메인 표 — 국가별 N* (2024)", "it": "Tabella Principale — N* per Paese (2024)",
        "fi": "Päätaulukko — N* maittain (2024)", "fr": "Tableau principal — N* par pays (2024)",
        "zh": "主表 — 各国N*（2024年）",
    },
    "tabela_principal_caption": {
        "pt": "N* = raiz quadrada do N_Base (decisão de 2026-07-09, sendo incorporada pelo autor na tese) — normaliza os casos extremos de países jovens/alta fecundidade sem empatar países entre si nem usar constante arbitrária. `N_Base` (valor demográfico bruto) fica ao lado, pra transparência. `NGII_Puro` já é depurado pelo Protocolo de Falseabilidade quantitativo (4 ajustes multiplicativos — migração, inércia demográfica, políticas natalistas temporárias, sub-registro/mortalidade — Anexo 9, v9.0); `NGII_Bruto` é o valor sem esse ajuste. `Farol`/`Fator_Aloc` aparecem como \"Pendente (NTA)\" porque dependem de National Transfer Accounts, ainda não integrado (Fase 2b). Detalhes em [docs/definitions.md](../../docs/definitions.md), seções 6, 7 e 8.",
        "en": "N* = square root of N_Base (2026-07-09 decision, being incorporated by the author into the thesis) — normalizes the extreme cases of young/high-fertility countries without tying countries to each other or using an arbitrary constant. `N_Base` (raw demographic value) sits alongside it, for transparency. `NGII_Puro` is already refined by the quantitative Falsifiability Protocol (4 multiplicative adjustments — migration, demographic inertia, temporary pronatalist policies, under-registration/mortality — Annex 9, v9.0); `NGII_Bruto` is the value without that adjustment. `Farol`/`Fator_Aloc` show as \"Pending (NTA)\" because they depend on National Transfer Accounts, not yet integrated (Phase 2b). Details in [docs/definitions.md](../../docs/definitions.md), sections 6, 7 and 8.",
        "es": "N* = raíz cuadrada del N_Base (decisión de 2026-07-09, siendo incorporada por el autor en la tesis) — normaliza los casos extremos de países jóvenes/alta fecundidad sin igualar países entre sí ni usar una constante arbitraria. `N_Base` (valor demográfico bruto) queda al lado, para transparencia. `NGII_Puro` ya está depurado por el Protocolo de Falseabilidad cuantitativo (4 ajustes multiplicativos — migración, inercia demográfica, políticas natalistas temporales, subregistro/mortalidad — Anexo 9, v9.0); `NGII_Bruto` es el valor sin ese ajuste. `Farol`/`Fator_Aloc` aparecen como \"Pendiente (NTA)\" porque dependen de National Transfer Accounts, aún no integrado (Fase 2b). Detalles en [docs/definitions.md](../../docs/definitions.md), secciones 6, 7 y 8.",
        "ja": "N\\* = N_Baseの平方根（2026年7月9日の決定、著者が論文に組み込み中）— 若年層・高出生率の国の極端なケースを、国同士を等しくしたり恣意的な定数を使ったりせずに正規化します。`N_Base`（生の人口統計値）は透明性のため隣に表示されます。`NGII_Puro`は既に定量的反証可能性プロトコル（4つの乗法的調整 — 移民、人口学的慣性、一時的な出産奨励政策、過小登録/死亡率 — 附属書9、v9.0）で精緻化済みです。`NGII_Bruto`はその調整前の値です。`Farol`/`Fator_Aloc`は「保留中（NTA）」と表示されますが、これはNational Transfer Accountsに依存しており、まだ統合されていないためです（フェーズ2b）。詳細は[docs/definitions.md](../../docs/definitions.md)の第6、7、8節をご覧ください。",
        "ko": "N\\* = N_Base의 제곱근(2026-07-09 결정, 저자가 논문에 반영 중) — 국가 간 순위를 동일하게 만들거나 임의의 상수를 쓰지 않고 청년층/고출산 국가의 극단적 사례를 정규화합니다. `N_Base`(원시 인구통계 값)는 투명성을 위해 옆에 표시됩니다. `NGII_Puro`는 이미 정량적 반증가능성 프로토콜(4가지 곱셈 조정 — 이주, 인구학적 관성, 일시적 출산장려 정책, 미등록/사망률 — 부록 9, v9.0)로 정제되었습니다. `NGII_Bruto`는 이 조정이 적용되지 않은 값입니다. `Farol`/`Fator_Aloc`은 국민이전계정(NTA)에 의존하며 아직 통합되지 않았기 때문에(2b단계) \"보류 중(NTA)\"으로 표시됩니다. 자세한 내용은 [docs/definitions.md](../../docs/definitions.md) 6, 7, 8절을 참고하세요.",
        "it": "N* = radice quadrata di N_Base (decisione del 2026-07-09, in corso di incorporazione da parte dell'autore nella tesi) — normalizza i casi estremi di paesi giovani/ad alta fecondità senza pareggiare i paesi tra loro né usare una costante arbitraria. `N_Base` (valore demografico grezzo) resta accanto, per trasparenza. `NGII_Puro` è già depurato dal Protocollo di Falsificabilità quantitativo (4 aggiustamenti moltiplicativi — migrazione, inerzia demografica, politiche natalistiche temporanee, sotto-registrazione/mortalità — Allegato 9, v9.0); `NGII_Bruto` è il valore senza tale aggiustamento. `Farol`/`Fator_Aloc` appaiono come \"In sospeso (NTA)\" perché dipendono dai National Transfer Accounts, non ancora integrati (Fase 2b). Dettagli in [docs/definitions.md](../../docs/definitions.md), sezioni 6, 7 e 8.",
        "fi": "N* = N_Basen neliöjuuri (päätös 2026-07-09, tekijä sisällyttää sen väitöskirjaan) — normalisoi nuorten/korkean hedelmällisyyden maiden ääritapaukset ilman maiden tasoittamista keskenään tai mielivaltaisen vakion käyttöä. `N_Base` (raaka väestötieteellinen arvo) on vieressä läpinäkyvyyden vuoksi. `NGII_Puro` on jo puhdistettu kvantitatiivisella falsifioitavuusprotokollalla (4 kertovaa korjausta — muuttoliike, demografinen hitaus, tilapäiset syntyvyyttä tukevat politiikat, alirekisteröinti/kuolleisuus — liite 9, v9.0); `NGII_Bruto` on arvo ilman tätä korjausta. `Farol`/`Fator_Aloc` näkyvät \"Odottaa (NTA)\" -tilassa, koska ne riippuvat National Transfer Accounts -tiedoista, joita ei ole vielä integroitu (vaihe 2b). Lisätiedot [docs/definitions.md](../../docs/definitions.md), osat 6, 7 ja 8.",
        "fr": "N* = racine carrée du N_Base (décision du 2026-07-09, en cours d'intégration par l'auteur dans la thèse) — normalise les cas extrêmes des pays jeunes/à forte fécondité sans égaliser les pays entre eux ni utiliser de constante arbitraire. `N_Base` (valeur démographique brute) figure à côté, pour la transparence. `NGII_Puro` est déjà épuré par le Protocole de Falsifiabilité quantitatif (4 ajustements multiplicatifs — migration, inertie démographique, politiques natalistes temporaires, sous-enregistrement/mortalité — Annexe 9, v9.0) ; `NGII_Bruto` est la valeur sans cet ajustement. `Farol`/`Fator_Aloc` apparaissent comme \"En attente (NTA)\" car ils dépendent des National Transfer Accounts, pas encore intégrés (Phase 2b). Détails dans [docs/definitions.md](../../docs/definitions.md), sections 6, 7 et 8.",
        "zh": "N* = N_Base的平方根（2026年7月9日的决定，作者正将其纳入论文）——在不使各国相互拉平、也不使用任意常数的情况下，对年轻/高生育率国家的极端情形进行归一化。`N_Base`（原始人口统计值）显示在旁边以保持透明。`NGII_Puro`已通过定量可证伪性协议（4项乘法调整——移民、人口惯性、临时鼓励生育政策、漏报/死亡率——附录9，v9.0）进行了净化；`NGII_Bruto`是未经此调整的值。`Farol`/`Fator_Aloc`显示为“待定（NTA）”，因为它们依赖于尚未整合的国民转移账户（第2b阶段）。详情见[docs/definitions.md](../../docs/definitions.md)第6、7、8节。",
    },
    "pendente_nta": {
        "pt": "Pendente (NTA)", "en": "Pending (NTA)", "es": "Pendiente (NTA)",
        "ja": "保留中（NTA）", "ko": "보류 중 (NTA)", "it": "In sospeso (NTA)",
        "fi": "Odottaa (NTA)", "fr": "En attente (NTA)", "zh": "待定（NTA）",
    },
    "col_farol": {
        "pt": "Farol", "en": "Beacon", "es": "Farol", "ja": "ビーコン", "ko": "신호등",
        "it": "Faro", "fi": "Valo", "fr": "Repère", "zh": "信号灯",
    },
    "nenhum_pais_filtro": {
        "pt": "Nenhum país corresponde aos filtros selecionados (ou não há dados carregados).",
        "en": "No country matches the selected filters (or no data is loaded).",
        "es": "Ningún país corresponde a los filtros seleccionados (o no hay datos cargados).",
        "ja": "選択したフィルターに一致する国がありません（またはデータが読み込まれていません）。",
        "ko": "선택한 필터에 해당하는 국가가 없습니다(또는 데이터가 로드되지 않았습니다).",
        "it": "Nessun paese corrisponde ai filtri selezionati (o non ci sono dati caricati).",
        "fi": "Yksikään maa ei vastaa valittuja suodattimia (tai dataa ei ole ladattu).",
        "fr": "Aucun pays ne correspond aux filtres sélectionnés (ou aucune donnée n'est chargée).",
        "zh": "没有国家符合所选筛选条件（或未加载数据）。",
    },
    "scatter_header": {
        "pt": "NGII_puro vs Fator_Alocativo (28 países, 2024)", "en": "NGII_puro vs Fator_Alocativo (28 countries, 2024)",
        "es": "NGII_puro vs Fator_Alocativo (28 países, 2024)", "ja": "NGII_puro 対 Fator_Alocativo（28か国、2024年）",
        "ko": "NGII_puro 대 Fator_Alocativo (28개국, 2024)", "it": "NGII_puro vs Fator_Alocativo (28 paesi, 2024)",
        "fi": "NGII_puro vs Fator_Alocativo (28 maata, 2024)", "fr": "NGII_puro vs Fator_Alocativo (28 pays, 2024)",
        "zh": "NGII_puro 与 Fator_Alocativo 对比（28个国家，2024年）",
    },
    "scatter_fallback": {
        "pt": "Gráfico indisponível: faltam dados ou a coluna `populacao` em `data/processed/n_index_2024.csv`.",
        "en": "Chart unavailable: missing data or the `populacao` column in `data/processed/n_index_2024.csv`.",
        "es": "Gráfico no disponible: faltan datos o la columna `populacao` en `data/processed/n_index_2024.csv`.",
        "ja": "グラフは利用できません：`data/processed/n_index_2024.csv` にデータまたは `populacao` 列がありません。",
        "ko": "차트를 사용할 수 없습니다: `data/processed/n_index_2024.csv`에 데이터 또는 `populacao` 열이 없습니다.",
        "it": "Grafico non disponibile: mancano dati o la colonna `populacao` in `data/processed/n_index_2024.csv`.",
        "fi": "Kaavio ei ole saatavilla: dataa tai `populacao`-sarake puuttuu tiedostosta `data/processed/n_index_2024.csv`.",
        "fr": "Graphique indisponible : données manquantes ou colonne `populacao` absente dans `data/processed/n_index_2024.csv`.",
        "zh": "图表不可用：`data/processed/n_index_2024.csv`中缺少数据或`populacao`列。",
    },
    "serie_historica_header": {
        "pt": "Evolução do N* — Série Histórica", "en": "N* Evolution — Historical Series",
        "es": "Evolución del N* — Serie Histórica", "ja": "N*の推移 — 過去のシリーズ",
        "ko": "N* 변화 추이 — 과거 시계열", "it": "Evoluzione dell'N* — Serie Storica",
        "fi": "N*:n kehitys — Historiallinen sarja", "fr": "Évolution du N* — Série historique",
        "zh": "N*演变 — 历史序列",
    },
    "selecione_paises_label": {
        "pt": "Selecione de 3 a 5 países", "en": "Select 3 to 5 countries",
        "es": "Seleccione de 3 a 5 países", "ja": "3〜5か国を選択してください",
        "ko": "3~5개국을 선택하세요", "it": "Seleziona da 3 a 5 paesi",
        "fi": "Valitse 3–5 maata", "fr": "Sélectionnez de 3 à 5 pays", "zh": "请选择3至5个国家",
    },
    "selecione_ao_menos_um_pais": {
        "pt": "Selecione ao menos um país para exibir a série histórica.",
        "en": "Select at least one country to display the historical series.",
        "es": "Seleccione al menos un país para mostrar la serie histórica.",
        "ja": "過去のシリーズを表示するには、少なくとも1か国を選択してください。",
        "ko": "과거 시계열을 표시하려면 최소 한 국가를 선택하세요.",
        "it": "Seleziona almeno un paese per visualizzare la serie storica.",
        "fi": "Valitse vähintään yksi maa nähdäksesi historiallisen sarjan.",
        "fr": "Sélectionnez au moins un pays pour afficher la série historique.",
        "zh": "请至少选择一个国家以显示历史序列。",
    },
    "serie_historica_indisponivel": {
        "pt": "Série histórica indisponível: `data/processed/n_index_historico.csv` ainda não foi gerado pelo pipeline (Fase 2+).",
        "en": "Historical series unavailable: `data/processed/n_index_historico.csv` hasn't been generated by the pipeline yet (Phase 2+).",
        "es": "Serie histórica no disponible: `data/processed/n_index_historico.csv` aún no ha sido generado por el pipeline (Fase 2+).",
        "ja": "過去のシリーズは利用できません：`data/processed/n_index_historico.csv` はまだパイプライン（フェーズ2+）で生成されていません。",
        "ko": "과거 시계열을 사용할 수 없습니다: `data/processed/n_index_historico.csv`가 아직 파이프라인(2단계+)에서 생성되지 않았습니다.",
        "it": "Serie storica non disponibile: `data/processed/n_index_historico.csv` non è ancora stato generato dalla pipeline (Fase 2+).",
        "fi": "Historiallinen sarja ei ole saatavilla: `data/processed/n_index_historico.csv` ei ole vielä putken (vaihe 2+) luoma.",
        "fr": "Série historique indisponible : `data/processed/n_index_historico.csv` n'a pas encore été généré par le pipeline (Phase 2+).",
        "zh": "历史序列不可用：流水线（第2阶段以上）尚未生成`data/processed/n_index_historico.csv`。",
    },
    "tabela_geracional_caption_ainu": {
        "pt": "Grade comparativa dos 28 países segundo o N* (Seção 9-A.7 da tese, revisão de 12/07/2026). Eixo horizontal = zona do Índice Narayama (Saturação/PEEC → Colapso/PEC); eixo vertical, dentro de cada zona = população atual, maior no topo. Mostra sempre os 28 países, independente dos filtros de Perfil/Região acima.",
        "en": "Comparative grid of the 28 countries by N* (thesis Section 9-A.7, 2026-07-12 revision). Horizontal axis = Narayama Index zone (Overbirths/PEEC → Collapse/PEC); vertical axis, within each zone = current population, largest at the top. Always shows all 28 countries, regardless of the Profile/Region filters above.",
        "es": "Cuadrícula comparativa de los 28 países según el N* (Sección 9-A.7 de la tesis, revisión del 12/07/2026). Eje horizontal = zona del Índice Narayama (Saturación/PEEC → Colapso/PEC); eje vertical, dentro de cada zona = población actual, mayor arriba. Muestra siempre los 28 países, independientemente de los filtros de Perfil/Región de arriba.",
        "ja": "N\\*による28か国の比較グリッド（論文セクション9-A.7、2026年7月12日改訂）。横軸＝ナラヤマ指数のゾーン（オーバーバース飽和/PEEC → 崩壊/PEC）、各ゾーン内の縦軸＝現在の人口（上ほど多い）。上部のプロファイル/地域フィルターにかかわらず、常に28か国すべてを表示します。",
        "ko": "N\\*에 따른 28개국 비교 그리드(논문 9-A.7절, 2026-07-12 개정). 가로축 = 나라야마 지수 구역(과잉출생/PEEC → 붕괴/PEC); 각 구역 내 세로축 = 현재 인구(위로 갈수록 많음). 위의 프로필/지역 필터와 무관하게 항상 28개국 전체를 표시합니다.",
        "it": "Griglia comparativa dei 28 paesi secondo l'N* (Sezione 9-A.7 della tesi, revisione del 12/07/2026). Asse orizzontale = zona dell'Indice Narayama (Saturazione/PEEC → Collasso/PEC); asse verticale, all'interno di ogni zona = popolazione attuale, maggiore in alto. Mostra sempre i 28 paesi, indipendentemente dai filtri di Profilo/Regione sopra.",
        "fi": "28 maan vertailuruudukko N*:n mukaan (väitöskirjan osa 9-A.7, tarkistettu 12.7.2026). Vaaka-akseli = Narayama-indeksin vyöhyke (ylisyntyvyys/PEEC → romahdus/PEC); pystyakseli kussakin vyöhykkeessä = nykyinen väestö, suurin ylhäällä. Näyttää aina kaikki 28 maata riippumatta yllä olevista profiili-/aluesuodattimista.",
        "fr": "Grille comparative des 28 pays selon le N* (Section 9-A.7 de la thèse, révision du 12/07/2026). Axe horizontal = zone de l'indice de Narayama (Surnatalité/PEEC → Effondrement/PEC) ; axe vertical, au sein de chaque zone = population actuelle, la plus grande en haut. Affiche toujours les 28 pays, indépendamment des filtres Profil/Région ci-dessus.",
        "zh": "按N*划分的28个国家比较网格（论文第9-A.7节，2026年7月12日修订）。横轴=楢山指数区域（过度生育/PEEC → 崩溃/PEC）；纵轴（各区域内）=当前人口，越靠上人口越多。无论上方的类型/地区筛选如何，始终显示全部28个国家。",
    },
    "farol_gap_caption": {
        "pt": "⚠️ **Lacuna registrada nos cards**: `farol (s/d)` — depende do Fator_Alocativo/NTA, sem fonte de dado real ainda (ver docs/definitions.md, seção 5).",
        "en": "⚠️ **Gap noted on the cards**: `farol (n/a)` — depends on Fator_Alocativo/NTA, no real data source yet (see docs/definitions.md, section 5).",
        "es": "⚠️ **Laguna registrada en las tarjetas**: `farol (s/d)` — depende del Fator_Alocativo/NTA, sin fuente de dato real todavía (ver docs/definitions.md, sección 5).",
        "ja": "⚠️ **カードに記録されたギャップ**：`farol (N/A)` — Fator_Alocativo/NTAに依存しており、実データの出典はまだありません（docs/definitions.md、セクション5参照）。",
        "ko": "⚠️ **카드에 표시된 공백**: `farol (N/A)` — Fator_Alocativo/NTA에 의존하며, 아직 실제 데이터 출처가 없습니다(docs/definitions.md 5절 참고).",
        "it": "⚠️ **Lacuna registrata nelle card**: `farol (n/d)` — dipende dal Fator_Alocativo/NTA, senza fonte di dati reali ancora (vedi docs/definitions.md, sezione 5).",
        "fi": "⚠️ **Kortteihin merkitty aukko**: `farol (N/A)` — riippuu Fator_Alocativosta/NTA:sta, ei vielä todellista tietolähdettä (katso docs/definitions.md, osa 5).",
        "fr": "⚠️ **Lacune signalée sur les cartes** : `farol (n/d)` — dépend du Fator_Alocativo/NTA, sans source de données réelles pour l'instant (voir docs/definitions.md, section 5).",
        "zh": "⚠️ **卡片中标注的空缺**：`farol (N/A)` — 依赖于Fator_Alocativo/NTA，目前尚无真实数据来源（见docs/definitions.md第5节）。",
    },
    "caption_arrow_ainu": {
        "pt": "**A seta compara dois cenários no mesmo ano (2074), não hoje vs. futuro**: P_tendência → P_eq. **P_tendência**: população em 2074 se a fecundidade real de cada país seguir sem mudança (dado real UN WPP 2024, variante \"Zero migration\"). **P_eq**: população em 2074 num cenário PROPOSTO em que o país converge linearmente até TFR=2,1 ao longo de 25 anos (2024-2049) e mantém essa taxa por mais 25 anos (2049-2074) — formalização do autor (2026-07-16), P_eq = P_E(t_c + 25), t_c = 2049, sempre com migração zerada. Comparar as duas no mesmo ano isola o efeito da recuperação de fecundidade da simples inércia etária (que sozinha já pode fazer a população crescer por décadas, mesmo sem mudança nenhuma — caso do Brasil). **Não é uma previsão nem um dado direto da ONU**: os nascimentos usados na simulação de P_eq são reais, só escalados pela razão entre a TFR proposta e a TFR real projetada pela ONU, ano a ano — óbitos ficam com o valor real. Simplificação documentada, não um modelo de coorte por idade — ver docs/definitions.md, seção 8-B.",
        "en": "**The arrow compares two scenarios in the same year (2074), not today vs. the future**: P_tendência → P_eq. **P_tendência**: population in 2074 if each country's real fertility continues unchanged (real UN WPP 2024 data, \"Zero migration\" variant). **P_eq**: population in 2074 under a PROPOSED scenario where the country converges linearly to TFR=2.1 over 25 years (2024-2049) and holds that rate for 25 more years (2049-2074) — the author's formalization (2026-07-16), P_eq = P_E(t_c + 25), t_c = 2049, always with zero migration. Comparing both in the same year isolates the effect of fertility recovery from plain age inertia (which alone can already make a population grow for decades, even with no change at all — Brazil's case). **This is not a forecast nor direct UN data**: the births used in the P_eq simulation are real, only scaled by the ratio between the proposed TFR and the UN's real projected TFR, year by year — deaths keep their real value. A documented simplification, not an age-cohort model — see docs/definitions.md, section 8-B.",
        "es": "**La flecha compara dos escenarios en el mismo año (2074), no hoy vs. futuro**: P_tendencia → P_eq. **P_tendencia**: población en 2074 si la fecundidad real de cada país continúa sin cambios (dato real UN WPP 2024, variante \"Zero migration\"). **P_eq**: población en 2074 bajo un escenario PROPUESTO en que el país converge linealmente hasta TFR=2,1 a lo largo de 25 años (2024-2049) y mantiene esa tasa por 25 años más (2049-2074) — formalización del autor (2026-07-16), P_eq = P_E(t_c + 25), t_c = 2049, siempre con migración cero. Comparar ambas en el mismo año aísla el efecto de la recuperación de fecundidad de la simple inercia etaria (que por sí sola ya puede hacer crecer la población por décadas, aun sin cambio alguno — caso de Brasil). **No es una previsión ni un dato directo de la ONU**: los nacimientos usados en la simulación de P_eq son reales, solo escalados por la razón entre la TFR propuesta y la TFR real proyectada por la ONU, año a año — las defunciones mantienen el valor real. Simplificación documentada, no un modelo de cohorte por edad — ver docs/definitions.md, sección 8-B.",
        "ja": "**この矢印は同じ年（2074年）の2つのシナリオを比較するもので、今日対未来ではありません**：P_tendência → P_eq。**P_tendência**：各国の実際の出生力が変わらず続いた場合の2074年の人口（実際のUN WPP 2024データ、「Zero migration」バリアント）。**P_eq**：その国が25年間（2024-2049年）でTFR=2.1に線形収束し、その後さらに25年間（2049-2074年）そのTFRを維持するという、提案されたシナリオでの2074年の人口 — 著者による定式化（2026年7月16日）、P_eq = P_E(t_c + 25)、t_c = 2049、常に移民ゼロ。同じ年で両者を比較することで、出生力回復の効果を単なる年齢構成の慣性（それだけでも何十年も人口を増加させうる — ブラジルの例）から切り離せます。**これは予測でも国連の直接データでもありません**：P_eqのシミュレーションに使われる出生数は実データで、提案TFRと国連の実際の予測TFRとの比率で年ごとに調整されているだけです — 死亡数は実際の値のままです。文書化された簡略化であり、年齢コーホートモデルではありません — docs/definitions.md、セクション8-B参照。",
        "ko": "**화살표는 오늘 대 미래가 아니라 같은 해(2074년)의 두 시나리오를 비교합니다**: P_tendência → P_eq. **P_tendência**: 각국의 실제 출산력이 변화 없이 지속될 경우 2074년의 인구(UN WPP 2024 실제 데이터, \"Zero migration\" 변형). **P_eq**: 해당 국가가 25년(2024-2049)에 걸쳐 TFR=2.1로 선형 수렴하고 이후 25년(2049-2074) 더 그 비율을 유지한다는 제안된 시나리오에서의 2074년 인구 — 저자의 공식화(2026-07-16), P_eq = P_E(t_c + 25), t_c = 2049, 항상 이주는 0으로 가정. 같은 해에 두 값을 비교하면 출산력 회복의 효과를 단순한 연령 관성(이것만으로도 아무 변화 없이 수십 년간 인구가 증가할 수 있음 — 브라질 사례)에서 분리할 수 있습니다. **이것은 예측도 유엔의 직접 데이터도 아닙니다**: P_eq 시뮬레이션에 사용된 출생아 수는 실제이며, 제안된 TFR과 유엔이 실제로 예측한 TFR의 비율로 매년 조정될 뿐입니다 — 사망자 수는 실제 값을 유지합니다. 문서화된 단순화이며 연령 코호트 모델이 아닙니다 — docs/definitions.md 8-B절 참고.",
        "it": "**La freccia confronta due scenari nello stesso anno (2074), non oggi vs. futuro**: P_tendencia → P_eq. **P_tendencia**: popolazione nel 2074 se la fecondità reale di ogni paese continuasse invariata (dato reale UN WPP 2024, variante \"Zero migration\"). **P_eq**: popolazione nel 2074 in uno scenario PROPOSTO in cui il paese converge linearmente a TFR=2,1 nell'arco di 25 anni (2024-2049) e mantiene quel tasso per altri 25 anni (2049-2074) — formalizzazione dell'autore (2026-07-16), P_eq = P_E(t_c + 25), t_c = 2049, sempre con migrazione zero. Confrontare i due nello stesso anno isola l'effetto del recupero della fecondità dalla semplice inerzia anagrafica (che da sola può già far crescere la popolazione per decenni, anche senza alcun cambiamento — caso del Brasile). **Non è una previsione né un dato diretto dell'ONU**: le nascite usate nella simulazione di P_eq sono reali, solo scalate dal rapporto tra la TFR proposta e la TFR reale proiettata dall'ONU, anno per anno — i decessi mantengono il valore reale. Semplificazione documentata, non un modello di coorte per età — vedi docs/definitions.md, sezione 8-B.",
        "fi": "**Nuoli vertaa kahta skenaariota samana vuonna (2074), ei tätä päivää tulevaisuuteen**: P_tendencia → P_eq. **P_tendencia**: väestö vuonna 2074, jos kunkin maan todellinen hedelmällisyys jatkuu muuttumattomana (todellinen UN WPP 2024 -data, \"Zero migration\" -variantti). **P_eq**: väestö vuonna 2074 EHDOTETUSSA skenaariossa, jossa maa lähestyy lineaarisesti TFR=2,1:tä 25 vuoden aikana (2024-2049) ja pitää sen tason vielä 25 vuotta (2049-2074) — tekijän formalisointi (2026-07-16), P_eq = P_E(t_c + 25), t_c = 2049, aina nollamuutolla. Kummankin vertaaminen samana vuonna erottaa hedelmällisyyden elpymisen vaikutuksen pelkästä ikärakenteen hitaudesta (joka yksinään voi jo kasvattaa väestöä vuosikymmeniä ilman mitään muutosta — Brasilian tapaus). **Tämä ei ole ennuste eikä suora YK-data**: P_eq-simulaatiossa käytetyt syntyvyysluvut ovat todellisia, vain skaalattu ehdotetun ja YK:n todella ennustaman TFR:n suhteella vuosittain — kuolleisuus säilyy todellisena. Dokumentoitu yksinkertaistus, ei ikäkohorttimalli — katso docs/definitions.md, osa 8-B.",
        "fr": "**La flèche compare deux scénarios la même année (2074), pas aujourd'hui contre le futur** : P_tendencia → P_eq. **P_tendencia** : population en 2074 si la fécondité réelle de chaque pays se poursuit sans changement (donnée réelle UN WPP 2024, variante \"Zero migration\"). **P_eq** : population en 2074 dans un scénario PROPOSÉ où le pays converge linéairement vers un TFR=2,1 sur 25 ans (2024-2049) puis maintient ce taux 25 années de plus (2049-2074) — formalisation de l'auteur (2026-07-16), P_eq = P_E(t_c + 25), t_c = 2049, toujours avec migration nulle. Comparer les deux la même année isole l'effet du redressement de la fécondité de la simple inertie d'âge (qui à elle seule peut déjà faire croître la population pendant des décennies, même sans aucun changement — cas du Brésil). **Ce n'est ni une prévision ni une donnée directe de l'ONU** : les naissances utilisées dans la simulation de P_eq sont réelles, seulement mises à l'échelle par le rapport entre le TFR proposé et le TFR réel projeté par l'ONU, année par année — les décès conservent leur valeur réelle. Simplification documentée, pas un modèle de cohorte par âge — voir docs/definitions.md, section 8-B.",
        "zh": "**箭头比较的是同一年（2074年）的两种情景，而非今天与未来的对比**：P_tendência → P_eq。**P_tendência**：如果各国实际生育率保持不变，2074年的人口（联合国UN WPP 2024真实数据，\"Zero migration\"情景）。**P_eq**：在一个提议情景下2074年的人口——该国在25年内（2024-2049年）线性收敛至TFR=2.1，并在此后25年（2049-2074年）保持该水平——作者的公式化表述（2026年7月16日），P_eq = P_E(t_c + 25)，t_c = 2049，始终假设零迁移。在同一年比较两者，可以将生育率恢复的效果与单纯的年龄结构惯性（仅凭这一点就可能让人口在几十年内持续增长，即使毫无变化——巴西即是如此）区分开。**这不是预测，也不是联合国的直接数据**：P_eq模拟中使用的出生人数是真实的，只是按提议TFR与联合国实际预测TFR的比率逐年调整——死亡人数保持真实值。这是一种有文档记录的简化，而非按年龄分组的队列模型——见docs/definitions.md第8-B节。",
    },
    "dados_insuficientes_tabela_geracional": {
        "pt": "Dados insuficientes para montar a tabela geracional.", "en": "Insufficient data to build the generational table.",
        "es": "Datos insuficientes para montar la tabla generacional.", "ja": "世代表を作成するにはデータが不十分です。",
        "ko": "세대 표를 만들기에 데이터가 부족합니다.", "it": "Dati insufficienti per costruire la tabella generazionale.",
        "fi": "Riittämättömät tiedot sukupolvitaulukon luomiseksi.", "fr": "Données insuffisantes pour construire le tableau générationnel.",
        "zh": "数据不足，无法生成世代表。",
    },
    "footer_ainu": {
        "pt": "**Dados**: UN World Population Prospects  \n**Metodologia**: Tese \"Do Dilema de Narayama ao Oicoceno Civilizacional\" v9.2  \n**Documentação**: [docs/definitions.md](../../docs/definitions.md)  \n**Versão pública**: [narayama.live](https://narayama.live)",
        "en": "**Data**: UN World Population Prospects  \n**Methodology**: Thesis \"From Narayama's Dilemma to the Civilizational Oikocene\" v9.2  \n**Documentation**: [docs/definitions.md](../../docs/definitions.md)  \n**Public version**: [narayama.live](https://narayama.live)",
        "es": "**Datos**: UN World Population Prospects  \n**Metodología**: Tesis \"Del Dilema de Narayama al Oicoceno Civilizacional\" v9.2  \n**Documentación**: [docs/definitions.md](../../docs/definitions.md)  \n**Versión pública**: [narayama.live](https://narayama.live)",
        "ja": "**データ**: UN World Population Prospects  \n**方法論**: 博士論文『ナラヤマのジレンマから文明的オイコセーンへ』v9.2  \n**ドキュメント**: [docs/definitions.md](../../docs/definitions.md)  \n**公開版**: [narayama.live](https://narayama.live)",
        "ko": "**데이터**: UN World Population Prospects  \n**방법론**: 논문 『나라야마의 딜레마에서 문명적 오이코세까지』 v9.2  \n**문서**: [docs/definitions.md](../../docs/definitions.md)  \n**공개 버전**: [narayama.live](https://narayama.live)",
        "it": "**Dati**: UN World Population Prospects  \n**Metodologia**: Tesi \"Dal Dilemma di Narayama all'Oicocene Civilizzazionale\" v9.2  \n**Documentazione**: [docs/definitions.md](../../docs/definitions.md)  \n**Versione pubblica**: [narayama.live](https://narayama.live)",
        "fi": "**Data**: UN World Population Prospects  \n**Menetelmä**: Väitöskirja \"Narayaman dilemmasta sivilisaation Oikoseeniin\" v9.2  \n**Dokumentaatio**: [docs/definitions.md](../../docs/definitions.md)  \n**Julkinen versio**: [narayama.live](https://narayama.live)",
        "fr": "**Données** : UN World Population Prospects  \n**Méthodologie** : Thèse \"Du Dilemme de Narayama à l'Oïcocène Civilisationnel\" v9.2  \n**Documentation** : [docs/definitions.md](../../docs/definitions.md)  \n**Version publique** : [narayama.live](https://narayama.live)",
        "zh": "**数据**：UN World Population Prospects  \n**方法论**：论文《从楢山难题到文明世的宜居纪》v9.2  \n**文档**：[docs/definitions.md](../../docs/definitions.md)  \n**公开版本**：[narayama.live](https://narayama.live)",
    },
}


def t(chave: str, lang: str, **fmt) -> str:
    """Busca o texto traduzido; cai em PT se faltar, nunca quebra."""
    entrada = T.get(chave)
    if not entrada:
        return chave
    texto = entrada.get(lang) or entrada.get(IDIOMA_PADRAO) or chave
    if fmt:
        try:
            return texto.format(**fmt)
        except (KeyError, IndexError):
            return texto
    return texto


def nome_pais(codigo: str, lang: str) -> str:
    entrada = NOMES_PAISES.get(codigo)
    if not entrada:
        return codigo
    return entrada.get(lang) or entrada.get(IDIOMA_PADRAO) or codigo


def nome_zona(zona_pt: str, lang: str) -> str:
    entrada = ZONAS.get(zona_pt)
    if not entrada:
        return zona_pt
    return entrada.get(lang) or entrada.get(IDIOMA_PADRAO) or zona_pt


def nome_regiao(regiao_pt: str, lang: str) -> str:
    entrada = REGIOES.get(regiao_pt)
    if not entrada:
        return regiao_pt
    return entrada.get(lang) or entrada.get(IDIOMA_PADRAO) or regiao_pt


def sufixo_milhoes(lang: str) -> str:
    return SUFIXO_MILHOES.get(lang, SUFIXO_MILHOES[IDIOMA_PADRAO])


def sem_dado(lang: str) -> str:
    return SEM_DADO.get(lang, SEM_DADO[IDIOMA_PADRAO])


def idioma_atual() -> str:
    lang = st.query_params.get("lang", IDIOMA_PADRAO)
    return lang if lang in IDIOMAS else IDIOMA_PADRAO


def seletor_idioma() -> str:
    """Barra superior com o seletor de idioma — PT é o padrão/fonte."""
    atual = idioma_atual()
    codigos = list(IDIOMAS.keys())
    _, coluna_seletor = st.columns([5, 2])
    with coluna_seletor:
        escolhido = st.selectbox(
            "🌐",
            codigos,
            index=codigos.index(atual),
            format_func=lambda c: IDIOMAS[c],
            label_visibility="collapsed",
            key="seletor_idioma_topo",
        )
    if escolhido != atual:
        st.query_params["lang"] = escolhido
        st.rerun()
    return escolhido
