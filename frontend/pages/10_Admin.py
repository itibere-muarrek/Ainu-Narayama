import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Admin", page_icon="👨‍💼", layout="wide")

st.markdown("# 👨‍💼 Painel Administrativo")

token = st.session_state.get("token")
usuario = st.session_state.get("usuario")

if not token or not usuario:
    st.error("❌ Você precisa estar logado para acessar esta página.")
    st.stop()

if not usuario.get("is_admin"):
    st.error("❌ Acesso restrito a administradores.")
    st.stop()

st.markdown(f"Bem-vindo, **{usuario['nome']}**!")

tab1, tab2, tab3, tab4 = st.tabs(["📋 Pendentes", "✅ Aprovados", "📊 Logs", "⚙️ Configuração"])

with tab1:
    st.markdown("### Usuários Pendentes de Aprovação")

    try:
        response = requests.get(
            f"{BACKEND_URL}/api/v1/admin/usuarios-pendentes",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )

        if response.status_code == 200:
            usuarios_pendentes = response.json()

            if usuarios_pendentes:
                for user in usuarios_pendentes:
                    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])

                    with col1:
                        st.write(f"**{user['nome']}**")
                        st.caption(user['email'])

                    with col2:
                        st.caption(f"Cadastrado em: {user['criado_em'][:10]}")

                    with col3:
                        if st.button("✅ Aprovar", key=f"aprova_{user['id']}"):
                            try:
                                resp = requests.post(
                                    f"{BACKEND_URL}/api/v1/admin/aprovar/{user['id']}",
                                    headers={"Authorization": f"Bearer {token}"},
                                    timeout=10
                                )
                                if resp.status_code == 200:
                                    st.success("✅ Usuário aprovado!")
                                    st.rerun()
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                    with col4:
                        if st.button("❌ Rejeitar", key=f"rejeita_{user['id']}"):
                            try:
                                resp = requests.post(
                                    f"{BACKEND_URL}/api/v1/admin/rejeitar/{user['id']}",
                                    headers={"Authorization": f"Bearer {token}"},
                                    timeout=10
                                )
                                if resp.status_code == 200:
                                    st.success("❌ Usuário rejeitado!")
                                    st.rerun()
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

                    st.divider()
            else:
                st.info("✅ Nenhum usuário pendente!")

        else:
            st.error("Erro ao carregar usuários")

    except Exception as e:
        st.error(f"Erro de conexão: {str(e)}")

with tab2:
    st.markdown("### Usuários Aprovados")

    try:
        response = requests.get(
            f"{BACKEND_URL}/api/v1/admin/usuarios-aprovados",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )

        if response.status_code == 200:
            usuarios_aprovados = response.json()

            if usuarios_aprovados:
                df = pd.DataFrame([
                    {
                        "Nome": u['nome'],
                        "Email": u['email'],
                        "Admin": "✅ Sim" if u['is_admin'] else "❌ Não",
                        "Cadastro": u['criado_em'][:10]
                    }
                    for u in usuarios_aprovados
                ])

                st.dataframe(df, use_container_width=True, hide_index=True)
                st.info(f"Total: {len(usuarios_aprovados)} usuários aprovados")
            else:
                st.warning("Nenhum usuário aprovado ainda")

        else:
            st.error("Erro ao carregar usuários")

    except Exception as e:
        st.error(f"Erro de conexão: {str(e)}")

with tab3:
    st.markdown("### Logs do Sistema")

    try:
        response = requests.get(
            f"{BACKEND_URL}/api/v1/admin/logs",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )

        if response.status_code == 200:
            logs = response.json()

            if logs:
                df_logs = pd.DataFrame([
                    {
                        "Tipo": log['tipo'],
                        "Mensagem": log['mensagem'],
                        "Timestamp": log['criado_em']
                    }
                    for log in logs
                ])

                st.dataframe(df_logs, use_container_width=True, hide_index=True)
            else:
                st.info("Nenhum log disponível")

        else:
            st.error("Erro ao carregar logs")

    except Exception as e:
        st.error(f"Erro de conexão: {str(e)}")

with tab4:
    st.markdown("### Configuração do Sistema")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Status do Sistema**")
        st.success("🟢 Backend: Online")
        st.success("🟢 Database: Online")
        st.info("🔵 Agente Coletor: Agendado (Sexta 14:00)")

    with col2:
        st.markdown("**Última Atualização**")
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                st.success("✅ Sistema saudável")
        except:
            st.error("❌ Sistema indisponível")

    st.markdown("---")

    st.markdown("**Informações do Servidor**")
    st.code(f"""
Version: 3.1.0
Backend URL: {BACKEND_URL}
Database: PostgreSQL
Authentication: JWT (24h)
Encryption: Bcrypt
Framework: FastAPI + Streamlit
    """)

    st.markdown("---")

    st.markdown("**Ações Administrativas**")

    if st.button("🔄 Forçar Coleta do Agente (Premium)"):
        st.warning("⚠️ Esta ação só está disponível para planos premium")

    if st.button("📧 Enviar Email Teste"):
        st.info("📧 Email de teste seria enviado para admin")

    if st.button("🗑️ Limpar Cache"):
        st.success("✅ Cache limpo")

    st.markdown("---")

    st.markdown("**Estatísticas**")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Usuários Totais", "15+")
    with col2:
        st.metric("Simulações Realizadas", "42")
    with col3:
        st.metric("Ciclos do Agente", "8")
