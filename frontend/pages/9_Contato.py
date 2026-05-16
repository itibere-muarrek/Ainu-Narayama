import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Contato", page_icon="💬", layout="wide")

st.markdown("# 💬 Entre em Contato")

token = st.session_state.get("token")
usuario = st.session_state.get("usuario")

st.markdown("""
Tem uma pergunta, sugestão ou relato de problema?
Entre em contato conosco! Responderemos o mais breve possível.
""")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Formulário de Contato")

    nome = st.text_input(
        "👤 Nome completo",
        value=usuario['nome'] if usuario else ""
    )

    email = st.text_input(
        "📧 Email",
        value=usuario['email'] if usuario else ""
    )

    assunto = st.selectbox(
        "📌 Assunto",
        [
            "Dúvida técnica",
            "Relato de bug",
            "Sugestão de melhoria",
            "Pedido de dados",
            "Parceria",
            "Outro"
        ]
    )

    mensagem = st.text_area(
        "💭 Sua mensagem",
        height=200,
        placeholder="Descreva sua dúvida ou feedback aqui..."
    )

    if st.button("📤 Enviar", use_container_width=True):
        if not nome or not email or not mensagem:
            st.error("❌ Preencha todos os campos!")
        else:
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/v1/admin/contato/enviar",
                    json={
                        "nome": nome,
                        "email": email,
                        "assunto": assunto,
                        "mensagem": mensagem
                    },
                    timeout=10
                )

                if response.status_code == 200:
                    st.success("✅ Mensagem enviada com sucesso! Responderemos em breve.")
                    st.balloons()
                else:
                    st.error("❌ Erro ao enviar. Tente novamente.")

            except Exception as e:
                st.error(f"❌ Erro de conexão: {str(e)}")

with col2:
    st.markdown("### Informações")
    st.markdown("""
    **Email**
    narayama.live@gmail.com

    **Website**
    https://narayama.live

    **Horário**
    Seg-Sex: 9h-18h (SP)

    **Tempo de Resposta**
    Até 48 horas
    """)

st.markdown("---")

st.markdown("### Outros Meios de Contato")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **📧 Email Direto**

    Para contatos diretos:
    narayama.live@gmail.com
    """)

with col2:
    st.markdown("""
    **🌐 Website**

    Visite nosso site:
    https://narayama.live
    """)

with col3:
    st.markdown("""
    **📚 Documentação**

    Consulte nossos guias:
    - Metodologia
    - FAQ
    - Sobre
    """)

st.markdown("---")

st.markdown("### Categorias de Contato")

with st.expander("🐛 Relatar um Bug"):
    st.markdown("""
    Se encontrou um problema técnico:
    1. Descreva o problema com detalhes
    2. Indique qual navegador/sistema você usa
    3. Inclua um print de tela se possível
    4. Passos para reproduzir o problema
    """)

with st.expander("💡 Sugerir Melhoria"):
    st.markdown("""
    Para sugerir novos recursos:
    1. Descreva a ideia
    2. Explique por que seria útil
    3. Indique para quem seria importante
    4. Sugira implementação se souber
    """)

with st.expander("❓ Dúvida Técnica"):
    st.markdown("""
    Para dúvidas sobre como usar AINU:
    1. Verifique a página FAQ primeiro
    2. Consulte Metodologia se for sobre fórmulas
    3. Descreva o que você tenta fazer
    4. Inclua exemplos se relevante
    """)

with st.expander("📊 Pedido de Dados"):
    st.markdown("""
    Para solicitar dados específicos:
    1. Indique qual dado você precisa
    2. Para qual país/período
    3. Uso previsto
    4. Formato desejado (CSV, JSON, etc)
    """)

with st.expander("🤝 Parceria"):
    st.markdown("""
    Para oportunidades de colaboração:
    1. Descreva sua organização
    2. Tipo de parceria proposta
    3. Objetivos esperados
    4. Contato direto para negociação
    """)

st.markdown("---")

st.markdown("""
### Tempo de Resposta

| Tipo | Tempo Médio |
|---|---|
| Dúvida | 24h |
| Bug | 48h |
| Sugestão | 1 semana |
| Parceria | 1 semana |

Mensagens recebidas fora do horário serão respondidas no próximo dia útil.
""")

st.markdown("---")

st.success("""
✨ **Sua opinião é importante para nós!**

Cada feedback ajuda AINU a melhorar.
Obrigado por usar nosso sistema!
""")
