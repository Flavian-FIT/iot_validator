#!/usr/bin/env python3
"""
Script para inserir conteúdo de alunos manualmente
Permite adicionar README, código, ou outros arquivos de forma manual
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime

RESULTADO_PATH = "/workspace/resultado_validacao"
ARQUIVO_AVALIACOES = "avaliacoes_com_feedback.json"
ARQUIVO_CONTEUDOS_MANUAIS = "conteudos_manuais.json"

def carregar_arquivo(nome_arquivo):
    """Carrega um arquivo JSON"""
    caminho = os.path.join(RESULTADO_PATH, nome_arquivo)
    if not os.path.exists(caminho):
        return None
    
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_conteudos_manuais(conteudos):
    """Salva os conteúdos manuais"""
    caminho = os.path.join(RESULTADO_PATH, ARQUIVO_CONTEUDOS_MANUAIS)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(conteudos, f, indent=2, ensure_ascii=False)
    print(f"✅ Conteúdos salvos em: {caminho}")

def listar_alunos(avaliacoes):
    """Lista todos os alunos"""
    print("\n" + "="*80)
    print("LISTA DE ALUNOS")
    print("="*80)
    
    for i, aluno in enumerate(avaliacoes, 1):
        nome = aluno.get('nome', 'Desconhecido')
        github = aluno.get('github_url', 'N/A')
        print(f"{i:3d}. {nome}")
        print(f"     GitHub: {github}")
    
    return len(avaliacoes)

def menu_principal():
    """Menu principal do script"""
    print("="*80)
    print("INSERÇÃO MANUAL DE CONTEÚDO - IOT")
    print("="*80)
    
    # Carregar avaliações
    avaliacoes = carregar_arquivo(ARQUIVO_AVALIACOES)
    if not avaliacoes:
        print(f"❌ Erro: Arquivo {ARQUIVO_AVALIACOES} não encontrado")
        return 1
    
    print(f"\n✅ {len(avaliacoes)} alunos carregados")
    
    # Carregar conteúdos manuais existentes
    conteudos_manuais = carregar_arquivo(ARQUIVO_CONTEUDOS_MANUAIS)
    if conteudos_manuais:
        print(f"📝 {len(conteudos_manuais)} conteúdos manuais encontrados")
    else:
        conteudos_manuais = {}
        print("📝 Nenhum conteúdo manual encontrado (será criado)")
    
    # Listar alunos
    total = listar_alunos(avaliacoes)
    
    # Menu de opções
    print("\n" + "="*80)
    print("OPÇÕES")
    print("="*80)
    print("1. Inserir conteúdo de um aluno")
    print("2. Visualizar conteúdos inseridos")
    print("3. Remover conteúdo de um aluno")
    print("4. Listar todos os alunos")
    print("5. Salvar e sair")
    print("6. Sair sem salvar")
    
    while True:
        opcao = input("\nEscolha uma opção (1-6): ").strip()
        
        if opcao == '1':
            # Inserir conteúdo
            idx_str = input("Digite o número do aluno (1-" + str(total) + "): ").strip()
            
            if not idx_str.isdigit():
                print("❌ Digite um número válido!")
                continue
            
            idx = int(idx_str) - 1
            if idx < 0 or idx >= total:
                print("❌ Número fora do intervalo!")
                continue
            
            aluno = avaliacoes[idx]
            nome = aluno.get('nome', '')
            
            print(f"\n{'='*80}")
            print(f"Inserindo conteúdo para: {nome}")
            print(f"{'='*80}")
            
            # Tipo de conteúdo
            print("\nTipo de conteúdo:")
            print("  1. README.md")
            print("  2. main.py (código)")
            print("  3. diagram.json (Wokwi)")
            print("  4. Outro arquivo")
            
            tipo = input("\nEscolha o tipo (1-4): ").strip()
            
            tipos_map = {
                '1': 'readme',
                '2': 'main_py',
                '3': 'diagram_json',
                '4': 'outro'
            }
            
            if tipo not in tipos_map:
                print("❌ Tipo inválido!")
                continue
            
            tipo_conteudo = tipos_map[tipo]
            
            if tipo == '4':
                tipo_conteudo = input("Digite o tipo/nome do arquivo: ").strip()
            
            # Conteúdo
            print("\n" + "="*80)
            print("COLE O CONTEÚDO ABAIXO")
            print("="*80)
            print("Digite o conteúdo e pressione Enter, depois digite 'FIM' em uma linha separada:")
            
            linhas = []
            while True:
                linha = input()
                if linha.strip() == 'FIM':
                    break
                linhas.append(linha)
            
            conteudo = '\n'.join(linhas)
            
            # Salvar no dicionário
            if nome not in conteudos_manuais:
                conteudos_manuais[nome] = {}
            
            conteudos_manuais[nome][tipo_conteudo] = {
                'conteudo': conteudo,
                'data_insercao': datetime.now().isoformat(),
                'tamanho': len(conteudo)
            }
            
            print(f"\n✅ Conteúdo '{tipo_conteudo}' inserido para {nome} ({len(conteudo)} caracteres)")
            
        elif opcao == '2':
            # Visualizar conteúdos
            if not conteudos_manuais:
                print("Nenhum conteúdo manual inserido ainda.")
                continue
            
            print("\n" + "="*80)
            print("CONTEÚDOS MANUAIS INSERIDOS")
            print("="*80)
            
            for nome, dados in conteudos_manuais.items():
                print(f"\n{nome}:")
                for tipo, info in dados.items():
                    if isinstance(info, dict):
                        tamanho = info.get('tamanho', 0)
                        data = info.get('data_insercao', 'N/A')
                        print(f"  - {tipo}: {tamanho} chars ({data})")
                    else:
                        print(f"  - {tipo}")
        
        elif opcao == '3':
            # Remover conteúdo
            nome = input("Digite o nome do aluno: ").strip()
            
            if nome in conteudos_manuais:
                confirm = input(f"Remover todo o conteúdo de {nome}? (s/n): ").strip().lower()
                if confirm == 's':
                    del conteudos_manuais[nome]
                    print(f"✅ Conteúdo removido para {nome}")
            else:
                print(f"⚠️  Nenhum conteúdo encontrado para {nome}")
        
        elif opcao == '4':
            # Listar alunos
            listar_alunos(avaliacoes)
        
        elif opcao == '5':
            # Salvar e sair
            salvar_conteudos_manuais(conteudos_manuais)
            print(f"\n✅ {len(conteudos_manuais)} conteúdos manuais salvos!")
            return 0
        
        elif opcao == '6':
            # Sair sem salvar
            confirm = input("Deseja sair sem salvar? (s/n): ").strip().lower()
            if confirm == 's':
                print("Operação cancelada.")
                return 0
    
    return 0

def modo_importar_arquivo():
    """Modo para importar conteúdo de arquivo"""
    print("\n" + "="*80)
    print("MODO IMPORTAR ARQUIVO")
    print("="*80)
    
    # Carregar avaliações
    avaliacoes = carregar_arquivo(ARQUIVO_AVALIACOES)
    if not avaliacoes:
        print(f"❌ Erro: Arquivo {ARQUIVO_AVALIACOES} não encontrado")
        return 1
    
    # Listar alunos
    total = listar_alunos(avaliacoes)
    
    idx_str = input("\nDigite o número do aluno (1-" + str(total) + "): ").strip()
    
    if not idx_str.isdigit():
        print("❌ Digite um número válido!")
        return 1
    
    idx = int(idx_str) - 1
    if idx < 0 or idx >= total:
        print("❌ Número fora do intervalo!")
        return 1
    
    aluno = avaliacoes[idx]
    nome = aluno.get('nome', '')
    
    # Caminho do arquivo
    arquivo_path = input("Digite o caminho do arquivo: ").strip()
    
    if not os.path.exists(arquivo_path):
        print(f"❌ Arquivo não encontrado: {arquivo_path}")
        return 1
    
    # Ler conteúdo
    with open(arquivo_path, 'r', encoding='utf-8', errors='ignore') as f:
        conteudo = f.read()
    
    # Determinar tipo
    if arquivo_path.endswith('.md'):
        tipo = 'readme'
    elif arquivo_path.endswith('.py'):
        tipo = 'main_py'
    elif arquivo_path.endswith('.json'):
        tipo = 'diagram_json'
    else:
        tipo = 'outro'
    
    # Carregar conteúdos existentes
    conteudos_manuais = carregar_arquivo(ARQUIVO_CONTEUDOS_MANUAIS)
    if not conteudos_manuais:
        conteudos_manuais = {}
    
    if nome not in conteudos_manuais:
        conteudos_manuais[nome] = {}
    
    conteudos_manuais[nome][tipo] = {
        'conteudo': conteudo,
        'data_insercao': datetime.now().isoformat(),
        'tamanho': len(conteudo),
        'arquivo_origem': arquivo_path
    }
    
    # Salvar
    salvar_conteudos_manuais(conteudos_manuais)
    print(f"\n✅ Conteúdo importado de {arquivo_path} para {nome}")
    
    return 0

if __name__ == '__main__':
    # Verificar modo de operação
    if len(sys.argv) > 1 and sys.argv[1] == '--import':
        sys.exit(modo_importar_arquivo())
    else:
        sys.exit(menu_principal())
