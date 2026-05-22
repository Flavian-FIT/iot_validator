# 📋 Documentação Completa - Pipeline de Validação IoT

## 🎯 Visão Geral

Este projeto processa automaticamente as submissões de alunos do processo seletivo de IoT, gerando um dashboard interativo com avaliações detalhadas.

## 📁 Estrutura do Projeto

```
/workspace/resultado_validacao/
│
├── 📄 Scripts Principais
│   ├── gerar_dashboard_completo.py    # Pipeline completo (recomendado)
│   ├── 00_run_all.py                  # Script mestre alternativo
│   ├── run.sh                         # Script bash
│   └── verificar_integridade.py       # Verificação de dados
│
├── 📄 Scripts de Fase (individuais)
│   ├── extrair_commits.py             # Fase 1: Extrai commits
│   ├── processar_dados_completos.py   # Fase 2: Processa dados
│   ├── gerar_feedbacks_llm.py         # Fase 3: Gera feedbacks
│   ├── aplicar_melhorias.py           # Fase 4: Aplica melhorias
│   ├── gerar_json_dashboard.py        # Fase 5: JSON consolidado
│   └── gerar_dashboard_final.py       # Fase 6: Dashboard HTML
│
├── 📄 Configuração
│   ├── config.json                    # Configurações do pipeline
│   └── config.py                      # Configurações em Python
│
├── 📄 Documentação
│   ├── README.md                      # Documentação completa
│   ├── INICIO_RAPIDO.md               # Início rápido
│   ├── RESUMO_EXECUCAO.md             # Resumo da execução
│   └── README_DASHBOARD.md            # Detalhes do dashboard
│
├── 📊 Saídas (Geradas)
│   ├── dashboard_final.html           # Dashboard interativo ⭐
│   ├── avaliacoes_melhoradas.json     # Dados processados
│   ├── avaliacoes_completas.json      # JSON consolidado
│   └── ... (outros arquivos intermediários)
│
└── 📁 Pastas
    ├── repos/                         # Repositórios clonados
    └── relatorios/                    # Relatórios individuais
```

## 🚀 Como Usar

### Opção 1: Pipeline Completo (Recomendado)

```bash
cd /workspace/resultado_validacao
python3 gerar_dashboard_completo.py
```

**O que este script faz:**
1. Carrega dados existentes
2. Extrai commits dos repositórios
3. Processa emails, imagens e artefatos
4. Gera feedbacks detalhados
5. Aplica melhorias e ranking
6. Consolida em JSON
7. Gera dashboard HTML final

### Opção 2: Script Bash

```bash
cd /workspace/resultado_validacao
./run.sh
```

### Opção 3: Scripts Individuais

Execute cada fase separadamente (avançado):

```bash
python3 extrair_commits.py
python3 processar_dados_completos.py
python3 gerar_feedbacks_llm.py
python3 aplicar_melhorias.py
python3 gerar_json_dashboard.py
python3 gerar_dashboard_final.py
```

## 📊 Saída Gerada

### Arquivo Principal
- **`dashboard_final.html`** - Dashboard interativo com todos os dados

### Arquivos de Dados
- `avaliacoes_melhoradas.json` - Dados completos com ranking
- `avaliacoes_completas.json` - JSON consolidado
- `avaliacoes_com_feedback.json` - Com feedbacks detalhados
- `avaliacoes_com_commits.json` - Com commits extraídos

## 🌐 Visualizar Dashboard

### Abrir Localmente
```bash
xdg-open /workspace/resultado_validacao/dashboard_final.html
```

### Servidor HTTP
```bash
cd /workspace/resultado_validacao
python3 -m http.server 8080
```
Acesse: http://localhost:8080/dashboard_final.html

## ✨ Funcionalidades do Dashboard

### Busca e Filtros
- 🔍 Busca por nome do aluno
- 📊 Filtro por faixa de nota (Excelente, Bom, Médio, Ruim)
- ✅ Filtro por status (Sucesso, Erro)

### Cards dos Alunos
- Nome e nota final (com cor baseada no desempenho)
- Email e link para repositório
- Status de submissão
- 5 critérios de avaliação

### Modal de Detalhes
- Feedback detalhado por critério (expansível)
- Resumo do projeto
- Histórico de commits
- Informações do projeto (arquivos presentes)
- Análise do projeto (pontos fortes e melhorias)
- Botões de ação (ver relatório, acessar repositório)

## 📈 Critérios de Avaliação

| Critério | Pontuação | Descrição |
|----------|-----------|-----------|
| Lógica do Firmware | 30 pts | Qualidade do código em src/main.py |
| Métrica/Wokwi | 20 pts | Diagrama do circuito no Wokwi |
| CI/CD | 25 pts | GitHub Actions e automação |
| Documentação | 10 pts | Qualidade do README.md |
| Estrutura | 10 pts | Organização e versionamento |

**Total:** 100 pontos

## 📊 Classificação por Nota

| Faixa | Classificação | Cor |
|-------|--------------|-----|
| 90-100 | Excelente | 🟢 Verde |
| 70-89 | Bom | 🔵 Azul |
| 50-69 | Médio | 🟡 Amarelo |
| 0-49 | Ruim | 🔴 Vermelho |

## 🔧 Configuração

### Arquivo `config.json`

```json
{
  "data_limite": "2026-05-04 23:59:59",
  "commit_inicial": "e560365081a8497c2e5dafba60c1430a7f31cdb7",
  "criterios": {
    "logica_firmware": {"peso": 30},
    "metrica_wokwi": {"peso": 20},
    "ci_cd": {"peso": 25},
    "documentacao": {"peso": 10},
    "estrutura": {"peso": 10}
  }
}
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

### Dados não aparecem
- Verifique se o JSON foi embutido corretamente
- Execute `python3 verificar_integridade.py`

## 📝 Fluxo de Execução

```
1. Carregar dados existentes (avaliacoes_com_feedback.json)
   ↓
2. Extrair commits dos repositórios (git log)
   ↓
3. Processar dados completos (emails, imagens, artefatos)
   ↓
4. Gerar feedbacks detalhados por critério
   ↓
5. Aplicar melhorias (ordenar, ranking, estatísticas)
   ↓
6. Consolidar em JSON (avaliacoes_completas.json)
   ↓
7. Gerar dashboard HTML (dashboard_final.html)
```

## 📊 Estatísticas Típicas

Após processar 77 alunos:
- **Total:** 77 alunos
- **Sucesso:** 72 (93.5%)
- **Erro:** 5 (6.5%)
- **Nota média:** 87.4
- **Maior nota:** 97.9
- **Menor nota:** 13.7
- **Commits extraídos:** 62

## 🔍 Verificação de Integridade

Execute para validar os dados:

```bash
python3 verificar_integridade.py
```

Verifica:
- Campos obrigatórios
- Faixas de nota válidas
- Critérios presentes
- Arquivo HTML gerado

## 📞 Suporte

Para dúvidas ou problemas:
- `README.md` - Documentação completa
- `INICIO_RAPIDO.md` - Guia rápido
- `RESUMO_EXECUCAO.md` - Resumo da última execução
- `plano_validacao_iot.md` - Plano original do projeto

## 🎯 Status

✅ **Pipeline funcional e testado**
- 77 alunos processados
- Dashboard gerado com sucesso
- Dados validados

## 📄 Licença

Projeto interno para processo seletivo IoT.
