"""
Orquestração do cálculo de N* para os 28 países (Fase 2a).

Lê data/raw/un_wpp.csv (via src.data_loader) e grava
data/processed/n_index_{ano}.csv com NGII_puro, Fator_Geracional,
N_Base e a zona de classificação, para todos os países presentes no
ano solicitado e em ano-25.

IMPORTANTE — escopo desta fase (confirmado em 2026-07-01): esta
função usa **apenas UN World Population Prospects**. Ainda não
calcula:
- Fator_Alocativo / farol institucional (+/n/-): depende de dados de
  NTA (National Transfer Accounts) e/ou OECD Social Expenditure
  Database, que não cobrem boa parte dos 28 países (OCDE só tem ~15
  membros na nossa lista). Fonte alternativa ainda não definida.
- O ajuste de escolaridade do NGII_puro (Taxa_Escolaridade_0-25 /
  Taxa_Esperada, Capítulo 5): não coberto por UN WPP nem OECD SOCX;
  precisaria de UNESCO ou World Bank Education Statistics. Por ora,
  usa-se 1,0/1,0 (fator neutro, sem efeito sobre o NGII_puro) —
  ver o parâmetro `taxa_escolaridade_neutra` abaixo.

Pop_Base/Pop_Topo (confirmado em 2026-07-01): usam as faixas etárias
por perfil da Seção V.III (Perfis A/B = 0-25/55+; Perfis C/D/E =
0-21/61+ — ver src.config.FAIXAS_ETARIAS_POR_PERFIL_V3), já agregadas
em data/raw/un_wpp.csv (colunas pop_base/pop_topo). Não é a faixa
fixa 0-25/25-65 do Capítulo 5 — só o terceiro fator (escolaridade) do
Capítulo 5 foi mantido.

Fonte de dados: UN World Population Prospects 2024
(population.un.org/wpp), arquivos "Demographic Indicators" e
"Population by Single Age" (não os grupos de 5 anos — os cortes em
21 e 61 anos exigem idade simples), variante "Medium".
"""

from pathlib import Path
from typing import Optional

import pandas as pd

from src.config import DATA_PROCESSED_DIR, DATA_RAW_DIR, PAISES
from src.data_loader import carregar_dados_un
from src.indices import calcular_fator_geracional, calcular_n_base, calcular_ngii_puro, classificar_zona_n_base

TAXA_ESCOLARIDADE_NEUTRA = 1.0  # fator = 1,0/1,0 = sem efeito (fonte ainda não integrada)
CICLO_GERACIONAL_ANOS = 25


def executar_pipeline_completo(ano: int, caminho_un: Optional[Path] = None) -> pd.DataFrame:
    """
    Calcula N* (NGII_puro x Fator_Geracional) para os 28 países da
    amostra, usando dados da UN WPP para `ano` e `ano - 25`.

    Args:
        ano: Ano de referência (ex.: 2024). Requer que data/raw/un_wpp.csv
            tenha linhas para este ano e para `ano - 25`.
        caminho_un: Caminho alternativo do CSV UN WPP (opcional, usa
            data/raw/un_wpp.csv por padrão).

    Returns:
        DataFrame com uma linha por país (só os países com dados em
        ambos os anos), colunas: codigo, n_base, farol, ngii_puro,
        fator_geracional, fator_alocativo, status, populacao. `farol`
        e `fator_alocativo` ficam None nesta fase (ver docstring do
        módulo). Também grava o resultado em
        data/processed/n_index_{ano}.csv.
    """
    caminho_un = caminho_un or (DATA_RAW_DIR / "un_wpp.csv")
    df = carregar_dados_un(caminho_un)

    ano_base = ano - CICLO_GERACIONAL_ANOS
    df_ano = df[df["ano"] == ano].set_index("pais_codigo")
    df_base = df[df["ano"] == ano_base].set_index("pais_codigo")

    resultados = []
    for codigo in PAISES:
        if codigo not in df_ano.index or codigo not in df_base.index:
            continue

        linha = df_ano.loc[codigo]

        ngii_puro = calcular_ngii_puro(
            pop_base=linha["pop_base"],
            pop_topo=linha["pop_topo"],
            nascimentos=linha["nascimentos"],
            mortes=linha["mortes"],
            taxa_escolaridade_0_25=TAXA_ESCOLARIDADE_NEUTRA,
            taxa_escolaridade_esperada=TAXA_ESCOLARIDADE_NEUTRA,
        )
        fator_geracional = calcular_fator_geracional(
            tfr_atual=linha["tfr"],
            tfr_25_anos_atras=df_base.loc[codigo, "tfr"],
        )
        n_base = calcular_n_base(ngii_puro, fator_geracional)

        resultados.append(
            {
                "codigo": codigo,
                "n_base": round(n_base, 4) if n_base is not None else None,
                "farol": None,  # Fator_Alocativo pendente (Fase 2b)
                "ngii_puro": round(ngii_puro, 4) if ngii_puro is not None else None,
                "fator_geracional": round(fator_geracional, 4) if fator_geracional is not None else None,
                "fator_alocativo": None,  # pendente (Fase 2b)
                "status": classificar_zona_n_base(n_base),
                "populacao": round(linha["pop_total"], 3),
            }
        )

    resultado_df = pd.DataFrame(resultados).sort_values("codigo").reset_index(drop=True)

    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    caminho_saida = DATA_PROCESSED_DIR / f"n_index_{ano}.csv"
    resultado_df.to_csv(caminho_saida, index=False)

    return resultado_df
