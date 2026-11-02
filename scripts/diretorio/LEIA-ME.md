# Diretório do AINU.systems — fase 0

Exporta a planilha `Matrizes_Operacionais_NTA_URSS_Narayama_v2.xlsx` (Paper 3) para JSON em `data/diretorio/`
(ignorado pelo git até o autor liberar). Nada é publicado.

```
python scripts/diretorio/exportar_diretorio.py [caminho_da_planilha]
```

## Saída
- `privado/`: tudo, com `status_publicacao` por registro, auditoria interna e `relatorio_filtro.md`.
- `publicavel/`: só o que passa no filtro.
- Arquivos: `meta.json`, `paises.json` (11 fichas), `evidencias.json` (P1_Disponibilidade), `evidencias_citadas.json`
  (todos os IDs `AINU-ISO-TIPO-ANO-seq` encontrados nas abas), `instrumentos.json` (+ SOCX), `lacunas.json`, `glossario.json`.

## Filtro de auditoria
- Instrumentos: publicável só com fonte L1; "misto" (L1 + L2) sai como `publicavel_com_ressalva`; L2, fontes secundárias
  e nível indeterminado ficam retidos; status "A confirmar", "Lacuna" ou "n/d" viram lacuna.
- Evidências: A, L, P publicáveis; B retida (página não aberta); N vira lacuna.
- Fichas: campos que citam L2 saem retidos. **N\* consolidado fica de fora do público** até o N\*_Obs (PQDF-N\*) ser recalculado.
- `Auditoria_Pendencias` só no privado.
- `overrides_nivel.json`: decisões manuais de nível por instrumento (chave `ISO|nome do instrumento`), com motivo.

## Esquema (0.1.0)
Cada campo das fichas: `{texto, valor, natureza}` (+ `nivel`, `lacuna`, `retido`). Naturezas: OBS, DER, EST, PROJ, SIM,
PROP, ENTRADA (correspondência com [E], [S], [C], [H] da tese em `meta.json`).

## Termos
Descendentes (Prometidos), Estruturadores, Ascendentes (Legadores). Definições no `glossario.json`.

## Fase 1 — prévia privada das fichas (PT e EN)
```
python scripts/diretorio/gerar_fichas.py
```
Lê `data/diretorio/publicavel/` e grava HTML estático autônomo (CSS embutido) em `data/diretorio/preview/`
(ignorado pelo git): `pt/` e `en/` com `index.html` (comparação, legenda das naturezas, glossário) e uma ficha por país
(`ITA.html`, …). Todas as páginas têm `noindex` e faixa de prévia privada. Nada vai para `landing/` nem para o Render.
Rótulos e glossário estão traduzidos para EN; textos livres (instrumentos, fontes, lacunas) ficam no português original,
marcados com `lang="pt"` e avisados na página em inglês.
Abrir: `data/diretorio/preview/index.html`.

## Fase 2 — registro unificado de fontes
`exportar_diretorio.py` gera `fontes.json` (todos os IDs `AINU-…` citados nas abas, 624) com `origem`, `descricao`, `url`, `url_status`:
`registrado` (URL da planilha: P1_Disponibilidade, Inventario_Dados, ou derivada do código da série WDI/ILOSTAT/WPP), `nao_aplicavel`
(produto derivado da própria planilha) e `a_registrar`. As URLs que faltam estão em `privado/fontes_urls_pendentes.csv`; preencha em
`scripts/diretorio/fontes_urls_manual.json` (`{"ID": "https://…"}`) e rode de novo. As fichas ligam cada ID à URL quando existe.

## Fase 3 — simulações no app (atrás do login)
O exportador também grava `simulacoes.json` (em `privado/` e `publicavel/`): por país, o custo do Dividendo a 10% do gasto
(% do PIB, SIM), o maior programa infantil e o gasto público em família (% do PIB), o incremento por criança e as variações
por horizonte da aba P5. O conjunto publicável herda o filtro de auditoria (programa de nível L2 sai sem valor; programa
aproximado ou derivado leva `ressalva`). O exportador confere que a escala linear da página reproduz os 25% e 50% da planilha.

A página `app/ainu_systems/pages/2_Consumo_e_Dividendo.py` (só para usuários logados) lê `data/diretorio/publicavel/simulacoes.json`
e deixa mudar: a porcentagem do Dividendo (0 a 50%), o número de crianças adicionais e o deslocamento de outro consumo (0 a 100%),
e escolher o cenário de fecundidade. Cálculos em `src/consumo_dividendo.py` (testes: `python test_consumo_dividendo.py`),
textos PT/EN em `src/i18n_consumo.py` (demais línguas caem em PT). Nenhum modelo novo.

`data/diretorio/` está no .gitignore: sem o arquivo, a página avisa que os dados não foram liberados (é o que o Render mostrará
até o autor liberar). Para liberar, o autor decide se `simulacoes.json` entra no repositório.

## Contas Nacionais por Nascimentos (nome do Diretório, 2026-11-02)
O Diretório passou a se chamar **Contas Nacionais por Nascimentos** (EN: *National Accounts by Births*, tradução minha, a confirmar).
A prévia (`gerar_fichas.py`) agora tem um índice com três portas: **Países** (as 11 fichas), **Dados verificáveis** (`dados.html`: todos
os dados com fonte externa, com identificador, série, período, código de verificação e link para conferir, com filtro; hoje 566 itens,
512 com link e 54 a registrar, mais 59 produtos derivados sem fonte externa) e **Simulações** (`simulacoes.html`: resumo e tabela de
custo do Dividendo; a página interativa fica no app, atrás do login). Os links vêm do registro da pesquisa e ainda não foram testados
automaticamente.

### Teste dos links
`python scripts/diretorio/testar_links.py` testa cada endereço único de `fontes.json` (HEAD, ou GET sem baixar o corpo; 2 conexões por
servidor; identificação honesta; uma segunda tentativa nas falhas) e grava `privado/links_status.json`. Bloqueios e erros de certificado
não são contornados: ficam como "não confirmado". O teste só mostra que o endereço responde, não que o conteúdo é o dado citado.
Depois, rode `gerar_fichas.py` para a página de dados mostrar o resultado.

### Fontes e referências no rodapé (2026-11-02)
Todas as páginas da prévia têm, no rodapé, o bloco "Fontes e referências desta página": nas fichas, as fontes do país agrupadas (instrumentos,
pesquisas de orçamento, insumo-produto, ICIO, uso do tempo, NTA, WPP, OIT, WDI) mais as referências de método do país; nas demais páginas, o resumo
e a lista de referências de método. Cada fonte mostra o link, os identificadores, se o endereço abriu e se o assunto confere.
- `referencias_metodo.json`: fontes de método e de cálculo que não são séries da planilha (Frey e Osborne, OIT WP140, correspondência BLS, ILOSTAT
  por ocupação, Eurostat, SOCX).
- `conferir_fontes.py`: triagem automática de conteúdo (palavras da descrição na página; PDF pelas 3 primeiras páginas) → `privado/conferencia_fontes.*`.
- `conferencia_manual.json`: conferência feita à mão (assunto confirmado, ressalva, lida antes, não confirmada).
- `nomes_fontes.json`: nomes legíveis de fontes cujo texto original é genérico.
- A página do app (Consumo e Dividendo) tem o mesmo bloco, em um quadro "Fontes e referências desta página".

### Conferência de números (2026-11-02)
- `conferir_numeros.py`: triagem automática dos números dos instrumentos contra o texto das fontes (dígitos significativos, qualquer formato); resultado em
  `privado/conferencia_numeros.md`. Serve para achar candidatos à leitura manual: muitos números "não batem" porque o endereço registrado é uma página geral
  e não o documento (ex.: Treasury), ou porque o número é derivado.
- `conferencia_numeros_manual.json`: os números de maior peso conferidos à mão contra o original (Treasury, CFA, CNAF, INPS, OPC, 3º informe do México,
  HCES) e refeitos com o PIB do Banco Mundial; aparece em `dados.html`, seção "Números conferidos contra a fonte", com o estado de cada um.
