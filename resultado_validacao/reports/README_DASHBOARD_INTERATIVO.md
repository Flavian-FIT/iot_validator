# 🚀 Dashboard Integrado IoT

Este sistema unifica a visualização detalhada das avaliações com a capacidade de gerenciamento manual.

## 🎯 Funcionalidades

1.  **Visualização Completa**: Acesso a commits, feedbacks detalhados, análise de artefatos e ranking.
2.  **Edição Ágil**: Botão "Editar" disponível diretamente no card do aluno ou no modal de detalhes.
3.  **Gestão de Notas**: Interface para inserir notas manuais (0-100) e comentários que sobrescrevem a avaliação automática.
4.  **Correção de Conteúdo**: Editor para adicionar `README.md` e `main.py` manualmente, útil para repositórios privados ou incompletos.
5.  **Pipeline Integrado**: Botão de consolidação que executa todo o processo de validação, ranking e geração do dashboard estático.

## 🚀 Como Executar

Execute o servidor Python:

```bash
cd /workspace/resultado_validacao
python3 server_interativo.py
```

O dashboard estará disponível em: **http://localhost:8000**

## 🔄 Fluxo de Trabalho

1.  **Exploração**: Navegue pelos alunos, use a busca e os filtros de nota/status.
2.  **Análise**: Clique no card de um aluno para ver o feedback da IA, histórico de commits e pontos fortes/fracos.
3.  **Ajuste**: Se necessário, clique em **✏️ Editar** para aplicar uma nota manual ou corrigir o comentário.
4.  **Salvamento**: Clique em **Salvar Alterações** para gravar os dados nos arquivos JSON.
5.  **Atualização**: Clique em **🔄 Consolidar Tudo** para regerar o ranking e o `dashboard_final.html`.

## 📁 Arquivos Relacionados

-   `server_interativo.py`: Servidor backend (API).
-   `dashboard_interativo.html`: Interface frontend.
-   `notas_manuais.json`: Armazena as notas inseridas via dashboard.
-   `conteudos_manuais.json`: Armazena os conteúdos inseridos via dashboard.

---
**Status**: ✅ IMPLEMENTADO E PRONTO PARA USO
