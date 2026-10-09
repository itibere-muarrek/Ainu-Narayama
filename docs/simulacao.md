# Simulação geracional (ainu.systems — beta)

Página separada (`app/ainu_systems/pages/1_Simulacao.py`), só para usuários
logados. Decisões do autor (2026-10-09): a simulação altera **apenas a TFR**;
mortalidade e migração seguem a tendência verificada (projeção média da UN WPP
2024); horizonte de **dois ciclos geracionais** (2024 → 2049 → 2074).

## O que ela faz

1. O usuário escolhe um país (os 11 do panorama) e uma TFR-alvo.
2. A TFR converge **linearmente** ao alvo em 25 anos e se mantém nos 25
   seguintes (mesma convenção do P_eq da tese — `definitions.md`, seção 8-B).
3. O motor projeta a população por idade simples e sexo e calcula, ano a ano,
   o N* pela mesma cadeia do projeto (NGII_bruto → NGII_puro → N_Base →
   N* = √N_Base).
4. A página mostra o resumo (2049 e 2074), três leituras de **ponto de
   virada**, e gráficos (população, N* sobre as 5 zonas, nascimentos e óbitos,
   estrutura etária com as faixas Pop_Base/Pop_Topo).

**Cenário, não previsão.** Responde "o que aconteceria *se* a TFR fizesse esta
trajetória, mantido todo o resto na tendência da ONU".

### Pontos de virada (os três são calculados)
- nascimentos passam a superar óbitos (saldo natural de negativo a positivo);
- população: ano do pico (se depois cai) e ano em que a queda termina;
- N* alcança 0,90 (piso do PEA), de baixo para cima.

Quando o evento não ocorre, a página diz o que acontece em vez de "não ocorre"
(ex.: "já ≥ 0,90 em 2024; abaixo a partir de 2063").

## Método (`src/projecao.py`)

Componentes de coorte, passo anual de 1º de julho a 1º de julho:

- **Sobrevivência:** `P(a+1,t+1) = P(a,t)·S(a,t) + M(a+1,t+1)`; `S` usa a taxa
  de mortalidade da ONU (óbitos/população por idade e sexo) média ao longo da
  diagonal de Lexis.
- **Migração:** `M` é o resíduo que faz o modelo reproduzir a projeção média da
  ONU, em número absoluto por idade/sexo/ano (confere com o `NetMigrations` da
  ONU — ver V2 da validação).
- **Nascimentos:** fecundidade por idade da ONU × mulheres em cada grupo
  quinquenal, escalada por `TFR_cenário/TFR_ONU` (preserva o padrão etário) e
  calibrada ao total oficial de nascimentos (`c(t)`, entre 0,99 e 1,01).
- **N\*:** cortes de Pop_Base/Pop_Topo calculados **na hora** a partir de
  `COMPOSICAO_PERFIL_POR_PAIS`; ajustes de falseabilidade constantes por país
  (calibrados em 2024 — mesma simplificação da série histórica).

## Ajuste à mão dos perfis (até 3 por país)

`COMPOSICAO_PERFIL_POR_PAIS` em `src/config.py` já guarda até 3 perfis
(A–E) por país, com pesos que somam 1. Na simulação os cortes etários são
recalculados a partir dela a cada execução, então **editar um peso tem efeito
imediato**, sem refazer nenhum arquivo. A própria página tem um painel
"Ajuste à mão" para testar outra composição sem mexer no código.

Observação: nos números *de produção* (`data/raw/un_wpp.csv` → `n_index_2024.csv`)
Pop_Base/Pop_Topo continuam pré-calculados por `scripts/build_un_wpp_raw.py`;
mudar a composição ali exige rodar esse script.

Limite conhecido: os perfis são definidos por faixas de TFR (Tabela 14); na
simulação a composição fica **fixa** mesmo quando a TFR muda muito.

## Dados e validação

- `scripts/build_projecao_inputs.py` → `data/processed/projecao_inputs.npz`
  (28 países, ~5 MB, versionado). Lê os dumps da ONU em `data/raw/_cache`:
  `proj.csv.gz` (população por idade), `deaths_proj.csv.gz` (óbitos por idade),
  `fertility_age5.csv.gz` (fecundidade por idade), `demographic_indicators.csv.gz`.
- `scripts/validar_projecao.py` → `docs/validacao_projecao.md` (relatório).
  Resumo: calibração de nascimentos ±1%; N* de 2024 do motor vs produção
  ≤ 0,03%; cenário sem migração vs variante "Zero migration" da ONU: 0,45%
  (mediana), 1,75% (máximo); migração residual acompanha o `NetMigrations`.
- `python test_projecao.py` — testes que rodam só com o repositório.

Ampliar de 11 para os 28 países: editar `PAISES_SIMULACAO` na página (os
insumos já cobrem os 28).

## Acesso (beta: Visitor1..Visitor6)

Ver `src/auth.py`. Gere logins com `python scripts/gerar_credenciais.py`:
senhas em texto em `~/ainu_credenciais/senhas_AAAAMMDD.txt` (fora do git;
entregar por canal separado) e hashes em `AINU_USERS_AAAAMMDD.json` — o
conteúdo deste vai na variável `AINU_USERS` do serviço `ainu-systems` no
Render. Rodar de novo gera senhas novas para todos.

## Limites (também exibidos na página)

Só a TFR varia; ajustes de falseabilidade constantes; composição de perfis
fixa; cenário condicional; TFR é medida de período (sem efeito de calendário);
controle de acesso simples (sem recuperação de senha nem 2FA).
