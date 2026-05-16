import streamlit as st

st.set_page_config(page_title="Metodologia", page_icon="📐", layout="wide")

st.markdown("# 📐 Metodologia AINU")

st.markdown("""
## Sistema de Índices

AINU utiliza dois índices principais para medir saúde demográfica:

### 1. N* (Índice Narayama Primário)

**Fórmula:**
```
N* = NGII_Puro × Fator_Geracional

Onde:
  NGII_Puro = (pop_base / pop_topo) × (nasc / mortes)
  Fator_Geracional = tfr_atual / tfr_1999
```

**Componentes:**
- **pop_base**: População base (milhões)
- **pop_topo**: População máxima potencial (milhões)
- **nasc**: Nascimentos anuais (milhões)
- **mortes**: Mortes anuais (milhões)
- **tfr_atual**: Taxa de Fecundidade Total atual
- **tfr_1999**: Taxa de Fecundidade Total em 1999

**Interpretação:**
| N* | Status | Descrição |
|---|---|---|
| > 1.3 | 🟢 PROMISSOR | População crescendo de forma saudável |
| 0.9 - 1.3 | 🔵 EQUILÍBRIO | População estável, sustentável |
| 0.5 - 0.9 | 🟠 CRÍTICO | População em risco de contração |
| < 0.5 | 🔴 COLAPSO | População em declínio acelerado |

---

### 2. IES (Índice Equilíbrio Sistêmico)

**Fórmula:**
```
IES = L × ∛(NGII × NCII × NSII)

Onde:
  NIH = max(0.35, min(0.85, 1 − (0.35·T + 0.25·U + 0.20·M + 0.20·I)))
  NSII = 0.45·A_ext + 0.55·NIH
```

**Componentes:**
- **L**: Fator de Ligação estrutural
- **NGII**: Índice Geração (pop_base / pop_topo)
- **NCII**: Índice Capacidade do sistema
- **NIH**: Índice Saúde Institucional
- **NSII**: Índice Sustentabilidade Institucional

**Fatores de Saúde (NIH):**
- **T**: Taxa Limitante (pressão externa)
- **U**: Fator Instabilidade (volatilidade)
- **M**: Fator Mobilidade (flexibilidade)
- **I**: Fator Inércia (resistência à mudança)

**Interpretação:**
| IES | Status | Descrição |
|---|---|---|
| > 0.8 | 🟢 SAUDÁVEL | Sistema robusto e resiliente |
| 0.6 - 0.8 | 🔵 ESTÁVEL | Sistema balanceado e funcional |
| 0.4 - 0.6 | 🟡 FRÁGIL | Sistema com vulnerabilidades |
| < 0.4 | 🔴 CRÍTICO | Sistema instável e em risco |

---

## 4 Testes de Falsificabilidade

AINU valida seus cálculos através de 4 testes independentes:

### Teste 1: TRR (Taxa Regressão Rápida)
- Índices não devem variar >10% em 1 ano
- Detecta mudanças anormais
- Garante consistência

### Teste 2: TSP (Teste Sensibilidade Padrão)
- ±5% mudança no TFR → mudança proporcional em N*
- Valida relações causais
- Confirma comportamento esperado

### Teste 3: TCE (Teste Coerência Estrutural)
- IES e N* devem variar proporcionalmente
- Detecta inconsistências
- Garante coesão do modelo

### Teste 4: TCD (Teste Coerência Demográfica)
- NIH + NSII consistente com índices
- Valida cascata de cálculos
- Confirma integridade dos dados

---

## Ciclo Automático (7 Fases)

O Agente Coletor executa automaticamente:

**Fase 1: PRÉ-COLETA**
- Validações de conectividade
- Verificação de permissões
- Validação de schema

**Fase 2: COLETA PARALELA**
- UN World Population Prospects
- World Bank Development Data
- Yale Environmental Performance Index

**Fase 3: TRANSFORMAÇÃO**
- Normalização de unidades
- Padronização de formatos
- Tratamento de valores faltantes

**Fase 4: CÁLCULO**
- Computação de N*
- Computação de IES
- Cálculo de indicadores auxiliares

**Fase 5: VALIDAÇÃO**
- Execução dos 4 testes
- Logging de resultados
- Escalação de anomalias

**Fase 6: PERSISTÊNCIA**
- Armazenamento em PostgreSQL
- Versionamento de dados
- Backup automático

**Fase 7: NOTIFICAÇÃO**
- Email para administrador
- Relatório executivo
- Alertas críticos

**Agendamento:** Sexta-feira às 14:00 (horário de São Paulo)

---

## Fontes de Dados

- **UN WPP**: Projeções e dados populacionais
- **World Bank**: Indicadores econômicos e sociais
- **Yale EPI**: Indicadores ambientais e de sustentabilidade
- **ONS**: Dados demográficos nacionais
- **Kaggle**: Bases de dados abertas

---

## Confiabilidade

- ✅ Método científico validado
- ✅ 4 testes de falsificabilidade
- ✅ Dados de fontes confiáveis
- ✅ Ciclos automáticos de atualização
- ✅ Documentação completa

""")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Citações")
    st.info("""
    Sistema desenvolvido com rigor científico.

    Para citações, favor usar:

    ```
    AINU.SYSTEMS v3.1.0
    Agente Inteligente Narayama de Uniformização
    https://narayama.live
    ```
    """)

with col2:
    st.markdown("### Contato Técnico")
    st.success("""
    Dúvidas sobre metodologia?

    📧 narayama.live@gmail.com

    Visite: https://narayama.live
    """)
