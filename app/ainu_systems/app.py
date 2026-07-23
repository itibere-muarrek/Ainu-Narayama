"""
ainu.systems — Plataforma restrita a pesquisadores e formuladores de política.

Cálculos detalhados, filtros por perfil/região e os componentes brutos
do N* (NGII_puro, Fator_Geracional, Fator_Alocativo) para os 28
países da amostra. Versão pública e minimalista: ver
app/narayama_live/app.py (7 países destaque, sem detalhamento técnico).

Fonte: V1_EcoPol_062426_v8.0.docx, Anexo 14 (Glossário — "AINU"):
"Interface pública: Narayama.live (7 países destaque); interface
restrita a pesquisadores: ainu.systems."

Fontes de dados esperadas (produzidas pelo pipeline da Fase 2+):
- data/processed/n_index_2024.csv: snapshot 2024, uma linha por país,
  colunas: codigo, n_base, n_estrela, farol, ngii_bruto, ngii_puro,
  fator_geracional, fator_alocativo, status, populacao.
- data/processed/n_index_historico.csv: série histórica, colunas:
  codigo, ano, n_base.

Nome/perfil/região dos países vêm de src.config.PAISES (não são
duplicados no CSV) e TFR 2024 vem de docs/paises_perfil.csv, usado só
para o diagnóstico de PEEC (que é feito pela TFR, não pelo N*).

Normalização (decisão de 2026-07-09, ver src.indices.normalizar_n_base):
`n_base` é o valor demográfico bruto (N_Base); `n_estrela` é o N*
reportado publicamente (sqrt(n_base)). Os limiares abaixo são os
brutos, usados pra classificar a zona (`status`) — a UI usa a versão
normalizada (src.config.LIMIARES_SIMPLES_NORMALIZADOS) só pra colorir
a tabela na escala exibida; a classificação em si é idêntica nas duas
escalas (raiz é monotônica).

Convenção de zonas do N_Base adotada (Tabela 4 / Anexo 8 da tese — ver
docs/definitions.md, seções 6 e 8): N_Base alto é melhor.
    N_Base > 1.10          -> Expansão Forte
    0.80 <= N_Base <= 1.10  -> Equilíbrio Sustentável (PEA)
    0.50 <= N_Base < 0.80   -> Tensão Acelerada
    N_Base < 0.50           -> Colapso de Narayama (PEC)
PEEC não é um limiar de N*: é diagnosticado por TFR > 2.8 (Cap. 3.2.1).

Seletor de idioma (2026-07-18, decisão do autor): barra superior com
9 idiomas (PT padrão/fonte + EN/ES/JA/KO/IT/FI/FR/ZH), via
src.i18n — ver esse módulo pra convenções de tradução. Nomes de
região são traduzidos; códigos de "perfil" (ex.: A35/B40/C25) são
alfanuméricos e não precisam de tradução.
"""

import os
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
    DOCS_DIR,
    LIMIAR_PEEC_TFR,
    PAISES,
)
from src.i18n import (
    nome_pais,
    nome_regiao,
    nome_zona,
    seletor_idioma,
    sem_dado,
    sufixo_milhoes,
    t,
)

# -----------------------------------------------------------------------
# Configuração da página
# -----------------------------------------------------------------------

st.set_page_config(page_title="ainu.systems", layout="wide")

lang = seletor_idioma()

# -----------------------------------------------------------------------
# Controle de acesso (placeholder — Fase 1)
# -----------------------------------------------------------------------
# "Plataforma restrita" na tese implica autenticação real (contas,
# papéis de pesquisador/formulador de política). Nesta fase, usamos
# apenas uma senha única via variável de ambiente AINU_SYSTEMS_PASSWORD
# como placeholder. Sem essa variável configurada, o acesso fica
# liberado (para não travar o desenvolvimento local) mas com aviso.


def _acesso_liberado() -> bool:
    senha_esperada = os.environ.get("AINU_SYSTEMS_PASSWORD")

    if not senha_esperada:
        st.warning(t("auth_nao_configurada", lang))
        return True

    senha_digitada = st.text_input(t("senha_prompt", lang), type="password")
    if senha_digitada == senha_esperada:
        return True
    if senha_digitada:
        st.error(t("senha_incorreta", lang))
    return False


if not _acesso_liberado():
    st.stop()

# -----------------------------------------------------------------------
# Cabeçalho
# -----------------------------------------------------------------------

st.title("ainu.systems")
st.markdown(f"### {t('ainu_subtitulo', lang)}")
st.markdown(t("ainu_intro", lang))

# -----------------------------------------------------------------------
# Carregamento de dados
# -----------------------------------------------------------------------


@st.cache_data
def carregar_n_index_2024() -> pd.DataFrame:
    """Carrega o snapshot 2024 do N* e enriquece com metadados dos países."""
    caminho = DATA_PROCESSED_DIR / "n_index_2024.csv"
    if not caminho.exists():
        return pd.DataFrame()

    df = pd.read_csv(caminho)

    metadados = pd.DataFrame.from_dict(PAISES, orient="index").reset_index()
    metadados = metadados.rename(columns={"index": "codigo"})[["codigo", "nome", "regiao", "perfil"]]

    df = df.merge(metadados, on="codigo", how="left")

    try:
        tfr_df = pd.read_csv(DOCS_DIR / "paises_perfil.csv")[["codigo", "tfr_2024"]]
        df = df.merge(tfr_df, on="codigo", how="left")
    except FileNotFoundError:
        df["tfr_2024"] = None

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


@st.cache_data
def carregar_n_index_historico() -> pd.DataFrame:
    """Carrega a série histórica do N* (1990-2024) por país."""
    caminho = DATA_PROCESSED_DIR / "n_index_historico.csv"
    if not caminho.exists():
        return pd.DataFrame()

    df = pd.read_csv(caminho)

    metadados = pd.DataFrame.from_dict(PAISES, orient="index").reset_index()
    metadados = metadados.rename(columns={"index": "codigo"})[["codigo", "nome"]]

    return df.merge(metadados, on="codigo", how="left")


df = carregar_n_index_2024()

if df.empty:
    st.warning(t("ainu_warning_sem_dado", lang))
else:
    df["nome_exibicao"] = df["codigo"].map(lambda c: nome_pais(c, lang))
    df["regiao_exibicao"] = df["regiao"].map(lambda r: nome_regiao(r, lang) if pd.notna(r) else r)

# -----------------------------------------------------------------------
# Filtros (sidebar)
# -----------------------------------------------------------------------

st.sidebar.header(t("filtros_header", lang))

_todos = t("todos", lang)
_todas = t("todas", lang)

perfis_disponiveis = [_todos] + sorted(df["perfil"].dropna().unique()) if not df.empty else [_todos]
perfil_selecionado = st.sidebar.selectbox(t("perfil_label", lang), perfis_disponiveis)

if not df.empty:
    _regioes_map = dict(zip(df["regiao_exibicao"], df["regiao"]))
    regioes_disponiveis_exibicao = [_todas] + sorted(df["regiao_exibicao"].dropna().unique())
else:
    _regioes_map = {}
    regioes_disponiveis_exibicao = [_todas]
regiao_selecionada_exibicao = st.sidebar.selectbox(t("regiao_label", lang), regioes_disponiveis_exibicao)
regiao_selecionada = _regioes_map.get(regiao_selecionada_exibicao, regiao_selecionada_exibicao)

busca_pais = st.sidebar.text_input(t("buscar_pais_label", lang))

df_filtrado = df.copy()
if not df_filtrado.empty:
    if perfil_selecionado != _todos:
        df_filtrado = df_filtrado[df_filtrado["perfil"] == perfil_selecionado]
    if regiao_selecionada_exibicao != _todas:
        df_filtrado = df_filtrado[df_filtrado["regiao"] == regiao_selecionada]
    if busca_pais:
        df_filtrado = df_filtrado[df_filtrado["nome_exibicao"].str.contains(busca_pais, case=False, na=False)]

# -----------------------------------------------------------------------
# Estatísticas (sidebar)
# -----------------------------------------------------------------------

st.sidebar.header(t("estatisticas_header", lang))

if not df.empty:
    contagem_zonas = df["status"].value_counts()
    st.sidebar.markdown(t("paises_por_zona_label", lang))
    for zona in [
        "Colapso de Narayama (PEC)",
        "Tensão Acelerada",
        "Equilíbrio Sustentável (PEA)",
        "Tensão Populacional",
        "Saturação por Overbirths (PEEC)",
    ]:
        st.sidebar.write(f"{nome_zona(zona, lang)}: {contagem_zonas.get(zona, 0)}")

    if "tfr_2024" in df.columns:
        risco_peec = int((df["tfr_2024"] > LIMIAR_PEEC_TFR).sum())
        st.sidebar.write(t("risco_peec_label", lang, limiar=LIMIAR_PEEC_TFR, valor=risco_peec))

    if "n_estrela" in df.columns and "perfil" in df.columns:
        st.sidebar.markdown(t("n_medio_perfil_label", lang))
        st.sidebar.dataframe(df.groupby("perfil")["n_estrela"].mean().round(3))

    if "fator_alocativo" in df.columns and "regiao_exibicao" in df.columns:
        st.sidebar.markdown(t("fator_alocativo_medio_regiao_label", lang))
        st.sidebar.dataframe(df.groupby("regiao_exibicao")["fator_alocativo"].mean().round(3))
else:
    st.sidebar.write(t("sem_dados_carregados", lang))

# -----------------------------------------------------------------------
# Tabela principal
# -----------------------------------------------------------------------

st.header(t("tabela_principal_header", lang))

st.caption(t("tabela_principal_caption", lang))

if not df_filtrado.empty:
    _pendente = t("pendente_nta", lang)
    _col_pais = t("col_pais", lang)
    _col_status = t("col_status", lang)
    _col_farol = t("col_farol", lang)

    df_tabela = df_filtrado.copy()
    df_tabela["farol"] = df_tabela["farol"].fillna(_pendente)
    df_tabela["fator_alocativo"] = df_tabela["fator_alocativo"].apply(
        lambda v: _pendente if pd.isna(v) else v
    )
    df_tabela[_col_pais] = df_tabela["nome_exibicao"]
    df_tabela[_col_status] = df_tabela["status"].map(lambda z: nome_zona(z, lang))
    df_tabela = df_tabela.sort_values("n_base").rename(
        columns={
            "n_estrela": "N*",
            "n_base": "N_Base",
            "farol": _col_farol,
            "ngii_bruto": "NGII_Bruto",
            "ngii_puro": "NGII_puro",
            "fator_geracional": "Fator_Ger",
            "fator_alocativo": "Fator_Aloc",
        }
    )

    colunas_exibidas = [
        c
        for c in [_col_pais, "N*", "N_Base", _col_farol, "NGII_Bruto", "NGII_puro", "Fator_Ger", "Fator_Aloc", _col_status]
        if c in df_tabela.columns
    ]

    def colorir_por_zona(linha: pd.Series) -> list:
        """Cores das 5 zonas (Seção 9-A.7) — mesma fonte que a coluna Status."""
        status_exibido = linha.get(_col_status)
        status_pt = next((z for z in CORES_5_ZONAS if nome_zona(z, lang) == status_exibido), status_exibido)
        cor_hex = CORES_5_ZONAS.get(status_pt)
        cor = f"background-color: {cor_hex}" if cor_hex else ""
        return [cor] * len(linha)

    st.dataframe(
        df_tabela[colunas_exibidas].style.apply(colorir_por_zona, axis=1),
        use_container_width=True,
    )
else:
    st.write(t("nenhum_pais_filtro", lang))

# -----------------------------------------------------------------------
# Gráfico 1 — Scatter Plot (NGII_puro vs Fator_Geracional)
# -----------------------------------------------------------------------
# Trocado de Fator_Alocativo pra Fator_Geracional em 2026-07-21: o
# usuário reportou o gráfico "não carregando" — não era bug de
# renderização, era fator_alocativo com 0/28 países preenchidos (NTA
# ainda não integrado, ver farol_gap_caption). Fator_Geracional é o
# outro componente real do N_Base (N_Base = NGII_puro × Fator_Geracional),
# sempre disponível pros 28 países — ver src/indices.py:calcular_n_base.

st.header(t("scatter_header", lang))

colunas_scatter = {"ngii_puro", "fator_geracional", "perfil", "populacao"}
if not df_filtrado.empty and colunas_scatter.issubset(df_filtrado.columns):
    fig_scatter = px.scatter(
        df_filtrado,
        x="ngii_puro",
        y="fator_geracional",
        color="perfil",
        size="populacao",
        hover_name="nome_exibicao",
        title=t("scatter_header", lang),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.write(t("scatter_fallback", lang))

# -----------------------------------------------------------------------
# Gráfico 2 — Série Temporal do N*
# -----------------------------------------------------------------------

st.header(t("serie_historica_header", lang))

df_historico = carregar_n_index_historico()

if not df_historico.empty:
    df_historico["nome_exibicao"] = df_historico["codigo"].map(lambda c: nome_pais(c, lang))
    paises_disponiveis = sorted(df_historico["nome_exibicao"].dropna().unique())
    paises_selecionados = st.multiselect(
        t("selecione_paises_label", lang),
        options=paises_disponiveis,
        default=paises_disponiveis[: min(5, len(paises_disponiveis))],
        max_selections=5,
    )

    df_historico_filtrado = df_historico[df_historico["nome_exibicao"].isin(paises_selecionados)]

    if not df_historico_filtrado.empty:
        fig_linha = px.line(
            df_historico_filtrado,
            x="ano",
            y="n_base",
            color="nome_exibicao",
            title=t("serie_historica_header", lang),
            labels={"ano": "Ano", "n_base": "N*", "nome_exibicao": t("col_pais", lang)},
        )
        st.plotly_chart(fig_linha, use_container_width=True)
    else:
        st.write(t("selecione_ao_menos_um_pais", lang))
else:
    st.write(t("serie_historica_indisponivel", lang))

# -----------------------------------------------------------------------
# Tabela Geracional de Narayama (visualização em formato periódico)
# -----------------------------------------------------------------------
# Layout fiel ao desenho original do usuário (2026-07-14): zonas como
# blocos lado a lado (eixo X = Índice Narayama), países ordenados
# dentro do bloco por tamanho de população (eixo Y), cada país
# identificado por nome + código DDI. Duas correções em relação à
# primeira versão (2026-07-13, linhas empilhadas por zona, código
# ISO3): não batiam com o desenho original.

st.header(t("tabela_geracional_header", lang))
st.caption(t("tabela_geracional_caption_ainu", lang))
st.caption(t("farol_gap_caption", lang))
st.caption(t("farol_provisorio_caption", lang))
st.caption(t("caption_arrow_ainu", lang))

_ORDEM_ZONAS = [
    "Saturação por Overbirths (PEEC)",
    "Tensão Populacional",
    "Equilíbrio Sustentável (PEA)",
    "Tensão Acelerada",
    "Colapso de Narayama (PEC)",
]

if not df.empty and {"status", "n_estrela", "codigo", "nome", "populacao"}.issubset(df.columns):
    _sd = sem_dado(lang)
    _mi = sufixo_milhoes(lang)
    _blocos_html = []
    for _zona in _ORDEM_ZONAS:
        _paises_zona = df[df["status"] == _zona].sort_values("populacao", ascending=False)
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
            f'<div style="flex:1;min-width:130px;">'
            f'<div style="font-size:0.8em;font-weight:600;margin-bottom:6px;text-align:center;">'
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
else:
    st.write(t("dados_insuficientes_tabela_geracional", lang))

# -----------------------------------------------------------------------
# Rodapé
# -----------------------------------------------------------------------

st.markdown("---")
st.markdown(t("footer_ainu", lang))
