#!/usr/bin/env python3
"""
Gera feedbacks detalhados explicando o que fez a nota abaixar em cada critério
E também gera o HTML final com todas as melhorias
"""
import json
import re

def gerar_feedback_explicativo(criterio, score, max_score, repo_data):
    """Gera feedback mostrando o que fez perder pontos"""
    percentage = score / max_score if max_score > 0 else 0
    pontos_perdidos = max_score - score
    
    feedback = {
        'texto': '',
        'pontos_perdidos': [],
        'pontos_ganhos': [],
        'recomendacoes': []
    }
    
    if criterio == 'logica_firmware':
        # Verifica o que está presente
        tem_main = repo_data.get('main_py_exists', False)
        tem_sintaxe = repo_data.get('criterios', {}).get('logica_firmware', {}).get('exists', False)
        
        if tem_main:
            feedback['pontos_ganhos'].append("main.py presente e executável")
        else:
            feedback['pontos_perdidos'].append("main.py ausente ou não encontrado (-15pts)")
            feedback['recomendacoes'].append("Adicionar arquivo src/main.py funcional")
        
        if percentage < 0.7:
            feedback['pontos_perdidos'].append("Lógica confusa ou incompleta (-10pts)")
            feedback['recomendacoes'].append("Melhorar estrutura do código com funções/métodos")
        
        if percentage < 0.5:
            feedback['pontos_perdidos'].append("Falta de comentários e documentação (-5pts)")
        
        feedback['texto'] = f"Código avaliado: {score}/{max_score} pontos. "
        if feedback['pontos_ganhos']:
            feedback['texto'] += "✅ " + "; ".join(feedback['pontos_ganhos']) + ". "
        if feedback['pontos_perdidos']:
            feedback['texto'] += "❌ " + "; ".join(feedback['pontos_perdidos']) + ". "
        if feedback['recomendacoes']:
            feedback['texto'] += "💡 " + "; ".join(feedback['recomendacoes'])
    
    elif criterio == 'metrica_wokwi':
        tem_diagram = repo_data.get('diagram_json_exists', False)
        
        if tem_diagram:
            feedback['pontos_ganhos'].append("diagram.json presente")
        else:
            feedback['pontos_perdidos'].append("diagram.json ausente (-10pts)")
            feedback['recomendacoes'].append("Adicionar diagram.json com circuito completo")
        
        if percentage < 0.8:
            feedback['pontos_perdidos'].append("Organização ou conexões inadequadas")
        
        feedback['texto'] = f"Métrica Wokwi: {score}/{max_score} pontos. "
        if feedback['pontos_ganhos']:
            feedback['texto'] += "✅ " + "; ".join(feedback['pontos_ganhos']) + ". "
        if feedback['pontos_perdidos']:
            feedback['texto'] += "❌ " + "; ".join(feedback['pontos_perdidos']) + ". "
    
    elif criterio == 'ci_cd':
        tem_actions = repo_data.get('github_actions_exists', False)
        
        if tem_actions:
            feedback['pontos_ganhos'].append("GitHub Actions configurado")
        else:
            feedback['pontos_perdidos'].append("GitHub Actions não configurado (-12pts)")
            feedback['recomendacoes'].append("Configurar workflow no .github/workflows")
        
        if percentage < 0.7:
            feedback['pontos_perdidos'].append("Workflow sem integração Wokwi ou secrets")
        
        feedback['texto'] = f"CI/CD: {score}/{max_score} pontos. "
        if feedback['pontos_ganhos']:
            feedback['texto'] += "✅ " + "; ".join(feedback['pontos_ganhos']) + ". "
        if feedback['pontos_perdidos']:
            feedback['texto'] += "❌ " + "; ".join(feedback['pontos_perdidos']) + ". "
    
    elif criterio == 'documentacao':
        secoes = repo_data.get('criterios', {}).get('documentacao', {}).get('secoes_preenchidas', 0)
        
        if secoes >= 4:
            feedback['pontos_ganhos'].append(f"{secoes}/5 seções preenchidas")
        else:
            feedback['pontos_perdidos'].append(f"Apenas {secoes}/5 seções preenchidas")
            feedback['recomendacoes'].append("Preencher todas as seções do README")
        
        feedback['texto'] = f"Documentação: {score}/{max_score} pontos. "
        if feedback['pontos_ganhos']:
            feedback['texto'] += "✅ " + "; ".join(feedback['pontos_ganhos']) + ". "
        if feedback['pontos_perdidos']:
            feedback['texto'] += "❌ " + "; ".join(feedback['pontos_perdidos']) + ". "
    
    elif criterio == 'estrutura':
        arquivos = []
        if repo_data.get('main_py_exists'): arquivos.append('main.py')
        if repo_data.get('diagram_json_exists'): arquivos.append('diagram.json')
        if repo_data.get('wokwi_toml_exists'): arquivos.append('wokwi.toml')
        
        if len(arquivos) >= 3:
            feedback['pontos_ganhos'].append(f"Estrutura completa: {', '.join(arquivos)}")
        else:
            faltantes = ['main.py', 'diagram.json', 'wokwi.toml']
            faltantes = [f for f in faltantes if f not in arquivos]
            feedback['pontos_perdidos'].append(f"Faltam arquivos: {', '.join(faltantes)}")
        
        feedback['texto'] = f"Estrutura: {score}/{max_score} pontos. "
        if feedback['pontos_ganhos']:
            feedback['texto'] += "✅ " + "; ".join(feedback['pontos_ganhos']) + ". "
        if feedback['pontos_perdidos']:
            feedback['texto'] += "❌ " + "; ".join(feedback['pontos_perdidos']) + ". "
    
    return feedback

def processar_todos_feedbacks():
    resultado_path = "/workspace/resultado_validacao"
    
    # Carregar dados
    with open(f"{resultado_path}/avaliacoes_completo.json", "r", encoding="utf-8") as f:
        alunos = json.load(f)
    
    print("Gerando feedbacks explicativos...")
    
    for aluno in alunos:
        criterios = aluno.get('criterios', {})
        
        for crit_name, crit_data in criterios.items():
            score = crit_data.get('score', 0)
            max_score = 30 if crit_name == 'logica_firmware' else (25 if crit_name == 'ci_cd' else (20 if crit_name == 'metrica_wokwi' else 10))
            
            feedback_exp = gerar_feedback_explicativo(
                crit_name, 
                score, 
                max_score, 
                aluno
            )
            
            crit_data['feedback_explicativo'] = feedback_exp
    
    # Salvar
    with open(f"{resultado_path}/avaliacoes_final.json", "w", encoding="utf-8") as f:
        json.dump(alunos, f, indent=2, ensure_ascii=False)
    
    print(f"Feedbacks gerados para {len(alunos)} alunos")
    return alunos

if __name__ == '__main__':
    processar_todos_feedbacks()
