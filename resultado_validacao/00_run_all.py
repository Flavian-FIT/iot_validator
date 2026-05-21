#!/usr/bin/env python3
"""
Script mestre para executar todo o pipeline de validação IoT
Organiza a execução de todos os scripts em sequência
"""
import os
import sys
import subprocess
from pathlib import Path

RESULTADO_PATH = "/workspace/resultado_validacao"

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
    """Executa um script Python e retorna o resultado"""
    script_path = os.path.join(RESULTADO_PATH, script_name)
    
    if not os.path.exists(script_path):
        print(f"❌ Script não encontrado: {script_path}")
        return False, f"Script não encontrado: {script_name}"
    
    print(f"\n{'='*60}")
    print(f"Executando: {script_name}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutos de timeout
            cwd=RESULTADO_PATH
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
    print("PIPELINE DE VALIDAÇÃO IOT")
    print("="*60)
    print("\nEste script executa todo o pipeline de validação em sequência.")
    print("Cada fase depende dos resultados da fase anterior.\n")
    
    # Verificar pré-requisitos
    print("Verificando pré-requisitos...")
    required_files = [
        'avaliacoes_com_feedback.json',
        'repositorios_processados.json'
    ]
    
    for file in required_files:
        if not os.path.exists(os.path.join(RESULTADO_PATH, file)):
            print(f"⚠️  Arquivo base não encontrado: {file}")
            print("   Certifique-se de ter executado as fases iniciais primeiro.")
    
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
            print("   Verifique os logs acima para detalhes.")
            return 1
    
    # Resumo final
    print("\n" + "="*60)
    print("RESUMO DA EXECUÇÃO")
    print("="*60)
    
    all_success = all(r['success'] for r in results)
    
    for r in results:
        status = "✅" if r['success'] else "❌"
        print(f"{status} Fase {r['phase']}: {r['name']}")
    
    if all_success:
        print("\n🎉 Pipeline concluído com sucesso!")
        print(f"\n📁 Arquivos de saída:")
        print(f"   - {RESULTADO_PATH}/avaliacoes_com_commits.json")
        print(f"   - {RESULTADO_PATH}/avaliacoes_completo.json")
        print(f"   - {RESULTADO_PATH}/avaliacoes_com_feedback.json")
        print(f"   - {RESULTADO_PATH}/avaliacoes_melhoradas.json")
        print(f"   - {RESULTADO_PATH}/avaliacoes_completas.json")
        print(f"   - {RESULTADO_PATH}/dashboard_final.html")
        print(f"\n🌐 Dashboard: file://{RESULTADO_PATH}/dashboard_final.html")
    else:
        print("\n❌ Algumas fases falharam. Verifique os logs.")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
