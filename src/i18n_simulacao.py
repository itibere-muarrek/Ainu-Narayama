"""
Textos da página de simulação e do login por usuário (ainu.systems, beta).

Só PT e EN por enquanto (a página é beta, para poucos testadores); os outros
idiomas caem em PT, como em src.i18n.t(). Chaves não encontradas aqui caem no
dicionário geral (src.i18n.T) — ex.: auth_nao_configurada, senha_prompt.
"""

from src.i18n import IDIOMA_PADRAO, t

TX_SIM: dict[str, dict[str, str]] = {
    # --- login ------------------------------------------------------------
    "login_usuario": {"pt": "Usuário", "en": "User"},
    "login_entrar": {"pt": "Entrar", "en": "Sign in"},
    "login_invalido": {"pt": "Usuário ou senha incorretos.", "en": "Wrong user or password."},
    "login_logado_como": {"pt": "Logado como {usuario}", "en": "Signed in as {usuario}"},
    "login_sair": {"pt": "Sair", "en": "Sign out"},
    # --- cabeçalho ---------------------------------------------------------
    "sim_titulo": {"pt": "Simulação geracional (beta)", "en": "Generational simulation (beta)"},
    "sim_intro": {
        "pt": (
            "Escolha um país e uma meta de fecundidade (TFR). O modelo projeta a população por idade e sexo em "
            "**dois ciclos geracionais** (2024 → 2049 → 2074): a TFR converge linearmente à meta em 25 anos e "
            "se mantém nos 25 seguintes. **Só a TFR muda.** Mortalidade e migração seguem a tendência da "
            "projeção média da ONU (UN WPP 2024)."
        ),
        "en": (
            "Pick a country and a fertility (TFR) target. The model projects population by age and sex over "
            "**two generational cycles** (2024 → 2049 → 2074): TFR converges linearly to the target in 25 years "
            "and holds for the next 25. **Only TFR changes.** Mortality and migration follow the UN WPP 2024 "
            "medium projection."
        ),
    },
    "sim_aviso": {
        "pt": (
            "**Cenário, não previsão.** O resultado diz o que aconteceria *se* a TFR seguisse a trajetória "
            "escolhida, mantido todo o resto na tendência da ONU. Versão beta: sujeita a ajustes."
        ),
        "en": (
            "**Scenario, not forecast.** The result shows what would happen *if* TFR followed the chosen path "
            "with everything else on the UN trend. Beta version: subject to change."
        ),
    },
    # --- controles -----------------------------------------------------------
    "sim_pais": {"pt": "País", "en": "Country"},
    "sim_tfr_alvo": {"pt": "TFR-alvo (filhos por mulher)", "en": "Target TFR (children per woman)"},
    "sim_tfr_atual": {"pt": "TFR atual (2024, ONU)", "en": "Current TFR (2024, UN)"},
    "sim_avancado": {"pt": "Ajuste à mão: composição de perfis do país", "en": "Manual adjustment: country profile mix"},
    "sim_avancado_ajuda": {
        "pt": (
            "Os cortes etários de Pop_Base/Pop_Topo vêm da composição de **até 3 perfis** (A–E, Tabela 14 da "
            "tese). Aqui você pode testar outra composição; os pesos devem somar 1. O padrão vem de "
            "`COMPOSICAO_PERFIL_POR_PAIS` em `src/config.py`."
        ),
        "en": (
            "Pop_Base/Pop_Topo age cuts come from a mix of **up to 3 profiles** (A–E, Table 14). You can try "
            "another mix here; weights must sum to 1. The default comes from `COMPOSICAO_PERFIL_POR_PAIS` in "
            "`src/config.py`."
        ),
    },
    "sim_peso": {"pt": "Peso do perfil {p}", "en": "Weight of profile {p}"},
    "sim_comp_invalida": {
        "pt": "Composição inválida ({motivo}); usando a composição padrão do país.",
        "en": "Invalid mix ({motivo}); using the country's default mix.",
    },
    "sim_comp_soma": {"pt": "os pesos somam {s:.2f}, não 1", "en": "weights sum to {s:.2f}, not 1"},
    "sim_comp_max3": {"pt": "mais de 3 perfis com peso", "en": "more than 3 profiles with weight"},
    "sim_cortes": {
        "pt": "Cortes resultantes: Pop_Base = idades 0–{b}; Pop_Topo = idades {t}+.",
        "en": "Resulting cuts: Pop_Base = ages 0–{b}; Pop_Topo = ages {t}+.",
    },
    # --- resultados ------------------------------------------------------------
    "sim_resumo": {"pt": "Resumo", "en": "Summary"},
    "sim_pop_titulo": {"pt": "População total (milhões)", "en": "Total population (millions)"},
    "sim_n_titulo": {"pt": "N\\* ao longo do tempo", "en": "N\\* over time"},
    "sim_cenario": {"pt": "Cenário (TFR → {alvo:.2f})", "en": "Scenario (TFR → {alvo:.2f})"},
    "sim_base": {"pt": "Tendência da ONU", "en": "UN trend"},
    "sim_ano": {"pt": "Ano", "en": "Year"},
    "sim_pop": {"pt": "População", "en": "Population"},
    "sim_pop_ano": {"pt": "População em {ano} (milhões)", "en": "Population in {ano} (millions)"},
    "sim_n_ano": {"pt": "N* em {ano}", "en": "N* in {ano}"},
    "sim_zona_ano": {"pt": "Zona em {ano}", "en": "Zone in {ano}"},
    "sim_virada_titulo": {"pt": "Pontos de virada", "en": "Turning points"},
    "sim_virada_nota": {
        "pt": "Três leituras de \"virada\", todas calculadas dentro do horizonte (até 2074).",
        "en": "Three readings of \"turning point\", all computed within the horizon (to 2074).",
    },
    "sim_v_saldo": {"pt": "Nascimentos passam a superar óbitos", "en": "Births come to exceed deaths"},
    "sim_v_pico": {"pt": "Pico da população (depois cai)", "en": "Population peak (then declines)"},
    "sim_v_fim_queda": {"pt": "Fim da queda (população volta a crescer)", "en": "End of decline (population grows again)"},
    "sim_v_n": {"pt": "N* alcança 0,90 (entra no PEA)", "en": "N* reaches 0.90 (enters PEA)"},
    "sim_v_sempre_pos": {"pt": "já era positivo", "en": "already positive"},
    "sim_v_sempre_neg": {"pt": "permanece negativo", "en": "stays negative"},
    "sim_v_nao": {"pt": "não ocorre até 2074", "en": "does not occur by 2074"},
    "sim_v_cresce": {"pt": "cresce o tempo todo", "en": "grows throughout"},
    "sim_v_cai": {"pt": "cai o tempo todo", "en": "declines throughout"},
    "sim_v_n_ja": {"pt": "já ≥ 0,90 em 2024 e se mantém", "en": "already ≥ 0.90 in 2024 and stays"},
    "sim_v_n_ja_cai": {"pt": "já ≥ 0,90 em 2024; abaixo a partir de {ano}", "en": "already ≥ 0.90 in 2024; below from {ano}"},
    "sim_v_n_nunca": {"pt": "não alcança 0,90 até 2074", "en": "does not reach 0.90 by 2074"},
    "sim_v_pos_depois_neg": {"pt": "já positivo; negativo a partir de {ano}", "en": "already positive; negative from {ano}"},
    "sim_col_item": {"pt": "Leitura", "en": "Reading"},
    "sim_nasc_obitos": {"pt": "Nascimentos e óbitos por ano (milhões)", "en": "Births and deaths per year (millions)"},
    "sim_nascimentos": {"pt": "Nascimentos", "en": "Births"},
    "sim_obitos": {"pt": "Óbitos", "en": "Deaths"},
    "sim_piramide_titulo": {"pt": "População por idade", "en": "Population by age"},
    "sim_piramide_ano": {"pt": "Ano da estrutura etária", "en": "Year of age structure"},
    "sim_idade": {"pt": "Idade", "en": "Age"},
    "sim_milhares": {"pt": "Milhares de pessoas", "en": "Thousands of people"},
    "sim_base_topo": {"pt": "Faixas Pop_Base e Pop_Topo", "en": "Pop_Base and Pop_Topo ranges"},
    # --- método ----------------------------------------------------------------
    "sim_metodo_titulo": {"pt": "Como o modelo funciona e o que ele NÃO faz", "en": "How the model works and what it does NOT do"},
    "sim_metodo": {
        "pt": (
            "**Método.** Projeção por componentes de coorte (idade simples × sexo), passo anual. Sobrevivência e "
            "migração líquida seguem a projeção média da ONU (a migração é o resíduo que reproduz a projeção da "
            "ONU, em número absoluto por idade). Os nascimentos vêm da fecundidade por idade da ONU, escalada "
            "para a TFR do cenário, e calibrados ao total oficial. O N\\* usa a mesma cadeia do projeto "
            "(NGII → NGII_puro → N_Base → N\\* = √N_Base), com os cortes etários da composição de perfis.\n\n"
            "**Validação** (`docs/validacao_projecao.md`): o N\\* de 2024 recalculado pelo motor difere do índice "
            "de produção em no máximo 0,03%; a calibração dos nascimentos fica em ±1% nos 28 países; o cenário "
            "sem migração desvia da variante \"Zero migration\" da ONU em 0,45% (mediana) e 1,75% (máximo).\n\n"
            "**Limites.** (1) Só a TFR varia: sem choque de mortalidade, sem mudança de migração. (2) Os 4 "
            "ajustes de falseabilidade do N\\* são constantes por país, calibradas para 2024 (mesma simplificação "
            "da série histórica). (3) Os perfis (A–E) são definidos por faixas de TFR; aqui a composição fica "
            "fixa mesmo quando a TFR muda muito. (4) É um cenário condicional, não uma previsão. (5) A TFR é "
            "medida de período; não modelamos efeito de calendário (adiamento/recuperação de nascimentos)."
        ),
        "en": (
            "**Method.** Cohort-component projection (single age × sex), annual step. Survival and net migration "
            "follow the UN medium projection (migration is the residual that reproduces the UN projection, in "
            "absolute numbers by age). Births use UN age-specific fertility, scaled to the scenario TFR and "
            "calibrated to the official total. N\\* uses the project's own chain (NGII → NGII_puro → N_Base → "
            "N\\* = √N_Base), with age cuts from the profile mix.\n\n"
            "**Validation** (`docs/validacao_projecao.md`): the model's 2024 N\\* differs from the production index "
            "by at most 0.03%; birth calibration stays within ±1% across 28 countries; the no-migration run "
            "deviates from the UN \"Zero migration\" variant by 0.45% (median) and 1.75% (max).\n\n"
            "**Limits.** (1) Only TFR varies: no mortality shock, no migration change. (2) The 4 falsifiability "
            "adjustments of N\\* are per-country constants calibrated for 2024 (same simplification as the "
            "historical series). (3) Profiles (A–E) are defined by TFR ranges; here the mix stays fixed even "
            "when TFR changes a lot. (4) A conditional scenario, not a forecast. (5) TFR is a period measure; "
            "tempo effects (birth postponement/recuperation) are not modeled."
        ),
    },
}


def ts(chave: str, lang: str, **fmt) -> str:
    """Texto da página de simulação; cai em PT, depois no dicionário geral."""
    entrada = TX_SIM.get(chave)
    if entrada is None:
        return t(chave, lang, **fmt)
    texto = entrada.get(lang) or entrada.get(IDIOMA_PADRAO) or chave
    if fmt:
        try:
            return texto.format(**fmt)
        except (KeyError, IndexError, ValueError):
            return texto
    return texto
