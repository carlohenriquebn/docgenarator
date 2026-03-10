# 🚀 ChatGPT API com Busca Recursiva LangChain

API backend em Python para integração com ChatGPT da OpenAI, com **sistema avançado de busca recursiva usando LangChain** para melhorar iterativamente a qualidade das respostas.

## 🎯 Funcionalidades

### ✨ Principais Features

1. **API REST com FastAPI** - Endpoints rápidos e bem documentados
2. **Integração com OpenAI** - Suporte a todos os modelos GPT
3. **Sistema de Seguros Automotivos** - Especializado em recomendações de seguradoras
4. **🔥 Busca Recursiva com LangChain** - Três estratégias avançadas:
   - **Recursive Search**: Refinamento iterativo com avaliação de qualidade
   - **Self-Ask**: Auto-questionamento estruturado
   - **Multi-Perspective**: Análise sob múltiplas perspectivas

## 📦 Instalação

### Pré-requisitos
- Python 3.10+
- Conta OpenAI com API Key

### Passos

1. **Clone o repositório** (ou crie os arquivos)

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure a API Key:**

Crie um arquivo `.env` na raiz do projeto:
```env
OPENAI_API_KEY=sua_chave_api_aqui
PORT=8000
```

4. **Execute a API:**
```bash
python main.py
```

A API estará disponível em: `http://localhost:8000`

Documentação interativa: `http://localhost:8000/docs`

## 🎮 Como Usar

### 1. Endpoint Básico (Sem Recursão)

```python
import requests

response = requests.post("http://localhost:8000/chat/insurance", json={
    "idade": 28,
    "cidade": "São Paulo",
    "estado": "SP",
    "modelo_carro": "Honda Civic",
    "ano_carro": 2022,
    "valor_carro": 120000.0,
    "mensagem": "Quero as melhores seguradoras"
})

print(response.json()["message"])
```

### 2. Busca Recursiva (Recomendado) 🔥

#### A) Recursive Search - Refinamento Iterativo

```python
response = requests.post("http://localhost:8000/chat/insurance/recursive", json={
    "profile": {
        "idade": 28,
        "cidade": "São Paulo",
        "modelo_carro": "Honda Civic",
        "ano_carro": 2022,
        "valor_carro": 120000.0,
        "mensagem": "Quero as melhores seguradoras com bom custo-benefício"
    },
    "search_type": "recursive",
    "max_iterations": 3,
    "quality_threshold": 8.0,
    "enable_logging": True,    # 📋 Habilita logs (NOVO!)
    "log_level": "INFO"         # DEBUG, INFO, WARNING, ERROR
})

result = response.json()
print(f"Resposta: {result['response']}")
print(f"Qualidade: {result['quality_score']}/10")
print(f"Iterações: {result['total_iterations']}")
```

**Como funciona:**
1. Gera resposta inicial
2. Avalia qualidade (0-10)
3. Identifica aspectos faltantes
4. Refina e melhora
5. Repete até atingir qualidade satisfatória

**💡 NOVO: Sistema de Logs**
- Acompanhe em tempo real o processo de refinamento
- Veja scores de qualidade, iterações e convergência
- Logs salvos em `recursive_search.log`
- Níveis: DEBUG (detalhado), INFO (padrão), WARNING, ERROR
- Veja `GUIA_LOGS.md` para mais detalhes

#### B) Self-Ask - Auto-Questionamento

```python
response = requests.post("http://localhost:8000/chat/insurance/recursive", json={
    "profile": {
        "idade": 35,
        "cidade": "Rio de Janeiro",
        "modelo_carro": "Toyota Corolla",
        "valor_carro": 95000.0,
        "mensagem": "Qual seguradora tem melhor custo-benefício?"
    },
    "search_type": "self_ask"
})

result = response.json()
print("Perguntas Intermediárias:")
for step in result['intermediate_steps']:
    print(f"- {step['question']}")
print(f"\nResposta Final: {result['response']}")
```

**Como funciona:**
1. Gera perguntas intermediárias relevantes
2. Responde cada pergunta
3. Sintetiza todas em resposta final

#### C) Multi-Perspective - Múltiplas Perspectivas

```python
response = requests.post("http://localhost:8000/chat/insurance/recursive", json={
    "profile": {
        "idade": 42,
        "cidade": "Curitiba",
        "modelo_carro": "Jeep Compass",
        "valor_carro": 180000.0,
        "mensagem": "Quero análise completa"
    },
    "search_type": "multi_perspective"
})

result = response.json()
print(f"Perspectivas Analisadas: {len(result['perspectives'])}")
print(f"Síntese: {result['response']}")
```

**Como funciona:**
1. Analisa sob 5 perspectivas diferentes:
   - Custo-benefício
   - Atendimento
   - Cobertura
   - Facilidade
   - Reputação
2. Sintetiza tudo em resposta equilibrada

## 🧪 Testando

Execute o script de demonstração interativo:

```bash
python test_recursive.py
```

Este script oferece um menu para testar todas as funcionalidades!

## 📊 Comparação dos Métodos

| Método | Qualidade | Velocidade | Custo | Melhor Para |
|--------|-----------|------------|-------|-------------|
| **Simples** | ⭐⭐⭐ | ⚡⚡⚡⚡⚡ | 💰 | Consultas rápidas |
| **Recursive** | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ | 💰💰💰 | Máxima qualidade |
| **Self-Ask** | ⭐⭐⭐⭐ | ⚡⚡ | 💰💰 | Análise estruturada |
| **Multi-Perspective** | ⭐⭐⭐⭐⭐ | ⚡ | 💰💰💰💰 | Visão holística |

## 📁 Estrutura do Projeto

```
chatgpt-api/
├── main.py                      # API principal com todos os endpoints
├── recursive_search.py          # Motor de busca recursiva com LangChain
├── test_recursive.py            # Script de teste interativo
├── requirements.txt             # Dependências do projeto
├── .env                         # Configurações (não commitado)
├── README.md                    # Este arquivo
└── RECURSIVE_SEARCH_GUIDE.md    # Guia detalhado de uso
```

## 🎛️ Endpoints Disponíveis

### GET `/`
Health check da API

### POST `/chat`
Chat genérico com histórico

**Request:**
```json
{
  "message": "Sua mensagem",
  "model": "gpt-4o-mini",
  "system_prompt": "Prompt do sistema (opcional)",
  "history": [...]  // opcional
}
```

### POST `/chat/simple`
Endpoint simplificado

**Request:**
```json
{
  "message": "Sua pergunta",
  "model": "gpt-4o-mini"
}
```

### POST `/chat/insurance`
Consulta de seguros (simples)

**Request:**
```json
{
  "idade": 28,
  "cidade": "São Paulo",
  "modelo_carro": "Honda Civic",
  "ano_carro": 2022,
  "valor_carro": 120000.0,
  // ... outros campos opcionais
  "mensagem": "Sua pergunta"
}
```

### POST `/chat/insurance/recursive` 🔥
Busca recursiva avançada (NOVO!)

**Request:**
```json
{
  "profile": {
    "idade": 28,
    "cidade": "São Paulo",
    "modelo_carro": "Honda Civic",
    "ano_carro": 2022,
    "valor_carro": 120000.0,
    "historico_sinistros": 0,
    "uso_veiculo": "particular",
    "cobertura_desejada": "compreensiva",
    "mensagem": "Sua pergunta"
  },
  "model": "gpt-4o-mini",
  "max_iterations": 3,
  "quality_threshold": 8.0,
  "search_type": "recursive"  // "recursive" | "self_ask" | "multi_perspective"
}
```

## ⚙️ Configurações

### Variáveis de Ambiente (.env)

```env
OPENAI_API_KEY=sk-...          # Obrigatório
PORT=8000                       # Opcional (padrão: 8000)
```

### Parâmetros de Busca Recursiva

| Parâmetro | Padrão | Descrição |
|-----------|--------|-----------|
| `max_iterations` | 3 | Máx. de iterações (1-5 recomendado) |
| `quality_threshold` | 8.0 | Pontuação mínima para parar (0-10) |
| `search_type` | "recursive" | Tipo de busca |
| `model` | "gpt-4o-mini" | Modelo OpenAI |

## 💡 Dicas de Uso

### Para Melhor Qualidade:
- ✅ Use `max_iterations: 3-4`
- ✅ Forneça o máximo de informações no perfil
- ✅ Use `search_type: "multi_perspective"` para decisões importantes
- ✅ Ajuste `quality_threshold: 9.0` para excelência máxima

### Para Melhor Performance:
- ✅ Use `max_iterations: 2`
- ✅ Mantenha `model: "gpt-4o-mini"`
- ✅ Use `search_type: "recursive"` (mais rápido que multi-perspective)

### Para Menor Custo:
- ✅ Use `max_iterations: 1-2`
- ✅ Mantenha `gpt-4o-mini` (10x mais barato)
- ✅ Use endpoint simples `/chat/insurance` quando recursão não é necessária

## 🔬 Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido
- **OpenAI API** - Modelos GPT (gpt-4o, gpt-4o-mini)
- **LangChain** - Framework para aplicações com LLMs
- **LangChain-OpenAI** - Integração LangChain + OpenAI
- **Pydantic** - Validação de dados
- **Python-dotenv** - Gerenciamento de variáveis de ambiente

## 📚 Documentação Adicional

- `RECURSIVE_SEARCH_GUIDE.md` - Guia completo de busca recursiva
- `http://localhost:8000/docs` - Documentação interativa Swagger
- `http://localhost:8000/redoc` - Documentação ReDoc

## 🎓 Conceitos de Busca Recursiva

### O que é Busca Recursiva?
Técnica onde o sistema melhora iterativamente suas respostas através de:
- **Auto-avaliação**: Analisa a qualidade da própria resposta
- **Refinamento**: Identifica gaps e melhora
- **Convergência**: Para quando atinge qualidade satisfatória

### Por que usar?
- ✅ **Qualidade Superior**: Respostas mais completas e precisas
- ✅ **Transparência**: Vê o processo de raciocínio
- ✅ **Adaptabilidade**: Ajusta-se à complexidade da pergunta
- ✅ **Confiabilidade**: Menos chance de respostas incompletas

### Inspirado em:
- **ReAct** (Reasoning + Acting)
- **Self-Ask** (Perguntas intermediárias)
- **Constitutional AI** (Auto-refinamento)
- **Chain-of-Thought** (Cadeia de raciocínio)

## 🤝 Contribuindo

Melhorias sugeridas:
- [ ] Cache de respostas para perfis similares
- [ ] Streaming de respostas em tempo real
- [ ] Ferramentas externas (web search, APIs)
- [ ] Métricas de custo por request
- [ ] Suporte a mais idiomas

## 📄 Licença

MIT - Sinta-se livre para usar e modificar!

## 💬 Suporte

- Documentação: `RECURSIVE_SEARCH_GUIDE.md`
- API Docs: `http://localhost:8000/docs`
- Issues: Abra uma issue no repositório

---

**Desenvolvido com ❤️ usando FastAPI, OpenAI e LangChain**
