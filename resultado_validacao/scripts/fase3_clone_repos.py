#!/usr/bin/env python3
"""
FASE 3: Clonar repositórios e extrair dados (README, commits, imagens)
"""
import os
import re
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

def clean_url(url):
    """Remove .git e barra do final da URL"""
    if url:
        if url.endswith('.git'):
            url = url[:-4]
        url = url.rstrip('/')
    return url

def clone_and_extract(repo_data, target_date="2026-05-04 23:59:59"):
    """
    Clona repositório e extrai informações
    Returns: dict com README, commits, imagens, etc.
    """
    nome = repo_data['nome']
    github_url = clean_url(repo_data['github_url'])
    pasta_original = repo_data['pasta']
    
    resultado = {
        'nome': nome,
        'github_url': github_url,
        'pasta_original': pasta_original,
        'status': 'sucesso',
        'erro': None,
        'readme_content': None,
        'readme_exists': False,
        'commits': [],
        'commit_hash': None,
        'imagens': [],
        'estrutura': [],
        'main_py_exists': False,
        'diagram_json_exists': False,
        'wokwi_toml_exists': False,
        'github_actions_exists': False
    }
    
    # Usar caminho relativo ao script
    base_path = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.join(base_path, "repos", nome.replace('/', '_').replace(' ', '_'))
    
    try:
        # Remover se já existir
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)
        
        # Clonar repositório
        print(f"Clonando: {nome}")
        clone_cmd = ['git', 'clone', '--depth', '1', github_url, repo_dir]
        git_result = subprocess.run(clone_cmd, capture_output=True, text=True, timeout=30)
        
        if git_result.returncode != 0:
            # Tentar sem --depth 1
            clone_cmd = ['git', 'clone', github_url, repo_dir]
            git_result = subprocess.run(clone_cmd, capture_output=True, text=True, timeout=60)
            
        if git_result.returncode != 0:
            resultado['status'] = 'erro_clone'
            resultado['erro'] = git_result.stderr[:500]
            return resultado
        
        # Navegar até o repositório
        os.chdir(repo_dir)
        
        # Pegar histórico de commits (últimos 20)
        try:
            log_cmd = ['git', 'log', '--oneline', '-20']
            log_result = subprocess.run(log_cmd, capture_output=True, text=True, timeout=10)
            if log_result.returncode == 0:
                resultado['commits'] = log_result.stdout.strip().split('\n')
                # Pegar hash do commit mais recente
                if resultado['commits']:
                    resultado['commit_hash'] = resultado['commits'][0].split()[0]
        except Exception as e:
            resultado['commits'] = []
        
        # Ler README.md
        readme_path = os.path.join(repo_dir, 'README.md')
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                resultado['readme_content'] = f.read()
            resultado['readme_exists'] = True
        
        # Verificar arquivos obrigatórios
        resultado['main_py_exists'] = os.path.exists(os.path.join(repo_dir, 'src', 'main.py'))
        resultado['diagram_json_exists'] = os.path.exists(os.path.join(repo_dir, 'diagram.json'))
        resultado['wokwi_toml_exists'] = os.path.exists(os.path.join(repo_dir, 'wokwi.toml'))
        
        # Verificar GitHub Actions
        actions_path = os.path.join(repo_dir, '.github', 'workflows')
        resultado['github_actions_exists'] = os.path.exists(actions_path) and os.path.isdir(actions_path)
        
        # Listar estrutura do repositório
        for root, dirs, files in os.walk(repo_dir):
            level = root.replace(repo_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            for file in files:
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, repo_dir)
                resultado['estrutura'].append(rel_path)
            
            # Limitar para não ficar muito grande
            if len(resultado['estrutura']) > 50:
                break
        
        # Encontrar imagens
        for file in os.listdir(repo_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                resultado['imagens'].append(file)
        
    finally:
        # Voltar para o diretório do script
        os.chdir(base_path)
    
    return resultado

if __name__ == '__main__':
    # Usar caminho absoluto baseado na localização do script
    base_path = os.path.dirname(os.path.abspath(__file__))
    resultado_path = base_path
    
    # Carregar links mapeados
    with open(f"{resultado_path}/links_mapeados.json", "r", encoding="utf-8") as f:
        links_mapeados = json.load(f)
    
    print(f"Total de repositórios para processar: {len(links_mapeados)}")
    
    resultados = []
    for i, (nome, dados) in enumerate(links_mapeados.items()):
        print(f"\n[{i+1}/{len(links_mapeados)}] Processando: {nome}")
        
        if dados['github_url']:
            resultado = clone_and_extract(dados)
            resultados.append(resultado)
        else:
            resultados.append({
                'nome': nome,
                'github_url': None,
                'status': 'sem_link',
                'erro': 'Link do GitHub não encontrado'
            })
    
    # Salvar resultados
    with open(f"{resultado_path}/repositorios_processados.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    # Estatísticas
    sucesso = [r for r in resultados if r['status'] == 'sucesso']
    erros = [r for r in resultados if r['status'] != 'sucesso']
    
    print(f"\n=== Resumo FASE 3 ===")
    print(f"Sucesso: {len(sucesso)}")
    print(f"Erros: {len(erros)}")
    
    if erros:
        print("\nErros:")
        for e in erros[:5]:
            print(f"  - {e['nome']}: {e['status']} - {e.get('erro', 'N/A')}")
