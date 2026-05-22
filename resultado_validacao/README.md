# 🧪 Resultados da Validação IoT

Este diretório contém os resultados processados da validação de projetos IoT. A estrutura foi organizada para manter a portabilidade e clareza.

## 📂 Estrutura de Pastas
- `scripts/`: Scripts Python modulares para cada fase da validação.
- `data/`: Dados intermediários (JSON), bancos de dados e repositórios clonados (`repos/`).
- `reports/`: Dashboards HTML, relatórios Markdown individuais (`relatorios/`) e resumos de execução.

## 🚀 Como Executar
O pipeline é orquestrado por um script mestre na raiz:

```bash
python3 00_run_all.py
```

Este comando executará todas as fases em sequência:
1. Extração de Commits
2. Processamento de Dados (Emails, Imagens, Artefatos)
3. Geração de Feedbacks via LLM
4. Consolidação e Ranking
5. Geração do Dashboard Final

## 📊 Saída Principal
O resultado final consolidado pode ser visualizado em:
- `reports/dashboard_final.html`: Dashboard interativo com todos os resultados.
- `data/avaliacoes_completas.json`: Dados brutos para integração com outros sistemas.

---
*Organizado seguindo os padrões de Engenharia de Sistemas Agêntica.*
