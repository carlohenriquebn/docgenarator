"""
═══════════════════════════════════════════════════════════════════════════════
                    FLUXOGRAMA - BUSCA RECURSIVA COM LANGCHAIN
═══════════════════════════════════════════════════════════════════════════════

Este arquivo explica visualmente como funciona cada tipo de busca recursiva.

═══════════════════════════════════════════════════════════════════════════════
1. RECURSIVE SEARCH (Refinamento Iterativo)
═══════════════════════════════════════════════════════════════════════════════

    ┌─────────────────────────────────────────────────────────────┐
    │ INÍCIO: Usuário envia perfil + pergunta                     │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ ITERAÇÃO 1: Gera resposta inicial                           │
    │ - LLM processa pergunta original                            │
    │ - Retorna primeira resposta                                 │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ AVALIAÇÃO DE QUALIDADE                                       │
    │ - Analisa completude (0-10)                                 │
    │ - Identifica aspectos faltantes                             │
    │ - Gera score de qualidade                                   │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────┴────────┐
                    │ Score >= 8.0?   │
                    │ ou max_iter?    │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                  SIM               NÃO
                    │                 │
                    │                 ▼
                    │   ┌─────────────────────────────────────────┐
                    │   │ REFINAMENTO                             │
                    │   │ - Analisa gaps na resposta              │
                    │   │ - Gera perguntas de refinamento         │
                    │   │ - Cria nova query focada                │
                    │   └──────────────┬──────────────────────────┘
                    │                  │
                    │                  ▼
                    │   ┌─────────────────────────────────────────┐
                    │   │ ITERAÇÃO N: Gera resposta refinada      │
                    │   │ - Usa contexto da iteração anterior     │
                    │   │ - Foca nos aspectos identificados       │
                    │   └──────────────┬──────────────────────────┘
                    │                  │
                    │                  └──────► VOLTA PARA AVALIAÇÃO
                    │
                    ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ FIM: Retorna melhor resposta + métricas                     │
    │ - Resposta final                                            │
    │ - Score de qualidade                                        │
    │ - Histórico de iterações                                    │
    └─────────────────────────────────────────────────────────────┘


EXEMPLO PRÁTICO:

Iteração 1:
  Query: "Quais as melhores seguradoras?"
  Resposta: "Porto Seguro, Itaú e SulAmérica são boas opções..."
  Score: 6.5/10
  Faltando: Comparação de preços, coberturas específicas

Iteração 2:
  Query: "Considerando sua resposta, detalhe mais sobre preços e coberturas..."
  Resposta: "Porto Seguro oferece cobertura compreensiva por R$2.500/ano..."
  Score: 8.5/10
  Faltando: []

RESULTADO: Score 8.5 >= 8.0 → PARA e retorna resposta da Iteração 2


═══════════════════════════════════════════════════════════════════════════════
2. SELF-ASK (Auto-Questionamento)
═══════════════════════════════════════════════════════════════════════════════

    ┌─────────────────────────────────────────────────────────────┐
    │ INÍCIO: Usuário envia perfil + pergunta principal           │
    │ Ex: "Qual a melhor seguradora para mim?"                    │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ FASE 1: DECOMPOSIÇÃO                                         │
    │ LLM analisa a pergunta e gera perguntas intermediárias      │
    │                                                              │
    │ Pergunta 1: "Qual o perfil de risco deste usuário?"        │
    │ Pergunta 2: "Quais seguradoras atuam em São Paulo?"        │
    │ Pergunta 3: "Qual o preço médio para este perfil?"         │
    │ Pergunta 4: "Qual tem melhor atendimento?"                 │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ FASE 2: RESPONDE PERGUNTA 1                                 │
    │ "Usuário tem perfil de BAIXO risco porque..."              │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ FASE 2: RESPONDE PERGUNTA 2                                 │
    │ "Em SP atuam: Porto Seguro, Itaú, SulAmérica..."          │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ FASE 2: RESPONDE PERGUNTA 3                                 │
    │ "Preço médio: R$ 2.000-3.000/ano..."                       │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ FASE 2: RESPONDE PERGUNTA 4                                 │
    │ "Porto Seguro tem melhor NPS..."                            │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ FASE 3: SÍNTESE                                              │
    │ Combina todas as respostas intermediárias em uma            │
    │ resposta final coesa e estruturada                          │
    │                                                              │
    │ "Baseado na análise do seu perfil de BAIXO risco,          │
    │  e considerando as seguradoras que atuam em SP,             │
    │  com preços entre R$ 2.000-3.000/ano,                       │
    │  recomendo Porto Seguro pelo melhor atendimento..."         │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ FIM: Retorna síntese + perguntas intermediárias             │
    └─────────────────────────────────────────────────────────────┘


VANTAGEM: Raciocínio explícito e estruturado


═══════════════════════════════════════════════════════════════════════════════
3. MULTI-PERSPECTIVE (Múltiplas Perspectivas)
═══════════════════════════════════════════════════════════════════════════════

    ┌─────────────────────────────────────────────────────────────┐
    │ INÍCIO: Usuário envia perfil + pergunta                     │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ DEFINE 5 PERSPECTIVAS DIFERENTES                            │
    │ 1. Custo-benefício e economia                               │
    │ 2. Qualidade de atendimento e satisfação                    │
    │ 3. Abrangência de cobertura e proteção                      │
    │ 4. Facilidade de contratação e burocracia                   │
    │ 5. Reputação e confiabilidade no mercado                    │
    └────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    │ PARALELO        │
                    │ (Conceitualmente)│
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
    ┌─────────┐        ┌─────────┐        ┌─────────┐
    │ ANÁLISE │        │ ANÁLISE │        │ ANÁLISE │
    │ PERSP 1 │        │ PERSP 2 │        │ PERSP 3 │
    │         │        │         │        │         │
    │ Foco em │        │ Foco em │        │ Foco em │
    │ CUSTO   │        │ ATEND.  │        │ COBERT. │
    └────┬────┘        └────┬────┘        └────┬────┘
         │                  │                   │
         │         ▼                   ▼        │
         │    ┌─────────┐        ┌─────────┐   │
         │    │ ANÁLISE │        │ ANÁLISE │   │
         │    │ PERSP 4 │        │ PERSP 5 │   │
         │    │         │        │         │   │
         │    │ Foco em │        │ Foco em │   │
         │    │ FACILID.│        │ REPUTAÇ.│   │
         │    └────┬────┘        └────┬────┘   │
         │         │                  │         │
         └─────────┴──────────┬───────┴─────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ SÍNTESE FINAL                                                │
    │                                                              │
    │ Integra todas as 5 perspectivas em uma resposta            │
    │ equilibrada que considera:                                  │
    │ - Prós e contras de cada seguradora                        │
    │ - Trade-offs entre diferentes aspectos                     │
    │ - Recomendação ponderada                                   │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ FIM: Retorna síntese + todas as análises por perspectiva   │
    └─────────────────────────────────────────────────────────────┘


EXEMPLO PRÁTICO:

Perspectiva 1 (Custo):
  "Porto Seguro oferece melhor custo-benefício com desconto de 20%..."

Perspectiva 2 (Atendimento):
  "Itaú Seguros tem o melhor NPS (Net Promoter Score) de 8.5..."

Perspectiva 3 (Cobertura):
  "SulAmérica oferece a cobertura mais abrangente incluindo..."

Perspectiva 4 (Facilidade):
  "Liberty Seguros tem processo 100% digital em 10 minutos..."

Perspectiva 5 (Reputação):
  "Porto Seguro é líder de mercado há 20 anos com..."

Síntese:
  "Analisando todos os aspectos, recomendo:
   1º Porto Seguro (melhor custo + reputação sólida)
   2º Itaú (melhor atendimento, preço médio)
   3º SulAmérica (cobertura mais completa, preço alto)
   
   Se prioridade é economia → Porto Seguro
   Se prioridade é atendimento → Itaú
   Se prioridade é cobertura → SulAmérica"


═══════════════════════════════════════════════════════════════════════════════
COMPARAÇÃO DOS MÉTODOS
═══════════════════════════════════════════════════════════════════════════════

┌──────────────────┬─────────────┬──────────────┬────────────────────┐
│ Aspecto          │ Recursive   │ Self-Ask     │ Multi-Perspective  │
├──────────────────┼─────────────┼──────────────┼────────────────────┤
│ Abordagem        │ Iterativa   │ Decomposição │ Paralela           │
│ Nº de chamadas   │ 2-4         │ 4-5          │ 6-7                │
│ Tempo médio      │ 20-40s      │ 30-50s       │ 60-90s             │
│ Custo (tokens)   │ Médio       │ Médio-Alto   │ Alto               │
│ Transparência    │ ⭐⭐⭐        │ ⭐⭐          │ ⭐                  │
│ Qualidade        │ ⭐⭐⭐⭐⭐     │ ⭐⭐⭐⭐       │ ⭐⭐⭐⭐⭐           │
│ Estruturação     │ ⭐⭐⭐        │ ⭐⭐⭐⭐⭐      │ ⭐⭐⭐⭐             │
└──────────────────┴─────────────┴──────────────┴────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
DECISÃO: QUAL MÉTODO USAR?
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│                                                                      │
│  PERGUNTA SIMPLES                                                   │
│  "Qual seguradora é mais barata?"                                   │
│  └──► Use BÁSICO (sem recursão)                                     │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  QUER MELHOR RESPOSTA POSSÍVEL                                      │
│  "Quero a recomendação mais completa e precisa"                    │
│  └──► Use RECURSIVE                                                 │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  PERGUNTA COMPLEXA/MULTIFACETADA                                    │
│  "Considerando meu histórico de sinistros, idade e região..."      │
│  └──► Use SELF-ASK                                                  │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  DECISÃO IMPORTANTE/CARA                                            │
│  "Vou assegurar um carro de R$ 250.000"                            │
│  └──► Use MULTI-PERSPECTIVE                                         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
IMPLEMENTAÇÃO TÉCNICA
═══════════════════════════════════════════════════════════════════════════════

Componentes principais no código:

RecursiveSearchEngine (recursive_search.py)
├── recursive_insurance_search()    → Implementa Recursive
│   ├── _generate_response()        → Chama LLM
│   ├── _evaluate_quality()         → Avalia score 0-10
│   ├── _generate_refinement()      → Identifica gaps
│   └── _build_refinement_query()   → Cria próxima query
│
├── self_ask_search()               → Implementa Self-Ask
│   ├── _generate_intermediate_questions()  → Decompõe
│   ├── _generate_response()        → Responde cada uma
│   └── _synthesize_final_answer()  → Sintetiza
│
└── multi_perspective_search()      → Implementa Multi-Perspective
    ├── _generate_response()        → Analisa cada perspectiva
    └── _synthesize_perspectives()  → Integra tudo


═══════════════════════════════════════════════════════════════════════════════
MÉTRICAS DE SUCESSO
═══════════════════════════════════════════════════════════════════════════════

RECURSIVE:
  ✓ Convergiu? (score >= threshold)
  ✓ Nº de iterações usadas
  ✓ Score final (0-10)
  ✓ Aspectos faltantes por iteração

SELF-ASK:
  ✓ Nº de perguntas intermediárias geradas
  ✓ Qualidade de cada resposta intermediária
  ✓ Coerência da síntese final

MULTI-PERSPECTIVE:
  ✓ Nº de perspectivas analisadas
  ✓ Profundidade de cada perspectiva
  ✓ Equilíbrio da síntese


═══════════════════════════════════════════════════════════════════════════════
FIM DO FLUXOGRAMA
═══════════════════════════════════════════════════════════════════════════════
"""

print(__doc__)
