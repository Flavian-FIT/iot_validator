#!/usr/bin/env python3
"""
FASE 5: Avaliar tecnicamente cada projeto usando rubrica

Critérios da rubrica:
1. Lógica do Firmware e Código (30 pts)
2. Métrica e Evidência de Resultado (20 pts)  
3. CI/CD e GitHub Actions (25 pts)
4. Documentação Técnica (README) (10 pts)
5. Estrutura do Repositório e Versionamento (10 pts)

Total: 95 pts → Normalizar para 0-100
"""
import os
import re
import json
from pathlib import Path

def verificar_main_py(repo_dir):
    """Verifica o arquivo main.py"""
    main_path = os.path.join(repo_dir, 'src', 'main.py')
    if not os.path.exists(main_path):
        return {'exists': False, 'score': 0, 'feedback': 'main.py não encontrado'}
    
    try:
        with open(main_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        tem_logica = False
        tem_comentarios = False
        
        if 'def ' in content or 'class ' in content or 'print(' in content:
            tem_logica = True
        
        if '#' in content:
            tem_comentarios = True
        
        if 'import' in content and ('wokwi' in content.lower() or 'gpio' in content.lower() or 'led' in content.lower()):
            tem_logica = True
        
        score = 0
        feedback_parts = []
        
        if content.strip():
            score += 15
            feedback_parts.append("Código presente")
        
        if tem_logica:
            score += 12
            feedback_parts.append("Lógica funcional")
        
        if tem_comentarios:
            score += 3
            feedback_parts.append("Com comentários")
        
        return {
            'exists': True,
            'score': min(score, 30),
            'feedback': '; '.join(feedback_parts),
            'content_length': len(content)
        }
    except Exception as e:
        return {'exists': False, 'score': 0, 'feedback': f'Erro: {str(e)}'}

def verificar_diagram_json(repo_dir):
    """Verifica o diagram.json do Wokwi"""
    diagram_path = os.path.join(repo_dir, 'diagram.json')
    if not os.path.exists(diagram_path):
        return {'exists': False, 'score': 0, 'feedback': 'diagram.json não encontrado'}
    
    try:
        with open(diagram_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        import json as json_lib
        try:
            data = json_lib.loads(content)
            tem_componentes = 'elements' in str(data) or 'connections' in str(data)
            tem_organizacao = len(content) > 500
        except:
            tem_componentes = False
            tem_organizacao = False
        
        score = 0
        feedback_parts = []
        
        if tem_componentes:
            score += 10
            feedback_parts.append("Componentes identificados")
        
        if tem_organizacao:
            score += 10
            feedback_parts.append("Diagrama organizado")
        
        return {
            'exists': True,
            'score': min(score, 20),
            'feedback': '; '.join(feedback_parts)
        }
    except Exception as e:
        return {'exists': False, 'score': 0, 'feedback': f'Erro: {str(e)}'}

def verificar_ci_cd(repo_dir):
    """Verifica GitHub Actions / CI/CD"""
    actions_path = os.path.join(repo_dir, '.github', 'workflows')
    
    if not os.path.exists(actions_path) or not os.path.isdir(actions_path):
        return {'exists': False, 'score': 0, 'feedback': 'GitHub Actions não configurado'}
    
    try:
        workflows = [f for f in os.listdir(actions_path) if f.endswith('.yml') or f.endswith('.yaml')]
        
        if not workflows:
            return {'exists': False, 'score': 0, 'feedback': 'Nenhum workflow encontrado'}
        
        tem_wokwi = False
        tem_api_key = False
        
        for wf in workflows:
            wf_path = os.path.join(actions_path, wf)
            with open(wf_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if 'wokwi' in content.lower():
                tem_wokwi = True
            if 'WOKWI_API_KEY' in content or 'api-key' in content.lower():
                tem_api_key = True
        
        score = 0
        feedback_parts = []
        
        if workflows:
            score += 12
            feedback_parts.append(f"{len(workflows)} workflow(s)")
        
        if tem_wokwi:
            score += 8
            feedback_parts.append("Integration Wokwi")
        
        if tem_api_key:
            score += 5
            feedback_parts.append("Usa secrets")
        
        return {
            'exists': True,
            'score': min(score, 25),
            'feedback': '; '.join(feedback_parts),
            'workflows': workflows
        }
    except Exception as e:
        return {'exists': False, 'score': 0, 'feedback': f'Erro: {str(e)}'}

def verificar_documentacao(readme_content, secoes):
    """Verifica qualidade da documentação"""
    if not readme_content:
        return {'score': 0, 'feedback': 'Sem README'}
    
    score = 0
    feedback_parts = []
    
    secoes_preenchidas = 0
    total_secoes = 5
    
    if secoes:
        if secoes.get('visao_geral') and len(secoes['visao_geral']) > 20:
            secoes_preenchidas += 1
        if secoes.get('arquitetura') and len(secoes['arquitetura']) > 20:
            secoes_preenchidas += 1
        if secoes.get('componentes') and len(secoes['componentes']) > 20:
            secoes_preenchidas += 1
        if secoes.get('decisoes_tecnicas') and len(secoes['decisoes_tecnicas']) > 20:
            secoes_preenchidas += 1
        if secoes.get('resultados') and len(secoes['resultados']) > 20:
            secoes_preenchidas += 1
    
    score = int((secoes_preenchidas / total_secoes) * 10)
    
    if secoes_preenchidas >= 4:
        feedback_parts.append(f"{secoes_preenchidas}/{total_secoes} seções preenchidas")
    elif secoes_preenchidas >= 2:
        feedback_parts.append(f"{secoes_preenchidas}/{total_secoes} seções (parcial)")
    else:
        feedback_parts.append(f"{secoes_preenchidas}/{total_secoes} seções (insuficiente)")
    
    return {
        'score': score,
        'feedback': '; '.join(feedback_parts),
        'secoes_preenchidas': secoes_preenchidas
    }

def verificar_estrutura(repo_dir):
    """Verifica estrutura do repositório"""
    score = 0
    feedback_parts = []
    
    # Verificar arquivos obrigatórios
    arquivos_esperados = ['README.md', 'src/main.py', 'diagram.json', 'wokwi.toml']
    arquivos_encontrados = []
    
    for arquivo in arquivos_esperados:
        if os.path.exists(os.path.join(repo_dir, arquivo)):
            arquivos_encontrados.append(arquivo)
    
    score += int((len(arquivos_encontrados) / len(arquivos_esperados)) * 6)
    feedback_parts.append(f"{len(arquivos_encontrados)}/{len(arquivos_esperados)} arquivos obrigatórios")
    
    # Verificar .gitignore
    if os.path.exists(os.path.join(repo_dir, '.gitignore')):
        score += 2
        feedback_parts.append("Possui .gitignore")
    
    # Verificar commits
    try:
        import subprocess
        result = subprocess.run(['git', 'log', '--oneline'], cwd=repo_dir, capture_output=True, text=True, timeout=5)
        commits = result.stdout.strip().split('\n') if result.returncode == 0 else []
        if len(commits) >= 3:
            score += 2
            feedback_parts.append(f"{len(commits)} commits")
    except:
        pass
    
    return {
        'score': min(score, 10),
        'feedback': '; '.join(feedback_parts)
    }

def avaliar_aluno(dados_repositorio, dados_documentacao):
    """Avalia um aluno completo"""
    nome = dados_repositorio['nome']
    repo_dir = f"/workspace/resultado_validacao/repos/{nome.replace('/', '_').replace(' ', '_')}"
    
    avaliacao = {
        'nome': nome,
        'criterios': {},
        'pontuacao_total': 0,
        'nota_final': 0,
        'feedback_geral': []
    }
    
    if dados_repositorio.get('status') != 'sucesso':
        avaliacao['erro'] = dados_repositorio.get('status', 'desconhecido')
        return avaliacao
    
    # 1. Lógica do Firmware (30 pts)
    avaliacao['criterios']['logica_firmware'] = verificar_main_py(repo_dir)
    
    # 2. Métrica/Wokwi (20 pts)
    avaliacao['criterios']['metrica_wokwi'] = verificar_diagram_json(repo_dir)
    
    # 3. CI/CD (25 pts)
    avaliacao['criterios']['ci_cd'] = verificar_ci_cd(repo_dir)
    
    # 4. Documentação (10 pts)
    readme_content = dados_repositorio.get('readme_content')
    secoes = dados_documentacao.get('secoes') if dados_documentacao else None
    avaliacao['criterios']['documentacao'] = verificar_documentacao(readme_content, secoes)
    
    # 5. Estrutura (10 pts)
    avaliacao['criterios']['estrutura'] = verificar_estrutura(repo_dir)
    
    # Calcular pontuação total
    total = 0
    max_pontos = 0
    for criterio, dados in avaliacao['criterios'].items():
        total += dados.get('score', 0)
        max_pontos += 25 if criterio == 'ci_cd' else (30 if criterio == 'logica_firmware' else (20 if criterio == 'metrica_wokwi' else 10))
    
    avaliacao['pontuacao_total'] = total
    avaliacao['nota_final'] = round((total / 95) * 100, 1) if total > 0 else 0
    
    return avaliacao

if __name__ == '__main__':
    resultado_path = "/workspace/resultado_validacao"
    
    # Carregar dados
    with open(f"{resultado_path}/repositorios_processados.json", "r", encoding="utf-8") as f:
        repos_processados = json.load(f)
    
    with open(f"{resultado_path}/documentacao_processada.json", "r", encoding="utf-8") as f:
        docs_processados = json.load(f)
    
    # Criar mapa de documentação
    docs_map = {d['nome']: d for d in docs_processados}
    
    print(f"Avaliando {len(repos_processados)} alunos...")
    
    avaliacoes = []
    for i, repo in enumerate(repos_processados):
        print(f"[{i+1}/{len(repos_processados)}] Avaliando: {repo['nome']}")
        
        doc = docs_map.get(repo['nome'], {})
        avaliacao = avaliar_aluno(repo, doc)
        avaliacoes.append(avaliacao)
    
    # Salvar resultados
    with open(f"{resultado_path}/avaliacoes.json", "w", encoding="utf-8") as f:
        json.dump(avaliacoes, f, indent=2, ensure_ascii=False)
    
    # Estatísticas
    notas = [a['nota_final'] for a in avaliacoes if 'erro' not in a]
    print(f"\n=== Resumo FASE 5 ===")
    print(f"Avaliações realizadas: {len(avaliacoes)}")
    if notas:
        print(f"Nota média: {sum(notas)/len(notas):.1f}")
        print(f"Maior nota: {max(notas):.1f}")
        print(f"Menor nota: {min(notas):.1f}")
