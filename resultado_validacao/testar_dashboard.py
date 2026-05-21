#!/usr/bin/env python3
"""
Testa se o dashboard final está funcional
"""
import os
import json

RESULTADO_PATH = "/workspace/resultado_validacao"

def testar_dashboard():
    print("="*60)
    print("TESTE DO DASHBOARD")
    print("="*60)
    
    # Verificar se o arquivo existe
    html_file = os.path.join(RESULTADO_PATH, 'dashboard_final.html')
    if not os.path.exists(html_file):
        print("❌ dashboard_final.html não encontrado")
        return False
    
    # Ler o HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"✅ Arquivo encontrado: {html_file}")
    print(f"   Tamanho: {len(html_content):,} caracteres")
    
    # Verificar se tem dados embutidos
    if 'let students = [{' in html_content:
        print("✅ Dados embutidos encontrados")
    else:
        print("❌ Dados não estão embutidos corretamente")
        return False
    
    # Extrair e validar JSON
    import re
    match = re.search(r'let students = (\[.*?\]);', html_content, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            students = json.loads(json_str)
            print(f"✅ JSON válido com {len(students)} alunos")
            
            # Verificar estrutura
            if len(students) > 0:
                aluno = students[0]
                campos_obrigatorios = ['nome', 'nota_final', 'status', 'criterios']
                campos_faltando = [c for c in campos_obrigatorios if c not in aluno]
                
                if campos_faltando:
                    print(f"⚠️  Campos faltando: {campos_faltando}")
                else:
                    print("✅ Estrutura dos dados OK")
                
                # Verificar se tem nota
                notas = [a['nota_final'] for a in students if 'nota_final' in a]
                if notas:
                    print(f"   Nota média: {sum(notas)/len(notas):.1f}")
                    print(f"   Maior nota: {max(notas):.1f}")
                    print(f"   Menor nota: {min(notas):.1f}")
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao parsear JSON: {e}")
            return False
    else:
        print("❌ Não foi possível extrair o JSON")
        return False
    
    # Verificar JavaScript
    if 'function filterStudents' in html_content:
        print("✅ Função filterStudents encontrada")
    else:
        print("⚠️  Função filterStudents não encontrada")
    
    if 'function renderStudents' in html_content or 'function displayStudents' in html_content:
        print("✅ Função de renderização encontrada")
    else:
        print("⚠️  Função de renderização não encontrada")
    
    # Verificar CSS
    if '.student-card' in html_content:
        print("✅ CSS dos cards encontrado")
    
    if '.controls' in html_content:
        print("✅ CSS dos controles encontrado")
    
    # Verificar elementos HTML
    if 'id="search"' in html_content:
        print("✅ Campo de busca encontrado")
    
    if 'id="students-container"' in html_content or 'class="students-grid"' in html_content:
        print("✅ Container dos alunos encontrado")
    
    print("\n" + "="*60)
    print("RESULTADO: ✅ DASHBOARD VÁLIDO")
    print("="*60)
    print(f"\n🌐 Acesse em: file://{html_file}")
    print(f"\n💡 Dica: Funciona sem servidor HTTP!")
    print(f"   Basta abrir o arquivo no navegador.")
    
    return True

if __name__ == '__main__':
    success = testar_dashboard()
    exit(0 if success else 1)
