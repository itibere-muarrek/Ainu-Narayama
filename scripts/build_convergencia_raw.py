"""
Constrói data/raw/convergencia_un.csv — P_2.1 e P_eq (Tabela
Geracional, "cenário proposto de recuperação da TFR"), a partir de um
cenário próprio de convergência em 25+25 anos, simulado sobre
nascimentos/óbitos/TFR reais da UN World Population Prospects 2024
Revision (variante "Zero migration").

Origem da formalização: documento do autor "tabela geracional -
formula.docx" (2026-07-16), que define três conceitos:
  - P_E(t): população endógena (só nascimentos - óbitos, sem migração).
  - P_2.1 = P_E(t_c), onde t_c é o instante em que a TFR atinge 2,1.
  - P_eq = P_E(t_c + 25) — a população ~1 geração depois, mantendo
    TFR=2,1 o período todo. O tamanho populacional sustentável real.

Histórico da implementação (por que não é mais um salto instantâneo):
a v1 (2026-07-16) usava a variante oficial "Instant replacement zero
migration" da UN WPP, que assume TFR=2,1 já a partir de 2024. Auditoria
do autor em 2026-07-18 encontrou que essa premissa produzia números sem
sentido pra países de fecundidade baixa persistente: China e Coreia do
Sul apareciam com P_eq MAIOR que a população atual, apesar de TFR real
hoje muito abaixo de 2,1 (China ~0,9-1,0; Coreia ~0,7) — porque o salto
instantâneo ignora a trajetória real desses países.

Tentativa 2 (mesma auditoria): usar direto a trajetória real da ONU
(variante "Zero migration", fecundidade "Medium" + migração zero, sem
nenhum salto). Resultado: nenhum dos 20 países com TFR hoje abaixo de
2,1 (dos 28 do projeto) cruza TFR=2,1 até 2100 — o fim do horizonte de
projeção da ONU. Isso inclui os 7 países destaque do narayama.live
(Argentina, Brasil, China, Coreia do Sul, EUA, Itália, Japão). Ou seja,
o dado real e puro da ONU não cobre esse cenário — não existe "ano em
que a TFR retorna a 2,1" dentro do horizonte disponível pra praticamente
nenhum país do projeto.

Implementação atual (v2, 2026-07-18) — cenário PROPOSTO de recuperação
em 25+25 anos: decisão do autor. Em vez de um dado direto da ONU (que
não cobre o cenário) ou um salto instantâneo (irreal), simula-se um
cenário próprio: todo país — esteja hoje acima ou abaixo de 2,1 —
segue um plano de convergência LINEAR até TFR=2,1 ao longo de 25 anos
(t_c: ANO_CONVERGENCIA = ANO_ANCORA + 25), e depois mantém TFR=2,1 por
mais 25 anos (ANO_EQUILIBRIO = ANO_CONVERGENCIA + 25). Convergir nos
dois sentidos (não só recuperar quem está abaixo de 2,1, mas também
países hoje acima, como Nigéria) é coerente com o enquadramento da tese:
PEC (colapso, TFR baixa) e PEEC (saturação, TFR alta) são os dois
extremos, PEA (TFR ~2,1) é o meio — o mesmo plano de convergência serve
pros dois lados.

**A única parte "proposta" (não um dado direto da ONU) é a trajetória
de TFR** (`TFR_ramp`, interpolação linear até 2,1). Os nascimentos e
óbitos usados pra simular a população SÃO reais: vêm da variante "Zero
migration" da própria ONU (Births, Deaths, TFR anuais, colunas que
existem em WPP2024_Demographic_Indicators_OtherVariants.csv.gz).
Nascimentos são escalados pela razão TFR_ramp(t)/TFR_real(t) a cada ano
— aproximação padrão quando não se tem fecundidade específica por
idade (que este projeto não tem — exigiria tábua de mortalidade e
fecundidade por idade). Óbitos ficam com o valor real da ONU (não
dependem do cenário de fecundidade no curto/médio prazo). Simplificação
explícita, documentada em docs/definitions.md (seção 8-B) — não é um
modelo de coorte por idade, é uma escala do total de nascimentos.

Correção de interpretação (2026-07-18, mesma auditoria): a v2 original
comparava "população hoje (2024) → P_eq (2074)". O autor identificou que
essa comparação mistura dois efeitos distintos — a inércia etária própria
do país (que sozinha já pode fazer a população crescer por décadas mesmo
sem nenhuma mudança de política, caso do Brasil: TFR real ~1,6, mas
população real da ONU cresce até ~2043 antes de cair, por causa da base
grande de mulheres em idade fértil herdada de décadas de fecundidade mais
alta) com o efeito do cenário de recuperação proposto. Pra isolar o
efeito da política, o CSV agora traz `p_tendencia` — a população no MESMO
ano final (ANO_EQUILIBRIO=2074), mas seguindo a trajetória real da ONU
sem nenhuma rampa — pra comparar `p_tendencia → p_eq` (mesmo ano, dois
cenários) em vez de `população_hoje → p_eq` (anos diferentes, cenários
misturados).

Fonte: WPP2024_Demographic_Indicators_OtherVariants.csv.gz (mesma
pasta CSV_FILES da UN WPP usada pelos outros scripts de coleta —
esse arquivo cobre todas as variantes "especiais" da revisão 2024:
Instant replacement, Constant fertility, Momentum, Zero migration,
etc., não só a variante Medium).

Uso:
    python scripts/build_convergencia_raw.py [--output CAMINHO]

Sem --output, escreve em data/raw/convergencia_un.csv.
"""

import argparse
import gzip
import shutil
import sys
import urllib.request
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import DATA_RAW_DIR, PAISES

CACHE_DIR = DATA_RAW_DIR / "_cache"

URL_OUTRAS_VARIANTES = (
    "https://population.un.org/wpp/assets/Excel%20Files/"
    "1_Indicator%20(Standard)/CSV_FILES/"
    "WPP2024_Demographic_Indicators_OtherVariants.csv.gz"
)

VARIANTE = "Zero migration"
TFR_ALVO = 2.1
ANO_ANCORA = 2024  # ano-base, mesmo ano do snapshot em n_index_2024.csv
ANO_CONVERGENCIA = ANO_ANCORA + 25  # t_c: fim da rampa de 25 anos (2049)
ANO_EQUILIBRIO = ANO_CONVERGENCIA + 25  # t_c + 25: fim da estabilização (2074)

CODIGOS_ISO3 = list(PAISES.keys())
USECOLS = ["ISO3_code", "Variant", "Time", "TPopulation1July", "TFR", "Births", "Deaths"]


def _baixar_se_necessario() -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    destino = CACHE_DIR / "other_variants.csv.gz"
    if destino.exists():
        print(f"[cache] {destino.name} já existe, pulando download.")
        return destino
    print(f"[download] {URL_OUTRAS_VARIANTES}")
    req = urllib.request.Request(URL_OUTRAS_VARIANTES, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(destino, "wb") as f:
        shutil.copyfileobj(resp, f)
    print(f"[download] salvo em {destino} ({destino.stat().st_size / 1e6:.1f} MB)")
    return destino


def _tfr_ramp(ano: int, tfr_2024: float) -> float:
    """TFR proposta em `ano`: rampa linear de tfr_2024 (em ANO_ANCORA) até
    TFR_ALVO (em ANO_CONVERGENCIA), depois mantida em TFR_ALVO."""
    if ano >= ANO_CONVERGENCIA:
        return TFR_ALVO
    progresso = (ano - ANO_ANCORA) / (ANO_CONVERGENCIA - ANO_ANCORA)
    return tfr_2024 + (TFR_ALVO - tfr_2024) * progresso


def _simular_pais(serie: pd.DataFrame) -> dict:
    """Simula P_ramp(t) pra um país, ano a ano, de ANO_ANCORA até
    ANO_EQUILIBRIO, escalando nascimentos reais pela razão TFR_ramp/TFR_real.
    Também lê P_tendência(ANO_EQUILIBRIO) — a população no MESMO ano final,
    mas seguindo a trajetória real da ONU sem nenhuma rampa/política — pra
    comparar os dois no mesmo ano em vez de comparar contra a população de
    hoje (que mistura o efeito da política com a simples passagem do tempo/
    inércia etária; ver docs/definitions.md, seção 8-B, "problema dos dois
    números").
    """
    serie = serie.set_index("Time").sort_index()
    tfr_2024 = serie.loc[ANO_ANCORA, "TFR"]

    p_ramp = serie.loc[ANO_ANCORA, "TPopulation1July"]
    p_2_1 = None
    for ano in range(ANO_ANCORA, ANO_EQUILIBRIO):
        tfr_real_ano = serie.loc[ano, "TFR"]
        nascimentos_real = serie.loc[ano, "Births"]
        obitos_real = serie.loc[ano, "Deaths"]
        tfr_proposta = _tfr_ramp(ano, tfr_2024)
        nascimentos_ramp = nascimentos_real * (tfr_proposta / tfr_real_ano)
        p_ramp = p_ramp + nascimentos_ramp - obitos_real
        if ano + 1 == ANO_CONVERGENCIA:
            p_2_1 = p_ramp

    p_tendencia = serie.loc[ANO_EQUILIBRIO, "TPopulation1July"]
    tfr_tendencia = serie.loc[ANO_EQUILIBRIO, "TFR"]

    return {
        "ano_2_1": ANO_CONVERGENCIA,
        "p_2_1": round(p_2_1 / 1000, 4),
        "tfr_2_1": TFR_ALVO,
        "ano_eq": ANO_EQUILIBRIO,
        "p_eq": round(p_ramp / 1000, 4),
        "tfr_eq": TFR_ALVO,
        "p_tendencia": round(p_tendencia / 1000, 4),
        "tfr_tendencia": round(tfr_tendencia, 4),
    }


def construir(caminho_saida: Path) -> pd.DataFrame:
    caminho_gz = _baixar_se_necessario()

    partes = []
    with gzip.open(caminho_gz, "rt", encoding="utf-8-sig") as f:
        for chunk in pd.read_csv(f, usecols=USECOLS, chunksize=1_000_000, low_memory=False):
            filtrado = chunk[
                chunk["ISO3_code"].isin(CODIGOS_ISO3)
                & (chunk["Variant"] == VARIANTE)
                & chunk["Time"].between(ANO_ANCORA, ANO_EQUILIBRIO)
            ]
            if len(filtrado):
                partes.append(filtrado)
    if not partes:
        raise RuntimeError(f"Nenhuma linha encontrada para a variante '{VARIANTE}'")
    dados = pd.concat(partes, ignore_index=True)

    linhas = []
    for codigo in CODIGOS_ISO3:
        serie = dados[dados["ISO3_code"] == codigo]
        anos_presentes = set(serie["Time"])
        anos_esperados = set(range(ANO_ANCORA, ANO_EQUILIBRIO + 1))
        if not anos_esperados.issubset(anos_presentes):
            print(f"[aviso] série incompleta para {codigo}, pulando.")
            continue

        resultado_pais = _simular_pais(serie)
        linhas.append({"pais_codigo": codigo, **resultado_pais})

    resultado = pd.DataFrame(linhas).sort_values("pais_codigo").reset_index(drop=True)
    resultado.to_csv(caminho_saida, index=False)
    print(f"[ok] {len(resultado)} linhas escritas em {caminho_saida}")
    return resultado


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DATA_RAW_DIR / "convergencia_un.csv",
        help="Caminho de saída (padrão: data/raw/convergencia_un.csv)",
    )
    args = parser.parse_args()
    construir(args.output)
