#!/bin/bash
#
# Script de execução do Pipeline de Validação IoT
# Uso: ./run.sh ou bash run.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=============================================="
echo "  Pipeline de Validação IoT"
echo "=============================================="
echo ""
echo "Diretório: $SCRIPT_DIR"
echo "Data: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Verificar pré-requisitos
echo "Verificando pré-requisitos..."

if [ ! -f "avaliacoes_com_feedback.json" ]; then
    echo "❌ Erro: avaliacoes_com_feedback.json não encontrado"
    echo "   Execute primeiro os scripts de processamento básico."
    exit 1
fi

if [ ! -f "dashboard_completo.html" ]; then
    echo "❌ Erro: dashboard_completo.html não encontrado"
    echo "   O template do dashboard é necessário."
    exit 1
fi

echo "✅ Pré-requisitos OK"
echo ""

# Executar pipeline completo
echo "Executando pipeline completo..."
echo ""

python3 gerar_dashboard_completo.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=============================================="
    echo "  ✅ Pipeline concluído com sucesso!"
    echo "=============================================="
    echo ""
    echo "Arquivos de saída:"
    echo "  - dashboard_final.html"
    echo "  - avaliacoes_melhoradas.json"
    echo "  - avaliacoes_completas.json"
    echo ""
    echo "Para visualizar:"
    echo "  xdg-open dashboard_final.html"
    echo ""
else
    echo ""
    echo "=============================================="
    echo "  ❌ Erro na execução do pipeline"
    echo "=============================================="
    exit 1
fi
