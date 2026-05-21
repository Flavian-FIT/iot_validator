# 🚀 Pipeline de Validação IoT - Guia de Uso

## 📋 Visão Geral

Este pipeline processa as submissões de alunos do processo seletivo de IoT e gera um dashboard interativo com as avaliações.

## 📁 Estrutura de Arquivos

```
/workspace/resultado_validacao/
├── 00_run_all.py                    # Script mestre (executa tudo)
├── server_interativo.py             # NOVO: Servidor do Dashboard Interativo ⭐
├── dashboard_interativo.html        # NOVO: Interface do Dashboard Interativo ⭐
├── gerar_dashboard_completo.py      # Pipeline completo (recomendado)
├── extrair_commits.py               # Fase 1: Extrai commits
├── processar_dados_completos.py     # Fase 2: Processa dados
├── gerar_feedbacks_llm.py           # Fase 3: Gera feedbacks
├── aplicar_melhorias.py             # Fase 4: Aplica melhorias
├── gerar_json_dashboard.py          # Fase 5: Consolida JSON
├── gerar_dashboard_final.py         # Fase 6: Gera dashboard
│
├── repos/                           # Repositórios clonados
├── relatorios/                      # Relatórios individuais
├── dashboard_final.html             # Dashboard final (saída)
├── avaliacoes_melhoradas.json       # Dados processados
└── README.md                        # Este arquivo
```

## ⚡ Uso Rápido (Recomendado)

### Opção 1: Pipeline Completo (Mais Simples)

```bash
cd /workspace/resultado_validacao
python3 gerar_dashboard_completo.py
```

**Este script executa todas as 6 fases automaticamente:**
1. Extração de commits
2. Processamento de dados (emails, imagens, artefatos)
3. Geração de feedbacks detalhados
4. Aplicação de melhorias e ranking
5. Consolidação em JSON
6. Geração do dashboard HTML final

### Opção 2: Script Mestre (Controle Total)

```bash
cd /workspace/resultado_validacao
python3 00_run_all.py
```

**Este script:**
- Executa cada script individualmente em sequência
- Mostra o progresso de cada fase
- Permite identificar onde ocorreu algum erro

### Opção 3: Scripts Individuais (Avançado)

Se quiser executar apenas uma fase específica:

```bash
# Fase 1: Extrair commits
python3 extrair_commits.py

# Fase 2: Processar dados completos
python3 processar_dados_completos.py

# Fase 3: Gerar feedbacks
python3 gerar_feedbacks_llm.py

# Fase 4: Aplicar melhorias
python3 aplicar_melhorias.py

# Fase 5: Gerar JSON consolidado
python3 gerar_json_dashboard.py

# Fase 6: Gerar dashboard final
python3 gerar_dashboard_final.py
```

## 📊 Saída Gerada

### Arquivo Principal
- **`dashboard_final.html`** - Dashboard interativo com todos os dados embutidos

### Arquivos de Dados
- `avaliacoes_com_commits.json` - Avaliações com commits extraídos
- `avaliacoes_completo.json` - Dados completos processados
- `avaliacoes_com_feedback.json` - Com feedbacks detalhados
- `avaliacoes_melhoradas.json` - Com melhorias e ranking
- `avaliacoes_completas.json` - JSON consolidado final

## 🌐 Dashboard Interativo (Modo Edição)

Para visualizar os alunos e **adicionar notas ou conteúdos manualmente** via interface web:

```bash
cd /workspace/resultado_validacao
python3 server_interativo.py
```
Acesse: `http://localhost:8000`

Recursos:
- ✅ Edição de notas manuais e comentários.
- ✅ Inserção de README e código main.py.
- ✅ Botão de consolidação automática.

---

## 🌐 Visualizar Dashboard (Estático)
```bash
# Linux
xdg-open /workspace/resultado_validacao/dashboard_final.html

# Windows (via WSL)
explorer.exe file:///workspace/resultado_validacao/dashboard_final.html

# Ou simplesmente abra no navegador
```

### Servidor HTTP Local
```bash
cd /workspace/resultado_validacao
python3 -m http.server 8080
```
Acesse: `http://localhost:8080/dashboard_final.html`

## 📈 Funcionalidades do Dashboard

### Busca e Filtros
- 🔍 Busca por nome do aluno
- 📊 Filtro por faixa de nota
- ✅ Filtro por status (sucesso/erro)

### Informações por Aluno
- Nome, email, link do repositório
- Nota final e ranking
- 5 critérios de avaliação:
  - Lógica do Firmware (30 pts)
  - Métrica/Wokwi (20 pts)
  - CI/CD (25 pts)
  - Documentação (10 pts)
  - Estrutura (10 pts)

### Detalhes no Modal
- Feedback detalhado por critério
- Histórico de commits
- Arquivos presentes (main.py, diagram.json, etc.)
- Pontos fortes e pontos a melhorar

## 🔧 Pré-requisitos

- Python 3.10+
- Git instalado
- Bibliotecas:
  ```bash
  pip install requests beautifulsoup4 markdown pandas
  ```

## 📝 Fluxo de Execução

```
1. Carregar dados existentes (avaliacoes_com_feedback.json)
   ↓
2. Extrair commits dos repositórios
   ↓
3. Processar dados completos (emails, imagens, artefatos)
   ↓
4. Gerar feedbacks detalhados por critério
   ↓
5. Aplicar melhorias (ordenar, ranking, estatísticas)
   ↓
6. Consolidar em JSON
   ↓
7. Gerar dashboard HTML final
```

## 🐛 Solução de Problemas

### Erro: "Arquivo não encontrado"
Certifique-se de que os arquivos base existem:
- `avaliacoes_com_feedback.json`
- `repositorios_processados.json`

### Erro: "Repositório não encontrado"
Verifique se a pasta `repos/` contém os repositórios clonados.

### Dashboard não carrega
- Verifique o console do navegador (F12)
- Tente outro navegador
- Limpe o cache (Ctrl+F5)

## 📊 Estrutura dos Dados

Cada aluno no JSON final contém:
```json
{
  "nome": "Nome do Aluno",
  "email": "email@aluno.com",
  "github_url": "https://github.com/...",
  "status": "sucesso",
  "nota_final": 92.5,
  "ranking": 1,
  "criterios": {
    "logica_firmware": { "score": 30, "feedback_detalhado": "..." },
    "metrica_wokwi": { "score": 20, "feedback_detalhado": "..." },
    "ci_cd": { "score": 25, "feedback_detalhado": "..." },
    "documentacao": { "score": 10, "feedback_detalhado": "..." },
    "estrutura": { "score": 7.5, "feedback_detalhado": "..." }
  },
  "commits_detalhados": [...],
  "artefatos_ia": [...],
  "analise_readme": {...}
}
```

## 🎯 Próximos Passos

1. ✅ **Executar pipeline**: `python3 gerar_dashboard_completo.py`
2. 🌐 **Abrir dashboard**: `xdg-open dashboard_final.html`
3. 📊 **Analisar resultados**: Ver ranking e estatísticas
4. 📤 **Compartilhar**: Enviar `dashboard_final.html` para equipe

## 📞 Suporte

Para dúvidas ou problemas, consulte:
- `README_DASHBOARD.md` - Detalhes do dashboard
- `plano_validacao_iot.md` - Plano original do projeto
