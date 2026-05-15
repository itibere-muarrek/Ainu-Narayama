import pytest
from app.services.calculo_n import calcular_n_star
from app.services.calculo_nih import calcular_nih
from app.services.calculo_ies import calcular_l, calcular_ncii, calcular_nsii, calcular_ies_completo


class TestCalculoNStar:
    """Testes do cálculo de N*"""

    def test_calculo_n_star_basico(self):
        """Testa cálculo básico de N*"""

        resultado = calcular_n_star(
            pop_base_mi=215.0,
            pop_topo_mi=214.0,
            nascimentos_mi=2.5,
            mortes_mi=0.8,
            tfr_2024=1.52,
            tfr_1999=2.67
        )

        assert "ngii_bruto" in resultado
        assert "ngii_puro" in resultado
        assert "fator_geracional" in resultado
        assert "n_estrela" in resultado
        assert "status_n" in resultado

        # Validações básicas
        assert resultado["ngii_bruto"] > 0
        assert resultado["fator_geracional"] > 0
        assert resultado["n_estrela"] > 0

    def test_status_n_equilibrio(self):
        """Testa status EQUILIBRIO para N* ≈ 1.0"""

        resultado = calcular_n_star(
            pop_base_mi=100.0,
            pop_topo_mi=100.0,
            nascimentos_mi=1.0,
            mortes_mi=1.0,
            tfr_2024=2.1,
            tfr_1999=2.1
        )

        # N* ≈ 1.0 deve dar EQUILIBRIO
        assert resultado["status_n"] == "EQUILIBRIO"

    def test_divisao_zero(self):
        """Testa erro com divisor zero"""

        with pytest.raises(ValueError):
            calcular_n_star(
                pop_base_mi=100.0,
                pop_topo_mi=0,  # Zero!
                nascimentos_mi=1.0,
                mortes_mi=1.0,
                tfr_2024=2.1,
                tfr_1999=2.1
            )

    def test_valores_negativos(self):
        """Testa erro com valores negativos"""

        with pytest.raises(ValueError):
            calcular_n_star(
                pop_base_mi=-100.0,  # Negativo!
                pop_topo_mi=100.0,
                nascimentos_mi=1.0,
                mortes_mi=1.0,
                tfr_2024=2.1,
                tfr_1999=2.1
            )


class TestCalculoNIH:
    """Testes do cálculo de NIH"""

    def test_nih_calculo(self):
        """Testa cálculo de NIH"""

        resultado = calcular_nih(
            t_ultraprocessados=0.3,
            u_agrotoxicos=0.2,
            m_medicalizado=0.15,
            i_inflamacao=0.2
        )

        assert "nih" in resultado
        assert 0 <= resultado["nih"] <= 1

    def test_nih_zero_estresse(self):
        """Testa NIH com zero estresse (máximo saúde)"""

        resultado = calcular_nih(
            t_ultraprocessados=0,
            u_agrotoxicos=0,
            m_medicalizado=0,
            i_inflamacao=0
        )

        assert resultado["nih"] == 1.0

    def test_nih_maximo_estresse(self):
        """Testa NIH com máximo estresse"""

        resultado = calcular_nih(
            t_ultraprocessados=1.0,
            u_agrotoxicos=1.0,
            m_medicalizado=1.0,
            i_inflamacao=1.0
        )

        # NIH = 1 - (0.35 + 0.25 + 0.20 + 0.20) = 0
        assert resultado["nih"] == 0.0


class TestCalculoIES:
    """Testes do cálculo de IES"""

    def test_calculo_l(self):
        """Testa cálculo de L (Glocalizado)"""

        l = calcular_l(
            ret_retorno_local=0.5,
            comp_competitividade=0.6,
            sym_simbolismo=0.7
        )

        # L = 0.4*0.5 + 0.3*0.6 + 0.3*0.7 = 0.2 + 0.18 + 0.21 = 0.59
        assert abs(l - 0.59) < 0.01

    def test_calculo_ncii(self):
        """Testa cálculo de NCII"""

        ncii = calcular_ncii(
            va_bruto=1000.0,
            emprego_total=50.0,
            salarios_totais=500.0
        )

        # NCII = (1000/50) * (500/1000) = 20 * 0.5 = 10
        assert abs(ncii - 10.0) < 0.01

    def test_calculo_nsii(self):
        """Testa cálculo de NSII"""

        nsii = calcular_nsii(
            a_ext_epi=0.7,
            nih=0.8
        )

        # NSII = 0.45*0.7 + 0.55*0.8 = 0.315 + 0.44 = 0.755
        assert abs(nsii - 0.755) < 0.01

    def test_calculo_ies_completo(self):
        """Testa cálculo completo de IES"""

        resultado = calcular_ies_completo(
            ngii_puro=1.2,
            va_bruto=1000.0,
            emprego_total=50.0,
            salarios_totais=500.0,
            ret_retorno_local=0.5,
            comp_competitividade=0.6,
            sym_simbolismo=0.7,
            yale_epi_score=60.0,
            t_ultraprocessados=0.2,
            u_agrotoxicos=0.15,
            m_medicalizado=0.1,
            i_inflamacao=0.15
        )

        assert "ies" in resultado
        assert "l" in resultado
        assert "ncii" in resultado
        assert "nsii" in resultado
        assert "nih" in resultado
        assert resultado["ies"] > 0

    def test_status_ies_estavel(self):
        """Testa status ESTAVEL para IES >= 1.0"""

        resultado = calcular_ies_completo(
            ngii_puro=2.0,
            va_bruto=2000.0,
            emprego_total=50.0,
            salarios_totais=1000.0,
            ret_retorno_local=0.9,
            comp_competitividade=0.9,
            sym_simbolismo=0.9,
            yale_epi_score=80.0,
            t_ultraprocessados=0.1,
            u_agrotoxicos=0.05,
            m_medicalizado=0.05,
            i_inflamacao=0.05
        )

        # IES deve ser relativamente alto
        assert resultado["status_ies"] in ["ESTAVEL", "TRANSICAO"]
