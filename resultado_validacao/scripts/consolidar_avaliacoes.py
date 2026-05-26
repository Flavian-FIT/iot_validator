#!/usr/bin/env python3
"""
Script para consolidar avaliações automáticas e manuais
Combina as notas do script com as notas manuais dos professores (média)
"""
import json
import os
import sys
from datetime import datetime

# Adicionar o diretório raiz ao path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from config import RESULTADO_PATH
except ImportError:
    RESULTADO_PATH = "/workspace/resultado_validacao"

ARQUIVO_AVALIACOES = "avaliacoes_com_feedback.json"
ARQUIVO_NOTAS_MANUAIS = "data/notas_manuais.json"
ARQUIVO_CONSOLIDADO = "data/avaliacoes_consolidadas.json"

def carregar_arquivo(nome_arquivo):
    """Carrega um arquivo JSON"""
    caminho = os.path.join(RESULTADO_PATH, nome_arquivo)
    if not os.path.exists(caminho):
        # Tentar sem o prefixo data se falhar
        if "data/" in nome_arquivo:
            caminho = os.path.join(RESULTADO_PATH, nome_arquivo.replace("data/", ""))
            if not os.path.exists(caminho):
                return None
        else:
            return None
    
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_consolidado(avaliacoes):
    """Salva as avaliações consolidadas"""
    caminho = os.path.join(RESULTADO_PATH, ARQUIVO_CONSOLIDADO)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(avaliacoes, f, indent=2, ensure_ascii=False)
    print(f"✅ Avaliações consolidadas salvas em: {caminho}")

def calcular_nota_automatica(criterios):
    """Calcula a nota total automática baseada nos critérios"""
    total = 0
    if isinstance(criterios, dict):
        for criterio, dados in criterios.items():
            if isinstance(dados, dict):
                total += dados.get('score', 0)
            else:
                total += dados # Caso seja apenas o valor
    return total

def consolidar_avaliacoes():
    """Consolida avaliações automáticas e manuais"""
    print("="*80)
    print("CONSOLIDANDO AVALIAÇÕES - AUTOMÁTICO + MÉDIA DOS PROFESSORES")
    print("="*80)
    
    # Carregar avaliações automáticas
    avaliacoes_auto = carregar_arquivo(ARQUIVO_AVALIACOES)
    if not avaliacoes_auto:
        # Tentar avaliacoes.json
        avaliacoes_auto = carregar_arquivo("data/avaliacoes.json")
        if not avaliacoes_auto:
            print(f"❌ Erro: Arquivo de avaliações automáticas não encontrado")
            return 1
    
    print(f"\n✅ {len(avaliacoes_auto)} avaliações automáticas carregadas")
    
    # Carregar notas manuais (se existirem)
    notas_manuais = carregar_arquivo(ARQUIVO_NOTAS_MANUAIS)
    if notas_manuais:
        print(f"📝 {len(notas_manuais)} registros de notas manuais encontrados")
    else:
        print("⚠️  Nenhuma nota manual encontrada. Usando apenas avaliação automática.")
        notas_manuais = {}
    
    # Consolidar
    avaliacoes_consolidadas = []
    
    for aluno in avaliacoes_auto:
        nome = aluno.get('nome', '')
        
        # Criar cópia do aluno
        aluno_consolidado = aluno.copy()
        
        # Adicionar dados de consolidação
        aluno_consolidado['data_consolidacao'] = datetime.now().isoformat()
        
        # Calcular nota automática
        criterios = aluno.get('criterios', {})
        nota_auto = calcular_nota_automatica(criterios)
        aluno_consolidado['nota_automatica'] = nota_auto
        
        # Verificar se tem nota manual
        if nome in notas_manuais:
            dados_manuais = notas_manuais[nome]
            aluno_consolidado['tem_avaliacao_manual'] = True
            
            # Suporte ao novo formato (avaliacoes_professores) e ao antigo
            if 'avaliacoes_professores' in dados_manuais:
                # Filtrar professores que realmente avaliaram (evitar média com zeros indevidos)
                profs_validos = {p: av for p, av in dados_manuais['avaliacoes_professores'].items() 
                                 if av.get('nota_total', 0) > 0 or any(c.get('observacao', '').strip() for c in av.get('criterios', {}).values())}
                
                if profs_validos:
                    notas_finais = [av['nota_total'] for av in profs_validos.values()]
                    aluno_consolidado['nota_manual'] = sum(notas_finais) / len(notas_finais)
                    aluno_consolidado['avaliacoes_professores'] = profs_validos
                    aluno_consolidado['comentario_professor'] = f"Média de {len(profs_validos)} professores"
                else:
                    aluno_consolidado['nota_manual'] = dados_manuais.get('nota_final_manual', 0)
                    aluno_consolidado['comentario_professor'] = dados_manuais.get('comentario', '')
            else:
                # Formato antigo
                aluno_consolidado['nota_manual'] = dados_manuais.get('nota_final_manual', 0)
                aluno_consolidado['comentario_professor'] = dados_manuais.get('comentario', '')
            
            # Calcular diferença
            diferenca = aluno_consolidado['nota_manual'] - nota_auto
            aluno_consolidado['diferenca'] = diferenca
            
            # Nota final: usa a manual se existir, senão usa automática
            aluno_consolidado['nota_final'] = aluno_consolidado['nota_manual']
            
            n_profs = len(aluno_consolidado.get('avaliacoes_professores', {})) if 'avaliacoes_professores' in aluno_consolidado else 1
            print(f"✓ {nome}: Auto={nota_auto:.1f}, Manual(Média)={aluno_consolidado['nota_manual']:.1f} ({n_profs} profs)")
        else:
            aluno_consolidado['tem_avaliacao_manual'] = False
            aluno_consolidado['nota_manual'] = None
            aluno_consolidado['comentario_professor'] = None
            aluno_consolidado['diferenca'] = None
            aluno_consolidado['nota_final'] = nota_auto
            
            print(f"  {nome}: Auto={nota_auto:.1f} (sem avaliação manual)")
        
        avaliacoes_consolidadas.append(aluno_consolidado)
    
    # Salvar consolidado
    salvar_consolidado(avaliacoes_consolidadas)
    
    return 0

def main():
    resultado = consolidar_avaliacoes()
    return resultado

if __name__ == '__main__':
    sys.exit(main())
