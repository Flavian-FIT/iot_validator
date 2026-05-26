"""
Configurações do Pipeline de Validação IoT
Centralização de caminhos e critérios de avaliação
"""
import os

# Caminho Base
RESULTADO_PATH = os.path.dirname(os.path.abspath(__file__))

# Subpastas para Organização
SCRIPTS_PATH = os.path.join(RESULTADO_PATH, "scripts")
DATA_PATH = os.path.join(RESULTADO_PATH, "data")
REPORTS_PATH = os.path.join(RESULTADO_PATH, "reports")

# Caminhos de Dados
REPOS_PATH = os.path.join(DATA_PATH, "repos")
RELATORIOS_PATH = os.path.join(REPORTS_PATH, "relatorios")

# Git
COMMIT_INICIAL = "e560365081a8497c2e5dafba60c1430a7f31cdb7"
DATA_LIMITE = "2026-05-04 23:59:59"

# Professores
PROFESSORES = [
    "Professor 1",
    "Professor 2",
    "Professor 3"
]

# Critérios de Avaliação
CRITERIOS = {
    'logica_firmware': {
        'peso': 30,
        'descricao': 'Lógica do Firmware'
    },
    'metrica_wokwi': {
        'peso': 20,
        'descricao': 'Métrica/Wokwi'
    },
    'ci_cd': {
        'peso': 25,
        'descricao': 'CI/CD'
    },
    'documentacao': {
        'peso': 10,
        'descricao': 'Documentação'
    },
    'estrutura': {
        'peso': 10,
        'descricao': 'Estrutura/Versionamento'
    }
}

# Faixas de Nota
FAIXAS_NOTA = {
    'excelente': (90, 100),
    'bom': (70, 89),
    'medio': (50, 69),
    'ruim': (0, 49)
}

# Arquivos de Saída (Caminhos Absolutos)
SAIDAS = {
    'dashboard': os.path.join(REPORTS_PATH, 'dashboard_final.html'),
    'json_completo': os.path.join(DATA_PATH, 'avaliacoes_melhoradas.json'),
    'json_consolidado': os.path.join(DATA_PATH, 'avaliacoes_completas.json')
}

# Templates de Feedback
FEEDBACKS = {
    'logica_firmware': {
        'high': "Código bem estruturado com lógica clara. Implementa funções/modularização adequada.",
        'medium': "Código funcional mas poderia ser mais organizado. Falta modularização.",
        'low': "Código com problemas de estrutura ou lógica."
    },
    'metrica_wokwi': {
        'high': "Diagrama completo e bem organizado no Wokwi.",
        'medium': "Diagrama funcional mas com organização básica.",
        'low': "Diagrama incompleto ou com problemas."
    },
    'ci_cd': {
        'high': "Pipeline CI/CD bem configurado com GitHub Actions.",
        'medium': "CI/CD configurado mas com limitações.",
        'low': "CI/CD ausente ou mal configurado."
    },
    'documentacao': {
        'high': "Documentação completa e bem estruturada.",
        'medium': "Documentação presente mas incompleta.",
        'low': "Documentação mínima ou ausente."
    },
    'estrutura': {
        'high': "Repositório bem organizado com estrutura clara.",
        'medium': "Estrutura básica presente. Poderia melhorar.",
        'low': "Estrutura desorganizada."
    }
}
