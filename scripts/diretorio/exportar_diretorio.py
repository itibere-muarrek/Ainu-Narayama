"""Fase 0 do Diretório do AINU.systems: exporta a planilha do Paper 3 para JSON.

Lê Matrizes_Operacionais_NTA_URSS_Narayama_v2.xlsx (fora do repositório) e
grava dois conjuntos em data/diretorio/:

  privado/    tudo, com o status de publicação de cada registro;
  publicavel/ só o que passa no filtro de auditoria (ver FILTRO abaixo).

Nada daqui é publicado: os JSON são insumo para as páginas das fases 1 e 2.
Uso:
    python scripts/diretorio/exportar_diretorio.py [caminho_da_planilha]

Regras do filtro (documentadas também em meta.json):
  - instrumentos: publicável só com fonte L1; "misto" (L1 + L2) sai como
    "publicavel_com_ressalva"; L2, "A confirmar" e indeterminado ficam retidos.
  - evidências (P1_Disponibilidade): publicáveis A, L e P; B é retido (página
    não aberta); N vai para as lacunas.
  - campos das fichas: retidos se o texto cita nível L2.
  - N*: retido do conjunto público enquanto o N*_Obs (PQDF-N*) não for
    recalculado; hoje a planilha só tem o N* consolidado do pipeline (v9.0).
  - auditoria interna (Auditoria_Pendencias): só no conjunto privado.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import openpyxl

RAIZ = Path(__file__).resolve().parents[2]
SAIDA = RAIZ / "data" / "diretorio"
PLANILHA_PADRAO = Path(r"C:\Users\LENOVO\Documents\i'M thinker\Papers\Paper 3 NTA\Matrizes_Operacionais_NTA_URSS_Narayama_v2.xlsx")
OVERRIDES = Path(__file__).with_name("overrides_nivel.json")
URLS_MANUAIS = Path(__file__).with_name("fontes_urls_manual.json")
REFERENCIAS = Path(__file__).with_name("referencias_metodo.json")          # fontes de método e de cálculo que não são séries da planilha
CONFERENCIA_NUMEROS = Path(__file__).with_name("conferencia_numeros_manual.json")
CONFERENCIA_MANUAL = Path(__file__).with_name("conferencia_manual.json")  # conferência de conteúdo feita à mão
# tipos de ID que são produtos derivados da própria planilha (não têm URL externa)
TIPOS_DERIVADOS = {"P34", "CENEMP", "CONTA", "P4", "P5HOR", "P5SIM", "P5CEN", "P5CMP", "MIPMULT", "CFC", "CFCC", "CFCCNTA", "CFCCTOT", "CONCCFCC", "IO", "IOCOORTE", "IOMULT",
                   "NTACMP", "P3CEN", "P3EMP", "P3GRF", "P3SET", "P3RASC", "P4AFI", "P4DIV", "P4MAT", "P6CMP", "NASC", "NP", "P7INC", "P8GRP", "P9MULT", "P10EXP", "P11IAG", "SHIWINV", "SHIWREG", "SHIWSTO"}
DESCRICAO_TIPO = {
    "ENGHO": "ENGHo 2017/18 (INDEC), microdados", "ENUT": "Encuesta de Uso del Tiempo (INDEC 2021; INEGI/INMUJERES 2019), microdados", "POF": "POF 2017–18 (IBGE), microdados",
    "ENIGH": "ENIGH 2024 (INEGI), microdados", "CE": "Consumer Expenditure Survey 2023–24 (BLS), microdados", "HBS": "Indagine sulle spese delle famiglie 2023 (ISTAT), arquivo público",
    "SHIW": "Indagine sui bilanci delle famiglie italiane, SHIW 2022 (Banca d'Italia)", "IO2015": "Tabelas de insumo-produto do Japão 2015 (e-Stat)", "SUT2020": "Tabelas de oferta e uso do Japão 2020 (e-Stat)",
    "IOBEA": "BEA, tabelas de insumo-produto dos EUA, 2023", "ATUS": "American Time Use Survey 2025 (BLS), tabelas publicadas", "PNADOFT": "PNAD Contínua, Outras formas de trabalho 2022 (IBGE)",
    "NTA": "NTA Data Sheet 2016 (perfis por idade)", "HCES": "MoSPI, Survey on Household Consumption Expenditure 2023-24 (NSS Report nº 592), relatório final",
}
VERSAO_ESQUEMA = "0.1.0"

PAISES = [  # ordem do Paper 3
    ("ITA", "Itália"), ("KOR", "Coreia do Sul"), ("JPN", "Japão"), ("MEX", "México"),
    ("ARG", "Argentina"), ("BRA", "Brasil"), ("USA", "Estados Unidos"), ("IND", "Índia"),
    ("NGA", "Nigéria"), ("FRA", "França"), ("CHN", "China"),
]
ISO_POR_NOME = {n: i for i, n in PAISES}
ZONAS = {
    "PEC": "Colapso de Narayama", "TA": "Tensão Acelerada",
    "PEA": "Ponto de Equilíbrio Autossustentável", "TP": "Tensão Populacional",
    "PEEC": "Saturação por Excesso de Contingente",
}
RE_ID = re.compile(r"AINU-[A-Z]{3}-[A-Z0-9]+-(?:\d{4}|NA)-\d{6}")

# (chave, prefixo do rótulo na P6_Comparativa, natureza)
CAMPOS_P6 = {
    "cobertura": [
        ("classe_provisoria", "Classe provisória", "ENTRADA"),
        ("perfil_consumo", "Perfil de consumo por idade", "OBS"),
        ("insumo_produto", "Insumo-produto", "OBS"),
        ("ano_contas", "Ano das contas por coorte", "OBS"),
        ("afi_tempo", "AFI (tempo de cuidado valorado)", "OBS"),
    ],
    "demografia": [
        ("tft_2025", "TFT em 2025", "OBS"),
        ("pop_2025_pct", "População 2025", "DER"),
        ("asc_estr_2025", "Ascendentes ÷ Estruturadores em 2025", "DER"),
        ("asc_estr_2075_tft_constante", "Ascendentes ÷ Estruturadores em 2075, TFT constante", "PROJ"),
        ("asc_estr_2075_wpp", "Ascendentes ÷ Estruturadores em 2075, WPP Medium", "PROJ"),
        ("dependencia_2025_2075_wpp", "Dependência (D+A) ÷ E", "PROJ"),
        ("estruturadores_2075_rel", "Estruturadores em 2075 em relação a 2025", "PROJ"),
        ("descendentes_2075_rel", "Descendentes em 2075 em relação a 2025", "PROJ"),
        ("carga_estr_2075_wpp", "Carga por Estruturador em 2075, WPP Medium", "PROJ"),
        ("carga_estr_2075_tft_constante", "Carga por Estruturador em 2075, TFT constante", "PROJ"),
        ("carga_estr_2075_rapida", "Carga por Estruturador em 2075, TFT 2,1", "PROJ"),
    ],
    "consumo": [
        ("cfcc_total_pct_desc_estr_asc", "CFCc total", "EST"),
        ("desc_privado_pesos_nta", "Descendentes no consumo privado, pesos NTA", "EST"),
        ("desc_privado_microdados_ancorados", "Descendentes no consumo privado, microdados ancorados", "EST"),
        ("desc_privado_regressao_bruta", "Descendentes no consumo privado, regressão bruta", "EST"),
        ("razao_0_24_sobre_25_64", "Razão 0–24 ÷ 25–64", "EST"),
        ("fator_ancoragem", "Fator de ancoragem", "EST"),
    ],
    "multiplicadores": [
        ("valor_adicionado", "Valor adicionado gerado", "EST"),
        ("importacoes", "Importações (diretas + indiretas)", "EST"),
        ("edpc_sobre_emprego", "EDPc total ÷ emprego modelado", "EST"),
    ],
    "valorizacao": [
        ("gasto_publico_familia_socx", "Gasto público em família, OECD SOCX", "OBS"),
        ("dividendo_10pct_pib", "Dividendo de 10% do gasto privado", "SIM"),
        ("maior_programa_infantil", "Maior programa infantil de renda", "OBS"),
        ("dividendo_sobre_programa", "Dividendo de 10% ÷", "SIM"),
        ("analogo_ifvi_empregador", "Análogo de IFVI com empregador", "OBS"),
    ],
}

GLOSSARIO = [
    ("Descendentes (Prometidos)", "Coorte de base (população jovem), com corte de idade próprio de cada país. Na tese V1_1: Prometidos.", "AINU.Systems; EcoPol V1_1 (tabela de perfis)"),
    ("Estruturadores", "Coorte de idades intermediárias; corresponde ao Provedor Geracional da tese (referência de 25 a 65 anos).", "AINU.Systems; EcoPol V1_1"),
    ("Ascendentes (Legadores)", "Coorte de topo (população idosa). Termo 'Legadores' confirmado pelo autor em 2026-11-01; a tese V1_1 ainda escreve 'Legatários'.", "Decisão do autor, 2026-11-01"),
    ("URSS (Unidade de Reprodução Social Sustentável)", "Estrutura funcional de caráter privado, familiar e civil que assume responsabilidade efetiva pela formação de Capital Humano Relacional (CHR) e pela continuidade geracional. Ativo civilizacional primário, não beneficiária de política social. Condição URSS: Ativa, Cumprida ou Inativa, por critério observável e independente da situação laboral.", "EcoPol V1_1, tabela V.I; src/i18n.py; Leia-me da planilha"),
    ("CHR (Capital Humano Relacional)", "A formação profissionalizante e socializante que os pais exercem sobre os filhos. Insubstituível, inelástica, sem remuneração.", "src/i18n.py"),
    ("UDE (Unidade Demográfica de Estado)", "O conjunto real das URSS existentes num dado momento; pertence a ela quem exerce responsabilidade efetiva pela formação e sustentação de ao menos um descendente de 0 a 25 anos, biológico ou adotivo. Leitura econômica: Investimento Total em UDE = NTA(0-25) + NTA(25-65) restrito aos Provedores em URSS (segundo termo sem fonte consolidada).", "EcoPol V1_1, seção 4.6"),
    ("CFCc", "Consumo Final por Coorte: despesa final atribuída à coorte.", "Leia-me da planilha"),
    ("CIEc", "Conteúdo Importado por Coorte: conteúdo estrangeiro direto e indireto.", "Leia-me da planilha"),
    ("VADc", "Valor Adicionado Doméstico atribuível à demanda final da coorte (não é PIB da coorte e não soma ao PIB).", "Leia-me da planilha"),
    ("EDPc", "Empregos Domésticos Sustentados pela demanda da coorte (bruto, deslocamento e líquido separados).", "Leia-me da planilha"),
    ("REAc", "Renda do trabalho apropriada por Estruturadores em URSS-Ativa; exige microdados.", "Leia-me da planilha"),
    ("AFI (Ativo de Formação Intergeracional)", "Investimento que os Estruturadores realizam em alimentação, habitação, saúde, educação, vestuário, transporte, proteção, desenvolvimento, cuidado cotidiano e acompanhamento e educação não remunerados. Nesta pesquisa é medido de forma operacional (gasto privado com a coorte de Descendentes, líquido de transferências, mais o valor do tempo de cuidado); as fórmulas seguem como proposta não aprovada.", "Protocolo v2.3 (seção A de Prompt 4)"),
    ("Dividendo Intergeracional", "Retorno parcial aos Estruturadores pelo investimento na formação de novas gerações. Não é salário, restituição integral dos gastos nem assistência convencional. Proposta do Narayama; aqui só simulado em custo.", "Protocolo v2.3"),
    ("IFVI (Incentivos Fiscais à Valorização Intergeracional)", "Benefícios tributários a agentes que ofereçam bens, serviços e infraestruturas que reduzam os custos e ampliem a sustentabilidade das URSS. Distinto do AFI e do Dividendo.", "Protocolo v2.3 (seção C de Prompt 4)"),
    ("N* (Índice de Narayama Sistêmico)", "N* = raiz quadrada de N_Base, com N_Base = NGII_puro × Fator_Geracional. Zonas: PEC < 0,71; Tensão Acelerada 0,71–0,90; PEA 0,90–1,40; Tensão Populacional 1,40–2,00; PEEC ≥ 2,00.", "EcoPol V1_1, seções V.II e 9-A.3"),
    ("PQDF-N*", "Protocolo de Qualidade, Decomposição e Falseabilidade do N*: o N*_Obs é sempre publicado; ajustes de migração, inércia, políticas e sub-registro são cenários separados (N*_k).", "EcoPol V1_1, Anexo 9"),
]

NATUREZAS = {
    "OBS": "Observado em fonte (equivale a [E] na tese)",
    "DER": "Derivado de dado observado por conta simples ([E])",
    "EST": "Estimado por modelo ([S])",
    "PROJ": "Projeção condicional a cenário ([C])",
    "SIM": "Simulação de mecanismo ([S])",
    "PROP": "Proposta conceitual do autor ([H])",
    "ENTRADA": "Entrada do plano ou regra provisória, não validada",
}


def texto(v) -> str | None:
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def numero(s: str):
    s = s.strip().replace("\u2212", "-")
    if re.fullmatch(r"-?\d+(?:[.,]\d+)?", s):
        return float(s.replace(",", "."))
    return None


def analisar(raw) -> dict:
    """Valor estruturado quando o texto é simples; o texto original sempre fica."""
    t = texto(raw)
    if t is None or t in ("—", "-"):
        return {"texto": t, "valor": None, "lacuna": True}
    if t.lower() in ("n/d", "n/c"):
        return {"texto": t, "valor": None, "lacuna": True}
    n = numero(t)
    if n is not None:
        return {"texto": t, "valor": n}
    partes = re.split(r"\s*(?:/|→)\s*", t)
    if len(partes) > 1 and all(numero(p) is not None for p in partes):
        return {"texto": t, "valor": [numero(p) for p in partes]}
    return {"texto": t, "valor": None}


def nivel_fonte(*campos) -> str:
    t = " ".join(c for c in (texto(x) for x in campos) if c)
    l1, l2 = bool(re.search(r"\bL1\b", t)), bool(re.search(r"\bL2\b", t))
    if l1 and l2:
        return "misto"
    if l1:
        return "L1"
    if l2:
        return "L2"
    if re.search(r"A confirmar|Lacuna|NÃO encontrad|Não encontrad", t, re.I):
        return "lacuna"
    return "indeterminado"


def ids_em(*campos) -> list[str]:
    out: list[str] = []
    for c in campos:
        out += RE_ID.findall(texto(c) or "")
    return sorted(set(out))


def carregar_overrides() -> dict:
    if OVERRIDES.exists():
        return json.loads(OVERRIDES.read_text(encoding="utf-8"))
    return {}


def construir(wb):
    avisos: list[str] = []
    overrides = carregar_overrides()

    # ---------- fichas dos países ----------
    p6 = list(wb["P6_Comparativa"].iter_rows(values_only=True))
    cab = next(r for r in p6 if r[0] == "Indicador")
    colunas = {ISO_POR_NOME[n]: i for i, n in enumerate(cab) if n in ISO_POR_NOME}
    assert len(colunas) == 11, colunas

    def linha(prefixo):
        achadas = [r for r in p6 if isinstance(r[0], str) and r[0].startswith(prefixo)]
        assert len(achadas) == 1, (prefixo, len(achadas))
        return achadas[0]

    amostra = {r[1]: r for r in wb["Amostra_11_Paises"].iter_rows(min_row=2, values_only=True) if r[1]}
    coortes = {r[1]: r for r in wb["P1_Coortes_Narayama"].iter_rows(min_row=2, values_only=True) if r[6] == 2025}
    comp = list(wb["P1_Comparativa"].iter_rows(values_only=True))
    comp_cab = comp[0]
    comp_por_iso = {r[1]: r for r in comp[1:] if r[1]}

    # incremento por criança adicional (aba P7), só para países com insumo-produto
    p7 = list(wb["P7_Incremento_Crianca"].iter_rows(values_only=True))
    h7 = next(k for k, r in enumerate(p7) if r[0] == "País" and r[1] == "ISO")
    incr = {}
    for r in p7[h7 + 1:]:
        if not r[1]:
            break
        incr[r[1]] = {
            "disponivel": True, "natureza": "EST", "n_pontos": r[4],
            "unidade_consumo": r[2], "unidade_vad": r[3],
            "vad_por_crianca_ano": {"mediana": r[5], "min": r[6], "max": r[7]},
            "cfcc_por_crianca_ano": r[8], "vad_sobre_cfcc": r[9],
            "empregos_brutos_por_crianca": {"mediana": r[10], "min": r[11], "max": r[12]},
            "empregos_liquidos_50": r[13], "empregos_liquidos_100": r[14], "criancas_por_emprego_bruto": r[15],
            "aviso": "Limite superior de demanda por criança adicional e por ano na coorte; não é efeito causal nem inclui a produção futura da criança.",
            "fonte": "P7_Incremento_Crianca (derivada de P3_Empregos_Temporal e *_Cenarios_Emp)",
        }

    # composição do consumo por grupo de atividade (aba P8), 4 países com microdados
    p8 = list(wb["P8_Composicao_Grupos"].iter_rows(values_only=True))
    h8 = next(k for k, r in enumerate(p8) if r[0] == "País" and r[2] == "Grupo de atividade")
    comp8: dict = {}
    for r in p8[h8 + 1:]:
        if not r[1]:
            break
        d = comp8.setdefault(r[1], {"grupos": [], "fonte": r[15], "natureza": "EST"})
        d["grupos"].append({"grupo": r[2],
                            "descendentes": {"marginal": r[3], "marginal_p5": r[4], "marginal_p95": r[5], "medio": r[6]},
                            "estruturadores": {"marginal": r[7], "marginal_p5": r[8], "marginal_p95": r[9], "medio": r[10]},
                            "ascendentes": {"marginal": r[11], "marginal_p5": r[12], "marginal_p95": r[13], "medio": r[14]}})
    h8b = next(k for k, r in enumerate(p8) if r[2] == "Domicílios (n)")
    for r in p8[h8b + 1:]:
        if not r[1]:
            break
        comp8[r[1]].update({"domicilios": r[2], "cobertura_gastos": r[3], "sobreposicao_desc_asc": {"marginal": r[4], "medio": r[5]},
                            "sobreposicao_desc_estr": {"marginal": r[6], "medio": r[7]}, "disponivel": True,
                            "aviso": "Só gasto privado das famílias; marginal = o que mais uma pessoa da coorte acrescenta ao gasto do domicílio, médio = divisão igual do gasto do domicílio."})

    # multiplicadores por grupo e decomposição da demanda (aba P9)
    p9 = list(wb["P9_Multiplicadores_Grupos"].iter_rows(values_only=True))
    ha = next(k for k, r in enumerate(p9) if r[0] == "País" and r[3] == "Parcela do gasto das famílias (%)")
    hb = next(k for k, r in enumerate(p9) if r[0] == "País" and r[3] == "VAD Desc. marginal")
    mult9: dict = {}
    for r in p9[ha + 1:]:
        if not r[1]:
            break
        d = mult9.setdefault(r[1], {"grupos": {}, "unidade_emprego": r[7], "metodo_emprego": r[8], "ano_base": r[9], "natureza": "EST"})
        d["grupos"][r[2]] = {"grupo": r[2], "parcela_gasto_pct": r[3], "vad_por_unidade": r[4], "importacao_direta": r[5], "empregos_por_milhao": r[6]}
    for r in p9[hb + 1:]:
        if not r[1]:
            break
        g = mult9[r[1]]["grupos"][r[2]]
        g["vad_participacao"] = {"descendentes": {"marginal": r[3], "medio": r[4]}, "ascendentes": {"marginal": r[5], "medio": r[6]}}
        g["emprego_participacao"] = {"descendentes": {"marginal": r[7], "medio": r[8]}, "ascendentes": {"marginal": r[9], "medio": r[10]}}
    for iso_, d in mult9.items():
        d["disponivel"] = True
        d["grupos"] = list(d["grupos"].values())
        d["aviso"] = ("Emprego por grupo por seção ISIC da OIT (20 seções): separa, por exemplo, educação de finanças, mas produtos da mesma seção têm a mesma intensidade." if d["metodo_emprego"].startswith("seções ISIC") else
                      "Emprego por produto da própria tabela de insumo-produto, conferido com as seções ISIC da OIT.")

    # exposição à automação (aba P10)
    p10 = list(wb["P10_Exposicao_Automacao"].iter_rows(values_only=True))
    hg = next(k for k, r in enumerate(p10) if r[0] == "País" and r[2] == "Grupo de atividade" and r[3] == "Probabilidade média")
    hc = next(k for k, r in enumerate(p10) if r[0] == "País" and r[2] == "Coorte")
    exp10: dict = {}
    for r in p10[hg + 1:]:
        if not r[1]:
            break
        d = exp10.setdefault(r[1], {"grupos": [], "coortes": {}, "natureza": "EST", "fonte": "Frey e Osborne (2013), cruzamento BLS SOC-ISCO e OIT (emprego por atividade e ocupação)"})
        d["grupos"].append({"grupo": r[2], "media": r[3], "baixa": r[4], "alta": r[5], "fracao_alta": r[6], "fracao_baixa": r[7]})
    for r in p10[hc + 1:]:
        if not r[1]:
            break
        exp10[r[1]]["coortes"][f"{'descendentes' if r[2] == 'Descendentes' else 'ascendentes'}_{r[3]}"] = {"media": r[4], "baixa": r[5], "alta": r[6], "fracao_alta": r[7], "fracao_baixa": r[8]}
    for d in exp10.values():
        d["disponivel"] = True
        d["aviso"] = ("Exposição técnica à automação (probabilidade de informatização de ocupações dos EUA em 2013), não previsão de perda de emprego; a IA generativa está na aba P11, só como base de referência.")

    # exposição à IA generativa (aba P11)
    p11 = list(wb["P11_Exposicao_IA_Generativa"].iter_rows(values_only=True))
    hg11 = next(k for k, r in enumerate(p11) if r[0] == "País" and r[2] == "Grupo de atividade" and r[3] == "Escore médio")
    hc11 = next(k for k, r in enumerate(p11) if r[0] == "País" and r[2] == "Coorte")
    exp11: dict = {}
    for r in p11[hg11 + 1:]:
        if not r[1]:
            break
        d = exp11.setdefault(r[1], {"grupos": [], "coortes": {}, "natureza": "EST", "fonte": "OIT, Working Paper 140 (2025), Tabela A1, e OIT/ILOSTAT (emprego por atividade e ocupação)"})
        d["grupos"].append({"grupo": r[2], "media": r[3], "baixa": r[4], "alta": r[5], "fracao_alta": r[6], "fracao_baixa": r[7]})
    for r in p11[hc11 + 1:]:
        if not r[1]:
            break
        exp11[r[1]]["coortes"][f"{'descendentes' if r[2] == 'Descendentes' else 'ascendentes'}_{r[3]}"] = {"media": r[4], "baixa": r[5], "alta": r[6], "fracao_alta": r[7], "fracao_baixa": r[8]}
    for d in exp11.values():
        d["disponivel"] = True
        d["aviso"] = "Exposição das tarefas ocupacionais à IA generativa (índice global da OIT); indica sobretudo transformação de ocupações, não previsão de perda de emprego."

    # consumo observado da Índia (relatório do HCES 2023-24)
    pi = list(wb["IND_Consumo_HCES"].iter_rows(values_only=True))
    ia = next(k for k, r in enumerate(pi) if r[0] == "Indicador")
    ib = next(k for k, r in enumerate(pi) if r[0] and str(r[0]).startswith("Grupo de itens"))
    niveis = []
    for r in pi[ia + 1:]:
        if not r[0]:
            break
        niveis.append({"indicador": r[0], "rural": r[1], "urbano": r[2], "pagina": r[3]})
    grupos_ind = []
    for r in pi[ib + 1:]:
        if not r[0]:
            break
        grupos_ind.append({"grupo": r[0], "rural_rs": r[1], "urbano_rs": r[2], "rural_pct": r[3], "urbano_pct": r[4], "tipo": r[5]})
    consumo_ind = {"disponivel": True, "natureza": "OBS", "niveis": niveis, "grupos": grupos_ind, "id": "AINU-IND-HCES-2024-000633",
                   "fonte": "MoSPI, NSO, Survey on Household Consumption Expenditure 2023-24 (NSS Report nº 592), capítulo 3 e Statements 9 e 15",
                   "aviso": "Médias sobre toda a população; os grupos são os do relatório, não os 8 grupos do Paper 3. O relatório não traz idade nem composição por coorte."}

    fichas = []
    for iso, nome in PAISES:
        f: dict = {"iso": iso, "nome": nome}
        c = coortes[iso]
        f["coortes"] = {"composicao_perfis": c[2], "descendentes": c[3], "estruturadores": c[4], "ascendentes": c[5],
                        "ano_referencia": 2025, "fonte": "P1_Coortes_Narayama"}
        a = amostra[iso]
        f["n_star"] = {
            "valor_plano_v5": a[2], "valor_pipeline_2024": a[4], "zona_sigla": a[3], "zona": ZONAS.get(a[3], a[3]),
            "natureza": "CONSOLIDADO_v9.0",
            "aviso": "N* consolidado do pipeline (com a calibração de falseabilidade da v9.0). Não é o N*_Obs do PQDF-N*, ainda não recalculado.",
        }
        i = colunas[iso]
        for bloco, itens in CAMPOS_P6.items():
            f[bloco] = {}
            for chave, prefixo, nat in itens:
                reg = analisar(linha(prefixo)[i])
                reg["natureza"] = nat
                if reg.get("texto") and re.search(r"\bL2\b", reg["texto"]):
                    reg["nivel"] = "L2"
                f[bloco][chave] = reg
        f["consumo_observado"] = consumo_ind if iso == "IND" else {"disponivel": False}
        f["exposicao_iagen"] = exp11.get(iso, {"disponivel": False, "motivo": "sem multiplicadores por grupo nesta rodada"})
        f["exposicao_automacao"] = exp10.get(iso, {"disponivel": False, "motivo": "sem multiplicadores por grupo nesta rodada"})
        f["multiplicadores_grupos"] = mult9.get(iso, {"disponivel": False, "motivo": "sem tabela de insumo-produto com microdados de orçamento harmonizados nesta rodada"})
        f["composicao_grupos"] = comp8.get(iso, {"disponivel": False, "motivo": "categorias do SHIW não harmonizadas por grupo nesta rodada" if iso == "ITA" else "sem microdados de orçamento familiar harmonizados nesta rodada"})
        f["incremento_crianca"] = incr.get(iso, {"disponivel": False, "motivo": "sem tabela de insumo-produto nesta rodada"})
        cr = comp_por_iso[iso]
        f["disponibilidade_de_dados"] = {}
        for k in range(2, len(comp_cab)):
            t = texto(cr[k])
            m = re.match(r"\[([A-Z])\]\s*", t or "")
            f["disponibilidade_de_dados"][str(comp_cab[k])] = {"texto": t, "verificacao": m.group(1) if m else None}
        fichas.append(f)

    # ---------- evidências ----------
    ev_rows = list(wb["P1_Disponibilidade"].iter_rows(values_only=True))
    ev_cab = ev_rows[0]
    evidencias, legenda_verif = [], None
    for r in ev_rows[1:]:
        if r[0] and str(r[0]).startswith("Legenda"):
            legenda_verif = r[0]
            continue
        if r[0] and str(r[1] or "").strip() == "" and len(str(r[0])) > 60:
            legenda_verif = r[0]
            continue
        if not r[0] and r[2] is not None and len(str(r[2])) > 60:
            legenda_verif = r[2]
            continue
        if not r[0] or not RE_ID.fullmatch(str(r[0])):
            continue
        v = texto(r[10])
        status = {"A": "publicavel", "L": "publicavel", "P": "publicavel", "B": "retido", "N": "lacuna"}.get(v, "retido")
        evidencias.append({
            "id": r[0], "iso": r[2], "bloco": texto(r[3]), "variavel": texto(r[4]), "fonte": texto(r[5]),
            "serie": texto(r[6]), "ano_inicial": texto(r[7]), "ano_final": texto(r[8]), "n_anos": texto(r[9]),
            "verificacao": v, "observacao": texto(r[11]), "status_publicacao": status,
        })

    # ---------- IDs citados em qualquer aba ----------
    citados: dict[str, set] = {}
    for ws in wb.worksheets:
        for row in ws.iter_rows(values_only=True):
            for cel in row:
                if isinstance(cel, str):
                    for m in RE_ID.findall(cel):
                        citados.setdefault(m, set()).add(ws.title)
    ids_citados = [
        {"id": k, "iso": k.split("-")[1], "tipo": k.split("-")[2], "abas": sorted(v)}
        for k, v in sorted(citados.items())
    ]
    registrados = {e["id"] for e in evidencias}
    registrados_ev = {e["id"]: e for e in evidencias}
    sem_registro = [x["id"] for x in ids_citados if x["id"] not in registrados]

    # ---------- instrumentos ----------
    instrumentos = []

    def adicionar(iso, linha_, fonte_txt, status_txt, aba):
        nome_instr = texto(linha_[0])
        chave = f"{iso}|{nome_instr}"
        nivel = overrides.get(chave, {}).get("nivel") or nivel_fonte(fonte_txt, status_txt)
        if nivel == "indeterminado" and not re.match(r"(A confirmar|Lacuna|n/d)", status_txt or "", re.I):
            avisos.append(f"nível indeterminado: {chave}")
        gate = {"L1": "publicavel", "misto": "publicavel_com_ressalva", "lacuna": "lacuna"}.get(nivel, "retido")
        # status explícito de pendência ou de dado inexistente prevalece sobre o nível da fonte
        if re.match(r"(A confirmar|Lacuna|n/d)", status_txt or "", re.I):
            gate = "lacuna"
        instrumentos.append({
            "iso": iso, "instrumento": nome_instr, "tipo": texto(linha_[1]), "beneficiario": texto(linha_[2]),
            "valor": texto(linha_[3]), "duracao_financiamento": texto(linha_[4]), "custo_fiscal": texto(linha_[5]),
            "resultados": texto(linha_[6]), "fonte_e_nivel": fonte_txt, "status": status_txt,
            "nivel": nivel, "status_publicacao": gate, "evidencias": ids_em(fonte_txt, status_txt, linha_[5]),
            "aba": aba,
        })

    for iso, nome in PAISES:
        if iso == "ITA":
            continue
        nome_aba = f"{iso}_Prompt4"
        rows = list(wb[nome_aba].iter_rows(values_only=True))
        h = next(k for k, r in enumerate(rows) if r[0] == "Instrumento")
        for r in rows[h + 1:]:
            if r[0] is None or r[1] is None:
                break
            adicionar(iso, r[0:7], texto(r[7]), texto(r[8]), nome_aba)
    m = list(wb["P4_Matriz_Instrumentos"].iter_rows(values_only=True))
    for r in m[2:]:
        if r[0] == "Itália" and r[1]:
            adicionar("ITA", r[1:8], texto(r[8]), None, "P4_Matriz_Instrumentos")
    socx = []
    for r in m:
        if r[0] in {i for i, _ in PAISES} and r[1] and re.fullmatch(r"\d{4}", str(r[1])):
            socx.append({"iso": r[0], "ano": int(r[1]), "abonos_familiares": texto(r[2]), "licenca": texto(r[3]),
                         "dinheiro_outros": texto(r[4]), "ecec": texto(r[5]), "apoio_domiciliar_moradia": texto(r[6]),
                         "outros_em_especie": texto(r[7]), "total_pct_pib": texto(r[8]), "natureza": "OBS",
                         "fonte": "OECD SOCX (coleta em P4_Matriz_Instrumentos)", "status_publicacao": "publicavel"})

    # ---------- registro unificado de fontes (fase 2) ----------
    urls_manuais = json.loads(URLS_MANUAIS.read_text(encoding="utf-8")) if URLS_MANUAIS.exists() else {}
    inv = {}
    for r in wb["Inventario_Dados"].iter_rows(min_row=2, values_only=True):
        if r[0] and str(r[0]).startswith("AINU"):
            inv[r[0]] = {"iso": r[0].split("-")[1], "descricao": f"{texto(r[2])} ({texto(r[1])})", "url": texto(r[6]), "obs": texto(r[11])}
    desc_instr: dict[str, str] = {}
    for it in instrumentos:
        for i_ in it["evidencias"]:
            desc_instr.setdefault(i_, f"{it['instrumento']}: {it['fonte_e_nivel'] or ''}"[:300])
    def url_de_serie(e_):
        """URL a partir da fonte (quando é endereço) ou do código da série (WDI, ILOSTAT, WPP, NTA)."""
        f_, c_ = e_["fonte"] or "", e_["serie"] or ""
        if f_.startswith("http"):
            return f_, "registrada"
        if "WDI" in f_ and re.fullmatch(r"[A-Z0-9_.]+", c_):
            return f"https://data.worldbank.org/indicator/{c_}", "derivada_do_codigo"
        if "ILOSTAT" in f_ and re.fullmatch(r"[A-Z0-9_]+", c_):
            return f"https://rplumber.ilo.org/data/indicator/?id={c_}&ref_area={e_['iso']}&format=.csv", "derivada_do_codigo"
        if "WPP" in f_ or "World Population Prospects" in f_:
            return "https://population.un.org/wpp/", "derivada_do_codigo"
        if "National Transfer Accounts" in f_:
            return "https://www.ntaccounts.org/doc/repository/NTA%20Data%20Sheet%202016.pdf", "registrada"
        if "ILOSTAT" in f_:
            return "https://ilostat.ilo.org/data/", "derivada_do_codigo"       # série composta: portal geral
        return None, None

    fontes = []
    for x in ids_citados:
        i_ = x["id"]
        if i_ in registrados_ev:
            e_ = registrados_ev[i_]
            u_, o_ = url_de_serie(e_)
            u_ = urls_manuais.get(i_) or u_
            fontes.append({"id": i_, "iso": x["iso"], "tipo": x["tipo"], "origem": "P1_Disponibilidade", "descricao": f"{e_['variavel']} ({e_['bloco']}); série {e_['serie']}",
                           "fonte": e_["fonte"] if not (e_["fonte"] or "").startswith("http") else None, "url": u_, "url_origem": o_ if u_ else None,
                           "url_status": "registrado" if u_ else "a_registrar", "verificacao": e_["verificacao"], "abas": x["abas"]})
        elif i_ in inv:
            fontes.append({"id": i_, "iso": x["iso"], "tipo": x["tipo"], "origem": "Inventario_Dados", "descricao": inv[i_]["descricao"], "fonte": None,
                           "url": inv[i_]["url"] if (inv[i_]["url"] or "").startswith("http") else urls_manuais.get(i_), "url_status": "registrado" if ((inv[i_]["url"] or "").startswith("http") or urls_manuais.get(i_)) else "a_registrar",
                           "verificacao": None, "abas": x["abas"]})
        elif x["tipo"] in TIPOS_DERIVADOS:
            fontes.append({"id": i_, "iso": x["iso"], "tipo": x["tipo"], "origem": "derivado", "descricao": "Produto derivado da planilha de pesquisa (ver abas citantes)", "fonte": None,
                           "url": None, "url_status": "nao_aplicavel", "verificacao": None, "abas": x["abas"]})
        else:
            fontes.append({"id": i_, "iso": x["iso"], "tipo": x["tipo"], "origem": "descrita_na_aba", "descricao": desc_instr.get(i_) or DESCRICAO_TIPO.get(x["tipo"], "Fonte descrita nas abas citantes"), "fonte": None,
                           "url": urls_manuais.get(i_), "url_status": "registrado" if urls_manuais.get(i_) else "a_registrar", "verificacao": None, "abas": x["abas"]})

    # ---------- lacunas e auditoria ----------
    nao_enc = [{"pais": r[0], "item": texto(r[1]), "situacao": texto(r[2]), "tentativas": texto(r[3]), "proximo_passo": texto(r[4])}
               for r in wb["P1_Nao_Encontrados"].iter_rows(min_row=2, values_only=True) if r[0]]
    auditoria = [{"pais": r[0], "item": texto(r[1]), "fontes_candidatas_nao_verificadas": texto(r[2]), "status": texto(r[3])}
                 for r in wb["Auditoria_Pendencias"].iter_rows(min_row=2, values_only=True) if r[0]]
    return fichas, evidencias, legenda_verif, ids_citados, sem_registro, instrumentos, socx, nao_enc, auditoria, avisos, fontes


def filtrar_ficha(f: dict) -> dict:
    """Versão pública da ficha: sem N* consolidado e sem campos citando L2."""
    g = json.loads(json.dumps(f))
    g.pop("n_star", None)
    g["n_star_pendente"] = "N*_Obs (PQDF-N*) ainda não recalculado; N* consolidado do pipeline retido."
    for bloco in ("cobertura", "demografia", "consumo", "multiplicadores", "valorizacao"):
        for k, reg in g[bloco].items():
            if reg.get("nivel") == "L2":
                g[bloco][k] = {"retido": True, "motivo": "fonte de nível L2 (original não lido)", "natureza": reg["natureza"]}
    for k, reg in g["disponibilidade_de_dados"].items():
        if reg["verificacao"] == "B":
            g["disponibilidade_de_dados"][k] = {"retido": True, "motivo": "resultado de busca, página não aberta"}
    return g


def _num(x):
    if x is None:
        return None
    try:
        return float(str(x).replace(",", ".").replace("−", "-"))
    except ValueError:
        return None


def _fontes_da_pagina(iso: str, fontes: list[dict], evid: list[dict], refs: list[dict]) -> list[dict]:
    """Fontes principais do país para o rodapé da página de simulação: tudo menos as séries WDI, ILOSTAT e WPP, que entram como uma linha cada."""
    nomes = json.loads(Path(__file__).with_name("nomes_fontes.json").read_text(encoding="utf-8"))
    ev = {x["id"]: x for x in evid}
    vistos: dict[str, dict] = {}
    for f in fontes:
        if f["iso"] != iso or not f.get("url"):
            continue
        if f["tipo"] in ("WDI", "ILO"):
            continue
        x = ev.get(f["id"])
        nome = nomes.get(f["id"]) or (f"{x['variavel']} ({x['serie']})" if x and x.get("serie") else x["variavel"] if x else (f["descricao"] or f["id"]).split(": AINU")[0])
        vistos.setdefault(f["url"], {"nome": nome, "url": f["url"], "ids": []})["ids"].append(f["id"])
    saida = list(vistos.values())
    for r in refs:
        if iso in r["paises"] and r["chave"] in ("socx", "eurostat_io", "eurostat_emp"):
            saida.append({"nome": r["nome"], "url": r["url"], "ids": []})
    return saida


def montar_simulacoes(wb, fichas: list[dict], fontes: list[dict] | None = None, evid: list[dict] | None = None, refs: list[dict] | None = None) -> dict:
    """Insumos da página de simulação (fase 3): só números já publicados nas fichas e na aba P5.

    Parte das fichas (filtradas ou não), de modo que o conjunto publicável herda o filtro de auditoria
    (programa de nível L2 sai sem valor). Nada é calculado aqui além do que a página escala linearmente.
    """
    ws = wb["P5_Simulacoes_Paises"]
    sheet = {r[0]: r for r in ws.iter_rows(min_row=3, values_only=True) if r[0]}
    hor: dict[str, list] = {}
    for r in wb["P5_Horizontes_Paises"].iter_rows(min_row=3, values_only=True):
        if not r[0] or r[0] not in ISO_POR_NOME:
            continue
        hor.setdefault(ISO_POR_NOME[r[0]], []).append({
            "horizonte": texto(r[1]), "ano": int(float(r[2])), "cenario": texto(r[3]), "tft": _num(r[4]),
            "delta_desc_pct": _num(r[5]), "delta_estr_pct": _num(r[6]), "delta_asc_pct": _num(r[7]),
            "delta_cfcc_total_pct": _num(r[8]), "delta_consumo_publico_pct": _num(r[9])})
    out = {}
    for f in fichas:
        iso, v = f["iso"], f["valorizacao"]
        d10 = v["dividendo_10pct_pib"].get("valor")
        item: dict = {"iso": iso, "nome": f["nome"], "natureza_dividendo": "SIM"}
        if isinstance(d10, (int, float)):
            item["dividendo_10pct_pib"] = d10
            linha_ = sheet[f["nome"]]
            for pct, col in ((25, 2), (50, 3)):                       # a escala linear da página tem de reproduzir a planilha
                ref = _num(linha_[col])
                assert ref is not None and abs(ref - d10 * pct / 10) <= 0.02, (iso, pct, ref, d10)
        else:
            item["dividendo_10pct_pib"] = None
        item["base_consumo_descendentes"] = texto(sheet[f["nome"]][8])
        pr = v["maior_programa_infantil"]
        m = re.match(r"^(.*?):\s*[≈~]?\s*([\d.,]+)%\s*do PIB\s*\((.*?)\)", pr.get("texto") or "")
        if pr.get("retido") or not m:
            item["programa"] = {"nome": None, "pct_pib": None, "ano": None, "texto": pr.get("texto"), "retido": bool(pr.get("retido"))}
        else:
            item["programa"] = {"nome": m.group(1), "pct_pib": _num(m.group(2)), "ano": m.group(3), "texto": pr["texto"], "retido": False,
                                "ressalva": bool(re.search(r"derivado|≈|~", pr["texto"]))}
        so = v["gasto_publico_familia_socx"]
        m2 = re.match(r"^([\d.,]+)\s*\((\d{4})\)", so.get("texto") or "")
        item["gasto_publico_familia"] = {"pct_pib": _num(m2.group(1)), "ano": int(m2.group(2)), "fonte": "OECD SOCX"} if m2 and not so.get("retido") else None
        inc = f.get("incremento_crianca", {})
        item["incremento_crianca"] = inc if inc.get("disponivel") else {"disponivel": False}
        item["horizontes"] = hor.get(iso, [])
        item["fontes"] = _fontes_da_pagina(iso, fontes or [], evid or [], refs or [])
        out[iso] = item
    return {
        "natureza": "SIM",
        "regra": "O custo do Dividendo é proporcional à porcentagem x do gasto privado por Descendente: custo(x) = x/10 × custo(10%). A escala foi conferida contra os 25% e 50% da planilha.",
        "paises": out,
    }


def gravar(pasta: Path, nome: str, obj):
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / nome).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")


def main():
    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else PLANILHA_PADRAO
    wb = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
    fichas, evid, legenda, ids_cit, sem_reg, instr, socx, nao_enc, aud, avisos, fontes = construir(wb)

    sha = hashlib.sha256(caminho.read_bytes()).hexdigest()
    contagem = lambda lst, campo="status_publicacao": {k: sum(1 for x in lst if x[campo] == k) for k in sorted({x[campo] for x in lst})}
    meta = {
        "esquema": VERSAO_ESQUEMA, "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "planilha": caminho.name, "planilha_sha256": sha, "idioma": "pt",
        "naturezas": NATUREZAS, "legenda_verificacao": legenda,
        "contagens": {"paises": len(fichas), "evidencias": contagem(evid), "instrumentos": contagem(instr),
                      "ids_citados": len(ids_cit), "ids_citados_sem_registro_em_P1": len(sem_reg), "fontes": {k: sum(1 for f in fontes if f["url_status"] == k) for k in ("registrado", "a_registrar", "nao_aplicavel")}},
        "filtro": __doc__.split("Regras do filtro")[1].strip(),
        "avisos": avisos + ["Termos: Descendentes (Prometidos), Estruturadores, Ascendentes (Legadores); a tese V1_1 ainda usa Legatários."],
        "publicacao": "Nada deste conjunto foi publicado. Uso interno até a fase 1 e a decisão do autor.",
        "autoria": "Itiberê L. G. C. Muarrek (pesquisa independente; AINU.Systems / Narayama)",
    }
    glos = [{"termo": t, "definicao": d, "fonte": f} for t, d, f in GLOSSARIO]

    # conjunto privado: tudo
    priv = SAIDA / "privado"
    gravar(priv, "meta.json", meta)
    gravar(priv, "paises.json", fichas)
    gravar(priv, "evidencias.json", evid)
    gravar(priv, "evidencias_citadas.json", ids_cit)
    gravar(priv, "instrumentos.json", {"instrumentos": instr, "socx": socx})
    gravar(priv, "lacunas.json", {"nao_encontrados": nao_enc, "auditoria_interna": aud})
    gravar(priv, "glossario.json", glos)
    gravar(priv, "fontes.json", fontes)
    ref_lista = json.loads(REFERENCIAS.read_text(encoding="utf-8"))
    conf_man = json.loads(CONFERENCIA_MANUAL.read_text(encoding="utf-8"))
    gravar(priv, "referencias.json", ref_lista)
    gravar(priv, "conferencia_manual.json", conf_man)
    conf_num = json.loads(CONFERENCIA_NUMEROS.read_text(encoding="utf-8"))
    gravar(priv, "conferencia_numeros_manual.json", conf_num)
    gravar(priv, "simulacoes.json", montar_simulacoes(wb, fichas, fontes, evid, ref_lista))
    pend = [f for f in fontes if f["url_status"] == "a_registrar"]
    import csv
    with open(priv / "fontes_urls_pendentes.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "iso", "origem", "descricao", "url_a_preencher"])
        for f in pend:
            w.writerow([f["id"], f["iso"], f["origem"], f["descricao"], ""])

    # conjunto publicável
    pub = SAIDA / "publicavel"
    gravar(pub, "meta.json", {**meta, "conjunto": "publicavel"})
    gravar(pub, "paises.json", [filtrar_ficha(f) for f in fichas])
    gravar(pub, "evidencias.json", [e for e in evid if e["status_publicacao"] == "publicavel"])
    gravar(pub, "instrumentos.json", {
        "instrumentos": [i for i in instr if i["status_publicacao"] in ("publicavel", "publicavel_com_ressalva")],
        "socx": socx})
    gravar(pub, "lacunas.json", {
        "nao_encontrados": [{k: v for k, v in x.items() if k != "proximo_passo"} for x in nao_enc]
        + [{"pais": e["iso"], "item": f"{e['variavel']} ({e['bloco']})", "situacao": "Não encontrado"} for e in evid if e["status_publicacao"] == "lacuna"]
        + [{"pais": i["iso"], "item": i["instrumento"], "situacao": i["status"] or i["nivel"]} for i in instr if i["status_publicacao"] == "lacuna"]})
    gravar(pub, "glossario.json", glos)
    gravar(pub, "referencias.json", ref_lista)
    gravar(pub, "conferencia_manual.json", conf_man)
    gravar(pub, "conferencia_numeros_manual.json", conf_num)
    gravar(pub, "simulacoes.json", montar_simulacoes(wb, [filtrar_ficha(f) for f in fichas], fontes, evid, ref_lista))
    gravar(pub, "fontes.json", [{k: v for k, v in f.items() if k != "fonte"} for f in fontes if f["origem"] != "descrita_na_aba" or f["url_status"] == "registrado" or True])

    # validações
    assert len(fichas) == 11
    ids = [e["id"] for e in evid]
    assert len(ids) == len(set(ids)), "IDs duplicados em P1_Disponibilidade"
    for i in json.loads((pub / "instrumentos.json").read_text(encoding="utf-8"))["instrumentos"]:
        assert i["nivel"] in ("L1", "misto"), i
    pub_txt = (pub / "paises.json").read_text(encoding="utf-8")
    assert '"n_star"' not in pub_txt

    # relatório do filtro
    ret = [i for i in instr if i["status_publicacao"] == "retido"]
    rel = [f"# Relatório do filtro de auditoria ({meta['gerado_em']})", "",
           f"Planilha: {caminho.name} (sha256 {sha[:12]}…)", "",
           f"- Países: {len(fichas)}", f"- Evidências (P1): {meta['contagens']['evidencias']}",
           f"- Instrumentos: {meta['contagens']['instrumentos']}",
           f"- IDs citados nas abas: {len(ids_cit)} (sem registro em P1_Disponibilidade: {len(sem_reg)})", "",
           "## Instrumentos retidos (nível L2, indeterminado ou a confirmar)", ""]
    rel += [f"- {i['iso']} | {i['instrumento']} | nível {i['nivel']} | {i['status']}" for i in ret]
    rel += ["", "## Avisos", ""] + [f"- {a}" for a in avisos]
    (priv / "relatorio_filtro.md").write_text("\n".join(rel), encoding="utf-8")
    print("\n".join(rel[:12]))
    print("avisos:", len(avisos), "| retidos:", len(ret))


if __name__ == "__main__":
    main()
