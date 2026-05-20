#!/usr/bin/env python3
"""
Extrair commits entre e560365081a8497c2e5dafba60c1430a7f31cdb7 e May 4, 2026
"""
import os
import subprocess
import json
from pathlib import Path

COMMIT_INICIAL = "e560365081a8497c2e5dafba60c1430a7f31cdb7"
DATA_LIMITE = "2026-05-04 23:59:59"

def get_all_commits_between(repo_path, start_commit, end_date):
    """
    Extrai todos os commits entre um commit específico e uma data
    """
    try:
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
    finally:
        os.chdir('/workspace/resultado_validacao')

if __name__ == '__main__':
    repos_path = "/workspace/resultado_validacao/repos"
    resultado_path = "/workspace/resultado_validacao"
    
    # Carregar dados existentes
    with open(f"{resultado_path}/avaliacoes_com_feedback.json", "r", encoding="utf-8") as f:
        alunos = json.load(f)
    
    print(f"Extraindo commits para {len(alunos)} alunos...")
    
    for i, aluno in enumerate(alunos):
        nome = aluno['nome']
        repo_dir = f"{repos_path}/{nome.replace('/', '_').replace(' ', '_')}"
        
        print(f"[{i+1}/{len(alunos)}] {nome}")
        
        if os.path.exists(repo_dir) and os.path.isdir(os.path.join(repo_dir, '.git')):
            commits = get_all_commits_between(repo_dir, COMMIT_INICIAL, DATA_LIMITE)
            aluno['commits_detalhados'] = commits
            aluno['total_commits'] = len(commits)
            print(f"  → {len(commits)} commits encontrados")
        else:
            aluno['commits_detalhados'] = []
            aluno['total_commits'] = 0
            print(f"  → Repositório não encontrado")
    
    # Salvar com commits atualizados
    with open(f"{resultado_path}/avaliacoes_com_commits.json", "w", encoding="utf-8") as f:
        json.dump(alunos, f, indent=2, ensure_ascii=False)
    
    print(f"\nCommits extraídos e salvos em: avaliacoes_com_commits.json")
