"""
Traduções da página "Condição média em TFT de reposição" para es, fr, it, ko, ja, zh e fi.

Mesmas chaves de src/i18n_condicao.TX (que já traz pt e en). Mescladas lá.
Traduções feitas por IA (2026-11-10), sem revisão por falante nativo, a pedido do autor
(que as revisará depois). Termos próprios do projeto (Ascendentes, Estruturadores, Descendentes, TFR,
NTA, N*, AINU.Systems) ficam como no resto do site.
"""

_N = "N\\*"  # asterisco escapado para o markdown do Streamlit

# colunas e rótulos curtos que não mudam de idioma
_FIXAS = {
    "cm_col_n24": "N* 2024",
    "cm_col_ae24": "A/E 2024",
    "cm_col_e24": "E/80+ 2024",
}

_LANG: dict[str, dict[str, str]] = {
    "es": {
        "cm_titulo": "Condición media con fecundidad de reemplazo (exploratorio)",
        "cm_intro": (
            "Pregunta: cuando la TFR converge al reemplazo (2,1) y se mantiene allí, ¿la estructura por edades se estabiliza "
            "en lugar de seguir deteriorándose? La única palanca es la TFR; la mortalidad y la migración siguen la proyección "
            "media de la ONU (WPP 2024). La página compara la Tendencia de la ONU con una Meta en ciclos de 25 años "
            "(2024, 2049, 2074, 2099)."
        ),
        "cm_aviso": (
            f"**Exploratorio y condicional, no una previsión.** El {_N} depende de la TFR y de la estructura por edades; por eso "
            f"su llegada a la zona de equilibrio es una comprobación de coherencia del índice y **no** evidencia de sostenibilidad. "
            f"Las razones Ascendentes/Estruturadores y Estruturadores por persona de 80+ (cuidador potencial, no efectivo) son "
            f"las medidas que no derivan del {_N}. Costa Rica y Paraguay se añadieron el 2026-11-10 con un perfil único según el "
            f"tramo de TFR (CRI = C, PRY = B), aprobado por el autor."
        ),
        "cm_alvo": "TFR objetivo de la Meta",
        "cm_rampa": "Años hasta alcanzar el objetivo",
        "cm_calculando": "Proyectando los países…",
        "cm_tab_titulo": "1. Resumen por país",
        "cm_tab_nota": "A/E = Ascendentes ÷ Estruturadores (cortes de edad del país). E/80+ = Estruturadores por persona de 80 años o más.",
        "cm_col_pais": "País",
        "cm_col_n99t": "N* 2099 Tendencia",
        "cm_col_n99m": "N* 2099 Meta",
        "cm_col_zona": "Zona 2099 (Meta)",
        "cm_col_ae74": "A/E 2074 Meta",
        "cm_col_ae99m": "A/E 2099 Meta",
        "cm_col_ae99t": "A/E 2099 Tendencia",
        "cm_col_e99m": "E/80+ 2099 Meta",
        "cm_col_e99t": "E/80+ 2099 Tendencia",
        "cm_mediana": "Mediana (todos los países mostrados)",
        "cm_mediana_sn": "Mediana sin Nigeria",
        "cm_baixar": "Descargar la tabla completa (CSV)",
        "cm_graf_titulo": "2. Trayectorias",
        "cm_graf_paises": "Países en el gráfico",
        "cm_graf_ae": "Ascendentes ÷ Estruturadores",
        "cm_graf_n": f"{_N} (cada punto es un ciclo de 25 años)",
        "cm_tendencia": "Tendencia ONU",
        "cm_meta": "Meta",
        "cm_ano": "Año",
        "cm_ler_titulo": "Cómo leer",
        "cm_ler": (
            "- **Estabilizar no es restaurar.** Si A/E deja de subir tras dos ciclos pero sigue por encima de su valor de 2024, "
            "el reemplazo estabiliza la estructura en un nivel más envejecido; no vuelve al pasado.\n"
            "- **2,1 es una referencia de reemplazo.** Para los países por encima (por ejemplo Nigeria, Paraguay) la Meta es una "
            "reducción; la lectura es de convergencia al equilibrio desde ambos lados.\n"
            "- **E/80+ cae en los dos escenarios**, porque las personas mayores de 2099 ya nacieron; la Meta solo evita la caída más profunda.\n"
            "- Limitaciones: un único conjunto de supuestos (rampa y horizonte), migración y mortalidad de la ONU, sin NTA ni economía."
        ),
        "cm_fonte": "Fuente: UN World Population Prospects 2024 (variante media); motor `src/projecao.py`; hipótesis H8 del plan del Paper 3.",
        "cm_p3": "países del Paper 3",
        "cm_nota_idioma": "Traducción hecha con IA, sin revisión nativa; en caso de duda prevalece el texto en portugués.",
    },
    "fr": {
        "cm_titulo": "Condition moyenne à la fécondité de remplacement (exploratoire)",
        "cm_intro": (
            "Question : lorsque la TFR converge vers le remplacement (2,1) et s'y maintient, la structure par âge se stabilise-t-elle "
            "au lieu de continuer à se dégrader ? Le seul levier est la TFR ; la mortalité et la migration suivent la projection "
            "moyenne de l'ONU (WPP 2024). La page compare la Tendance de l'ONU à une Cible sur des cycles de 25 ans "
            "(2024, 2049, 2074, 2099)."
        ),
        "cm_aviso": (
            f"**Exploratoire et conditionnel, pas une prévision.** Le {_N} dépend de la TFR et de la structure par âge ; son arrivée "
            f"dans la zone d'équilibre est donc un contrôle de cohérence de l'indice et **non** une preuve de soutenabilité. Les "
            f"rapports Ascendentes/Estruturadores et Estruturadores par personne de 80 ans et plus (aidant potentiel, non effectif) "
            f"sont les mesures qui ne dérivent pas du {_N}. Le Costa Rica et le Paraguay ont été ajoutés le 2026-11-10 avec un profil "
            f"unique selon la tranche de TFR (CRI = C, PRY = B), approuvé par l'auteur."
        ),
        "cm_alvo": "TFR cible",
        "cm_rampa": "Années pour atteindre la cible",
        "cm_calculando": "Projection des pays…",
        "cm_tab_titulo": "1. Résumé par pays",
        "cm_tab_nota": "A/E = Ascendentes ÷ Estruturadores (seuils d'âge du pays). E/80+ = Estruturadores par personne de 80 ans ou plus.",
        "cm_col_pais": "Pays",
        "cm_col_n99t": "N* 2099 Tendance",
        "cm_col_n99m": "N* 2099 Cible",
        "cm_col_zona": "Zone 2099 (Cible)",
        "cm_col_ae74": "A/E 2074 Cible",
        "cm_col_ae99m": "A/E 2099 Cible",
        "cm_col_ae99t": "A/E 2099 Tendance",
        "cm_col_e99m": "E/80+ 2099 Cible",
        "cm_col_e99t": "E/80+ 2099 Tendance",
        "cm_mediana": "Médiane (tous les pays affichés)",
        "cm_mediana_sn": "Médiane hors Nigéria",
        "cm_baixar": "Télécharger le tableau complet (CSV)",
        "cm_graf_titulo": "2. Trajectoires",
        "cm_graf_paises": "Pays dans le graphique",
        "cm_graf_ae": "Ascendentes ÷ Estruturadores",
        "cm_graf_n": f"{_N} (chaque point est un cycle de 25 ans)",
        "cm_tendencia": "Tendance ONU",
        "cm_meta": "Cible",
        "cm_ano": "Année",
        "cm_ler_titulo": "Comment lire",
        "cm_ler": (
            "- **Stabiliser n'est pas restaurer.** Si A/E cesse de monter après deux cycles mais reste au-dessus de sa valeur de 2024, "
            "le remplacement stabilise la structure à un niveau plus âgé ; il ne revient pas au passé.\n"
            "- **2,1 est une référence de remplacement.** Pour les pays au-dessus (par exemple Nigéria, Paraguay), la Cible est une "
            "baisse ; la lecture est celle d'une convergence vers l'équilibre des deux côtés.\n"
            "- **E/80+ baisse dans les deux scénarios**, parce que les personnes âgées de 2099 sont déjà nées ; la Cible évite seulement la baisse la plus forte.\n"
            "- Limites : un seul jeu d'hypothèses (rampe et horizon), migration et mortalité de l'ONU, sans NTA ni économie."
        ),
        "cm_fonte": "Source : UN World Population Prospects 2024 (variante moyenne) ; moteur `src/projecao.py` ; hypothèse H8 du plan du Paper 3.",
        "cm_p3": "pays du Paper 3",
        "cm_nota_idioma": "Traduction faite par IA, sans relecture native ; en cas de doute, le texte portugais prévaut.",
    },
    "it": {
        "cm_titulo": "Condizione media alla fecondità di sostituzione (esplorativo)",
        "cm_intro": (
            "Domanda: quando la TFR converge alla sostituzione (2,1) e vi viene mantenuta, la struttura per età si stabilizza invece "
            "di continuare a deteriorarsi? L'unica leva è la TFR; mortalità e migrazione seguono la proiezione media dell'ONU "
            "(WPP 2024). La pagina confronta la Tendenza dell'ONU con un Obiettivo su cicli di 25 anni (2024, 2049, 2074, 2099)."
        ),
        "cm_aviso": (
            f"**Esplorativo e condizionale, non una previsione.** L'{_N} dipende dalla TFR e dalla struttura per età; perciò il suo "
            f"arrivo nella zona di equilibrio è un controllo di coerenza dell'indice e **non** una prova di sostenibilità. I rapporti "
            f"Ascendentes/Estruturadores e Estruturadores per persona di 80+ anni (caregiver potenziale, non effettivo) sono le misure "
            f"che non derivano dall'{_N}. Costa Rica e Paraguay sono stati aggiunti il 2026-11-10 con un profilo unico per fascia di "
            f"TFR (CRI = C, PRY = B), approvato dall'autore."
        ),
        "cm_alvo": "TFR obiettivo",
        "cm_rampa": "Anni per raggiungere l'obiettivo",
        "cm_calculando": "Proiezione dei paesi…",
        "cm_tab_titulo": "1. Riepilogo per paese",
        "cm_tab_nota": "A/E = Ascendentes ÷ Estruturadores (soglie di età del paese). E/80+ = Estruturadores per persona di 80 anni o più.",
        "cm_col_pais": "Paese",
        "cm_col_n99t": "N* 2099 Tendenza",
        "cm_col_n99m": "N* 2099 Obiettivo",
        "cm_col_zona": "Zona 2099 (Obiettivo)",
        "cm_col_ae74": "A/E 2074 Obiettivo",
        "cm_col_ae99m": "A/E 2099 Obiettivo",
        "cm_col_ae99t": "A/E 2099 Tendenza",
        "cm_col_e99m": "E/80+ 2099 Obiettivo",
        "cm_col_e99t": "E/80+ 2099 Tendenza",
        "cm_mediana": "Mediana (tutti i paesi mostrati)",
        "cm_mediana_sn": "Mediana senza la Nigeria",
        "cm_baixar": "Scarica la tabella completa (CSV)",
        "cm_graf_titulo": "2. Traiettorie",
        "cm_graf_paises": "Paesi nel grafico",
        "cm_graf_ae": "Ascendentes ÷ Estruturadores",
        "cm_graf_n": f"{_N} (ogni punto è un ciclo di 25 anni)",
        "cm_tendencia": "Tendenza ONU",
        "cm_meta": "Obiettivo",
        "cm_ano": "Anno",
        "cm_ler_titulo": "Come leggere",
        "cm_ler": (
            "- **Stabilizzare non è ripristinare.** Se A/E smette di salire dopo due cicli ma resta sopra il valore del 2024, la "
            "sostituzione stabilizza la struttura a un livello più anziano; non torna al passato.\n"
            "- **2,1 è un riferimento di sostituzione.** Per i paesi sopra tale valore (ad esempio Nigeria, Paraguay) l'Obiettivo è "
            "una riduzione; la lettura è di convergenza all'equilibrio da entrambi i lati.\n"
            "- **E/80+ scende in entrambi gli scenari**, perché gli anziani del 2099 sono già nati; l'Obiettivo evita soltanto il calo più profondo.\n"
            "- Limiti: un solo insieme di ipotesi (rampa e orizzonte), migrazione e mortalità dell'ONU, senza NTA né economia."
        ),
        "cm_fonte": "Fonte: UN World Population Prospects 2024 (variante media); motore `src/projecao.py`; ipotesi H8 del piano del Paper 3.",
        "cm_p3": "paesi del Paper 3",
        "cm_nota_idioma": "Traduzione fatta con IA, senza revisione madrelingua; in caso di dubbio prevale il testo portoghese.",
    },
    "fi": {
        "cm_titulo": "Keskimääräinen tila korvaavuustasoisella hedelmällisyydellä (tutkiva)",
        "cm_intro": (
            "Kysymys: kun TFR lähenee korvaavuustasoa (2,1) ja pysyy siinä, vakiintuuko ikärakenne sen sijaan, että se jatkaisi "
            "heikkenemistään? Ainoa vipu on TFR; kuolleisuus ja muuttoliike noudattavat YK:n keskimmäistä ennustetta (WPP 2024). "
            "Sivu vertaa YK:n Trendiä Tavoitteeseen 25 vuoden sykleissä (2024, 2049, 2074, 2099)."
        ),
        "cm_aviso": (
            f"**Tutkiva ja ehdollinen, ei ennuste.** {_N} riippuu TFR:stä ja ikärakenteesta, joten sen saapuminen tasapainovyöhykkeelle "
            f"on indeksin johdonmukaisuustarkistus eikä **todiste** kestävyydestä. Suhdeluvut Ascendentes/Estruturadores ja "
            f"Estruturadores yli 80-vuotiasta kohti (potentiaalinen, ei todellinen hoivaaja) ovat mittareita, jotka eivät johdu "
            f"{_N}:sta. Costa Rica ja Paraguay lisättiin 2026-11-10 yhdellä TFR-luokan mukaisella profiililla (CRI = C, PRY = B), "
            f"jonka tekijä on hyväksynyt."
        ),
        "cm_alvo": "Tavoitteen TFR",
        "cm_rampa": "Vuosia tavoitteeseen",
        "cm_calculando": "Projisoidaan maita…",
        "cm_tab_titulo": "1. Yhteenveto maittain",
        "cm_tab_nota": "A/E = Ascendentes ÷ Estruturadores (maan ikärajat). E/80+ = Estruturadores yli 80-vuotiasta kohti.",
        "cm_col_pais": "Maa",
        "cm_col_n99t": "N* 2099 Trendi",
        "cm_col_n99m": "N* 2099 Tavoite",
        "cm_col_zona": "Vyöhyke 2099 (Tavoite)",
        "cm_col_ae74": "A/E 2074 Tavoite",
        "cm_col_ae99m": "A/E 2099 Tavoite",
        "cm_col_ae99t": "A/E 2099 Trendi",
        "cm_col_e99m": "E/80+ 2099 Tavoite",
        "cm_col_e99t": "E/80+ 2099 Trendi",
        "cm_mediana": "Mediaani (kaikki näytetyt maat)",
        "cm_mediana_sn": "Mediaani ilman Nigeriaa",
        "cm_baixar": "Lataa koko taulukko (CSV)",
        "cm_graf_titulo": "2. Kehityskulut",
        "cm_graf_paises": "Kuvion maat",
        "cm_graf_ae": "Ascendentes ÷ Estruturadores",
        "cm_graf_n": f"{_N} (jokainen piste on 25 vuoden sykli)",
        "cm_tendencia": "YK:n Trendi",
        "cm_meta": "Tavoite",
        "cm_ano": "Vuosi",
        "cm_ler_titulo": "Miten lukea",
        "cm_ler": (
            "- **Vakauttaminen ei ole palauttamista.** Jos A/E lakkaa nousemasta kahden syklin jälkeen mutta pysyy vuoden 2024 arvon "
            "yläpuolella, korvaavuustaso vakauttaa rakenteen vanhemmalle tasolle; se ei palaa menneeseen.\n"
            "- **2,1 on korvaavuustason viitearvo.** Sen yläpuolella oleville maille (esim. Nigeria, Paraguay) Tavoite on lasku; "
            "tulkinta on lähentyminen tasapainoon molemmilta puolilta.\n"
            "- **E/80+ laskee molemmissa skenaarioissa**, koska vuoden 2099 vanhukset ovat jo syntyneet; Tavoite vain välttää syvimmän laskun.\n"
            "- Rajoitukset: yksi oletusjoukko (kasvu- ja aikahorisontti), YK:n muuttoliike ja kuolleisuus, ei NTA:ta eikä taloutta."
        ),
        "cm_fonte": "Lähde: UN World Population Prospects 2024 (keskimmäinen variantti); moottori `src/projecao.py`; Paper 3 -suunnitelman hypoteesi H8.",
        "cm_p3": "Paper 3:n maat",
        "cm_nota_idioma": "Käännös tehty tekoälyllä ilman äidinkielisen tarkistusta; epäselvissä tapauksissa portugalinkielinen teksti on ensisijainen.",
    },
    "ja": {
        "cm_titulo": "置換水準の出生率における平均的条件(探索的)",
        "cm_intro": (
            "問い:TFR が置換水準(2.1)に収れんしてそこで維持されたとき、年齢構造は悪化し続けずに安定するか。唯一の変数は TFR で、"
            "死亡率と移民は国連の中位推計(WPP 2024)に従います。このページでは、25年周期(2024、2049、2074、2099)で"
            "国連のトレンドと目標シナリオを比較します。"
        ),
        "cm_aviso": (
            f"**探索的かつ条件付きであり、予測ではありません。** {_N} は TFR と年齢構造に依存するため、均衡ゾーンへの到達は指数の"
            f"整合性チェックであって、持続可能性の**証拠ではありません**。Ascendentes/Estruturadores の比率と、80歳以上1人あたりの "
            f"Estruturadores(潜在的であり実際ではない介護者)が、{_N} から導かれない指標です。コスタリカとパラグアイは 2026-11-10 に、"
            f"TFR 帯ごとの単一プロファイル(CRI = C、PRY = B)で追加され、著者が承認しました。"
        ),
        "cm_alvo": "目標シナリオの TFR",
        "cm_rampa": "目標到達までの年数",
        "cm_calculando": "各国を推計中…",
        "cm_tab_titulo": "1. 国別の要約",
        "cm_tab_nota": "A/E = Ascendentes ÷ Estruturadores(各国の年齢区分)。E/80+ = 80歳以上1人あたりの Estruturadores。",
        "cm_col_pais": "国",
        "cm_col_n99t": "N* 2099 トレンド",
        "cm_col_n99m": "N* 2099 目標",
        "cm_col_zona": "2099年のゾーン(目標)",
        "cm_col_ae74": "A/E 2074 目標",
        "cm_col_ae99m": "A/E 2099 目標",
        "cm_col_ae99t": "A/E 2099 トレンド",
        "cm_col_e99m": "E/80+ 2099 目標",
        "cm_col_e99t": "E/80+ 2099 トレンド",
        "cm_mediana": "中央値(表示した全ての国)",
        "cm_mediana_sn": "中央値(ナイジェリアを除く)",
        "cm_baixar": "完全な表をダウンロード(CSV)",
        "cm_graf_titulo": "2. 推移",
        "cm_graf_paises": "グラフの対象国",
        "cm_graf_ae": "Ascendentes ÷ Estruturadores",
        "cm_graf_n": f"{_N}(各点は25年周期)",
        "cm_tendencia": "国連トレンド",
        "cm_meta": "目標",
        "cm_ano": "年",
        "cm_ler_titulo": "読み方",
        "cm_ler": (
            "- **安定化は回復ではありません。** 2サイクル後に A/E の上昇が止まっても 2024 年の値を上回っていれば、置換水準は構造を"
            "より高齢の水準で安定させるだけで、過去には戻りません。\n"
            "- **2.1 は置換水準の目安です。** これを上回る国(例:ナイジェリア、パラグアイ)では目標は引き下げであり、両側から"
            "均衡へ収れんするという読み方になります。\n"
            "- **E/80+ は両シナリオで低下します。** 2099年の高齢者はすでに生まれているためで、目標シナリオは最も深い低下を避けるにとどまります。\n"
            "- 限界:仮定は1組のみ(移行期間と期間)、移民と死亡率は国連の推計、NTA と経済は含みません。"
        ),
        "cm_fonte": "出典:UN World Population Prospects 2024(中位推計)、エンジン `src/projecao.py`、Paper 3 計画の仮説 H8。",
        "cm_p3": "Paper 3 の対象国",
        "cm_nota_idioma": "AI による翻訳であり、ネイティブによる校閲は受けていません。疑義がある場合はポルトガル語の本文が優先されます。",
    },
    "ko": {
        "cm_titulo": "대체 출산율에서의 평균 조건(탐색적)",
        "cm_intro": (
            "질문: TFR이 대체 수준(2.1)으로 수렴하여 그 수준을 유지하면, 연령 구조는 계속 악화되는 대신 안정되는가? 유일한 변수는 "
            "TFR이며, 사망률과 이민은 유엔 중위 추계(WPP 2024)를 따릅니다. 이 페이지는 25년 주기(2024, 2049, 2074, 2099)로 "
            "유엔 추세와 목표 시나리오를 비교합니다."
        ),
        "cm_aviso": (
            f"**탐색적이며 조건부이고, 예측이 아닙니다.** {_N}는 TFR과 연령 구조에 좌우되므로, 균형 구간에 도달하는 것은 지수의 "
            f"정합성 점검일 뿐 지속가능성의 **증거가 아닙니다**. Ascendentes/Estruturadores 비율과 80세 이상 1인당 Estruturadores"
            f"(잠재적이며 실제가 아닌 돌봄 인력)는 {_N}에서 파생되지 않는 지표입니다. 코스타리카와 파라과이는 2026-11-10에 "
            f"TFR 구간별 단일 프로파일(CRI = C, PRY = B)로 추가되었으며 저자가 승인했습니다."
        ),
        "cm_alvo": "목표 시나리오의 TFR",
        "cm_rampa": "목표 도달까지의 연수",
        "cm_calculando": "국가별 추계 중…",
        "cm_tab_titulo": "1. 국가별 요약",
        "cm_tab_nota": "A/E = Ascendentes ÷ Estruturadores(국가별 연령 기준). E/80+ = 80세 이상 1인당 Estruturadores.",
        "cm_col_pais": "국가",
        "cm_col_n99t": "N* 2099 추세",
        "cm_col_n99m": "N* 2099 목표",
        "cm_col_zona": "2099년 구간(목표)",
        "cm_col_ae74": "A/E 2074 목표",
        "cm_col_ae99m": "A/E 2099 목표",
        "cm_col_ae99t": "A/E 2099 추세",
        "cm_col_e99m": "E/80+ 2099 목표",
        "cm_col_e99t": "E/80+ 2099 추세",
        "cm_mediana": "중앙값(표시된 모든 국가)",
        "cm_mediana_sn": "중앙값(나이지리아 제외)",
        "cm_baixar": "전체 표 내려받기(CSV)",
        "cm_graf_titulo": "2. 추이",
        "cm_graf_paises": "그래프에 표시할 국가",
        "cm_graf_ae": "Ascendentes ÷ Estruturadores",
        "cm_graf_n": f"{_N}(각 점은 25년 주기)",
        "cm_tendencia": "유엔 추세",
        "cm_meta": "목표",
        "cm_ano": "연도",
        "cm_ler_titulo": "읽는 방법",
        "cm_ler": (
            "- **안정화는 회복이 아닙니다.** 두 주기 뒤 A/E 상승이 멈추더라도 2024년 값보다 높다면, 대체 수준은 구조를 더 고령화된 "
            "수준에서 안정시킬 뿐 과거로 되돌리지 않습니다.\n"
            "- **2.1은 대체 수준의 기준입니다.** 이보다 높은 국가(예: 나이지리아, 파라과이)에서는 목표가 감소를 뜻하며, 양쪽에서 "
            "균형으로 수렴한다고 읽습니다.\n"
            "- **E/80+는 두 시나리오 모두에서 하락합니다.** 2099년의 고령자는 이미 태어났기 때문이며, 목표 시나리오는 가장 큰 하락을 피하게 할 뿐입니다.\n"
            "- 한계: 가정은 한 묶음뿐(이행 기간과 기간), 이민과 사망률은 유엔 추계, NTA와 경제는 포함하지 않습니다."
        ),
        "cm_fonte": "출처: UN World Population Prospects 2024(중위 추계), 엔진 `src/projecao.py`, Paper 3 계획의 가설 H8.",
        "cm_p3": "Paper 3 대상 국가",
        "cm_nota_idioma": "AI로 번역했으며 원어민 검수를 받지 않았습니다. 의문이 있으면 포르투갈어 본문이 우선합니다.",
    },
    "zh": {
        "cm_titulo": "更替水平生育率下的平均状况(探索性)",
        "cm_intro": (
            "问题:当 TFR 收敛到更替水平(2.1)并保持在该水平时,年龄结构是否会趋于稳定,而不是继续恶化?唯一的变量是 TFR;"
            "死亡率和迁移遵循联合国中方案预测(WPP 2024)。本页以25年为一个周期(2024、2049、2074、2099)比较联合国趋势与目标情景。"
        ),
        "cm_aviso": (
            f"**探索性且有条件,不是预测。** {_N} 取决于 TFR 和年龄结构,因此它进入均衡区只是指数的一致性检验,**不是**可持续性的证据。"
            f"Ascendentes/Estruturadores 之比,以及每位80岁及以上老人对应的 Estruturadores 数(潜在而非实际的照护者),才是不由 {_N} "
            f"推导出的指标。哥斯达黎加和巴拉圭于 2026-11-10 按 TFR 区间采用单一档案(CRI = C,PRY = B)加入,已获作者批准。"
        ),
        "cm_alvo": "目标情景的 TFR",
        "cm_rampa": "达到目标所需年数",
        "cm_calculando": "正在推算各国……",
        "cm_tab_titulo": "1. 各国汇总",
        "cm_tab_nota": "A/E = Ascendentes ÷ Estruturadores(各国年龄划分)。E/80+ = 每位80岁及以上老人对应的 Estruturadores 数。",
        "cm_col_pais": "国家",
        "cm_col_n99t": "N* 2099 趋势",
        "cm_col_n99m": "N* 2099 目标",
        "cm_col_zona": "2099年区间(目标)",
        "cm_col_ae74": "A/E 2074 目标",
        "cm_col_ae99m": "A/E 2099 目标",
        "cm_col_ae99t": "A/E 2099 趋势",
        "cm_col_e99m": "E/80+ 2099 目标",
        "cm_col_e99t": "E/80+ 2099 趋势",
        "cm_mediana": "中位数(所有显示的国家)",
        "cm_mediana_sn": "中位数(不含尼日利亚)",
        "cm_baixar": "下载完整表格(CSV)",
        "cm_graf_titulo": "2. 变化轨迹",
        "cm_graf_paises": "图中的国家",
        "cm_graf_ae": "Ascendentes ÷ Estruturadores",
        "cm_graf_n": f"{_N}(每个点为一个25年周期)",
        "cm_tendencia": "联合国趋势",
        "cm_meta": "目标",
        "cm_ano": "年份",
        "cm_ler_titulo": "如何阅读",
        "cm_ler": (
            "- **稳定不等于恢复。** 如果 A/E 在两个周期后停止上升,但仍高于2024年的值,则更替水平只是把结构稳定在更老龄化的水平,并不会回到过去。\n"
            "- **2.1 是更替水平的参照值。** 对高于该值的国家(例如尼日利亚、巴拉圭),目标情景意味着下降;应理解为从两侧向均衡收敛。\n"
            "- **E/80+ 在两种情景下都会下降**,因为2099年的老年人已经出生;目标情景只是避免更深的下降。\n"
            "- 局限:只有一组假设(过渡期与期限),迁移和死亡率取自联合国,不含 NTA 和经济。"
        ),
        "cm_fonte": "来源:UN World Population Prospects 2024(中方案);引擎 `src/projecao.py`;Paper 3 计划中的假设 H8。",
        "cm_p3": "Paper 3 的国家",
        "cm_nota_idioma": "由 AI 翻译,未经母语者审校;如有疑问,以葡萄牙语文本为准。",
    },
}

# monta no formato {chave: {idioma: texto}} que src.i18n_condicao mescla em TX
TRAD: dict[str, dict[str, str]] = {}
for _lang, _d in _LANG.items():
    for _k, _v in {**_FIXAS, **_d}.items():
        TRAD.setdefault(_k, {})[_lang] = _v
