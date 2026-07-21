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

Ordem da página (reorganizada em 2026-07-16, a pedido do autor: "a
tabela geracional de narayama deve encabeçar a página"): a Tabela
Geracional agora é o primeiro conteúdo visual da página, logo após o
cabeçalho/legenda — a tabela minimalista e o gráfico de barras viram
detalhe de apoio, abaixo dela.

Seletor de idioma (2026-07-18, decisão do autor): barra superior com
9 idiomas (PT padrão/fonte + EN/ES/JA/KO/IT/FI/FR/ZH), via
src.i18n — ver esse módulo pra convenções de tradução.
"""

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.config import (
    CODIGO_DDI_POR_PAIS,
    CORES_5_ZONAS,
    DATA_PROCESSED_DIR,
    DATA_RAW_DIR,
    PAISES,
    PAISES_DESTAQUE_NARAYAMA_LIVE,
)
from src.i18n import (
    nome_pais,
    nome_zona,
    seletor_idioma,
    sem_dado,
    sufixo_milhoes,
    t,
)

# -----------------------------------------------------------------------
# Configuração da página
# -----------------------------------------------------------------------

st.set_page_config(page_title="Narayama.live", layout="centered")

lang = seletor_idioma()

# -----------------------------------------------------------------------
# Cabeçalho
# -----------------------------------------------------------------------

st.title("Narayama.live")
st.markdown(f"### {t('narayama_subtitulo', lang)}")
st.markdown(t("narayama_intro", lang))
st.info(t("narayama_info", lang))

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

    try:
        conv_df = pd.read_csv(DATA_RAW_DIR / "convergencia_un.csv")
        conv_df = conv_df.rename(columns={"pais_codigo": "codigo"})[
            ["codigo", "p_eq", "ano_eq", "p_tendencia"]
        ]
        df = df.merge(conv_df, on="codigo", how="left")
    except FileNotFoundError:
        df["p_eq"] = None
        df["ano_eq"] = None
        df["p_tendencia"] = None

    return df


df = carregar_destaques()

if df.empty:
    st.warning(t("narayama_warning_sem_dado", lang))
    st.stop()

df["nome_exibicao"] = df["codigo"].map(lambda c: nome_pais(c, lang))

# -----------------------------------------------------------------------
# Tabela Geracional de Narayama (versão reduzida, 7 países destaque)
# -----------------------------------------------------------------------
# Mesma grade do ainu.systems (ver app/ainu_systems/app.py — Seção
# 9-A.7 da tese), portada em 2026-07-15. Movida para o topo da página
# em 2026-07-16, a pedido do autor.

st.header(t("tabela_geracional_header", lang))
st.caption(t("narayama_caption_grade", lang))
st.caption(t("caption_arrow_narayama", lang))

_ORDEM_ZONAS = [
    "Saturação por Overbirths (PEEC)",
    "Tensão Populacional",
    "Equilíbrio Sustentável (PEA)",
    "Tensão Acelerada",
    "Colapso de Narayama (PEC)",
]

if {"status", "n_estrela", "codigo", "nome", "populacao"}.issubset(df.columns):
    _sd = sem_dado(lang)
    _mi = sufixo_milhoes(lang)
    _blocos_html = []
    for _zona in _ORDEM_ZONAS:
        _paises_zona = df[df["status"] == _zona].sort_values("populacao", ascending=False)
        if _paises_zona.empty:
            continue
        _cor = CORES_5_ZONAS.get(_zona, "#eeeeee")
        _cards = []
        for _linha in _paises_zona.itertuples():
            _ddi = CODIGO_DDI_POR_PAIS.get(_linha.codigo, "?")
            _p_tendencia = getattr(_linha, "p_tendencia", None)
            _pop_tendencia = f"{_p_tendencia:.0f}{_mi}" if pd.notna(_p_tendencia) else _sd
            _p_eq = getattr(_linha, "p_eq", None)
            _pop_eq = f"{_p_eq:.0f}{_mi}" if pd.notna(_p_eq) else _sd
            _cards.append(
                f'<div style="background:{_cor};border:2px solid #1a1a1a;'
                f'border-radius:6px;padding:8px;margin-bottom:6px;'
                f'text-align:center;font-family:monospace;color:#1a1a1a;">'
                f'<div style="font-weight:700;font-size:0.8em;">{_linha.nome_exibicao} ({_ddi})</div>'
                f'<div style="font-weight:700;font-size:1.2em;">{_linha.n_estrela:.2f}'
                f'<span style="font-size:0.55em;font-weight:400;"> ({_sd})</span></div>'
                f'<div style="font-size:0.72em;">{_pop_tendencia} → {_pop_eq}</div>'
                f"</div>"
            )
        _blocos_html.append(
            f'<div style="flex:1;min-width:120px;">'
            f'<div style="font-size:0.75em;font-weight:600;margin-bottom:6px;text-align:center;">'
            f"{nome_zona(_zona, lang)} ({len(_paises_zona)})</div>"
            f'{"".join(_cards)}'
            f"</div>"
        )
    _grade_html = (
        '<div style="display:flex;gap:8px;align-items:flex-start;'
        'border-bottom:2px solid #1a1a1a;padding-bottom:8px;">'
        + "".join(_blocos_html)
        + "</div>"
        + '<div style="text-align:right;font-size:0.8em;font-weight:600;margin-top:4px;">'
        + t("indice_narayama_seta", lang)
        + "</div>"
    )
    st.markdown(_grade_html, unsafe_allow_html=True)

# -----------------------------------------------------------------------
# Tabela minimalista
# -----------------------------------------------------------------------

st.header(t("n_star_header_destaque", lang))

_col_pais = t("col_pais", lang)
_col_status = t("col_status", lang)
df_tabela = df.copy()
df_tabela[_col_pais] = df_tabela["nome_exibicao"]
df_tabela[_col_status] = df_tabela["status"].map(lambda z: nome_zona(z, lang))
df_tabela = df_tabela.sort_values("n_estrela")

colunas_exibidas = [c for c in [_col_pais, "N*", _col_status] if c in df_tabela.columns]
st.dataframe(df_tabela[colunas_exibidas], use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------
# Gráfico — N* por país
# -----------------------------------------------------------------------

if "n_estrela" in df.columns:
    fig = px.bar(
        df.sort_values("n_estrela"),
        x="nome_exibicao",
        y="n_estrela",
        color="farol" if "farol" in df.columns else None,
        title=t("bar_chart_title", lang),
        labels={"nome_exibicao": t("col_pais", lang), "n_estrela": "N*"},
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------
# Rodapé
# -----------------------------------------------------------------------

st.markdown("---")
st.markdown(t("footer_narayama", lang))
