"""
Teste de sanidade do motor de cálculo (src/indices.py).

TESTE A reproduz o exemplo do docstring de calcular_ngii_puro (a razão do NGII), confirmando que o código bate com sua própria
documentação. TESTE B calcula o Brasil 2024 com os dados reais da UN WPP (mesmos de src/data_pipeline.py) e mostra o valor
publicado, o N*_Obs (PQDF-N*, camada A, sem ajustes), ao lado da calibração histórica do autor (N*_cal), só como referência.
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
    classificar_zona_5,
    normalizar_n_base,
)


def formatar_br(valor: float, casas: int = 4) -> str:
    """Formata um float com vírgula decimal, no padrão usado na tese."""
    return f"{valor:.{casas}f}".replace(".", ",")


# TESTE A — sanidade
ngii_a = calcular_ngii_puro(pop_base=65.0, pop_topo=110.0, nascimentos=2.7, mortes=1.6)
n_a = calcular_n_base(ngii_a, calcular_fator_geracional(tfr_atual=1.60, tfr_25_anos_atras=2.40))
esperado_a = 0.6647727272727274
assert abs(n_a - esperado_a) < 1e-9, f"esperado {esperado_a}, calculado {n_a}"
print("TESTE A: PASSOU (bate exato com o docstring de calcular_ngii_puro)")
print()

# TESTE B — Brasil 2024 (composição B30/C40/D30), valor publicado = N*_Obs
ngii_obs = calcular_ngii_puro(pop_base=62.7004, pop_topo=36.4930, nascimentos=2.5721, mortes=1.4984)
fg = calcular_fator_geracional(tfr_atual=1.6143, tfr_25_anos_atras=2.3353)
n_base = calcular_n_base(ngii_obs, fg)
n_obs = normalizar_n_base(n_base)

print("TESTE B: Brasil 2024 (dados reais UN WPP)")
print(f"NGII_Obs: {formatar_br(ngii_obs)} | Fator_Geracional: {formatar_br(fg)} | N_Base: {formatar_br(n_base)}")
print(f"N*_Obs (publicado): {formatar_br(n_obs)} | zona: {classificar_zona_5(n_base)}")

n_base_cal = calcular_n_base(aplicar_falseabilidade_quantitativa(ngii_obs, AJUSTES_FALSEABILIDADE_POR_PAIS["BRA"]), fg)
print(f"N*_cal (calibração histórica do autor, só referência): {formatar_br(normalizar_n_base(n_base_cal))} | zona: {classificar_zona_5(n_base_cal)}")

assert abs(n_obs - 1.4278) < 5e-4, f"N*_Obs do Brasil fora do esperado: {n_obs}"
assert abs(normalizar_n_base(n_base_cal) - 1.1731) < 5e-4, "N*_cal do Brasil mudou"
print()
print("TESTE B: PASSOU")
