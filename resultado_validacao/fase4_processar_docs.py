#!/usr/bin/env python3
"""
FASE 4: Processar documentação e extrair metadados dos alunos
"""
import os
import re
import json
from pathlib import Path

def extrair_secao(readme_content, inicio_marker, fim_marker=None):
    """Extrai uma seção do README baseada em markers"""
    if not readme_content:
        return None
    
    padrao = re.compile(f"{re.escape(inicio_marker)}.*?(?={re.escape(fim_marker)}|$)", re.IGNORECASE | re.DOTALL)
    match = padrao.search(readme_content)
    if match:
        return match.group(0).strip()
    return None

def extrair_metadados(readme_content):
    """Extrai metadados do aluno do README"""
    metadados = {
        'nome_completo': None,
        'github': None,
        'email': None,
        'wokwi_link': None
    }
    
    if not readme_content:
        return metadados
    
    # Extrair Nome completo
    match = re.search(r'\*\*Nome completo:\*\*\s*(.+?)(?:\n|$)', readme_content, re.IGNORECASE)
    if match:
        metadados['nome_completo'] = match.group(1).strip()
    
    # Extrair GitHub
    match = re.search(r'\*\*GitHub:\*\*\s*(?:\[.*?\])?\((https://github\.com/[\w\-_]+)\)', readme_content, re.IGNORECASE)
    if match:
        metadados['github'] = match.group(1)
    else:
        match = re.search(r'\*\*GitHub:\*\*\s*(@[\w\-_]+|https://github\.com/[\w\-_]+)', readme_content, re.IGNORECASE)
        if match:
            metadados['github'] = match.group(1)
    
    # Extrair link Wokwi
    match = re.search(r'(?:Wokwi|wokwi).*?(https://wokwi\.com/share/[\w\-_]+|https://wokwi\.com/projects/[\w\-_]+)', readme_content, re.IGNORECASE)
    if match:
        metadados['wokwi_link'] = match.group(1)
    else:
        match = re.search(r'(https://wokwi\.com/share/[\w\-_]+|https://wokwi\.com/projects/[\w\-_]+)', readme_content)
        if match:
            metadados['wokwi_link'] = match.group(1)
    
    return metadados

def extrair_secoes_relatorio(readme_content):
    """Extrai as seções do relatório do aluno"""
    secoes = {
        'visao_geral': None,
        'arquitetura': None,
        'componentes': None,
        'decisoes_tecnicas': None,
        'resultados': None,
        'comentarios_adicionais': None
    }
    
    if not readme_content:
        return secoes
    
    # Visão Geral
    match = re.search(r'## 1️⃣ Visão Geral da Solução.*?(?=## 2️⃣|$)', readme_content, re.DOTALL | re.IGNORECASE)
    if match:
        secoes['visao_geral'] = match.group(0).strip()
    
    # Arquitetura
    match = re.search(r'## 2️⃣ Arquitetura do Sistema Embarcado.*?(?=## 3️⃣|$)', readme_content, re.DOTALL | re.IGNORECASE)
    if match:
        secoes['arquitetura'] = match.group(0).strip()
    
    # Componentes
    match = re.search(r'## 3️⃣ Componentes Utilizados.*?(?=## 4️⃣|$)', readme_content, re.DOTALL | re.IGNORECASE)
    if match:
        secoes['componentes'] = match.group(0).strip()
    
    # Decisões Técnicas
    match = re.search(r'## 4️⃣ Decisões Técnicas.*?(?=## 5️⃣|$)', readme_content, re.DOTALL | re.IGNORECASE)
    if match:
        secoes['decisoes_tecnicas'] = match.group(0).strip()
    
    # Resultados
    match = re.search(r'## 5️⃣ Resultados Obtidos.*?(?=## 6️⃣|$)', readme_content, re.DOTALL | re.IGNORECASE)
    if match:
        secoes['resultados'] = match.group(0).strip()
    
    # Comentários Adicionais
    match = re.search(r'## 6️⃣ Comentários Adicionais.*?(?=##|$|> ✅)', readme_content, re.DOTALL | re.IGNORECASE)
    if match:
        secoes['comentarios_adicionais'] = match.group(0).strip()
    
    return secoes

def processar_aluno(dados_repositorio):
    """Processa um único aluno"""
    nome = dados_repositorio['nome']
    repo_dir = f"/workspace/resultado_validacao/repos/{nome.replace('/', '_').replace(' ', '_')}"
    
    resultado = {
        'nome': nome,
        'status': 'sucesso',
        'erro': None,
        'metadados': None,
        'secoes': None,
        'readme_contenido': False,
        'resumo': None
    }
    
    try:
        # Ler README
        readme_path = os.path.join(repo_dir, 'README.md')
        if not os.path.exists(readme_path):
            resultado['status'] = 'sem_readme'
            return resultado
        
        with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
            readme_content = f.read()
        
        resultado['readme_contenido'] = True
        
        # Extrair metadados
        resultado['metadados'] = extrair_metadados(readme_content)
        
        # Extrair seções
        resultado['secoes'] = extrair_secoes_relatorio(readme_content)
        
        # Criar resumo
        resumo_parts = []
        if resultado['secoes'] and resultado['secoes'].get('visao_geral'):
            visao = resultado['secoes']['visao_geral'][:200]
            resumo_parts.append(visao)
        
        if resultado['secoes'] and resultado['secoes'].get('resultados'):
            resultados = resultado['secoes']['resultados'][:200]
            resumo_parts.append(resultados)
        
        resultado['resumo'] = '\n'.join(resumo_parts)[:400] if resumo_parts else None
        
    except Exception as e:
        resultado['status'] = 'erro'
        resultado['erro'] = str(e)[:500]
    
    return resultado

if __name__ == '__main__':
    resultado_path = "/workspace/resultado_validacao"
    
    # Carregar repositórios processados
    with open(f"{resultado_path}/repositorios_processados.json", "r", encoding="utf-8") as f:
        repos_processados = json.load(f)
    
    print(f"Total de repositórios para processar: {len(repos_processados)}")
    
    resultados = []
    for i, dados in enumerate(repos_processados):
        print(f"[{i+1}/{len(repos_processados)}] Processando: {dados['nome']}")
        
        if dados['status'] == 'sucesso':
            resultado = processar_aluno(dados)
            resultados.append(resultado)
        else:
            resultados.append({
                'nome': dados['nome'],
                'status': 'repo_erro',
                'erro_repo': dados.get('status'),
                'metadados': None,
                'secoes': None
            })
    
    # Salvar resultados
    with open(f"{resultado_path}/documentacao_processada.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    # Estatísticas
    com_readme = [r for r in resultados if r.get('readme_contenido')]
    sem_readme = [r for r in resultados if r.get('status') == 'sem_readme']
    
    print(f"\n=== Resumo FASE 4 ===")
    print(f"Com README: {len(com_readme)}")
    print(f"Sem README: {len(sem_readme)}")
    
    # Mostrar alguns exemplos
    print("\nExemplos de metadados extraídos:")
    for r in resultados[:3]:
        if r.get('metadados'):
            print(f"  {r['nome']}:")
            print(f"    Nome: {r['metadados'].get('nome_completo', 'N/A')}")
            print(f"    GitHub: {r['metadados'].get('github', 'N/A')}")
