#!/usr/bin/env python3
"""
Guia Rápido de Uso - Sistema de Avaliação Manual
Execute este script para ver um resumo das opções disponíveis
"""
import os
import sys

RESULTADO_PATH = "/workspace/resultado_validacao"

def verificar_arquivos():
    """Verifica quais arquivos existem"""
    print("\n" + "="*80)
    print("VERIFICANDO ARQUIVOS")
    print("="*80)
    
    arquivos = [
        'avaliacoes_com_feedback.json',
        'notas_manuais.json',
        'conteudos_manuais.json',
        'avaliacoes_consolidadas.json'
    ]
    
    for arquivo in arquivos:
        caminho = os.path.join(RESULTADO_PATH, arquivo)
        if os.path.exists(caminho):
            print(f"  ✓ {arquivo}")
        else:
            print(f"  ✗ {arquivo} (não encontrado)")

def main():
    print("\n" + "="*80)
    print(" SISTEMA DE AVALIAÇÃO MANUAL E INSERÇÃO DE CONTEÚDO - IOT")
    print("="*80)
    print()
    print(" Este sistema permite:")
    print("  1. Adicionar notas manualmente (professor)")
    print("  2. Inserir conteúdo de alunos manualmente")
    print("  3. Combinar avaliações automáticas e manuais")
    print()
    
    # Verificar arquivos
    verificar_arquivos()
    
    print("\n" + "="*80)
    print(" COMANDOS DISPONÍVEIS")
    print("="*80)
    print()
    print(" 1. Adicionar notas manuais:")
    print("    python3 adicionar_notas_manuais.py")
    print()
    print(" 2. Inserir conteúdo manual:")
    print("    python3 inserir_conteudo_manual.py")
    print()
    print(" 3. Consolidar avaliações:")
    print("    python3 consolidar_avaliacoes.py")
    print()
    print(" 4. Este guia (ajuda):")
    print("    python3 guia_rapido.py")
    print()
    
    print("="*80)
    print(" EXEMPLO DE FLUXO COMPLETO")
    print("="*80)
    print()
    print(" # 1. Adicionar notas manuais")
    print(" python3 adicionar_notas_manuais.py")
    print()
    print(" # 2. (Opcional) Inserir conteúdo manual")
    print(" python3 inserir_conteudo_manual.py")
    print()
    print(" # 3. Consolidar avaliações")
    print(" python3 consolidar_avaliacoes.py")
    print()
    print(" # 4. Gerar dashboard")
    print(" python3 gerar_dashboard_final.py")
    print()
    
    print("="*80)
    print(" DOCUMENTAÇÃO COMPLETA")
    print("="*80)
    print()
    print(" Consulte: /workspace/resultado_validacao/COMO_USAR_AVALIACAO_MANUAL.md")
    print(" Resumo:   /workspace/resultado_validacao/RESUMO_IMPLEMENTACAO.md")
    print()
    print("="*80)

if __name__ == '__main__':
    main()
