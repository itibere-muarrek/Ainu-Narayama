import streamlit as st

st.set_page_config(page_title="FAQ", page_icon="❓", layout="wide")

st.markdown("# ❓ Perguntas Frequentes")

st.markdown("""
## Sobre AINU

### O que significa AINU?
AINU significa "Agente Inteligente Narayama de Uniformização".
O nome homenageia o filme clássico de Shohei Imamura que explora
temas de ciclo de vida, morte e sustentabilidade populacional.

### O que AINU faz?
AINU analisa dados demográficos de 29 países usando dois índices principais:
- **N***: Mede capacidade regenerativa de populações
- **IES**: Mede sustentabilidade do sistema

### Quantos países AINU analisa?
29 países distribuídos em 5 continentes, cobrindo ~40% da população mundial.

---

## Índices

### O que é N*?
N* (Índice Narayama) mede a capacidade de uma população se regenerar.
- N* > 1.3 = 🟢 PROMISSOR (crescimento saudável)
- 0.9-1.3 = 🔵 EQUILÍBRIO (estável)
- 0.5-0.9 = 🟠 CRÍTICO (em risco)
- N* < 0.5 = 🔴 COLAPSO (declínio acelerado)

### O que é IES?
IES (Índice Equilíbrio Sistêmico) mede sustentabilidade do sistema
e sua capacidade de se adaptar a mudanças.
- IES > 0.8 = 🟢 SAUDÁVEL
- 0.6-0.8 = 🔵 ESTÁVEL
- 0.4-0.6 = 🟡 FRÁGIL
- IES < 0.4 = 🔴 CRÍTICO

### Como N* e IES diferem?
- **N*** é sobre capacidade de reprodução e crescimento
- **IES** é sobre robustez institucional e sustentabilidade do sistema

Ambos são importantes para entender saúde demográfica completa.

### Por que TFR (Taxa de Fecundidade Total) é importante?
TFR mede quantos filhos uma mulher tem em média ao longo da vida.
É um dos indicadores mais importantes de tendências populacionais.
- TFR < 2.1 = população encolhendo
- TFR ≈ 2.1 = população estável
- TFR > 2.1 = população crescendo

---

## Dados e Metodologia

### De onde vêm os dados?
AINU coleta de fontes confiáveis:
- UN World Population Prospects
- World Bank Development Data
- Yale Environmental Performance Index

### Quão atualizados são os dados?
- Dados históricos: até 2024
- Atualizações automáticas: toda sexta-feira às 14:00 (SP)
- Projeções: até 2034

### Como posso confiar nos números?
AINU valida todos os cálculos com 4 testes independentes:
- TRR (Taxa Regressão Rápida)
- TSP (Teste Sensibilidade Padrão)
- TCE (Coerência Estrutural)
- TCD (Coerência Demográfica)

### As fórmulas são públicas?
Sim! Veja a página "Metodologia" para todas as fórmulas completas.

### Como o Agente Coletor funciona?
Executa 7 fases automaticamente toda sexta-feira:
1. Pré-coleta (validações)
2. Coleta paralela (dados)
3. Transformação (normalização)
4. Cálculo (índices)
5. Validação (testes)
6. Persistência (banco de dados)
7. Notificação (email admin)

---

## Simuladores

### Como funcionam os simuladores?
Os simuladores permitem você ajustar parâmetros (±25%) e ver
como isso afeta N* ou IES em tempo real.

### Qual é o intervalo válido para ajustes?
Você pode variar parâmetros em ±25% do valor original.
Isto evita cenários irrealistas.

### Os resultados são salvos?
Sim, todas as simulações são salvas no histórico pessoal.

### Posso comparar múltiplos cenários?
Atualmente você vê um cenário por vez.
Você pode fazer múltiplas simulações e comparar.

---

## Usuários e Contas

### Preciso de conta para usar AINU?
Sim, você precisa se registrar e ser aprovado por um administrador.

### Quanto tempo leva para aprovação?
Normalmente 24-48 horas.

### Posso usar um email diferente?
Sim, você pode se registrar com qualquer email válido.

### Esqueci minha senha!
Entre em contato conosco: narayama.live@gmail.com

### Quanto custa usar AINU?
AINU é completamente gratuito para pesquisadores e cidadãos.

---

## Dados Pessoais e Privacidade

### Meus dados são seguros?
Sim, usamos:
- HTTPS para transmissão
- JWT tokens para autenticação
- PostgreSQL com backups
- Senhas com hashing bcrypt

### Você compartilha dados pessoais?
Não, nunca. Veja nossa política de privacidade.

### Como solicito exclusão de dados?
Entre em contato: narayama.live@gmail.com

---

## Problemas Técnicos

### A página não carrega
- Limpe o cache do navegador
- Verifique conexão de internet
- Tente outro navegador

### Gráficos não aparecem
- Isso pode ser um problema de JavaScript
- Tente desabilitar extensões do navegador
- Verifique compatibilidade do navegador

### Simulador está lento
- Isso é normal em conexões lentas
- Os cálculos acontecem localmente no seu navegador
- Espere alguns segundos

### Consegui um erro 401
Você não está autenticado:
- Faça login novamente
- Verifique se seu token expirou (24 horas)
- Limpe cookies do navegador

---

## Pesquisa e Estudos

### Posso usar dados de AINU em publicações?
Sim, desde que cite:
```
AINU.SYSTEMS v3.1.0
https://narayama.live
```

### AINU é revisado por pares?
A metodologia é baseada em literatura científica estabelecida.
Os índices são validados com 4 testes de falsificabilidade.

### Há papers sobre a metodologia?
Visite nossa página de metodologia para referências completas.

---

## Suporte

### Tenho uma dúvida não respondida aqui
📧 Contate: narayama.live@gmail.com

### Quero reportar um bug
📧 Email: narayama.live@gmail.com

### Quero sugerir uma melhoria
📧 Email: narayama.live@gmail.com

### Onde vejo o status do sistema?
Verificamos uptime continuamente. Em caso de problemas,
você receberá email da equipe.

---

## Próximos Passos

1. ✅ Explorar o Dashboard
2. ✅ Testar os Simuladores
3. ✅ Ler a Metodologia
4. ✅ Entrar em contato com dúvidas

Boa sorte explorando AINU!
""")
