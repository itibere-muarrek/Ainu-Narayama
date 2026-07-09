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

from src.config import DATA_PROCESSED_DIR, DOCS_DIR, LIMIARES_SIMPLES_NORMALIZADOS, LIMIAR_PEEC_TFR, PAISES
from src.indices import classificar_zona_n_base

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

    if "n_base" in df.columns:
        df["zona"] = df["n_base"].apply(classificar_zona_n_base)

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
    contagem_zonas = df["zona"].value_counts()
    st.sidebar.markdown("**Países por zona de N\\*:**")
    for zona in ["Colapso de Narayama (PEC)", "Tensão Acelerada", "Equilíbrio Sustentável (PEA)", "Expansão Forte"]:
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
        """Vermelho = Colapso (PEC), amarelo = Tensão Acelerada, verde = PEA/Expansão Forte."""
        n_estrela = linha.get("N*")
        if n_estrela is None or pd.isna(n_estrela):
            cor = ""
        elif n_estrela < LIMIARES_SIMPLES_NORMALIZADOS["pec"]:
            cor = "background-color: #f8d7da"  # vermelho claro
        elif n_estrela < LIMIARES_SIMPLES_NORMALIZADOS["pea"]:
            cor = "background-color: #fff3cd"  # amarelo claro
        else:
            cor = "background-color: #d4edda"  # verde claro
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
# Rodapé
# -----------------------------------------------------------------------

st.markdown("---")
st.markdown(
    "**Dados**: UN World Population Prospects + OECD Social Expenditure Database  \n"
    "**Metodologia**: Tese \"Do Dilema de Narayama ao Oicoceno Civilizacional\" v8.0  \n"
    "**Documentação**: [docs/definitions.md](../../docs/definitions.md)  \n"
    "**Versão pública**: [narayama.live](https://narayama.live)"
)
