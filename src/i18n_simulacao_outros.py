"""
Traduções da página de simulação para es, fr, it, ko, ja, zh e fi.

Mesmas chaves de src/i18n_simulacao.TX_SIM (que já traz pt e en). Mesclado lá.
Traduções feitas por IA (2026-10-09), sem revisão por falante nativo: termos
técnicos (TFR, N*, PEA, Pop_Base/Pop_Topo) mantidos como no resto do projeto;
vale revisar antes de divulgar fora do beta.

Marcadores de formato ({alvo}, {ano}, {usuario}, {b}, {t}, {p}, {motivo},
{s}, {v1}...) devem permanecer idênticos em todos os idiomas.
"""

TRAD: dict[str, dict[str, str]] = {
    # --- login -------------------------------------------------------------
    "login_usuario": {"es": "Usuario", "fr": "Utilisateur", "it": "Utente", "ko": "사용자", "ja": "ユーザー", "zh": "用户", "fi": "Käyttäjä"},
    "login_entrar": {"es": "Entrar", "fr": "Se connecter", "it": "Accedi", "ko": "로그인", "ja": "ログイン", "zh": "登录", "fi": "Kirjaudu"},
    "login_invalido": {
        "es": "Usuario o contraseña incorrectos.", "fr": "Utilisateur ou mot de passe incorrect.",
        "it": "Utente o password errati.", "ko": "사용자 또는 비밀번호가 올바르지 않습니다.",
        "ja": "ユーザー名またはパスワードが正しくありません。", "zh": "用户名或密码错误。",
        "fi": "Väärä käyttäjätunnus tai salasana.",
    },
    "login_logado_como": {
        "es": "Sesión iniciada como {usuario}", "fr": "Connecté en tant que {usuario}",
        "it": "Connesso come {usuario}", "ko": "{usuario}(으)로 로그인됨",
        "ja": "{usuario} としてログイン中", "zh": "已登录：{usuario}", "fi": "Kirjautunut: {usuario}",
    },
    "login_sair": {"es": "Salir", "fr": "Se déconnecter", "it": "Esci", "ko": "로그아웃", "ja": "ログアウト", "zh": "退出", "fi": "Kirjaudu ulos"},
    # --- cabeçalho ----------------------------------------------------------
    "sim_titulo": {
        "es": "Simulación generacional (beta)", "fr": "Simulation générationnelle (bêta)",
        "it": "Simulazione generazionale (beta)", "ko": "세대 시뮬레이션 (베타)",
        "ja": "世代シミュレーション（ベータ）", "zh": "代际模拟（测试版）", "fi": "Sukupolvisimulaatio (beta)",
    },
    "sim_intro": {
        "es": (
            "Elija un país y una meta de fecundidad (TFR). El modelo proyecta la población por edad y sexo en "
            "**dos ciclos generacionales** (2024 → 2049 → 2074): la TFR converge linealmente a la meta en 25 años "
            "y se mantiene los 25 siguientes. **Solo cambia la TFR.** La mortalidad y la migración siguen la "
            "proyección media de la ONU (UN WPP 2024)."
        ),
        "fr": (
            "Choisissez un pays et un objectif de fécondité (TFR). Le modèle projette la population par âge et "
            "par sexe sur **deux cycles générationnels** (2024 → 2049 → 2074) : la TFR converge linéairement "
            "vers l'objectif en 25 ans puis se maintient pendant 25 ans. **Seule la TFR change.** La mortalité "
            "et la migration suivent la projection moyenne de l'ONU (UN WPP 2024)."
        ),
        "it": (
            "Scegli un paese e un obiettivo di fecondità (TFR). Il modello proietta la popolazione per età e "
            "sesso su **due cicli generazionali** (2024 → 2049 → 2074): la TFR converge linearmente verso "
            "l'obiettivo in 25 anni e si mantiene per i 25 successivi. **Cambia solo la TFR.** Mortalità e "
            "migrazione seguono la proiezione media dell'ONU (UN WPP 2024)."
        ),
        "ko": (
            "국가와 출산율(TFR) 목표를 선택하세요. 모델은 연령·성별 인구를 **두 세대 주기**(2024 → 2049 → 2074)에 "
            "걸쳐 추정합니다. TFR은 25년 동안 목표치로 선형 수렴한 뒤 이후 25년간 유지됩니다. **바뀌는 것은 TFR뿐입니다.** "
            "사망률과 이주는 UN WPP 2024 중위 추계를 따릅니다."
        ),
        "ja": (
            "国と出生率（TFR）の目標を選んでください。モデルは年齢・性別の人口を**2つの世代サイクル**（2024 → 2049 → 2074）"
            "にわたって推計します。TFRは25年かけて目標値へ直線的に収束し、その後の25年は維持されます。**変わるのはTFRだけです。**"
            "死亡率と移民は国連WPP 2024の中位推計に従います。"
        ),
        "zh": (
            "选择国家和生育率（TFR）目标。模型按年龄和性别推算**两个世代周期**（2024 → 2049 → 2074）的人口："
            "TFR在25年内线性收敛到目标，并在随后的25年保持不变。**只有TFR发生变化。**死亡率和迁移遵循联合国WPP 2024中方案。"
        ),
        "fi": (
            "Valitse maa ja hedelmällisyyden (TFR) tavoite. Malli ennustaa väestön iän ja sukupuolen mukaan "
            "**kahden sukupolvisyklin** ajan (2024 → 2049 → 2074): TFR lähestyy tavoitetta lineaarisesti 25 "
            "vuodessa ja pysyy siinä seuraavat 25 vuotta. **Vain TFR muuttuu.** Kuolleisuus ja muutto seuraavat "
            "YK:n WPP 2024 -keskiennustetta."
        ),
    },
    "sim_aviso": {
        "es": "**Escenario, no pronóstico.** El resultado muestra lo que ocurriría *si* la TFR siguiera la trayectoria elegida, con todo lo demás en la tendencia de la ONU. Versión beta: sujeta a cambios.",
        "fr": "**Scénario, pas prévision.** Le résultat montre ce qui se passerait *si* la TFR suivait la trajectoire choisie, tout le reste suivant la tendance de l'ONU. Version bêta : susceptible d'évoluer.",
        "it": "**Scenario, non previsione.** Il risultato mostra cosa accadrebbe *se* la TFR seguisse la traiettoria scelta, con tutto il resto sulla tendenza ONU. Versione beta: soggetta a modifiche.",
        "ko": "**시나리오이며 예측이 아닙니다.** 선택한 경로로 TFR이 움직이고 나머지는 UN 추세를 따른다면 *어떻게 되는지*를 보여 줍니다. 베타 버전으로 변경될 수 있습니다.",
        "ja": "**予測ではなくシナリオです。** 選んだ経路でTFRが推移し、他はすべて国連のトレンドに従う場合に*何が起こるか*を示します。ベータ版のため変更されることがあります。",
        "zh": "**这是情景，不是预测。**结果显示：*如果*TFR沿所选路径变化，其余一切保持联合国趋势，会发生什么。测试版，可能调整。",
        "fi": "**Skenaario, ei ennuste.** Tulos näyttää, mitä tapahtuisi, *jos* TFR kulkisi valittua polkua ja kaikki muu seuraisi YK:n trendiä. Beta-versio: voi muuttua.",
    },
    # --- controles ------------------------------------------------------------
    "sim_pais": {"es": "País", "fr": "Pays", "it": "Paese", "ko": "국가", "ja": "国", "zh": "国家", "fi": "Maa"},
    "sim_tfr_alvo": {
        "es": "TFR objetivo (hijos por mujer)", "fr": "TFR cible (enfants par femme)",
        "it": "TFR obiettivo (figli per donna)", "ko": "목표 TFR (여성 1인당 자녀 수)",
        "ja": "目標TFR（女性1人あたりの子ども数）", "zh": "目标TFR（每名女性生育子女数）", "fi": "Tavoite-TFR (lasta naista kohti)",
    },
    "sim_tfr_atual": {
        "es": "TFR actual (2024, ONU)", "fr": "TFR actuel (2024, ONU)", "it": "TFR attuale (2024, ONU)",
        "ko": "현재 TFR (2024, UN)", "ja": "現在のTFR（2024年、国連）", "zh": "当前TFR（2024年，联合国）", "fi": "Nykyinen TFR (2024, YK)",
    },
    "sim_avancado": {
        "es": "Ajuste manual: mezcla de perfiles del país", "fr": "Ajustement manuel : mélange de profils du pays",
        "it": "Regolazione manuale: mix di profili del paese", "ko": "수동 조정: 국가의 프로필 구성",
        "ja": "手動調整：国のプロファイル構成", "zh": "手动调整：国家的类型构成", "fi": "Manuaalinen säätö: maan profiiliyhdistelmä",
    },
    "sim_avancado_ajuda": {
        "es": "Los cortes de edad de Pop_Base/Pop_Topo provienen de una mezcla de **hasta 3 perfiles** (A–E, Tabla 14). Aquí puede probar otra mezcla; los pesos deben sumar 1. El valor por defecto proviene de `COMPOSICAO_PERFIL_POR_PAIS` en `src/config.py`.",
        "fr": "Les seuils d'âge de Pop_Base/Pop_Topo proviennent d'un mélange de **3 profils au plus** (A–E, Tableau 14). Vous pouvez tester ici un autre mélange ; les poids doivent totaliser 1. La valeur par défaut vient de `COMPOSICAO_PERFIL_POR_PAIS` dans `src/config.py`.",
        "it": "I limiti d'età di Pop_Base/Pop_Topo derivano da un mix di **al massimo 3 profili** (A–E, Tabella 14). Qui puoi provare un altro mix; i pesi devono sommare 1. Il valore predefinito proviene da `COMPOSICAO_PERFIL_POR_PAIS` in `src/config.py`.",
        "ko": "Pop_Base/Pop_Topo의 연령 구분은 **최대 3개 프로필**(A–E, 표 14)의 구성에서 나옵니다. 여기서 다른 구성을 시험해 볼 수 있으며 가중치의 합은 1이어야 합니다. 기본값은 `src/config.py`의 `COMPOSICAO_PERFIL_POR_PAIS`입니다.",
        "ja": "Pop_Base/Pop_Topoの年齢区分は**最大3つのプロファイル**（A–E、表14）の構成から決まります。ここで別の構成を試せます。重みの合計は1にしてください。既定値は `src/config.py` の `COMPOSICAO_PERFIL_POR_PAIS` です。",
        "zh": "Pop_Base/Pop_Topo的年龄分界来自**最多3个类型**（A–E，表14）的构成。您可以在此尝试其他构成；权重之和必须为1。默认值来自 `src/config.py` 中的 `COMPOSICAO_PERFIL_POR_PAIS`。",
        "fi": "Pop_Base/Pop_Topo-ikärajat tulevat **enintään 3 profiilin** yhdistelmästä (A–E, taulukko 14). Voit kokeilla tässä toista yhdistelmää; painojen summan on oltava 1. Oletus tulee `src/config.py`-tiedoston kohdasta `COMPOSICAO_PERFIL_POR_PAIS`.",
    },
    "sim_peso": {
        "es": "Peso del perfil {p}", "fr": "Poids du profil {p}", "it": "Peso del profilo {p}",
        "ko": "프로필 {p} 가중치", "ja": "プロファイル{p}の重み", "zh": "类型{p}权重", "fi": "Profiilin {p} paino",
    },
    "sim_comp_invalida": {
        "es": "Mezcla no válida ({motivo}); se usa la mezcla por defecto del país.",
        "fr": "Mélange invalide ({motivo}) ; utilisation du mélange par défaut du pays.",
        "it": "Mix non valido ({motivo}); si usa il mix predefinito del paese.",
        "ko": "구성이 올바르지 않습니다({motivo}). 국가 기본 구성을 사용합니다.",
        "ja": "構成が無効です（{motivo}）。国の既定の構成を使用します。",
        "zh": "构成无效（{motivo}）；使用该国默认构成。",
        "fi": "Virheellinen yhdistelmä ({motivo}); käytetään maan oletusyhdistelmää.",
    },
    "sim_comp_soma": {
        "es": "los pesos suman {s:.2f}, no 1", "fr": "les poids totalisent {s:.2f}, pas 1",
        "it": "i pesi sommano {s:.2f}, non 1", "ko": "가중치 합이 1이 아니라 {s:.2f}입니다",
        "ja": "重みの合計が1ではなく{s:.2f}です", "zh": "权重之和为{s:.2f}，不是1", "fi": "painojen summa on {s:.2f}, ei 1",
    },
    "sim_comp_max3": {
        "es": "más de 3 perfiles con peso", "fr": "plus de 3 profils pondérés", "it": "più di 3 profili con peso",
        "ko": "가중치가 있는 프로필이 3개를 초과합니다", "ja": "重みのあるプロファイルが3つを超えています",
        "zh": "有权重的类型超过3个", "fi": "yli 3 profiilia painotettu",
    },
    "sim_cortes": {
        "es": "Cortes resultantes: Pop_Base = edades 0–{b}; Pop_Topo = edades {t}+.",
        "fr": "Seuils obtenus : Pop_Base = âges 0–{b} ; Pop_Topo = âges {t}+.",
        "it": "Limiti risultanti: Pop_Base = età 0–{b}; Pop_Topo = età {t}+.",
        "ko": "결과 구분: Pop_Base = {b}세까지(0–{b}), Pop_Topo = {t}세 이상.",
        "ja": "結果の区分：Pop_Base = 0–{b}歳、Pop_Topo = {t}歳以上。",
        "zh": "所得分界：Pop_Base = 0–{b}岁；Pop_Topo = {t}岁及以上。",
        "fi": "Tuloksena rajat: Pop_Base = iät 0–{b}; Pop_Topo = iät {t}+.",
    },
    # --- resultados -------------------------------------------------------------
    "sim_resumo": {"es": "Resumen", "fr": "Résumé", "it": "Riepilogo", "ko": "요약", "ja": "概要", "zh": "摘要", "fi": "Yhteenveto"},
    "sim_pop_titulo": {
        "es": "Población total (millones)", "fr": "Population totale (millions)", "it": "Popolazione totale (milioni)",
        "ko": "총인구 (백만 명)", "ja": "総人口（百万人）", "zh": "总人口（百万）", "fi": "Kokonaisväestö (miljoonaa)",
    },
    "sim_n_titulo": {
        "es": "N\\* a lo largo del tiempo", "fr": "N\\* au fil du temps", "it": "N\\* nel tempo",
        "ko": "N\\* 추이", "ja": "N\\* の推移", "zh": "N\\* 随时间变化", "fi": "N\\* ajan myötä",
    },
    "sim_cenario": {
        "es": "Escenario (TFR → {alvo:.2f})", "fr": "Scénario (TFR → {alvo:.2f})", "it": "Scenario (TFR → {alvo:.2f})",
        "ko": "시나리오 (TFR → {alvo:.2f})", "ja": "シナリオ（TFR → {alvo:.2f}）", "zh": "情景（TFR → {alvo:.2f}）",
        "fi": "Skenaario (TFR → {alvo:.2f})",
    },
    "sim_base": {
        "es": "Tendencia de la ONU", "fr": "Tendance de l'ONU", "it": "Tendenza ONU",
        "ko": "UN 추세", "ja": "国連トレンド", "zh": "联合国趋势", "fi": "YK:n trendi",
    },
    "sim_ano": {"es": "Año", "fr": "Année", "it": "Anno", "ko": "연도", "ja": "年", "zh": "年份", "fi": "Vuosi"},
    "sim_pop": {"es": "Población", "fr": "Population", "it": "Popolazione", "ko": "인구", "ja": "人口", "zh": "人口", "fi": "Väestö"},
    "sim_pop_ano": {
        "es": "Población en {ano} (millones)", "fr": "Population en {ano} (millions)", "it": "Popolazione nel {ano} (milioni)",
        "ko": "{ano}년 인구 (백만 명)", "ja": "{ano}年の人口（百万人）", "zh": "{ano}年人口（百万）", "fi": "Väestö vuonna {ano} (miljoonaa)",
    },
    "sim_n_ano": {
        "es": "N* en {ano}", "fr": "N* en {ano}", "it": "N* nel {ano}", "ko": "{ano}년 N*",
        "ja": "{ano}年のN*", "zh": "{ano}年N*", "fi": "N* vuonna {ano}",
    },
    "sim_zona_ano": {
        "es": "Zona en {ano}", "fr": "Zone en {ano}", "it": "Zona nel {ano}", "ko": "{ano}년 구역",
        "ja": "{ano}年のゾーン", "zh": "{ano}年区域", "fi": "Vyöhyke vuonna {ano}",
    },
    "sim_virada_titulo": {
        "es": "Puntos de inflexión", "fr": "Points de bascule", "it": "Punti di svolta",
        "ko": "전환점", "ja": "転換点", "zh": "拐点", "fi": "Käännekohdat",
    },
    "sim_virada_nota": {
        "es": "Tres lecturas de \"punto de inflexión\", todas calculadas dentro del horizonte (hasta 2074).",
        "fr": "Trois lectures du « point de bascule », toutes calculées dans l'horizon (jusqu'en 2074).",
        "it": "Tre letture di \"punto di svolta\", tutte calcolate entro l'orizzonte (fino al 2074).",
        "ko": "\"전환점\"의 세 가지 해석이며, 모두 전망 기간(2074년까지) 안에서 계산됩니다.",
        "ja": "「転換点」の3つの読み方で、いずれも期間内（2074年まで）で計算します。",
        "zh": "“拐点”的三种解读，均在预测期内（至2074年）计算。",
        "fi": "Kolme tulkintaa \"käännekohdasta\", kaikki laskettu aikajänteen sisällä (vuoteen 2074).",
    },
    "sim_v_saldo": {
        "es": "Los nacimientos pasan a superar a las muertes", "fr": "Les naissances dépassent les décès",
        "it": "Le nascite superano i decessi", "ko": "출생이 사망을 넘어섬",
        "ja": "出生数が死亡数を上回る", "zh": "出生数开始超过死亡数", "fi": "Syntyneet ylittävät kuolleet",
    },
    "sim_v_pico": {
        "es": "Pico de la población (luego cae)", "fr": "Pic de population (puis baisse)",
        "it": "Picco della popolazione (poi cala)", "ko": "인구 정점 (이후 감소)",
        "ja": "人口のピーク（その後減少）", "zh": "人口峰值（此后下降）", "fi": "Väestön huippu (sen jälkeen laskee)",
    },
    "sim_v_fim_queda": {
        "es": "Fin de la caída (la población vuelve a crecer)", "fr": "Fin du déclin (la population recroît)",
        "it": "Fine del calo (la popolazione torna a crescere)", "ko": "감소 종료 (인구가 다시 증가)",
        "ja": "減少の終わり（人口が再び増加）", "zh": "下降结束（人口重新增长）", "fi": "Laskun loppu (väestö kasvaa taas)",
    },
    "sim_v_n": {
        "es": "N* alcanza 0,90 (entra en el PEA)", "fr": "N* atteint 0,90 (entre dans le PEA)",
        "it": "N* raggiunge 0,90 (entra nel PEA)", "ko": "N*가 0.90에 도달 (PEA 진입)",
        "ja": "N*が0.90に到達（PEAに入る）", "zh": "N*达到0.90（进入PEA）", "fi": "N* saavuttaa 0,90 (siirtyy PEA:han)",
    },
    "sim_v_sempre_pos": {
        "es": "ya era positivo", "fr": "déjà positif", "it": "già positivo", "ko": "이미 양(+)임",
        "ja": "すでにプラス", "zh": "本来就为正", "fi": "jo positiivinen",
    },
    "sim_v_sempre_neg": {
        "es": "permanece negativo", "fr": "reste négatif", "it": "resta negativo", "ko": "계속 음(−)임",
        "ja": "マイナスのまま", "zh": "始终为负", "fi": "pysyy negatiivisena",
    },
    "sim_v_nao": {
        "es": "no ocurre hasta 2074", "fr": "n'a pas lieu avant 2074", "it": "non avviene entro il 2074",
        "ko": "2074년까지 발생하지 않음", "ja": "2074年までに起こらない", "zh": "至2074年不会发生", "fi": "ei tapahdu vuoteen 2074 mennessä",
    },
    "sim_v_cresce": {
        "es": "crece todo el tiempo", "fr": "croît en permanence", "it": "cresce per tutto il periodo",
        "ko": "내내 증가", "ja": "一貫して増加", "zh": "持续增长", "fi": "kasvaa koko ajan",
    },
    "sim_v_cai": {
        "es": "cae todo el tiempo", "fr": "décroît en permanence", "it": "cala per tutto il periodo",
        "ko": "내내 감소", "ja": "一貫して減少", "zh": "持续下降", "fi": "laskee koko ajan",
    },
    "sim_v_n_ja": {
        "es": "ya ≥ 0,90 en 2024 y se mantiene", "fr": "déjà ≥ 0,90 en 2024 et s'y maintient",
        "it": "già ≥ 0,90 nel 2024 e vi rimane", "ko": "2024년에 이미 ≥ 0.90이며 유지됨",
        "ja": "2024年にすでに0.90以上で維持", "zh": "2024年已≥0.90并保持", "fi": "jo ≥ 0,90 vuonna 2024 ja pysyy",
    },
    "sim_v_n_ja_cai": {
        "es": "ya ≥ 0,90 en 2024; por debajo desde {ano}", "fr": "déjà ≥ 0,90 en 2024 ; en dessous à partir de {ano}",
        "it": "già ≥ 0,90 nel 2024; sotto dal {ano}", "ko": "2024년에 이미 ≥ 0.90; {ano}년부터 하회",
        "ja": "2024年にすでに0.90以上；{ano}年から下回る", "zh": "2024年已≥0.90；自{ano}年起低于0.90",
        "fi": "jo ≥ 0,90 vuonna 2024; alle vuodesta {ano}",
    },
    "sim_v_n_nunca": {
        "es": "no alcanza 0,90 hasta 2074", "fr": "n'atteint pas 0,90 avant 2074", "it": "non raggiunge 0,90 entro il 2074",
        "ko": "2074년까지 0.90에 도달하지 못함", "ja": "2074年までに0.90に達しない", "zh": "至2074年未达到0.90", "fi": "ei saavuta 0,90:ää vuoteen 2074 mennessä",
    },
    "sim_v_pos_depois_neg": {
        "es": "ya positivo; negativo desde {ano}", "fr": "déjà positif ; négatif à partir de {ano}",
        "it": "già positivo; negativo dal {ano}", "ko": "이미 양(+); {ano}년부터 음(−)",
        "ja": "すでにプラス；{ano}年からマイナス", "zh": "本来为正；自{ano}年起为负", "fi": "jo positiivinen; negatiivinen vuodesta {ano}",
    },
    "sim_col_item": {"es": "Lectura", "fr": "Lecture", "it": "Lettura", "ko": "항목", "ja": "項目", "zh": "解读", "fi": "Tulkinta"},
    "sim_nasc_obitos": {
        "es": "Nacimientos y muertes por año (millones)", "fr": "Naissances et décès par an (millions)",
        "it": "Nascite e decessi all'anno (milioni)", "ko": "연간 출생·사망 (백만 명)",
        "ja": "年間の出生数と死亡数（百万人）", "zh": "年出生与死亡人数（百万）", "fi": "Syntyneet ja kuolleet vuodessa (miljoonaa)",
    },
    "sim_nascimentos": {"es": "Nacimientos", "fr": "Naissances", "it": "Nascite", "ko": "출생", "ja": "出生", "zh": "出生", "fi": "Syntyneet"},
    "sim_obitos": {"es": "Muertes", "fr": "Décès", "it": "Decessi", "ko": "사망", "ja": "死亡", "zh": "死亡", "fi": "Kuolleet"},
    "sim_piramide_titulo": {
        "es": "Población por edad", "fr": "Population par âge", "it": "Popolazione per età",
        "ko": "연령별 인구", "ja": "年齢別人口", "zh": "按年龄划分的人口", "fi": "Väestö iän mukaan",
    },
    "sim_piramide_ano": {
        "es": "Año de la estructura por edad", "fr": "Année de la structure par âge", "it": "Anno della struttura per età",
        "ko": "연령 구조 연도", "ja": "年齢構成の年", "zh": "年龄结构年份", "fi": "Ikärakenteen vuosi",
    },
    "sim_idade": {"es": "Edad", "fr": "Âge", "it": "Età", "ko": "연령", "ja": "年齢", "zh": "年龄", "fi": "Ikä"},
    "sim_milhares": {
        "es": "Miles de personas", "fr": "Milliers de personnes", "it": "Migliaia di persone",
        "ko": "천 명", "ja": "千人", "zh": "千人", "fi": "Tuhatta henkeä",
    },
    "sim_base_topo": {
        "es": "Rangos Pop_Base y Pop_Topo", "fr": "Tranches Pop_Base et Pop_Topo", "it": "Fasce Pop_Base e Pop_Topo",
        "ko": "Pop_Base 및 Pop_Topo 범위", "ja": "Pop_BaseとPop_Topoの範囲", "zh": "Pop_Base与Pop_Topo范围", "fi": "Pop_Base- ja Pop_Topo-alueet",
    },
    # --- método ------------------------------------------------------------------
    "sim_metodo_titulo": {
        "es": "Cómo funciona el modelo y qué NO hace", "fr": "Comment fonctionne le modèle et ce qu'il ne fait PAS",
        "it": "Come funziona il modello e cosa NON fa", "ko": "모델의 작동 방식과 하지 않는 것",
        "ja": "モデルの仕組みと、しないこと", "zh": "模型如何运作及其不做什么", "fi": "Miten malli toimii ja mitä se EI tee",
    },
    "sim_metodo": {
        "es": (
            "**Método.** Proyección por componentes de cohorte (edad simple × sexo), paso anual. La supervivencia y "
            "la migración neta siguen la proyección media de la ONU (la migración es el residuo que reproduce la "
            "proyección de la ONU, en números absolutos por edad). Los nacimientos usan la fecundidad por edad de "
            "la ONU, escalada a la TFR del escenario y calibrada al total oficial. N\\* usa la misma cadena del "
            "proyecto (NGII → NGII_puro → N_Base → N\\* = √N_Base), con los cortes de edad de la mezcla de perfiles.\n\n"
            "**Validación** (`docs/validacao_projecao.md`): el N\\* de 2024 recalculado por el motor difiere del "
            "índice de producción en como máximo {v3}; la calibración de nacimientos queda dentro de {v1} del total "
            "oficial en 28 países; el escenario sin migración se desvía de la variante \"Zero migration\" de la ONU "
            "en {v4med} (mediana) y {v4max} (máximo).\n\n"
            "**Límites.** (1) Solo varía la TFR: sin choque de mortalidad ni cambio de migración. (2) Los 4 ajustes "
            "de falsabilidad de N\\* son constantes por país calibradas para 2024 (misma simplificación de la serie "
            "histórica). (3) Los perfiles (A–E) se definen por rangos de TFR; aquí la mezcla queda fija aunque la "
            "TFR cambie mucho. (4) Es un escenario condicional, no un pronóstico. (5) La TFR es una medida de "
            "período; no se modelan efectos de calendario. (6) El P_eq público de narayama.live usa un método más "
            "simple (sin el efecto eco de los nacimientos sobre el número de mujeres fértiles 25 años después); "
            "los valores pueden diferir en torno a {v5med} (mediana) y {v5max} (máximo) para el mismo escenario."
        ),
        "fr": (
            "**Méthode.** Projection par composantes de cohorte (âge simple × sexe), pas annuel. La survie et la "
            "migration nette suivent la projection moyenne de l'ONU (la migration est le résidu qui reproduit la "
            "projection de l'ONU, en nombres absolus par âge). Les naissances utilisent la fécondité par âge de "
            "l'ONU, mise à l'échelle de la TFR du scénario et calibrée sur le total officiel. N\\* suit la chaîne "
            "du projet (NGII → NGII_puro → N_Base → N\\* = √N_Base), avec les seuils d'âge du mélange de profils.\n\n"
            "**Validation** (`docs/validacao_projecao.md`) : le N\\* de 2024 recalculé par le moteur diffère de "
            "l'indice de production de {v3} au plus ; la calibration des naissances reste à moins de {v1} du total "
            "officiel dans 28 pays ; le scénario sans migration s'écarte de la variante « Zero migration » de l'ONU "
            "de {v4med} (médiane) et {v4max} (maximum).\n\n"
            "**Limites.** (1) Seule la TFR varie : pas de choc de mortalité ni de changement de migration. (2) Les "
            "4 ajustements de falsifiabilité de N\\* sont des constantes par pays calibrées pour 2024 (même "
            "simplification que la série historique). (3) Les profils (A–E) sont définis par des plages de TFR ; "
            "ici le mélange reste fixe même quand la TFR change beaucoup. (4) Scénario conditionnel, pas une "
            "prévision. (5) La TFR est une mesure de période ; les effets de calendrier ne sont pas modélisés. "
            "(6) Le P_eq public de narayama.live utilise une méthode plus simple (sans l'effet d'écho des naissances "
            "sur le nombre de femmes fécondes 25 ans plus tard) ; les valeurs peuvent différer d'environ {v5med} "
            "(médiane) à {v5max} (maximum) pour le même scénario."
        ),
        "it": (
            "**Metodo.** Proiezione per componenti di coorte (età singola × sesso), passo annuale. Sopravvivenza e "
            "migrazione netta seguono la proiezione media dell'ONU (la migrazione è il residuo che riproduce la "
            "proiezione ONU, in numeri assoluti per età). Le nascite usano la fecondità per età dell'ONU, scalata "
            "alla TFR dello scenario e calibrata sul totale ufficiale. N\\* usa la catena del progetto (NGII → "
            "NGII_puro → N_Base → N\\* = √N_Base), con i limiti d'età del mix di profili.\n\n"
            "**Validazione** (`docs/validacao_projecao.md`): l'N\\* del 2024 ricalcolato dal motore differisce "
            "dall'indice di produzione al massimo di {v3}; la calibrazione delle nascite resta entro {v1} del "
            "totale ufficiale in 28 paesi; lo scenario senza migrazione si discosta dalla variante \"Zero "
            "migration\" dell'ONU di {v4med} (mediana) e {v4max} (massimo).\n\n"
            "**Limiti.** (1) Varia solo la TFR: nessuno shock di mortalità né cambio di migrazione. (2) I 4 "
            "aggiustamenti di falsificabilità di N\\* sono costanti per paese calibrate sul 2024 (stessa "
            "semplificazione della serie storica). (3) I profili (A–E) sono definiti da fasce di TFR; qui il mix "
            "resta fisso anche quando la TFR cambia molto. (4) Scenario condizionale, non una previsione. (5) La "
            "TFR è una misura di periodo; gli effetti di calendario non sono modellati. (6) Il P_eq pubblico di "
            "narayama.live usa un metodo più semplice (senza l'effetto eco delle nascite sul numero di donne "
            "fertili 25 anni dopo); i valori possono differire di circa {v5med} (mediana) fino a {v5max} (massimo) "
            "per lo stesso scenario."
        ),
        "ko": (
            "**방법.** 연령(단일 연령) × 성별 코호트 요인법, 연 단위 추계입니다. 생존과 순이동은 UN 중위 추계를 따릅니다"
            "(이동은 UN 추계를 재현하는 잔차로, 연령별 절대 수입니다). 출생은 UN의 연령별 출산율을 시나리오 TFR에 맞게 "
            "조정하고 공식 총계에 보정해 계산합니다. N\\*는 프로젝트의 동일한 계산 사슬(NGII → NGII_puro → N_Base → "
            "N\\* = √N_Base)을 사용하며, 연령 구분은 프로필 구성에서 나옵니다.\n\n"
            "**검증**(`docs/validacao_projecao.md`): 모델로 다시 계산한 2024년 N\\*는 운영 지수와 최대 {v3} 차이이고, "
            "출생 보정은 28개국에서 공식 총계의 {v1} 이내이며, 이동 없는 시나리오는 UN \"Zero migration\" 변형과 "
            "{v4med}(중앙값), {v4max}(최대) 차이입니다.\n\n"
            "**한계.** (1) TFR만 변합니다: 사망률 충격이나 이동 변화는 없습니다. (2) N\\*의 4가지 반증가능성 조정은 "
            "2024년 기준 국가별 상수입니다(역사 시계열과 같은 단순화). (3) 프로필(A–E)은 TFR 구간으로 정의되지만 여기서는 "
            "TFR이 크게 변해도 구성이 고정됩니다. (4) 조건부 시나리오이며 예측이 아닙니다. (5) TFR은 기간 지표이며 "
            "시기(타이밍) 효과는 모델링하지 않습니다. (6) narayama.live의 공개 P_eq는 더 단순한 방법을 사용하며"
            "(출생이 25년 뒤 가임 여성 수에 미치는 반향 효과 없음), 같은 시나리오에서 값이 대략 {v5med}(중앙값)에서 "
            "{v5max}(최대)까지 다를 수 있습니다."
        ),
        "ja": (
            "**方法。** 年齢（1歳階級）×性別のコーホート要因法による年次推計です。生存と純移動は国連の中位推計に従います"
            "（移動は国連推計を再現する残差で、年齢別の絶対数）。出生は国連の年齢別出生率をシナリオのTFRに合わせて拡縮し、"
            "公式総数に較正します。N\\*はプロジェクトと同じ計算連鎖（NGII → NGII_puro → N_Base → N\\* = √N_Base）を使い、"
            "年齢区分はプロファイル構成から決まります。\n\n"
            "**検証**（`docs/validacao_projecao.md`）：モデルで再計算した2024年のN\\*は本番指数と最大でも{v3}の差、"
            "出生の較正は28か国で公式総数の{v1}以内、移動なしシナリオは国連の「Zero migration」変種と{v4med}（中央値）、"
            "{v4max}（最大）の乖離です。\n\n"
            "**限界。** (1) 変わるのはTFRだけで、死亡率ショックや移動の変化はありません。(2) N\\*の4つの反証可能性調整は"
            "2024年に較正した国別の定数です（歴史系列と同じ単純化）。(3) プロファイル（A–E）はTFRの範囲で定義されますが、"
            "ここではTFRが大きく変わっても構成は固定です。(4) 条件付きシナリオであり、予測ではありません。(5) TFRは期間指標で、"
            "タイミング効果はモデル化していません。(6) narayama.liveの公開P_eqはより単純な方法（出生が25年後の出産可能な女性数に"
            "及ぼす反響効果なし）を使っており、同じシナリオでも値が{v5med}（中央値）から{v5max}（最大）ほど異なることがあります。"
        ),
        "zh": (
            "**方法。**按年龄（单岁）×性别的队列要素法逐年推算。生存和净迁移遵循联合国中方案（迁移是复现联合国推算的残差，"
            "为各年龄的绝对数）。出生数采用联合国的分年龄生育率，按情景TFR缩放并校准到官方总数。N\\*沿用项目的同一计算链"
            "（NGII → NGII_puro → N_Base → N\\* = √N_Base），年龄分界来自类型构成。\n\n"
            "**验证**（`docs/validacao_projecao.md`）：模型重算的2024年N\\*与生产指数最多相差{v3}；出生数校准在28个国家中"
            "不超过官方总数的{v1}；无迁移情景与联合国“Zero migration”变体相差{v4med}（中位数）、{v4max}（最大）。\n\n"
            "**局限。**(1)只有TFR变化：没有死亡率冲击，也没有迁移变化。(2)N\\*的4项可证伪性调整是按2024年校准的国别常数"
            "（与历史序列相同的简化）。(3)类型（A–E）由TFR区间定义；此处即使TFR大幅变化，构成也保持固定。(4)这是条件情景，"
            "不是预测。(5)TFR是时期指标，未模拟时序效应。(6)narayama.live公开的P_eq使用更简单的方法（没有出生数对25年后"
            "育龄女性人数的回声效应），同一情景下数值可能相差约{v5med}（中位数）至{v5max}（最大）。"
        ),
        "fi": (
            "**Menetelmä.** Kohortti-komponenttiennuste (yksittäinen ikä × sukupuoli), vuosittainen askel. "
            "Eloonjääminen ja nettomuutto seuraavat YK:n keskiennustetta (muutto on jäännös, joka toistaa YK:n "
            "ennusteen absoluuttisina lukuina iän mukaan). Syntyneet lasketaan YK:n ikäkohtaisesta hedelmällisyydestä, "
            "skaalattuna skenaarion TFR:ään ja kalibroituna virallisiin kokonaislukuihin. N\\* käyttää projektin "
            "omaa laskentaketjua (NGII → NGII_puro → N_Base → N\\* = √N_Base), ikärajat tulevat profiiliyhdistelmästä.\n\n"
            "**Validointi** (`docs/validacao_projecao.md`): mallilla uudelleenlaskettu vuoden 2024 N\\* eroaa "
            "tuotantoindeksistä enintään {v3}; syntyneiden kalibrointi pysyy {v1} sisällä viralliseen kokonaislukuun "
            "nähden 28 maassa; ilman muuttoa -skenaario poikkeaa YK:n \"Zero migration\" -variantista {v4med} "
            "(mediaani) ja {v4max} (maksimi).\n\n"
            "**Rajoitukset.** (1) Vain TFR vaihtelee: ei kuolleisuusshokkia eikä muuton muutosta. (2) N\\*:n 4 "
            "falsifioitavuussäätöä ovat maakohtaisia vuoteen 2024 kalibroituja vakioita (sama yksinkertaistus kuin "
            "historiasarjassa). (3) Profiilit (A–E) määritellään TFR-rajoilla; tässä yhdistelmä pysyy kiinteänä, "
            "vaikka TFR muuttuisi paljon. (4) Ehdollinen skenaario, ei ennuste. (5) TFR on jaksomitta; "
            "ajoitusvaikutuksia ei mallinneta. (6) narayama.liven julkinen P_eq käyttää yksinkertaisempaa "
            "menetelmää (ilman syntyneiden kaikuvaikutusta hedelmällisten naisten määrään 25 vuotta myöhemmin); "
            "arvot voivat erota saman skenaarion osalta noin {v5med} (mediaani) – {v5max} (maksimi)."
        ),
    },
}
