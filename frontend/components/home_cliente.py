import streamlit as st
from components.ainu_theme import card, stat_box, alert, AINU_COLORS


def mostrar_home_cliente(user_data):
    """
    Home para usuários LOGADOS E APROVADOS
    """

    st.markdown(f"### 👋 Olá, {user_data.get('nome', 'Usuário')}!")

    # Verificar se está aprovado
    if user_data.get("status") == "APROVADO":
        st.success("✓ Sua conta foi aprovada! Acesso total ao sistema.")

        # SEÇÃO: ESTATÍSTICAS
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            stat_box("Países", "29", "", "🌍")

        with col2:
            stat_box("N*", "Calculado", "", "📈")

        with col3:
            stat_box("IES", "Calculado", "", "⚖️")

        with col4:
            stat_box("Simulações", "Disponível", "", "🎮")

        st.divider()

        # SEÇÃO: EXPLORE O SISTEMA
        st.markdown("### 📚 Explore o Sistema")
        st.caption("Use o menu lateral para acessar Dashboard, Simuladores e Documentação")

        col1, col2, col3 = st.columns(3)

        with col1:
            card(
                "Dashboard",
                "Visualize índices e dados de todos os 29 países com gráficos interativos.",
                "📊",
                "azul_profundo"
            )

        with col2:
            card(
                "Simulador N*",
                "Ajuste variáveis socioeconômicas e veja como o índice N* é afetado.",
                "🎮",
                "dourado"
            )

        with col3:
            card(
                "Simulador IES",
                "Explore cenários de sustentabilidade econômica com projeções futuras.",
                "🎲",
                "terracota"
            )

        st.divider()

        # SEÇÃO: INFORMAÇÕES DA CONTA
        st.markdown("### 👤 Sua Conta")

        col1, col2 = st.columns(2)

        with col1:
            st.info(f"📧 **Email**: {user_data.get('email', 'N/A')}")

        with col2:
            instituicao = user_data.get("instituicao", "Não informada")
            st.info(f"🏢 **Instituição**: {instituicao}")

    else:
        # Conta em revisão
        alert(
            "aviso",
            f"👤 Sua conta está em revisão. Admin notificará quando aprovada. (Status: {user_data.get('status', 'DESCONHECIDO')})"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.info("📖 Leia sobre AINU em 'Sobre'")

        with col2:
            st.info("❓ Perguntas? Veja 'FAQ'")
