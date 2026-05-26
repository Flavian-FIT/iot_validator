#!/usr/bin/env python3
"""
Pipeline Completo de Validação IoT
Gera o dashboard final com todos os dados processados

Executa todas as etapas:
1. Extração de commits
2. Processamento de dados (emails, imagens, artefatos)
3. Geração de feedbacks detalhados
4. Aplicação de melhorias e ranking
5. Consolidação em JSON
6. Geração do dashboard HTML final

Uso: python3 gerar_dashboard_completo.py
"""
import os
import sys
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime

# Adicionar pasta pai ao path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from config import RESULTADO_PATH, PROFESSORES, CRITERIOS, SAIDAS, REPORTS_PATH, DATA_PATH
except ImportError:
    RESULTADO_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORTS_PATH = os.path.join(RESULTADO_PATH, 'reports')
    DATA_PATH = os.path.join(RESULTADO_PATH, 'data')
    PROFESSORES = ["Professor 1"]
    CRITERIOS = {}
    SAIDAS = {'json_consolidado': os.path.join(DATA_PATH, 'avaliacoes_consolidadas.json')}

ARQUIVO_AVALIACOES = SAIDAS.get('json_consolidado', os.path.join(DATA_PATH, 'avaliacoes_consolidadas.json'))

class PipelineValidacao:
    """Pipeline completo de validação de projetos IoT"""
    
    def __init__(self, resultado_path=RESULTADO_PATH):
        self.resultado_path = resultado_path
        self.repos_path = os.path.join(DATA_PATH, 'repos')
        self.dados = None
        self.stats = {
            'total_alunos': 0,
            'com_sucesso': 0,
            'com_erro': 0,
            'nota_media': 0,
            'maior_nota': 0,
            'menor_nota': 100
        }
    
    def sanitize_string(self, text):
        """Corrige problemas de encoding em strings (nomes, emails, etc)"""
        if not text: return text
        
        # Mapa de substituições comuns de encoding quebrado (UTF-8 interpretado como CP850/Outros)
        replacements = {
            '├│': 'ó', '├║': 'ú', '├й': 'é', '├б': 'á', '├н': 'í', 
            '├г': 'ã', '├к': 'ê', '├з': 'ç', '├┤': 'ô', '├в': 'â',
            '├и': 'è', '├Т': 'ò', '├п': 'ï', '├Б': 'Á', '├И': 'É',
            '├Н': 'Í', '├У': 'Ó', '├Ъ': 'Ú', '├З': 'Ç', '├Ф': 'Ô',
            '├Х': 'Õ', '├А': 'À', '├Г': 'Ã', '├д': 'ä', '├е': 'å',
            '├ж': 'æ', '├ш': 'ø', '├╣': 'ù', '├ы': 'û', '├ь': 'ü',
            '├с': 'ñ'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
            
        return text

    def load_data(self):
        """Carrega dados iniciais dos alunos"""
        arquivo_avaliacoes = ARQUIVO_AVALIACOES
        if not os.path.exists(arquivo_avaliacoes):
            # Tentar fallback
            arquivo_avaliacoes = os.path.join(DATA_PATH, 'avaliacoes_completas.json')
            if not os.path.exists(arquivo_avaliacoes):
                arquivo_avaliacoes = os.path.join(DATA_PATH, 'avaliacoes.json')
                if not os.path.exists(arquivo_avaliacoes):
                    return []
            
        with open(arquivo_avaliacoes, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            
        # Limpar nomes e emails ao carregar
        for aluno in dados:
            aluno['nome_exibicao'] = self.sanitize_string(aluno.get('nome'))
            if 'email' in aluno:
                aluno['email'] = self.sanitize_string(aluno['email'])
            
        return dados

    def carregar_dados_existentes(self):
        """Carrega dados já processados"""
        self.dados = self.load_data()
        
        if not self.dados:
            print(f"❌ Arquivo de avaliações não encontrado em: {ARQUIVO_AVALIACOES}")
            return False
        
        self.stats['total_alunos'] = len(self.dados)
        print(f"✅ Carregados {len(self.dados)} alunos")
        return True

    def gerar_html(self):
        """Gera dashboard HTML final com dados embutidos"""
        print("\n" + "="*60)
        print("FASE FINAL: Gerando Dashboard HTML")
        print("="*60)
        
        # Ler template HTML (usar o integrado)
        template_file = os.path.join(REPORTS_PATH, 'dashboard_integrado.html')
        if not os.path.exists(template_file):
            template_file = os.path.join(REPORTS_PATH, 'dashboard_completo.html')
            
        if not os.path.exists(template_file):
            print(f"❌ Template HTML não encontrado: {template_file}")
            return False
            
        with open(template_file, 'r', encoding='utf-8') as f:
            html_lines = f.readlines()
        
        # Converter dados para JSON
        students_json_str = json.dumps(self.dados, ensure_ascii=False)
        
        # Procurar e substituir a linha com "let students = [];"
        html_final_lines = []
        for line in html_lines:
            if 'let students = []' in line:
                # Manter a identação
                indent = line[:len(line) - len(line.lstrip())]
                html_final_lines.append(f"{indent}let students = {students_json_str};\n")
                html_final_lines.append(f"{indent}let professors_list = {json.dumps(PROFESSORES, ensure_ascii=False)};\n")
                html_final_lines.append(f"{indent}let criteria_config = {json.dumps(CRITERIOS, ensure_ascii=False)};\n")
            else:
                html_final_lines.append(line)
        
        html_final = ''.join(html_final_lines)
        
        # Salvar HTML final
        output_file = os.path.join(REPORTS_PATH, 'dashboard_final.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_final)
            
        print(f"✅ Dashboard gerado com sucesso!")
        print(f"   Arquivo: {output_file}")
        print(f"   Alunos: {len(self.dados)}")
        print(f"   Tamanho: {len(html_final):,} caracteres")
        
        return True

    def run(self):
        """Executa todo o pipeline"""
        print("="*60)
        print("PIPELINE DE VALIDAÇÃO IOT")
        print("="*60)
        print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Diretório: {self.resultado_path}")
        print("="*60)
        
        if not self.carregar_dados_existentes():
            return 1
            
        # Para este script simplificado, apenas geramos o HTML a partir dos dados consolidados
        # Se precisar de extração de commits, etc, deve-se usar os scripts específicos
        
        if self.gerar_html():
            print(f"\nDashboard: file://{REPORTS_PATH}/dashboard_final.html")
            return 0
        else:
            return 1

if __name__ == "__main__":
    pipeline = PipelineValidacao()
    sys.exit(pipeline.run())
