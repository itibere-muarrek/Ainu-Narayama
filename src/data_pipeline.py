"""
Orquestração do cálculo de N* para os 28 países (Fase 2a).

Lê data/raw/un_wpp.csv (via src.data_loader) e grava
data/processed/n_index_{ano}.csv com NGII_Bruto, NGII_puro (pós
falseabilidade), Fator_Geracional, N_Base e a zona de classificação,
para todos os países presentes no ano solicitado e em ano-25.

IMPORTANTE — escopo desta fase (confirmado em 2026-07-01): esta
função usa **apenas UN World Population Prospects**. Ainda não
calcula Fator_Alocativo / farol institucional (+/n/-): depende de
dados de NTA (National Transfer Accounts) e/ou OECD Social
Expenditure Database, que não cobrem boa parte dos 28 países (OCDE
só tem ~15 membros na nossa lista). Fonte alternativa ainda não definida.

NGII_puro (atualizado em 2026-07-02): usa a fórmula de 2 componentes
do Anexo 1 — (Pop_Base/Pop_Topo) × (Nasc/Mort) — sem fator de
escolaridade (o terceiro fator do Capítulo 5 foi removido, ver
src/indices.py). O Anexo 1 não especifica normalização do N_Base:
valores altos em países jovens/alta fecundidade são esperados (ver
docs/definitions.md, seção 8).

Pop_Base/Pop_Topo (atualizado em 2026-07-04): cada país usa o corte
etário da média ponderada de sua composição de perfis (Seção 5.2 —
ver src.config.COMPOSICAO_PERFIL_POR_PAIS e src.config.PAISES), já
agregadas em data/raw/un_wpp.csv (colunas pop_base/pop_topo) pelo
script scripts/build_un_wpp_raw.py.

Protocolo de Falseabilidade (atualizado em 2026-07-07): a razão
calculada diretamente de Pop_Base/Pop_Topo/Nasc/Mort é o NGII_Bruto,
não o NGII_puro — antes desta data, o pipeline tratava um como o
outro por falta de dado real de falseabilidade. Agora o NGII_Bruto
passa pelo Protocolo de Falseabilidade quantitativo da v9.0
(V1_EcoPol_070726_v9.0.docx, Anexo 9 — ver
src.falseability.aplicar_falseabilidade_quantitativa e
src.config.AJUSTES_FALSEABILIDADE_POR_PAIS) para se tornar o
NGII_puro real, que então alimenta o N_Base.

Normalização (atualizada em 2026-07-09): `n_base` é o valor demográfico
bruto (N_Base = NGII_puro × Fator_Geracional). `n_estrela` é o N*
reportado publicamente — `sqrt(n_base)`, decisão do autor incorporada
diretamente na tese (ver src.indices.normalizar_n_base pro racional
completo). A zona (`status`) continua classificada a partir do
`n_base` bruto — matematicamente equivalente, já que a raiz é
monotônica.

Zonas (atualizado em 2026-07-13): `status` usa
`src.indices.classificar_zona_5` (5 zonas, revisão do autor de
12/07/2026), não mais `classificar_zona_n_base` (4 zonas, mantida
como referência histórica). Principal mudança: PEEC passa a ser
também um limiar de N_Base/N*, não só diagnosticado por TFR.

Fonte de dados: UN World Population Prospects 2024
(population.un.org/wpp), arquivos "Demographic Indicators" e
"Population by Single Age" (não os grupos de 5 anos — os cortes em
21 e 61 anos exigem idade simples), variante "Medium".
"""

from pathlib import Path
from typing import Optional

import pandas as pd

from src.config import AJUSTES_FALSEABILIDADE_POR_PAIS, DATA_PROCESSED_DIR, DATA_RAW_DIR, PAISES
from src.data_loader import carregar_dados_un
from src.falseability import aplicar_falseabilidade_quantitativa
from src.indices import (
    calcular_fator_geracional,
    calcular_n_base,
    calcular_ngii_puro,
    classificar_zona_5,
    normalizar_n_base,
)

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
        ambos os anos), colunas: codigo, n_base, n_estrela, farol,
        ngii_bruto, ngii_puro, fator_geracional, fator_alocativo,
        status, populacao. `farol` e `fator_alocativo` ficam None
        nesta fase (ver docstring do módulo). Também grava o resultado
        em data/processed/n_index_{ano}.csv.
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
        if codigo not in AJUSTES_FALSEABILIDADE_POR_PAIS:
            continue

        linha = df_ano.loc[codigo]

        ngii_bruto = calcular_ngii_puro(
            pop_base=linha["pop_base"],
            pop_topo=linha["pop_topo"],
            nascimentos=linha["nascimentos"],
            mortes=linha["mortes"],
        )
        ngii_puro = (
            aplicar_falseabilidade_quantitativa(ngii_bruto, AJUSTES_FALSEABILIDADE_POR_PAIS[codigo])
            if ngii_bruto is not None
            else None
        )
        fator_geracional = calcular_fator_geracional(
            tfr_atual=linha["tfr"],
            tfr_25_anos_atras=df_base.loc[codigo, "tfr"],
        )
        n_base = calcular_n_base(ngii_puro, fator_geracional)
        n_estrela = normalizar_n_base(n_base)

        resultados.append(
            {
                "codigo": codigo,
                "n_base": round(n_base, 4) if n_base is not None else None,
                "n_estrela": round(n_estrela, 4) if n_estrela is not None else None,
                "farol": None,  # Fator_Alocativo pendente (Fase 2b)
                "ngii_bruto": round(ngii_bruto, 4) if ngii_bruto is not None else None,
                "ngii_puro": round(ngii_puro, 4) if ngii_puro is not None else None,
                "fator_geracional": round(fator_geracional, 4) if fator_geracional is not None else None,
                "fator_alocativo": None,  # pendente (Fase 2b)
                "status": classificar_zona_5(n_base),
                "populacao": round(linha["pop_total"], 3),
            }
        )

    resultado_df = pd.DataFrame(resultados).sort_values("codigo").reset_index(drop=True)

    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    caminho_saida = DATA_PROCESSED_DIR / f"n_index_{ano}.csv"
    resultado_df.to_csv(caminho_saida, index=False)

    return resultado_df
