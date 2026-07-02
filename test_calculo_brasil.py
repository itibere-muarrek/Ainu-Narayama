"""
Teste manual de sanidade do motor de cálculo (src/indices.py) usando
dados reais do Brasil 2024.

IMPORTANTE — leia antes de interpretar o resultado:
1. A fórmula usada é a de 2 componentes do Anexo 1 / Seção V.III
   (NGII_puro = Pop_Base/Pop_Topo × Nasc/Mort), com Pop_Base=0-21 e
   Pop_Topo=59+ pro Brasil. O corte não vem mais de um único "Perfil C"
   (Tabela 14 simplificada) — desde 2026-07-04, Pop_Base/Pop_Topo são a
   média ponderada dos cortes por perfil conforme a composição real do
   país na Seção 5.2 da tese (Brasil = 30% B + 40% C + 30% D, não
   Perfil C puro — ver src.config.COMPOSICAO_PERFIL_POR_PAIS). Não tem
   fator de escolaridade (o terceiro fator do Capítulo 5 foi removido em
   2026-07-02 — ver docs/definitions.md, seção 3).
2. A tese não especifica nenhum passo de normalização do N_Base — os
   valores altos do TESTE B abaixo (bem acima de 1,0) são uma
   consequência matemática da fórmula tal como publicada no Anexo 1,
   não um bug. Ver docs/definitions.md, seção 8.
3. A própria tese publica QUATRO valores diferentes de N* para o
   Brasil 2024 em pontos distintos do texto: 0,45 (Tabela 3), ~0,605
   (implícito no Anexo 8), 0,695 (Anexo 12) e 0,72 (notação de farol,
   Seção V.III-bis: "Brasil 2024: N* = 0,72(-)"). Nenhum é
   reproduzível sem os dados brutos exatos usados pelo autor (não
   publicados) — por isso o TESTE B abaixo não é comparado contra
   nenhum desses quatro valores, só reporta o resultado com dados
   reais da UN WPP.

Por isso, este script tem dois testes:
- TESTE A: reproduz o exemplo do próprio docstring de
  calcular_ngii_puro() — confirma que o código bate com sua própria
  documentação (sanidade da implementação).
- TESTE B: Brasil 2024, dados reais da UN World Population Prospects
  (mesmos usados em src/data_pipeline.py) — mostra o valor que
  efetivamente está publicado nos sites hoje.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.indices import calcular_fator_geracional, calcular_n_base, calcular_ngii_puro, classificar_zona_n_base


def formatar_br(valor: float, casas: int = 4) -> str:
    """Formata um float com vírgula decimal, no padrão usado na tese."""
    return f"{valor:.{casas}f}".replace(".", ",")


def rodar_teste(titulo: str, ngii_puro: float, fator_geracional: float) -> float:
    n_calculado = calcular_n_base(ngii_puro, fator_geracional)
    zona = classificar_zona_n_base(n_calculado)

    print(f"TESTE: {titulo}")
    print("=" * (7 + len(titulo)))
    print(f"NGII_puro calculado: {formatar_br(ngii_puro)}")
    print(f"Fator_Geracional calculado: {formatar_br(fator_geracional)}")
    print(f"N* calculado: {formatar_br(n_calculado)}")
    print(f"Zona: {zona}")
    print()

    return n_calculado


# -----------------------------------------------------------------------
# TESTE A — sanidade: reproduz o exemplo do docstring de calcular_ngii_puro()
# -----------------------------------------------------------------------

ngii_a = calcular_ngii_puro(pop_base=65.0, pop_topo=110.0, nascimentos=2.7, mortes=1.6)
fg_a = calcular_fator_geracional(tfr_atual=1.60, tfr_25_anos_atras=2.40)
n_a = rodar_teste("Sanidade — exemplo do docstring", ngii_a, fg_a)

esperado_a = 0.6647727272727274
assert abs(n_a - esperado_a) < 1e-9, f"esperado {esperado_a}, calculado {n_a}"
print(f"Status TESTE A: PASSOU (bate exato com o docstring de calcular_ngii_puro)")
print()

# -----------------------------------------------------------------------
# TESTE B — Brasil 2024, dados reais da UN WPP (composição B30/C40/D30,
# Seção 5.2: Pop_Base=0-21, Pop_Topo=59+)
# -----------------------------------------------------------------------
# Mesmos dados usados em data/raw/un_wpp.csv / src/data_pipeline.py.

n_b = rodar_teste(
    "Brasil 2024 (dados reais UN WPP)",
    ngii_puro=calcular_ngii_puro(pop_base=62.7004, pop_topo=36.4930, nascimentos=2.5721, mortes=1.4984),
    fator_geracional=calcular_fator_geracional(tfr_atual=1.6143, tfr_25_anos_atras=2.3353),
)

print(
    "Nota: N* > 1,0 é esperado para o Brasil sob esta fórmula — Pop_Topo "
    "(59+) é bem menor que Pop_Base (0-21) na pirâmide etária brasileira "
    "atual. Não é um erro de cálculo; é a fórmula do Anexo 1 aplicada a "
    "dados reais, sem nenhum passo de normalização definido pela tese."
)
