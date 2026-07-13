"""
Motor de cálculo dos índices do AINU-Narayama.

Implementa as fórmulas centrais da tese v8.0 para obtenção do Índice
de Narayama Sistêmico (N*). Ver docs/definitions.md para a
fundamentação teórica completa, exemplos numéricos e a nota sobre
inconsistências internas identificadas no texto da tese.

Fonte: V1_EcoPol_062426_v8.0.docx — Anexo 1 (A1.2, Formalização
Matemática do Modelo — fórmula de referência do NGII_puro), V.III
(Fator_Geracional; faixas etárias de Pop_Base/Pop_Topo por perfil),
V.III-bis (Fator_Alocativo).

Decisão vigente (atualizada em 2026-07-02): NGII_puro usa a fórmula
de 2 componentes do Anexo 1/V.III — (Pop_Base/Pop_Topo) × (Nasc/Mort)
— sem o terceiro fator de escolaridade do Capítulo 5, que foi
removido. O Anexo 1 (seção mais formal da tese) não inclui
escolaridade na fórmula do NGII_puro, e não especifica nenhum passo
de normalização — valores muito altos em países jovens/alta
fecundidade são uma consequência matemática da fórmula tal como
publicada, não um bug da implementação (ver docs/definitions.md,
seção 8).

Tratamento de erro: todas as funções retornam None quando as
entradas tornam o cálculo indefinido (ex.: divisão por zero) ou
quando alguma entrada já é None (propagação), em vez de levantar
exceção.
"""

import math
from typing import Optional


def calcular_ngii_puro(
    pop_base: float,
    pop_topo: float,
    nascimentos: float,
    mortes: float,
) -> Optional[float]:
    """
    Calcula o NGII_puro (Potência Geracional — Pilar 1 da Flor de Narayama).

    Mede a capacidade real de uma sociedade gerar, formar e sustentar
    os futuros provedores: combina o peso relativo da coorte formadora
    frente à coorte legatária/dependente com o saldo vegetativo do
    período.

    Fórmula (Anexo 1, A1.2 — faixas etárias da Seção V.III):
        NGII_puro = (Pop_Base / Pop_Topo) × (Nascimentos / Mortes)

    Args:
        pop_base: População da coorte formadora, em milhões. Faixa
            etária é a média ponderada dos cortes por perfil conforme
            a composição do país (Seção 5.2) — ver
            src.config.COMPOSICAO_PERFIL_POR_PAIS e src.config.PAISES,
            não duplicado aqui para evitar uma segunda fonte que pode
            ficar desatualizada.
        pop_topo: População da coorte legatária/dependente, em
            milhões. Mesma fonte de faixa etária que pop_base, acima.
        nascimentos: Nascimentos anuais, em milhões.
        mortes: Mortes anuais, em milhões.

    Returns:
        Valor do NGII_puro (adimensional), ou None se pop_topo ou
        mortes forem zero.

    Exemplo (ilustrativo — não reproduz a calibração oficial da tese,
    cujos dados brutos de entrada não são publicados no texto):
        >>> calcular_ngii_puro(pop_base=65.0, pop_topo=110.0, nascimentos=2.7, mortes=1.6)
        0.9971590909090909

    Nota:
        O valor de entrada deve ser o NGII já depurado pelo Protocolo
        de Falseabilidade (Anexo 9 — ver src/falseability.py), que
        transforma o NGII_Bruto em NGII_Puro removendo distorções
        (imigração compensatória, políticas natalistas temporárias,
        choques conjunturais, inércia demográfica e substituição
        civilizacional). A tese não especifica nenhum passo de
        normalização adicional — valores muito altos em países
        jovens/alta fecundidade são esperados (ver docs/definitions.md).
    """
    if pop_topo == 0 or mortes == 0:
        return None

    return (pop_base / pop_topo) * (nascimentos / mortes)


def calcular_fator_geracional(tfr_atual: float, tfr_25_anos_atras: float) -> Optional[float]:
    """
    Calcula o Fator_Geracional.

    Compara a Taxa de Fecundidade Total (TFR) atual com a TFR de uma
    geração atrás (~25 anos), capturando a direção do movimento
    geracional: se a próxima geração de provedores será maior ou
    menor que a atual.

    Fórmula (V.III):
        Fator_Geracional = TFR(i,t) / TFR(i, t-25)

    Args:
        tfr_atual: Taxa de Fecundidade Total do ano corrente.
        tfr_25_anos_atras: Taxa de Fecundidade Total de ~25 anos atrás.

    Returns:
        Fator_Geracional (adimensional), ou None se
        tfr_25_anos_atras for zero.
        > 1 = expansão reprodutiva (fecundidade melhorou entre gerações)
        = 1 = estabilidade reprodutiva
        < 1 = contração reprodutiva (fecundidade piorou entre gerações)

    Exemplo:
        >>> calcular_fator_geracional(tfr_atual=1.60, tfr_25_anos_atras=2.14)
        0.7476635514018691
    """
    if tfr_25_anos_atras == 0:
        return None

    return tfr_atual / tfr_25_anos_atras


def calcular_n_base(ngii_puro: Optional[float], fator_geracional: Optional[float]) -> Optional[float]:
    """
    Calcula o N* (Índice de Narayama Sistêmico), em sua forma base (N_Base).

    Combina a Potência Geracional presente (NGII_puro) com a tendência
    geracional de fecundidade (Fator_Geracional). Ambos os componentes
    são de natureza puramente demográfica (estoque × trajetória); por
    isso se multiplicam diretamente, sem mistura com o Fator_Alocativo
    (que é institucional/fiscal e opera como farol, não como
    componente — ver calcular_fator_alocativo).

    Fórmula (V.II / Capítulo 3):
        N*(i,t) = N_Base(i,t) = NGII_puro(i,t) × Fator_Geracional(i,t)

    Classificação de zonas (Tabela 4 / Anexo 8 — convenção adotada
    neste projeto, ver docs/definitions.md para a nota sobre a
    convenção alternativa e contraditória usada na Seção 3.2):
        N_Base > 1.10          -> Expansão Forte
        0.80 <= N_Base <= 1.10 -> Equilíbrio Sustentável (PEA)
        0.50 <= N_Base < 0.80  -> Tensão Acelerada
        N_Base < 0.50          -> Colapso de Narayama (PEC)

    Args:
        ngii_puro: Resultado de calcular_ngii_puro().
        fator_geracional: Resultado de calcular_fator_geracional().

    Returns:
        Valor do N* / N_Base (adimensional), ou None se ngii_puro ou
        fator_geracional forem None.

    Exemplo:
        >>> calcular_n_base(ngii_puro=1.02, fator_geracional=0.748)
        0.76296
    """
    if ngii_puro is None or fator_geracional is None:
        return None

    return ngii_puro * fator_geracional


def calcular_fator_alocativo(nta_0_25: float, nta_65_mais: float) -> Optional[float]:
    """
    Calcula o Fator_Alocativo (Condicionante Direto / Farol Institucional).

    NÃO é componente do N_Base — é um indicador institucional/fiscal
    que revela a prioridade real que a sociedade dá ao futuro (coorte
    formadora) frente ao presente (coorte idosa), sem alterar a
    magnitude demográfica intrínseca do N_Base.

    Fórmula (V.III-bis):
        Fator_Alocativo(i,t) = NTA(0-25, i,t) / NTA(65+, i,t)

    Args:
        nta_0_25: Fluxo líquido de transferências à coorte formadora
            (educação + saúde infantojuvenil + transferências privadas
            de famílias para filhos), em unidades monetárias.
        nta_65_mais: Fluxo líquido de transferências à coorte idosa
            (previdência + saúde geriátrica + transferências privadas
            de filhos para pais idosos), na mesma unidade monetária.

    Returns:
        Fator_Alocativo (adimensional), ou None se nta_65_mais for zero.
        > 1 = prioridade ao futuro; = 1 = equilíbrio; < 1 = gerontocracia.

    Exemplo:
        >>> calcular_fator_alocativo(nta_0_25=1.0, nta_65_mais=1.20)
        0.8333333333333334
    """
    if nta_65_mais == 0:
        return None

    return nta_0_25 / nta_65_mais


def classificar_farol_alocativo(fator_alocativo: Optional[float]) -> Optional[str]:
    """
    Classifica o Fator_Alocativo em farol institucional (+/n/-).

    Notação (V.III-bis):
        '+' -> Fator_Alocativo > 1.05 (reforça o destino para cima)
        'n' -> 0.95 <= Fator_Alocativo <= 1.05 (neutro)
        '-' -> Fator_Alocativo < 0.95 (pressão gerontocrática)

    Args:
        fator_alocativo: Resultado de calcular_fator_alocativo().

    Returns:
        Um entre '+', 'n', '-', ou None se fator_alocativo for None.

    Exemplo:
        >>> classificar_farol_alocativo(0.8333333333333334)
        '-'
    """
    if fator_alocativo is None:
        return None

    from src.config import FATOR_ALOCATIVO_INFERIOR, FATOR_ALOCATIVO_SUPERIOR

    if fator_alocativo > FATOR_ALOCATIVO_SUPERIOR:
        return "+"
    if fator_alocativo < FATOR_ALOCATIVO_INFERIOR:
        return "-"
    return "n"


def classificar_zona_n_base(n_base: Optional[float]) -> Optional[str]:
    """
    Classifica o N_Base em uma das quatro zonas da Tabela 4 / Anexo 8.

    Args:
        n_base: Resultado de calcular_n_base().

    Returns:
        Uma entre: "Expansão Forte", "Equilíbrio Sustentável (PEA)",
        "Tensão Acelerada", "Colapso de Narayama (PEC)", ou None se
        n_base for None.

    Exemplo:
        >>> classificar_zona_n_base(0.6647727272727274)
        'Tensão Acelerada'
    """
    if n_base is None:
        return None

    from src.config import LIMIAR_EXPANSAO_FORTE, LIMIAR_PEA_INFERIOR, LIMIAR_TENSAO_INFERIOR

    if n_base > LIMIAR_EXPANSAO_FORTE:
        return "Expansão Forte"
    if n_base >= LIMIAR_PEA_INFERIOR:
        return "Equilíbrio Sustentável (PEA)"
    if n_base >= LIMIAR_TENSAO_INFERIOR:
        return "Tensão Acelerada"
    return "Colapso de Narayama (PEC)"


def classificar_zona_5(n_base: Optional[float]) -> Optional[str]:
    """
    Classifica o N_Base em uma das cinco zonas da revisão do autor
    (12/07/2026, Seção 9-A.3/9-A.7), que substitui a convenção de 4
    zonas (classificar_zona_n_base) como a oficial da tese. Principal
    mudança: PEEC deixa de ser diagnosticado só por TFR e passa a ser
    também um limiar de N_Base/N*.

    Limiares (N_Base bruto — ver src.config.LIMIARES_5_ZONAS):
        N_Base < 0,50                  -> Colapso de Narayama (PEC)
        0,50 <= N_Base < 0,81          -> Tensão Acelerada
        0,81 <= N_Base < 1,96          -> Equilíbrio Sustentável (PEA)
        1,96 <= N_Base < 4,00          -> Tensão Populacional
        N_Base >= 4,00                 -> Saturação por Overbirths (PEEC)

    Args:
        n_base: Resultado de calcular_n_base().

    Returns:
        Uma das 5 zonas acima, ou None se n_base for None.

    Exemplo:
        >>> classificar_zona_5(1.3761)
        'Equilíbrio Sustentável (PEA)'
    """
    if n_base is None:
        return None

    from src.config import LIMIARES_5_ZONAS

    if n_base < LIMIARES_5_ZONAS["pec"]:
        return "Colapso de Narayama (PEC)"
    if n_base < LIMIARES_5_ZONAS["tensao_acelerada"]:
        return "Tensão Acelerada"
    if n_base < LIMIARES_5_ZONAS["pea"]:
        return "Equilíbrio Sustentável (PEA)"
    if n_base < LIMIARES_5_ZONAS["tensao_populacional"]:
        return "Tensão Populacional"
    return "Saturação por Overbirths (PEEC)"


def normalizar_n_base(n_base: Optional[float]) -> Optional[float]:
    """
    Normaliza o N_Base para o N* reportado publicamente (decisão de
    2026-07-09).

    A tese nunca definiu um passo de normalização pro N_Base (ver
    docs/definitions.md, seção 8) — mesmo após a composição ponderada
    de perfis e o Protocolo de Falseabilidade quantitativo, países
    jovens/alta fecundidade (RD Congo, Arábia Saudita, Etiópia, Egito,
    Nigéria) ainda produziam N_Base entre ~6,6 e ~11,6, sem
    plausibilidade física.

    Três métodos foram comparados com os dados reais dos 28 países
    antes de escolher este:
    - Truncamento (min/max hard-cap): gera empates — 5 países colavam
      no teto, 3 no piso, perdendo diferenciação real entre eles.
    - Divisão pela mediana da amostra: não limita nada (o maior
      permanecia em ~10x a mediana).
    - Raiz quadrada (escolhida): preserva a ordenação total (nenhum
      empate), não exige nenhuma constante arbitrária, e mantém
      N_Base=1 como ponto fixo (sqrt(1)=1).

    Diferente de outras lacunas documentadas neste projeto, esta
    normalização está sendo formalizada pelo próprio autor como parte
    da tese (não é uma extensão só do projeto).

    Os limiares de zona (Tabela 4/Anexo 8) foram recalculados na mesma
    escala — ver src.config.LIMIARES_SIMPLES_NORMALIZADOS. A
    classificação de zona em si (classificar_zona_n_base) não muda:
    como a raiz é estritamente monotônica para valores não-negativos,
    classificar o N_Base bruto contra os limiares brutos dá exatamente
    a mesma zona que classificar o N* normalizado contra os limiares
    normalizados.

    Args:
        n_base: Resultado de calcular_n_base().

    Returns:
        sqrt(n_base), ou None se n_base for None ou negativo.

    Exemplo:
        >>> normalizar_n_base(11.6160)
        3.408225344662527
    """
    if n_base is None or n_base < 0:
        return None

    return math.sqrt(n_base)
