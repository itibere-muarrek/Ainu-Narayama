# AINU.Systems — Observatório de Sustentabilidade Intergeracional

Cálculo do Índice de Narayama Sistêmico (N\*) para 30 economias, projeção de população por coorte e o Diretório
"Contas Nacionais por Nascimentos" (dados levantados e testados, e simulações como suposições para pesquisadores).

Implementação computacional da pesquisa independente "Do Dilema de Narayama ao Oicoceno Civilizacional" (V1_1,
Anexo 9 — PQDF-N\*). Definições: [`docs/definitions.md`](docs/definitions.md).

## O que o sistema publica

- **N\*_Obs** (valor observado, das fontes oficiais, sem ajustes): `N*_Obs = √(NGII_Obs × Fator_Geracional)`, com
  `NGII_Obs = (Pop_Base / Pop_Topo) × (Nascimentos / Mortes)`.
- **Cenários** separados (migração, inércia, políticas, sub-registro), só como referência.
- **Zonas provisórias**: o teste F4 do protocolo mostra ordenação estável, mas zona sensível a escolhas metodológicas
  ([`docs/testes_pqdf_n_estrela.md`](docs/testes_pqdf_n_estrela.md)).
- **Farol / Fator_Alocativo**: pendentes (dependem de National Transfer Accounts). Nenhum valor provisório é publicado.

## Plataformas

| Plataforma | Acesso | Conteúdo |
|---|---|---|
| `ainu.systems` (landing) e app `ainu-systems` | landing pública; app com login individual | 30 países, Tabela Geracional, Simulação, Consumo e Dividendo, Diretório |
| `narayama.live` (landing) e app `narayama-live` | público | países destaque (8 + 3 de exemplo) |

Interface em 9 idiomas (PT e EN são texto-fonte; ES, FR, IT, KO, JA, ZH e FI são traduções por IA, sem revisão nativa).

## Começar

```bash
pip install -r app/requirements.txt
python scripts/build_un_wpp_raw.py        # Pop_Base/Pop_Topo/Nasc/Mortes/TFR (UN WPP)
python scripts/build_migracao_raw.py      # estoque de migrantes (UN), referência do cenário migratório
python scripts/build_historico_raw.py     # série quinquenal 1990–2024
python scripts/build_convergencia_raw.py  # P_2.1/P_eq (Tabela Geracional)
```

```python
from src.data_pipeline import executar_pipeline_completo, executar_pipeline_historico
executar_pipeline_completo(2024)   # data/processed/n_index_2024.csv
executar_pipeline_historico()      # data/processed/n_index_historico.csv
```

```bash
streamlit run app/ainu_systems/app.py     # http://localhost:8501
streamlit run app/narayama_live/app.py    # http://localhost:8502
python scripts/testes_pqdf.py             # F1, F4 e parte de F5 do PQDF-N*
python test_projecao.py && python test_consumo_dividendo.py
```

Um workflow mensal (`.github/workflows/atualizar_dados.yml`) coleta os dados da ONU e abre um Pull Request se algo mudou;
nunca grava direto em `main`.

## Acesso ao app restrito

Logins **individuais**: a variável `AINU_USERS` (só no Render) guarda um JSON de *hashes* PBKDF2-SHA256, nunca senhas.
`python scripts/gerar_credenciais.py` gera os hashes e grava as senhas num arquivo fora do repositório, para entrega
individual por canal separado. O login do administrador usa `AINU_SYSTEMS_PASSWORD`. Páginas restritas ao administrador
(ex.: Compêndio) leem o conteúdo de um Secret File do Render, que não está neste repositório. Detalhes e limites em `src/auth.py`.

## Os dados deste repositório são públicos

O repositório é público. Os arquivos em `data/diretorio/publicavel/` (dados do Diretório, com fonte, nível e identificador de
evidência) podem ser lidos por qualquer pessoa; o login protege as páginas do app, não esses arquivos. Só entra neles o que
foi levantado e testado (natureza OBS/DER); estimativas, projeções e simulações ficam em área separada e rotuladas como
suposições para pesquisadores. Material de uso interno fica em `docs/privado/`, que o git ignora.

## Deploy

Render (`render.yaml`): serviços `ainu-systems`, `narayama-live` e as duas landings estáticas. Todo push em `main` redesploya.
`.github/workflows/ci.yml` valida configuração, cadeia de cálculo e série histórica antes do push chegar ao Render.
Variáveis secretas (`AINU_USERS`, `AINU_SYSTEMS_PASSWORD`, `AINU_LEGACY_USER`) são definidas só no painel do Render.

## Estrutura

- `src/` — cálculo (`indices.py`, `data_pipeline.py`, `projecao.py`), login, textos em 9 idiomas
- `scripts/` — coleta de dados e `scripts/diretorio/` (exportação, páginas, conferência de links, fontes e números)
- `app/ainu_systems/`, `app/narayama_live/` — apps Streamlit
- `landing/` — páginas estáticas e PDFs dos papers
- `data/raw/`, `data/processed/`, `data/diretorio/publicavel/` — dados
- `docs/` — definições, simulação, validação, testes do PQDF-N\*, infraestrutura

## Limites

Ver `docs/definitions.md` (seção 9) e `docs/testes_pqdf_n_estrela.md`: camada B e N\*_Estrutural não implementadas; testes F2, F3,
F6, F7, F8 e F9 não executados; farol sem dado; traduções sem revisão nativa.

## Licença

Fase de prototipagem de uma pesquisa independente em Economia Política, em andamento.

- Código-fonte: licença MIT (`LICENSE`).
- Dados derivados e documentação: CC BY 4.0 (`LICENSE-DATA.md`).
- Dados de terceiros (ONU, NTA, OCDE, OIT e outras fontes): termos de cada fonte, em `THIRD_PARTY_DATA.md`.
- Logotipos e identidade visual (AINU, Narayama): todos os direitos reservados.
- Como citar: `CITATION.cff`.
