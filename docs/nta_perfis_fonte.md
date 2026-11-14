# Perfis NTA usados pelo AINU.Systems (data/raw/nta_perfis_C_YL_S.csv)

- **O que é:** perfis por idade simples (0 a 90+, 85+ na Coreia do Sul, 100+ na França) de consumo total (C, privado e público), renda do trabalho (YL) e poupança (S), tipo "Smooth Mean".
- **Fonte:** portal das National Transfer Accounts, https://ntaccounts.org/ (dados públicos de cada país; país e ano do perfil na própria linha do arquivo). Obtido em novembro de 2026.
- **Colunas:** `pais, var, ano, tipo, unidade, idade_max, valores_por_idade_0_a_n` (valores separados por espaço). `unidade` indica "Units" (moeda por pessoa) ou "Thousands" (milhares de moeda local por pessoa).
- **Países e anos (C):** Argentina 2016, Brasil 2008, China 2014, França 2011, Índia 2004, Itália 2008, Japão 2004, México 2014, Nigéria 2016, Coreia do Sul 2019, Estados Unidos 2011. Costa Rica e Paraguai não estão neste arquivo.
- **Uso no código:** `src/nta_derivados.py` (participação das coortes no consumo, com os cortes de `src/config.py` e a população do motor) e `scripts/diretorio/coortes_motor.py` (campo CFCc das fichas do Diretório).
- **Limites:** perfil suavizado de um ano que pode diferir do ano da população; a última idade do perfil é estendida às idades acima; consumo total, sem separar privado e público.
- **Redistribuição:** sem licença identificada (ver `THIRD_PARTY_DATA.md`). Pedido de autorização à coordenação da rede NTA preparado; enquanto não houver resposta, o arquivo fica fora dos pacotes de release (`.gitattributes`).
- **Como obter os dados sem o arquivo do repositório:** no portal https://ntaccounts.org/ (Browse database), escolha o país e o ano, as variáveis Consumption (C), Labor Income (YL) e Saving (S), o tipo "Smooth Mean" e baixe em formato largo; os países e anos usados estão acima. O código espera as colunas descritas acima.
