# 📋 Product Requirements Document (PRD) - Hermes Validator

## 1. Visão Geral
O Hermes Validator é uma ferramenta para automação da avaliação de candidatos em processos seletivos de IoT. Ele deve processar submissões (links de GitHub), extrair dados técnicos e gerar uma nota baseada em uma rubrica pré-definida.

## 2. Requisitos Funcionais
- **RF01: Extração de Links**: Identificar links de GitHub em arquivos HTML de submissão.
- **RF02: Inspeção de Repositório**: Clonar repositórios e extrair README.md, histórico de commits e imagens.
- **RF03: Avaliação Técnica**: Aplicar rubrica de 5 critérios (Firmware, Wokwi, CI/CD, Documentação, Versionamento).
- **RF04: Consolidação de Resultados**: Gerar CSV e JSONs com os resultados de todos os alunos.
- **RF05: Dashboard Interativo**: Gerar um dashboard HTML que funcione offline (file://) para visualização dos resultados.

## 3. Requisitos Não-Funcionais
- **RNF01: Estabilidade**: Tratar erros de repositórios privados ou inexistentes.
- **RNF02: Desempenho**: Processar 50+ alunos em menos de 1 hora.
- **RNF03: Rastreabilidade**: Manter logs claros de cada etapa do pipeline.

## 4. Stakeholders
- **Recrutadores**: Usuários finais que visualizam o dashboard.
- **Candidatos**: Sujeitos da avaliação.
