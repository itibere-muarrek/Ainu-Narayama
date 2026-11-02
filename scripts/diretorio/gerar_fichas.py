"""Fase 1 do Diretório do AINU.systems: gera a PRÉVIA PRIVADA das fichas (PT e EN).

Lê data/diretorio/publicavel/*.json (saída de exportar_diretorio.py) e grava HTML
estático em data/diretorio/preview/ (ignorado pelo git). As páginas levam
noindex e uma faixa de "prévia privada"; nada vai para landing/ nem para o Render.

Uso:
    python scripts/diretorio/gerar_fichas.py
"""
from __future__ import annotations

import html
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DADOS = RAIZ / "data" / "diretorio" / "publicavel"
PREVIA = RAIZ / "data" / "diretorio" / "preview"
LOGO = RAIZ / "landing" / "ainu-systems" / "Ainu-transparente.png"

PAISES_EN = {"Itália": "Italy", "Coreia do Sul": "South Korea", "Japão": "Japan", "México": "Mexico", "Argentina": "Argentina",
             "Brasil": "Brazil", "Estados Unidos": "United States", "Índia": "India", "Nigéria": "Nigeria", "França": "France",
             "China": "China"}
ZONAS_EN = {}

T = {  # textos de interface
    "pt": {
        "titulo": "Contas Nacionais por Nascimentos", "sub": "Diretório de países: NTA, URSS e sustentabilidade econômica intergeracional",
        "nav_paises": "Países", "nav_dados": "Dados verificáveis", "nav_sim": "Simulações",
        "hub_paises": "Países", "hub_paises_d": "Onze fichas com demografia, consumo por coorte, produção e emprego, instrumentos e lacunas.",
        "hub_dados": "Dados verificáveis", "hub_dados_d": "Cada dado com seu identificador, a fonte, o período e o link para conferir no original.",
        "hub_sim": "Simulações", "hub_sim_d": "Custo do Dividendo Intergeracional, efeito de crianças adicionais e cenários de fecundidade.",
        "d_titulo": "Dados verificáveis", "d_intro": "Lista de todos os dados do Diretório que têm fonte externa, com o link para conferir. O código de verificação diz o que foi feito com a fonte (legenda abaixo); o identificador liga cada número das fichas à sua fonte.",
        "d_filtro": "Filtrar por país, fonte ou identificador", "d_global": "Global / vários países",
        "d_resumo_total": "dados com fonte externa", "d_resumo_link": "com link para conferir", "d_resumo_sem": "link ainda a registrar", "d_resumo_der": "produtos derivados do próprio estudo (sem fonte externa)",
        "d_col_pais": "País", "d_col_dado": "Dado e fonte", "d_col_serie": "Série", "d_col_per": "Período", "d_col_verif": "Verificação", "d_col_link": "Conferir",
        "d_conferir": "abrir fonte ↗", "d_sem_link": "link a registrar", "d_leg": "Legenda da verificação",
        "n_titulo": "Números conferidos contra a fonte", "n_intro": "Conferência dos números de maior peso, feita em {data}: o número da pesquisa foi comparado com o texto da fonte e, nos percentuais do PIB, refeito com o PIB do Banco Mundial. Itens que não deu para conferir ficam marcados.",
        "n_col_item": "Número", "n_col_fonte": "Fonte", "n_col_estado": "Resultado", "n_col_nota": "O que foi conferido",
        "n_confere": "confere", "n_confere_parcial": "confere em parte", "n_nao_conferido": "não conferido",
        "f_titulo": "Fontes e referências desta página", "f_refs": "Referências de método e de cálculo",
        "f_intro": "Cada fonte tem o link para conferir, o identificador que a liga aos números da página e o resultado da conferência feita em {data}: se o endereço abriu e se o assunto da página confere com o que a fonte cita. A conferência confirma o assunto, não cada número; a curadoria das referências teóricas segue pendente.",
        "f_g_wdi": "Banco Mundial, WDI (séries)", "f_g_oit": "OIT, ILOSTAT (séries)", "f_g_onu": "ONU, World Population Prospects", "f_g_nta": "National Transfer Accounts",
        "f_g_icio": "OCDE, matriz multirregional (ICIO)", "f_g_tus": "Pesquisas de uso do tempo", "f_g_hbs": "Pesquisas de orçamento familiar", "f_g_io": "Tabelas de insumo-produto",
        "f_g_instr": "Instrumentos de política e programas (documentos oficiais)", "f_g_pesq": "Pesquisas e microdados usados nos cálculos",
        "f_abriu": "abriu", "f_redir": "abriu (mudou de endereço)", "f_bloq": "servidor recusa acesso automático", "f_naoenc": "não encontrado", "f_sem": "sem resposta no teste", "f_erro": "erro do servidor", "f_nt": "não testado",
        "f_confere": "assunto conferido", "f_confere_auto": "assunto conferido (automático)", "f_ressalva": "ressalva", "f_lida": "lida antes", "f_nao_conf": "não confirmada", "f_revisar": "conteúdo a revisar", "f_nv": "conteúdo não verificado automaticamente",
        "f_sem_link": "link a registrar", "f_ids": "identificadores", "f_calculo": "Cálculos do autor (Paper 3, planilha Matrizes_Operacionais_NTA_URSS_Narayama_v2; rascunho não revisado).",
        "f_global_n": "fonte(s)", "f_ver_dados": "Lista completa, com filtro: Dados verificáveis.",
        "l_ok": "abriu no teste", "l_redirecionado": "abriu (mudou de endereço)", "l_bloqueado": "servidor recusa robôs; abra no navegador", "l_nao_encontrado": "não encontrado (404)",
        "l_erro_servidor": "erro do servidor no teste", "l_sem_resposta": "não respondeu no teste; tente no navegador", "l_nao_testado": "não testado",
        "l_resumo": "endereços únicos testados em", "l_ok_n": "abriram", "l_prob_n": "não confirmados (recusa de robôs, sem resposta ou erro)",
        "d_nota": "Os links vêm do registro da pesquisa; o teste automático só confirma que o endereço responde, não que o conteúdo é o dado citado. Fontes oficiais mudam de endereço, e um link que não abre deve ser avisado ao autor. Dados marcados B (resultado de busca, página não aberta) não entram aqui. Os produtos derivados (cálculos do próprio estudo) têm identificador na planilha, mas não têm link externo.",
        "s_titulo": "Simulações", "s_intro": "As simulações interativas ficam no app do ainu.systems, atrás de login (menu «Consumo e Dividendo»). Elas escalam números que o Paper 3 já calculou; não há modelo novo, previsão nem estimativa de efeito causal. Esta página resume o que há lá.",
        "s_l1": "Dividendo Intergeracional: escolha x% (0 a 50) do gasto privado por Descendente e veja o custo em % do PIB, comparado ao maior programa infantil de renda e ao gasto público em família.",
        "s_l2": "Criança adicional: escolha o número de crianças e a parcela do gasto que desloca outro consumo; veja consumo, valor adicionado e empregos sustentados (limite superior, por ano).",
        "s_l3": "Cenários de fecundidade: variação de Descendentes, Estruturadores, Ascendentes e consumo por horizonte, em relação à continuidade da TFT.",
        "s_tab": "Custo do Dividendo (% do PIB) por país", "s_col10": "10% do gasto", "s_col25": "25%", "s_col50": "50%", "s_colprog": "Maior programa infantil (% do PIB)", "s_colrazao": "Dividendo 10% ÷ programa",
        "s_nota_tab": "Custo proporcional a x; os 25% e 50% reproduzem a planilha do Paper 3. Programas de nível L2 ficam sem valor; os marcados com ≈ são aproximados ou derivados.",
        "s_acesso": "Acesso: faça login no app do ainu.systems e abra «Consumo e Dividendo». Nesta prévia privada a página interativa não está embutida.",
        "banner": "PRÉVIA PRIVADA: conteúdo em auditoria, não publicado. Não compartilhe este endereço.",
        "voltar": "Todos os países", "idioma": "English",
        "intro": "Onze países, uma mesma metodologia e a fonte de cada número. Os dados vêm da planilha de pesquisa do Paper 3 e passam por um filtro de auditoria: só entra o que foi conferido em documento original (nível L1); o que ainda não foi conferido aparece como lacuna ou em confirmação.",
        "aviso_cortes": "Os cortes de idade das coortes são próprios de cada país (ver cada ficha); por isso as participações não são comparáveis ponto a ponto.",
        "aviso_nstar": "O N* (Índice de Narayama) está em recálculo conforme o PQDF-N* e não é exibido nesta prévia.",
        "aviso_indep": "Pesquisa independente (AINU.Systems / Narayama). Nenhum resultado aqui estima efeito causal de política.",
        "aviso_texto_pt": "Os textos livres vêm do original em português.",
        "tabela": "Comparação", "legenda": "Natureza de cada dado",
        "classe": "Classe de cobertura", "classes": {"1": "1 · análise completa", "2": "2 · análise parcial", "3": "3 · comparação contextual"},
        "coortes": "Coortes (idades)", "demografia": "Demografia e carga por coorte", "consumo": "Consumo por coorte",
        "multiplicadores": "Produção e emprego", "valorizacao": "Valorização", "cobertura": "Dados e método",
        "instrumentos": "Instrumentos oficiais", "lacunas": "Lacunas", "fontes": "Fontes de dados", "glossario": "Glossário",
        "ind": "Indicador", "valor": "Valor", "nat": "Natureza", "nivel": "Nível da fonte", "custo": "Custo fiscal",
        "em_conf": "em confirmação", "np": "não pesquisado", "nd": "n/d", "anos": "anos", "n_evid": "registros de evidência verificados",
        "nota_demog": "Projeção condicional a cenário, com consumo por pessoa constante: não é previsão.",
        "nota_consumo": "O peso dos Descendentes no consumo privado depende da ancoragem aos pesos NTA; sem ela, a regressão dá 6% a 8%.",
        "nota_valor": "Simulação de custo (Dividendo Intergeracional): não estima efeito nem recomenda desenho.",
        "id": "ID", "variavel": "Variável", "fonte": "Fonte", "serie": "Série", "periodo": "Período", "verif": "Verificação",
        "ressalva": "Parte deste registro (marcada no texto como L2) vem de resumo de busca e não foi conferida no documento original.",
        "incr_titulo": "Incremento por nova criança",
        "incr_nota": "Valor por criança adicional e por ano em que ela permanece na coorte de Descendentes, em demanda de consumo privado e público. Os empregos são os que essa demanda sustenta na economia (diretos e indiretos, líquidos de importações), não os da criança.",
        "incr_emp": "Empregos brutos por criança", "incr_equiv": "≈ 1 emprego para cada {n} crianças", "incr_faixa": "faixa entre cenários",
        "incr_liq": "Empregos líquidos por criança se metade do gasto deslocar outro consumo", "incr_vad": "Valor adicionado por criança por ano",
        "incr_razao": "Valor adicionado ÷ consumo atribuído à criança", "incr_nd": "Não calculado nesta rodada: sem tabela de insumo-produto.",
        "incr_lim": ["Limite superior de demanda: supõe que todo o gasto adicional é novo; o deslocamento de 50% é parâmetro de sensibilidade, não estimativa.",
                     "Usa o consumo médio por Descendente; o custo marginal de um filho a mais pode ser menor (economias de escala no domicílio).",
                     "Depende da ancoragem do consumo infantil aos pesos NTA; sem ela, o peso dos Descendentes no consumo privado cai para 6% a 8%.",
                     "Ordem de grandeza: os valores monetários aparecem com dois algarismos significativos, porque as abas de cenários de origem têm valores arredondados.",
                     "É um valor por ano: não acumula os anos de cada criança nem desconta valores, e não inclui a produção futura da criança como trabalhadora e contribuinte nem o financiamento do gasto público."],
        "incr_col": "Empregos por criança", "n_pontos": "cenários",
        "grp_titulo": "Para onde vai o consumo de crianças e de idosos",
        "grp_nota": "Composição do gasto privado por grupo de atividade (em % do gasto de cada coorte). Dois olhares: o gasto marginal (o que mais uma pessoa da coorte acrescenta ao gasto do domicílio) e o gasto médio (divisão igual do gasto do domicílio entre os membros). O gasto real fica entre os dois.",
        "grp_grupo": "Grupo de atividade", "grp_desc": "Descendentes", "grp_asc": "Ascendentes", "grp_marg": "marginal", "grp_med": "médio",
        "grp_sobre": "Sobreposição entre crianças e idosos (0 a 1)", "grp_cobre": "Parcela do gasto total coberta pelos grupos",
        "mul_titulo": "Quanto valor adicionado e emprego cada grupo sustenta",
        "mul_nota": "Multiplicadores da tabela de insumo-produto do país: valor adicionado doméstico e empregos por unidade de gasto das famílias em cada grupo, e quanto cada grupo representa no valor adicionado que a demanda de uma criança e a de um idoso sustentam.",
        "mul_vad": "Valor adicionado por unidade de gasto", "mul_emp": "Empregos por milhão de moeda local", "mul_d": "Parcela do valor adicionado da criança (%)", "mul_a": "Parcela do valor adicionado do idoso (%)",
        "mul_aviso_set": "O emprego por grupo vem das seções ISIC da OIT (20 seções): separa, por exemplo, educação de finanças, mas produtos da mesma seção têm a mesma intensidade, e o trabalho informal pode estar subestimado nos grupos de bens.",
        "mul_aviso_a64": "O emprego por grupo vem das atividades A64 do Eurostat (64 atividades), mais finas que as seções ISIC.",
        "mul_aviso_prod": "O emprego por grupo vem dos postos de trabalho por produto da própria tabela de insumo-produto; conferido com as seções ISIC da OIT, que dão resultado próximo na maioria dos grupos.",
        "mul_lim": ["Multiplicadores de um ano-base, aplicados a composições de gasto de outros anos; só gasto privado, sem aluguel imputado.",
                    "Os grupos são grupos de demanda; o mapa de produtos para grupos é decisão de classificação (nos EUA os farmacêuticos ficam em cuidados pessoais e outros bens, não em saúde).",
                    "Moedas e anos diferentes por país: compare as participações e a ordem dos grupos, não os valores de emprego entre países."],
        "iag_titulo": "Exposição à IA generativa (base de referência)", "iag_ref": "Ver a base de referência: ainda não sustenta resultados do texto principal",
        "iag_nota": "Escore médio de exposição à IA generativa das ocupações (índice da OIT, 2025), ponderado como acima. Indica sobretudo transformação de tarefas, não previsão de perda de emprego. As duas medidas dão ordens quase opostas: a automação atinge mais as ocupações rotineiras e manuais, a IA generativa as de escritório e profissionais.",
        "iag_media": "Escore médio (faixa)", "iag_alta": "Fração de ocupações nos gradientes 3 e 4 (mais expostas)",
        "iag_lim": ["Escore global da OIT para ocupações ISCO-08, sem ajuste por país; médias de grande grupo sem pesos de emprego, daí a faixa.",
                    "Alimentos e bebidas e vestuário estão entre os menos expostos à IA generativa (cuidados pessoais também, fora dos EUA); educação e saúde, entre os mais expostos, o oposto do resultado com a automação. Nenhum grupo é pouco exposto nas duas medidas ao mesmo tempo.",
                    "A OIT enfatiza que exposição indica transformação das ocupações, porque a maioria combina tarefas que exigem trabalho humano."],
        "exp_titulo": "Exposição à automação do emprego de cada grupo",
        "exp_nota": "Probabilidade média de informatização das ocupações (Frey e Osborne, 2013), ponderada pela composição ocupacional de cada setor e pelo emprego que o gasto do grupo sustenta. É exposição técnica das tarefas, não previsão de perda de emprego. A faixa usa o quartil inferior e o superior das ocupações dentro de cada grande grupo ocupacional.",
        "exp_media": "Probabilidade média (faixa)", "exp_alta": "Fração de ocupações com probabilidade acima de 0,7",
        "exp_coorte": "Exposição média do emprego sustentado por uma criança e por um idoso", "exp_c": "Criança, gasto marginal / médio", "exp_i": "Idoso, gasto marginal / médio",
        "exp_lim": ["Ocupações e escores são dos EUA em 2013, aplicados a outros países pelo cruzamento SOC-ISCO do BLS; a IA generativa (OIT, 2025) vem na seção seguinte.",
                    "Os grandes grupos ocupacionais são médias sem pesos de emprego e a dispersão dentro deles é grande; por isso a faixa.",
                    "A educação é o grupo menos exposto nos quatro países e a saúde vem em seguida; alimentos e bebidas ficam entre os mais expostos, porque as ocupações agropecuárias e de operação de máquinas têm escores altos. O argumento da tese para a agricultura familiar é a escala, que um escore por ocupação não mede."],
        "co_titulo": "Consumo observado: relatório do HCES 2023-24 (Índia)",
        "co_nota": "Valores lidos no relatório oficial (MoSPI, NSS Report nº 592), em rúpias correntes por pessoa e por mês. As médias usam toda a população; os grupos são os do relatório e não os 8 grupos do Paper 3. O relatório não traz idade nem composição por coorte, que dependem do microdado.",
        "co_ind": "Indicador", "co_rural": "Rural", "co_urbano": "Urbano", "co_grupo": "Grupo de itens", "co_pct": "% do gasto",
        "grp_nd": "Não calculado nesta rodada: sem microdados de orçamento familiar harmonizados.",
        "grp_nd_ita": "Não calculado nesta rodada.",
        "exp_nd_ita": "Ainda não calculado para a Itália: falta baixar da OIT o emprego por atividade e ocupação do país e ligar as atividades do Eurostat às seções ISIC.",
        "ita_nota": "Itália: a ISTAT HBS 2023 (arquivo público) traz só classes de idade, então Descendentes são os menores de 18 anos, Estruturadores de 18 a 64 e Ascendentes de 65 em diante; e a habitação inclui o aluguel imputado, ao contrário dos outros países. Multiplicadores e emprego vêm da tabela simétrica do Eurostat de 2022 e das atividades A64.",
        "grp_lim": ["São grupos de demanda (o que se consome), não setores de oferta; a correspondência com as atividades da tese (alimentos locais, energia regional, cadeias curtas, educação articulada à pesquisa) é hipótese, não medida.",
                    "Só gasto privado das famílias, sem aluguel imputado; educação e saúde públicas ficam de fora.",
                    "Zeros no gasto marginal significam gasto não distinguível de zero, não ausência de consumo.",
                    "A sobreposição mostra quanto a demanda de crianças e de idosos se dirige aos mesmos grupos; não mede convivência."],
        "sem_instr": "Nenhum instrumento publicável nesta rodada.", "sem_lac": "Sem lacunas registradas.",
        "rodape": "Pesquisa independente. Dados e método rastreáveis por ID de evidência. Prévia gerada em",
        "ver_site": "ainu.systems",
    },
    "en": {
        "titulo": "National Accounts by Births", "sub": "Country directory: NTA, URSS and intergenerational economic sustainability",
        "nav_paises": "Countries", "nav_dados": "Verifiable data", "nav_sim": "Simulations",
        "hub_paises": "Countries", "hub_paises_d": "Eleven country pages with demography, cohort consumption, output and jobs, instruments and gaps.",
        "hub_dados": "Verifiable data", "hub_dados_d": "Every data point with its identifier, source, period and a link to check it at the original.",
        "hub_sim": "Simulations", "hub_sim_d": "Cost of the Intergenerational Dividend, effect of additional children and fertility scenarios.",
        "d_titulo": "Verifiable data", "d_intro": "List of all Directory data that has an external source, with a link to check it. The verification code says what was done with the source (legend below); the identifier ties each number on the country pages to its source.",
        "d_filtro": "Filter by country, source or identifier", "d_global": "Global / several countries",
        "d_resumo_total": "data points with an external source", "d_resumo_link": "with a link to check", "d_resumo_sem": "link still to be registered", "d_resumo_der": "products derived from the study itself (no external source)",
        "d_col_pais": "Country", "d_col_dado": "Data and source", "d_col_serie": "Series", "d_col_per": "Period", "d_col_verif": "Verification", "d_col_link": "Check",
        "d_conferir": "open source ↗", "d_sem_link": "link to be registered", "d_leg": "Verification legend",
        "n_titulo": "Numbers checked against the source", "n_intro": "Check of the most important numbers, made on {data}: the research number was compared with the source text and, for percentages of GDP, recomputed with World Bank GDP. Items that could not be checked are marked.",
        "n_col_item": "Number", "n_col_fonte": "Source", "n_col_estado": "Result", "n_col_nota": "What was checked",
        "n_confere": "matches", "n_confere_parcial": "partly matches", "n_nao_conferido": "not checked",
        "f_titulo": "Sources and references for this page", "f_refs": "Method and calculation references",
        "f_intro": "Each source has a link to check it, the identifier tying it to the numbers on the page, and the result of the check made on {data}: whether the address opened and whether the page's subject matches what the source is cited for. The check confirms the subject, not each number; curation of theoretical references is still pending.",
        "f_g_wdi": "World Bank, WDI (series)", "f_g_oit": "ILO, ILOSTAT (series)", "f_g_onu": "UN, World Population Prospects", "f_g_nta": "National Transfer Accounts",
        "f_g_icio": "OECD multiregional table (ICIO)", "f_g_tus": "Time use surveys", "f_g_hbs": "Household budget surveys", "f_g_io": "Input-output tables",
        "f_g_instr": "Policy instruments and programmes (official documents)", "f_g_pesq": "Surveys and microdata used in the calculations",
        "f_abriu": "opened", "f_redir": "opened (address changed)", "f_bloq": "server refuses automated access", "f_naoenc": "not found", "f_sem": "no response in the test", "f_erro": "server error", "f_nt": "not tested",
        "f_confere": "subject checked", "f_confere_auto": "subject checked (automatic)", "f_ressalva": "caveat", "f_lida": "read earlier", "f_nao_conf": "not confirmed", "f_revisar": "content to review", "f_nv": "content not verified automatically",
        "f_sem_link": "link to be registered", "f_ids": "identifiers", "f_calculo": "Author's calculations (Paper 3, workbook Matrizes_Operacionais_NTA_URSS_Narayama_v2; unreviewed draft).",
        "f_global_n": "source(s)", "f_ver_dados": "Full list, with filter: Verifiable data.",
        "l_ok": "opened in the test", "l_redirecionado": "opened (address changed)", "l_bloqueado": "server refuses robots; open in a browser", "l_nao_encontrado": "not found (404)",
        "l_erro_servidor": "server error in the test", "l_sem_resposta": "no response in the test; try in a browser", "l_nao_testado": "not tested",
        "l_resumo": "unique addresses tested on", "l_ok_n": "opened", "l_prob_n": "not confirmed (robot refusal, no response or error)",
        "d_nota": "The links come from the research record; the automatic test only confirms the address responds, not that the content is the cited data. Official sources change address, so tell the author if one does not open. Items marked B (search result, page not opened) are not listed. Derived products (the study's own calculations) have an identifier in the workbook but no external link.",
        "s_titulo": "Simulations", "s_intro": "The interactive simulations live in the ainu.systems app, behind login (menu «Consumo e Dividendo»). They rescale numbers Paper 3 has already computed; there is no new model, forecast or causal effect estimate. This page summarises what is there.",
        "s_l1": "Intergenerational Dividend: pick x% (0 to 50) of private spending per Descendente and see the cost as % of GDP, compared with the largest child cash programme and with public family spending.",
        "s_l2": "Additional child: pick the number of children and the share of spending that displaces other consumption; see the consumption, value added and jobs sustained (upper bound, per year).",
        "s_l3": "Fertility scenarios: change in Descendentes, Estruturadores, Ascendentes and consumption by horizon, relative to a constant TFR.",
        "s_tab": "Dividend cost (% of GDP) by country", "s_col10": "10% of spending", "s_col25": "25%", "s_col50": "50%", "s_colprog": "Largest child programme (% of GDP)", "s_colrazao": "10% Dividend ÷ programme",
        "s_nota_tab": "Cost is proportional to x; 25% and 50% reproduce the Paper 3 workbook. Level L2 programmes show no value; those marked ≈ are approximate or derived.",
        "s_acesso": "Access: sign in to the ainu.systems app and open «Consumo e Dividendo». In this private preview the interactive page is not embedded.",
        "banner": "PRIVATE PREVIEW: content under audit, not published. Do not share this address.",
        "voltar": "All countries", "idioma": "Português",
        "intro": "Eleven countries, one methodology, and the source of every number. Data come from the Paper 3 research workbook and go through an audit filter: only what was checked against an original document (level L1) is shown; anything not yet checked appears as a gap or as pending confirmation.",
        "aviso_cortes": "Cohort age cutoffs are specific to each country (see each profile), so shares are not comparable point by point.",
        "aviso_nstar": "The N* (Narayama Index) is being recalculated under the PQDF-N* and is not shown in this preview.",
        "aviso_indep": "Independent research (AINU.Systems / Narayama). Nothing here estimates a causal policy effect.",
        "aviso_texto_pt": "Free-text fields are shown in the original Portuguese.",
        "tabela": "Comparison", "legenda": "Nature of each datum",
        "classe": "Coverage class", "classes": {"1": "1 · full analysis", "2": "2 · partial analysis", "3": "3 · contextual comparison"},
        "coortes": "Cohorts (ages)", "demografia": "Demography and cohort burden", "consumo": "Consumption by cohort",
        "multiplicadores": "Production and employment", "valorizacao": "Valorization", "cobertura": "Data and method",
        "instrumentos": "Official instruments", "lacunas": "Gaps", "fontes": "Data sources", "glossario": "Glossary",
        "ind": "Indicator", "valor": "Value", "nat": "Nature", "nivel": "Source level", "custo": "Fiscal cost",
        "em_conf": "pending confirmation", "np": "not researched", "nd": "n/a", "anos": "years", "n_evid": "verified evidence records",
        "nota_demog": "Scenario-conditional projection with constant per-person consumption: not a forecast.",
        "nota_consumo": "The weight of Descendants in private consumption depends on anchoring to NTA weights; without it the regression gives 6% to 8%.",
        "nota_valor": "Cost simulation (Intergenerational Dividend): it does not estimate effects or recommend a design.",
        "id": "ID", "variavel": "Variable", "fonte": "Source", "serie": "Series", "periodo": "Period", "verif": "Verification",
        "ressalva": "Part of this record (marked in the text as L2) comes from a search summary and was not checked against the original document.",
        "incr_titulo": "Increment per additional child",
        "incr_nota": "Value per additional child and per year in which the child stays in the Descendants cohort, in private and public consumption demand. The jobs are those that this demand sustains in the economy (direct and indirect, net of imports), not the child's own.",
        "incr_emp": "Gross jobs per child", "incr_equiv": "≈ 1 job for every {n} children", "incr_faixa": "range across scenarios",
        "incr_liq": "Net jobs per child if half of the spending displaces other consumption", "incr_vad": "Value added per child per year",
        "incr_razao": "Value added ÷ consumption attributed to the child", "incr_nd": "Not calculated in this round: no input-output table.",
        "incr_lim": ["Upper bound on demand: assumes all additional spending is new; the 50% displacement is a sensitivity parameter, not an estimate.",
                     "Uses average consumption per Descendant; the marginal cost of one more child may be lower (household economies of scale).",
                     "Depends on anchoring child consumption to NTA weights; without it, the Descendants' weight in private consumption falls to 6% to 8%.",
                     "Order of magnitude: monetary values are shown with two significant figures, because the source scenario sheets hold rounded values.",
                     "It is a per-year value: it does not accumulate each child's years or discount, and it excludes the child's future output as a worker and taxpayer and the financing of public spending."],
        "incr_col": "Jobs per child", "n_pontos": "scenarios",
        "grp_titulo": "Where children's and older people's consumption goes",
        "grp_nota": "Composition of private spending by activity group (in % of each cohort's spending). Two views: marginal spending (what one more person in the cohort adds to household spending) and average spending (household spending split equally among members). Actual spending lies between the two.",
        "grp_grupo": "Activity group", "grp_desc": "Descendants", "grp_asc": "Ascendants", "grp_marg": "marginal", "grp_med": "average",
        "grp_sobre": "Overlap between children and older people (0 to 1)", "grp_cobre": "Share of total spending covered by the groups",
        "mul_titulo": "How much value added and employment each group sustains",
        "mul_nota": "Multipliers from the country's input-output table: domestic value added and jobs per unit of household spending in each group, and how much each group represents in the value added sustained by a child's and an older person's demand.",
        "mul_vad": "Value added per unit of spending", "mul_emp": "Jobs per million local currency", "mul_d": "Share of the child's value added (%)", "mul_a": "Share of the older person's value added (%)",
        "mul_aviso_set": "Employment by group comes from ILO ISIC sections (20 sections): it separates, for example, education from finance, but products in the same section share the same intensity, and informal work may be understated in goods groups.",
        "mul_aviso_a64": "Employment by group comes from Eurostat A64 activities (64 activities), finer than ISIC sections.",
        "mul_aviso_prod": "Employment by group comes from jobs by product in the country's own input-output table; checked against ILO ISIC sections, which give a close result for most groups.",
        "mul_lim": ["Multipliers for one base year, applied to spending compositions from other years; private spending only, excluding imputed rent.",
                    "Groups are demand groups; the product-to-group map is a classification decision (in the US pharmaceuticals sit in personal care and other goods, not in health).",
                    "Different currencies and years by country: compare shares and the ordering of groups, not employment values across countries."],
        "iag_titulo": "Generative AI exposure (reference base)", "iag_ref": "Show the reference base: it does not yet support results in the main text",
        "iag_nota": "Average generative AI exposure score of occupations (ILO index, 2025), weighted as above. It mainly indicates task transformation, not a forecast of job loss. The two measures give almost opposite orderings: automation hits routine and manual occupations more, generative AI hits clerical and professional ones.",
        "iag_media": "Average score (range)", "iag_alta": "Share of occupations in gradients 3 and 4 (most exposed)",
        "iag_lim": ["Global ILO score for ISCO-08 occupations, with no country adjustment; major-group averages are unweighted by employment, hence the range.",
                    "Food and beverages and clothing are among the least exposed to generative AI (personal care too, outside the US); education and health are among the most exposed, the opposite of the automation result. No group is lightly exposed on both measures at once.",
                    "The ILO stresses that exposure indicates occupational transformation, since most occupations combine tasks that need human work."],
        "exp_titulo": "Automation exposure of each group's employment",
        "exp_nota": "Average probability of computerisation of occupations (Frey and Osborne, 2013), weighted by each sector's occupational composition and by the employment that the group's spending sustains. It is technical exposure of tasks, not a forecast of job loss. The range uses the lower and upper quartiles of occupations within each major occupational group.",
        "exp_media": "Average probability (range)", "exp_alta": "Share of occupations with probability above 0.7",
        "exp_coorte": "Average exposure of the employment sustained by a child and by an older person", "exp_c": "Child, marginal / average spending", "exp_i": "Older person, marginal / average spending",
        "exp_lim": ["Occupations and scores are for the US in 2013, applied to other countries through the BLS SOC-ISCO crosswalk; generative AI (ILO, 2025) follows in the next section.",
                    "Major occupational groups are unweighted averages and dispersion within them is large; hence the range.",
                    "Education is the least exposed group in all four countries and health comes next; food and beverages are among the most exposed, because agricultural and machine-operation occupations have high scores. The thesis's argument for family farming is scale, which an occupation score does not measure."],
        "co_titulo": "Observed consumption: HCES 2023-24 report (India)",
        "co_nota": "Values read from the official report (MoSPI, NSS Report no. 592), in current rupees per person per month. Averages use the whole population; the groups are the report's own, not the Paper 3 eight groups. The report has no age or cohort breakdown, which depends on the microdata.",
        "co_ind": "Indicator", "co_rural": "Rural", "co_urbano": "Urban", "co_grupo": "Item group", "co_pct": "% of spending",
        "grp_nd": "Not calculated in this round: no harmonized household budget microdata.",
        "grp_nd_ita": "Not calculated in this round.",
        "exp_nd_ita": "Not yet calculated for Italy: the ILO employment by activity and occupation for the country has yet to be downloaded and Eurostat activities linked to ISIC sections.",
        "ita_nota": "Italy: the ISTAT HBS 2023 (public file) only carries age classes, so Descendants are those under 18, Builders 18 to 64 and Ascendants 65 and over; and housing includes imputed rent, unlike the other countries. Multipliers and employment come from the Eurostat symmetric table for 2022 and the A64 activities.",
        "grp_lim": ["These are demand groups (what is consumed), not supply sectors; the match with the thesis activities (local food, regional energy, short chains, research-linked education) is a hypothesis, not a measurement.",
                    "Private household spending only, excluding imputed rent; public education and health are left out.",
                    "Zeros in marginal spending mean spending indistinguishable from zero, not absence of consumption.",
                    "The overlap shows how much children's and older people's demand goes to the same groups; it does not measure coexistence."],
        "sem_instr": "No publishable instrument in this round.", "sem_lac": "No gaps recorded.",
        "rodape": "Independent research. Data and method traceable by evidence ID. Preview generated on",
        "ver_site": "ainu.systems",
    },
}

NATUREZA = {
    "pt": {"OBS": "Observado", "DER": "Derivado", "EST": "Estimado", "PROJ": "Projeção", "SIM": "Simulação", "ENTRADA": "Entrada"},
    "en": {"OBS": "Observed", "DER": "Derived", "EST": "Estimated", "PROJ": "Projection", "SIM": "Simulation", "ENTRADA": "Input"},
}
NATUREZA_DESC = {
    "pt": {"OBS": "Dado observado em fonte", "DER": "Conta simples sobre dado observado", "EST": "Estimado por modelo",
           "PROJ": "Projeção condicional a cenário", "SIM": "Simulação de mecanismo", "ENTRADA": "Entrada do plano de pesquisa, não validada"},
    "en": {"OBS": "Observed in a source", "DER": "Simple calculation on observed data", "EST": "Model estimate",
           "PROJ": "Scenario-conditional projection", "SIM": "Mechanism simulation", "ENTRADA": "Research-plan input, not validated"},
}
ROT = {  # (bloco, chave) -> (pt, en, unidade)
    ("coortes", "descendentes"): ("Descendentes (Prometidos)", "Descendants (Promised)", ""),
    ("coortes", "estruturadores"): ("Estruturadores", "Builders (Estruturadores)", ""),
    ("coortes", "ascendentes"): ("Ascendentes (Legadores)", "Ascendants (Legators)", ""),
    ("cobertura", "perfil_consumo"): ("Perfil de consumo por idade", "Consumption profile by age", ""),
    ("cobertura", "insumo_produto"): ("Insumo-produto", "Input-output tables", ""),
    ("cobertura", "ano_contas"): ("Ano das contas por coorte", "Year of the cohort accounts", ""),
    ("cobertura", "afi_tempo"): ("AFI (tempo de cuidado valorado)", "AFI (valued care time)", ""),
    ("demografia", "tft_2025"): ("TFT em 2025 (WPP Medium)", "TFR in 2025 (WPP Medium)", ""),
    ("demografia", "pop_2025_pct"): ("População 2025: Descendentes / Estruturadores / Ascendentes", "Population 2025: Descendants / Builders / Ascendants", "%"),
    ("demografia", "asc_estr_2025"): ("Ascendentes ÷ Estruturadores, 2025", "Ascendants ÷ Builders, 2025", ""),
    ("demografia", "asc_estr_2075_wpp"): ("Ascendentes ÷ Estruturadores, 2075 (WPP Medium)", "Ascendants ÷ Builders, 2075 (WPP Medium)", ""),
    ("demografia", "asc_estr_2075_tft_constante"): ("Ascendentes ÷ Estruturadores, 2075 (TFT constante)", "Ascendants ÷ Builders, 2075 (constant TFR)", ""),
    ("demografia", "dependencia_2025_2075_wpp"): ("Dependência (D+A) ÷ E, 2025 → 2075", "Dependency (D+A) ÷ B, 2025 → 2075", ""),
    ("demografia", "estruturadores_2075_rel"): ("Estruturadores em 2075 (2025 = 100)", "Builders in 2075 (2025 = 100)", ""),
    ("demografia", "descendentes_2075_rel"): ("Descendentes em 2075 (2025 = 100)", "Descendants in 2075 (2025 = 100)", ""),
    ("demografia", "carga_estr_2075_wpp"): ("Carga por Estruturador em 2075, WPP Medium (2025 = 100)", "Burden per Builder in 2075, WPP Medium (2025 = 100)", ""),
    ("demografia", "carga_estr_2075_tft_constante"): ("Carga por Estruturador em 2075, TFT constante", "Burden per Builder in 2075, constant TFR", ""),
    ("demografia", "carga_estr_2075_rapida"): ("Carga por Estruturador em 2075, TFT 2,1 até 2035", "Burden per Builder in 2075, TFR 2.1 by 2035", ""),
    ("consumo", "cfcc_total_pct_desc_estr_asc"): ("CFCc total (privado + público): D / E / A", "Total CFCc (private + public): D / B / A", "%"),
    ("consumo", "desc_privado_pesos_nta"): ("Descendentes no consumo privado, pesos NTA", "Descendants in private consumption, NTA weights", "%"),
    ("consumo", "desc_privado_microdados_ancorados"): ("Descendentes no consumo privado, microdados ancorados no NTA", "Descendants in private consumption, microdata anchored to NTA", "%"),
    ("consumo", "desc_privado_regressao_bruta"): ("Descendentes no consumo privado, regressão bruta", "Descendants in private consumption, raw regression", "%"),
    ("consumo", "razao_0_24_sobre_25_64"): ("Consumo privado 0–24 ÷ 25–64: NTA / regressão / divisão igual", "Private consumption 0–24 ÷ 25–64: NTA / regression / equal split", ""),
    ("consumo", "fator_ancoragem"): ("Fator de ancoragem das crianças", "Child anchoring factor", ""),
    ("multiplicadores", "valor_adicionado"): ("Valor adicionado gerado por unidade de consumo privado", "Value added generated per unit of private consumption", ""),
    ("multiplicadores", "importacoes"): ("Importações (diretas + indiretas)", "Imports (direct + indirect)", ""),
    ("multiplicadores", "edpc_sobre_emprego"): ("EDPc ÷ emprego modelado", "EDPc ÷ modeled employment", ""),
    ("valorizacao", "gasto_publico_familia_socx"): ("Gasto público em família (OECD SOCX), % do PIB", "Public family spending (OECD SOCX), % of GDP", ""),
    ("valorizacao", "dividendo_10pct_pib"): ("Dividendo de 10% do gasto privado por Descendente", "Dividend of 10% of private spending per Descendant", "% do PIB"),
    ("valorizacao", "maior_programa_infantil"): ("Maior programa infantil de renda", "Largest child income programme", ""),
    ("valorizacao", "dividendo_sobre_programa"): ("Dividendo de 10% ÷ maior programa", "10% Dividend ÷ largest programme", "×"),
    ("valorizacao", "analogo_ifvi_empregador"): ("Análogo de IFVI pago pelo empregador", "Employer-paid IFVI analogue", ""),
}
BLOCOS = ["demografia", "consumo", "multiplicadores", "valorizacao", "cobertura"]
GLOSS_EN = {
    "Descendentes (Prometidos)": ("Descendants (Promised)", "Base cohort (young population), with an age cutoff specific to each country. In the V1_1 thesis: Prometidos."),
    "Estruturadores": ("Builders (Estruturadores)", "Cohort of intermediate ages; corresponds to the thesis's Generational Provider (reference ages 25 to 65)."),
    "Ascendentes (Legadores)": ("Ascendants (Legators)", "Top cohort (older population). The term 'Legadores' (those who leave a legacy) was confirmed by the author on 2026-11-01."),
    "URSS (Unidade de Reprodução Social Sustentável)": ("URSS (Sustainable Social Reproduction Unit)", "Functional structure, private, family and civil in character, that takes effective responsibility for forming Relational Human Capital (CHR) and for generational continuity. A primary civilizational asset, not a welfare beneficiary. URSS condition: Active, Fulfilled or Inactive, by an observable criterion independent of employment status."),
    "CHR (Capital Humano Relacional)": ("CHR (Relational Human Capital)", "The professionalizing and socializing formation that parents provide to their children. Irreplaceable, inelastic, unpaid."),
    "UDE (Unidade Demográfica de Estado)": ("UDE (State Demographic Unit)", "The real set of URSS existing at a given moment; belonging requires effective responsibility for forming and sustaining at least one descendant aged 0 to 25, biological or adopted. Economic reading: Total Investment in UDE = NTA(0-25) + NTA(25-65) restricted to Providers in a URSS (the second term has no consolidated source)."),
    "CFCc": ("CFCc", "Final Consumption by Cohort: final expenditure attributed to the cohort."),
    "CIEc": ("CIEc", "Imported Content by Cohort: direct and indirect foreign content."),
    "VADc": ("VADc", "Domestic Value Added attributable to the cohort's final demand (not a cohort GDP; it does not add up to GDP)."),
    "EDPc": ("EDPc", "Domestic Jobs Sustained by cohort demand (gross, displacement and net kept separate)."),
    "REAc": ("REAc", "Labor income appropriated by Builders in an Active URSS; requires microdata."),
    "AFI (Ativo de Formação Intergeracional)": ("AFI (Intergenerational Formation Asset)", "The investment Builders make in food, housing, health, education, clothing, transport, protection, development, daily care and unpaid accompaniment and education. In this research it is measured operationally (private spending on the Descendants cohort, net of transfers, plus the value of care time); the formulas remain an unapproved proposal."),
    "Dividendo Intergeracional": ("Intergenerational Dividend", "A partial return to Builders for investing in forming new generations. It is not a wage, a full reimbursement of spending or conventional assistance. A Narayama proposal; here only simulated in cost."),
    "IFVI (Incentivos Fiscais à Valorização Intergeracional)": ("IFVI (Tax Incentives for Intergenerational Valorization)", "Tax benefits to agents that provide goods, services and infrastructure that lower costs and improve the sustainability of URSS. Distinct from the AFI and the Dividend."),
    "N* (Índice de Narayama Sistêmico)": ("N* (Systemic Narayama Index)", "N* = square root of N_Base, with N_Base = NGII_puro × Generational Factor. Zones: PEC < 0.71; Accelerated Tension 0.71–0.90; PEA 0.90–1.40; Population Tension 1.40–2.00; PEEC ≥ 2.00."),
    "PQDF-N*": ("PQDF-N*", "Quality, Decomposition and Falsifiability Protocol for the N*: the observed N* (N*_Obs) is always published; adjustments for migration, inertia, policies and under-registration are separate scenarios (N*_k)."),
}


def e(s) -> str:
    return html.escape(str(s), quote=True)


def num(texto: str, lang: str) -> str:
    sep = "," if lang == "pt" else "."
    return re.sub(r"(?<=\d)[.,](?=\d)", sep, texto)


def valor_txt(reg: dict, lang: str, unidade: str) -> tuple[str, bool]:
    """(html do valor, é texto livre em português?)"""
    if reg.get("retido"):
        return f'<span class="muted">{e(T[lang]["em_conf"])}</span>', False
    t = reg.get("texto")
    if t is None or reg.get("lacuna"):
        return f'<span class="muted">{e(T[lang]["nd"])}</span>', False
    if re.search(r"a confirmar", t, re.I):
        return f'<span class="muted">{e(T[lang]["em_conf"])}</span>', False
    if re.match(r"(Instrumentos oficiais não pesquisados|Não pesquisad)", t, re.I):
        return f'<span class="muted">{e(T[lang]["np"])}</span>', False
    if re.fullmatch(r"[\d.,]+ \(\d{4}\)", t):
        return e(num(t, lang)), False
    if reg.get("valor") is not None:
        if lang == "en":
            unidade = unidade.replace("% do PIB", "% of GDP")
        u = f" {unidade}" if unidade and unidade != "×" else ""
        pos = "×" if unidade == "×" else ""
        return e(num(t, lang) + u + pos), False
    if re.fullmatch(r"[\d.,]+×", t):
        return e(num(t, lang)), False
    return f'<span lang="pt">{e(t)}</span>', True


def sig2(n):
    """Dois algarismos significativos: as entradas das abas de cenários vêm arredondadas (bi, tri)."""
    from math import floor, log10
    if n == 0:
        return 0
    k = 1 - floor(log10(abs(n)))
    return round(n, k)


def milhar(n, lang: str) -> str:
    t = f"{round(sig2(n)):,}"
    return t.replace(",", ".") if lang == "pt" else t


def dec(n, casas: int, lang: str) -> str:
    return f"{n:.{casas}f}".replace(".", ",") if lang == "pt" else f"{n:.{casas}f}"


def faixa(lo, hi, fmt, t) -> str:
    a, b = fmt(lo), fmt(hi)
    return "" if a == b else f" · {e(t['incr_faixa'])}: {a}–{b}"


GRUPOS_EN = {"Alimentos e bebidas": "Food and beverages", "Habitação, energia e equipamento do lar": "Housing, energy and household equipment",
             "Saúde": "Health", "Educação": "Education", "Vestuário e calçado": "Clothing and footwear",
             "Transporte e comunicação": "Transport and communication", "Recreação, cultura, restaurantes e hotéis": "Recreation, culture, restaurants and hotels",
             "Cuidados pessoais, serviços e outros bens": "Personal care, services and other goods"}


def grupos_html(p: dict, lang: str) -> str:
    t = T[lang]
    g = p["composicao_grupos"]
    cab = f"<h2>{e(t['grp_titulo'])}</h2>"
    if not g.get("disponivel"):
        return cab + f"<p class='muted'>{e(t['grp_nd_ita'] if p['iso'] == 'ITA' else t['grp_nd'])}</p>"
    f1 = lambda x: dec(x, 1, lang)
    linhas = ""
    for r in g["grupos"]:
        nome_g = r["grupo"] if lang == "pt" else GRUPOS_EN[r["grupo"]]
        d, a = r["descendentes"], r["ascendentes"]
        linhas += (f"<tr><td>{e(nome_g)}</td><td class='v'>{f1(d['marginal'])}</td><td class='v'>{f1(d['medio'])}</td>"
                   f"<td class='v'>{f1(a['marginal'])}</td><td class='v'>{f1(a['medio'])}</td></tr>")
    so, cb = g["sobreposicao_desc_asc"], g["cobertura_gastos"]
    cab_t = (f"<tr><th rowspan='2'>{e(t['grp_grupo'])}</th><th colspan='2'>{e(t['grp_desc'])} (%)</th><th colspan='2'>{e(t['grp_asc'])} (%)</th></tr>"
             f"<tr><th>{e(t['grp_marg'])}</th><th>{e(t['grp_med'])}</th><th>{e(t['grp_marg'])}</th><th>{e(t['grp_med'])}</th></tr>")
    kv = (f"<div class='kv'><div><small>{e(t['grp_sobre'])} · {e(t['grp_marg'])} / {e(t['grp_med'])}</small><b>{dec(so['marginal'], 2, lang)} / {dec(so['medio'], 2, lang)}</b></div>"
          f"<div><small>{e(t['grp_cobre'])}</small><b>{dec(cb * 100, 0, lang)}%</b></div></div>")
    lim = "".join(f"<li>{e(x)}</li>" for x in t["grp_lim"]) + (f"<li>{e(t['ita_nota'])}</li>" if p["iso"] == "ITA" else "")
    return (cab + f"<p class='nota'>{e(t['grp_nota'])} {chip('EST', lang)}</p><div class='tw'><table><thead>{cab_t}</thead><tbody>{linhas}</tbody></table></div>"
            f"{kv}<ul class='nota'>{lim}</ul>")


def mult_html(p: dict, lang: str) -> str:
    t = T[lang]
    m = p["multiplicadores_grupos"]
    cab = f"<h2>{e(t['mul_titulo'])}</h2>"
    if not m.get("disponivel"):
        return cab + f"<p class='muted'>{e(t['grp_nd_ita'] if p['iso'] == 'ITA' else t['grp_nd'])}</p>"
    f1 = lambda x: dec(x, 1, lang)
    linhas = ""
    for r in m["grupos"]:
        nome_g = r["grupo"] if lang == "pt" else GRUPOS_EN[r["grupo"]]
        d, a = r["vad_participacao"]["descendentes"], r["vad_participacao"]["ascendentes"]
        linhas += (f"<tr><td>{e(nome_g)}</td><td class='v'>{dec(r['vad_por_unidade'], 2, lang)}</td><td class='v'>{dec(r['empregos_por_milhao'], 1, lang)}</td>"
                   f"<td class='v'>{f1(d['marginal'])} / {f1(d['medio'])}</td><td class='v'>{f1(a['marginal'])} / {f1(a['medio'])}</td></tr>")
    aviso = (t["mul_aviso_set"] if m["metodo_emprego"].startswith("seções ISIC") else
             t["mul_aviso_a64"] if m["metodo_emprego"].startswith("atividades A64") else t["mul_aviso_prod"])
    lim = "".join(f"<li>{e(x)}</li>" for x in t["mul_lim"]) + (f"<li>{e(t['ita_nota'])}</li>" if p["iso"] == "ITA" else "")
    return (cab + f"<p class='nota'>{e(t['mul_nota'])} {chip('EST', lang)}</p><div class='tw'><table><thead><tr><th>{e(t['grp_grupo'])}</th><th>{e(t['mul_vad'])}</th>"
            f"<th>{e(t['mul_emp'])}</th><th>{e(t['mul_d'])}<br>{e(t['grp_marg'])} / {e(t['grp_med'])}</th><th>{e(t['mul_a'])}<br>{e(t['grp_marg'])} / {e(t['grp_med'])}</th></tr></thead>"
            f"<tbody>{linhas}</tbody></table></div><p class='nota'>{e(aviso)}</p><ul class='nota'>{lim}</ul>")


def iag_html(p: dict, lang: str) -> str:
    t = T[lang]
    x = p["exposicao_iagen"]
    cab = f"<h2>{e(t['iag_titulo'])}</h2>"
    if not x.get("disponivel"):
        return cab + f"<p class='muted'>{e(t['exp_nd_ita'] if p['iso'] == 'ITA' else t['grp_nd'])}</p>"
    d2 = lambda v: dec(v, 2, lang)
    linhas = ""
    for r in x["grupos"]:
        nome_g = r["grupo"] if lang == "pt" else GRUPOS_EN[r["grupo"]]
        linhas += f"<tr><td>{e(nome_g)}</td><td class='v'>{d2(r['media'])} ({d2(r['baixa'])}–{d2(r['alta'])})</td><td class='v'>{d2(r['fracao_alta'])}</td></tr>"
    c = x["coortes"]
    cm = lambda k: f"{d2(c[k + '_marginal']['media'])} / {d2(c[k + '_médio']['media'])}"
    kv = (f"<div class='kv'><div><small>{e(t['exp_c'])}</small><b>{cm('descendentes')}</b></div>"
          f"<div><small>{e(t['exp_i'])}</small><b>{cm('ascendentes')}</b></div></div>")
    lim = "".join(f"<li>{e(y)}</li>" for y in t["iag_lim"])
    return (cab + f"<details><summary>{e(t['iag_ref'])}</summary><p class='nota'>{e(t['iag_nota'])} {chip('EST', lang)}</p><div class='tw'><table><thead><tr><th>{e(t['grp_grupo'])}</th><th>{e(t['iag_media'])}</th><th>{e(t['iag_alta'])}</th></tr></thead>"
            f"<tbody>{linhas}</tbody></table></div><p class='nota'><b>{e(t['exp_coorte'])}</b></p>{kv}<ul class='nota'>{lim}</ul></details>")


def exp_html(p: dict, lang: str) -> str:
    t = T[lang]
    x = p["exposicao_automacao"]
    cab = f"<h2>{e(t['exp_titulo'])}</h2>"
    if not x.get("disponivel"):
        return cab + f"<p class='muted'>{e(t['exp_nd_ita'] if p['iso'] == 'ITA' else t['grp_nd'])}</p>"
    d2 = lambda v: dec(v, 2, lang)
    linhas = ""
    for r in x["grupos"]:
        nome_g = r["grupo"] if lang == "pt" else GRUPOS_EN[r["grupo"]]
        linhas += (f"<tr><td>{e(nome_g)}</td><td class='v'>{d2(r['media'])} ({d2(r['baixa'])}–{d2(r['alta'])})</td><td class='v'>{d2(r['fracao_alta'])}</td></tr>")
    c = x["coortes"]
    cm = lambda k: f"{d2(c[k + '_marginal']['media'])} / {d2(c[k + '_médio']['media'])}"
    kv = (f"<div class='kv'><div><small>{e(t['exp_c'])}</small><b>{cm('descendentes')}</b></div>"
          f"<div><small>{e(t['exp_i'])}</small><b>{cm('ascendentes')}</b></div></div>")
    lim = "".join(f"<li>{e(y)}</li>" for y in t["exp_lim"])
    return (cab + f"<p class='nota'>{e(t['exp_nota'])} {chip('EST', lang)}</p><div class='tw'><table><thead><tr><th>{e(t['grp_grupo'])}</th><th>{e(t['exp_media'])}</th><th>{e(t['exp_alta'])}</th></tr></thead>"
            f"<tbody>{linhas}</tbody></table></div><p class='nota'><b>{e(t['exp_coorte'])}</b></p>{kv}<ul class='nota'>{lim}</ul>")


CO_EN = {"cereais e substitutos": "cereals and substitutes", "leguminosas e derivados": "pulses and products", "açúcar e sal": "sugar and salt", "leite e derivados": "milk and milk products",
         "hortaliças": "vegetables", "frutas": "fruits", "ovos, peixe e carne": "egg, fish and meat", "óleos comestíveis": "edible oil", "temperos": "spices",
         "bebidas, lanches e alimentos processados (inclui refeições prontas compradas)": "beverages, refreshments and processed food (includes purchased cooked meals)",
         "ALIMENTOS, total": "FOOD, total", "pan, tabaco e intoxicantes": "pan, tobacco and intoxicants", "combustível e luz": "fuel and light", "educação": "education", "saúde (medical)": "medical",
         "transporte (conveyance)": "conveyance", "serviços ao consumidor, exceto transporte": "consumer services excluding conveyance", "bens diversos e entretenimento": "miscellaneous goods and entertainment",
         "aluguel": "rent", "impostos e taxas": "taxes and cesses", "vestuário, roupa de cama e calçado": "clothing, bedding and footwear", "bens duráveis": "durable goods",
         "NÃO ALIMENTOS, total": "NON-FOOD, total", "TODOS OS ITENS": "ALL ITEMS"}
CO_IND_EN = {"MPCE médio 2023-24": "Average MPCE 2023-24", "Mediana do MPCE (P50) 2023-24": "Median MPCE (P50) 2023-24", "Coeficiente de Gini do consumo por pessoa": "Gini coefficient of per-person consumption"}


def consumo_obs_html(p: dict, lang: str) -> str:
    c = p.get("consumo_observado", {})
    if not c.get("disponivel"):
        return ""
    t = T[lang]
    sel = [n for n in c["niveis"] if n["indicador"] in ("MPCE médio 2023-24", "Mediana do MPCE (P50) 2023-24", "Coeficiente de Gini do consumo por pessoa", "P10", "P90")]
    val = lambda v: (f"{int(v):,}".replace(",", ".") if lang == "pt" else f"{int(v):,}") if v > 1 else dec(v, 3, lang)   # valores observados: sem arredondar
    lin = "".join(f"<tr><td>{e(n['indicador'] if lang == 'pt' else CO_IND_EN.get(n['indicador'], n['indicador']))}</td><td class='v'>{e(val(n['rural']))}</td>"
                  f"<td class='v'>{e(val(n['urbano']))}</td><td>{e(n['pagina'])}</td></tr>" for n in sel)
    gl = "".join(f"<tr><td>{e(r['grupo'] if lang == 'pt' else CO_EN.get(r['grupo'], r['grupo']))}</td><td class='v'>{dec(r['rural_pct'], 1, lang)}</td><td class='v'>{dec(r['urbano_pct'], 1, lang)}</td></tr>" for r in c["grupos"])
    return (f"<h2>{e(t['co_titulo'])}</h2><p class='nota'>{e(t['co_nota'])} {chip('OBS', lang)}</p>"
            f"<div class='tw'><table><thead><tr><th>{e(t['co_ind'])}</th><th>{e(t['co_rural'])}</th><th>{e(t['co_urbano'])}</th><th>p.</th></tr></thead><tbody>{lin}</tbody></table></div>"
            f"<div class='tw'><table><thead><tr><th>{e(t['co_grupo'])}</th><th>{e(t['co_rural'])} ({e(t['co_pct'])})</th><th>{e(t['co_urbano'])} ({e(t['co_pct'])})</th></tr></thead><tbody>{gl}</tbody></table></div>"
            f"<p class='nota'>ID: <code>{link_id(c['id'])}</code></p>")


def incremento_html(p: dict, lang: str) -> str:
    t = T[lang]
    i = p["incremento_crianca"]
    cab = f"<h2>{e(t['incr_titulo'])}</h2>"
    if not i.get("disponivel"):
        return cab + f"<p class='muted'>{e(t['incr_nd'])}</p>"
    em, vd = i["empregos_brutos_por_crianca"], i["vad_por_crianca_ano"]
    un = i["unidade_vad"]
    if lang == "en":
        un = {"€ de 2022": "2022 euros (€)", "pesos de 2018": "2018 pesos", "R$ de 2015": "2015 reais (R$)", "R$ de 2018": "2018 reais (R$)",
              "US$ de 2023": "2023 US dollars (US$)", "¥ de 2022": "2022 yen (¥)"}.get(un, un)
    cards = (
        f"<div><small>{e(t['incr_emp'])} {chip('EST', lang)}</small><b>{dec(em['mediana'], 2, lang)}</b>"
        f"<small>{e(t['incr_equiv'].format(n=dec(i['criancas_por_emprego_bruto'], 1, lang)))}{faixa(em['min'], em['max'], lambda x: dec(x, 2, lang), t)}</small></div>"
        f"<div><small>{e(t['incr_liq'])}</small><b>{dec(i['empregos_liquidos_50'], 2, lang)}</b></div>"
        f"<div><small>{e(t['incr_vad'])}</small><b>{milhar(vd['mediana'], lang)}</b><small>{e(un)}{faixa(vd['min'], vd['max'], lambda x: milhar(x, lang), t)}</small></div>"
        f"<div><small>{e(t['incr_razao'])}</small><b>{dec(i['vad_sobre_cfcc'] * 100, 0, lang)}%</b></div>")
    lim = "".join(f"<li>{e(x)}</li>" for x in t["incr_lim"])
    return cab + f"<p class='nota'>{e(t['incr_nota'])}</p><div class='kv'>{cards}</div><ul class='nota'>{lim}</ul>"


def chip(nat: str, lang: str) -> str:
    return f'<span class="chip c-{e(nat)}" title="{e(NATUREZA_DESC[lang][nat])}">{e(NATUREZA[lang][nat])}</span>'


def nome(p: dict, lang: str) -> str:
    return p["nome"] if lang == "pt" else PAISES_EN.get(p["nome"], p["nome"])


FONTES: dict = {}
EVID: list = []


def link_id(i: str) -> str:
    f = FONTES.get(i)
    if f and f.get("url"):
        return f"<a href='{e(f['url'])}' rel='noopener' target='_blank'>{e(i)}</a>"
    return e(i)


CSS = """
:root{--ink:#0D1B2A;--soft:#3D5166;--sky:#1B6CA8;--glow:#6E92A8;--paper:#F7F9FB;--line:#D8E4EE;--white:#fff;--warn:#8a5a00;--warnbg:#fff4d6}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:Inter,system-ui,sans-serif;color:var(--ink);background:var(--paper);line-height:1.55}
.banner{background:var(--warnbg);color:var(--warn);font-size:.8rem;font-weight:600;text-align:center;padding:.45rem 1rem;border-bottom:1px solid #e8d49a;position:sticky;top:0;z-index:20}
nav{display:flex;align-items:center;justify-content:space-between;padding:.8rem 1.6rem;background:rgba(247,249,251,.95);border-bottom:1px solid var(--line);position:sticky;top:2rem;z-index:10}
.logo{font-family:'JetBrains Mono',monospace;font-size:.85rem;letter-spacing:.18em;color:var(--sky);text-decoration:none;font-weight:500}
.navr a{font-size:.82rem;color:var(--soft);text-decoration:none;margin-left:1.2rem;font-weight:500}.navr a:hover{color:var(--sky)}
main{max-width:1040px;margin:0 auto;padding:2rem 1.2rem 4rem}
h1{font-size:2rem;margin:.2rem 0 .3rem}h2{font-size:1.25rem;margin:2.2rem 0 .6rem;padding-top:.3rem;border-top:1px solid var(--line)}
.sub{color:var(--soft);margin:0 0 1.2rem}.lead{max-width:760px}
.crumb{font-size:.82rem;margin-bottom:.8rem}.crumb a{color:var(--sky);text-decoration:none}
.avisos{background:var(--white);border:1px solid var(--line);border-left:3px solid var(--glow);border-radius:6px;padding:.7rem 1rem;font-size:.86rem;color:var(--soft);margin:1rem 0}
.avisos p{margin:.25rem 0}
table{width:100%;border-collapse:collapse;background:var(--white);border:1px solid var(--line);border-radius:6px;font-size:.88rem}
th,td{text-align:left;padding:.5rem .7rem;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:.74rem;text-transform:uppercase;letter-spacing:.06em;color:var(--soft);background:#eef3f8}
td.v{font-variant-numeric:tabular-nums}
.tw{overflow-x:auto}
.muted{color:#7a8ea2}
.chip{display:inline-block;font-size:.68rem;font-weight:600;padding:.1rem .45rem;border-radius:99px;border:1px solid var(--line);white-space:nowrap}
.c-OBS{background:#e6f2ea;color:#1c6b3a}.c-DER{background:#e8f0f8;color:#1b5a8f}.c-EST{background:#efe9f8;color:#5b3c99}
.c-PROJ{background:#fdf0dc;color:#8a5a00}.c-SIM{background:#fbe6e6;color:#9a2b2b}.c-ENTRADA{background:#eee;color:#555}
.nv{font-family:'JetBrains Mono',monospace;font-size:.72rem;padding:.1rem .4rem;border-radius:4px;background:#e6f2ea;color:#1c6b3a}
.nv.misto{background:#fdf0dc;color:#8a5a00}
.hub{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:.9rem;margin:1.4rem 0}
.hub a{display:block;background:var(--white);border:1px solid var(--line);border-top:3px solid var(--sky);border-radius:6px;padding:1rem 1.1rem;text-decoration:none;color:var(--ink)}
.hub a:hover{border-color:var(--sky)}.hub b{display:block;font-size:1.08rem;margin-bottom:.25rem}.hub span{font-size:.86rem;color:var(--soft)}
#filtro{width:100%;max-width:520px;padding:.5rem .7rem;border:1px solid var(--line);border-radius:6px;font-size:.9rem;margin:.4rem .6rem .8rem 0}
.rodfontes{border-bottom:1px solid var(--line);margin-bottom:1rem;padding-bottom:.6rem}
.rodfontes h2{margin:.2rem 0 .4rem;border:0;font-size:1.05rem}.rodfontes details{margin:.35rem 0;padding:.35rem .7rem;font-size:.82rem}
.rodfontes ul{margin:.4rem 0;padding-left:1.1rem}.rodfontes li{margin:.25rem 0}.rodfontes small{color:var(--soft)}
.est-ok{color:#1c6b3a}.est-av{color:#8a5a00}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:.8rem;margin:1.2rem 0}
.card{display:block;background:var(--white);border:1px solid var(--line);border-radius:6px;padding:.9rem 1rem;text-decoration:none;color:var(--ink)}
.card:hover{border-color:var(--sky)}.card b{display:block;font-size:1.02rem}.card span{font-size:.8rem;color:var(--soft)}
.kv{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:.8rem;margin:1rem 0}
.kv div{background:var(--white);border:1px solid var(--line);border-radius:6px;padding:.7rem .9rem}.kv small{display:block;color:var(--soft);font-size:.74rem}.kv b{font-size:1.15rem}
.nota{font-size:.82rem;color:var(--soft);margin:.4rem 0 0}
details{background:var(--white);border:1px solid var(--line);border-radius:6px;padding:.5rem .9rem;margin:.5rem 0}
summary{cursor:pointer;font-weight:600;font-size:.92rem}
.instr{border:1px solid var(--line);background:var(--white);border-radius:6px;padding:.7rem .9rem;margin:.6rem 0;font-size:.88rem}
.instr h3{margin:0 0 .3rem;font-size:.98rem}.instr dl{display:grid;grid-template-columns:150px 1fr;gap:.2rem .8rem;margin:.4rem 0 0}.instr dt{color:var(--soft);font-size:.78rem}.instr dd{margin:0}
.lg{display:flex;flex-wrap:wrap;gap:.5rem 1.2rem;font-size:.8rem;color:var(--soft);margin:.6rem 0}
footer{max-width:1040px;margin:0 auto;padding:1.5rem 1.2rem 3rem;font-size:.78rem;color:var(--soft);border-top:1px solid var(--line)}
@media(max-width:640px){nav{padding:.6rem 1rem}.instr dl{grid-template-columns:1fr}h1{font-size:1.6rem}}
"""


EMBED = False   # True dentro do app (iframe): sem faixa de prévia nem navegação, e os links entre páginas viram "#"


def _sem_links_internos(h: str) -> str:
    return re.sub(r"""href=(['"])(?:\.\./(?:pt|en)/)?(?:index|dados|simulacoes|[A-Z]{3})\.html[^'"]*\1""", "href='#' target='_self'", h)


def pagina(lang: str, titulo: str, corpo: str, caminho_outra: str, raiz: str = "../", rodape_extra: str = "") -> str:
    t = T[lang]
    if EMBED:
        return _sem_links_internos(f"""<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><base target="_blank"><title>{e(titulo)}</title>
<style>{CSS}body{{background:transparent}}main{{padding-top:.5rem}}</style></head><body>
<main>{corpo}</main>
<footer>{rodape_extra}{e(t['rodape'])} {datetime.now().strftime('%Y-%m-%d')}. {e(t['aviso_indep'])}</footer></body></html>""")
    return f"""<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>{e(titulo)} · AINU.SYSTEMS</title>
<style>{CSS}</style></head><body>
<div class="banner">{e(t['banner'])}</div>
<nav><a class="logo" href="index.html">AINU.SYSTEMS</a><div class="navr"><a href="index.html#paises">{e(t['nav_paises'])}</a><a href="dados.html">{e(t['nav_dados'])}</a><a href="simulacoes.html">{e(t['nav_sim'])}</a><a href="{caminho_outra}">{e(t['idioma'])}</a></div></nav>
<main>{corpo}</main>
<footer>{rodape_extra}{e(t['rodape'])} {datetime.now().strftime('%Y-%m-%d')}. {e(t['aviso_indep'])}</footer></body></html>"""


def tabela_bloco(p: dict, bloco: str, lang: str) -> str:
    t = T[lang]
    linhas, tem_pt = [], False
    for chave, reg in p[bloco].items():
        if (bloco, chave) == ("cobertura", "classe_provisoria"):
            continue  # já aparece no resumo da ficha
        pt, en, un = ROT[(bloco, chave)]
        val, livre = valor_txt(reg, lang, un)
        tem_pt = tem_pt or livre
        nat_td = "" if bloco == "cobertura" else f"<td>{chip(reg['natureza'], lang)}</td>"
        linhas.append(f"<tr><td>{e(pt if lang == 'pt' else en)}</td><td class='v'>{val}</td>{nat_td}</tr>")
    nat_th = "" if bloco == "cobertura" else f"<th>{e(t['nat'])}</th>"
    return (f"<div class='tw'><table><thead><tr><th>{e(t['ind'])}</th><th>{e(t['valor'])}</th>{nat_th}</tr></thead>"
            f"<tbody>{''.join(linhas)}</tbody></table></div>"), tem_pt


def instrumentos_html(iso: str, instrs: list, lang: str) -> str:
    t = T[lang]
    sel = [i for i in instrs if i["iso"] == iso and i["status_publicacao"] != "lacuna"]
    if not sel:
        return f"<p class='muted'>{e(t['sem_instr'])}</p>"
    out = []
    for i in sel:
        nv = "L1" if i["nivel"] == "L1" else "L1 + L2"
        css = "" if i["nivel"] == "L1" else " misto"
        det = []
        for rot_pt, rot_en, k in (("Beneficiário", "Beneficiary", "beneficiario"), ("Valor", "Amount", "valor"),
                                  ("Financiamento", "Funding", "duracao_financiamento"), ("Custo fiscal", "Fiscal cost", "custo_fiscal")):
            if i.get(k):
                det.append(f"<dt>{e(rot_pt if lang == 'pt' else rot_en)}</dt><dd lang='pt'>{e(i[k])}</dd>")
        ids = ", ".join(link_id(x) for x in i["evidencias"])
        if ids:
            det.append(f"<dt>{e(t['id'])}</dt><dd><code>{ids}</code></dd>")
        ress = "" if i["nivel"] == "L1" else f"<p class='nota'>{e(t['ressalva'])}</p>"
        out.append(f"<div class='instr'><h3 lang='pt'>{e(i['instrumento'])} <span class='nv{css}' title='{e(t['nivel'])}'>{nv}</span></h3><dl>{''.join(det)}</dl>{ress}</div>")
    return "".join(out)


GRUPO_TIPO = {"WDI": "wdi", "ILO": "oit", "WPP": "onu", "NTA": "nta", "MRIO": "icio", "TUS": "tus", "HBS": "hbs", "IO": "io"}
ORDEM_GRUPOS = ["instr", "hbs", "pesq", "io", "icio", "tus", "nta", "onu", "oit", "wdi"]
NOME_MANUAL = json.loads(Path(__file__).with_name("nomes_fontes.json").read_text(encoding="utf-8"))
_CARGA: dict = {}


def _carga():
    if _CARGA:
        return _CARGA
    pri = DADOS.parent / "privado"
    ler = lambda a: json.loads(a.read_text(encoding="utf-8")) if a.exists() else {}
    _CARGA["auto"] = ler(pri / "conferencia_fontes.json").get("urls", {}) or ler(DADOS / "conferencia_fontes_estado.json")
    _CARGA["man"] = {k: v for k, v in ler(DADOS / "conferencia_manual.json").items() if not k.startswith("_")}
    _CARGA["links"] = ler(pri / "links_status.json") or ler(DADOS / "links_status.json")
    _CARGA["refs"] = ler(DADOS / "referencias.json") or []
    return _CARGA


def estado_fonte(url: str, lang: str) -> str:
    t, c = T[lang], _carga()
    lk = c["links"].get("links", {}).get(url)
    partes = []
    if lk:
        txt = {"ok": t["f_abriu"], "redirecionado": t["f_redir"], "bloqueado": t["f_bloq"], "nao_encontrado": t["f_naoenc"], "sem_resposta": t["f_sem"],
               "erro_servidor": t["f_erro"], "nao_testado": t["f_nt"]}[lk["estado"]]
        partes.append(f"<span class='{'est-ok' if lk['estado'] in ('ok', 'redirecionado') else 'est-av'}'>{e(txt)}</span>")
    m = c["man"].get(url)
    if m:
        rot = {"confere": t["f_confere"], "ressalva": t["f_ressalva"], "lida_antes": t["f_lida"], "nao_confirmada": t["f_nao_conf"]}[m["estado"]]
        partes.append(f"<span class='{'est-ok' if m['estado'] == 'confere' else 'est-av'}'>{e(rot)}</span>" + (f" <span lang='pt'>({e(m['nota'])})</span>" if m["estado"] != "confere" else ""))
    elif url in c["auto"]:
        a = c["auto"][url]["estado"]
        partes.append(f"<span class='{'est-ok' if a == 'confere' else 'est-av'}'>{e({'confere': t['f_confere_auto'], 'revisar': t['f_revisar'], 'nao_verificavel': t['f_nv']}[a])}</span>")
    return " · ".join(partes)


def _nome_fonte(f: dict, ev: dict) -> str:
    if f["id"] in NOME_MANUAL:
        return NOME_MANUAL[f["id"]]
    x = ev.get(f["id"])
    if x:
        return f"{x['variavel']} ({x['serie']})" if x.get("serie") else x["variavel"]
    return (f["descricao"] or f["id"]).split(": AINU")[0]


def _grupo(f: dict) -> str:
    g = GRUPO_TIPO.get(f["tipo"])
    if g:
        return g
    return "instr" if ": AINU" in (f["descricao"] or "") else "pesq"


def rodape_fontes(iso: str | None, evid: list, lang: str) -> str:
    """Bloco 'Fontes e referências desta página' do rodapé. iso=None: fontes de todo o Diretório, em resumo."""
    t, c = T[lang], _carga()
    ev = {x["id"]: x for x in evid}
    fs = [f for f in FONTES.values() if f.get("url") and (iso is None or f["iso"] == iso)]
    grupos: dict[str, dict[str, dict]] = {}
    for f in fs:
        g = grupos.setdefault(_grupo(f), {})
        item = g.setdefault(f["url"], {"nome": _nome_fonte(f, ev), "ids": []})
        item["ids"].append(f["id"])
    data = (c["links"].get("testado_em") or "")[:10] or "—"
    out = [f"<section class='rodfontes'><h2>{e(t['f_titulo'])}</h2><p class='nota'>{e(t['f_intro'].format(data=data))}</p>"]
    for g in ORDEM_GRUPOS:
        if g not in grupos:
            continue
        itens = grupos[g]
        if iso is None:
            out.append(f"<details><summary>{e(t['f_g_' + g])} ({len(itens)} {e(t['f_global_n'])})</summary></details>")
            continue
        lis = "".join(f"<li><a href='{e(u)}' rel='noopener' target='_blank'>{e(i['nome'])}</a> <small>({e(', '.join(sorted(set(i['ids']))[:3]))}{'…' if len(set(i['ids'])) > 3 else ''})</small><br><small>{estado_fonte(u, lang)}</small></li>"
                      for u, i in sorted(itens.items(), key=lambda kv: kv[1]["nome"]))
        out.append(f"<details{' open' if g in ('instr', 'hbs', 'pesq') else ''}><summary>{e(t['f_g_' + g])} ({len(itens)})</summary><ul>{lis}</ul></details>")
    refs = [r for r in c["refs"] if iso is None or iso in r["paises"]]
    if refs:
        lis = "".join(f"<li><a href='{e(r['url'])}' rel='noopener' target='_blank' lang='pt'>{e(r['nome'])}</a><br><small lang='pt'>{e(r['uso'])}</small><br><small>{estado_fonte(r['url'], lang)}</small></li>" for r in refs)
        out.append(f"<details open><summary>{e(t['f_refs'])} ({len(refs)})</summary><ul>{lis}</ul></details>")
    out.append(f"<p class='nota'>{e(t['f_calculo'])} <a href='dados.html'>{e(t['f_ver_dados'])}</a></p></section>")
    return "".join(out)


def ficha(p: dict, instrs, evid, lacunas, lang: str) -> str:
    t = T[lang]
    iso = p["iso"]
    c = p["coortes"]
    classe = (p["cobertura"]["classe_provisoria"].get("texto") or "")[:1]
    nome_ = nome(p, lang)
    corpo = [f"<div class='crumb'><a href='index.html'>← {e(t['voltar'])}</a></div>",
             f"<h1>{e(nome_)} <span class='muted' style='font-size:1rem'>{e(iso)}</span></h1>",
             f"<p class='sub'>{e(t['sub'])}</p>",
             "<div class='kv'>"
             f"<div><small>{e(t['classe'])}</small><b>{e(t['classes'].get(classe, classe))}</b></div>"
             f"<div><small>{e(ROT[('coortes','descendentes')][0 if lang=='pt' else 1])}</small><b>{e(c['descendentes'])}</b></div>"
             f"<div><small>{e(ROT[('coortes','estruturadores')][0 if lang=='pt' else 1])}</small><b>{e(c['estruturadores'])}</b></div>"
             f"<div><small>{e(ROT[('coortes','ascendentes')][0 if lang=='pt' else 1])}</small><b>{e(c['ascendentes'])}</b></div></div>",
             f"<div class='avisos'><p>{e(t['aviso_cortes'])}</p><p>{e(t['aviso_nstar'])}</p></div>"]
    notas = {"demografia": t["nota_demog"], "consumo": t["nota_consumo"], "valorizacao": t["nota_valor"]}
    for b in BLOCOS:
        tab, _ = tabela_bloco(p, b, lang)
        corpo.append(f"<h2>{e(t[b])}</h2>{tab}")
        if b == "multiplicadores":
            corpo.append(incremento_html(p, lang))
            corpo.append(grupos_html(p, lang))
            corpo.append(consumo_obs_html(p, lang))
            corpo.append(mult_html(p, lang))
            corpo.append(exp_html(p, lang))
            corpo.append(iag_html(p, lang))
        if b in notas:
            corpo.append(f"<p class='nota'>{e(notas[b])}</p>")
        if b == "valorizacao":
            corpo.append(f"<h2>{e(t['instrumentos'])}</h2>")
            if lang == "en":
                corpo.append(f"<p class='nota'>{e(t['aviso_texto_pt'])}</p>")
            corpo.append(instrumentos_html(iso, instrs, lang))
    lac = [x for x in lacunas if x["pais"] in (iso, p["nome"])]
    corpo.append(f"<h2>{e(t['lacunas'])}</h2>")
    if lac:
        corpo.append("<ul>" + "".join(f"<li lang='pt'>{e(x['item'])}" + (f" <span class='muted'>— {e(x['situacao'])}</span>" if x.get('situacao') else "") + "</li>" for x in lac) + "</ul>")
    else:
        corpo.append(f"<p class='muted'>{e(t['sem_lac'])}</p>")
    ev = [x for x in evid if x["iso"] == iso]
    linhas = "".join(
        f"<tr><td><code>{link_id(x['id'])}</code></td><td lang='pt'>{e(x['variavel'] or '')}</td><td lang='pt'>{e(x['fonte'] or '')}</td>"
        f"<td>{e(x['serie'] or '')}</td><td>{e((x['ano_inicial'] or '') + '–' + (x['ano_final'] or ''))}</td><td>{e(x['verificacao'])}</td></tr>" for x in ev)
    corpo.append(f"<h2>{e(t['fontes'])}</h2><details><summary>{len(ev)} {e(t['n_evid'])}</summary><div class='tw'><table><thead><tr>"
                 f"<th>{e(t['id'])}</th><th>{e(t['variavel'])}</th><th>{e(t['fonte'])}</th><th>{e(t['serie'])}</th><th>{e(t['periodo'])}</th><th>{e(t['verif'])}</th></tr></thead><tbody>{linhas}</tbody></table></div></details>")
    outra = "en" if lang == "pt" else "pt"
    return pagina(lang, nome_, "".join(corpo), f"../{outra}/{iso}.html", rodape_extra=rodape_fontes(iso, evid, lang))


def inc_txt(p: dict, lang: str) -> str:
    i = p["incremento_crianca"]
    if not i.get("disponivel"):
        return f"<span class='muted'>{e(T[lang]['nd'])}</span>"
    return dec(i["empregos_brutos_por_crianca"]["mediana"], 2, lang)


def indice(paises, glos, lang: str) -> str:
    t = T[lang]
    cols = [("classe", t["classe"]), ("tft", "TFT 2025" if lang == "pt" else "TFR 2025"),
            ("pop", "D / E / A (%)" if lang == "pt" else "D / B / A (%)"),
            ("carga", "Carga/Estr. 2075" if lang == "pt" else "Burden/Builder 2075"),
            ("div", "Dividendo 10% (% PIB)" if lang == "pt" else "10% Dividend (% GDP)"),
            ("inc", T[lang]["incr_col"])]
    th = "".join(f"<th>{e(x[1])}</th>" for x in cols)
    linhas, cards = [], []
    for p in paises:
        d, v = p["demografia"], p["valorizacao"]
        cl = (p["cobertura"]["classe_provisoria"].get("texto") or "")[:1]

        def g(reg):
            return valor_txt(reg, lang, "")[0]
        linhas.append(f"<tr><td><a href='{e(p['iso'])}.html'>{e(nome(p, lang))}</a></td><td>{e(cl)}</td><td class='v'>{g(d['tft_2025'])}</td>"
                      f"<td class='v'>{g(d['pop_2025_pct'])}</td><td class='v'>{g(d['carga_estr_2075_wpp'])}</td><td class='v'>{g(v['dividendo_10pct_pib'])}</td><td class='v'>{inc_txt(p, lang)}</td></tr>")
        cards.append(f"<a class='card' href='{e(p['iso'])}.html'><b>{e(nome(p, lang))}</b><span>{e(p['iso'])} · {e(t['classes'].get(cl, cl))}</span></a>")
    leg = "".join(f"<span>{chip(k, lang)} {e(NATUREZA_DESC[lang][k])}</span>" for k in NATUREZA[lang])
    gl = []
    for g in glos:
        termo, defin = g["termo"], g["definicao"]
        if lang == "en":
            termo, defin = GLOSS_EN[g["termo"]]
        gl.append(f"<details><summary>{e(termo)}</summary><p>{e(defin)}</p></details>")
    hub = "" if EMBED else (f"<div class='hub'><a href='#paises'><b>{e(t['hub_paises'])}</b><span>{e(t['hub_paises_d'])}</span></a>"
                            f"<a href='dados.html'><b>{e(t['hub_dados'])}</b><span>{e(t['hub_dados_d'])}</span></a>"
                            f"<a href='simulacoes.html'><b>{e(t['hub_sim'])}</b><span>{e(t['hub_sim_d'])}</span></a></div>")
    corpo = (f"<h1>{e(t['titulo'])}</h1><p class='sub'>{e(t['sub'])}</p><p class='lead'>{e(t['intro'])}</p>"
             f"<div class='avisos'><p>{e(t['aviso_cortes'])}</p><p>{e(t['aviso_nstar'])}</p><p>{e(t['aviso_indep'])}</p></div>"
             f"{hub}<h2 id='paises'>{e(t['hub_paises'])}</h2><div class='grid'>{''.join(cards)}</div><h2>{e(t['tabela'])}</h2>"
             f"<div class='tw'><table><thead><tr><th>{'País' if lang == 'pt' else 'Country'}</th>{th}</tr></thead><tbody>{''.join(linhas)}</tbody></table></div>"
             f"<p class='nota'>{e(t['nota_demog'])}</p><h2>{e(t['legenda'])}</h2><div class='lg'>{leg}</div>"
             f"<h2>{e(t['glossario'])}</h2>{''.join(gl)}")
    outra = "en" if lang == "pt" else "pt"
    return pagina(lang, t["titulo"], corpo, f"../{outra}/index.html", rodape_extra=rodape_fontes(None, EVID, lang))


def dados_pagina(evid, fontes, legenda: str, paises, lang: str, links: dict | None = None) -> str:
    t = T[lang]
    stl = (links or {}).get("links", {})
    nomes = {p["iso"]: nome(p, lang) for p in paises}
    nomes["ALL"] = t["d_global"]
    ev = {x["id"]: x for x in evid}
    ordem = {p["iso"]: k for k, p in enumerate(paises)}
    itens = [f for f in fontes if f["url_status"] != "nao_aplicavel"]
    n_der = sum(1 for f in fontes if f["url_status"] == "nao_aplicavel")
    itens.sort(key=lambda f: (ordem.get(f["iso"], -1), f["id"]))
    com_link = sum(1 for f in itens if f.get("url"))
    linhas = []
    for f in itens:
        x = ev.get(f["id"])
        if x:
            dado = f"<b lang='pt'>{e(x['variavel'] or '')}</b><br><span class='muted' lang='pt'>{e(x['fonte'] or '')}</span>"
            serie = e(x["serie"] or "")
            per = e((x["ano_inicial"] or "") + "–" + (x["ano_final"] or "")) if x.get("ano_inicial") else ""
            verif = x["verificacao"]
        else:
            dado = f"<span lang='pt'>{e(f['descricao'])}</span>"
            serie, per, verif = "", "", f.get("verificacao") or ""
        if f.get("url"):
            lk = f"<a href='{e(f['url'])}' rel='noopener' target='_blank'>{e(t['d_conferir'])}</a>"
            r_ = stl.get(f["url"])
            if r_:
                cor = {"ok": "#1c6b3a", "redirecionado": "#1c6b3a"}.get(r_["estado"], "#8a5a00")
                lk += f"<br><small style='color:{cor}'>{e(t['l_' + r_['estado']])}</small>"
        else:
            lk = f"<span class='muted'>{e(t['d_sem_link'])}</span>"
        busca = e(f"{nomes.get(f['iso'], f['iso'])} {f['iso']} {f['id']} {f['descricao']} {(x or {}).get('fonte') or ''}".lower())
        linhas.append(f"<tr data-b='{busca}'><td>{e(nomes.get(f['iso'], f['iso']))}</td><td><code>{e(f['id'])}</code></td><td>{dado}</td><td>{serie}</td><td>{per}</td><td>{e(verif)}</td><td>{lk}</td></tr>")
    resumo = (f"<div class='kv'><div><small>{e(t['d_resumo_total'])}</small><b>{len(itens)}</b></div><div><small>{e(t['d_resumo_link'])}</small><b>{com_link}</b></div>"
              f"<div><small>{e(t['d_resumo_sem'])}</small><b>{len(itens) - com_link}</b></div><div><small>{e(t['d_resumo_der'])}</small><b>{n_der}</b></div></div>")
    if stl:
        uni = [stl[u] for u in {f["url"] for f in itens if f.get("url")} if u in stl]
        ok_n = sum(1 for r in uni if r["estado"] in ("ok", "redirecionado"))
        resumo += (f"<p class='nota'>{len(uni)} {e(t['l_resumo'])} {e(links['testado_em'][:10])}: {ok_n} {e(t['l_ok_n'])}; {len(uni) - ok_n} {e(t['l_prob_n'])}.</p>")
    js = ("<script>const f=document.getElementById('filtro');f.addEventListener('input',()=>{const q=f.value.toLowerCase().trim();"
          "document.querySelectorAll('#dados tbody tr').forEach(r=>{r.style.display=r.dataset.b.includes(q)?'':'none'})});</script>")
    corpo = (f"<div class='crumb'><a href='index.html'>← {e(t['titulo'])}</a></div><h1>{e(t['d_titulo'])}</h1><p class='lead'>{e(t['d_intro'])}</p>{resumo}"
             f"<input id='filtro' type='search' placeholder='{e(t['d_filtro'])}' aria-label='{e(t['d_filtro'])}'>"
             f"<div class='tw'><table id='dados'><thead><tr><th>{e(t['d_col_pais'])}</th><th>ID</th><th>{e(t['d_col_dado'])}</th><th>{e(t['d_col_serie'])}</th><th>{e(t['d_col_per'])}</th>"
             f"<th>{e(t['d_col_verif'])}</th><th>{e(t['d_col_link'])}</th></tr></thead><tbody>{''.join(linhas)}</tbody></table></div>"
             f"<h2>{e(t['d_leg'])}</h2><p class='nota' lang='pt'>{e(legenda)}</p><p class='nota'>{e(t['d_nota'])}</p>{js}")
    nums = json.loads((DADOS / "conferencia_numeros_manual.json").read_text(encoding="utf-8")) if (DADOS / "conferencia_numeros_manual.json").exists() else []
    if nums:
        lin = "".join(
            f"<tr><td><b lang='pt'>{e(n['item'])}</b><br><small>{e(n['iso'])}</small></td><td lang='pt'>{('<a href=' + chr(39) + e(n['url']) + chr(39) + ' rel=noopener target=_blank>' + e(n['fonte']) + '</a>') if n['url'] else e(n['fonte'])}</td>"
            f"<td><span class='{'est-ok' if n['estado'] == 'confere' else 'est-av'}'>{e(t['n_' + n['estado']])}</span></td><td lang='pt'>{e(n['nota'])}</td></tr>" for n in nums)
        data_n = ((json.loads((DADOS.parent / 'privado' / 'conferencia_numeros.json').read_text(encoding='utf-8')) if (DADOS.parent / 'privado' / 'conferencia_numeros.json').exists() else {}).get('conferido_em') or '2026-11-02')[:10]
        corpo += (f"<h2>{e(t['n_titulo'])}</h2><p class='nota'>{e(t['n_intro'].format(data=data_n))}</p><div class='tw'><table><thead><tr><th>{e(t['n_col_item'])}</th><th>{e(t['n_col_fonte'])}</th>"
                  f"<th>{e(t['n_col_estado'])}</th><th>{e(t['n_col_nota'])}</th></tr></thead><tbody>{lin}</tbody></table></div>")
    outra = "en" if lang == "pt" else "pt"
    return pagina(lang, t["d_titulo"], corpo, f"../{outra}/dados.html", rodape_extra=rodape_fontes(None, evid, lang))


def simulacoes_pagina(sim: dict, lang: str) -> str:
    t = T[lang]
    nd = t["nd"]
    linhas = []
    for iso, d in sim["paises"].items():
        d10 = d["dividendo_10pct_pib"]
        pr = d["programa"]
        nm = PAISES_EN.get(d["nome"], d["nome"]) if lang == "en" else d["nome"]
        if d10 is None:
            linhas.append(f"<tr><td>{e(nm)}</td><td colspan='5'><span class='muted'>{e(nd)}</span></td></tr>")
            continue
        if pr.get("pct_pib") is not None:
            pct = num(format(pr["pct_pib"], "g"), lang)
            aprox = "≈ " if pr.get("ressalva") else ""
            ptxt = f"{aprox}{pct} <span class='muted'>({e(pr['nome'])}, {e(pr['ano'])})</span>"
            razao = num(format(d10 / pr["pct_pib"], ".1f"), lang) + "×"
        else:
            ptxt, razao = f"<span class='muted'>{e(nd)}</span>", "—"
        c10, c25, c50 = (num(format(d10 * k, ".2f"), lang) for k in (1, 2.5, 5))
        linhas.append(f"<tr><td>{e(nm)}</td><td class='v'>{c10}</td><td class='v'>{c25}</td><td class='v'>{c50}</td><td>{ptxt}</td><td class='v'>{razao}</td></tr>")
    corpo = (f"<div class='crumb'><a href='index.html'>← {e(t['titulo'])}</a></div><h1>{e(t['s_titulo'])}</h1><p class='lead'>{e(t['s_intro'])}</p>"
             f"<ul><li>{e(t['s_l1'])}</li><li>{e(t['s_l2'])}</li><li>{e(t['s_l3'])}</li></ul>"
             f"<div class='avisos'><p>{e(t['s_acesso'])}</p></div>"
             f"<h2>{e(t['s_tab'])}</h2><div class='tw'><table><thead><tr><th>{e(t['d_col_pais'])}</th><th>{e(t['s_col10'])}</th><th>{e(t['s_col25'])}</th><th>{e(t['s_col50'])}</th>"
             f"<th>{e(t['s_colprog'])}</th><th>{e(t['s_colrazao'])}</th></tr></thead><tbody>{''.join(linhas)}</tbody></table></div><p class='nota'>{e(t['s_nota_tab'])}</p>")
    outra = "en" if lang == "pt" else "pt"
    return pagina(lang, t["s_titulo"], corpo, f"../{outra}/simulacoes.html", rodape_extra=rodape_fontes(None, EVID, lang))


def carregar() -> dict:
    """Lê os JSON publicáveis e prepara FONTES e EVID (usados pelo rodapé). Devolve tudo num dicionário."""
    global FONTES, EVID
    ler = lambda nome: json.loads((DADOS / nome).read_text(encoding="utf-8"))
    evid = ler("evidencias.json")
    EVID = evid
    fontes_lista = ler("fontes.json")
    FONTES = {f["id"]: f for f in fontes_lista}
    links = _carga()["links"] or None
    glos = ler("glossario.json")
    assert {g["termo"] for g in glos} == set(GLOSS_EN), "glossário PT e EN fora de sincronia"
    return {"paises": ler("paises.json"), "instr": ler("instrumentos.json")["instrumentos"], "evid": evid, "lac": ler("lacunas.json")["nao_encontrados"],
            "glos": glos, "fontes": fontes_lista, "legenda": ler("meta.json").get("legenda_verificacao") or "", "sim": ler("simulacoes.json"), "links": links}


def _lang_ok(lang: str) -> str:
    return lang if lang in T else "pt"


def html_indice(lang: str) -> str:
    d = carregar()
    return indice(d["paises"], d["glos"], _lang_ok(lang))


def html_ficha(iso: str, lang: str) -> str:
    d = carregar()
    p = next(x for x in d["paises"] if x["iso"] == iso)
    return ficha(p, d["instr"], d["evid"], d["lac"], _lang_ok(lang))


def html_dados(lang: str) -> str:
    d = carregar()
    return dados_pagina(d["evid"], d["fontes"], d["legenda"], d["paises"], _lang_ok(lang), d["links"])


def main():
    d = carregar()
    paises, instr, evid, lac, glos = d["paises"], d["instr"], d["evid"], d["lac"], d["glos"]
    fontes_lista, legenda_verif, sim, links = d["fontes"], d["legenda"], d["sim"], d["links"]
    if PREVIA.exists():
        shutil.rmtree(PREVIA)
    (PREVIA / "assets").mkdir(parents=True)
    (PREVIA / "assets" / "style.css").write_text(CSS, encoding="utf-8")
    if LOGO.exists():
        shutil.copy(LOGO, PREVIA / "assets" / LOGO.name)
    for lang in ("pt", "en"):
        pasta = PREVIA / lang
        pasta.mkdir()
        (pasta / "index.html").write_text(indice(paises, glos, lang), encoding="utf-8")
        (pasta / "dados.html").write_text(dados_pagina(evid, fontes_lista, legenda_verif, paises, lang, links), encoding="utf-8")
        (pasta / "simulacoes.html").write_text(simulacoes_pagina(sim, lang), encoding="utf-8")
        for p in paises:
            (pasta / f"{p['iso']}.html").write_text(ficha(p, instr, evid, lac, lang), encoding="utf-8")
    (PREVIA / "index.html").write_text('<!DOCTYPE html><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=pt/index.html">', encoding="utf-8")
    n = len(list(PREVIA.rglob("*.html")))
    print(f"{n} páginas em {PREVIA}")


if __name__ == "__main__":
    main()
