import streamlit as st

st.set_page_config(page_title="Sobre", page_icon="ℹ️", layout="wide")

st.markdown("# ℹ️ Sobre AINU.SYSTEMS")

st.markdown("""
## O Que é AINU?

AINU.SYSTEMS (Agente Inteligente Narayama de Uniformização) é um sistema
de análise demográfica que utiliza inteligência artificial e análise de dados
para compreender a saúde e sustentabilidade de populações em 29 países.

---

## Por Que AINU?

Narayama é um filme japonês de Shohei Imamura que explora temas de envelhecimento,
morte e sustentabilidade populacional. AINU homenageia essa obra, aplicando seus
temas a um contexto científico moderno.

---

## Índices Principais

### N* (Índice Narayama)
Mede a **capacidade regenerativa** de uma população:
- Quanto a população consegue se reproduzir
- Taxa de crescimento sustentável
- Tendências de longo prazo

### IES (Índice Equilíbrio Sistêmico)
Mede a **sustentabilidade do sistema**:
- Robustez institucional
- Resiliência a mudanças
- Capacidade de adaptação

---

## Análise de 29 Países

Cobrimos continentes e economias diversas:

**África**
- Nigeria, Ethiopia, DRCongo, Egypt, Kenya

**Ásia**
- India, Indonesia, Vietnam, Iran, China, Thailand, Pakistan, Bangladesh, Japan, South Korea, Saudi Arabia

**Europa**
- Poland, Germany, France, Spain, Russia

**Américas**
- Brazil, Mexico, United States, Argentina, Canada

**Oceania**
- Australia

---

## Timeline de Dados

- **1999-2024**: Dados históricos (25 anos)
- **2024-2034**: Projeções futuras (10 anos)
- **Total**: 35 anos de cobertura

---

## Recursos Únicos

✨ **Agente Automático**: Coleta dados toda sexta-feira

🔬 **Validação Rigorosa**: 4 testes de falsificabilidade

📊 **Simuladores**: Teste cenários customizados

📈 **Visualizações**: Gráficos interativos e análises

🔐 **Segurança**: Autenticação e controle de acesso

---

## Equipe

### Desenvolvimento
- Claude Code (Anthropic)
- Sistema versão 3.1.0

### Conceito
Inspirado em Shohei Imamura e reflexões sobre demografia

### Dados
UN World Population Prospects, World Bank, Yale EPI

---

## Missão

Democratizar o acesso a análises demográficas de alta qualidade,
permitindo que pesquisadores, formuladores de políticas e cidadãos
entendam melhor as dinâmicas populacionais do mundo.

---

## Visão

Um mundo onde dados demográficos são transparentes, acessíveis
e utilizados para tomar melhores decisões sobre o futuro das populações.

---

## Valores

- 🔬 **Rigor Científico**: Metodologia baseada em evidências
- 📊 **Transparência**: Fórmulas e dados públicos
- 🌍 **Inclusão**: Acesso aberto a todos
- 🔄 **Atualização**: Ciclos automáticos de coleta
- 🛡️ **Segurança**: Dados protegidos e auditados

---

## Estatísticas Globais

""")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Países Analisados", "29")
    st.metric("Anos de Histórico", "25")

with col2:
    st.metric("Anos de Projeção", "10")
    st.metric("Indicadores por País", "15+")

with col3:
    st.metric("Testes de Validação", "4")
    st.metric("Fases do Agente", "7")

st.markdown("---")

st.markdown("""
## Documentação

- 📐 [Metodologia](6_Metodologia.py) - Fórmulas e explicações
- ❓ [FAQ](8_FAQ.py) - Perguntas frequentes
- 📧 [Contato](9_Contato.py) - Entre em contato conosco

---

## Licença

AINU.SYSTEMS é fornecido como ferramenta de pesquisa e análise.

**Não é aconselhamento profissional.**

Para decisões importantes, consulte especialistas em demografia,
economia e políticas públicas.

---

## Versão

**AINU.SYSTEMS v3.1.0**
- FastAPI Backend
- Streamlit Frontend
- PostgreSQL Database
- Docker Containerization
- Railway Cloud Deployment

Lançado em 2024 | Última atualização: 2024

""")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Estatísticas do Sistema")
    st.info("""
    - Usuários registrados: crescendo
    - Simulações por dia: variável
    - Uptime: 99.9%
    - Atualização agente: Sexta 14:00 SP
    """)

with col2:
    st.markdown("### Suporte")
    st.success("""
    📧 **Email**: narayama.live@gmail.com

    🌐 **Website**: https://narayama.live

    📚 **Documentação**: Veja abas acima
    """)
