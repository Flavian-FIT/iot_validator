#!/usr/bin/env python3
"""
Script para adicionar notas manuais do professor
Permite inserir notas manualmente para cada aluno e combinar com avaliação automática
Suporta múltiplos professores e avaliação por critério
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Adicionar o diretório raiz ao path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from config import RESULTADO_PATH, PROFESSORES, CRITERIOS
except ImportError:
    RESULTADO_PATH = "/workspace/resultado_validacao"
    PROFESSORES = ["Professor 1", "Professor 2", "Professor 3"]
    CRITERIOS = {
        'logica_firmware': {'peso': 30, 'descricao': 'Lógica do Firmware'},
        'metrica_wokwi': {'peso': 20, 'descricao': 'Métrica/Wokwi'},
        'ci_cd': {'peso': 25, 'descricao': 'CI/CD'},
        'documentacao': {'peso': 10, 'descricao': 'Documentação'},
        'estrutura': {'peso': 10, 'descricao': 'Estrutura/Versionamento'}
    }

ARQUIVO_AVALIACOES = "avaliacoes_com_feedback.json"
ARQUIVO_NOTAS_MANUAIS = "data/notas_manuais.json"

def carregar_avaliacoes():
    """Carrega as avaliações automáticas existentes"""
    caminho = os.path.join(RESULTADO_PATH, ARQUIVO_AVALIACOES)
    if not os.path.exists(caminho):
        # Tentar na pasta data
        caminho = os.path.join(RESULTADO_PATH, "data", "avaliacoes.json")
        if not os.path.exists(caminho):
            print(f"❌ Arquivo não encontrado: {caminho}")
            return None
    
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_ou_criar_notas_manuais():
    """Carrega notas manuais existentes ou cria estrutura vazia"""
    caminho = os.path.join(RESULTADO_PATH, ARQUIVO_NOTAS_MANUAIS)
    
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # Criar estrutura vazia
    return {}

def salvar_notas_manuais(notas_manuais):
    """Salva as notas manuais no arquivo"""
    caminho = os.path.join(RESULTADO_PATH, ARQUIVO_NOTAS_MANUAIS)
    # Garantir que o diretório existe
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(notas_manuais, f, indent=2, ensure_ascii=False)
    print(f"✅ Notas salvas em: {caminho}")

def listar_alunos(avaliacoes):
    """Lista todos os alunos com seus índices"""
    print("\n" + "="*80)
    print("LISTA DE ALUNOS")
    print("="*80)
    
    for i, aluno in enumerate(avaliacoes, 1):
        nome = aluno.get('nome', 'Desconhecido')
        nota_auto = aluno.get('nota_final', 0)
        print(f"{i:3d}. {nome} (Nota Automática: {nota_auto:.1f})")
    
    return len(avaliacoes)

def selecionar_professor():
    """Permite selecionar um professor da lista"""
    print("\n" + "="*80)
    print("SELECIONE O PROFESSOR")
    print("="*80)
    for i, prof in enumerate(PROFESSORES, 1):
        print(f"{i}. {prof}")
    
    while True:
        try:
            escolha = input("\nProfessor (número): ").strip()
            idx = int(escolha) - 1
            if 0 <= idx < len(PROFESSORES):
                return PROFESSORES[idx]
            else:
                print(f"❌ Escolha entre 1 e {len(PROFESSORES)}")
        except ValueError:
            print("❌ Entrada inválida. Digite o número do professor.")

def calcular_media_aluno(dados_aluno):
    """Calcula a média das notas dos professores para um aluno"""
    if 'avaliacoes_professores' not in dados_aluno or not dados_aluno['avaliacoes_professores']:
        return 0
    
    notas = [av['nota_total'] for av in dados_aluno['avaliacoes_professores'].values()]
    return sum(notas) / len(notas)

def modo_interativo(avaliacoes, notas_manuais):
    """Modo interativo para adicionar notas manualmente"""
    professor_atual = selecionar_professor()
    print(f"\n👨‍🏫 Avaliando como: {professor_atual}")
    
    print("\n" + "="*80)
    print("MODO INTERATIVO - ADICIONAR NOTAS MANUAIS")
    print("="*80)
    print("\nComandos:")
    print("  - Digite o número do aluno para avaliar")
    print("  - 'p' para trocar de professor")
    print("  - 'l' para listar alunos")
    print("  - 'v' para visualizar avaliações salvas")
    print("  - 's' para salvar e sair")
    print("  - 'q' para sair sem salvar")
    print("="*80)
    
    while True:
        entrada = input(f"\n[{professor_atual}] Aluno (número), comando (p/l/v/s/q): ").strip().lower()
        
        if entrada == 'q':
            confirm = input("Deseja sair sem salvar? (s/n): ").strip().lower()
            if confirm == 's':
                return False
            
        elif entrada == 'p':
            professor_atual = selecionar_professor()
            print(f"👨‍🏫 Professor alterado para: {professor_atual}")
            
        elif entrada == 'l':
            listar_alunos(avaliacoes)
            
        elif entrada == 'v':
            if not notas_manuais:
                print("Nenhuma avaliação manual salva ainda.")
            else:
                print(f"\nAvaliações manuais salvas: {len(notas_manuais)}")
                for nome, dados in notas_manuais.items():
                    n_profs = len(dados.get('avaliacoes_professores', {}))
                    nota_media = dados.get('nota_final_manual', 0)
                    print(f"  - {nome}: Média = {nota_media:.1f} ({n_profs} professores)")
                    
        elif entrada == 's':
            if notas_manuais:
                salvar_notas_manuais(notas_manuais)
                print(f"✅ {len(notas_manuais)} avaliações manuais salvas!")
            return True
            
        elif entrada.isdigit():
            idx = int(entrada) - 1
            if 0 <= idx < len(avaliacoes):
                aluno = avaliacoes[idx]
                nome = aluno.get('nome', 'Desconhecido')
                print(f"\n{'='*80}")
                print(f"Avaliando: {nome}")
                print(f"Professor: {professor_atual}")
                print(f"{'='*80}")
                
                # Inicializar estrutura se não existir
                if nome not in notas_manuais:
                    notas_manuais[nome] = {
                        'avaliacoes_professores': {},
                        'nota_final_manual': 0,
                        'comentario': "Média das avaliações dos professores"
                    }
                
                if 'avaliacoes_professores' not in notas_manuais[nome]:
                    notas_manuais[nome]['avaliacoes_professores'] = {}

                # Coletar notas por critério
                av_prof = {
                    'criterios': {},
                    'nota_total': 0,
                    'data_avaliacao': datetime.now().isoformat()
                }
                
                nota_total = 0
                for crit_id, crit_info in CRITERIOS.items():
                    print(f"\nCritério: {crit_info['descricao']} (Peso máx: {crit_info['peso']})")
                    
                    # Nota
                    while True:
                        try:
                            nota_str = input(f"  Nota (0-{crit_info['peso']}): ").strip()
                            if nota_str == '': nota = 0
                            else: nota = float(nota_str)
                            
                            if 0 <= nota <= crit_info['peso']:
                                break
                            else:
                                print(f"  ❌ Nota deve estar entre 0 e {crit_info['peso']}")
                        except ValueError:
                            print("  ❌ Valor inválido!")
                    
                    # Observação
                    obs = input(f"  Observação sobre {crit_info['descricao']}: ").strip()
                    
                    av_prof['criterios'][crit_id] = {
                        'nota': nota,
                        'observacao': obs
                    }
                    nota_total += nota
                
                av_prof['nota_total'] = nota_total
                
                # Salvar avaliação deste professor
                notas_manuais[nome]['avaliacoes_professores'][professor_atual] = av_prof
                
                # Recalcular média final do aluno
                notas_manuais[nome]['nota_final_manual'] = calcular_media_aluno(notas_manuais[nome])
                
                print(f"\n✅ Avaliação de {professor_atual} salva para {nome}!")
                print(f"   Nota Total do Professor: {nota_total:.1f}/100")
                print(f"   Nova Média do Aluno: {notas_manuais[nome]['nota_final_manual']:.1f}")
                
            else:
                print(f"❌ Índice inválido! Digite um número entre 1 e {len(avaliacoes)}")
        else:
            print("Comando não reconhecido. Use 'p', 'l', 'v', 's', 'q' ou um número.")

def main():
    print("="*80)
    print("SISTEMA DE AVALIAÇÃO MANUAL MULTI-PROFESSOR - IOT")
    print("="*80)
    
    # Carregar avaliações automáticas
    avaliacoes = carregar_avaliacoes()
    if not avaliacoes:
        return 1
    
    print(f"\n✅ {len(avaliacoes)} alunos carregados")
    
    # Carregar ou criar notas manuais
    notas_manuais = carregar_ou_criar_notas_manuais()
    if notas_manuais:
        print(f"📝 {len(notas_manuais)} alunos já possuem alguma avaliação manual")
    
    # Listar alunos
    total = listar_alunos(avaliacoes)
    
    # Executar modo interativo por padrão (já que é o principal uso agora)
    sucesso = modo_interativo(avaliacoes, notas_manuais)
    if sucesso and notas_manuais:
        salvar_notas_manuais(notas_manuais)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
