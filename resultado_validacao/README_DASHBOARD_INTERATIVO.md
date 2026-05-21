# 🚀 Dashboard Interativo IoT

Este sistema permite gerenciar as avaliações dos alunos de forma visual e interativa.

## 🎯 Funcionalidades

1.  **Visualizar Alunos**: Lista completa com notas automáticas e manuais.
2.  **Adicionar Notas Manuais**: Interface simples para inserir notas (0-100) e comentários.
3.  **Inserir Conteúdo Manual**: Editor para adicionar `README.md` e `main.py` de alunos que não enviaram ou possuem repositórios privados.
4.  **Consolidação Automática**: Botão para atualizar todos os dados e gerar o dashboard final.

## 🚀 Como Executar

Execute o servidor Python:

```bash
cd /workspace/resultado_validacao
python3 server_interativo.py
```

O dashboard estará disponível em: **http://localhost:8000**

## 🔄 Fluxo de Trabalho

1.  Abra o dashboard no navegador.
2.  Use a busca para encontrar um aluno.
3.  Clique em **✏️ Editar Notas/Conteúdo**.
4.  Insira a nota, comentário ou código manual.
5.  Clique em **Salvar Alterações**.
6.  Após editar todos os alunos desejados, clique em **🔄 Consolidar e Atualizar** no topo da página.
7.  Os dados serão processados e o dashboard principal (`dashboard_final.html`) será atualizado automaticamente.

## 📁 Arquivos Relacionados

-   `server_interativo.py`: Servidor backend (API).
-   `dashboard_interativo.html`: Interface frontend.
-   `notas_manuais.json`: Armazena as notas inseridas via dashboard.
-   `conteudos_manuais.json`: Armazena os conteúdos inseridos via dashboard.

---
**Status**: ✅ IMPLEMENTADO E PRONTO PARA USO
