# 📝 Sistema de Avaliação Manual Multi-Professor

## Visão Geral

O sistema foi atualizado para suportar múltiplos professores avaliando o mesmo aluno. Cada professor pode atribuir notas individuais por critério e a nota final do aluno será a **média aritmética** das avaliações de todos os professores.

## 🎯 Novas Funcionalidades

### 1. **Avaliação por Professor**
- Lista de professores configurável em `config.py`.
- Cada professor possui seu próprio registro de avaliação.
- Identificação do professor no momento da avaliação.

### 2. **Avaliação por Critério**
- Notas individuais para cada um dos 5 critérios (Lógica, Wokwi, CI/CD, Docs, Estrutura).
- Observações específicas para cada critério.
- Cálculo automático da nota total do professor.

### 3. **Cálculo de Média**
- A nota final manual do aluno é a média das notas totais de todos os professores que o avaliaram.
- Transparência no dashboard sobre quem avaliou e quais foram as notas.

---

## 📚 Como Usar

### Passo 1: Configurar Professores

Edite o arquivo `config.py` na raiz do projeto:

```python
# Professores
PROFESSORES = [
    "Professor 1",
    "Professor 2",
    "Professor 3"
]
```

### Passo 2: Adicionar Notas Manuais (CLI)

```bash
python3 scripts/adicionar_notas_manuais.py
```

1. **Selecione o Professor**: No início, escolha quem está avaliando.
2. **Escolha o Aluno**: Digite o número do aluno na lista.
3. **Avalie por Critério**:
   - Insira a nota para o critério (ex: Lógica de Firmware).
   - Insira uma observação para aquele critério.
4. **Salve**: Use o comando `s` para salvar as alterações.

### Passo 3: Avaliação via Dashboard Interativo

1. Inicie o servidor:
   ```bash
   python3 scripts/server_interativo.py
   ```
2. Acesse o dashboard no navegador.
3. Abra o modal de um aluno.
4. Na seção **Edição Manual**:
   - Selecione o seu nome na lista de professores.
   - Insira a nota e o comentário geral.
   - O sistema salvará automaticamente e calculará a média.

---

## 📊 Dashboard Aprimorado

O dashboard modal foi redesenhado para fornecer uma visão completa e sem rolagem:

### 1. **Navegação Rápida**
- Botões **◀ Anterior** e **Próximo ▶** no topo do modal, ao lado do nome do aluno.
- Suporte a navegação por teclado (Setas Esquerda/Direita).

### 2. **Layout Compacto (3 Colunas)**
- **Coluna 1**: Critérios Automáticos e Detalhes das Avaliações dos Professores.
- **Coluna 2**: Detalhes Técnicos, Checklist de Validação e Status do Repositório.
- **Coluna 3**: Edição Manual, Commits Recentes e Ações de IA.

### 3. **Visibilidade Total**
- O modal foi otimizado para caber inteiramente na tela (98% da altura do monitor padrão), eliminando a necessidade de rolagem interna.

---

## 📊 Estrutura de Dados (Novo Formato)

**data/notas_manuais.json:**
```json
{
  "Nome do Aluno": {
    "avaliacoes_professores": {
      "Professor 1": {
        "nota_total": 85.0,
        "data_avaliacao": "2026-05-26T14:30:00",
        "criterios": {
          "logica_firmware": { "nota": 25, "observacao": "Boa lógica" },
          "metrica_wokwi": { "nota": 15, "observacao": "Circuito básico" },
          ...
        }
      },
      "Professor 2": { ... }
    },
    "nota_final_manual": 85.0,
    "comentario": "Média das avaliações dos professores"
  }
}
```

---

## 🔄 Fluxo de Trabalho Atualizado

1. **Pipeline Automático**: `python3 00_run_all.py`
2. **Avaliação Manual**: `python3 scripts/adicionar_notas_manuais.py` (Múltiplos professores podem rodar este script).
3. **Consolidação**: `python3 scripts/consolidar_avaliacoes.py` (Calcula a média final).
4. **Visualização**: `python3 scripts/server_interativo.py` ou abra `reports/dashboard_final.html`.

---

**Documentação atualizada em: 26/05/2026**
**Versão: 2.0 (Sistema Multi-Professor)**
