"""
Protocolo de Falseabilidade do Índice de Narayama (AINU-Narayama v8.0).

Implementa os 7 testes descritos no Anexo 9 da tese, que transformam
o NGII_Bruto em NGII_Puro removendo fatores que mascaram a real
trajetória de sustentabilidade intergeracional:

    NGII Bruto -> Protocolo de Falseabilidade (7 Testes) -> NGII Puro -> N*

Cada teste retorna um veredito qualitativo ("aprovado"/"maquiagem
suspeita") e uma justificativa, já que a maior parte dos critérios do
Anexo 9 é definida em termos de séries históricas e comparações
qualitativas, não apenas limiares numéricos de um único ano.

Fonte: V1_EcoPol_062426_v8.0.docx, Anexo 9 — Protocolo de
Falseabilidade do Índice de Narayama (7 Testes).

Este arquivo também contém aplicar_protocolo_falseabilidade_simplificado(),
uma versão operacional de 3 testes para a Fase 1 do projeto, usada
enquanto os dados históricos ricos exigidos pelos 7 testes completos
(séries de 15+ anos, TFR nativa estimada, casos de choque) ainda não
estão disponíveis no pipeline.
"""

from typing import Any, Dict, List, Optional, Tuple


def teste_1_falseabilidade_migratoria(
    ngii_bruto: float, ngii_sem_migracao: float, limite: float = 0.15
) -> Dict[str, Any]:
    """
    TESTE 1 — Falseabilidade Migratória.

    Pergunta: O sistema continua sustentável quando os fluxos
    migratórios são removidos?

    Critério: diferença relativa > 12-15% entre NGII_Bruto e NGII sem
    saldo migratório indica maquiagem estatística (dependência
    estrutural da imigração).

    Args:
        ngii_bruto: NGII calculado com todos os fluxos populacionais.
        ngii_sem_migracao: NGII recalculado excluindo o saldo migratório.
        limite: Limite de diferença relativa aceitável (padrão 0.15).

    Returns:
        {"aprovado": bool, "diferenca_relativa": float, "motivo": str}
    """
    if not ngii_bruto:
        return {"aprovado": False, "diferenca_relativa": None, "motivo": "NGII_Bruto ausente ou zero"}

    diferenca_relativa = abs(ngii_bruto - ngii_sem_migracao) / ngii_bruto
    aprovado = diferenca_relativa <= limite

    motivo = (
        f"Diferença {diferenca_relativa:.1%} (limite {limite:.0%}): "
        + ("renovação predominantemente interna" if aprovado else "dependência estrutural da imigração")
    )

    return {"aprovado": aprovado, "diferenca_relativa": diferenca_relativa, "motivo": motivo}


def teste_2_falseabilidade_assistencial(
    crescimento_populacional: float, crescimento_base_provedora: float
) -> Dict[str, Any]:
    """
    TESTE 2 — Falseabilidade Assistencial.

    Pergunta: O crescimento observado gera novos provedores ou novos
    dependentes?

    Critério: quando o crescimento demográfico total não é
    acompanhado de expansão proporcional da base provedora (25-65),
    o NGII deve ser ajustado para baixo.

    Args:
        crescimento_populacional: Taxa de crescimento da população total no período.
        crescimento_base_provedora: Taxa de crescimento da coorte provedora (25-65) no período.

    Returns:
        {"aprovado": bool, "motivo": str}
    """
    aprovado = crescimento_base_provedora >= crescimento_populacional

    motivo = (
        "crescimento acompanhado de expansão proporcional da base provedora"
        if aprovado
        else "crescimento populacional não acompanhado pela base provedora — NGII_Bruto superestima capacidade real"
    )

    return {"aprovado": aprovado, "motivo": motivo}


def teste_3_falseabilidade_conjuntural(
    anos_deterioracao_pre_evento: Optional[int], limite_anos: int = 10
) -> Dict[str, Any]:
    """
    TESTE 3 — Falseabilidade Conjuntural.

    Pergunta: A tendência de deterioração observada já existia antes
    do evento disruptivo (guerra, pandemia, crise financeira, choque
    energético etc.)?

    Critério: se a deterioração do N* antecede o evento em mais de 10
    anos, o colapso é estrutural — não conjuntural.

    Args:
        anos_deterioracao_pre_evento: Quantos anos antes do evento
            disruptivo a deterioração do N* já era observável. None
            se não há evento disruptivo a avaliar (teste não se aplica).
        limite_anos: Limiar de anos para caracterizar colapso estrutural.

    Returns:
        {"aprovado": bool, "motivo": str}
        "aprovado" aqui significa "teste aplicado sem indício de
        maquiagem por atribuição indevida a evento conjuntural".
    """
    if anos_deterioracao_pre_evento is None:
        return {"aprovado": True, "motivo": "sem evento disruptivo a avaliar neste período"}

    estrutural = anos_deterioracao_pre_evento > limite_anos

    motivo = (
        f"deterioração antecede o evento em {anos_deterioracao_pre_evento} anos "
        f"(limite {limite_anos}): colapso {'estrutural' if estrutural else 'possivelmente conjuntural'}"
    )

    return {"aprovado": True, "estrutural": estrutural, "motivo": motivo}


def teste_4_falseabilidade_natalista(
    anos_desde_fim_da_politica: Optional[int], persistiu: bool, limite_anos: int = 10
) -> Dict[str, Any]:
    """
    TESTE 4 — Falseabilidade Natalista.

    Pergunta: O aumento de fertilidade persiste ao longo de um ciclo
    geracional completo (25 anos), ou é efeito de bônus, subsídio
    temporário ou programa eleitoral?

    Critério: apenas mudanças persistentes (> 10 anos após o fim da
    política) alteram significativamente o Fator_Geracional.

    Args:
        anos_desde_fim_da_politica: Anos passados desde o fim da
            política natalista avaliada. None se não há política a avaliar.
        persistiu: Se a elevação de TFR persistiu além de 5 anos após
            o fim da política.
        limite_anos: Limiar de anos para considerar a mudança persistente.

    Returns:
        {"aprovado": bool, "motivo": str}
    """
    if anos_desde_fim_da_politica is None:
        return {"aprovado": True, "motivo": "sem política natalista a avaliar neste período"}

    aprovado = persistiu and anos_desde_fim_da_politica > limite_anos

    motivo = (
        "elevação de TFR persistente, atribuível ao Fator_Geracional"
        if aprovado
        else "elevação de TFR não persistente — possível distorção por política temporária"
    )

    return {"aprovado": aprovado, "motivo": motivo}


def teste_5_falseabilidade_etaria(razao_filhos_mae: float) -> Dict[str, Any]:
    """
    TESTE 5 — Falseabilidade Etária.

    Pergunta: O crescimento observado decorre de renovação efetiva ou
    de inércia demográfica (geração numerosa gerando muitos
    nascimentos absolutos mesmo quando filhos < pais)?

    Critério: se a razão filhos/mãe < 1, o NGII_Bruto é inflado por
    inércia — não por renovação real.

    Args:
        razao_filhos_mae: Razão entre gerações sucessivas (nº de
            filhas por mulher em idade reprodutiva, relativa à geração anterior).

    Returns:
        {"aprovado": bool, "motivo": str}
    """
    aprovado = razao_filhos_mae >= 1.0

    motivo = (
        f"razão filhos/mãe {razao_filhos_mae:.3f}: "
        + ("renovação real" if aprovado else "inflado por inércia demográfica, não por renovação real")
    )

    return {"aprovado": aprovado, "motivo": motivo}


def teste_6_falseabilidade_substituicao_civilizacional(
    tfr_oficial: float, tfr_nativa_estimada: float, limite_diferenca: float = 0.25
) -> Dict[str, Any]:
    """
    TESTE 6 — Falseabilidade de Substituição Civilizacional.

    Pergunta: A estrutura demográfica observada está se reproduzindo
    (continuidade) ou sendo substituída pela entrada contínua de
    novos grupos com estrutura demográfica diferente (substituição)?

    Critério: quando a TFR nativa estimada é significativamente
    inferior à TFR oficial (diferença > 0.25), há sinal de
    substituição — não continuidade. Casos históricos exemplares:
    Suécia, Alemanha, Estados Unidos.

    Args:
        tfr_oficial: TFR oficial reportada para o país.
        tfr_nativa_estimada: TFR estimada apenas para a população nativa.
        limite_diferenca: Diferença absoluta de TFR que caracteriza substituição.

    Returns:
        {"aprovado": bool, "diferenca": float, "motivo": str}
    """
    diferenca = tfr_oficial - tfr_nativa_estimada
    aprovado = diferenca <= limite_diferenca

    motivo = (
        f"diferença TFR oficial-nativa {diferenca:.2f} (limite {limite_diferenca}): "
        + ("continuidade demográfica" if aprovado else "sinal de substituição civilizacional")
    )

    return {"aprovado": aprovado, "diferenca": diferenca, "motivo": motivo}


def teste_7_resistencia_a_choques(
    anos_antecedencia_sinal: Optional[int], limite_minimo_anos: int = 5
) -> Dict[str, Any]:
    """
    TESTE 7 — Resistência a Choques (Validação Empírica).

    Pergunta: O N* é capaz de demonstrar que a rarefação estrutural
    antecede o evento visível (guerra, crise política, ruptura
    econômica)? Casos de teste da tese: Ucrânia, Rússia, Irã, Síria,
    Japão, Alemanha, Coreia do Sul.

    Critério de sucesso: o N* deve sinalizar deterioração estrutural
    pelo menos 5-10 anos antes do evento visível nos casos de colapso
    estrutural — distinguindo colapso conjuntural (evento externo) de
    colapso estrutural (incapacidade persistente de renovação).

    Args:
        anos_antecedencia_sinal: Quantos anos antes do evento visível
            o N* já sinalizava deterioração estrutural. None se não
            há caso de choque a validar neste período.
        limite_minimo_anos: Antecedência mínima exigida (padrão 5 anos).

    Returns:
        {"aprovado": bool, "motivo": str}
    """
    if anos_antecedencia_sinal is None:
        return {"aprovado": True, "motivo": "sem caso de choque a validar neste período"}

    aprovado = anos_antecedencia_sinal >= limite_minimo_anos

    motivo = (
        f"N* sinalizou deterioração {anos_antecedencia_sinal} anos antes do evento "
        f"(mínimo exigido {limite_minimo_anos}): "
        + ("colapso estrutural confirmado" if aprovado else "sinal insuficiente para distinguir de colapso conjuntural")
    )

    return {"aprovado": aprovado, "motivo": motivo}


def aplicar_protocolo_falseabilidade(dados_pais: Dict[str, Any]) -> Dict[str, Any]:
    """
    Aplica os 7 testes do Protocolo de Falseabilidade (Anexo 9) a um país.

    Cada teste é aplicado apenas se os dados necessários estiverem
    presentes em `dados_pais`; testes sem dados suficientes (ex.: sem
    evento disruptivo ou sem política natalista a avaliar no período)
    retornam "aprovado" por vacuidade e devem ser reexecutados quando
    o dado relevante estiver disponível.

    Args:
        dados_pais: dicionário podendo conter as chaves:
            pais_nome,
            ngii_bruto, ngii_sem_migracao,
            crescimento_populacional, crescimento_base_provedora,
            anos_deterioracao_pre_evento,
            anos_desde_fim_da_politica_natalista, tfr_persistiu,
            razao_filhos_mae,
            tfr_oficial, tfr_nativa_estimada,
            anos_antecedencia_sinal_choque.

    Returns:
        {
            "passou": bool,
            "testes": {"teste_1": {...}, ..., "teste_7": {...}},
        }
    """
    testes = {}

    if "ngii_bruto" in dados_pais and "ngii_sem_migracao" in dados_pais:
        testes["teste_1_migratoria"] = teste_1_falseabilidade_migratoria(
            dados_pais["ngii_bruto"], dados_pais["ngii_sem_migracao"]
        )

    if "crescimento_populacional" in dados_pais and "crescimento_base_provedora" in dados_pais:
        testes["teste_2_assistencial"] = teste_2_falseabilidade_assistencial(
            dados_pais["crescimento_populacional"], dados_pais["crescimento_base_provedora"]
        )

    testes["teste_3_conjuntural"] = teste_3_falseabilidade_conjuntural(
        dados_pais.get("anos_deterioracao_pre_evento")
    )

    testes["teste_4_natalista"] = teste_4_falseabilidade_natalista(
        dados_pais.get("anos_desde_fim_da_politica_natalista"),
        dados_pais.get("tfr_persistiu", False),
    )

    if "razao_filhos_mae" in dados_pais:
        testes["teste_5_etaria"] = teste_5_falseabilidade_etaria(dados_pais["razao_filhos_mae"])

    if "tfr_oficial" in dados_pais and "tfr_nativa_estimada" in dados_pais:
        testes["teste_6_substituicao"] = teste_6_falseabilidade_substituicao_civilizacional(
            dados_pais["tfr_oficial"], dados_pais["tfr_nativa_estimada"]
        )

    testes["teste_7_resistencia_a_choques"] = teste_7_resistencia_a_choques(
        dados_pais.get("anos_antecedencia_sinal_choque")
    )

    return {
        "passou": all(t["aprovado"] for t in testes.values()),
        "testes": testes,
    }


def aplicar_protocolo_falseabilidade_simplificado(
    pais_codigo: str,
    ano: int,
    ngii_bruto: float,
    taxa_migracao_anual: float,
    proporcao_provedores: float,
) -> Optional[Tuple[float, List[str]]]:
    """
    Versão operacional simplificada (Fase 1) do Protocolo de Falseabilidade.

    Aplica 3 testes simplificados sobre o NGII_Bruto, em vez dos 7
    testes completos do Anexo 9 (ver aplicar_protocolo_falseabilidade()),
    que exigem dados históricos ricos ainda não disponíveis no
    pipeline desta fase (séries de 15+ anos, TFR nativa estimada,
    casos de choque). Deve ser substituída pela versão completa assim
    que esses dados estiverem disponíveis.

    Testes:
        1. Migração: se taxa_migracao_anual > 0.12, reduz o NGII em
           5% e alerta "Dependência migratória detectada".
        2. Estrutura de Provedores: se proporcao_provedores < 0.50,
           reduz o NGII (já ajustado pelo teste 1) em 10% e alerta
           "Compressão de provedores detectada".
        3. Conjuntura (simplificado): se ano == 2020, apenas alerta
           "Efeito conjuntural COVID-19", sem ajuste numérico.

    Args:
        pais_codigo: Código ISO3 do país (string de 3 caracteres, ex.: "BRA").
        ano: Ano de referência dos dados.
        ngii_bruto: NGII calculado sem ajustes de falseabilidade.
        taxa_migracao_anual: Taxa líquida de migração anual (proporção, ex.: 0.008 = 0.8%).
        proporcao_provedores: Proporção da população em idade ativa/provedora (0 a 1).

    Returns:
        Tupla (ngii_puro_final, lista_de_alertas). Se nenhum teste
        disparar alerta, a lista contém apenas "Sem problemas
        detectados". Retorna None se ngii_bruto < 0 ou se
        pais_codigo não for uma string de 3 caracteres.

    Exemplo:
        >>> aplicar_protocolo_falseabilidade_simplificado(
        ...     pais_codigo="BRA", ano=2024, ngii_bruto=1.05,
        ...     taxa_migracao_anual=0.008, proporcao_provedores=0.55,
        ... )
        (1.05, ['Sem problemas detectados'])

        >>> aplicar_protocolo_falseabilidade_simplificado(
        ...     pais_codigo="SWE", ano=2024, ngii_bruto=1.05,
        ...     taxa_migracao_anual=0.15, proporcao_provedores=0.55,
        ... )
        (0.9974999999999999, ['Dependência migratória detectada'])
    """
    if ngii_bruto < 0:
        return None
    if not isinstance(pais_codigo, str) or len(pais_codigo) != 3:
        return None

    ngii_puro = ngii_bruto
    alertas: List[str] = []

    # Teste 1 - Migração
    if taxa_migracao_anual > 0.12:
        ngii_puro = ngii_puro * 0.95
        alertas.append("Dependência migratória detectada")

    # Teste 2 - Estrutura de Provedores
    if proporcao_provedores < 0.50:
        ngii_puro = ngii_puro * 0.90
        alertas.append("Compressão de provedores detectada")

    # Teste 3 - Sinalização de Conjuntura (simplificado)
    if ano == 2020:
        alertas.append("Efeito conjuntural COVID-19")

    if not alertas:
        alertas = ["Sem problemas detectados"]

    return (ngii_puro, alertas)
