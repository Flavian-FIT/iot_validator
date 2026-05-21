#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import subprocess
import urllib.parse
from datetime import datetime

PORT = 8000
RESULTADO_PATH = "/workspace/resultado_validacao"

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/dashboard_integrado.html'
        
        if self.path == '/api/students':
            # Use avaliacoes_melhoradas.json as it's the most complete
            self.send_json_file('avaliacoes_melhoradas.json')
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
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if self.path == '/api/update_grade':
            self.update_grade(data)
            self.send_success()
        
        elif self.path == '/api/update_content':
            self.update_content(data)
            self.send_success()
            
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
        
        notas = self.load_json('notas_manuais.json', {})
        notas[name] = {
            'nota_final_manual': grade,
            'comentario': comment,
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
        
        if readme:
            conteudos[name]['readme'] = {
                'conteudo': readme,
                'data_insercao': datetime.now().isoformat(),
                'tamanho': len(readme)
            }
        
        if main_py:
            conteudos[name]['main_py'] = {
                'conteudo': main_py,
                'data_insercao': datetime.now().isoformat(),
                'tamanho': len(main_py)
            }
            
        self.save_json('conteudos_manuais.json', conteudos)

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
