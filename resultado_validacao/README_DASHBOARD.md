# 🎯 Dashboard de Resultados - Processo Seletivo IoT

## 📁 Arquivos Gerados

### Principal:
- **`dashboard_final.html`** - Dashboard interativo completo com todos os dados embutidos

### Suporte:
- `dashboard_completo.html` - Template HTML (precisa do JSON separado)
- `avaliacoes_com_feedback.json` - Dados das avaliações com feedbacks detalhados
- `index.html` - Versão original do dashboard

---

## 🚀 Como Usar

### Opção 1: Abrir Localmente (Recomendado)

1. Abra o arquivo `dashboard_final.html` no seu navegador:
   ```bash
   # No Linux
   xdg-open dashboard_final.html
   
   # No Windows (via WSL)
   explorer.exe file:///workspace/resultado_validacao/dashboard_final.html
   
   # Ou simplesmente clique duas vezes no arquivo
   ```

2. O dashboard carrega automaticamente com **todos os 77 alunos**

### Opção 2: Servidor HTTP Local

```bash
cd /workspace/resultado_validacao
python3 -m http.server 8080
```

Acesse: `http://localhost:8080/dashboard_final.html`

---

## ✨ Funcionalidades do Dashboard

### 1. **Busca e Filtros**
- 🔍 **Busca por nome**: Digite o nome do aluno
- 📊 **Filtro por nota**: Excelente (90-100), Bom (70-89), Médio (50-69), Ruim (<50)
- ✅ **Filtro por status**: Sucesso ou Erro

### 2. **Cards dos Alunos**
Cada card mostra:
- Nome e nota final (com cor baseada no desempenho)
- Email e link para repositório
- Status de submissão
- 5 critérios de avaliação em formato compacto

### 3. **Modal de Detalhes** (clique no card)

#### Critérios de Avaliação (Expansível)
- **Clique no cabeçalho** de cada critério para ver o feedback detalhado
- Feedback gerado automaticamente baseado na pontuação
- Cores indicam desempenho: 🟢 Verde (bom), 🟡 Amarelo (médio), 🔴 Vermelho (ruim)

#### Resumo do Projeto
- Texto rolável e expansível
- **Botão "Ler mais"** expande/recolhe o conteúdo
- Ideal para textos longos

#### Histórico de Commits
- Lista rolável com todos os commits
- Hash do commit em destaque
- Mensagem completa do commit

#### Informações do Projeto
- Link do repositório (clicável)
- Status da submissão
- Presença de arquivos importantes:
  - ✅ main.py
  - ✅ diagram.json
  - ✅ wokwi.toml
  - ✅ GitHub Actions

#### Análise do Projeto
- **Pontos Fortes**: O que o aluno fez bem
- **Pontos a Melhorar**: O que pode ser aprimorado

### 4. **Ações Rápidas**
No modal, dois botões:
- 📄 **Ver Relatório Completo**: Abre o relatório em Markdown
- 🔗 **Acessar Repositório**: Abre o repositório no GitHub

---

## 🎨 Cores das Notas

| Faixa | Cor | Classificação |
|-------|-----|---------------|
| 90-100 | 🟢 Verde | Excelente |
| 70-89 | 🔵 Azul | Bom |
| 50-69 | 🟡 Amarelo | Médio |
| 0-49 | 🔴 Vermelho | Abaixo do esperado |

---

## 📊 Estatísticas do Dashboard

- **Total de Alunos**: 77
- **Avaliações com Sucesso**: 72 (93.5%)
- **Nota Média**: 87.4
- **Maior Nota**: 97.9
- **Menor Nota**: 0.0 (repositórios não acessíveis)

---

## 🔧 Personalização

### Adicionar Mais Dados

Edite o script `gerar_feedbacks_llm.py` para incluir mais critérios ou mudar os feedbacks.

### Mudar Cores

No `dashboard_completo.html`, procure por `:root` no CSS e altere as variáveis:
```css
:root {
    --primary: #2563eb;  /* Cor principal */
    --success: #10b981;  /* Sucesso */
    --warning: #f59e0b;  /* Atenção */
    --danger: #ef4444;   /* Erro/Perigo */
}
```

### Adicionar Novas Funcionalidades

O dashboard é totalmente estático (HTML + CSS + JavaScript puro). Pode ser:
- Hospedado em qualquer servidor web
- Enviado por email (arquivo único)
- Aberto localmente sem servidor

---

## 🐛 Solução de Problemas

### Dashboard não carrega
- Verifique se o arquivo `dashboard_final.html` está completo
- Tente abrir em outro navegador (Chrome, Firefox, Edge)

### Dados não aparecem
- Verifique o console do navegador (F12) por erros
- Confirme que o JSON foi embutido corretamente

### Layout quebrado
- Limpe o cache do navegador (Ctrl+F5)
- Verifique se o CSS está sendo carregado

---

## 📝 Próximos Passos Sugeridos

1. ✅ **Dashboard concluído e funcional**
2. 🔄 Atualizar com novos dados (se necessário)
3. 📤 Compartilhar com a equipe
4. 🎯 Usar para avaliação final dos candidatos

---

**Dashboard gerado automaticamente em**: 2026-05-20  
**Local**: `/workspace/resultado_validacao/`  
**Arquivo principal**: `dashboard_final.html`
