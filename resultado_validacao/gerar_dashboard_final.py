#!/usr/bin/env python3
"""
Gera dashboard HTML final com dados embutidos
Funciona sem servidor HTTP (file://)
"""
import json
import os

RESULTADO_PATH = "/workspace/resultado_validacao"

def main():
    resultado_path = RESULTADO_PATH
    
    # Ler o HTML template
    template_file = os.path.join(resultado_path, 'dashboard_completo.html')
    with open(template_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Ler o JSON com dados
    json_file = os.path.join(resultado_path, 'avaliacoes_melhoradas.json')
    with open(json_file, 'r', encoding='utf-8') as f:
        students_data = json.load(f)
    
    # Converter para string JSON
    students_json_str = json.dumps(students_data, ensure_ascii=False)
    
    # Encontrar e substituir a lista de estudantes
    # Procura por: let students = []; ou let students = [];
    import re
    
    # Substituir a declaração da variável students
    pattern = r'let\s+students\s*=\s*\[\];'
    replacement = f'let students = {students_json_str};'
    
    html_final = re.sub(pattern, replacement, html_content)
    
    # Se não encontrou o padrão, tenta outro
    if 'let students = ' not in html_final:
        # Adiciona antes do fechamento do head
        html_final = html_final.replace(
            '// Dados dos alunos - serão substituídos pelo script de build',
            f'let students = {students_json_str};'
        )
    
    # Salvar HTML final
    output_file = os.path.join(resultado_path, 'dashboard_final.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_final)
    
    print(f"✅ Dashboard final gerado: {output_file}")
    print(f"   Tamanho: {len(html_final):,} caracteres")
    print(f"   Número de alunos: {len(students_data)}")
    print(f"\n🌐 Acesse em: file://{output_file}")
    print(f"\n💡 Dica: Funciona sem servidor HTTP!")

if __name__ == '__main__':
    main()
