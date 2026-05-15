"""
Testes de Falseabilidade do AINU-Narayama

4 testes de validação de qualidade dos dados:
1. TRR - Teste Rarefação Residual
2. TSP - Teste Sinal Penalização
3. TCE - Teste Coerência Estrutural
4. TCD - Teste Consistência Dados
"""

from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class TestadorFalseabilidade:
    """Coordena os 4 testes de falseabilidade"""

    def __init__(self):
        self.resultados = {}
        self.avisos = []
        self.erros = []

    def executar_todos_testes(self, indices_calculados: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executa os 4 testes de falseabilidade em paralelo.

        Retorna:
        {
            "passou": True/False,
            "testes": {
                "trr": {"passou": bool, "motivo": str},
                "tsp": {"passou": bool, "motivo": str},
                "tce": {"passou": bool, "motivo": str},
                "tcd": {"passou": bool, "motivo": str}
            },
            "avisos": [...]
        }
        """

        resultados = {
            "trr": self._teste_trr(indices_calculados),
            "tsp": self._teste_tsp(indices_calculados),
            "tce": self._teste_tce(indices_calculados),
            "tcd": self._teste_tcd(indices_calculados)
        }

        # Agregar resultado final
        passou_todos = all(r.get("passou", False) for r in resultados.values())

        return {
            "passou": passou_todos,
            "testes": resultados,
            "avisos": self.avisos,
            "erros": self.erros
        }

    def _teste_trr(self, indices: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        TRR - Teste Rarefação Residual

        Valida: NGII_Puro - NGII_Bruto < 15%
        (Se > 15%: há maquiagem de dados)
        """

        logger.info("Executando TRR - Teste Rarefação Residual...")

        problemas = []
        total_paises = len(indices)
        paises_com_problema = 0

        for indice in indices:
            try:
                ngii_bruto = indice.get("ngii_bruto", 0)
                ngii_puro = indice.get("ngii_puro", 0)
                pais = indice.get("pais_nome", "UNKNOWN")

                if ngii_bruto == 0:
                    problemas.append(f"{pais}: NGII_Bruto é zero")
                    paises_com_problema += 1
                    continue

                diferenca_relativa = abs(ngii_puro - ngii_bruto) / ngii_bruto
                limite = 0.15

                if diferenca_relativa > limite:
                    msg = f"{pais}: Rarefação {diferenca_relativa:.1%} > {limite:.0%} (MAQUIAGEM SUSPEITA)"
                    problemas.append(msg)
                    self.avisos.append(msg)
                    paises_com_problema += 1

            except Exception as e:
                logger.error(f"Erro ao validar TRR em {indice.get('pais_nome')}: {e}")
                self.erros.append(str(e))
                paises_com_problema += 1

        passou = paises_com_problema == 0

        resultado = {
            "passou": passou,
            "motivo": f"{total_paises - paises_com_problema}/{total_paises} países passaram",
            "detalhe": "Rarefação Residual validada"
        }

        if not passou:
            resultado["problemas"] = problemas

        logger.info(f"  ✓ TRR: {resultado['motivo']}")

        return resultado

    def _teste_tsp(self, indices: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        TSP - Teste Sinal Penalização

        Valida: Estruturadores conseguem sustentar Legatários?
        Razão Estruturadores/Legatários > 0.5

        Nota: Em contexto AINU, isso seria população em idade produtiva /
        população dependente.
        """

        logger.info("Executando TSP - Teste Sinal Penalização...")

        problemas = []
        total_paises = len(indices)
        paises_com_problema = 0

        for indice in indices:
            try:
                # Usar NGII como proxy: razão demográfica
                # Se NGII < 0.5: há desequilíbrio populacional
                ngii = indice.get("ngii_puro", 1.0)
                pais = indice.get("pais_nome", "UNKNOWN")

                limite = 0.5

                if ngii < limite:
                    msg = f"{pais}: NGII {ngii:.3f} < {limite} (ESTRUTURADOR PENALIZADO)"
                    problemas.append(msg)
                    self.avisos.append(msg)
                    paises_com_problema += 1

            except Exception as e:
                logger.error(f"Erro ao validar TSP em {indice.get('pais_nome')}: {e}")
                self.erros.append(str(e))
                paises_com_problema += 1

        passou = paises_com_problema == 0

        resultado = {
            "passou": passou,
            "motivo": f"{total_paises - paises_com_problema}/{total_paises} países têm NGII adequado",
            "detalhe": "Penalização Estrutural validada"
        }

        if not passou:
            resultado["problemas"] = problemas

        logger.info(f"  ✓ TSP: {resultado['motivo']}")

        return resultado

    def _teste_tce(self, indices: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        TCE - Teste Coerência Estrutural

        Valida: População, TFR, Nascimentos e Mortes são coerentes?
        """

        logger.info("Executando TCE - Teste Coerência Estrutural...")

        problemas = []
        total_paises = len(indices)
        paises_com_problema = 0

        for indice in indices:
            try:
                pop_base = indice.get("pop_base_mi", 0)
                pop_topo = indice.get("pop_topo_mi", 0)
                tfr_2024 = indice.get("tfr_2024", 0)
                nasc = indice.get("nascimentos_mi", 0)
                mortes = indice.get("mortes_mi", 0)
                pais = indice.get("pais_nome", "UNKNOWN")

                # Validações
                erros_pais = []

                if pop_base <= 0 or pop_topo <= 0:
                    erros_pais.append("Populações negativas ou zero")

                if tfr_2024 < 0.5 or tfr_2024 > 9.0:
                    erros_pais.append(f"TFR {tfr_2024:.2f} fora do range [0.5, 9.0]")

                if nasc < 0 or mortes < 0:
                    erros_pais.append("Nascimentos ou mortes negativas")

                # Validar coerência: razão população/nascimentos
                if nasc > 0:
                    ratio_pop_nasc = pop_base / nasc
                    if ratio_pop_nasc < 10 or ratio_pop_nasc > 1000:
                        erros_pais.append(f"Razão Pop/Nasc {ratio_pop_nasc:.1f} suspeita")

                if erros_pais:
                    msg = f"{pais}: {'; '.join(erros_pais)}"
                    problemas.append(msg)
                    self.avisos.append(msg)
                    paises_com_problema += 1

            except Exception as e:
                logger.error(f"Erro ao validar TCE em {indice.get('pais_nome')}: {e}")
                self.erros.append(str(e))
                paises_com_problema += 1

        passou = paises_com_problema == 0

        resultado = {
            "passou": passou,
            "motivo": f"{total_paises - paises_com_problema}/{total_paises} países coerentes",
            "detalhe": "Coerência Estrutural validada"
        }

        if not passou:
            resultado["problemas"] = problemas

        logger.info(f"  ✓ TCE: {resultado['motivo']}")

        return resultado

    def _teste_tcd(self, indices: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        TCD - Teste Consistência Dados

        Valida: Diferentes campos conversam entre si?
        Exemplo: VA, Emprego e Salários devem ter correlação plausível
        """

        logger.info("Executando TCD - Teste Consistência Dados...")

        problemas = []
        total_paises = len(indices)
        paises_com_problema = 0

        for indice in indices:
            try:
                va_bruto = indice.get("va_bruto", 0)
                emprego_total = indice.get("emprego_total", 0)
                salarios_totais = indice.get("salarios_totais", 0)
                pais = indice.get("pais_nome", "UNKNOWN")
                confiabilidade = indice.get("confiabilidade", "Media")

                # Se houver dados econômicos, validar consistência
                if va_bruto > 0 and emprego_total > 0:
                    va_por_emp = va_bruto / emprego_total

                    # VA per capita de emprego deve estar em range plausível
                    # (em milhões de unidades)
                    if va_por_emp < 0.001 or va_por_emp > 100:
                        msg = f"{pais}: VA/Emprego {va_por_emp:.3f} suspeito"
                        problemas.append(msg)
                        self.avisos.append(msg)
                        paises_com_problema += 1

                if salarios_totais > va_bruto and va_bruto > 0:
                    msg = f"{pais}: Salários > VA (inconsistência)"
                    problemas.append(msg)
                    self.avisos.append(msg)
                    paises_com_problema += 1

                # Dados com baixa confiabilidade geram aviso
                if confiabilidade == "Baixa":
                    msg = f"{pais}: Confiabilidade baixa - revisar manualmente"
                    self.avisos.append(msg)

            except Exception as e:
                logger.error(f"Erro ao validar TCD em {indice.get('pais_nome')}: {e}")
                self.erros.append(str(e))
                paises_com_problema += 1

        passou = paises_com_problema == 0

        resultado = {
            "passou": passou,
            "motivo": f"{total_paises - paises_com_problema}/{total_paises} países consistentes",
            "detalhe": "Consistência Dados validada"
        }

        if not passou:
            resultado["problemas"] = problemas

        logger.info(f"  ✓ TCD: {resultado['motivo']}")

        return resultado


def executar_validacao(indices_calculados: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Função de conveniência para executar todos os testes.

    Retorna resultado agregado de validação.
    """

    testador = TestadorFalseabilidade()
    resultado = testador.executar_todos_testes(indices_calculados)

    logger.info(
        f"\n{'='*60}\n"
        f"RESULTADO VALIDAÇÃO FALSEABILIDADE\n"
        f"  Passou: {'✅' if resultado['passou'] else '❌'}\n"
        f"  Avisos: {len(resultado['avisos'])}\n"
        f"  Erros: {len(resultado['erros'])}\n"
        f"{'='*60}\n"
    )

    return resultado
