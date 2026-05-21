# 📝 Sistema de Avaliação Manual e Inserção de Conteúdo

## Visão Geral

Este sistema permite **adicionar notas manualmente** e **inserir conteúdo de alunos** de forma manual, combinando com a avaliação automática do script.

## 🎯 Funcionalidades Adicionadas

### 1. **Notas Manuais do Professor**
- Adicionar notas manualmente para cada aluno
- Inserir comentários do professor
- Comparar notas automáticas vs manuais
- Visualizar diferenças entre as duas avaliações

### 2. **Inserção de Conteúdo Manual**
- Inserir README.md manualmente
- Adicionar código main.py
- Inserir diagram.json (Wokwi)
- Importar de arquivos externos

### 3. **Consolidação de Avaliações**
- Combina notas automáticas e manuais
- Gera relatório comparativo
- Mantém histórico de ambas as avaliações

---

## 📚 Como Usar

### Passo 1: Adicionar Notas Manuais

```bash
cd /workspace/resultado_validacao
python3 adicionar_notas_manuais.py
```

**Opções disponíveis:**

1. **Modo Interativo**
   - Digite o número do aluno
   - Insira a nota (0-100)
   - Adicione comentário (opcional)
   - Repita para vários alunos

2. **Modo Planilha CSV**
   - Gera template CSV
   - Preencha externamente
   - Ideal para muitas avaliações

**Exemplo de uso:**
```
ESCOLHA O MODO DE OPERAÇÃO
1. Modo Interativo (adicionar notas uma a uma)
2. Gerar planilha CSV (preencher externamente)
3. Sair

Opção (1/2/3): 1

Aluno (número), comando (l/v/s/q): 1

================================================================================
Avaliando: Maria Madalena Silva_203
================================================================================

📊 AVALIAÇÃO AUTOMÁTICA:
  logica_firmware: 27/30
  metrica_wokvi: 20/20
  ci_cd: 20/25
  documentacao: 10/10
  estrutura: 8/10
  TOTAL: 89.5/100

📝 INSERIR NOTAS MANUAIS (0-100):
  Nota Final Manual (0-100): 92
  Comentário do Professor: Excelente trabalho, mas pode melhorar CI/CD

✅ Nota manual salva para Maria Madalena Silva_203: 92.0
```

---

### Passo 2: Inserir Conteúdo Manualmente

```bash
python3 inserir_conteudo_manual.py
```

**Tipos de conteúdo suportados:**
- README.md - Documentação do projeto
- main.py - Código do firmware
- diagram.json - Diagrama do Wokwi
- Outros arquivos

**Exemplo de uso:**
```
1. Inserir conteúdo de um aluno
2. Visualizar conteúdos inseridos
3. Remover conteúdo de um aluno
4. Listar todos os alunos
5. Salvar e sair

Escolha uma opção (1-5): 1

Digite o número do aluno (1-50): 1

================================================================================
Inserindo conteúdo para: Maria Madalena Silva_203
================================================================================

Tipo de conteúdo:
  1. README.md
  2. main.py (código)
  3. diagram.json (Wokwi)
  4. Outro arquivo

Escolha o tipo (1-4): 1

================================================================================
COLE O CONTEÚDO ABAIXO
================================================================================
Digite o conteúdo e pressione Enter, depois digite 'FIM':

# Projeto IoT
Conteúdo do README aqui...

FIM

✅ Conteúdo 'readme' inserido para Maria Madalena Silva_203 (1234 caracteres)
```

**Importar de arquivo:**
```bash
python3 inserir_conteudo_manual.py --import
```

---

### Passo 3: Consolidar Avaliações

```bash
python3 consolidar_avaliacoes.py
```

**O que este script faz:**
- Carrega avaliações automáticas
- Carrega notas manuais (se existirem)
- Combina as duas fontes
- Calcula diferenças
- Gera relatório comparativo

**Saída:**
```
================================================================================
CONSOLIDANDO AVALIAÇÕES - AUTOMÁTICO + MANUAL
================================================================================

✅ 50 avaliações automáticas carregadas
📝 15 notas manuais encontradas

✓ Maria Madalena Silva_203: Auto=89.5, Manual=92.0, Diferença=+2.5
  João Silva_145: Auto=75.0 (sem avaliação manual)

================================================================================
RESUMO DA CONSOLIDAÇÃO
================================================================================
Total de alunos: 50
Com avaliação manual: 15
Sem avaliação manual: 35

Estatísticas das diferenças (Manual - Automática):
  Média: +3.2
  Máxima: +8.5
  Mínima: -2.0

Notas Finais (com manual quando disponível):
  Média: 82.45
  Máxima: 95.00
  Mínima: 45.00
```

---

## 📊 Estrutura de Arquivos

### Arquivos Gerados

| Arquivo | Descrição |
|---------|-----------|
| `notas_manuais.json` | Notas e comentários dos professores |
| `conteudos_manuais.json` | Conteúdos manuais inseridos |
| `avaliacoes_consolidadas.json` | Avaliações combinadas (auto + manual) |
| `relatorio_comparativo.txt` | Relatório comparativo |

### Estrutura de Dados

**notas_manuais.json:**
```json
{
  "Maria Madalena Silva_203": {
    "nota_final_manual": 92.0,
    "comentario": "Excelente trabalho, mas pode melhorar CI/CD",
    "nota_automatica": 89.5,
    "data_avaliacao": "2026-05-20T14:30:00"
  }
}
```

**conteudos_manuais.json:**
```json
{
  "Maria Madalena Silva_203": {
    "readme": {
      "conteudo": "# Projeto IoT...",
      "data_insercao": "2026-05-20T14:30:00",
      "tamanho": 1234
    }
  }
}
```

**avaliacoes_consolidadas.json:**
```json
{
  "nome": "Maria Madalena Silva_203",
  "nota_automatica": 89.5,
  "nota_manual": 92.0,
  "nota_final": 92.0,
  "diferenca": 2.5,
  "tem_avaliacao_manual": true,
  "comentario_professor": "Excelente trabalho..."
}
```

---

## 🔄 Fluxo de Trabalho Recomendado

### Cenário 1: Avaliação Completa

1. **Executar pipeline automático**
   ```bash
   python3 00_run_all.py
   ```

2. **Adicionar notas manuais**
   ```bash
   python3 adicionar_notas_manuais.py
   ```

3. **Inserir conteúdo faltante (opcional)**
   ```bash
   python3 inserir_conteudo_manual.py
   ```

4. **Consolidar resultados**
   ```bash
   python3 consolidar_avaliacoes.py
   ```

5. **Gerar dashboard final**
   ```bash
   python3 gerar_dashboard_final.py
   ```

### Cenário 2: Apenas Notas Manuais

Se quiser usar APENAS notas manuais (ignorar automática):

```bash
# 1. Adicione as notas manuais
python3 adicionar_notas_manuais.py

# 2. Consolide (usará manual quando existir)
python3 consolidar_avaliacoes.py
```

### Cenário 3: Conteúdo Manual Apenas

Se o repositório não existe ou está incompleto:

```bash
# 1. Insira o conteúdo manualmente
python3 inserir_conteudo_manual.py

# 2. O conteúdo será usado na próxima execução do pipeline
```

---

## 📋 Comandos Rápidos

```bash
# Listar alunos
python3 adicionar_notas_manuais.py  # e use comando 'l'

# Adicionar nota para aluno específico
python3 adicionar_notas_manuais.py  # modo interativo

# Inserir README manual
python3 inserir_conteudo_manual.py

# Importar conteúdo de arquivo
python3 inserir_conteudo_manual.py --import

# Consolidar tudo
python3 consolidar_avaliacoes.py

# Visualizar relatório
cat relatorio_comparativo.txt
```

---

## ⚠️ Pontos de Atenção

1. **Notas Manuais:**
   - Devem estar entre 0 e 100
   - Comentários são opcionais
   - Podem ser alteradas a qualquer momento

2. **Conteúdo Manual:**
   - Suporta UTF-8 (acentos, emojis)
   - Tamanho máximo: ilimitado (depende do disco)
   - Substitui conteúdo automático se existir

3. **Consolidação:**
   - Usa nota manual quando disponível
   - Usa nota automática como fallback
   - Mantém histórico de ambas

4. **Arquivos:**
   - Sempre faça backup antes de editar manualmente
   - Use encoding UTF-8
   - Não edite JSON manualmente (use os scripts)

---

## 🎓 Exemplos de Uso

### Exemplo 1: Corrigir nota de um aluno

```bash
$ python3 adicionar_notas_manuais.py

Escolha uma opção (1/2/3): 1

Aluno (número), comando (l/v/s/q): 1
Avaliando: Maria Madalena Silva_203

Nota Final Manual (0-100): 95
Comentário: Aluna demonstrou excelente domínio do conteúdo.

✅ Nota manual salva
```

### Exemplo 2: Inserir README de repositório privado

```bash
$ python3 inserir_conteudo_manual.py

Opção: 1
Aluno: 1
Tipo: 1 (README.md)

[cole o conteúdo do README]
FIM

✅ Conteúdo 'readme' inserido
```

### Exemplo 3: Importar código de arquivo

```bash
$ python3 inserir_conteudo_manual.py --import

Aluno: 5
Caminho: /caminho/para/main.py

✅ Conteúdo importado de /caminho/para/main.py
```

---

## 📞 Suporte

Em caso de dúvidas ou problemas:

1. Verifique os logs dos scripts
2. Confira se os arquivos JSON são válidos
3. Use encoding UTF-8
4. Mantenha backup dos arquivos originais

---

## 📊 Dashboard

Após consolidar as avaliações, execute:

```bash
python3 gerar_dashboard_final.py
```

O dashboard mostrará:
- ✅ Notas automáticas
- 📝 Notas manuais (quando disponíveis)
- 📈 Comparativo entre as duas
- 💡 Comentários do professor

---

**Documentação criada em: 2026-05-20**
**Versão: 1.0**
