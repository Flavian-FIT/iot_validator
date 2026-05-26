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
1. `resultado_validacao/scripts/`: Lógica modular do pipeline (Fases 1-6).
2. `resultado_validacao/data/`: JSONs intermediários, CSVs e a pasta `repos/`.
3. `resultado_validacao/reports/`: Dashboards HTML, MDs e a pasta `relatorios/`.
4. `dashboard_final.html`: Principal artefato de visualização (Localizado em `reports/`).

## 4. Gestão de Caminhos e Portabilidade
O sistema utiliza um padrão de **Gestão Centralizada de Caminhos**:
- **config.py**: Define caminhos absolutos baseados no diretório raiz do projeto.
- **Injeção de Contexto**: O orquestrador `00_run_all.py` injeta o diretório raiz no `PYTHONPATH` de cada subprocesso.
- **Servidor Interativo**: Sobrescreve o método `translate_path` para servir arquivos de múltiplas pastas físicas (`data/` e `reports/`) sob uma mesma URL virtual.

## 5. Tecnologias
- **Linguagem**: Python 3.10+
- **Bibliotecas**: BeautifulSoap4, Requests, GitPython, Pandas.
- **UI**: HTML/JS Vanilla para o Dashboard (Offline-first).
