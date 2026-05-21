#!/usr/bin/env python3
"""
Verifica a integridade dos dados processados
"""
import json
import os

RESULTADO_PATH = "/workspace/resultado_validacao"

def verificar_integridade():
    print("="*60)
    print("VERIFICAÇÃO DE INTEGRIDADE")
    print("="*60)
    
    erros = []
    avisos = []
    
    # Carregar dados
    arquivo_json = os.path.join(RESULTADO_PATH, 'avaliacoes_melhoradas.json')
    if not os.path.exists(arquivo_json):
        print(f"❌ Arquivo não encontrado: {arquivo_json}")
        return False
    
    with open(arquivo_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    print(f"Total de alunos: {len(dados)}")
    
    # Verificar cada aluno
    for i, aluno in enumerate(dados):
        # Verificar campos obrigatórios
        campos_obrigatorios = ['nome', 'nota_final', 'status', 'criterios']
        for campo in campos_obrigatorios:
            if campo not in aluno:
                erros.append(f"Aluno {i+1}: Campo '{campo}' ausente")
        
        # Verificar nota
        if 'nota_final' in aluno:
            nota = aluno['nota_final']
            if nota < 0 or nota > 100:
                erros.append(f"Aluno {i+1}: Nota inválida ({nota})")
        
        # Verificar critérios
        if 'criterios' in aluno:
            criterios = aluno['criterios']
            if 'logica_firmware' not in criterios:
                avisos.append(f"Aluno {i+1}: Sem lógica do firmware")
            if 'ci_cd' not in criterios:
                avisos.append(f"Aluno {i+1}: Sem CI/CD")
        
        # Verificar ranking
        if 'ranking' not in aluno:
            avisos.append(f"Aluno {i+1}: Sem ranking")
    
    # Verificar arquivo HTML
    html_file = os.path.join(RESULTADO_PATH, 'dashboard_final.html')
    if not os.path.exists(html_file):
        avisos.append("Dashboard HTML não encontrado")
    else:
        tamanho = os.path.getsize(html_file)
        if tamanho < 1000:
            erros.append(f"Dashboard HTML muito pequeno ({tamanho} bytes)")
    
    # Relatório
    print("\n" + "="*60)
    print("RESULTADO")
    print("="*60)
    
    if erros:
        print(f"\n❌ Erros encontrados: {len(erros)}")
        for erro in erros[:10]:  # Mostrar primeiros 10
            print(f"   - {erro}")
        if len(erros) > 10:
            print(f"   ... e mais {len(erros)-10} erros")
    else:
        print("\n✅ Nenhum erro encontrado")
    
    if avisos:
        print(f"\n⚠️  Avisos: {len(avisos)}")
        for aviso in avisos[:5]:  # Mostrar primeiros 5
            print(f"   - {aviso}")
        if len(avisos) > 5:
            print(f"   ... e mais {len(avisos)-5} avisos")
    
    # Estatísticas
    print("\n" + "="*60)
    print("ESTATÍSTICAS")
    print("="*60)
    
    notas = [a['nota_final'] for a in dados if 'nota_final' in a]
    if notas:
        print(f"Nota média: {sum(notas)/len(notas):.1f}")
        print(f"Maior nota: {max(notas):.1f}")
        print(f"Menor nota: {min(notas):.1f}")
        print(f"Alunos com nota >= 90: {len([n for n in notas if n >= 90])}")
        print(f"Alunos com nota >= 70: {len([n for n in notas if n >= 70])}")
    
    print("\n" + "="*60)
    
    return len(erros) == 0

if __name__ == '__main__':
    success = verificar_integridade()
    exit(0 if success else 1)
