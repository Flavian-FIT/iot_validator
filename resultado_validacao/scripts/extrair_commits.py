#!/usr/bin/env python3
"""
Extrair commits entre commit inicial e data limite
Versão Reorganizada - Usa config.py
"""
import os
import subprocess
import json
import sys
from pathlib import Path

# Adicionar pasta pai ao path para importar config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def get_all_commits_between(repo_path, start_commit, end_date):
    """
    Extrai todos os commits entre um commit específico e uma data
    """
    try:
        # Salvar diretório atual
        original_cwd = os.getcwd()
        os.chdir(repo_path)
        
        # Primeiro, verificar se o commit inicial existe neste repositório
        result = subprocess.run(
            ['git', 'cat-file', '-e', start_commit],
            capture_output=True, text=True
        )
        
        if result.returncode != 0:
            # Commit não existe neste repositório
            # Pegar todos os commits até a data limite
            result = subprocess.run(
                ['git', 'log', f'--before="{end_date}"', '--pretty=format:%h|%an|%ae|%ar|%s'],
                capture_output=True, text=True, timeout=30
            )
        else:
            # Pegar commits entre o commit inicial e a data
            result = subprocess.run(
                ['git', 'log', f'{start_commit}..HEAD', f'--before="{end_date}"', '--pretty=format:%h|%an|%ae|%ar|%s'],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode != 0 or not result.stdout.strip():
                # Se não houver commits após o inicial, incluir o próprio commit inicial
                result = subprocess.run(
                    ['git', 'log', '-1', start_commit, '--pretty=format:%h|%an|%ae|%ar|%s'],
                    capture_output=True, text=True, timeout=10
                )
        
        # Voltar para o diretório original
        os.chdir(original_cwd)

        if result.returncode == 0 and result.stdout.strip():
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    parts = line.split('|')
                    if len(parts) >= 5:
                        commits.append({
                            'hash': parts[0],
                            'author': parts[1],
                            'email': parts[2],
                            'date': parts[3],
                            'message': '|'.join(parts[4:])
                        })
            return commits
        return []
    except Exception as e:
        print(f"Erro ao extrair commits: {e}")
        return []

if __name__ == '__main__':
    # Caminhos baseados no config.py
    repos_path = config.REPOS_PATH
    input_json = os.path.join(config.DATA_PATH, "avaliacoes_com_feedback.json")
    output_json = os.path.join(config.DATA_PATH, "avaliacoes_com_commits.json")
    
    # Carregar dados existentes
    if not os.path.exists(input_json):
        print(f"❌ Arquivo de entrada não encontrado: {input_json}")
        sys.exit(1)

    with open(input_json, "r", encoding="utf-8") as f:
        alunos = json.load(f)
    
    print(f"Extraindo commits para {len(alunos)} alunos...")
    
    for i, aluno in enumerate(alunos):
        nome = aluno['nome']
        repo_dir = f"{repos_path}/{nome.replace('/', '_').replace(' ', '_')}"
        
        print(f"[{i+1}/{len(alunos)}] {nome}")
        
        if os.path.exists(repo_dir) and os.path.isdir(os.path.join(repo_dir, '.git')):
            commits = get_all_commits_between(repo_dir, config.COMMIT_INICIAL, config.DATA_LIMITE)
            aluno['commits_detalhados'] = commits
            aluno['total_commits'] = len(commits)
            print(f"  → {len(commits)} commits encontrados")
        else:
            aluno['commits_detalhados'] = []
            aluno['total_commits'] = 0
            print(f"  → Repositório não encontrado")
    
    # Salvar com commits atualizados
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(alunos, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Commits extraídos e salvos em: {output_json}")
