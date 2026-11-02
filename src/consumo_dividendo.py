"""
Cálculos da página "Consumo por coorte e Dividendo" (ainu.systems, atrás do login).

Tudo aqui é ESCALA LINEAR de números que o AINU.Systems já calculou e que o Diretório exporta
(data/diretorio/publicavel/simulacoes.json, gerado por scripts/diretorio/exportar_diretorio.py).
Nenhum modelo novo: a página deixa o usuário mudar a porcentagem do Dividendo e o número de
crianças adicionais, e mostra o que as fichas já mostram, na escala escolhida.

- custo do Dividendo: proporcional a x (x% do gasto privado por Descendente); conferido contra
  os 25% e 50% da planilha no exportador.
- crianças adicionais: valor por criança e por ano (limite superior, consumo médio), vezes N.

Os arquivos de dados ficam fora do git até o autor liberá-los; sem eles a página avisa e não calcula.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

RAIZ = Path(__file__).resolve().parent.parent
ARQUIVO = RAIZ / "data" / "diretorio" / "publicavel" / "simulacoes.json"
BASE_PCT = 10.0  # o AINU.Systems simula 10%, 25% e 50%; a escala parte dos 10%


def carregar(caminho: Path = ARQUIVO) -> Optional[dict]:
    """Lê simulacoes.json; None se o arquivo não existe ou está ilegível."""
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return dados if isinstance(dados.get("paises"), dict) else None


def custo_dividendo(pct_gasto: float, custo_10pct_pib: Optional[float]) -> Optional[float]:
    """Custo (% do PIB) de um Dividendo de `pct_gasto`% do gasto privado por Descendente."""
    if custo_10pct_pib is None or pct_gasto < 0:
        return None
    return custo_10pct_pib * pct_gasto / BASE_PCT


def razao_programa(custo_pib: Optional[float], programa_pib: Optional[float]) -> Optional[float]:
    """Quantas vezes o Dividendo custa o maior programa infantil de renda do país."""
    if custo_pib is None or not programa_pib:
        return None
    return custo_pib / programa_pib


def razao_gasto_familia(custo_pib: Optional[float], gasto_familia_pib: Optional[float]) -> Optional[float]:
    """Dividendo como fração do gasto público em família (OECD SOCX)."""
    if custo_pib is None or not gasto_familia_pib:
        return None
    return custo_pib / gasto_familia_pib


def incremento(criancas: float, por_crianca: Optional[float]) -> Optional[float]:
    """Valor por ano de `criancas` crianças adicionais (limite superior; consumo médio)."""
    if por_crianca is None or criancas < 0:
        return None
    return criancas * por_crianca


def empregos_liquidos(brutos: Optional[float], liq50: Optional[float], liq100: Optional[float], pct_deslocado: float) -> Optional[float]:
    """Empregos por criança se `pct_deslocado`% do gasto deslocar outro consumo (0 a 100).

    A planilha traz três pontos (0%: bruto; 50% e 100% de deslocamento). A função interpola
    linearmente entre eles, e por isso reproduz os três exatamente; entre os pontos é só uma leitura
    de ordem de grandeza.
    """
    if None in (brutos, liq50, liq100) or not 0 <= pct_deslocado <= 100:
        return None
    if pct_deslocado <= 50:
        return brutos + (liq50 - brutos) * pct_deslocado / 50.0
    return liq50 + (liq100 - liq50) * (pct_deslocado - 50) / 50.0


def horizontes_do_cenario(horizontes: list[dict], cenario: str) -> list[dict]:
    """Linhas do cenário escolhido, em ordem de ano."""
    return sorted((h for h in horizontes if h["cenario"] == cenario), key=lambda h: h["ano"])


def cenarios(horizontes: list[dict]) -> list[str]:
    """Nomes dos cenários na ordem em que aparecem (um a três por país)."""
    vistos: list[str] = []
    for h in horizontes:
        if h["cenario"] not in vistos:
            vistos.append(h["cenario"])
    return vistos
