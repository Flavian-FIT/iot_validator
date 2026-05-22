#!/usr/bin/env python3
"""
Gera dashboard HTML final com dados embutidos
Reorganizado - Usa config.py
"""
import json
import os
import sys
import re

# Adicionar pasta pai ao path para importar config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def main():
    # Caminhos via config
    reports_path = config.REPORTS_PATH
    data_path = config.DATA_PATH
    
    # Ler o HTML template (está em reports/)
    template_file = os.path.join(reports_path, 'dashboard_completo.html')
    if not os.path.exists(template_file):
        print(f"❌ Erro: Template {template_file} não encontrado.")
        return

    with open(template_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Ler o JSON com dados (está em data/)
    json_file = config.SAIDAS['json_completo']
    if not os.path.exists(json_file):
        print(f"❌ Erro: JSON de dados {json_file} não encontrado.")
        return

    with open(json_file, 'r', encoding='utf-8') as f:
        students_data = json.load(f)
    
    # Converter para string JSON
    students_json_str = json.dumps(students_data, ensure_ascii=False)
    
    # Substituir a declaração da variável students
    pattern = r'let\s+students\s*=\s*\[\];'
    replacement = f'let students = {students_json_str};'
    
    html_final = re.sub(pattern, replacement, html_content)
    
    # Se não encontrou o padrão, tenta outro
    if 'let students = ' not in html_final:
        # Adiciona antes do fechamento do head ou comentário específico
        html_final = html_final.replace(
            '// Dados dos alunos - serão substituídos pelo script de build',
            f'let students = {students_json_str};'
        )
    
    # Salvar HTML final (caminho configurado)
    output_file = config.SAIDAS['dashboard']
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_final)
    
    print(f"✅ Dashboard final gerado: {output_file}")
    print(f"   Tamanho: {len(html_final):,} caracteres")
    print(f"   Número de alunos: {len(students_data)}")
    print(f"\n🌐 Acesse em: file://{output_file}")

if __name__ == '__main__':
    main()
