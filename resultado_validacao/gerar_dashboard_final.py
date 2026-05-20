#!/usr/bin/env python3
"""
Gera o HTML final com dados embutidos para o dashboard
"""
import json

resultado_path = "/workspace/resultado_validacao"

# Ler o HTML template
with open(f"{resultado_path}/dashboard_completo.html", 'r', encoding='utf-8') as f:
    html_content = f.read()

# Ler o JSON com feedbacks
with open(f"{resultado_path}/avaliacoes_com_feedback.json", 'r', encoding='utf-8') as f:
    students_data = json.load(f)

# Converter para string JSON
students_json_str = json.dumps(students_data, ensure_ascii=False)

# Substituir a linha onde os dados serão carregados
placeholder = "// Dados dos alunos - serão substituídos pelo script de build\n        let students = [];"
replacement = f"// Dados dos alunos - embutidos no build\n        let students = {students_json_str};"

html_final = html_content.replace(placeholder, replacement)

# Salvar HTML final
with open(f"{resultado_path}/dashboard_final.html", 'w', encoding='utf-8') as f:
    f.write(html_final)

print(f"Dashboard final gerado: dashboard_final.html")
print(f"Tamanho: {len(html_final):,} caracteres")
print(f"Número de alunos: {len(students_data)}")
print(f"\nAcesse em: file://{resultado_path}/dashboard_final.html")
