#!/usr/bin/env python3
"""
Script mestre para executar todo o pipeline de validação IoT
Organiza a execução de todos os scripts em sequência
Versão Reorganizada - Scripts em ./scripts/ e Dados em ./data/
"""
import os
import sys
import subprocess
from pathlib import Path

# Adicionar pasta raiz ao path para importar config.py
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_PATH)

import config

scripts_order = [
    {
        'name': 'Fase 1: Extrair commits',
        'script': 'extrair_commits.py',
        'description': 'Extrai commits entre commit inicial e data limite'
    },
    {
        'name': 'Fase 2: Processar dados completos',
        'script': 'processar_dados_completos.py',
        'description': 'Processa commits, emails, imagens e artefatos'
    },
    {
        'name': 'Fase 3: Gerar feedbacks LLM',
        'script': 'gerar_feedbacks_llm.py',
        'description': 'Gera feedbacks detalhados para cada critério'
    },
    {
        'name': 'Fase 4: Aplicar melhorias',
        'script': 'aplicar_melhorias.py',
        'description': 'Aplica melhorias, ranking e feedback completo'
    },
    {
        'name': 'Fase 5: Gerar JSON do dashboard',
        'script': 'gerar_json_dashboard.py',
        'description': 'Consolida dados em JSON para o dashboard'
    },
    {
        'name': 'Fase 6: Gerar dashboard final',
        'script': 'gerar_dashboard_final.py',
        'description': 'Gera HTML final com dados embutidos'
    }
]

def run_script(script_name):
    """Executa um script Python na pasta scripts/ e retorna o resultado"""
    script_path = os.path.join(config.SCRIPTS_PATH, script_name)
    
    if not os.path.exists(script_path):
        print(f"❌ Script não encontrado: {script_path}")
        return False, f"Script não encontrado: {script_name}"
    
    print(f"\n{'='*60}")
    print(f"Executando: {script_name}")
    print(f"{'='*60}\n")
    
    try:
        # Passar a pasta raiz para que os scripts encontrem config.py
        env = os.environ.copy()
        env["PYTHONPATH"] = ROOT_PATH + os.pathsep + env.get("PYTHONPATH", "")
        
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutos de timeout
            cwd=ROOT_PATH, # Executar da raiz para caminhos relativos funcionarem se não usarem config.py
            env=env
        )
        
        if result.returncode == 0:
            print(f"✅ {script_name} concluído com sucesso")
            if result.stdout:
                print(result.stdout)
            return True, result.stdout
        else:
            print(f"❌ Erro ao executar {script_name}")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False, result.stderr
            
    except subprocess.TimeoutExpired:
        print(f"❌ Timeout: {script_name} excedeu 5 minutos")
        return False, "Timeout"
    except Exception as e:
        print(f"❌ Exceção: {e}")
        return False, str(e)

def main():
    print("="*60)
    print("PIPELINE DE VALIDAÇÃO IOT (ORGANIZADO)")
    print("="*60)
    
    # Criar pastas se não existirem
    os.makedirs(config.DATA_PATH, exist_ok=True)
    os.makedirs(config.REPORTS_PATH, exist_ok=True)
    
    # Executar scripts em sequência
    results = []
    for i, phase in enumerate(scripts_order, 1):
        print(f"\n{'#'*60}")
        print(f"# FASE {i}: {phase['name']}")
        print(f"# {phase['description']}")
        print(f"{'#'*60}")
        
        success, output = run_script(phase['script'])
        results.append({
            'phase': i,
            'name': phase['name'],
            'success': success,
            'output': output
        })
        
        if not success:
            print(f"\n❌ Pipeline interrompido na fase {i}: {phase['name']}")
            return 1
    
    # Resumo final
    print("\n" + "="*60)
    print("RESUMO DA EXECUÇÃO")
    print("="*60)
    
    for r in results:
        status = "✅" if r['success'] else "❌"
        print(f"{status} Fase {r['phase']}: {r['name']}")
    
    if all(r['success'] for r in results):
        print("\n🎉 Pipeline concluído com sucesso!")
        print(f"\n📁 Resultados disponíveis em: {config.DATA_PATH}")
        print(f"🌐 Dashboard gerado em: {config.SAIDAS['dashboard']}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
