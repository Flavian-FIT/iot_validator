# 📓 Engineering Notes - Hermes Validator

## 🛑 Traps (Armadilhas Encontradas)

### 2026-05-22: Bug de rstrip em URLs de Git
- **Problema**: O uso de `url.rstrip(".git")` no script `fase3_clone_repos.py` removia caracteres válidos do final da URL se eles estivessem contidos no conjunto `.git` (ex: `Lonnalt` virava `Lonna`).
- **Impacto**: Falha no clone para alunos com nomes de usuário terminando em 't', 'l', 'i', 'g'.
- **Solução**: Alterado para `if url.endswith('.git'): url = url[:-4]`.

### 2026-05-22: Caminhos Hardcoded para /workspace/
- **Problema**: Scripts assumiam que o projeto estava montado em `/workspace/`, mas o ambiente atual utiliza `/home/flv/projetos_crewai/hermes_validator/workspace/`.
- **Impacto**: Erros de "File not found" e permissões em diversos scripts (`fase3`, `fase4`, `extrair_commits`, `processar_dados`, `gerar_dashboard`, etc).
- **Solução**: Refatorado todos os scripts principais para usar `os.path.dirname(os.path.abspath(__file__))` ou `cwd` dinâmico em `subprocess.run`.

### 2026-05-22: Reorganização de Resultados (Estrutura Limpa)
- **Problema**: O diretório `resultado_validacao/` estava poluído com scripts, JSONs e HTMLs misturados na raiz.
- **Solução**: Implementada arquitetura de subpastas (`scripts/`, `data/`, `reports/`) com gestão centralizada de caminhos via `config.py`.
- **Benefício**: Melhor manutenibilidade e separação de lógica vs. dados. O orquestrador `00_run_all.py` foi atualizado para gerenciar a execução cross-directory via `PYTHONPATH`.

## 🚀 Resultados Finais (2026-05-22)

O pipeline foi corrigido e re-executado com os seguintes resultados:
- **Total de Alunos**: 77
- **Sucesso no Processamento**: 72
- **Erros**: 5 (Majoritariamente repositórios privados)
- **Nota Média**: 83.0 (após aplicação de notas manuais)
- **Dashboard Gerado**: `resultado_validacao/dashboard_final.html`

### Melhorias Realizadas
1. **Correção do Bug de Clone**: Alunos como `LUANN DE LIMA_220` agora são processados corretamente após ajuste na função `clean_url`.
2. **Ambiente Portável**: Todos os scripts agora utilizam caminhos relativos ao executável, permitindo a execução fora do ambiente `/workspace/` fixo.
3. **Mapeamento de Link**: Corrigido link do aluno Pedro Henrique Fernandes Bezerra_249.
