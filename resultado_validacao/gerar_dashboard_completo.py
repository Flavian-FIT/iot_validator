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

RESULTADO_PATH = "/workspace/resultado_validacao"
ARQUIVO_NOTAS_MANUAIS = "notas_manuais.json"
ARQUIVO_CONTEUDOS_MANUAIS = "conteudos_manuais.json"
COMMIT_INICIAL = "e560365081a8497c2e5dafba60c1430a7f31cdb7"
DATA_LIMITE = "2026-05-04 23:59:59"

class PipelineValidacao:
    """Pipeline completo de validação de projetos IoT"""
    
    def __init__(self, resultado_path=RESULTADO_PATH):
        self.resultado_path = resultado_path
        self.repos_path = os.path.join(resultado_path, 'repos')
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
        
        # Tentar primeiro uma limpeza sistemática se possível
        try:
            # Muitos desses erros vêm de UTF-8 lido como CP850
            # Mas como há caracteres estranhos no meio, o map é mais seguro
            pass
        except:
            pass

        for old, new in replacements.items():
            text = text.replace(old, new)
            
        return text

    def load_data(self):
        """Carrega dados iniciais dos alunos"""
        arquivo_avaliacoes = os.path.join(self.resultado_path, 'avaliacoes_com_feedback.json')
        if not os.path.exists(arquivo_avaliacoes):
            arquivo_avaliacoes = os.path.join(self.resultado_path, 'avaliacoes.json')
            
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
            print("❌ Arquivo de avaliações não encontrado")
            return False
        
        self.stats['total_alunos'] = len(self.dados)
        print(f"✅ Carregados {len(self.dados)} alunos")
        return True
    
    def extrair_commits(self):
        """Extrai commits detalhados de cada repositório"""
        print("\n" + "="*60)
        print("FASE 1: Extraindo commits")
        print("="*60)
        
        commits_count = 0
        for i, aluno in enumerate(self.dados):
            nome = aluno['nome']
            repo_dir = os.path.join(self.repos_path, f"{nome.replace('/', '_').replace(' ', '_')}")
            
            print(f"[{i+1}/{len(self.dados)}] {aluno['nome_exibicao']}...", end=" ")
            
            if os.path.exists(repo_dir) and os.path.isdir(os.path.join(repo_dir, '.git')):
                try:
                    os.chdir(repo_dir)
                    # Usar range de commits: do COMMIT_INICIAL até o final (incluindo todas as branches)
                    # Filtrando pela data limite
                    range_spec = f"{COMMIT_INICIAL}.."
                    
                    # --all garante que pegamos commits em qualquer branch
                    result = subprocess.run(
                        ['git', 'log', '--all', range_spec, f'--before="{DATA_LIMITE}"', '--pretty=format:%h|%an|%ae|%ar|%s'],
                        capture_output=True, text=True, timeout=30
                    )
                    
                    if result.returncode != 0:
                        # Fallback se o range falhar (ex: COMMIT_INICIAL não encontrado)
                        result = subprocess.run(
                            ['git', 'log', '--all', f'--before="{DATA_LIMITE}"', '--pretty=format:%h|%an|%ae|%ar|%s'],
                            capture_output=True, text=True, timeout=30
                        )
                    
                    if result.returncode == 0 and result.stdout.strip():
                        commits = []
                        # Usar um set para evitar duplicatas se o mesmo commit estiver em múltiplas branches
                        seen_hashes = set()
                        for line in result.stdout.strip().split('\n'):
                            if line.strip():
                                parts = line.split('|')
                                if len(parts) >= 5:
                                    h = parts[0]
                                    if h not in seen_hashes:
                                        seen_hashes.add(h)
                                        commits.append({
                                            'hash': h,
                                            'author': self.sanitize_string(parts[1]),
                                            'email': self.sanitize_string(parts[2]),
                                            'date': parts[3],
                                            'message': self.sanitize_string('|'.join(parts[4:]))
                                        })
                        aluno['commits_detalhados'] = commits
                        aluno['total_commits'] = len(commits)
                        commits_count += len(commits)
                        print(f"{len(commits)} commits")
                    else:
                        aluno['commits_detalhados'] = []
                        aluno['total_commits'] = 0
                        print("0 commits")
                except Exception as e:
                    aluno['commits_detalhados'] = []
                    aluno['total_commits'] = 0
                    print(f"Erro: {e}")
                finally:
                    os.chdir(self.resultado_path)
            else:
                aluno['commits_detalhados'] = []
                aluno['total_commits'] = 0
                print("Repo não encontrado")
        
        print(f"\nTotal de commits extraídos: {commits_count}")
        return True
    
    def _extract_student_email(self, aluno, repo_dir):
        """Extrai o email real do aluno a partir dos commits ou README"""
        # 1. Tentar extrair dos commits (mais confiável)
        if os.path.exists(repo_dir) and os.path.isdir(os.path.join(repo_dir, '.git')):
            try:
                # Pegar todos os emails dos autores de commits, exceto o template
                cmd = ['git', 'log', '--all', '--format=%ae']
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_dir)
                if result.returncode == 0:
                    emails = result.stdout.strip().split('\n')
                    # Filtrar emails de sistema/template
                    exclude_patterns = ['noreply@github.com', 'support@github.com', '@fit-tecnologia.org.br']
                    valid_emails = []
                    for e in emails:
                        e = e.strip()
                        if not e: continue
                        is_excluded = False
                        for pattern in exclude_patterns:
                            if pattern in e:
                                is_excluded = True
                                break
                        if not is_excluded:
                            valid_emails.append(e)
                    
                    if valid_emails:
                        # Retornar o email mais frequente
                        from collections import Counter
                        most_common = Counter(valid_emails).most_common(1)
                        if most_common:
                            return most_common[0][0]
            except Exception:
                pass

        # 2. Tentar extrair do README
        readme_content = aluno.get('readme_content', '')
        if readme_content:
            email_readme = self._extract_email_from_readme(readme_content)
            if email_readme:
                return email_readme

        # 3. Retornar o que já tem se nada novo for encontrado
        return aluno.get('email')

    def processar_dados_completos(self):
        """Processa dados completos (emails, imagens, artefatos)"""
        print("\n" + "="*60)
        print("FASE 2: Processando dados completos")
        print("="*60)
        
        for i, aluno in enumerate(self.dados):
            nome = aluno['nome']
            repo_dir = os.path.join(self.repos_path, f"{nome.replace('/', '_').replace(' ', '_')}")
            
            print(f"[{i+1}/{len(self.dados)}] {aluno['nome_exibicao']}...", end=" ")
            
            # Melhorar extração de email
            email = self._extract_student_email(aluno, repo_dir)
            if email:
                email = self.sanitize_string(email)
                aluno['email'] = email
                print(f"Email: {email}")
            else:
                print("Email não encontrado")
            
            # Extrair imagens
            readme_content = aluno.get('readme_content', '')
            repo_url = aluno.get('github_url', '')
            imagens = self._extract_images_from_readme(readme_content, repo_url)
            aluno['imagens'] = imagens
            
            # Detectar artefatos
            main_py_content = ''
            main_py_path = os.path.join(repo_dir, 'src', 'main.py')
            if os.path.exists(main_py_path):
                with open(main_py_path, 'r', encoding='utf-8', errors='ignore') as f:
                    main_py_content = f.read()
            
            artefatos = self._detectar_artefatos_ia(readme_content, aluno.get('commits_detalhados', []), main_py_content)
            aluno['artefatos_ia'] = artefatos
            
            # Análise do README
            aluno['analise_readme'] = {
                'tamanho': len(readme_content) if readme_content else 0,
                'tem_secoes': bool(re.search(r'##', readme_content)) if readme_content else False,
                'tem_codigo': bool(re.search(r'```', readme_content)) if readme_content else False,
                'tem_imagens': len(imagens) > 0
            }
        
        print(f"✅ Dados processados")
        return True
    
    def _processar_aluno_feedbacks(self, aluno):
        """Processa feedbacks para todos os critérios de um aluno"""
        criterios = aluno.get('criterios', {})
        for criterio, dados in criterios.items():
            score = dados.get('score', 0)
            max_score = 30 if criterio == 'logica_firmware' else (25 if criterio == 'ci_cd' else (20 if criterio == 'metrica_wokwi' else 10))
            feedback = self._gerar_feedback(criterio, score, max_score, aluno)
            dados['feedback_detalhado'] = feedback

    def gerar_feedbacks(self):
        """Gera feedbacks detalhados para cada critério"""
        print("\n" + "="*60)
        print("FASE 3: Gerando feedbacks")
        print("="*60)

        for aluno in self.dados:
            self._processar_aluno_feedbacks(aluno)

        print(f"✅ Feedbacks gerados")
        return True
    def aplicar_melhorias(self):
        """Aplica melhorias e ranking"""
        print("\n" + "="*60)
        print("FASE 4: Aplicando melhorias")
        print("="*60)
        
        # Ordenar por nota (decrescente) e nome
        self.dados.sort(key=lambda x: (-x.get('nota_final', 0), x['nome']))
        
        # Adicionar ranking
        for i, aluno in enumerate(self.dados):
            aluno['ranking'] = i + 1
        
        # Calcular estatísticas
        notas = [a['nota_final'] for a in self.dados if a['status'] == 'sucesso']
        if notas:
            self.stats['com_sucesso'] = len([a for a in self.dados if a['status'] == 'sucesso'])
            self.stats['com_erro'] = len([a for a in self.dados if a['status'] != 'sucesso'])
            self.stats['nota_media'] = sum(notas) / len(notas)
            self.stats['maior_nota'] = max(notas)
            self.stats['menor_nota'] = min(notas)
        
        print(f"✅ Melhorias aplicadas")
        return True

    def aplicar_dados_manuais(self):
        """Aplica notas e conteúdos manuais do professor"""
        print("\n" + "="*60)
        print("FASE EXTRA: Aplicando dados manuais")
        print("="*60)
        
        # Carregar notas manuais
        notas_manuais_path = os.path.join(self.resultado_path, ARQUIVO_NOTAS_MANUAIS)
        notas_manuais = {}
        if os.path.exists(notas_manuais_path):
            with open(notas_manuais_path, 'r', encoding='utf-8') as f:
                notas_manuais = json.load(f)
            print(f"📝 {len(notas_manuais)} notas manuais carregadas")
        
        # Carregar conteúdos manuais
        conteudos_manuais_path = os.path.join(self.resultado_path, ARQUIVO_CONTEUDOS_MANUAIS)
        conteudos_manuais = {}
        if os.path.exists(conteudos_manuais_path):
            with open(conteudos_manuais_path, 'r', encoding='utf-8') as f:
                conteudos_manuais = json.load(f)
            print(f"📝 {len(conteudos_manuais)} conteúdos manuais carregadas")
            
        for aluno in self.dados:
            nome = aluno['nome']
            
            # Nota Automática original
            criterios = aluno.get('criterios', {})
            nota_auto = sum(d.get('score', 0) for d in criterios.values())
            aluno['nota_automatica'] = nota_auto
            
            # Aplicar nota manual se existir
            if nome in notas_manuais:
                dados_manuais = notas_manuais[nome]
                aluno['tem_avaliacao_manual'] = True
                aluno['nota_manual'] = dados_manuais.get('nota_final_manual', nota_auto)
                aluno['comentario_professor'] = dados_manuais.get('comentario', '')
                aluno['checklist_manual'] = dados_manuais.get('checklist', {})
                aluno['criterios_manuais'] = dados_manuais.get('criterios', {})
                
                # Mesclar scores manuais nos critérios se existirem
                if aluno['criterios_manuais']:
                    for crit_id, manual_score in aluno['criterios_manuais'].items():
                        if crit_id in aluno.get('criterios', {}):
                            aluno['criterios'][crit_id]['score'] = manual_score
                            aluno['criterios'][crit_id]['is_manual'] = True
                
                aluno['nota_final'] = aluno['nota_manual']
                print(f"✓ {aluno['nome_exibicao']}: Nota Manual {aluno['nota_manual']:.1f}")
            else:
                aluno['tem_avaliacao_manual'] = False
                aluno['checklist_manual'] = {}
                aluno['criterios_manuais'] = {}
                aluno['nota_final'] = nota_auto
                
            # Aplicar conteúdo manual se existir
            if nome in conteudos_manuais:
                c_manuais = conteudos_manuais[nome]
                if 'readme' in c_manuais and c_manuais['readme'].get('conteudo'):
                    aluno['readme_content'] = c_manuais['readme']['conteudo']
                    aluno['manual_readme'] = True
                if 'main_py' in c_manuais and c_manuais['main_py'].get('conteudo'):
                    aluno['main_py_content'] = c_manuais['main_py']['conteudo']
                    aluno['manual_main_py'] = True
                    aluno['main_py_exists'] = True
        
        return True

    def reanalisar_aluno(self, nome_aluno):
        """Reanalisa um aluno específico e retorna os dados atualizados"""
        # Carregar dados atuais
        self.dados = self.load_data()
        aluno = next((a for a in self.dados if a['nome'] == nome_aluno), None)
        
        if not aluno:
            return None
            
        print(f"Reanalisando aluno: {nome_aluno}")
        
        # 1. Aplicar dados manuais primeiro para garantir que o LLM veja o conteúdo atualizado
        self.aplicar_dados_manuais()
        
        # 2. Gerar feedback para este aluno específico
        self._processar_aluno_feedbacks(aluno)
        
        # 3. Recalcular nota final se não houver nota manual
        if not aluno.get('tem_avaliacao_manual'):
            criterios = aluno.get('criterios', {})
            aluno['nota_final'] = sum(d.get('score', 0) for d in criterios.values())
            
        # 4. Salvar estado atualizado
        self.salvar_resultados()
        
        return aluno

    def consolidar_json(self):
        """Consolida dados em JSON para dashboard"""
        print("\n" + "="*60)
        print("FASE 5: Consolidando JSON")
        print("="*60)
        
        # Salvar JSON consolidado
        output_file = os.path.join(self.resultado_path, 'avaliacoes_completas.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.dados, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON consolidado: {output_file}")
        return True
    
    def gerar_dashboard(self):
        """Gera dashboard HTML final com dados embutidos"""
        print("\n" + "="*60)
        print("FASE 6: Gerando dashboard")
        print("="*60)
        
        # Ler template HTML (usar o integrado)
        template_file = os.path.join(self.resultado_path, 'dashboard_integrado.html')
        if not os.path.exists(template_file):
            template_file = os.path.join(self.resultado_path, 'dashboard_completo.html')
            
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
            else:
                html_final_lines.append(line)
        
        html_final = ''.join(html_final_lines)
        
        # Salvar HTML final
        output_file = os.path.join(self.resultado_path, 'dashboard_final.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_final)
        
        print(f"✅ Dashboard gerado: {output_file}")
        print(f"   Tamanho: {len(html_final):,} caracteres")
        print(f"   Número de alunos: {len(self.dados)}")
        return True
    
    def salvar_resultados(self):
        """Salva todos os resultados intermediários"""
        print("\n" + "="*60)
        print("Salvando resultados")
        print("="*60)
        
        # Salvar JSON com melhorias
        output_file = os.path.join(self.resultado_path, 'avaliacoes_melhoradas.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.dados, f, indent=2, ensure_ascii=False)
        print(f"✅ {output_file}")
        
        return True
    
    def _extract_email_from_readme(self, readme_content):
        """Extrai email do README"""
        if not readme_content:
            return None
        
        # Padrão simples para email
        pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        match = re.search(pattern, readme_content, re.IGNORECASE)
        if match:
            return match.group(0)
        
        return None
    
    def _extract_images_from_readme(self, readme_content, repo_url):
        """Extrai URLs de imagens do README"""
        if not readme_content:
            return []
        
        images = []
        patterns = [
            r'!\[.*?\]\((https?://[^\s\)]+)\)',
            r'!\[.*?\]\((https?://github\.com/[^\s\)]+)\)',
            r'<img.*?src="(https?://[^"]+)"'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, readme_content)
            for match in matches:
                if match not in images:
                    images.append(match)
        
        return images
    
    def _detectar_artefatos_ia(self, readme_content, commits, main_py_content):
        """Detecta possíveis artefatos de IA"""
        artefatos = []
        
        if readme_content:
            if len(readme_content) < 500:
                artefatos.append({'tipo': 'README_curto', 'descricao': 'README muito curto', 'severidade': 'baixa'})
        
        if main_py_content:
            if '# Generated code' in main_py_content or '# Este código foi gerado' in main_py_content:
                artefatos.append({'tipo': 'Comentario_IA', 'descricao': 'Código gerado automaticamente', 'severidade': 'media'})
        
        if commits and len(commits) == 1:
            artefatos.append({'tipo': 'Unico_commit', 'descricao': 'Apenas um commit', 'severidade': 'media'})
        
        return artefatos
    
    def _gerar_feedback(self, criterio, score, max_score, aluno):
        """Gera feedback para um critério"""
        percentage = score / max_score if max_score > 0 else 0
        
        feedbacks = {
            'logica_firmware': {
                'high': "Código bem estruturado com lógica clara. Implementa funções/modularização adequada.",
                'medium': "Código funcional mas poderia ser mais organizado. Falta modularização.",
                'low': "Código com problemas de estrutura ou lógica."
            },
            'metrica_wokwi': {
                'high': "Diagrama completo e bem organizado no Wokwi.",
                'medium': "Diagrama funcional mas com organização básica.",
                'low': "Diagrama incompleto ou com problemas."
            },
            'ci_cd': {
                'high': "Pipeline CI/CD bem configurado com GitHub Actions.",
                'medium': "CI/CD configurado mas com limitações.",
                'low': "CI/CD ausente ou mal configurado."
            },
            'documentacao': {
                'high': "Documentação completa e bem estruturada.",
                'medium': "Documentação presente mas incompleta.",
                'low': "Documentação mínima ou ausente."
            },
            'estrutura': {
                'high': "Repositório bem organizado com estrutura clara.",
                'medium': "Estrutura básica presente. Poderia melhorar.",
                'low': "Estrutura desorganizada."
            }
        }
        
        if percentage >= 0.8:
            return feedbacks[criterio]['high']
        elif percentage >= 0.5:
            return feedbacks[criterio]['medium']
        else:
            return feedbacks[criterio]['low']
    
    def executar(self):
        """Executa todo o pipeline"""
        print("="*60)
        print("PIPELINE DE VALIDAÇÃO IOT")
        print("="*60)
        print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Diretório: {self.resultado_path}")
        print("="*60)
        
        # Carregar dados
        if not self.carregar_dados_existentes():
            return False
        
        # Executar fases
        self.extrair_commits()
        self.processar_dados_completos()
        self.gerar_feedbacks()
        self.aplicar_dados_manuais()
        self.aplicar_melhorias()
        self.consolidar_json()
        self.salvar_resultados()
        self.gerar_dashboard()
        
        # Resumo final
        print("\n" + "="*60)
        print("RESUMO FINAL")
        print("="*60)
        print(f"Total de alunos: {self.stats['total_alunos']}")
        print(f"Com sucesso: {self.stats['com_sucesso']}")
        print(f"Com erro: {self.stats['com_erro']}")
        print(f"Nota média: {self.stats['nota_media']:.1f}")
        print(f"Maior nota: {self.stats['maior_nota']:.1f}")
        print(f"Menor nota: {self.stats['menor_nota']:.1f}")
        print(f"\nDashboard: file://{self.resultado_path}/dashboard_final.html")
        print("="*60)
        
        return True


def main():
    pipeline = PipelineValidacao()
    success = pipeline.executar()
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
