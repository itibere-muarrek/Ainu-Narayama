"""
Teste manual de sanidade do motor de cálculo (src/indices.py) usando
dados reais do Brasil 2024.

IMPORTANTE — leia antes de interpretar o resultado:
1. A fórmula usada é a de 2 componentes do Anexo 1 / Seção V.III
   (NGII_Bruto = Pop_Base/Pop_Topo × Nasc/Mort), com Pop_Base=0-21 e
   Pop_Topo=59+ pro Brasil. O corte não vem mais de um único "Perfil C"
   (Tabela 14 simplificada) — desde 2026-07-04, Pop_Base/Pop_Topo são a
   média ponderada dos cortes por perfil conforme a composição real do
   país na Seção 5.2 da tese (Brasil = 30% B + 40% C + 30% D, não
   Perfil C puro — ver src.config.COMPOSICAO_PERFIL_POR_PAIS). Não tem
   fator de escolaridade (o terceiro fator do Capítulo 5 foi removido em
   2026-07-02 — ver docs/definitions.md, seção 3).
2. Desde 2026-07-07, o NGII_Bruto passa pelo Protocolo de
   Falseabilidade quantitativo da v9.0 (4 ajustes multiplicativos,
   Anexo 9 — ver src.falseability.aplicar_falseabilidade_quantitativa e
   src.config.AJUSTES_FALSEABILIDADE_POR_PAIS) antes de virar o
   NGII_puro usado no N_Base. Antes dessa data, o pipeline tratava o
   NGII_Bruto como se já fosse o NGII_puro, por falta de dado real.
3. Desde 2026-07-09, o N_Base (bruto) é normalizado via raiz quadrada
   pra virar o N* reportado publicamente (ver
   src.indices.normalizar_n_base) — decisão que o autor está
   incorporando na tese, não uma extensão externa. TESTE B abaixo
   mostra os dois valores, bruto e normalizado.
4. A própria tese publica valores de N* divergentes entre si em
   pontos distintos do texto (ver docs/definitions.md, seção 7, para o
   histórico completo) — nenhum é reproduzível sem os dados brutos
   exatos usados pelo autor. O TESTE B abaixo não é comparado contra
   nenhum valor publicado no texto, só reporta o resultado com dados
   reais da UN WPP e a calibração de falseabilidade aprovada.

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

from src.config import AJUSTES_FALSEABILIDADE_POR_PAIS
from src.falseability import aplicar_falseabilidade_quantitativa
from src.indices import (
    calcular_fator_geracional,
    calcular_n_base,
    calcular_ngii_puro,
    classificar_zona_n_base,
    normalizar_n_base,
)


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
# Seção 5.2: Pop_Base=0-21, Pop_Topo=59+), com falseabilidade quantitativa
# -----------------------------------------------------------------------
# Mesmos dados usados em data/raw/un_wpp.csv / src/data_pipeline.py.

ngii_bruto_brasil = calcular_ngii_puro(pop_base=62.7004, pop_topo=36.4930, nascimentos=2.5721, mortes=1.4984)
ngii_puro_brasil = aplicar_falseabilidade_quantitativa(ngii_bruto_brasil, AJUSTES_FALSEABILIDADE_POR_PAIS["BRA"])

print(f"NGII_Bruto (Brasil, pré-falseabilidade): {formatar_br(ngii_bruto_brasil)}")

n_b = rodar_teste(
    "Brasil 2024 (dados reais UN WPP + falseabilidade)",
    ngii_puro=ngii_puro_brasil,
    fator_geracional=calcular_fator_geracional(tfr_atual=1.6143, tfr_25_anos_atras=2.3353),
)

n_b_normalizado = normalizar_n_base(n_b)
print(f"N_Base (bruto): {formatar_br(n_b)}")
print(f"N* (normalizado, sqrt(N_Base)): {formatar_br(n_b_normalizado)}")
print()

print(
    "Nota: N_Base > 1,0 é esperado para o Brasil mesmo pós-falseabilidade "
    "— os 4 ajustes reduzem o NGII_Bruto em ~32%, não o eliminam. A raiz "
    "quadrada (decisão de 2026-07-09) comprime esse valor pro N* "
    "reportado publicamente, sem alterar a zona de classificação (a raiz "
    "é monotônica)."
)
