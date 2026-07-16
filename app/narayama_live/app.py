"""
narayama.live — Interface pública minimalista do AINU-Narayama.

Mostra o Índice de Narayama Sistêmico (N*) apenas para os 7 países
destaque, sem os filtros e componentes técnicos detalhados (esses
ficam na plataforma restrita: ver app/ainu_systems/app.py).

Fonte: V1_EcoPol_062426_v8.0.docx, Anexo 14 (Glossário — "AINU"):
"Interface pública: Narayama.live (7 países destaque); interface
restrita a pesquisadores: ainu.systems." Lista dos 7 países destaque
confirmada pelo autor da tese em 2026-07-01 (ver
src.config.PAISES_DESTAQUE_NARAYAMA_LIVE): Argentina, Brasil, China,
Coreia do Sul, EUA, Itália, Japão.

Fonte de dados esperada (produzida pelo pipeline da Fase 2+):
data/processed/n_index_2024.csv — colunas: codigo, n_base, n_estrela,
farol, status. O N* mostrado aqui é `n_estrela` (sqrt(n_base) —
normalização de 2026-07-09, ver src.indices.normalizar_n_base), o
valor comprimido pra faixa plausível, mais adequado pra uma interface
pública minimalista do que o N_Base bruto.

Convenção de zonas do N* (atualizada em 2026-07-15 — a nota antiga
deste docstring, "N* alto é melhor", ficou desatualizada pela
classificação de 5 zonas de 12/07/2026, ver
src.indices.classificar_zona_5): não é "quanto maior melhor" — é um
equilíbrio no meio da escala. N* muito baixo (< 0,71) é Colapso de
Narayama (PEC); N* muito alto (≥ 2,00) é Saturação por Overbirths
(PEEC); o ideal fica no meio, entre 0,90 e 1,40 (Equilíbrio
Sustentável / PEA).
"""

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.config import DATA_PROCESSED_DIR, PAISES, PAISES_DESTAQUE_NARAYAMA_LIVE

# -----------------------------------------------------------------------
# Configuração da página
# -----------------------------------------------------------------------

st.set_page_config(page_title="Narayama.live", layout="centered")

# -----------------------------------------------------------------------
# Cabeçalho
# -----------------------------------------------------------------------

st.title("Narayama.live")
st.markdown("### Termômetro do Índice de Narayama Sistêmico")
st.markdown(
    "Acompanhe, de forma simples, a capacidade de renovação geracional "
    "de 7 países ao final de um ciclo de 25 anos — com base na tese de "
    "doutorado \"Do Dilema de Narayama ao Oicoceno Civilizacional\" (v8.0). "
    "Para análises detalhadas, simulações e calibração, veja "
    "[ainu.systems](https://ainu.systems)."
)
st.info(
    "**Como ler o N\\*:** não é uma nota de \"quanto maior, melhor\" — é um "
    "equilíbrio. N\\* muito baixo indica **Colapso de Narayama (PEC)**: "
    "poucos nascimentos não repõem a geração legatária. N\\* muito alto "
    "indica **Saturação por Overbirths (PEEC)**: crescimento populacional "
    "acelerado além da capacidade de absorção institucional. O ideal fica "
    "no meio da escala, faixa chamada de **Equilíbrio Sustentável (PEA)**. "
    "O farol institucional (+/n/-) ainda não aparece aqui: depende de "
    "dados de Contas de Transferências Nacionais (NTA) que este projeto "
    "ainda não tem — ver [ainu.systems](https://ainu.systems) para o "
    "detalhamento completo da metodologia."
)

# -----------------------------------------------------------------------
# Carregamento de dados
# -----------------------------------------------------------------------


@st.cache_data
def carregar_destaques() -> pd.DataFrame:
    """Carrega o snapshot 2024 do N*, restrito aos 7 países destaque."""
    caminho = DATA_PROCESSED_DIR / "n_index_2024.csv"
    if not caminho.exists():
        return pd.DataFrame()

    df = pd.read_csv(caminho)
    df = df[df["codigo"].isin(PAISES_DESTAQUE_NARAYAMA_LIVE)].copy()

    df["nome"] = df["codigo"].map(lambda c: PAISES[c]["nome"])

    if "n_estrela" in df.columns:
        def _formatar_n_estrela(linha: pd.Series) -> str | None:
            if pd.isna(linha["n_estrela"]):
                return None
            if "farol" in df.columns and pd.notna(linha.get("farol")):
                return f"{linha['n_estrela']:.2f}({linha['farol']})"
            # Farol ainda não calculado nesta fase (Fator_Alocativo
            # pendente — ver src/data_pipeline.py): mostra só o N*.
            return f"{linha['n_estrela']:.2f}"

        df["N*"] = df.apply(_formatar_n_estrela, axis=1)

    return df


df = carregar_destaques()

if df.empty:
    st.warning(
        "Nenhum dado encontrado em `data/processed/n_index_2024.csv`. "
        "Este arquivo ainda não foi gerado pelo pipeline de cálculo "
        "(Fase 2)."
    )
    st.stop()

# -----------------------------------------------------------------------
# Tabela minimalista
# -----------------------------------------------------------------------

st.header("N* — 7 Países Destaque (2024)")

df_tabela = df.sort_values("n_estrela").rename(columns={"nome": "País", "status": "Status"})

colunas_exibidas = [c for c in ["País", "N*", "Status"] if c in df_tabela.columns]
st.dataframe(df_tabela[colunas_exibidas], use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------
# Gráfico — N* por país
# -----------------------------------------------------------------------

if "n_estrela" in df.columns:
    fig = px.bar(
        df.sort_values("n_estrela"),
        x="nome",
        y="n_estrela",
        color="farol" if "farol" in df.columns else None,
        title="N* por país (2024)",
        labels={"nome": "País", "n_estrela": "N*"},
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------
# Rodapé
# -----------------------------------------------------------------------

st.markdown("---")
st.markdown(
    "**Dados**: UN World Population Prospects + OECD Social Expenditure Database  \n"
    "**Metodologia**: Tese \"Do Dilema de Narayama ao Oicoceno Civilizacional\" v8.0  \n"
    "**Análise detalhada**: [ainu.systems](https://ainu.systems)"
)
