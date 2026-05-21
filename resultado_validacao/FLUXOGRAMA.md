# 🔄 Fluxograma do Sistema de Avaliação

## Visão Geral do Processo

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIPELINE DE AVALIAÇÃO IOT                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │  1. pipeline Automático (00_run_all.py) │
         │     - Extrai commits                    │
         │     - Processa dados                    │
         │     - Gera feedback LLM                 │
         │     - Cria dashboard                    │
         └────────────────────────────────────────┘
                              │
                              ▼
    ┌───────────────────────────────────────────────────┐
    │        SAÍDA: avaliacoes_com_feedback.json        │
    │        (Avaliação Automática - Script)            │
    └───────────────────────────────────────────────────┘
                    │                    │
                    │                    │
        ┌───────────┘                    └───────────┐
        │                                            │
        ▼                                            ▼
┌──────────────────┐                      ┌──────────────────┐
│  MODO A:         │                      │  MODO B:         │
│  Apenas          │                      │  Híbrido         │
│  Automático      │                      │  (Auto + Manual) │
└──────────────────┘                      └──────────────────┘
        │                                            │
        │                                            ▼
        │                          ┌─────────────────────────────┐
        │                          │ 2. Inserir Avaliação Manual │
        │                          │    (adicionar_notas_        │
        │                          │     manuais.py)             │
        │                          │    - Nota do professor      │
        │                          │    - Comentários            │
        │                          └─────────────────────────────┘
        │                                            │
        │                                            ▼
        │                          ┌─────────────────────────────┐
        │                          │ 3. (Opcional) Conteúdo      │
        │                          │    Manual                   │
        │                          │    (inserir_conteudo_       │
        │                          │     manual.py)              │
        │                          │    - README                 │
        │                          │    - main.py                │
        │                          │    - diagram.json           │
        │                          └─────────────────────────────┘
        │                                            │
        ▼                                            ▼
┌───────────────────────────────────────────────────────────────┐
│                    CONSOLIDAÇÃO                                │
│            (consolidar_avaliacoes.py)                         │
│                                                               │
│  - Carrega avaliação automática                               │
│  - Carrega avaliação manual (se existir)                      │
│  - Combina as duas fontes                                     │
│  - Calcula diferenças                                         │
│  - Gera relatório comparativo                                 │
└───────────────────────────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │     SAÍDA: avaliacoes_consolidadas.json │
         │     - nota_automatica                   │
         │     - nota_manual (opcional)            │
         │     - nota_final (usa manual se existir)│
         │     - diferenca                         │
         │     - comentario_professor              │
         └────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │  4. Dashboard Final                    │
         │     (gerar_dashboard_final.py)         │
         └────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │     dashboard_final.html               │
         │     (Visualização dos resultados)      │
         └────────────────────────────────────────┘
```

---

## Detalhe: Inserção de Notas Manuais

```
┌─────────────────────────────────────────────────────────────┐
│  ADICIONAR NOTAS MANUAIS (adicionar_notas_manuais.py)      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────┐
         │  Carrega: avaliacoes_com_feedback.json │
         └────────────────────────────────────┘
                              │
                              ▼
    ┌───────────────────────────────────────────┐
    │  Escolha o Modo:                          │
    │  ┌────────────────┐  ┌────────────────┐   │
    │  │ 1. Interativo  │  │ 2. Planilha    │   │
    │  │    (um a um)   │  │    CSV         │   │
    │  └────────────────┘  └────────────────┘   │
    └───────────────────────────────────────────┘
                    │                    │
                    │                    │
    ┌───────────────┘                    └──────────────┐
    │                                                   │
    ▼                                                   ▼
┌─────────────────────┐                     ┌──────────────────┐
│ Modo Interativo:    │                     │ Modo Planilha:   │
│ - Lista alunos      │                     │ - Gera CSV       │
│ - Professor digita  │                     │ - Preenche fora  │
│   nota (0-100)      │                     │ - (futuro)       │
│ - Adiciona comentário                      │
└─────────────────────┘                     └──────────────────┘
                    │
                    ▼
         ┌─────────────────────────────┐
         │  Salva em:                  │
         │  notas_manuais.json         │
         │                             │
         │  Estrutura:                 │
         │  {                          │
         │    "Nome Aluno": {          │
         │      "nota_final_manual":92│
         │      "comentario": "...",  │
         │      "data": "2026-..."    │
         │    }                        │
         │  }                          │
         └─────────────────────────────┘
```

---

## Detalhe: Inserção de Conteúdo Manual

```
┌─────────────────────────────────────────────────────────────┐
│  INSERIR CONTEÚDO MANUAL (inserir_conteudo_manual.py)      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────┐
         │  Escolha o Tipo de Conteúdo:       │
         │  1. README.md                       │
         │  2. main.py (código)                │
         │  3. diagram.json (Wokwi)            │
         │  4. Outro arquivo                   │
         │  5. Importar de arquivo             │
         └────────────────────────────────────┘
                              │
                              ▼
    ┌───────────────────────────────────────────┐
    │  Método de Entrada:                       │
    │  ┌─────────────────┐  ┌──────────────┐   │
    │  │ Digitar/Colar   │  │ Importar de  │   │
    │  │ (terminal)      │  │ arquivo      │   │
    │  └─────────────────┘  └──────────────┘   │
    └───────────────────────────────────────────┘
                    │
                    ▼
         ┌─────────────────────────────┐
         │  Salva em:                  │
         │  conteudos_manuais.json     │
         │                             │
         │  Estrutura:                 │
         │  {                          │
         │    "Nome Aluno": {          │
         │      "readme": {            │
         │        "conteudo": "...",  │
         │        "tamanho": 1234,    │
         │        "data": "..."       │
         │      }                      │
         │    }                        │
         │  }                          │
         └─────────────────────────────┘
```

---

## Detalhe: Consolidação

```
┌─────────────────────────────────────────────────────────────┐
│  CONSOLIDAR AVALIAÇÕES (consolidar_avaliacoes.py)          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
    ┌───────────────────────────────────────────┐
    │  1. Carrega: avaliacoes_com_feedback.json │
    │     (avaliação automática)                │
    └───────────────────────────────────────────┘
                              │
                              ▼
    ┌───────────────────────────────────────────┐
    │  2. Carrega: notas_manuais.json           │
    │     (avaliação manual, se existir)        │
    └───────────────────────────────────────────┘
                              │
                              ▼
    ┌───────────────────────────────────────────┐
    │  3. Para cada aluno:                      │
    │     - Se tem nota manual:                 │
    │         nota_final = nota_manual          │
    │     - Senão:                              │
    │         nota_final = nota_automatica      │
    │     - Calcula diferença                   │
    │     - Adiciona comentário (se existir)    │
    └───────────────────────────────────────────┘
                              │
                              ▼
    ┌───────────────────────────────────────────┐
    │  4. Gera:                                 │
    │     - avaliacoes_consolidadas.json        │
    │     - relatorio_comparativo.txt           │
    │                                           │
    │  Estrutura consolidada:                   │
    │  {                                        │
    │    "nome": "...",                        │
    │    "nota_automatica": 89.5,              │
    │    "nota_manual": 92.0,                  │
    │    "nota_final": 92.0,                   │
    │    "diferenca": +2.5,                    │
    │    "tem_avaliacao_manual": true,         │
    │    "comentario_professor": "..."         │
    │  }                                        │
    └───────────────────────────────────────────┘
                              │
                              ▼
    ┌───────────────────────────────────────────┐
    │  5. Estatísticas:                         │
    │     - Total de alunos                     │
    │     - Com avaliação manual                │
    │     - Sem avaliação manual                │
    │     - Média das diferenças                │
    │     - Máxima/Mínima diferença             │
    └───────────────────────────────────────────┘
```

---

## Comparação: Antes vs Depois

### ANTES (Apenas Automático)

```
┌─────────────────────────────────────┐
│  Script Automático                  │
│  - Analisa repositório              │
│  - Atribui nota: 89.5               │
│  - Gera feedback                    │
└─────────────────────────────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │  NOTA FINAL: 89.5       │
    │  (sem intervenção)      │
    └─────────────────────────┘
```

### DEPOIS (Híbrido: Auto + Manual)

```
┌─────────────────────────────────────┐
│  Script Automático                  │
│  - Analisa repositório              │
│  - Atribui nota: 89.5               │
└─────────────────────────────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │  NOTA AUTOMÁTICA: 89.5  │
    └─────────────────────────┘
                 │
                 ▼
    ┌─────────────────────────────────────┐
    │  Professor Avalia Manualmente       │
    │  - Revisa projeto                   │
    │  - Considera contexto               │
    │  - Atribui nota: 92.0               │
    │  - Adiciona comentário              │
    └─────────────────────────────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │  NOTA MANUAL: 92.0      │
    │  Comentário: "Excel..." │
    └─────────────────────────┘
                 │
                 ▼
    ┌─────────────────────────────────────┐
    │  Consolidação                       │
    │  - nota_automatica: 89.5            │
    │  - nota_manual: 92.0                │
    │  - diferenca: +2.5                  │
    │  - usa nota_manual como final       │
    └─────────────────────────────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │  NOTA FINAL: 92.0       │
    │  (com justificativa)    │
    └─────────────────────────┘
```

---

## Vantagens do Sistema Híbrido

```
┌────────────────────────────────────────────────────────────┐
│  VANTAGENS                                                 │
├────────────────────────────────────────────────────────────┤
│  ✓ Flexibilidade: professor pode ajustar notas            │
│  ✓ Transparência: mantém ambas as notas                   │
│  ✓ Rastreabilidade: histórico completo                    │
│  ✓ Contexto: considera fatores não automáticos            │
│  ✓ Qualidade: combina velocidade + julgamento humano     │
│  ✓ Comparação: vê diferenças entre auto e manual          │
│  ✓ Feedback: comentários do professor                     │
└────────────────────────────────────────────────────────────┘
```

---

## Exemplo de Resultado Consolidado

```json
{
  "nome": "Maria Madalena Silva_203",
  "email": "maria.madalena.silva_203@aluno.com",
  "github_url": "https://github.com/...",
  
  "nota_automatica": 89.5,
  "nota_manual": 92.0,
  "nota_final": 92.0,
  "diferenca": 2.5,
  
  "tem_avaliacao_manual": true,
  "comentario_professor": "Excelente trabalho, demonstrou ótimo domínio do conteúdo. Ponto de melhoria: CI/CD.",
  
  "criterios": {
    "logica_firmware": {"score": 27, ...},
    "metrica_wokwi": {"score": 20, ...},
    "ci_cd": {"score": 20, ...},
    "documentacao": {"score": 10, ...},
    "estrutura": {"score": 8, ...}
  }
}
```

---

**Fluxograma criado em:** 2026-05-20
**Versão:** 1.0
