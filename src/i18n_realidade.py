"""
Textos da página "Consumo e Dividendo: a realidade dos países" e do título da página de simulação (ainu.systems, atrás do login).

PT e EN são o texto-fonte; es, fr, it, ko, ja, zh e fi foram traduzidos por IA (2026-11-02), sem revisão nativa, a pedido do autor,
que as revisará depois. Idioma ou chave ausente cai em PT. Termos próprios do projeto (Descendentes, Estruturadores, Dividendo
Intergeracional, SOCX, WDI) ficam como no resto do site.
"""

from src.i18n import IDIOMA_PADRAO, t

TX_REAL: dict[str, dict[str, str]] = {
    "r_titulo": {
        "pt": "Consumo e Dividendo: a realidade dos países", "en": "Consumption and Dividend: the reality of the countries",
        "es": "Consumo y Dividendo: la realidad de los países", "fr": "Consommation et Dividende : la réalité des pays",
        "it": "Consumo e Dividendo: la realtà dei paesi", "ko": "소비와 배당: 각국의 현실",
        "ja": "消費と配当:各国の実態", "zh": "消费与红利:各国的现实", "fi": "Kulutus ja osinko: maiden todellisuus",
    },
    "r_intro": {
        "pt": "Valores observados em fontes oficiais: quanto cada país consome e quanto já transfere às famílias com crianças. Nada aqui é estimativa, projeção ou simulação. Para as suposições (custo do Dividendo, crianças adicionais, cenários de fecundidade), use a página Simulacao Dividendo.",
        "en": "Values observed in official sources: how much each country consumes and how much it already transfers to families with children. Nothing here is an estimate, projection or simulation. For assumptions (Dividend cost, additional children, fertility scenarios), use the Simulacao Dividendo page.",
        "es": "Valores observados en fuentes oficiales: cuánto consume cada país y cuánto transfiere ya a las familias con hijos. Nada aquí es estimación, proyección ni simulación. Para las suposiciones (costo del Dividendo, niños adicionales, escenarios de fecundidad), use la página Simulacao Dividendo.",
        "fr": "Valeurs observées dans des sources officielles : combien chaque pays consomme et combien il transfère déjà aux familles avec enfants. Rien ici n'est une estimation, une projection ou une simulation. Pour les hypothèses (coût du Dividende, enfants supplémentaires, scénarios de fécondité), utilisez la page Simulacao Dividendo.",
        "it": "Valori osservati in fonti ufficiali: quanto consuma ogni paese e quanto trasferisce già alle famiglie con figli. Nulla qui è una stima, una proiezione o una simulazione. Per le ipotesi (costo del Dividendo, bambini aggiuntivi, scenari di fecondità), usare la pagina Simulacao Dividendo.",
        "ko": "공식 출처에서 관측한 값입니다. 각국이 얼마를 소비하고, 아동이 있는 가구에 이미 얼마를 이전하는지를 보여 줍니다. 여기에 추정, 전망, 시뮬레이션은 없습니다. 가정(배당 비용, 추가 아동, 출산율 시나리오)은 Simulacao Dividendo 페이지를 이용하세요.",
        "ja": "公式の出典で観測された値です。各国がどれだけ消費し、子どものいる世帯にすでにどれだけ移転しているかを示します。ここに推定・推計・シミュレーションはありません。仮定(配当の費用、追加の子ども、出生率シナリオ)は Simulacao Dividendo ページをご利用ください。",
        "zh": "官方来源中观测到的数值:各国消费多少,以及已经向有孩子的家庭转移多少。这里没有估计、预测或模拟。若需假设(红利成本、新增儿童、生育率情景),请使用 Simulacao Dividendo 页面。",
        "fi": "Virallisista lähteistä havaitut arvot: kuinka paljon kukin maa kuluttaa ja kuinka paljon se jo siirtää lapsiperheille. Mikään tässä ei ole arvio, ennuste tai simulaatio. Oletuksia (osingon kustannus, lisälapset, hedelmällisyysskenaariot) varten käytä sivua Simulacao Dividendo.",
    },
    "r_sem": {
        "pt": "Os dados do Diretório ainda não foram liberados neste ambiente (arquivo realidade.json ausente).",
        "en": "The Directory data has not been released in this environment (realidade.json is missing).",
        "es": "Los datos del Directorio aún no se han liberado en este entorno (falta el archivo realidade.json).",
        "fr": "Les données du Répertoire n'ont pas encore été publiées dans cet environnement (le fichier realidade.json est absent).",
        "it": "I dati del Repertorio non sono ancora stati rilasciati in questo ambiente (manca il file realidade.json).",
        "ko": "이 환경에서는 디렉터리 데이터가 아직 공개되지 않았습니다(realidade.json 파일 없음).",
        "ja": "この環境ではディレクトリのデータがまだ公開されていません(realidade.json がありません)。",
        "zh": "此环境中尚未发布名录数据(缺少 realidade.json 文件)。",
        "fi": "Hakemiston tietoja ei ole vielä julkaistu tässä ympäristössä (tiedosto realidade.json puuttuu).",
    },
    "r_comp": {
        "pt": "Comparação entre países", "en": "Comparison across countries", "es": "Comparación entre países", "fr": "Comparaison entre pays",
        "it": "Confronto tra paesi", "ko": "국가 간 비교", "ja": "国どうしの比較", "zh": "国家间比较", "fi": "Maiden vertailu",
    },
    "r_pais": {"pt": "País", "en": "Country", "es": "País", "fr": "Pays", "it": "Paese", "ko": "국가", "ja": "国", "zh": "国家", "fi": "Maa"},
    "r_cons": {
        "pt": "Consumo das famílias (% do PIB)", "en": "Household consumption (% of GDP)", "es": "Consumo de los hogares (% del PIB)",
        "fr": "Consommation des ménages (% du PIB)", "it": "Consumo delle famiglie (% del PIL)", "ko": "가계 소비(GDP 대비 %)",
        "ja": "家計消費(GDP比 %)", "zh": "居民消费(占 GDP 的 %)", "fi": "Kotitalouksien kulutus (% BKT:stä)",
    },
    "r_gov": {
        "pt": "Consumo do governo (% do PIB)", "en": "Government consumption (% of GDP)", "es": "Consumo del gobierno (% del PIB)",
        "fr": "Consommation des administrations (% du PIB)", "it": "Consumo delle amministrazioni pubbliche (% del PIL)", "ko": "정부 소비(GDP 대비 %)",
        "ja": "政府消費(GDP比 %)", "zh": "政府消费(占 GDP 的 %)", "fi": "Julkinen kulutus (% BKT:stä)",
    },
    "r_pc": {
        "pt": "Consumo das famílias por pessoa (US$ de 2015)", "en": "Household consumption per person (2015 US$)", "es": "Consumo de los hogares por persona (US$ de 2015)",
        "fr": "Consommation des ménages par personne (US$ de 2015)", "it": "Consumo delle famiglie per persona (US$ del 2015)", "ko": "1인당 가계 소비(2015년 US$)",
        "ja": "1人当たり家計消費(2015年米ドル)", "zh": "人均居民消费(2015 年美元)", "fi": "Kotitalouksien kulutus henkeä kohti (2015 US$)",
    },
    "r_fam": {
        "pt": "Gasto público em família (% do PIB)", "en": "Public spending on families (% of GDP)", "es": "Gasto público en familia (% del PIB)",
        "fr": "Dépenses publiques pour la famille (% du PIB)", "it": "Spesa pubblica per la famiglia (% del PIL)", "ko": "가족 관련 공공지출(GDP 대비 %)",
        "ja": "家族向け公的支出(GDP比 %)", "zh": "家庭公共支出(占 GDP 的 %)", "fi": "Perheisiin kohdistuvat julkiset menot (% BKT:stä)",
    },
    "r_prog": {
        "pt": "Maior programa infantil de renda (% do PIB)", "en": "Largest child cash programme (% of GDP)", "es": "Mayor programa infantil de renta (% del PIB)",
        "fr": "Plus grand programme de revenu pour enfants (% du PIB)", "it": "Maggiore programma di reddito per l'infanzia (% del PIL)", "ko": "최대 아동 소득 프로그램(GDP 대비 %)",
        "ja": "最大の児童向け現金給付(GDP比 %)", "zh": "最大的儿童现金项目(占 GDP 的 %)", "fi": "Suurin lapsille suunnattu tulonsiirto-ohjelma (% BKT:stä)",
    },
    "r_det": {
        "pt": "Transferências às famílias, país a país", "en": "Transfers to families, country by country", "es": "Transferencias a las familias, país por país",
        "fr": "Transferts aux familles, pays par pays", "it": "Trasferimenti alle famiglie, paese per paese", "ko": "국가별 가구 이전",
        "ja": "国別の家族への移転", "zh": "分国家的家庭转移", "fi": "Siirrot perheille maittain",
    },
    "r_nenhum": {
        "pt": "Nenhum instrumento de nível de fonte confirmado para este país.", "en": "No instrument with a confirmed source level for this country.",
        "es": "Ningún instrumento con nivel de fuente confirmado para este país.", "fr": "Aucun instrument dont le niveau de source soit confirmé pour ce pays.",
        "it": "Nessuno strumento con livello di fonte confermato per questo paese.", "ko": "이 국가에는 출처 수준이 확인된 제도가 없습니다.",
        "ja": "この国には出典水準が確認済みの制度はありません。", "zh": "该国没有来源等级已确认的制度。", "fi": "Tälle maalle ei ole instrumenttia, jonka lähdetaso on vahvistettu.",
    },
    "r_fontes": {
        "pt": "Fontes: consumo e PIB, Banco Mundial (WDI), valor mais recente de cada país (o ano aparece entre parênteses); gasto público em família, OCDE SOCX; programas, documentos oficiais de cada país, com link e conferência na página Dados Verificaveis. A Nigéria não tem níveis de consumo no WDI.",
        "en": "Sources: consumption and GDP, World Bank (WDI), latest value for each country (the year is in parentheses); public spending on families, OECD SOCX; programmes, each country's official documents, with links and checks on the Dados Verificaveis page. Nigeria has no consumption levels in the WDI.",
        "es": "Fuentes: consumo y PIB, Banco Mundial (WDI), valor más reciente de cada país (el año aparece entre paréntesis); gasto público en familia, OECD SOCX; programas, documentos oficiales de cada país, con enlace y comprobación en la página Dados Verificaveis. Nigeria no tiene niveles de consumo en el WDI.",
        "fr": "Sources : consommation et PIB, Banque mondiale (WDI), dernière valeur de chaque pays (l'année est entre parenthèses) ; dépenses publiques pour la famille, OECD SOCX ; programmes, documents officiels de chaque pays, avec lien et vérification sur la page Dados Verificaveis. Le Nigéria n'a pas de niveaux de consommation dans le WDI.",
        "it": "Fonti: consumo e PIL, Banca mondiale (WDI), valore più recente di ogni paese (l'anno è tra parentesi); spesa pubblica per la famiglia, OECD SOCX; programmi, documenti ufficiali di ciascun paese, con link e verifica nella pagina Dados Verificaveis. La Nigeria non ha livelli di consumo nel WDI.",
        "ko": "출처: 소비와 GDP는 세계은행(WDI)의 국가별 최신 값(연도는 괄호 안), 가족 관련 공공지출은 OECD SOCX, 프로그램은 각국의 공식 문서이며 링크와 점검은 Dados Verificaveis 페이지에 있습니다. 나이지리아는 WDI에 소비 수준 자료가 없습니다.",
        "ja": "出典:消費と GDP は世界銀行(WDI)の各国の最新値(年は括弧内)、家族向け公的支出は OECD SOCX、制度は各国の公式文書で、リンクと点検は Dados Verificaveis ページにあります。ナイジェリアは WDI に消費水準のデータがありません。",
        "zh": "来源:消费和 GDP 来自世界银行(WDI)各国最新数值(括号内为年份);家庭公共支出来自 OECD SOCX;项目来自各国官方文件,链接与核查见 Dados Verificaveis 页面。WDI 中没有尼日利亚的消费水平数据。",
        "fi": "Lähteet: kulutus ja BKT, Maailmanpankki (WDI), kunkin maan uusin arvo (vuosi suluissa); perheisiin kohdistuvat julkiset menot, OECD SOCX; ohjelmat, kunkin maan viralliset asiakirjat linkkeineen ja tarkistuksineen sivulla Dados Verificaveis. Nigerialle ei ole kulutustasoja WDI:ssä.",
    },
    "r_nota": {
        "pt": "O Dividendo Intergeracional é uma proposta do autor. Aqui aparece apenas o que os países já pagam às famílias com crianças.",
        "en": "The Intergenerational Dividend is the author's proposal. Only what countries already pay to families with children appears here.",
        "es": "El Dividendo Intergeneracional es una propuesta del autor. Aquí aparece solo lo que los países ya pagan a las familias con hijos.",
        "fr": "Le Dividende Intergénérationnel est une proposition de l'auteur. Ne figure ici que ce que les pays versent déjà aux familles avec enfants.",
        "it": "Il Dividendo Intergenerazionale è una proposta dell'autore. Qui compare solo ciò che i paesi già pagano alle famiglie con figli.",
        "ko": "세대 간 배당은 저자의 제안입니다. 여기에는 각국이 아동이 있는 가구에 이미 지급하는 것만 나옵니다.",
        "ja": "世代間配当は著者の提案です。ここには、各国が子どものいる世帯にすでに支払っているものだけが表示されます。",
        "zh": "代际红利是作者的提议。这里只显示各国已经向有孩子的家庭支付的内容。",
        "fi": "Sukupolvien välinen osinko on kirjoittajan ehdotus. Tässä näkyy vain se, mitä maat jo maksavat lapsiperheille.",
    },
    "r_nd": {"pt": "sem dado", "en": "no data", "es": "sin dato", "fr": "pas de donnée", "it": "nessun dato", "ko": "자료 없음", "ja": "データなし", "zh": "无数据", "fi": "ei tietoa"},
    "r_valor": {"pt": "Valor", "en": "Amount", "es": "Valor", "fr": "Montant", "it": "Importo", "ko": "금액", "ja": "金額", "zh": "金额", "fi": "Määrä"},
    "r_custo": {"pt": "Custo", "en": "Cost", "es": "Costo", "fr": "Coût", "it": "Costo", "ko": "비용", "ja": "費用", "zh": "成本", "fi": "Kustannus"},
    "r_texto_pt": {
        "pt": "", "en": "Descriptions of programmes are in the original Portuguese text.", "es": "Las descripciones de los programas están en el texto original en portugués.",
        "fr": "Les descriptions des programmes sont dans le texte original en portugais.", "it": "Le descrizioni dei programmi sono nel testo originale in portoghese.",
        "ko": "프로그램 설명은 포르투갈어 원문으로 되어 있습니다.", "ja": "制度の説明はポルトガル語の原文のままです。", "zh": "项目说明为葡萄牙语原文。", "fi": "Ohjelmien kuvaukset ovat alkuperäisellä portugalinkielisellä tekstillä.",
    },
    "t_sim": {
        "pt": "Simulação do Dividendo Intergeracional (beta)", "en": "Intergenerational Dividend simulation (beta)",
        "es": "Simulación del Dividendo Intergeneracional (beta)", "fr": "Simulation du Dividende Intergénérationnel (bêta)",
        "it": "Simulazione del Dividendo Intergenerazionale (beta)", "ko": "세대 간 배당 시뮬레이션 (베타)",
        "ja": "世代間配当のシミュレーション(ベータ版)", "zh": "代际红利模拟(测试版)", "fi": "Sukupolvien välisen osingon simulaatio (beta)",
    },
}


def tr(chave: str, lang: str, **fmt) -> str:
    entrada = TX_REAL.get(chave)
    if entrada is None:
        return t(chave, lang, **fmt)
    texto = entrada.get(lang) or entrada.get(IDIOMA_PADRAO) or chave
    if fmt:
        try:
            return texto.format(**fmt)
        except (KeyError, IndexError, ValueError):
            return texto
    return texto
