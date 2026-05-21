#!/usr/bin/env python3
"""
Script para consolidar avaliações automáticas e manuais
Combina as notas do script com as notas manuais do professor
"""
import json
import os
import sys
from datetime import datetime

RESULTADO_PATH = "/workspace/resultado_validacao"
ARQUIVO_AVALIACOES = "avaliacoes_com_feedback.json"
ARQUIVO_NOTAS_MANUAIS = "notas_manuais.json"
ARQUIVO_CONOLIDADO = "avaliacoes_consolidadas.json"

def carregar_arquivo(nome_arquivo):
    """Carrega um arquivo JSON"""
    caminho = os.path.join(RESULTADO_PATH, nome_arquivo)
    if not os.path.exists(caminho):
        return None
    
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_consolidado(avaliacoes):
    """Salva as avaliações consolidadas"""
    caminho = os.path.join(RESULTADO_PATH, ARQUIVO_CONOLIDADO)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(avaliacoes, f, indent=2, ensure_ascii=False)
    print(f"✅ Avaliações consolidadas salvas em: {caminho}")

def calcular_nota_automatica(criterios):
    """Calcula a nota total automática baseada nos critérios"""
    total = 0
    for criterio, dados in criterios.items():
        total += dados.get('score', 0)
    return total

def consolidar_avaliacoes():
    """Consolida avaliações automáticas e manuais"""
    print("="*80)
    print("CONSOLIDANDO AVALIAÇÕES - AUTOMÁTICO + MANUAL")
    print("="*80)
    
    # Carregar avaliações automáticas
    avaliacoes_auto = carregar_arquivo(ARQUIVO_AVALIACOES)
    if not avaliacoes_auto:
        print(f"❌ Erro: Arquivo {ARQUIVO_AVALIACOES} não encontrado")
        return 1
    
    print(f"\n✅ {len(avaliacoes_auto)} avaliações automáticas carregadas")
    
    # Carregar notas manuais (se existirem)
    notas_manuais = carregar_arquivo(ARQUIVO_NOTAS_MANUAIS)
    if notas_manuais:
        print(f"📝 {len(notas_manuais)} notas manuais encontradas")
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
            aluno_consolidado['nota_manual'] = dados_manuais.get('nota_final_manual', 0)
            aluno_consolidado['comentario_professor'] = dados_manuais.get('comentario', '')
            
            # Calcular diferença
            diferenca = aluno_consolidado['nota_manual'] - nota_auto
            aluno_consolidado['diferenca'] = diferenca
            
            # Nota final: usa a manual se existir, senão usa automática
            aluno_consolidado['nota_final'] = aluno_consolidado['nota_manual']
            
            print(f"✓ {nome}: Auto={nota_auto:.1f}, Manual={aluno_consolidado['nota_manual']:.1f}, Diferença={diferenca:+.1f}")
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
    
    # Estatísticas
    print("\n" + "="*80)
    print("RESUMO DA CONSOLIDAÇÃO")
    print("="*80)
    
    com_manual = sum(1 for a in avaliacoes_consolidadas if a.get('tem_avaliacao_manual'))
    sem_manual = len(avaliacoes_consolidadas) - com_manual
    
    print(f"Total de alunos: {len(avaliacoes_consolidadas)}")
    print(f"Com avaliação manual: {com_manual}")
    print(f"Sem avaliação manual: {sem_manual}")
    
    if com_manual > 0:
        diffs = [a['diferenca'] for a in avaliacoes_consolidadas if a.get('diferenca') is not None]
        media_diferenca = sum(diffs) / len(diffs)
        max_diferenca = max(diffs)
        min_diferenca = min(diffs)
        
        print(f"\nEstatísticas das diferenças (Manual - Automática):")
        print(f"  Média: {media_diferenca:+.2f}")
        print(f"  Máxima: {max_diferenca:+.2f}")
        print(f"  Mínima: {min_diferenca:+.2f}")
    
    # Calcular novas estatísticas de notas
    notas_finais = [a['nota_final'] for a in avaliacoes_consolidadas]
    notas_auto = [a['nota_automatica'] for a in avaliacoes_consolidadas]
    
    print(f"\nNotas Finais (com manual quando disponível):")
    print(f"  Média: {sum(notas_finais)/len(notas_finais):.2f}")
    print(f"  Máxima: {max(notas_finais):.2f}")
    print(f"  Mínima: {min(notas_finais):.2f}")
    
    print(f"\nNotas Automáticas (todas):")
    print(f"  Média: {sum(notas_auto)/len(notas_auto):.2f}")
    print(f"  Máxima: {max(notas_auto):.2f}")
    print(f"  Mínima: {min(notas_auto):.2f}")
    
    return 0

def gerar_relatorio_comparativo():
    """Gera relatório comparativo entre notas automáticas e manuais"""
    avaliacoes = carregar_arquivo(ARQUIVO_CONOLIDADO)
    if not avaliacoes:
        print("❌ Sem avaliações consolidadas. Execute a consolidação primeiro.")
        return
    
    # Filtrar apenas os que têm avaliação manual
    com_manual = [a for a in avaliacoes if a.get('tem_avaliacao_manual')]
    
    if not com_manual:
        print("⚠️  Nenhuma avaliação manual encontrada.")
        return
    
    print("\n" + "="*80)
    print("RELATÓRIO COMPARATIVO - NOTAS AUTOMÁTICAS vs MANUAIS")
    print("="*80)
    
    # Ordenar por diferença (maior divergência primeiro)
    com_manual_sorted = sorted(com_manual, key=lambda x: abs(x.get('diferenca', 0)), reverse=True)
    
    print(f"\nAlunos com maior divergência entre avaliação automática e manual:")
    print("-" * 80)
    
    for aluno in com_manual_sorted[:10]:  # Top 10 divergências
        nome = aluno.get('nome', 'Desconhecido')
        auto = aluno.get('nota_automatica', 0)
        manual = aluno.get('nota_manual', 0)
        diff = aluno.get('diferenca', 0)
        comentario = aluno.get('comentario_professor', '')
        
        print(f"\n{nome}:")
        print(f"  Automática: {auto:.1f}")
        print(f"  Manual: {manual:.1f}")
        print(f"  Diferença: {diff:+.1f}")
        if comentario:
            print(f"  Comentário: {comentario}")
    
    # Salvar relatório em arquivo
    relatorio_path = os.path.join(RESULTADO_PATH, "relatorio_comparativo.txt")
    with open(relatorio_path, 'w', encoding='utf-8') as f:
        f.write("RELATÓRIO COMPARATIVO - NOTAS AUTOMÁTICAS vs MANUAIS\n")
        f.write("="*80 + "\n\n")
        f.write(f"Total de alunos com avaliação manual: {len(com_manual)}\n\n")
        
        for aluno in com_manual_sorted:
            nome = aluno.get('nome', 'Desconhecido')
            auto = aluno.get('nota_automatica', 0)
            manual = aluno.get('nota_manual', 0)
            diff = aluno.get('diferenca', 0)
            comentario = aluno.get('comentario_professor', '')
            
            f.write(f"{nome}:\n")
            f.write(f"  Automática: {auto:.1f}\n")
            f.write(f"  Manual: {manual:.1f}\n")
            f.write(f"  Diferença: {diff:+.1f}\n")
            if comentario:
                f.write(f"  Comentário: {comentario}\n")
            f.write("\n")
    
    print(f"\n✅ Relatório salvo em: {relatorio_path}")

def main():
    print("="*80)
    print("CONSOLIDADOR DE AVALIAÇÕES - IOT")
    print("="*80)
    
    # Executar consolidação
    resultado = consolidar_avaliacoes()
    
    if resultado == 0:
        # Gerar relatório comparativo
        gerar_relatorio_comparativo()
        
        print("\n" + "="*80)
        print("PRÓXIMOS PASSOS")
        print("="*80)
        print("1. Execute 'adicionar_notas_manuais.py' para adicionar notas manuais")
        print("2. Execute este script novamente para atualizar consolidação")
        print("3. Execute 'gerar_dashboard_final.py' para visualizar resultados")
        print("="*80)
    
    return resultado

if __name__ == '__main__':
    sys.exit(main())
