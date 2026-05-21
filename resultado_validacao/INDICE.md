# 📚 Índice - Pipeline de Validação IoT

## 🚀 Comece Aqui

**Primeiro acesso?** → Veja [INICIO_RAPIDO.md](INICIO_RAPIDO.md)

**Quer entender o pipeline?** → Veja [DOCUMENTACAO.md](DOCUMENTACAO.md)

**Precisa de ajuda?** → Veja [README.md](README.md)

---

## 📋 Arquivos de Documentação

| Arquivo | Descrição | Quando Usar |
|---------|-----------|-------------|
| `INICIO_RAPIDO.md` | Guia de início rápido | Primeira vez usando |
| `README.md` | Documentação completa | Precisa de detalhes |
| `DOCUMENTACAO.md` | Documentação técnica | Implementação |
| `RESUMO_EXECUCAO.md` | Resumo da execução | Ver resultados |
| `RESUMO.txt` | Resumo em texto simples | Visão rápida |
| `README_DASHBOARD.md` | Detalhes do dashboard | Entender o dashboard |

---

## 🛠️ Scripts

### Principais

| Script | Descrição | Uso |
|--------|-----------|-----|
| `gerar_dashboard_completo.py` | Pipeline completo | **Recomendado** |
| `00_run_all.py` | Script mestre | Alternativa |
| `run.sh` | Script bash | Linux/WSL |
| `verificar_integridade.py` | Valida dados | Verificar erros |

### Fases Individuais (Avançado)

| Script | Fase | Descrição |
|--------|------|-----------|
| `extrair_commits.py` | 1 | Extrai commits |
| `processar_dados_completos.py` | 2 | Processa dados |
| `gerar_feedbacks_llm.py` | 3 | Gera feedbacks |
| `aplicar_melhorias.py` | 4 | Aplica melhorias |
| `gerar_json_dashboard.py` | 5 | JSON consolidado |
| `gerar_dashboard_final.py` | 6 | Dashboard HTML |

---

## 📊 Arquivos de Dados

### Entrada

| Arquivo | Descrição |
|---------|-----------|
| `avaliacoes_com_feedback.json` | Dados base com feedbacks |
| `repositorios_processados.json` | Repositórios clonados |
| `links_mapeados.json` | Links GitHub mapeados |

### Saída

| Arquivo | Descrição |
|---------|-----------|
| `dashboard_final.html` | **Dashboard interativo** ⭐ |
| `avaliacoes_melhoradas.json` | Dados completos |
| `avaliacoes_completas.json` | JSON consolidado |
| `avaliacoes_com_feedback.json` | Com feedbacks |
| `avaliacoes_com_commits.json` | Com commits |

---

## ⚙️ Configuração

| Arquivo | Descrição |
|---------|-----------|
| `config.json` | Configurações em JSON |
| `config.py` | Configurações em Python |

---

## 📁 Pastas

| Pasta | Descrição |
|-------|-----------|
| `repos/` | Repositórios clonados dos alunos |
| `relatorios/` | Relatórios individuais em Markdown |

---

## 🔍 Busca Rápida

### "Como executar o pipeline?"
→ `python3 gerar_dashboard_completo.py`

### "Como visualizar o dashboard?"
→ `xdg-open dashboard_final.html`

### "Como verificar se os dados estão corretos?"
→ `python3 verificar_integridade.py`

### "Onde está o resultado final?"
→ `dashboard_final.html`

### "Como funciona a avaliação?"
→ Veja critérios em [DOCUMENTACAO.md](DOCUMENTACAO.md#critérios-de-avaliação)

### "Preciso de ajuda"
→ Veja [README.md](README.md#solução-de-problemas)

---

## 📈 Estatísticas Rápidas

- **Total de alunos:** 77
- **Sucesso:** 72 (93.5%)
- **Nota média:** 87.4
- **Maior nota:** 97.9

---

## 🔗 Links Úteis

- [Plano Original](../plano_validacao_iot.md)
- [Dashboard Final](dashboard_final.html)
- [Documentação Completa](DOCUMENTACAO.md)

---

## 📞 Precisa de Mais Ajuda?

1. Verifique [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
2. Consulte [DOCUMENTACAO.md](DOCUMENTACAO.md)
3. Execute `python3 verificar_integridade.py`
4. Veja [RESUMO_EXECUCAO.md](RESUMO_EXECUCAO.md)

---

**Última atualização:** 2026-05-20  
**Status:** ✅ Funcional
