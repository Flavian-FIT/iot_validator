#!/usr/bin/env python3
"""
FASE 6: Consolidar resultados em CSV final
FASE 7: Gerar relatórios individuais em markdown
"""
import os
import re
import json
import csv
from pathlib import Path

def gerar_relatorio_individual(avaliacao, dados_documentacao, dados_repositorio):
    """Gera relatório individual em markdown para um aluno"""
    nome = avaliacao.get('nome', 'Desconhecido')
    
    relatorio = f"""# Relatório de Avaliação - Processo Seletivo IoT

## 👤 Identificação do Aluno
- **Nome:** {nome}
- **Repositório:** {dados_repositorio.get('github_url', 'N/A')}
- **Status:** {dados_repositorio.get('status', 'desconhecido')}

---

## 📊 Resumo da Avaliação

### Nota Final: **{avaliacao.get('nota_final', 0):.1f}/100**

### Pontuação por Critério:

| Critério | Pontuação | Máximo |
|----------|-----------|--------|
"""
    
    # Adicionar critérios
    criterios = avaliacao.get('criterios', {})
    
    criterios_map = {
        'logica_firmware': ('Lógica do Firmware e Código', 30),
        'metrica_wokwi': ('Métrica e Evidência (Wokwi)', 20),
        'ci_cd': ('CI/CD e GitHub Actions', 25),
        'documentacao': ('Documentação Técnica', 10),
        'estrutura': ('Estrutura do Repositório', 10)
    }
    
    total = 0
    for key, (nome_criterio, maximo) in criterios_map.items():
        dados = criterios.get(key, {})
        pontos = dados.get('score', 0)
        total += pontos
        relatorio += f"| {nome_criterio} | **{pontos}** | {maximo} |\n"
    
    resumo = ''
    if dados_documentacao and dados_documentacao.get('resumo'):
        resumo = dados_documentacao.get('resumo', '')[:300]
    elif dados_documentacao:
        resumo = 'Resumo não disponível'
    else:
        resumo = 'N/A'
    
    relatorio += f"""
---

## 📝 Análise Técnica

### Estrutura do Projeto
- **main.py:** {'✅ Presente' if dados_repositorio.get('main_py_exists') else '❌ Ausente'}
- **diagram.json:** {'✅ Presente' if dados_repositorio.get('diagram_json_exists') else '❌ Ausente'}
- **wokwi.toml:** {'✅ Presente' if dados_repositorio.get('wokwi_toml_exists') else '❌ Ausente'}
- **GitHub Actions:** {'✅ Configurado' if dados_repositorio.get('github_actions_exists') else '❌ Não configurado'}

### Commits
"""
    
    commits = dados_repositorio.get('commits', [])
    if commits:
        for commit in commits[:5]:
            relatorio += f"- {commit}\n"
    else:
        relatorio += "- Sem histórico de commits\n"
    
    relatorio += f"""
---

## 📋 Resumo do Projeto

{resumo if resumo else 'Resumo não disponível'}

---

## 🔍 Feedback Detalhado por Critério

"""
    
    for key, dados in criterios.items():
        feedback = dados.get('feedback', 'Sem feedback')
        score = dados.get('score', 0)
        relatorio += f"### {key.replace('_', ' ').title()}\n"
        relatorio += f"- **Pontuação:** {score}\n"
        relatorio += f"- **Feedback:** {feedback}\n\n"
    
    relatorio += """
---

## ✅ Conclusão

"""
    
    nota = avaliacao.get('nota_final', 0)
    if nota >= 80:
        relatorio += "**Aprovado** - Projeto atende aos requisitos com excelência."
    elif nota >= 60:
        relatorio += "**Aprovado** - Projeto atende aos requisitos mínimos."
    elif nota >= 40:
        relatorio += "**Em análise** - Projeto precisa de melhorias."
    else:
        relatorio += "**Não aprovado** - Projeto não atende aos requisitos mínimos."
    
    relatorio += f"""

---

*Relatório gerado automaticamente em {Path(__file__).parent}*
"""
    
    return relatorio

if __name__ == '__main__':
    resultado_path = "/workspace/resultado_validacao"
    
    # Carregar dados
    with open(f"{resultado_path}/avaliacoes.json", "r", encoding="utf-8") as f:
        avaliacoes = json.load(f)
    
    with open(f"{resultado_path}/documentacao_processada.json", "r", encoding="utf-8") as f:
        docs_processados = json.load(f)
    
    with open(f"{resultado_path}/repositorios_processados.json", "r", encoding="utf-8") as f:
        repos_processados = json.load(f)
    
    # Criar mapas
    docs_map = {d['nome']: d for d in docs_processados}
    repos_map = {r['nome']: r for r in repos_processados}
    
    print(f"=== FASE 6: Gerando CSV ===")
    
    # Gerar CSV
    csv_path = f"{resultado_path}/resultado_final.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Nome", "Email", "Link do Repositório", "Resumo do Projeto", "Pontuação Detalhada", "Nota Final"])
        
        for avaliacao in avaliacoes:
            nome = avaliacao.get('nome', '')
            repo = repos_map.get(nome, {})
            doc = docs_map.get(nome, {})
            
            # Extrair email (se disponível)
            email = doc.get('metadados', {}).get('email', '') if doc.get('metadados') else ''
            if not email:
                email = f"{nome.replace(' ', '.').lower()}@aluno.com"
            
            # Link do repositório
            repo_link = repo.get('github_url', '') or avaliacao.get('github_url', '')
            
            # Resumo
            resumo = ''
            if doc and doc.get('resumo'):
                resumo = doc.get('resumo', '')[:200]
            if not resumo:
                resumo = avaliacao.get('criterios', {}).get('documentacao', {}).get('feedback', '')[:200]
            
            # Pontuação detalhada
            criterios = avaliacao.get('criterios', {})
            pontuacoes = []
            for key, dados in criterios.items():
                pontuacoes.append(f"{key}: {dados.get('score', 0)} pts")
            pontuacao_detalhada = " | ".join(pontuacoes)
            
            # Nota final
            nota_final = avaliacao.get('nota_final', 0)
            
            writer.writerow([nome, email, repo_link, resumo, pontuacao_detalhada, nota_final])
    
    print(f"CSV salvo em: {csv_path}")
    
    print(f"\n=== FASE 7: Gerando Relatórios Individuais ===")
    
    # Gerar relatórios individuais
    relatorios_path = f"{resultado_path}/relatorios"
    os.makedirs(relatorios_path, exist_ok=True)
    
    for i, avaliacao in enumerate(avaliacoes):
        nome = avaliacao.get('nome', f'aluno_{i}')
        repo = repos_map.get(nome, {})
        doc = docs_map.get(nome, {})
        
        relatorio = gerar_relatorio_individual(avaliacao, doc, repo)
        
        # Salvar relatório
        nome_arquivo = nome.replace('/', '_').replace(' ', '_').replace('.', '_')
        relatorio_path = f"{relatorios_path}/{nome_arquivo}_relatorio.md"
        
        with open(relatorio_path, 'w', encoding='utf-8') as f:
            f.write(relatorio)
        
        if (i + 1) % 10 == 0:
            print(f"[{i+1}/{len(avaliacoes)}] Relatórios gerados...")
    
    print(f"\n=== Resumo Final ===")
    print(f"Total de alunos processados: {len(avaliacoes)}")
    print(f"CSV final: {csv_path}")
    print(f"Relatórios: {relatorios_path}/")
    
    # Mostrar algumas notas
    print("\nTop 5 alunos:")
    avaliacoes_ordenadas = sorted(avaliacoes, key=lambda x: x.get('nota_final', 0), reverse=True)
    for a in avaliacoes_ordenadas[:5]:
        print(f"  {a['nota_final']:.1f} - {a['nome']}")
    
    print("\nÚltimos 5 alunos:")
    for a in avaliacoes_ordenadas[-5:]:
        print(f"  {a['nota_final']:.1f} - {a['nome']}")
