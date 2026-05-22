#!/usr/bin/env python3
"""
Script completo para melhorias do dashboard
Reorganizado - Usa config.py
"""
import os
import subprocess
import json
import re
import sys
from pathlib import Path

# Adicionar pasta pai ao path para importar config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def get_all_commits(repo_path):
    """Extrai todos os commits até a data limite"""
    original_cwd = os.getcwd()
    try:
        os.chdir(repo_path)
        result = subprocess.run(
            ['git', 'log', f'--before="{config.DATA_LIMITE}"', '--pretty=format:%h|%an|%ae|%ar|%s|%b'],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0 and result.stdout.strip():
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    parts = line.split('|')
                    commits.append({
                        'hash': parts[0] if len(parts) >= 1 else '',
                        'author': parts[1] if len(parts) >= 2 else '',
                        'email': parts[2] if len(parts) >= 3 else '',
                        'date': parts[3] if len(parts) >= 4 else '',
                        'message': parts[4] if len(parts) >= 5 else '',
                        'body': parts[5] if len(parts) >= 6 else ''
                    })
            return commits
        return []
    except Exception as e:
        return []
    finally:
        os.chdir(original_cwd)

def analisar_artefatos(repo_path, readme_content, main_py_content):
    """
    Analisa artefatos do projeto para detectar problemas
    """
    artefatos = {
        'tem_readme': False,
        'tem_main_py': False,
        'tem_diagram_json': False,
        'tem_wokwi_toml': False,
        'tem_github_actions': False,
        'tem_imagens': [],
        'readme_preenchido': False,
        'main_py_funcional': False,
        'problemas_detectados': []
    }
    
    # Verificar README
    readme_path = os.path.join(repo_path, 'README.md')
    if os.path.exists(readme_path):
        artefatos['tem_readme'] = True
        if readme_content and len(readme_content) > 500:
            # Verificar seções preenchidas
            secoes_preenchidas = 0
            if '## 1️⃣' in readme_content or 'Visão Geral' in readme_content:
                secoes_preenchidas += 1
            if '## 2️⃣' in readme_content or 'Arquitetura' in readme_content:
                secoes_preenchidas += 1
            if '## 3️⃣' in readme_content or 'Componentes' in readme_content:
                secoes_preenchidas += 1
            if '## 4️⃣' in readme_content or 'Decisões' in readme_content:
                secoes_preenchidas += 1
            if '## 5️⃣' in readme_content or 'Resultados' in readme_content:
                secoes_preenchidas += 1
            
            if secoes_preenchidas >= 4:
                artefatos['readme_preenchido'] = True
            elif secoes_preenchidas < 2:
                artefatos['problemas_detectados'].append('README com poucas seções preenchidas')
    
    # Verificar main.py
    main_path = os.path.join(repo_path, 'src', 'main.py')
    if os.path.exists(main_path):
        artefatos['tem_main_py'] = True
        if main_py_content and len(main_py_content) > 100:
            if 'import' in main_py_content and ('wokwi' in main_py_content.lower() or 'gpio' in main_py_content.lower() or 'def ' in main_py_content):
                artefatos['main_py_funcional'] = True
            else:
                artefatos['problemas_detectados'].append('main.py presente mas parece incompleto')
    
    # Verificar diagram.json
    if os.path.exists(os.path.join(repo_path, 'diagram.json')):
        artefatos['tem_diagram_json'] = True
    
    # Verificar wokwi.toml
    if os.path.exists(os.path.join(repo_path, 'wokwi.toml')):
        artefatos['tem_wokwi_toml'] = True
    
    # Verificar GitHub Actions
    actions_path = os.path.join(repo_path, '.github', 'workflows')
    if os.path.exists(actions_path) and os.path.isdir(actions_path):
        artefatos['tem_github_actions'] = True
    
    # Procurar imagens no README
    if readme_content:
        imagens = re.findall(r'!\[.*?\]\((.*?)\)', readme_content)
        artefatos['tem_imagens'] = imagens[:5]  # Limitar a 5 imagens
    
    return artefatos

def gerar_feedback_completo(criterio, score, max_score, artefatos, commits):
    """
    Gera feedback completo explicando o que fez a nota abaixar
    """
    percentage = score / max_score if max_score > 0 else 0
    pontos_perdidos = max_score - score
    
    # Feedback centralizado no config ou local fallback
    feedbacks = config.FEEDBACKS
    
    base_feedback = feedbacks[criterio]['high' if percentage >= 0.8 else ('medium' if percentage >= 0.5 else 'low')]
    
    # Adicionar o que fez perder pontos
    detalhes_perda = ""
    if pontos_perdidos > 0:
        if criterio == 'logica_firmware':
            if not artefatos.get('main_py_funcional'):
                detalhes_perda = "Pontos perdidos: main.py ausente ou não funcional. "
            elif percentage < 0.8:
                detalhes_perda = "Pontos perdidos: falta de comentários ou modularização. "
        elif criterio == 'metrica_wokwi':
            if not artefatos.get('tem_diagram_json'):
                detalhes_perda = "Pontos perdidos: diagram.json ausente. "
            elif percentage < 0.8:
                detalhes_perda = "Pontos perdidos: organização do diagrama pode melhorar. "
        elif criterio == 'ci_cd':
            if not artefatos.get('tem_github_actions'):
                detalhes_perda = "Pontos perdidos: GitHub Actions não configurado. "
            elif percentage < 0.8:
                detalhes_perda = "Pontos perdidos: workflow pode ser melhorado. "
        elif criterio == 'documentacao':
            if not artefatos.get('readme_preenchido'):
                detalhes_perda = "Pontos perdidos: README com seções incompletas. "
            elif percentage < 0.8:
                detalhes_perda = "Pontos perdidos: documentação poderia ser mais detalhada. "
        elif criterio == 'estrutura':
            missing = []
            if not artefatos.get('tem_main_py'): missing.append('main.py')
            if not artefatos.get('tem_diagram_json'): missing.append('diagram.json')
            if not artefatos.get('tem_wokwi_toml'): missing.append('wokwi.toml')
            if missing:
                detalhes_perda = f"Pontos perdidos: arquivos ausentes ({', '.join(missing)}). "
    
    return f"{base_feedback} {detalhes_perda}".strip()

if __name__ == '__main__':
    data_path = config.DATA_PATH
    repos_path = config.REPOS_PATH
    
    input_file = os.path.join(data_path, "avaliacoes_com_feedback.json")
    output_file = config.SAIDAS['json_completo']
    
    # Carregar dados
    if not os.path.exists(input_file):
        print(f"❌ Erro: Arquivo {input_file} não encontrado.")
        sys.exit(1)

    with open(input_file, "r", encoding="utf-8") as f:
        alunos = json.load(f)
    
    print("Aplicando melhorias completas...")
    
    for i, aluno in enumerate(alunos):
        nome = aluno['nome']
        repo_dir = f"{repos_path}/{nome.replace('/', '_').replace(' ', '_')}"
        
        print(f"[{i+1}/{len(alunos)}] {nome}")
        
        # 1. Extrair commits detalhados
        if os.path.exists(repo_dir) and os.path.isdir(os.path.join(repo_dir, '.git')):
            commits = get_all_commits(repo_dir)
            aluno['commits_detalhados'] = commits
            aluno['total_commits'] = len(commits)
            
            # Extrair email do GitHub se disponível
            github_email = commits[0]['email'] if commits else None
            if github_email and '@' in github_email:
                aluno['github_email'] = github_email
        else:
            aluno['commits_detalhados'] = []
            aluno['total_commits'] = 0
            aluno['github_email'] = None
        
        # 2. Analisar artefatos
        readme_content = aluno.get('readme_content', '')
        main_py_content = ""
        main_path = os.path.join(repo_dir, 'src', 'main.py')
        if os.path.exists(main_path):
            with open(main_path, 'r', encoding='utf-8', errors='ignore') as f:
                main_py_content = f.read()
        
        artefatos = analisar_artefatos(repo_dir, readme_content, main_py_content)
        aluno['artefatos'] = artefatos
        
        # 3. Gerar feedback completo com explicação de perda de pontos
        for criterio, metadata in config.CRITERIOS.items():
            max_score = metadata['peso']
            if 'criterios' in aluno and criterio in aluno['criterios']:
                score = aluno['criterios'][criterio].get('score', 0)
                feedback_completo = gerar_feedback_completo(
                    criterio, score, max_score, artefatos, commits
                )
                aluno['criterios'][criterio]['feedback_completo'] = feedback_completo
        
        # 4. Adicionar email do GitHub se disponível
        if not aluno.get('email') or '@aluno.com' in aluno.get('email', ''):
            if aluno.get('github_email'):
                aluno['email'] = aluno['github_email']
    
    # 5. Ordenar por nome e nota
    alunos.sort(key=lambda x: (-x['nota_final'], x['nome']))
    
    # Adicionar ranking
    for i, aluno in enumerate(alunos):
        aluno['ranking'] = i + 1
    
    # Salvar com melhorias
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(alunos, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Melhorias aplicadas em {len(alunos)} alunos")
    print(f"Arquivo: {output_file}")
