# Busca Recursiva com LangChain - Guia de Uso

## 🚀 Visão Geral

Este sistema implementa **três estratégias de busca recursiva** usando LangChain para melhorar iterativamente a qualidade das recomendações de seguro automotivo.

## 📦 Instalação

```bash
pip install -r requirements.txt
```

## 🎯 Tipos de Busca Disponíveis

### 1. **Recursive Search** (Busca Recursiva com Refinamento)
Refina a resposta iterativamente, avaliando a qualidade e melhorando em cada iteração.

**Como funciona:**
1. Gera uma resposta inicial
2. Avalia a qualidade (pontuação de 0-10)
3. Identifica aspectos faltantes
4. Gera uma nova query focada nesses aspectos
5. Repete até atingir qualidade satisfatória ou número máximo de iterações

**Vantagens:**
- Respostas progressivamente melhores
- Avaliação objetiva de qualidade
- Transparência sobre o processo iterativo

### 2. **Self-Ask** (Auto-Questionamento)
O agente faz perguntas intermediárias a si mesmo antes de responder.

**Como funciona:**
1. Analisa a pergunta principal
2. Gera 3-4 perguntas intermediárias relevantes
3. Responde cada pergunta intermediária
4. Sintetiza todas as respostas em uma resposta final

**Vantagens:**
- Abordagem mais estruturada
- Cobre múltiplos aspectos da questão
- Raciocínio explícito e transparente

### 3. **Multi-Perspective** (Múltiplas Perspectivas)
Analisa a questão sob diferentes perspectivas e sintetiza.

**Como funciona:**
1. Analisa sob 5 perspectivas diferentes:
   - Custo-benefício e economia
   - Qualidade de atendimento
   - Abrangência de cobertura
   - Facilidade de contratação
   - Reputação no mercado
2. Sintetiza todas as perspectivas em uma resposta equilibrada

**Vantagens:**
- Visão holística e equilibrada
- Considera trade-offs importantes
- Menos viés em uma única dimensão

## 📝 Exemplos de Uso

### Exemplo 1: Busca Recursiva Básica

```python
import requests

payload = {
    "profile": {
        "idade": 28,
        "cidade": "São Paulo",
        "estado": "SP",
        "modelo_carro": "Honda Civic",
        "ano_carro": 2022,
        "valor_carro": 120000.0,
        "historico_sinistros": 0,
        "uso_veiculo": "particular",
        "cobertura_desejada": "compreensiva",
        "mensagem": "Quero as melhores seguradoras com bom custo-benefício"
    },
    "model": "gpt-4o-mini",
    "max_iterations": 3,
    "quality_threshold": 8.0,
    "search_type": "recursive"
}

response = requests.post("http://localhost:8000/chat/insurance/recursive", json=payload)
result = response.json()

print(f"Resposta Final: {result['response']}")
print(f"Pontuação de Qualidade: {result['quality_score']}")
print(f"Iterações: {result['total_iterations']}")
print(f"Convergiu: {result['converged']}")
```

### Exemplo 2: Self-Ask

```python
payload = {
    "profile": {
        "idade": 35,
        "cidade": "Rio de Janeiro",
        "estado": "RJ",
        "modelo_carro": "Toyota Corolla",
        "ano_carro": 2020,
        "valor_carro": 95000.0,
        "mensagem": "Qual seguradora tem o melhor custo-benefício para mim?"
    },
    "search_type": "self_ask"
}

response = requests.post("http://localhost:8000/chat/insurance/recursive", json=payload)
result = response.json()

print("Perguntas Intermediárias:")
for step in result['intermediate_steps']:
    print(f"\nP: {step['question']}")
    print(f"R: {step['answer'][:200]}...")

print(f"\n\nResposta Final: {result['response']}")
```

### Exemplo 3: Multi-Perspective

```python
payload = {
    "profile": {
        "idade": 42,
        "cidade": "Curitiba",
        "estado": "PR",
        "modelo_carro": "Jeep Compass",
        "ano_carro": 2023,
        "valor_carro": 180000.0,
        "mensagem": "Quero uma análise completa das opções disponíveis"
    },
    "search_type": "multi_perspective"
}

response = requests.post("http://localhost:8000/chat/insurance/recursive", json=payload)
result = response.json()

print("Análises por Perspectiva:")
for perspective in result['perspectives']:
    print(f"\n{perspective['perspective'].upper()}")
    print(perspective['response'][:300])

print(f"\n\nSÍNTESE FINAL:\n{result['response']}")
```

## 🎛️ Parâmetros Configuráveis

### RecursiveSearchRequest

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `profile` | InsuranceProfile | (obrigatório) | Perfil do usuário |
| `model` | str | "gpt-4o-mini" | Modelo da OpenAI a usar |
| `max_iterations` | int | 3 | Número máximo de iterações (recursive) |
| `quality_threshold` | float | 8.0 | Pontuação mínima para convergência |
| `search_type` | str | "recursive" | Tipo de busca: "recursive", "self_ask", "multi_perspective" |

### InsuranceProfile

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `idade` | int | Idade do condutor |
| `cidade` | str | Cidade do usuário |
| `estado` | str | Estado (UF) |
| `modelo_carro` | str | Modelo do veículo |
| `ano_carro` | int | Ano do veículo |
| `valor_carro` | float | Valor do veículo em R$ |
| `historico_sinistros` | int | Número de sinistros nos últimos anos |
| `uso_veiculo` | str | "particular", "trabalho", "ambos" |
| `cobertura_desejada` | str | "compreensiva", "terceiros", "roubo_furto" |
| `mensagem` | str | Pergunta ou observação adicional |

## 🔧 Como Escolher o Tipo de Busca

### Use **Recursive Search** quando:
- ✅ Quer a melhor resposta possível
- ✅ Qualidade é mais importante que velocidade
- ✅ Quer transparência sobre o processo de refinamento

### Use **Self-Ask** quando:
- ✅ A pergunta é complexa e multifacetada
- ✅ Quer ver o raciocínio passo a passo
- ✅ Precisa de uma análise estruturada

### Use **Multi-Perspective** quando:
- ✅ Quer uma visão equilibrada e holística
- ✅ Precisa considerar múltiplos trade-offs
- ✅ Quer comparar diferentes aspectos lado a lado

## 📊 Entendendo os Resultados

### Recursive Search Response
```json
{
  "response": "Resposta final refinada...",
  "quality_score": 8.5,
  "iterations": [
    {
      "iteration": 1,
      "query": "Pergunta original...",
      "response": "Primeira resposta...",
      "quality_score": 6.5,
      "reasoning": "Falta detalhar preços...",
      "missing_aspects": ["Comparação de preços", "Coberturas específicas"]
    },
    {
      "iteration": 2,
      "query": "Pergunta refinada...",
      "response": "Resposta melhorada...",
      "quality_score": 8.5,
      "reasoning": "Resposta completa e detalhada",
      "missing_aspects": []
    }
  ],
  "total_iterations": 2,
  "converged": true
}
```

### Self-Ask Response
```json
{
  "response": "Síntese final...",
  "intermediate_steps": [
    {
      "question": "Qual o perfil de risco deste usuário?",
      "answer": "Análise do perfil..."
    },
    {
      "question": "Quais seguradoras são mais competitivas nesta região?",
      "answer": "Análise regional..."
    }
  ],
  "search_type": "self_ask"
}
```

### Multi-Perspective Response
```json
{
  "response": "Síntese equilibrada de todas as perspectivas...",
  "perspectives": [
    {
      "perspective": "custo-benefício e economia",
      "response": "Análise de custos..."
    },
    {
      "perspective": "qualidade de atendimento",
      "response": "Análise de atendimento..."
    }
  ],
  "search_type": "multi_perspective"
}
```

## 🎯 Dicas de Otimização

### Para Melhor Performance:
1. **Forneça o máximo de informações no perfil** - quanto mais contexto, melhor a resposta
2. **Use `max_iterations: 2`** para balanço entre qualidade e velocidade
3. **Ajuste `quality_threshold`** conforme suas necessidades (7.0 = bom, 8.0 = ótimo, 9.0 = excelente)

### Para Melhor Qualidade:
1. **Use `max_iterations: 3-4`** para refinamento máximo
2. **Escolha `gpt-4o`** para respostas mais sofisticadas
3. **Use `multi_perspective`** para decisões importantes

### Para Melhor Custo:
1. **Use `max_iterations: 1-2`**
2. **Mantenha `gpt-4o-mini`** (10x mais barato que GPT-4)
3. **Use `recursive`** ao invés de `multi_perspective` (menos chamadas)

## 🚀 Executando a API

```bash
python main.py
```

A API estará disponível em `http://localhost:8000`

Documentação interativa: `http://localhost:8000/docs`

## 🧪 Testando

```bash
# Teste básico
curl http://localhost:8000/

# Teste busca recursiva
curl -X POST http://localhost:8000/chat/insurance/recursive \
  -H "Content-Type: application/json" \
  -d '{
    "profile": {
      "idade": 30,
      "cidade": "São Paulo",
      "modelo_carro": "Honda Civic",
      "valor_carro": 100000,
      "mensagem": "Quero as melhores opções"
    },
    "search_type": "recursive",
    "max_iterations": 2
  }'
```

## 📈 Comparação de Desempenho

| Métrica | Busca Simples | Recursive | Self-Ask | Multi-Perspective |
|---------|---------------|-----------|----------|-------------------|
| Qualidade | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Velocidade | ⚡⚡⚡⚡⚡ | ⚡⚡⚡ | ⚡⚡ | ⚡ |
| Custo | 💰 | 💰💰💰 | 💰💰 | 💰💰💰💰 |
| Transparência | ❌ | ✅✅✅ | ✅✅ | ✅ |
| Completude | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🤝 Contribuindo

Ideias para melhorias:
- [ ] Adicionar cache de respostas para perfis similares
- [ ] Implementar busca com ferramentas externas (web search, APIs de seguradoras)
- [ ] Adicionar suporte a streaming para ver o progresso em tempo real
- [ ] Implementar ReAct (Reasoning + Acting) com ferramentas
- [ ] Adicionar métricas de custo por request

## 📄 Licença

MIT
