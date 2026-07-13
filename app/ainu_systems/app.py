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
"""

import os
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.config import CORES_5_ZONAS, DATA_PROCESSED_DIR, DOCS_DIR, LIMIAR_PEEC_TFR, PAISES

# -----------------------------------------------------------------------
# Configuração da página
# -----------------------------------------------------------------------

st.set_page_config(page_title="ainu.systems", layout="wide")

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
        st.warning(
            "Autenticação não configurada nesta instância (Fase 1 — "
            "placeholder). Defina a variável de ambiente "
            "`AINU_SYSTEMS_PASSWORD` para restringir o acesso."
        )
        return True

    senha_digitada = st.text_input("Senha de acesso (ainu.systems)", type="password")
    if senha_digitada == senha_esperada:
        return True
    if senha_digitada:
        st.error("Senha incorreta.")
    return False


if not _acesso_liberado():
    st.stop()

# -----------------------------------------------------------------------
# Cabeçalho
# -----------------------------------------------------------------------

st.title("ainu.systems")
st.markdown("### Plataforma restrita a pesquisadores e formuladores de política")
st.markdown(
    "Cálculos detalhados do Índice de Narayama Sistêmico (N*) para os "
    "28 países da amostra, com base na tese de doutorado "
    "\"Do Dilema de Narayama ao Oicoceno Civilizacional\" (v8.0). "
    "Para a visão pública e simplificada, veja "
    "[narayama.live](https://narayama.live)."
)

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
    st.warning(
        "Nenhum dado encontrado em `data/processed/n_index_2024.csv`. "
        "Este arquivo ainda não foi gerado pelo pipeline de cálculo "
        "(Fase 2). As seções abaixo aparecem vazias até que os dados "
        "existam."
    )

# -----------------------------------------------------------------------
# Filtros (sidebar)
# -----------------------------------------------------------------------

st.sidebar.header("Filtros")

perfis_disponiveis = ["Todos"] + sorted(df["perfil"].dropna().unique()) if not df.empty else ["Todos"]
perfil_selecionado = st.sidebar.selectbox("Perfil", perfis_disponiveis)

regioes_disponiveis = ["Todas"] + sorted(df["regiao"].dropna().unique()) if not df.empty else ["Todas"]
regiao_selecionada = st.sidebar.selectbox("Região", regioes_disponiveis)

busca_pais = st.sidebar.text_input("Buscar país")

df_filtrado = df.copy()
if not df_filtrado.empty:
    if perfil_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["perfil"] == perfil_selecionado]
    if regiao_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado["regiao"] == regiao_selecionada]
    if busca_pais:
        df_filtrado = df_filtrado[df_filtrado["nome"].str.contains(busca_pais, case=False, na=False)]

# -----------------------------------------------------------------------
# Estatísticas (sidebar)
# -----------------------------------------------------------------------

st.sidebar.header("Estatísticas")

if not df.empty:
    contagem_zonas = df["status"].value_counts()
    st.sidebar.markdown("**Países por zona de N\\*:**")
    for zona in [
        "Colapso de Narayama (PEC)",
        "Tensão Acelerada",
        "Equilíbrio Sustentável (PEA)",
        "Tensão Populacional",
        "Saturação por Overbirths (PEEC)",
    ]:
        st.sidebar.write(f"{zona}: {contagem_zonas.get(zona, 0)}")

    if "tfr_2024" in df.columns:
        risco_peec = int((df["tfr_2024"] > LIMIAR_PEEC_TFR).sum())
        st.sidebar.write(f"Risco PEEC (TFR > {LIMIAR_PEEC_TFR}): {risco_peec}")

    if "n_estrela" in df.columns and "perfil" in df.columns:
        st.sidebar.markdown("**N\\* médio por perfil:**")
        st.sidebar.dataframe(df.groupby("perfil")["n_estrela"].mean().round(3))

    if "fator_alocativo" in df.columns and "regiao" in df.columns:
        st.sidebar.markdown("**Fator_Alocativo médio por região:**")
        st.sidebar.dataframe(df.groupby("regiao")["fator_alocativo"].mean().round(3))
else:
    st.sidebar.write("Sem dados carregados.")

# -----------------------------------------------------------------------
# Tabela principal
# -----------------------------------------------------------------------

st.header("Tabela Principal — N* por País (2024)")

st.caption(
    "N* = raiz quadrada do N_Base (decisão de 2026-07-09, sendo "
    "incorporada pelo autor na tese) — normaliza os casos extremos de "
    "países jovens/alta fecundidade sem empatar países entre si nem "
    "usar constante arbitrária. `N_Base` (valor demográfico bruto) "
    "fica ao lado, pra transparência. `NGII_Puro` já é depurado pelo "
    "Protocolo de Falseabilidade quantitativo (4 ajustes multiplicativos "
    "— migração, inércia demográfica, políticas natalistas temporárias, "
    "sub-registro/mortalidade — Anexo 9, v9.0); `NGII_Bruto` é o valor "
    "sem esse ajuste. `Farol`/`Fator_Aloc` aparecem como \"Pendente "
    "(NTA)\" porque dependem de National Transfer Accounts, ainda não "
    "integrado (Fase 2b). Detalhes em "
    "[docs/definitions.md](../../docs/definitions.md), seções 6, 7 e 8."
)

if not df_filtrado.empty:
    df_tabela = df_filtrado.copy()
    df_tabela["farol"] = df_tabela["farol"].fillna("Pendente (NTA)")
    df_tabela["fator_alocativo"] = df_tabela["fator_alocativo"].apply(
        lambda v: "Pendente (NTA)" if pd.isna(v) else v
    )
    df_tabela = df_tabela.sort_values("n_base").rename(
        columns={
            "nome": "País",
            "n_estrela": "N*",
            "n_base": "N_Base",
            "farol": "Farol",
            "ngii_bruto": "NGII_Bruto",
            "ngii_puro": "NGII_puro",
            "fator_geracional": "Fator_Ger",
            "fator_alocativo": "Fator_Aloc",
            "status": "Status",
        }
    )

    colunas_exibidas = [
        c
        for c in ["País", "N*", "N_Base", "Farol", "NGII_Bruto", "NGII_puro", "Fator_Ger", "Fator_Aloc", "Status"]
        if c in df_tabela.columns
    ]

    def colorir_por_zona(linha: pd.Series) -> list:
        """Cores das 5 zonas (Seção 9-A.7) — mesma fonte que a coluna Status."""
        status = linha.get("Status")
        cor_hex = CORES_5_ZONAS.get(status)
        cor = f"background-color: {cor_hex}" if cor_hex else ""
        return [cor] * len(linha)

    st.dataframe(
        df_tabela[colunas_exibidas].style.apply(colorir_por_zona, axis=1),
        use_container_width=True,
    )
else:
    st.write("Nenhum país corresponde aos filtros selecionados (ou não há dados carregados).")

# -----------------------------------------------------------------------
# Gráfico 1 — Scatter Plot (NGII_puro vs Fator_Alocativo)
# -----------------------------------------------------------------------

st.header("NGII_puro vs Fator_Alocativo (28 países, 2024)")

colunas_scatter = {"ngii_puro", "fator_alocativo", "perfil", "populacao"}
if not df_filtrado.empty and colunas_scatter.issubset(df_filtrado.columns):
    fig_scatter = px.scatter(
        df_filtrado,
        x="ngii_puro",
        y="fator_alocativo",
        color="perfil",
        size="populacao",
        hover_name="nome",
        title="NGII_puro vs Fator_Alocativo (28 países 2024)",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.write(
        "Gráfico indisponível: faltam dados ou a coluna `populacao` "
        "em `data/processed/n_index_2024.csv`."
    )

# -----------------------------------------------------------------------
# Gráfico 2 — Série Temporal do N*
# -----------------------------------------------------------------------

st.header("Evolução do N* — Série Histórica")

df_historico = carregar_n_index_historico()

if not df_historico.empty:
    paises_disponiveis = sorted(df_historico["nome"].dropna().unique())
    paises_selecionados = st.multiselect(
        "Selecione de 3 a 5 países",
        options=paises_disponiveis,
        default=paises_disponiveis[: min(5, len(paises_disponiveis))],
        max_selections=5,
    )

    df_historico_filtrado = df_historico[df_historico["nome"].isin(paises_selecionados)]

    if not df_historico_filtrado.empty:
        fig_linha = px.line(
            df_historico_filtrado,
            x="ano",
            y="n_base",
            color="nome",
            title="Evolução do N* — Série Histórica",
            labels={"ano": "Ano", "n_base": "N*", "nome": "País"},
        )
        st.plotly_chart(fig_linha, use_container_width=True)
    else:
        st.write("Selecione ao menos um país para exibir a série histórica.")
else:
    st.write(
        "Série histórica indisponível: `data/processed/n_index_historico.csv` "
        "ainda não foi gerado pelo pipeline (Fase 2+)."
    )

# -----------------------------------------------------------------------
# Tabela Geracional de Narayama (visualização em formato periódico)
# -----------------------------------------------------------------------

st.header("Tabela Geracional de Narayama")
st.caption(
    "Grade comparativa dos 28 países segundo o N* (Seção 9-A.7 da tese, "
    "revisão de 12/07/2026), organizada nas 5 zonas da Seção 9-A.3. "
    "Dentro de cada zona, países ordenados por N* decrescente — mostra "
    "sempre os 28 países, independente dos filtros de Perfil/Região "
    "acima. Farol institucional, gerações até estabilização e projeção "
    "populacional não aparecem aqui: dependem de National Transfer "
    "Accounts (Fator_Alocativo) ou de um modelo de projeção TFR que "
    "este projeto ainda não implementa — ver seções 5 e 9 de "
    "[docs/definitions.md](../../docs/definitions.md)."
)

_ORDEM_ZONAS = [
    "Colapso de Narayama (PEC)",
    "Tensão Acelerada",
    "Equilíbrio Sustentável (PEA)",
    "Tensão Populacional",
    "Saturação por Overbirths (PEEC)",
]

if not df.empty and {"status", "n_estrela", "codigo"}.issubset(df.columns):
    _linhas_html = []
    for _zona in _ORDEM_ZONAS:
        _paises_zona = df[df["status"] == _zona].sort_values("n_estrela", ascending=False)
        _cor = CORES_5_ZONAS.get(_zona, "#eeeeee")
        _tiles = "".join(
            f'<div style="background:{_cor};border:1px solid rgba(0,0,0,0.2);'
            f'border-radius:6px;padding:6px 10px;min-width:64px;text-align:center;'
            f'font-family:monospace;color:#1a1a1a;">'
            f'<div style="font-weight:700;font-size:0.95em;">{_linha.codigo}</div>'
            f'<div style="font-size:0.85em;">{_linha.n_estrela:.2f}</div>'
            f"</div>"
            for _linha in _paises_zona.itertuples()
        )
        _linhas_html.append(
            f'<div style="margin-bottom:12px;">'
            f'<div style="font-size:0.85em;font-weight:600;margin-bottom:4px;">{_zona} ({len(_paises_zona)})</div>'
            f'<div style="display:flex;flex-wrap:wrap;gap:6px;">{_tiles}</div>'
            f"</div>"
        )
    st.markdown("".join(_linhas_html), unsafe_allow_html=True)
else:
    st.write("Dados insuficientes para montar a tabela geracional.")

# -----------------------------------------------------------------------
# Rodapé
# -----------------------------------------------------------------------

st.markdown("---")
st.markdown(
    "**Dados**: UN World Population Prospects + OECD Social Expenditure Database  \n"
    "**Metodologia**: Tese \"Do Dilema de Narayama ao Oicoceno Civilizacional\" v8.0  \n"
    "**Documentação**: [docs/definitions.md](../../docs/definitions.md)  \n"
    "**Versão pública**: [narayama.live](https://narayama.live)"
)
