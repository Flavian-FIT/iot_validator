# 🚀 Início Rápido - Pipeline de Validação IoT

## Executar Pipeline Completo

```bash
cd /workspace/resultado_validacao
python3 gerar_dashboard_completo.py
```

## Visualizar Dashboard

```bash
# Linux
xdg-open dashboard_final.html

# Windows (WSL)
explorer.exe file:///workspace/resultado_validacao/dashboard_final.html
```

## Estrutura

- `gerar_dashboard_completo.py` - Pipeline completo (6 fases)
- `00_run_all.py` - Script mestre alternativo
- `run.sh` - Script bash
- `README.md` - Documentação completa
- `RESUMO_EXECUCAO.md` - Resumo da última execução

## Saída

- `dashboard_final.html` - Dashboard interativo
- `avaliacoes_melhoradas.json` - Dados processados
- `avaliacoes_completas.json` - JSON consolidado

## Status

✅ **Pipeline funcional - 77 alunos processados**
