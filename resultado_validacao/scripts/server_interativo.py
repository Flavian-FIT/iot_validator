#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import subprocess
import urllib.parse
from datetime import datetime
from gerar_dashboard_completo import PipelineValidacao

PORT = 8000
RESULTADO_PATH = "/workspace/resultado_validacao"

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/dashboard_integrado.html'
        
        if self.path == '/api/students':
            # Serve merged data on the fly
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
            
            # Extract plain text content
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
        # 1. Load the most recent fully processed data
        path = os.path.join(RESULTADO_PATH, 'avaliacoes_melhoradas.json')
        if not os.path.exists(path):
            path = os.path.join(RESULTADO_PATH, 'avaliacoes_com_feedback.json')
        
        students = []
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                students = json.load(f)
        
        # 2. Patch with latest manual notes
        notas_manuais = self.load_json('notas_manuais.json', {})
        conteudos_manuais = self.load_json('conteudos_manuais.json', {})
        
        for aluno in students:
            nome = aluno['nome']
            
            # Apply latest manual notes/checklist/criterios
            if nome in notas_manuais:
                dados_manuais = notas_manuais[nome]
                aluno['tem_avaliacao_manual'] = True
                
                # Ensure each criterion has score_auto before patching
                criterios = aluno.get('criterios', {})
                for crit_id, d in criterios.items():
                    if 'score_auto' not in d:
                        d['score_auto'] = d.get('score', 0)
                
                aluno['nota_manual'] = dados_manuais.get('nota_final_manual', aluno.get('nota_final'))
                aluno['comentario_professor'] = dados_manuais.get('comentario', aluno.get('comentario_professor'))
                aluno['checklist_manual'] = dados_manuais.get('checklist', aluno.get('checklist_manual', {}))
                aluno['criterios_manuais'] = dados_manuais.get('criterios', aluno.get('criterios_manuais', {}))
                
                # Patch criteria scores
                if aluno['criterios_manuais']:
                    for crit_id, manual_score in aluno['criterios_manuais'].items():
                        if crit_id in criterios:
                            aluno['criterios'][crit_id]['score_manual'] = manual_score
                            aluno['criterios'][crit_id]['score'] = manual_score
                            aluno['criterios'][crit_id]['is_manual'] = True
                
                aluno['nota_final'] = aluno['nota_manual']
            else:
                # Ensure score_auto exists even if no manual note yet
                criterios = aluno.get('criterios', {})
                for crit_id, d in criterios.items():
                    if 'score_auto' not in d:
                        d['score_auto'] = d.get('score', 0)
                    d['score'] = d['score_auto']
                    d['is_manual'] = False
            
            # Apply latest manual content
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

    def send_json_file(self, filename):
        path = os.path.join(RESULTADO_PATH, filename)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.send_json(data)
        else:
            self.send_json([])

    def send_success(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status": "ok"}')

    def load_json(self, filename, default=None):
        path = os.path.join(RESULTADO_PATH, filename)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default

    def save_json(self, filename, data):
        path = os.path.join(RESULTADO_PATH, filename)
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
            conteudos[name]['readme'] = {
                'conteudo': readme,
                'data_insercao': datetime.now().isoformat(),
                'tamanho': len(readme)
            }
        
        if main_py is not None:
            conteudos[name]['main_py'] = {
                'conteudo': main_py,
                'data_insercao': datetime.now().isoformat(),
                'tamanho': len(main_py)
            }
            
        self.save_json('conteudos_manuais.json', conteudos)

    def analyze_student(self, data):
        name = data.get('name')
        if not name:
            return None
        
        try:
            pipeline = PipelineValidacao()
            student_data = pipeline.reanalisar_aluno(name)
            return student_data
        except Exception as e:
            print(f"Error analyzing student: {e}")
            return None

    def run_consolidation(self):
        try:
            # Execute the full pipeline to ensure everything is updated
            print("Running full pipeline consolidation...")
            subprocess.run(['python3', 'gerar_dashboard_completo.py'], cwd=RESULTADO_PATH, check=True)
            return True
        except Exception as e:
            print(f"Error in consolidation: {e}")
            return False

if __name__ == "__main__":
    os.chdir(RESULTADO_PATH)
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"Servidor interativo rodando em http://localhost:{PORT}")
        print("Pressione Ctrl+C para encerrar")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
