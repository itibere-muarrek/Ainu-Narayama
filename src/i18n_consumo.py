"""
Textos da página "Consumo por coorte e Dividendo" (ainu.systems, atrás do login).

PT e EN são o texto-fonte. Idioma ou chave ausente cai em PT, como em src.i18n.t(); chaves que
não estão aqui caem no dicionário geral (src.i18n.T). Não há tradução às demais sete línguas
do site: fichas e tabelas desta página têm muito texto técnico e ficam para depois da revisão do autor.
"""

from src.i18n import IDIOMA_PADRAO, t

TX_CONS: dict[str, dict[str, str]] = {
    "c_titulo": {"pt": "Consumo por coorte e Dividendo Intergeracional (beta)", "en": "Cohort consumption and Intergenerational Dividend (beta)"},
    "c_intro": {
        "pt": (
            "Esta página escala números que o AINU.Systems já calculou (rascunho de pesquisa independente, não revisado). "
            "Você muda a porcentagem do Dividendo e o número de crianças adicionais; a página mostra o resultado na escala escolhida. "
            "**Nenhum modelo novo, nenhuma previsão e nenhuma estimativa de efeito causal.**"
        ),
        "en": (
            "This page rescales numbers that AINU.Systems has already computed (an independent research draft, not peer reviewed). "
            "You change the Dividend percentage and the number of additional children; the page shows the result at the chosen scale. "
            "**No new model, no forecast, and no causal effect estimate.**"
        ),
    },
    "c_sem_dados": {
        "pt": "Os dados do Diretório ainda não foram liberados neste ambiente (arquivo simulacoes.json ausente). A página só funciona depois que o autor libera os dados.",
        "en": "The Directory data has not been released in this environment (simulacoes.json is missing). The page only works after the author releases the data.",
    },
    "c_pais": {"pt": "País", "en": "Country"},
    "c_naturezas": {
        "pt": "Marcas: **SIM** simulação de mecanismo (custo), **EST** estimado por modelo, **PROJ** projeção condicional a cenário.",
        "en": "Labels: **SIM** mechanism simulation (cost), **EST** model estimate, **PROJ** scenario-conditional projection.",
    },
    # --- Dividendo ---------------------------------------------------------
    "c_div_titulo": {"pt": "1. Quanto custaria o Dividendo Intergeracional?", "en": "1. What would the Intergenerational Dividend cost?"},
    "c_div_ajuda": {
        "pt": "O Dividendo é pago aos Estruturadores e equivale a x% do gasto privado por Descendente, aplicado à coorte inteira. O custo é proporcional a x (conferido contra os 25% e 50% da planilha). Mede só o custo, não o efeito.",
        "en": "The Dividend is paid to Estruturadores and equals x% of private spending per Descendente, applied to the whole cohort. Cost is proportional to x (checked against the spreadsheet's 25% and 50%). It measures cost only, not effect.",
    },
    "c_div_slider": {"pt": "Dividendo, em % do gasto privado por Descendente", "en": "Dividend, as % of private spending per Descendente"},
    "c_div_custo": {"pt": "Custo anual (% do PIB)", "en": "Annual cost (% of GDP)"},
    "c_div_prog": {"pt": "Custo ÷ maior programa infantil de renda", "en": "Cost ÷ largest child cash programme"},
    "c_div_prog_nome": {"pt": "Maior programa: {nome}, {pct} do PIB ({ano})", "en": "Largest programme: {nome}, {pct} of GDP ({ano})"},
    "c_div_prog_ressalva": {"pt": "Valor aproximado ou derivado; ver a ficha do país antes de citar.", "en": "Approximate or derived value; see the country page before citing."},
    "c_div_prog_nd": {"pt": "Sem programa de nível de fonte confirmado para comparar.", "en": "No programme with a confirmed source level to compare."},
    "c_div_fam": {"pt": "Custo ÷ gasto público em família", "en": "Cost ÷ public family spending"},
    "c_div_fam_nome": {"pt": "Gasto público em família: {pct} do PIB ({ano}, OECD SOCX)", "en": "Public family spending: {pct} of GDP ({ano}, OECD SOCX)"},
    "c_div_fam_nd": {"pt": "A OECD SOCX não cobre este país.", "en": "OECD SOCX does not cover this country."},
    "c_div_base": {"pt": "Base do consumo dos Descendentes: {base}.", "en": "Base for Descendentes consumption: {base}."},
    "c_div_nd": {"pt": "Dividendo não calculável para este país (sem consumo em nível).", "en": "Dividend cannot be computed for this country (no consumption levels)."},
    "c_vezes": {"pt": "{x} vezes", "en": "{x} times"},
    # --- criança adicional --------------------------------------------------
    "c_inc_titulo": {"pt": "2. O que sustenta cada criança adicional?", "en": "2. What does each additional child sustain?"},
    "c_inc_ajuda": {
        "pt": "Valor por criança e por ano, do AINU.Systems (demanda de consumo, privado e público, que a criança representa), multiplicado pelo número de crianças. É um limite superior: usa o consumo médio por Descendente, vale por ano na coorte, não acumula nem desconta e não inclui a produção futura da criança.",
        "en": "Per-child, per-year value from AINU.Systems (the consumption demand, private and public, that the child represents), times the number of children. It is an upper bound: it uses average consumption per Descendente, holds per year in the cohort, does not accumulate or discount, and excludes the child's future output.",
    },
    "c_inc_n": {"pt": "Crianças adicionais", "en": "Additional children"},
    "c_inc_desloc": {"pt": "Parcela do gasto que desloca outro consumo (%)", "en": "Share of spending that displaces other consumption (%)"},
    "c_inc_consumo": {"pt": "Consumo atribuído por ano ({un})", "en": "Consumption attributed per year ({un})"},
    "c_inc_vad": {"pt": "Valor adicionado doméstico por ano ({un})", "en": "Domestic value added per year ({un})"},
    "c_inc_emp_bruto": {"pt": "Empregos brutos por ano", "en": "Gross jobs per year"},
    "c_inc_emp_liq": {"pt": "Empregos com o deslocamento escolhido", "en": "Jobs at the chosen displacement"},
    "c_inc_nd": {"pt": "Não calculado para este país: {motivo}", "en": "Not computed for this country: {motivo}"},
    "c_inc_motivo_default": {"pt": "sem tabela de insumo-produto nesta rodada.", "en": "no input-output table in this round."},
    "c_inc_nota": {
        "pt": "Os empregos são os que a demanda sustenta na economia, não os ocupados pela criança. Com 100% de deslocamento, a criança quase não acrescenta emprego, porque o gasto apenas troca de lugar.",
        "en": "These jobs are the ones the demand sustains in the economy, not jobs held by the child. At 100% displacement the child adds almost no jobs, because spending only moves elsewhere.",
    },
    # --- cenários ------------------------------------------------------------
    "c_cen_titulo": {"pt": "3. E se a fecundidade mudar?", "en": "3. What if fertility changes?"},
    "c_cen_ajuda": {
        "pt": "Variação em relação à continuidade da TFT, com consumo por pessoa constante (aba P5). São cenários do modelo de coortes do AINU.Systems (os nomes e as metas de TFT podem variar por país) e não previsões. Escolha o cenário para ver a variação em cada horizonte.",
        "en": "Change relative to a constant-TFR path, with per-person consumption held constant (sheet P5). These are scenarios of the AINU.Systems cohort model (names and TFR targets can vary by country) and not forecasts. Pick a scenario to see the change at each horizon.",
    },
    "c_cen_escolha": {"pt": "Cenário de fecundidade", "en": "Fertility scenario"},
    "c_cen_horizonte": {"pt": "Horizonte", "en": "Horizon"},
    "c_cen_ano": {"pt": "Ano", "en": "Year"},
    "c_cen_tft": {"pt": "TFT no ano", "en": "TFR in year"},
    "c_cen_desc": {"pt": "Δ Descendentes (%)", "en": "Δ Descendentes (%)"},
    "c_cen_estr": {"pt": "Δ Estruturadores (%)", "en": "Δ Estruturadores (%)"},
    "c_cen_asc": {"pt": "Δ Ascendentes (%)", "en": "Δ Ascendentes (%)"},
    "c_cen_cfcc": {"pt": "Δ consumo total (%)", "en": "Δ total consumption (%)"},
    "c_cen_pub": {"pt": "Δ consumo público (%)", "en": "Δ public consumption (%)"},
    "c_cen_nota": {
        "pt": "Os Estruturadores só diferem do contrafactual depois de cerca de duas décadas; por isso a variação de curto prazo vem quase toda dos Descendentes.",
        "en": "Estruturadores only differ from the counterfactual after about two decades; short-run changes come almost entirely from Descendentes.",
    },
    # --- rodapé --------------------------------------------------------------
    "c_rodape": {
        "pt": "Fonte: Diretório do AINU.Systems (rascunho v0.1; prévia privada). Cada número tem identificador de evidência na ficha do país. Itiberê L. G. C. Muarrek, pesquisa independente. Termos: Descendentes (Prometidos), Estruturadores, Ascendentes (Legadores).",
        "en": "Source: AINU.Systems Directory (draft v0.1; private preview). Each number has an evidence identifier on the country page. Itiberê L. G. C. Muarrek, independent research. Terms: Descendentes (Prometidos), Estruturadores, Ascendentes (Legadores).",
    },
    "c_fontes_titulo": {"pt": "Fontes e referências desta página", "en": "Sources and references for this page"},
    "c_fontes_nota": {
        "pt": "Fontes do país escolhido (menos as séries do Banco Mundial e da OIT, que ficam na ficha do país no Diretório), com o link para conferir e o identificador de evidência. Cálculos do autor (rascunho não revisado). A conferência de cada fonte (se o endereço abre e se o assunto confere) está no Diretório, em Dados verificáveis.",
        "en": "Sources for the chosen country (except the World Bank and ILO series, which are on the country page in the Directory), with a link to check and the evidence identifier. Author's calculations (unreviewed draft). The check of each source (whether the address opens and the subject matches) is in the Directory, under Verifiable data.",
    },
    "c_aviso_sup": {
        "pt": "SUPOSIÇÕES PARA PESQUISADORES. Esta página escala estimativas de modelo (marcas EST, PROJ e SIM) que dependem de premissas declaradas. Não são dados levantados nem testados contra uma fonte: os dados levantados e testados estão no Diretório (páginas Contas por Nascimentos e Dados Verificaveis).",
        "en": "ASSUMPTIONS FOR RESEARCHERS. This page rescales model estimates (labels EST, PROJ and SIM) that depend on declared premises. They are not data gathered or tested against a source: the gathered and tested data are in the Directory (pages Contas por Nascimentos and Dados Verificaveis).",
    },
    "c_est_titulo": {"pt": "4. Estimativas e projeções de modelo, por país (suposições)", "en": "4. Model estimates and projections, by country (assumptions)"},
    "c_est_ajuda": {
        "pt": "Tudo o que o AINU.Systems estima ou projeta para o país escolhido acima (consumo por coorte, projeção demográfica, multiplicadores, composição por grupo, exposição à automação e Dividendo), e a comparação entre países. São suposições de modelo, não dados observados.",
        "en": "Everything AINU.Systems estimates or projects for the country chosen above (cohort consumption, demographic projection, multipliers, group composition, automation exposure and Dividend), and the comparison across countries. They are model assumptions, not observed data.",
    },
    "c_est_comp": {"pt": "Comparação entre países", "en": "Comparison across countries"},
    "c_est_pais": {"pt": "País escolhido acima", "en": "Country chosen above"},
    "c_nota_idioma": {"pt": "", "en": "Translation made with AI, without native review; in case of doubt, the Portuguese text prevails."},
}


# mescla as demais línguas (es, fr, it, ko, ja, zh, fi), traduzidas por IA e ainda sem revisão nativa
from src.i18n_consumo_outros import TRAD  # noqa: E402

for _chave, _traducoes in TRAD.items():
    TX_CONS[_chave].update(_traducoes)


def tc(chave: str, lang: str, **fmt) -> str:
    entrada = TX_CONS.get(chave)
    if entrada is None:
        return t(chave, lang, **fmt)
    texto = entrada.get(lang) or entrada.get(IDIOMA_PADRAO) or chave
    if fmt:
        try:
            return texto.format(**fmt)
        except (KeyError, IndexError, ValueError):
            return texto
    return texto
