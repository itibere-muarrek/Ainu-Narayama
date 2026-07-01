"""
Teste manual de sanidade do motor de cálculo (src/indices.py) usando
uma estimativa ilustrativa para o Brasil 2024.

IMPORTANTE — leia antes de interpretar o resultado:
1. A fórmula usada é a do Capítulo 5 da tese (3 fatores, Pop_Topo =
   25-65 "provedores atuais"), não a versão de 2 fatores da Seção
   V.III (Pop_Topo = 55+/61+ "idosos"). As duas definições de
   Pop_Topo não são intercambiáveis: a população brasileira de 25-65
   anos é bem maior que a de 55+.
2. Pop_Topo (25-65) e as taxas de escolaridade não são publicadas no
   texto da tese para o Brasil — são estimativas/placeholders deste
   teste, não a calibração oficial.
3. A própria tese publica QUATRO valores diferentes de N* para o
   Brasil 2024 em pontos distintos do texto: 0,45 (Tabela 3), ~0,605
   (implícito no Anexo 8), 0,695 (Anexo 12) e 0,72 (notação de farol,
   Seção V.III-bis: "Brasil 2024: N* = 0,72(-)"). Este teste usa 0,72
   por ser o valor pedido, mas nenhum dos quatro é reproduzível sem
   os dados brutos exatos usados pelo autor.

Por isso, este script tem dois testes:
- TESTE A: reproduz o exemplo do próprio docstring de
  calcular_ngii_puro() — confirma que o código bate com sua própria
  documentação (sanidade da implementação).
- TESTE B: estimativa ilustrativa para o Brasil 2024, comparada ao
  N*=0,72 publicado — mede o quanto uma estimativa razoável (mas não
  calibrada) diverge do número oficial, e não deve ser lido como
  "o código está errado" se a diferença for grande.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.indices import calcular_fator_geracional, calcular_n_base, calcular_ngii_puro

TOLERANCIA = 0.10  # 10%


def formatar_br(valor: float, casas: int = 3) -> str:
    """Formata um float com vírgula decimal, no padrão usado na tese."""
    return f"{valor:.{casas}f}".replace(".", ",")


def rodar_teste(titulo: str, ngii_puro: float, fator_geracional: float, n_esperado: float) -> bool:
    n_calculado = calcular_n_base(ngii_puro, fator_geracional)

    print(f"TESTE: {titulo}")
    print("=" * (7 + len(titulo)))
    print(f"NGII_puro calculado: {formatar_br(ngii_puro)}")
    print(f"Fator_Geracional calculado: {formatar_br(fator_geracional)}")
    print(f"N* calculado: {formatar_br(n_calculado)}")
    print()
    print(f"N* esperado: {formatar_br(n_esperado, 2)}")

    diferenca = abs(n_calculado - n_esperado)
    diferenca_pct = diferenca / n_esperado
    print(f"Diferença: {formatar_br(diferenca)} ({formatar_br(diferenca_pct * 100, 1)}%)")

    passou = diferenca_pct < TOLERANCIA
    print()
    print(f"Status: {'PASSOU' if passou else 'NÃO PASSOU'} (diferença {'<' if passou else '>='} {int(TOLERANCIA * 100)}%)")
    print()

    return passou


# -----------------------------------------------------------------------
# TESTE A — sanidade: reproduz o exemplo do docstring de calcular_ngii_puro()
# -----------------------------------------------------------------------

ngii_a = calcular_ngii_puro(
    pop_base=65.0, pop_topo=110.0, nascimentos=2.7, mortes=1.6,
    taxa_escolaridade_0_25=0.75, taxa_escolaridade_esperada=0.85,
)
fg_a = calcular_fator_geracional(tfr_atual=1.60, tfr_25_anos_atras=2.40)
passou_a = rodar_teste("Sanidade — exemplo do docstring", ngii_a, fg_a, n_esperado=0.5866)

# -----------------------------------------------------------------------
# TESTE B — estimativa ilustrativa Brasil 2024 vs. N*=0,72 (tese, V.III-bis)
# -----------------------------------------------------------------------
# Pop_Base (0-25): 50 milhões — valor fornecido, compatível com as
#   duas convenções de Pop_Topo (não muda).
# Pop_Topo (25-65): 130 milhões — ESTIMATIVA (não publicada na tese;
#   Pop_Topo aqui é "provedores atuais" 25-65, não "55+").
# Nascimentos/Mortes 2024: 2,6M / 1,4M — valores fornecidos.
# TFR 2024 / TFR 1999: 1,60 / 2,14 — valores fornecidos.
# Taxa_Escolaridade: 0,75/0,85 — placeholder (não publicada na tese).

ngii_b = calcular_ngii_puro(
    pop_base=50.0, pop_topo=130.0, nascimentos=2.6, mortes=1.4,
    taxa_escolaridade_0_25=0.75, taxa_escolaridade_esperada=0.85,
)
fg_b = calcular_fator_geracional(tfr_atual=1.60, tfr_25_anos_atras=2.14)
passou_b = rodar_teste("Brasil 2024 (estimativa ilustrativa)", ngii_b, fg_b, n_esperado=0.72)

if not passou_b:
    print(
        "Nota: a divergência acima é esperada — Pop_Topo (25-65) e as "
        "taxas de escolaridade usadas são estimativas, não os dados "
        "brutos reais que o autor da tese usou para calibrar N*=0,72. "
        "Isso não indica um erro nas fórmulas de src/indices.py (ver "
        "TESTE A, que bate exatamente com a documentação do código)."
    )
