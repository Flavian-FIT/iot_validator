# 🏗️ Arquitetura do Sistema - Hermes Validator

## 1. Visão Geral
O sistema é composto por um pipeline de processamento em Python que utiliza scripts modulares para cada fase do processo de validação.

## 2. Componentes Principais (Pipeline)
- **Fase 2 (Extração)**: `fase2_extrair_links.py` (Mapeamento Aluno -> GitHub).
- **Fase 3 (Clone)**: `fase3_clone_repos.py` (Download e inspeção Git).
- **Fase 4 (Documentação)**: `fase4_processar_docs.py` (Parsing de READMEs).
- **Fase 5 (Avaliação)**: `fase5_avaliar.py` (Análise técnica via LLM/Regras).
- **Fase 6/7 (Relatórios)**: `fase6_7_csv_relatorios.py` (Consolidação final).

## 3. Fluxo de Dados e Estrutura (Organizado)
1. `resultado_validacao/scripts/` (Lógica do pipeline)
2. `resultado_validacao/data/` (JSONs, CSVs e repos/)
3. `resultado_validacao/reports/` (HTMLs, MDs e relatorios/)
4. `dashboard_final.html` (Localizado em `reports/`)

## 4. Tecnologias
- **Linguagem**: Python 3.10+
- **Bibliotecas**: BeautifulSoap4, Requests, GitPython, Pandas.
- **UI**: HTML/JS Vanilla para o Dashboard.
