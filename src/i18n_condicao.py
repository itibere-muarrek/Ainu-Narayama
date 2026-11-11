"""
Textos da página "Condição média em TFT de reposição" (ainu.systems, atrás do login).

PT e EN são o texto-fonte. Idioma ausente cai em PT, como em src.i18n_consumo. As demais sete línguas ainda não
foram traduzidas (tradução por IA, sem revisão nativa, fica para depois da revisão do autor).
"""

from src.i18n import IDIOMA_PADRAO

TX: dict[str, dict[str, str]] = {
    "cm_titulo": {
        "pt": "Condição média em TFT de reposição (exploratório)",
        "en": "Average condition at replacement fertility (exploratory)",
    },
    "cm_intro": {
        "pt": (
            "Pergunta: quando a TFT converge para a reposição (2,1) e é mantida, a estrutura etária se estabiliza em vez de "
            "continuar se deteriorando? A única alavanca é a TFT; mortalidade e migração seguem a projeção média da ONU (WPP 2024). "
            "A página compara a Tendência da ONU com uma Meta nos ciclos de 25 anos (2024, 2049, 2074, 2099)."
        ),
        "en": (
            "Question: when fertility converges to replacement (2.1) and is held there, does the age structure stabilise instead of "
            "continuing to deteriorate? The only lever is fertility; mortality and migration follow the UN medium projection (WPP 2024). "
            "The page compares the UN Trend with a Target at 25-year cycles (2024, 2049, 2074, 2099)."
        ),
    },
    "cm_aviso": {
        "pt": (
            "**Exploratório e condicional, não previsão.** O N\\* depende da TFT e da estrutura etária; por isso sua chegada à zona de "
            "equilíbrio é uma checagem de coerência do índice e **não** evidência de sustentabilidade. As razões Ascendentes/Estruturador "
            "e Estruturadores por pessoa de 80+ (cuidador potencial, não efetivo) são as medidas que não derivam do N\\*. "
            "Costa Rica e Paraguai foram acrescentados em 2026-11-10 com perfil único pela faixa de TFT (CRI = C50/D50 (2026-11-11), PRY = B), aprovado pelo autor."
        ),
        "en": (
            "**Exploratory and conditional, not a forecast.** N\\* depends on fertility and age structure, so its arrival in the "
            "equilibrium zone is a coherence check of the index and **not** evidence of sustainability. The Ascendentes/Estruturadores "
            "ratio and Estruturadores per person aged 80+ (potential, not actual caregivers) are the measures that do not derive from N\\*. "
            "Costa Rica and Paraguay were added on 2026-11-10 with a single profile by fertility band (CRI = C50/D50 (2026-11-11), PRY = B), approved by the author."
        ),
    },
    "cm_alvo": {"pt": "TFT-alvo da Meta", "en": "Target TFR"},
    "cm_rampa": {"pt": "Anos até o alvo", "en": "Years to reach the target"},
    "cm_calculando": {"pt": "Projetando os países…", "en": "Projecting the countries…"},
    "cm_tab_titulo": {"pt": "1. Resumo por país", "en": "1. Summary by country"},
    "cm_tab_nota": {
        "pt": "A/E = Ascendentes ÷ Estruturadores (cortes etários do país). E/80+ = Estruturadores por pessoa de 80 anos ou mais.",
        "en": "A/E = Ascendentes ÷ Estruturadores (country age cuts). E/80+ = Estruturadores per person aged 80 or over.",
    },
    "cm_col_pais": {"pt": "País", "en": "Country"},
    "cm_col_n24": {"pt": "N* 2024", "en": "N* 2024"},
    "cm_col_n99t": {"pt": "N* 2099 Tendência", "en": "N* 2099 Trend"},
    "cm_col_n99m": {"pt": "N* 2099 Meta", "en": "N* 2099 Target"},
    "cm_col_zona": {"pt": "Zona 2099 (Meta)", "en": "Zone 2099 (Target)"},
    "cm_col_ae24": {"pt": "A/E 2024", "en": "A/E 2024"},
    "cm_col_ae74": {"pt": "A/E 2074 Meta", "en": "A/E 2074 Target"},
    "cm_col_ae99m": {"pt": "A/E 2099 Meta", "en": "A/E 2099 Target"},
    "cm_col_ae99t": {"pt": "A/E 2099 Tendência", "en": "A/E 2099 Trend"},
    "cm_col_e24": {"pt": "E/80+ 2024", "en": "E/80+ 2024"},
    "cm_col_e99m": {"pt": "E/80+ 2099 Meta", "en": "E/80+ 2099 Target"},
    "cm_col_e99t": {"pt": "E/80+ 2099 Tendência", "en": "E/80+ 2099 Trend"},
    "cm_mediana": {"pt": "Mediana (todos os países mostrados)", "en": "Median (all countries shown)"},
    "cm_mediana_sn": {"pt": "Mediana sem a Nigéria", "en": "Median excluding Nigeria"},
    "cm_baixar": {"pt": "Baixar a tabela completa (CSV)", "en": "Download the full table (CSV)"},
    "cm_graf_titulo": {"pt": "2. Trajetórias", "en": "2. Trajectories"},
    "cm_graf_paises": {"pt": "Países no gráfico", "en": "Countries in the chart"},
    "cm_graf_ae": {"pt": "Ascendentes ÷ Estruturadores", "en": "Ascendentes ÷ Estruturadores"},
    "cm_graf_n": {"pt": "N\\* (cada ponto é um ciclo de 25 anos)", "en": "N\\* (each point is a 25-year cycle)"},
    "cm_tendencia": {"pt": "Tendência ONU", "en": "UN Trend"},
    "cm_meta": {"pt": "Meta", "en": "Target"},
    "cm_ano": {"pt": "Ano", "en": "Year"},
    "cm_ler_titulo": {"pt": "Como ler", "en": "How to read"},
    "cm_ler": {
        "pt": (
            "- **Estabilizar não é restaurar.** Se A/E para de subir depois de dois ciclos mas fica acima do valor de 2024, a "
            "reposição estabiliza a estrutura em um nível mais envelhecido, não volta ao passado.\n"
            "- **2,1 é referência de reposição.** Para países com TFT acima dela (por exemplo Nigéria, Paraguai) a Meta é uma "
            "redução; a leitura é de convergência ao equilíbrio dos dois lados.\n"
            "- **E/80+ cai nos dois cenários**, porque os idosos de 2099 já nasceram; a Meta apenas evita a queda mais funda.\n"
            "- Limitações: um único conjunto de hipóteses (rampa e horizonte), migração e mortalidade da ONU, sem NTA nem economia."
        ),
        "en": (
            "- **Stabilising is not restoring.** If A/E stops rising after two cycles but stays above its 2024 value, replacement "
            "stabilises the structure at an older level; it does not return to the past.\n"
            "- **2.1 is a replacement reference.** For countries above it (e.g. Nigeria, Paraguay) the Target is a decrease; the "
            "reading is convergence to equilibrium from both sides.\n"
            "- **E/80+ falls in both scenarios**, because the 2099 elderly are already born; the Target only avoids the deeper fall.\n"
            "- Limitations: one set of assumptions (ramp and horizon), UN migration and mortality, no NTA and no economics."
        ),
    },
    "cm_fonte": {
        "pt": "Fonte: UN World Population Prospects 2024 (variante média); motor `src/projecao.py`; hipótese H8 do plano do Paper 3.",
        "en": "Source: UN World Population Prospects 2024 (medium variant); engine `src/projecao.py`; hypothesis H8 of the Paper 3 plan.",
    },
    "cm_p3": {"pt": "países do Paper 3", "en": "Paper 3 countries"},
    "cm_nota_idioma": {"pt": "", "en": "Translation made with AI, without native review; in case of doubt, the Portuguese text prevails."},
}

# mescla as demais línguas (es, fr, it, ko, ja, zh, fi), traduzidas por IA e ainda sem revisão nativa
from src.i18n_condicao_outros import TRAD  # noqa: E402

for _chave, _traducoes in TRAD.items():
    TX[_chave].update(_traducoes)


def tcm(chave: str, lang: str, **fmt) -> str:
    entrada = TX.get(chave)
    if entrada is None:
        return chave
    texto = entrada.get(lang)
    if texto is None:  # texto vazio é válido (PT não leva a nota de tradução)
        texto = entrada.get(IDIOMA_PADRAO, chave)
    if fmt:
        try:
            return texto.format(**fmt)
        except (KeyError, IndexError, ValueError):
            return texto
    return texto
