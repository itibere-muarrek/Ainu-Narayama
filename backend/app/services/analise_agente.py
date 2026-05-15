from typing import Dict, Any, Optional
import json


def analisar_cenario(
    pais_nome: str,
    tipo_indice: str,
    dados_originais: Dict[str, Any],
    dados_simulados: Dict[str, Any],
    resultado_calculo: Dict[str, Any]
) -> str:
    """
    Analisa e gera um relatório textual de um cenário simulado.

    Parâmetros:
    - pais_nome: Nome do país
    - tipo_indice: "N_STAR" ou "IES"
    - dados_originais: Dados originais do país
    - dados_simulados: Dados modificados na simulação
    - resultado_calculo: Resultado dos cálculos

    Retorna:
    - String com análise narrativa
    """

    analise = []
    analise.append(f"=== ANÁLISE DE CENÁRIO: {pais_nome.upper()} ===\n")

    # Identificar alterações
    alteracoes = {}
    for chave in dados_simulados:
        if chave in dados_originais and dados_originais[chave] != dados_simulados[chave]:
            orig = dados_originais[chave]
            sim = dados_simulados[chave]
            pct = ((sim - orig) / orig * 100) if orig != 0 else 0
            alteracoes[chave] = {
                "original": orig,
                "simulado": sim,
                "variacao_pct": round(pct, 2)
            }

    if alteracoes:
        analise.append("ALTERAÇÕES APLICADAS:")
        for chave, info in alteracoes.items():
            analise.append(
                f"  • {chave}: {info['original']} → {info['simulado']} "
                f"({info['variacao_pct']:+.1f}%)"
            )
        analise.append("")

    # Análise por tipo de índice
    if tipo_indice == "N_STAR":
        analise.extend(_analisar_n_star(resultado_calculo, alteracoes))
    elif tipo_indice == "IES":
        analise.extend(_analisar_ies(resultado_calculo, alteracoes))

    return "\n".join(analise)


def _analisar_n_star(resultado: Dict[str, Any], alteracoes: Dict[str, Any]) -> list:
    """Análise específica para N*"""
    analise = []

    analise.append("ANÁLISE N* (NET GENERATIONAL IMPACT INDEX):")
    analise.append(f"  • N* = {resultado['n_estrela']}")
    analise.append(f"  • Status: {resultado['status_n']}")
    analise.append(f"  • NGII Puro: {resultado['ngii_puro']}")
    analise.append(f"  • Fator Geracional: {resultado['fator_geracional']}")
    analise.append("")

    # Interpretação do status
    status_dict = {
        "PROMISSOR": "País em trajetória de crescimento geracional sustentável",
        "EQUILIBRIO": "País em equilíbrio entre gerações (substituição 1:1)",
        "CRITICO": "Primeira sinais de contração geracional",
        "COLAPSO": "Contração severa - necessária reversão de políticas"
    }

    analise.append(f"INTERPRETAÇÃO: {status_dict.get(resultado['status_n'], 'Desconhecido')}")
    analise.append("")

    if alteracoes:
        analise.append("IMPACTO DAS ALTERAÇÕES:")
        if "tfr_2024" in alteracoes or "fator_geracional" in alteracoes:
            analise.append(
                "  • Alterações em TFR (Taxa de Fecundidade) afetam diretamente "
                "o Fator Geracional"
            )
        if "nascimentos_mi" in alteracoes or "mortes_mi" in alteracoes:
            analise.append(
                "  • Mudanças no balanço demográfico (nascimentos/mortes) "
                "alteram NGII Bruto"
            )

    return analise


def _analisar_ies(resultado: Dict[str, Any], alteracoes: Dict[str, Any]) -> list:
    """Análise específica para IES"""
    analise = []

    analise.append("ANÁLISE IES (ÍNDICE DE ESTABILIDADE SISTÊMICA):")
    analise.append(f"  • IES = {resultado['ies']}")
    analise.append(f"  • Status: {resultado['status_ies']}")
    analise.append(f"  • Componente L (Glocalizado): {resultado.get('l', 'N/A')}")
    analise.append(f"  • NCII (Competitividade): {resultado.get('ncii', 'N/A')}")
    analise.append(f"  • NSII (Nutrição): {resultado.get('nsii', 'N/A')}")
    analise.append(f"  • NIH (Saúde Nutricional): {resultado.get('nih', 'N/A')}")
    analise.append("")

    # Interpretação
    status_dict = {
        "ESTAVEL": "Sistema em estabilidade — condições saudáveis mantidas",
        "TRANSICAO": "Sistema em transição — possível inflexão sem ação",
        "CRITICO": "Sistema crítico — intervenção necessária"
    }

    analise.append(f"INTERPRETAÇÃO: {status_dict.get(resultado['status_ies'], 'Desconhecido')}")
    analise.append("")

    if alteracoes:
        analise.append("IMPACTO SETORIAL:")
        if any(k in alteracoes for k in ["va_bruto", "emprego_total", "salarios_totais"]):
            analise.append("  • Alterações econômicas afetam NCII (competitividade)")
        if any(k in alteracoes for k in ["t_ultraprocessados", "u_agrotoxicos", "m_medicalizado", "i_inflamacao"]):
            analise.append("  • Alterações de saúde/nutrição afetam NSII")
        if any(k in alteracoes for k in ["ret_retorno_local", "comp_competitividade", "sym_simbolismo"]):
            analise.append("  • Alterações estruturais afetam L (fator glocalizado)")

    return analise


def _gerar_recomendacoes(resultado: Dict[str, Any], tipo_indice: str) -> list:
    """Gera recomendações baseadas nos resultados"""
    recomendacoes = []

    if tipo_indice == "N_STAR":
        status = resultado.get("status_n", "")
        if status == "COLAPSO":
            recomendacoes.append("RECOMENDAÇÕES: Políticas de reversão demográfica urgentes")
            recomendacoes.append("  - Incentivos para natalidade")
            recomendacoes.append("  - Atração de migrantes qualificados")
        elif status == "CRITICO":
            recomendacoes.append("RECOMENDAÇÕES: Vigilância e ações preventivas")
            recomendacoes.append("  - Monitoramento de indicadores mensais")
            recomendacoes.append("  - Estudos de causa-raiz")

    elif tipo_indice == "IES":
        status = resultado.get("status_ies", "")
        if status == "CRITICO":
            recomendacoes.append("RECOMENDAÇÕES: Intervenções multi-setor necessárias")
            recomendacoes.append("  - Revisar competitividade econômica")
            recomendacoes.append("  - Fortalecer infraestrutura de saúde")
            recomendacoes.append("  - Resgatar identidade sistêmica local")

    return recomendacoes
