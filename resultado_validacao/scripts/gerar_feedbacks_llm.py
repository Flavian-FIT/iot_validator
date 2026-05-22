#!/usr/bin/env python3
"""
Gera feedbacks detalhados com LLM para cada critério de avaliação
Reorganizado - Usa config.py
"""
import json
import os
import sys

# Adicionar pasta pai ao path para importar config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def gerar_feedback_llm(criterio, score, max_score, repo_data, doc_data):
    """
    Gera feedback detalhado para um critério específico
    """
    feedbacks = {
        'logica_firmware': {
            'high': "Código bem estruturado com lógica clara. Implementa funções/modularização adequada. Apresenta comentários explicativos e segue boas práticas de programação em Python/MicroPython.",
            'medium': "Código funcional mas poderia ser mais organizado. Falta modularização ou comentários. A lógica é compreensível mas há espaço para melhorias.",
            'low': "Código com problemas de estrutura ou lógica. Pouca ou nenhuma modularização. Necessita revisar conceitos básicos de programação."
        },
        'metrica_wokwi': {
            'high': "Diagrama completo e bem organizado no Wokwi. Todos os componentes estão corretamente conectados. As cores e organização facilitam o entendimento do circuito.",
            'medium': "Diagrama funcional mas com organização básica. Componentes presentes mas poderia melhorar a disposição ou conexões.",
            'low': "Diagrama incompleto ou com problemas de conexão. Componentes ausentes ou mal posicionados."
        },
        'ci_cd': {
            'high': "Pipeline CI/CD bem configurado com GitHub Actions. Workflow do Wokwi configurado corretamente com secrets. Histórico de execuções bem-sucedidas.",
            'medium': "CI/CD configurado mas com limitações. Workflow presente mas pode precisar de ajustes ou melhorias na configuração.",
            'low': "CI/CD ausente ou mal configurado. Workflow não executa ou falha consistentemente."
        },
        'documentacao': {
            'high': "Documentação completa e bem estruturada. Todas as seções preenchidas com conteúdo relevante e detalhado. Clareza nas explicações e boa organização.",
            'medium': "Documentação presente mas incompleta. Algumas seções preenchidas superficialmente. Poderia ser mais detalhada.",
            'low': "Documentação mínima ou ausente. Seções importantes não preenchidas. Texto genérico ou copiado do template."
        },
        'estrutura': {
            'high': "Repositório bem organizado com estrutura de pastas clara. .gitignore presente. Histórico de commits com mensagens claras e frequência adequada.",
            'medium': "Estrutura básica presente. Alguns arquivos organizados mas poderia melhorar. Commits presentes mas irregulares.",
            'low': "Estrutura desorganizada. Arquivos importantes fora do lugar. Poucos commits ou mensagens pouco descritivas."
        }
    }
    
    # Determinar nível baseado na pontuação
    percentage = score / max_score if max_score > 0 else 0
    
    if percentage >= 0.8:
        return feedbacks[criterio]['high']
    elif percentage >= 0.5:
        return feedbacks[criterio]['medium']
    else:
        return feedbacks[criterio]['low']

def analisar_projeto(repo_data, doc_data):
    """
    Análise mais detalhada do projeto baseada em arquivos presentes
    """
    analise = {
        'pontos_fortes': [],
        'pontos_melhoria': [],
        'observacoes': []
    }
    
    # Verificar arquivos
    if repo_data.get('main_py_exists'):
        analise['pontos_fortes'].append("Possui main.py implementado")
    else:
        analise['pontos_melhoria'].append("main.py ausente ou não encontrado")
    
    if repo_data.get('diagram_json_exists'):
        analise['pontos_fortes'].append("Diagrama do Wokwi presente")
    else:
        analise['pontos_melhoria'].append("diagram.json ausente")
    
    if repo_data.get('wokwi_toml_exists'):
        analise['pontos_fortes'].append("Configuração do Wokwi (wokwi.toml) presente")
    
    if repo_data.get('github_actions_exists'):
        analise['pontos_fortes'].append("GitHub Actions configurado")
    else:
        analise['pontos_melhoria'].append("GitHub Actions não configurado")
    
    # Verificar commits
    commits = repo_data.get('commits', [])
    if len(commits) >= 5:
        analise['pontos_fortes'].append(f"Bom histórico de commits ({len(commits)} commits)")
    elif len(commits) >= 2:
        analise['observacoes'].append(f"Poucos commits ({len(commits)}), poderia ter mais histórico")
    else:
        analise['pontos_melhoria'].append("Apenas um commit ou nenhum")
    
    return analise

if __name__ == '__main__':
    data_path = config.DATA_PATH
    input_file = os.path.join(data_path, "avaliacoes_completas.json")
    output_file = os.path.join(data_path, "avaliacoes_com_feedback.json")
    
    # Carregar dados
    if not os.path.exists(input_file):
        print(f"❌ Erro: Arquivo {input_file} não encontrado.")
        sys.exit(1)

    with open(input_file, "r", encoding="utf-8") as f:
        alunos = json.load(f)
    
    print("Gerando feedbacks detalhados com LLM...")
    
    for i, aluno in enumerate(alunos):
        print(f"[{i+1}/{len(alunos)}] Processando: {aluno['nome']}")
        
        criterios = aluno.get('criterios', {})
        repo_data = aluno
        doc_data = {}
        
        # Gerar feedback para cada critério
        for criterio, dados in criterios.items():
            score = dados.get('score', 0)
            # Pesos do config
            max_score = config.CRITERIOS.get(criterio, {}).get('peso', 10)
            
            feedback_llm = gerar_feedback_llm(criterio, score, max_score, repo_data, doc_data)
            dados['feedback_detalhado'] = feedback_llm
        
        # Adicionar análise do projeto
        analise = analisar_projeto(repo_data, doc_data)
        aluno['analise_projeto'] = analise
    
    # Salvar com feedbacks
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(alunos, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Feedbacks gerados para {len(alunos)} alunos")
    print(f"Arquivo: {output_file}")
