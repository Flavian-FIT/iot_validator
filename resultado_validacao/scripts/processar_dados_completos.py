#!/usr/bin/env python3
"""
FASE 2: Processar dados completos
Reorganizado - Usa config.py para caminhos
"""
import os
import re
import json
import subprocess
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Adicionar pasta pai ao path para importar config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def get_all_commits(repo_dir, base_commit=None, target_date=config.DATA_LIMITE):
    """
    Obtém todos os commits entre um commit base e a data limite
    """
    original_cwd = os.getcwd()
    try:
        os.chdir(repo_dir)
        
        # Se tiver base_commit, pega todos os commits entre base e HEAD
        if base_commit:
            # Verifica se o base_commit existe no repositório
            check_cmd = ['git', 'rev-parse', f'{base_commit}^{{commit}}']
            result = subprocess.run(check_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Commit base existe, pega todos entre base e HEAD
                cmd = ['git', 'log', '--format=%H|%s|%ai', f'{base_commit}..HEAD']
            else:
                # Base commit não existe, pega todos até a data
                cmd = ['git', 'log', f'--before="{target_date}"', '--format=%H|%s|%ai']
        else:
            cmd = ['git', 'log', f'--before="{target_date}"', '--format=%H|%s|%ai']
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        commit_hash = parts[0]
                        message = parts[1]
                        date = parts[2]
                        commits.append({
                            'hash': commit_hash,
                            'message': message,
                            'date': date,
                            'full': f"{commit_hash[:7]} - {message}"
                        })
            return commits
        return []
    except Exception as e:
        print(f"Erro ao obter commits: {e}")
        return []
    finally:
        os.chdir(original_cwd)

def extract_email_from_readme(readme_content):
    """Extrai email do conteúdo do README"""
    if not readme_content:
        return None
    
    # Padrões comuns de email
    patterns = [
        r'[\w\.-]+@[\w\.-]+\.\w+',
        r'Email:\s*([\w\.-]+@[\w\.-]+\.\w+)',
        r'E-mail:\s*([\w\.-]+@[\w\.-]+\.\w+)',
        r'Contato:\s*([\w\.-]+@[\w\.-]+\.\w+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, readme_content, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None

def extract_images_from_readme(readme_content, repo_url):
    """Extrai URLs de imagens do README"""
    if not readme_content:
        return []
    
    images = []
    
    # Padrões para imagens
    patterns = [
        r'!\[.*?\]\((https?://[^\s\)]+)\)',
        r'!\[.*?\]\((https?://github\.com/[^\s\)]+)\)',
        r'<img.*?src="(https?://[^\"]+)"'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, readme_content)
        for match in matches:
            if match not in images:
                images.append(match)
    
    # Se for URL relativa do GitHub, converte para absoluta
    base_url = repo_url.rstrip('/') if repo_url else ''
    for i, img in enumerate(images):
        if img.startswith('/') and base_url:
            images[i] = f"{base_url}{img}"
    
    return images

def detectar_artefatos_ia(readme_content, commits, main_py_content):
    """
    Detecta possíveis "artefatos" de IA no projeto
    """
    artefatos = []
    
    if readme_content:
        # Verifica se o README é muito genérico
        if len(readme_content) < 500:
            artefatos.append({
                'tipo': 'README_curto',
                'descricao': 'README muito curto pode indicar conteúdo gerado',
                'severidade': 'baixa'
            })
        
        # Procura por frases muito genéricas
        genericas = ['este projeto foi desenvolvido', 'solução inovadora', 'tecnologia de ponta']
        for frase in genericas:
            if frase.lower() in readme_content.lower():
                artefatos.append({
                    'tipo': 'Texto_generico',
                    'descricao': f'Frase genérica detectada: "{frase}"',
                    'severidade': 'baixa'
                })
    
    if main_py_content:
        # Verifica comentários muito genéricos
        if '# Este código foi gerado' in main_py_content or '# Generated code' in main_py_content:
            artefatos.append({
                'tipo': 'Comentario_IA',
                'descricao': 'Comentário indica código gerado automaticamente',
                'severidade': 'media'
            })
        
        # Muitas variáveis genéricas
        if re.search(r'var\d+|temp\d+|data\d+', main_py_content):
            artefatos.append({
                'tipo': 'Variaveis_genericas',
                'descricao': 'Uso de variáveis com nomes genéricos',
                'severidade': 'baixa'
            })
    
    # Verifica commits
    if commits:
        if len(commits) == 1:
            artefatos.append({
                'tipo': 'Unico_commit',
                'descricao': 'Apenas um commit pode indicar envio único sem histórico',
                'severidade': 'media'
            })
    
    return artefatos

def processar_alunos():
    # Caminhos via config
    data_path = config.DATA_PATH
    repos_path = config.REPOS_PATH
    
    input_alunos = os.path.join(data_path, "avaliacoes_com_feedback.json")
    input_repos = os.path.join(data_path, "repositorios_processados.json")
    output_file = os.path.join(data_path, "avaliacoes_completo.json")
    
    # Carregar dados existentes
    if not os.path.exists(input_alunos):
        print(f"❌ Erro: Arquivo {input_alunos} não encontrado.")
        return
        
    if not os.path.exists(input_repos):
        print(f"❌ Erro: Arquivo {input_repos} não encontrado.")
        return

    with open(input_alunos, "r", encoding="utf-8") as f:
        alunos = json.load(f)
    
    with open(input_repos, "r", encoding="utf-8") as f:
        repos_data = json.load(f)
    
    print(f"Processando {len(alunos)} alunos...")
    
    for i, aluno in enumerate(alunos):
        print(f"[{i+1}/{len(alunos)}] Processando: {aluno['nome']}")
        
        nome = aluno['nome']
        repo_info = next((r for r in repos_data if r['nome'] == nome), None)
        
        if not repo_info or repo_info.get('status') != 'sucesso':
            continue
        
        repo_dir = os.path.join(repos_path, nome.replace('/', '_').replace(' ', '_'))
        
        if not os.path.exists(repo_dir):
            continue
        
        try:
            # 1. Obter commits
            commits = get_all_commits(repo_dir, base_commit=config.COMMIT_INICIAL)
            aluno['commits_detalhados'] = commits
            aluno['num_commits'] = len(commits)
            
            # 2. Extrair email do README
            readme_content = repo_info.get('readme_content', '')
            email_github = extract_email_from_readme(readme_content)
            if email_github:
                aluno['email_github'] = email_github
            
            # 3. Extrair imagens do README
            repo_url = repo_info.get('github_url', '')
            imagens = extract_images_from_readme(readme_content, repo_url)
            aluno['imagens'] = imagens
            
            # 4. Detectar artefatos de IA
            main_py_path = os.path.join(repo_dir, 'src', 'main.py')
            main_py_content = ''
            if os.path.exists(main_py_path):
                with open(main_py_path, 'r', encoding='utf-8', errors='ignore') as f:
                    main_py_content = f.read()
            
            artefatos = detectar_artefatos_ia(readme_content, commits, main_py_content)
            aluno['artefatos_ia'] = artefatos
            
            # 5. Adicionar análise de qualidade do README
            aluno['analise_readme'] = {
                'tamanho': len(readme_content) if readme_content else 0,
                'tem_secoes': bool(re.search(r'##', readme_content)),
                'tem_codigo': bool(re.search(r'```', readme_content)),
                'tem_imagens': len(imagens) > 0
            }
            
        except Exception as e:
            print(f"Erro ao processar {nome}: {e}")
            continue
    
    # Salvar dados atualizados
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(alunos, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Dados salvos em: {output_file}")
    print(f"Total de alunos processados: {len(alunos)}")
    
    # Estatísticas
    com_email = sum(1 for a in alunos if a.get('email_github'))
    com_imagens = sum(1 for a in alunos if a.get('imagens'))
    com_artefatos = sum(1 for a in alunos if a.get('artefatos_ia'))
    
    print(f"Alunos com email extraído: {com_email}")
    print(f"Alunos com imagens: {com_imagens}")
    print(f"Alunos com artefatos detectados: {com_artefatos}")

if __name__ == '__main__':
    processar_alunos()
