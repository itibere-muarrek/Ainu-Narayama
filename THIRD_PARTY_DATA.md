# Dados de terceiros: origem, licença e o que o repositório contém

Conferido em 14 de novembro de 2026. "Verificado" significa que li a declaração de licença da própria fonte ou de publicação oficial dela; o que não pude confirmar está marcado como pendente.

| Fonte | O que este repositório contém | Licença / termos | Situação e ação |
|---|---|---|---|
| ONU, DESA, Divisão de População. *World Population Prospects 2024* (variante média, idade simples) | `data/raw/un_wpp.csv`, `un_wpp_historico.csv`, `convergencia_un.csv`, `migracao_un.csv`; derivados em `data/processed/` | CC BY 3.0 IGO (declarada nas publicações da WPP; a página de termos de population.un.org não foi consultada diretamente) | Verificado nas publicações. Atribuir, indicar que os dados foram adaptados e não sugerir endosso da ONU |
| National Transfer Accounts (ntaccounts.org) | `data/raw/nta_perfis_C_YL_S.csv` (perfis por idade de consumo, renda do trabalho e poupança de 11 países) | Nenhuma licença de redistribuição identificada. O portal pede que se cite o site com a data de acesso e que se compartilhe a pesquisa que usa os dados | **Pendente.** Pedido de autorização escrita à coordenação da rede NTA preparado. Enquanto não houver resposta, o arquivo está excluído dos pacotes de release (`.gitattributes`) e o download no portal está documentado em `docs/nta_perfis_fonte.md`. Resultados derivados (participações por coorte) permanecem, com atribuição |
| OCDE, *Inter-Country Input-Output Database* (ICIO) | Nenhum arquivo bruto; apenas valores derivados nas fichas | Padrão da OCDE: CC BY 4.0 para conteúdo publicado desde 1 de julho de 2024; licença específica do ICIO não confirmada | Não redistribuir os arquivos brutos. Citar OECD (2023) e Yamano et al. (2023) |
| OIT, ILOSTAT | Nenhum arquivo bruto; apenas valores derivados | CC BY 4.0 para bases publicadas a partir de 3 de maio de 2023 (página de direitos da OIT); anteriores, verificar caso a caso | Atribuir a OIT como fonte |
| CCP-UCR, Cuentas Nacionales de Transferencias de Costa Rica | Nenhum (só nas análises do autor) | A página de download não traz texto de licença; direitos da Universidad de Costa Rica | Não redistribuir; citar a fonte e o arquivo |
| Institutos nacionais e outras bases citadas nas fichas (ISTAT, INEC, KOSTAT, Eurostat, BEA, BLS, IBGE, INDEC, INEGI, Banca d'Italia) | Apenas valores pontuais e links, com a fonte indicada; nenhum microdado | Termos de cada instituição não verificados | Citar; não incluir microdados sem verificar os termos |

Regras gerais deste repositório:
1. Nenhum arquivo bruto de terceiros é adicionado sem a licença verificada e registrada nesta tabela.
2. Todo valor exibido tem a fonte indicada (ver `data/diretorio/publicavel/fontes.json`).
3. Esta tabela deve ser atualizada a cada nova fonte.
