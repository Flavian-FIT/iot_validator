#!/usr/bin/env python3
"""
Gera JSON consolidado para o dashboard HTML
"""
import json
import os

resultado_path = "/workspace/resultado_validacao"

# Carregar dados
with open(f"{resultado_path}/avaliacoes.json", "r", encoding="utf-8") as f:
    avaliacoes = json.load(f)

with open(f"{resultado_path}/documentacao_processada.json", "r", encoding="utf-8") as f:
    docs = json.load(f)

with open(f"{resultado_path}/repositorios_processados.json", "r", encoding="utf-8") as f:
    repos = json.load(f)

with open(f"{resultado_path}/links_mapeados.json", "r", encoding="utf-8") as f:
    links = json.load(f)

# Criar mapas
docs_map = {d['nome']: d for d in docs}
repos_map = {r['nome']: r for r in repos}
links_map = links

# Consolidar dados
dados_consolidados = []
for avaliacao in avaliacoes:
    nome = avaliacao['nome']
    doc = docs_map.get(nome, {})
    repo = repos_map.get(nome, {})
    link_data = links_map.get(nome, {})
    
    # Extrair email do metadados
    email = doc.get('metadados', {}).get('email', '') if doc.get('metadados') else ''
    if not email:
        email = f"{nome.replace(' ', '.').lower()}@aluno.com"
    
    consolidado = {
        'nome': nome,
        'email': email,
        'github_url': repo.get('github_url') or link_data.get('github_url', ''),
        'status': repo.get('status', 'desconhecido'),
        'nota_final': avaliacao.get('nota_final', 0),
        'criterios': avaliacao.get('criterios', {}),
        'commits': repo.get('commits', []),
        'resumo': doc.get('resumo', '') if doc else '',
        'readme_content': repo.get('readme_content', '') if repo else '',
        'main_py_exists': repo.get('main_py_exists', False),
        'diagram_json_exists': repo.get('diagram_json_exists', False),
        'wokwi_toml_exists': repo.get('wokwi_toml_exists', False),
        'github_actions_exists': repo.get('github_actions_exists', False)
    }
    
    dados_consolidados.append(consolidado)

# Salvar JSON consolidado
with open(f"{resultado_path}/avaliacoes_completas.json", "w", encoding="utf-8") as f:
    json.dump(dados_consolidados, f, indent=2, ensure_ascii=False)

print(f"JSON consolidado gerado: {len(dados_consolidados)} alunos")
print(f"Arquivo: {resultado_path}/avaliacoes_completas.json")
