#!/usr/bin/env python3
"""
Script para adicionar notas manuais do professor
Permite inserir notas manualmente para cada aluno e combinar com avaliação automática
"""
import json
import os
import sys
from pathlib import Path

RESULTADO_PATH = "/workspace/resultado_validacao"
ARQUIVO_AVALIACOES = "avaliacoes_com_feedback.json"
ARQUIVO_NOTAS_MANUAIS = "notas_manuais.json"

def carregar_avaliacoes():
    """Carrega as avaliações automáticas existentes"""
    caminho = os.path.join(RESULTADO_PATH, ARQUIVO_AVALIACOES)
    if not os.path.exists(caminho):
        print(f"❌ Arquivo não encontrado: {caminho}")
        return None
    
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_ou_criar_notas_manuais():
    """Carrega notas manuais existentes ou cria estrutura vazia"""
    caminho = os.path.join(RESULTADO_PATH, ARQUIVO_NOTAS_MANUAIS)
    
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # Criar estrutura vazia
    return {}

def salvar_notas_manuais(notas_manuais):
    """Salva as notas manuais no arquivo"""
    caminho = os.path.join(RESULTADO_PATH, ARQUIVO_NOTAS_MANUAIS)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(notas_manuais, f, indent=2, ensure_ascii=False)
    print(f"✅ Notas salvas em: {caminho}")

def listar_alunos(avaliacoes):
    """Lista todos os alunos com seus índices"""
    print("\n" + "="*80)
    print("LISTA DE ALUNOS")
    print("="*80)
    
    for i, aluno in enumerate(avaliacoes, 1):
        nome = aluno.get('nome', 'Desconhecido')
        nota_auto = aluno.get('nota_final', 0)
        print(f"{i:3d}. {nome} (Nota Automática: {nota_auto:.1f})")
    
    return len(avaliacoes)

def calcular_nota_final(criterios):
    """Calcula a nota total baseada nos critérios"""
    total = 0
    for criterio, dados in criterios.items():
        total += dados.get('score', 0)
    return total

def modo_interativo(avaliacoes, notas_manuais):
    """Modo interativo para adicionar notas manualmente"""
    print("\n" + "="*80)
    print("MODO INTERATIVO - ADICIONAR NOTAS MANUAIS")
    print("="*80)
    print("\nComandos:")
    print("  - Digite o número do aluno para avaliar")
    print("  - 'l' para listar alunos")
    print("  - 'v' para visualizar avaliações salvas")
    print("  - 's' para salvar e sair")
    print("  - 'q' para sair sem salvar")
    print("="*80)
    
    while True:
        entrada = input("\nAluno (número), comando (l/v/s/q): ").strip().lower()
        
        if entrada == 'q':
            confirm = input("Deseja sair sem salvar? (s/n): ").strip().lower()
            if confirm == 's':
                return False
            
        elif entrada == 'l':
            listar_alunos(avaliacoes)
            
        elif entrada == 'v':
            if not notas_manuais:
                print("Nenhuma avaliação manual salva ainda.")
            else:
                print(f"\nAvaliações manuais salvas: {len(notas_manuais)}")
                for nome, dados in notas_manuais.items():
                    print(f"  - {nome}: Nota = {dados.get('nota_final_manual', 0)}")
                    
        elif entrada == 's':
            if notas_manuais:
                salvar_notas_manuais(notas_manuais)
                print(f"✅ {len(notas_manuais)} avaliações manuais salvas!")
            return True
            
        elif entrada.isdigit():
            idx = int(entrada) - 1
            if 0 <= idx < len(avaliacoes):
                aluno = avaliacoes[idx]
                nome = aluno.get('nome', 'Desconhecido')
                print(f"\n{'='*80}")
                print(f"Avaliando: {nome}")
                print(f"{'='*80}")
                
                # Mostrar avaliação automática atual
                print("\n📊 AVALIAÇÃO AUTOMÁTICA:")
                criterios_auto = aluno.get('criterios', {})
                for crit, dados in criterios_auto.items():
                    score = dados.get('score', 0)
                    max_score = 30 if crit == 'logica_firmware' else (25 if crit == 'ci_cd' else (20 if crit == 'metrica_wokwi' else 10))
                    print(f"  {crit}: {score}/{max_score}")
                print(f"  TOTAL: {calcular_nota_final(criterios_auto)}/100")
                
                # Coletar notas manuais
                print("\n📝 INSERIR NOTAS MANUAIS (0-100):")
                
                try:
                    nota_final_manual = input("  Nota Final Manual (0-100): ").strip()
                    if nota_final_manual == '':
                        print("  ⚠️ Nota não informada, pulando...")
                        continue
                    
                    nota_final_manual = float(nota_final_manual)
                    if nota_final_manual < 0 or nota_final_manual > 100:
                        print("  ❌ Nota deve estar entre 0 e 100")
                        continue
                        
                except ValueError:
                    print("  ❌ Valor inválido!")
                    continue
                
                # Coletar comentário do professor
                print("\n  Comentário do Professor (opcional, 'pula' para pular):")
                comentario = input("  > ").strip()
                if comentario.lower() == 'pula':
                    comentario = ""
                
                # Salvar nota manual
                notas_manuais[nome] = {
                    'nota_final_manual': nota_final_manual,
                    'comentario': comentario,
                    'nota_automatica': calcular_nota_final(criterios_auto),
                    'data_avaliacao': str(pd.Timestamp.now()) if 'pd' in sys.modules else str(pd.Timestamp.now()) if 'pd' in locals() else str(pd.Timestamp.now())
                }
                
                print(f"\n✅ Nota manual salva para {nome}: {nota_final_manual}")
                print(f"   Comentário: {comentario if comentario else '(sem comentário)'}")
                
            else:
                print(f"❌ Índice inválido! Digite um número entre 1 e {len(avaliacoes)}")
        else:
            print("Comando não reconhecido. Use 'l', 'v', 's', 'q' ou um número.")

def modo_arquivo(avaliacoes, notas_manuais):
    """Modo que gera arquivo CSV para preenchimento externo"""
    import csv
    
    print("\n" + "="*80)
    print("MODO ARQUIVO - GERAR PLANILHA PARA PREENCHIMENTO")
    print("="*80)
    
    # Gerar CSV com estrutura para preenchimento
    csv_path = os.path.join(RESULTADO_PATH, "notas_manuais_template.csv")
    
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['nome_aluno', 'nota_manual', 'comentario_professor'])
        writer.writerow('# Preencha as notas abaixo (0-100) e comentários')
        
        for aluno in avaliacoes:
            nome = aluno.get('nome', '')
            writer.writerow([nome, '', ''])
    
    print(f"\n✅ Planilha template gerada: {csv_path}")
    print("\nInstruções:")
    print("1. Abra o arquivo CSV em um editor de texto ou planilha")
    print("2. Preencha a coluna 'nota_manual' com valores de 0-100")
    import time
    time.sleep(2)

def main():
    print("="*80)
    print("SISTEMA DE AVALIAÇÃO MANUAL - IOT")
    print("="*80)
    
    # Carregar avaliações automáticas
    avaliacoes = carregar_avaliacoes()
    if not avaliacoes:
        return 1
    
    print(f"\n✅ {len(avaliacoes)} alunos carregados das avaliações automáticas")
    
    # Carregar ou criar notas manuais
    notas_manuais = carregar_ou_criar_notas_manuais()
    if notas_manuais:
        print(f"📝 {len(notas_manuais)} avaliações manuais encontradas")
    
    # Listar alunos
    total = listar_alunos(avaliacoes)
    
    # Menu principal
    print("\n" + "="*80)
    print("ESCOLHA O MODO DE OPERAÇÃO")
    print("="*80)
    print("1. Modo Interativo (adicionar notas uma a uma)")
    print("2. Gerar planilha CSV (preencher externamente)")
    print("3. Sair")
    
    escolha = input("\nOpção (1/2/3): ").strip()
    
    if escolha == '1':
        sucesso = modo_interativo(avaliacoes, notas_manuais)
        if sucesso and notas_manuais:
            salvar_notas_manuais(notas_manuais)
    elif escolha == '2':
        modo_arquivo(avaliacoes, notas_manuais)
    else:
        print("Operação cancelada.")
        return 0
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
