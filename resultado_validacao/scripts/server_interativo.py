#!/usr/bin/env python3
"""
Servidor Interativo para o Dashboard de Validação IoT
Reorganizado - Gerencia rotas para servir arquivos das subpastas data/ e reports/
"""
import http.server
import socketserver
import json
import os
import sys
import subprocess
import urllib.parse
from datetime import datetime

# Adicionar pasta pai ao path para importar config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    import config
except ImportError:
    # Fallback se rodar de fora da pasta scripts
    sys.path.append(os.path.join(os.getcwd(), '..'))
    import config

PORT = 8000

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        """
        Mapeia rotas virtuais para os caminhos físicos organizados
        """
        # Parse path to ignore query parameters
        parsed_path = urllib.parse.urlparse(path).path
        
        # Se pedir a raiz ou index.html, serve o dashboard integrado
        if parsed_path == '/' or parsed_path == '/index.html':
            return os.path.join(config.REPORTS_PATH, 'dashboard_integrado.html')
        
        # Tenta encontrar o arquivo em reports/ (HTML, CSS, JS)
        reports_file = os.path.join(config.REPORTS_PATH, parsed_path.lstrip('/'))
        if os.path.exists(reports_file) and os.path.isfile(reports_file):
            return reports_file
            
        # Tenta encontrar o arquivo em data/ (JSONs, CSVs)
        data_file = os.path.join(config.DATA_PATH, parsed_path.lstrip('/'))
        if os.path.exists(data_file) and os.path.isfile(data_file):
            return data_file
            
        # Tenta encontrar o arquivo na raiz do resultado_validacao
        root_file = os.path.join(config.RESULTADO_PATH, parsed_path.lstrip('/'))
        if os.path.exists(root_file) and os.path.isfile(root_file):
            return root_file
            
        # Comportamento padrão (relativo ao CWD do servidor)
        return super().translate_path(path)

    def do_GET(self):
        # Rotas de API
        if self.path == '/api/students':
            self.send_students_data()
            return
        
        if self.path.startswith('/api/get_content'):
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            name = query.get('name', [None])[0]
            if not name:
                self.send_error(400, "Name required")
                return
            
            conteudos = self.load_json('conteudos_manuais.json', {})
            aluno_content = conteudos.get(name, {})
            
            result = {
                'readme': aluno_content.get('readme', {}).get('conteudo', ''),
                'main_py': aluno_content.get('main_py', {}).get('conteudo', '')
            }
            self.send_json(result)
            return

        return super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b''
        
        data = {}
        if post_data:
            try:
                data = json.loads(post_data)
            except json.JSONDecodeError:
                pass

        if self.path == '/api/update_grade':
            self.update_grade(data)
            self.send_success()
        
        elif self.path == '/api/update_content':
            self.update_content(data)
            self.send_success()
            
        elif self.path == '/api/analyze_student':
            result = self.analyze_student(data)
            if result:
                self.send_json(result)
            else:
                self.send_error(500, "Analysis failed")
                
        elif self.path == '/api/consolidate':
            success = self.run_consolidation()
            if success:
                self.send_success()
            else:
                self.send_error(500, "Consolidation failed")
        else:
            self.send_error(404)

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def send_students_data(self):
        # 1. Carregar dados processados
        path = config.SAIDAS['json_completo']
        if not os.path.exists(path):
            path = os.path.join(config.DATA_PATH, 'avaliacoes_com_feedback.json')
        
        students = []
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                students = json.load(f)
        
        # 2. Patch com notas manuais
        notas_manuais = self.load_json('notas_manuais.json', {})
        conteudos_manuais = self.load_json('conteudos_manuais.json', {})
        
        for aluno in students:
            nome = aluno['nome']
            if nome in notas_manuais:
                dados_manuais = notas_manuais[nome]
                aluno['tem_avaliacao_manual'] = True
                criterios = aluno.get('criterios', {})
                for crit_id, d in criterios.items():
                    if 'score_auto' not in d:
                        d['score_auto'] = d.get('score', 0)
                
                aluno['nota_manual'] = dados_manuais.get('nota_final_manual', aluno.get('nota_final'))
                aluno['comentario_professor'] = dados_manuais.get('comentario', aluno.get('comentario_professor'))
                aluno['checklist_manual'] = dados_manuais.get('checklist', aluno.get('checklist_manual', {}))
                aluno['criterios_manuais'] = dados_manuais.get('criterios', aluno.get('criterios_manuais', {}))
                
                if aluno['criterios_manuais']:
                    for crit_id, manual_score in aluno['criterios_manuais'].items():
                        if crit_id in criterios:
                            aluno['criterios'][crit_id]['score_manual'] = manual_score
                            aluno['criterios'][crit_id]['score'] = manual_score
                            aluno['criterios'][crit_id]['is_manual'] = True
                aluno['nota_final'] = aluno['nota_manual']
            else:
                criterios = aluno.get('criterios', {})
                for crit_id, d in criterios.items():
                    if 'score_auto' not in d:
                        d['score_auto'] = d.get('score', 0)
                    d['score'] = d['score_auto']
                    d['is_manual'] = False
            
            if nome in conteudos_manuais:
                c_manuais = conteudos_manuais[nome]
                if 'readme' in c_manuais and c_manuais['readme'].get('conteudo'):
                    aluno['readme_content'] = c_manuais['readme']['conteudo']
                    aluno['manual_readme'] = True
                if 'main_py' in c_manuais and c_manuais['main_py'].get('conteudo'):
                    aluno['main_py_content'] = c_manuais['main_py']['conteudo']
                    aluno['manual_main_py'] = True
                    aluno['main_py_exists'] = True

        self.send_json(students)

    def send_success(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status": "ok"}')

    def load_json(self, filename, default=None):
        path = os.path.join(config.DATA_PATH, filename)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default

    def save_json(self, filename, data):
        path = os.path.join(config.DATA_PATH, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def update_grade(self, data):
        name = data['name']
        grade = data['grade']
        comment = data['comment']
        checklist = data.get('checklist', {})
        criterios = data.get('criterios', {})
        
        notas = self.load_json('notas_manuais.json', {})
        notas[name] = {
            'nota_final_manual': grade,
            'comentario': comment,
            'checklist': checklist,
            'criterios': criterios,
            'data_avaliacao': datetime.now().isoformat()
        }
        self.save_json('notas_manuais.json', notas)

    def update_content(self, data):
        name = data['name']
        readme = data.get('readme')
        main_py = data.get('main_py')
        
        conteudos = self.load_json('conteudos_manuais.json', {})
        if name not in conteudos:
            conteudos[name] = {}
        
        if readme is not None:
            conteudos[name]['readme'] = {'conteudo': readme, 'data_insercao': datetime.now().isoformat()}
        
        if main_py is not None:
            conteudos[name]['main_py'] = {'conteudo': main_py, 'data_insercao': datetime.now().isoformat()}
            
        self.save_json('conteudos_manuais.json', conteudos)

    def analyze_student(self, data):
        name = data.get('name')
        if not name: return None
        try:
            # Tenta importar Pipeline de onde quer que ele esteja agora
            sys.path.append(config.SCRIPTS_PATH)
            from fase5_avaliar import PipelineValidacao # Exemplo de onde a classe pode estar
            pipeline = PipelineValidacao()
            return pipeline.reanalisar_aluno(name)
        except Exception as e:
            print(f"Error analyzing student: {e}")
            return None

    def run_consolidation(self):
        try:
            subprocess.run([sys.executable, os.path.join(config.RESULTADO_PATH, '00_run_all.py')], check=True)
            return True
        except Exception as e:
            print(f"Error in consolidation: {e}")
            return False

if __name__ == "__main__":
    # O servidor DEVE rodar da pasta resultado_validacao para que caminhos relativos no front-end funcionem
    os.chdir(config.RESULTADO_PATH)
    socketserver.TCPServer.allow_reuse_address = True # Resolve o problema de "Address already in use" rápido
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"✅ Servidor interativo REORGANIZADO rodando em http://localhost:{PORT}")
        print(f"📁 Root: {config.RESULTADO_PATH}")
        print(f"📁 Reports: {config.REPORTS_PATH}")
        print(f"📁 Data: {config.DATA_PATH}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")
