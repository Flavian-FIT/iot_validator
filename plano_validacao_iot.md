# Plano de Execução - Validação de Entregas IoT (Sem CrewAI)

## 📋 Visão Geral do Projeto CrewAI Original

O projeto `iot_validator` usa CrewAI para automatizar a validação de entregas de alunos do processo seletivo de IoT. Ele executa 4 agentes especializados em sequência:

### Agentes e Responsabilidades:

1. **repository_inspector**: 
   - Extrai link do GitHub dos arquivos dos alunos
   - Clona repositório e identifica último commit antes da data limite
   - Recupera README.md, histórico de commits e imagens

2. **documentation_specialist**:
   - Compara README do aluno com template padrão
   - Extrai metadados (nome, email, github, wokwi)
   - Gera relatório formatado em `relatorio_final.md`

3. **technical_evaluator**:
   - Analisa projeto (resumo, funcionalidades, técnica, commits)
   - Aplica rubrica de avaliação (5 critérios)
   - Atribui nota final (0-100)

4. **csv_analyst**:
   - Consolida resultados em CSV
   - Formato: Nome | Email | Repo | Resumo | Pontuação | Nota

---

## 🎯 Tarefa a Ser Executada

Recriar as mesmas funcionalidades do projeto CrewAI **sem usar CrewAI**, processando as 50+ submissões de alunos na pasta `/workspace/alunos_extraidos/`.

---

## 📁 Estrutura de Entrada

Cada aluno tem uma pasta em `/workspace/alunos_extraidos/` com:
- `textoonline.html`: Arquivo HTML contendo o link do repositório GitHub
- Exemplo: `Leonardo Vieira_236_assignsubmission_onlinetext/textoonline.html`
- Conteúdo típico: `link para o repositório: https://github.com/leonardo897/processoseletivoIoT`

---

## 🛠️ Abordagem Proposta

### Opção 1: Script Python Tradicional (Recomendado)
**Vantagens**: Mais rápido, sem overhead de agents, controle total
**Desvantagens**: Código mais verboso

### Opção 2: Script com LLM via API Direta
**Vantagens**: Mantém inteligência da análise
**Desvantagens**: Requer configuração de API, mais lento

### Opção 3: Abordagem Híbrida
- Script Python para extração e organização
- LLM apenas para análise técnica e avaliação
- Mais equilibrado em custo-benefício

---

## 📝 Plano Detalhado de Execução

### FASE 1: Preparação do Ambiente
1.1. Criar estrutura de pastas para saída
   - `/workspace/resultado_validacao/`
   - `/workspace/resultado_validacao/relatorios/`
   - `/workspace/resultado_validacao/repos/`

1.2. Copiar arquivos de conhecimento do projeto original
   - `rubrica.md` → critérios de avaliação
   - `default_readme.md` → template base

1.3. Verificar dependências
   - Git instalado
   - Python 3.10+
   - Bibliotecas: requests, beautifulsoup4, markdown

---

### FASE 2: Extração de Links GitHub
2.1. Listar todas as pastas de alunos em `/workspace/alunos_extraidos/`
2.2. Para cada pasta:
   - Localizar `textoonline.html`
   - Extrair URL do repositório GitHub (regex)
   - Mapear: `nome_aluno → url_github`

2.3. Salvar mapeamento em `links_mapeados.json`

---

### FASE 3: Clone e Extração de Repositórios
3.1. Para cada repositório mapeado:
   - Clonar em `/workspace/resultado_validacao/repos/{nome_aluno}/`
   - Identificar último commit antes de `2026-05-04 23:59:59`
   - Extrair:
     - README.md
     - Histórico de commits
     - Imagens do projeto
     - Estrutura de arquivos

3.2. Tratar erros:
   - Repositório privado
   - Repositório não encontrado
   - Sem README.md

---

### FASE 4: Processamento de Documentação
4.1. Para cada aluno:
   - Ler README.md do repositório
   - Comparar com `default_readme.md`
   - Extrair seções preenchidas:
     - Nome completo
     - GitHub
     - Visão geral da solução
     - Arquitetura do sistema
     - Componentes utilizados
     - Decisões técnicas
     - Resultados obtidos

4.2. Identificar:
   - Email do aluno (nome da pasta ou extração do HTML)
   - Link do Wokwi (se houver no README)

4.3. Gerar `relatorio_final.md` por aluno

---

### FASE 5: Avaliação Técnica (Com LLM ou Regras)
5.1. Para cada projeto, avaliar 5 critérios da rubrica:

| Critério | Pontuação | Como Avaliar |
|----------|-----------|--------------|
| **Lógica do Firmware** | 30 pts | Verificar `src/main.py`: sintaxe, estrutura, funcionalidade |
| **Métrica/Wokwi** | 20 pts | Verificar `diagram.json`: componentes, conexões |
| **CI/CD** | 25 pts | Verificar `.github/workflows`: pipelines, status |
| **Documentação** | 10 pts | Qualidade do README: seções, clareza, profundidade |
| **Estrutura/Versionamento** | 10 pts | Organização de pastas, commits, .gitignore |

5.2. Cálculo da nota:
   - Somar pontos de cada critério
   - Normalizar para 0-100

5.3. Gerar justificativa detalhada por critério

---

### FASE 6: Consolidação em CSV
6.1. Criar CSV com colunas:
   - Nome
   - Email
   - Link do Repositório
   - Resumo do Projeto
   - Pontuação Detalhada
   - Nota Final

6.2. Preencher uma linha por aluno

6.3. Salvar em `/workspace/resultado_validacao/resultado_final.csv`

---

### FASE 7: Geração de Relatórios Individuais
7.1. Para cada aluno, criar:
   - `relatorio_final.md` na pasta do aluno
   - Incluir:
     - Cabeçalho com identificação
     - Análise técnica
     - Pontuação por critério
     - Nota final
     - Feedback

7.2. Opcional: Versão HTML para visualização

---

## 🔧 Ferramentas Necessárias

### Python Libraries:
```python
requests          # Clonar repositórios via API
beautifulsoup4    # Extrair links do HTML
markdown          # Parse de README.md
pyyaml            # Configurações
pandas            # Gerar CSV
gitpython         # Operações Git
```

### Comandos Git:
- `git clone`
- `git log --before="data"`
- `git rev-list`
- `git checkout`

---

## 📊 Estrutura de Saída Esperada

```
/workspace/resultado_validacao/
├── repos/
│   ├── leonardo_vieira/
│   │   ├── repo_clonado/
│   │   ├── README.md
│   │   ├── commits.txt
│   │   └── imagens.txt
│   └── ...
├── relatorios/
│   ├── leonardo_vieira_relatorio.md
│   └── ...
├── resultado_final.csv
└── resumo_execucao.json
```

---

## ⚠️ Pontos de Atenção

1. **Repositórios Privados**: Alguns alunos podem ter repositórios privados
   - Solução: Tentar API do GitHub com token (se disponível)
   - Alternativa: Marcar como "Não avaliado - repositório privado"

2. **Prazos**: Commits após `2026-05-04 23:59:59` devem ser desconsiderados
   - Usar `git log --before="2026-05-04 23:59:59"`

3. **HTML Variado**: Formato do `textoonline.html` pode variar
   - Usar regex flexível para extrair URLs

4. **Encoding**: Nomes de alunos com caracteres especiais
   - Usar UTF-8 consistentemente

5. **Rate Limiting**: GitHub API tem limites
   - Usar git clone em vez de API quando possível
   - Adicionar delays entre requisições

---

## 🚀 Próximos Passos Imediatos

1. **Validar entendimento**: Confirmar se o plano está correto
2. **Escolher abordagem**: 
   - Opção A: Script 100% Python (mais rápido)
   - Opção B: Script com LLM para análise (mais preciso)
3. **Configurar ambiente**: Instalar dependências
4. **Executar em lote de teste**: Processar 3-5 alunos primeiro
5. **Ajustar e escalar**: Processar todos os 50+ alunos

---

## 📌 Decisões Pendentes

- [ ] Usar LLM para avaliação técnica ou regras manuais?
- [ ] Token do GitHub necessário? (para repositórios privados)
- [ ] Formato exato do CSV de saída (confirmar colunas)
- [ ] Incluir feedback detalhado por aluno no relatório?
- [ ] Gerar também versão HTML dos relatórios?

---

## 💡 Recomendação

**Abordagem Híbrida**:
- Python puro para: extração, clone, organização, CSV
- LLM (via API) apenas para: avaliação técnica qualitativa
- Vantagem: Equilíbrio entre velocidade e qualidade de análise

**Tempo estimado**:
- Preparação: 30 min
- Execução (50 alunos): 15-30 min (com paralelização)
- Total: ~1 hora

---

**Aguardando aprovação do plano para iniciar a implementação.**
