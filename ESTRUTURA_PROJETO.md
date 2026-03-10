# 📂 ESTRUTURA DO PROJETO - Busca Recursiva com LangChain

## 🎯 Visão Geral

Este projeto implementa **três estratégias avançadas de busca recursiva** usando LangChain para melhorar iterativamente a qualidade das recomendações de seguro automotivo.

---

## 📁 Arquivos Criados

```
chatgpt-api/
│
├── 🔧 ARQUIVOS PRINCIPAIS
│   ├── main.py                          ⭐ API FastAPI com todos os endpoints
│   ├── recursive_search.py              ⭐ Motor de busca recursiva (LangChain)
│   └── requirements.txt                 📦 Dependências do projeto
│
├── 🧪 TESTES E EXEMPLOS
│   ├── test_recursive.py                🧪 Script de teste interativo
│   ├── exemplos_uso.py                  📝 Exemplos práticos de uso
│   └── FLUXOGRAMA.py                    📊 Visualização dos algoritmos
│
├── 📚 DOCUMENTAÇÃO
│   ├── README.md                        📖 Documentação principal
│   ├── RECURSIVE_SEARCH_GUIDE.md        📘 Guia detalhado de busca recursiva
│   ├── CHEAT_SHEET.md                   ⚡ Referência rápida
│   └── ESTRUTURA_PROJETO.md             📂 Este arquivo
│
└── ⚙️ CONFIGURAÇÃO
    └── .env.example                     🔑 Exemplo de configuração
```

---

## 📖 Descrição Detalhada dos Arquivos

### 🔧 Arquivos Principais

#### `main.py` ⭐
**O que faz:** API FastAPI com 5 endpoints

**Endpoints:**
1. `GET /` - Health check
2. `POST /chat` - Chat genérico com histórico
3. `POST /chat/simple` - Chat simplificado
4. `POST /chat/insurance` - Recomendação de seguros (básica)
5. `POST /chat/insurance/recursive` 🔥 - Busca recursiva avançada

**Principais funcionalidades:**
- Integração com OpenAI
- Sistema especializado em seguros automotivos
- Suporte a três tipos de busca recursiva
- CORS configurado para frontend
- Validação de dados com Pydantic

---

#### `recursive_search.py` ⭐
**O que faz:** Implementa os algoritmos de busca recursiva

**Classe principal:** `RecursiveSearchEngine`

**Métodos públicos:**
1. `recursive_insurance_search()` - Refinamento iterativo
2. `self_ask_search()` - Auto-questionamento estruturado
3. `multi_perspective_search()` - Análise multi-perspectiva

**Métodos auxiliares:**
- `_generate_response()` - Chama o LLM
- `_evaluate_quality()` - Avalia qualidade (0-10)
- `_generate_refinement()` - Identifica gaps e melhora
- `_synthesize_final_answer()` - Sintetiza respostas
- E mais...

**Modelos Pydantic:**
- `QualityScore` - Pontuação de qualidade
- `RefinementSuggestion` - Sugestões de melhoria

---

#### `requirements.txt` 📦
**O que faz:** Lista todas as dependências

**Dependências principais:**
```
fastapi==0.109.0          # Framework web
uvicorn[standard]==0.27.0 # Servidor ASGI
openai==1.12.0            # API da OpenAI
langchain==0.1.8          # Framework para LLMs
langchain-openai==0.0.5   # Integração LangChain + OpenAI
```

---

### 🧪 Testes e Exemplos

#### `test_recursive.py` 🧪
**O que faz:** Script interativo para testar todos os métodos

**Features:**
- Menu interativo
- 3 tipos de teste (um para cada método)
- Comparação visual dos métodos
- Resultados formatados e coloridos
- Verificação automática se API está rodando

**Como usar:**
```bash
python test_recursive.py
```

---

#### `exemplos_uso.py` 📝
**O que faz:** Demonstrações práticas de código

**Inclui:**
- 5 exemplos diferentes
- Código comentado e explicado
- Casos de uso reais
- Comparação entre métodos

**Exemplos incluídos:**
1. Consulta básica (sem recursão)
2. Recursive Search
3. Self-Ask
4. Multi-Perspective
5. Comparação dos métodos

---

#### `FLUXOGRAMA.py` 📊
**O que faz:** Visualização ASCII dos algoritmos

**Conteúdo:**
- Fluxograma do Recursive Search
- Fluxograma do Self-Ask
- Fluxograma do Multi-Perspective
- Comparação visual
- Guia de decisão

**Como visualizar:**
```bash
python FLUXOGRAMA.py
# ou
cat FLUXOGRAMA.py
```

---

### 📚 Documentação

#### `README.md` 📖
**O que tem:** Documentação principal do projeto

**Seções:**
- Funcionalidades principais
- Instalação passo a passo
- Como usar (com exemplos)
- Comparação dos métodos
- Estrutura do projeto
- Endpoints disponíveis
- Configurações
- Dicas de uso
- Tecnologias utilizadas

**Para quem:** Desenvolvedores que querem entender o projeto completo

---

#### `RECURSIVE_SEARCH_GUIDE.md` 📘
**O que tem:** Guia detalhado de busca recursiva

**Seções:**
- Explicação de cada tipo de busca
- Exemplos práticos de código
- Parâmetros configuráveis
- Como escolher o tipo de busca
- Entendendo os resultados
- Dicas de otimização
- Comparação de performance
- Troubleshooting

**Para quem:** Desenvolvedores que querem dominar a busca recursiva

---

#### `CHEAT_SHEET.md` ⚡
**O que tem:** Referência rápida

**Seções:**
- Comandos de instalação
- Snippets de código prontos
- Tabelas de comparação
- Troubleshooting rápido
- Dicas e recomendações

**Para quem:** Desenvolvedores que precisam de referência rápida

---

#### `ESTRUTURA_PROJETO.md` 📂
**O que tem:** Este arquivo! Mapa completo do projeto

**Para quem:** Qualquer pessoa que quer entender a organização

---

### ⚙️ Configuração

#### `.env.example` 🔑
**O que tem:** Exemplo de arquivo de configuração

**Variáveis:**
```env
OPENAI_API_KEY=sk-your-api-key-here
PORT=8000
```

**Como usar:**
```bash
cp .env.example .env
# Edite .env com sua chave real
```

---

## 🚀 Fluxo de Início Rápido

### 1️⃣ **Primeiro acesso ao projeto?**
Leia: `README.md`

### 2️⃣ **Quer instalar e executar?**
Siga: Seção "Instalação" do `README.md`

### 3️⃣ **Quer testar rapidamente?**
Execute: `python test_recursive.py`

### 4️⃣ **Quer aprender busca recursiva?**
Leia: `RECURSIVE_SEARCH_GUIDE.md`

### 5️⃣ **Precisa de código de exemplo?**
Execute ou leia: `exemplos_uso.py`

### 6️⃣ **Quer referência rápida?**
Consulte: `CHEAT_SHEET.md`

### 7️⃣ **Quer entender os algoritmos?**
Visualize: `FLUXOGRAMA.py`

### 8️⃣ **Quer modificar o código?**
Edite: `main.py` ou `recursive_search.py`

---

## 📊 Fluxo de Dados

```
┌─────────────┐
│   USUÁRIO   │
└──────┬──────┘
       │ (1) POST /chat/insurance/recursive
       │     { profile, search_type, ... }
       ▼
┌─────────────────────────────────────┐
│           main.py                   │
│  ┌───────────────────────────────┐ │
│  │ chat_insurance_recursive()    │ │
│  │ - Valida request              │ │
│  │ - Monta perfil do usuário     │ │
│  └──────────┬────────────────────┘ │
└─────────────┼───────────────────────┘
              │ (2) Chama RecursiveSearchEngine
              ▼
┌─────────────────────────────────────┐
│      recursive_search.py            │
│  ┌───────────────────────────────┐ │
│  │ RecursiveSearchEngine         │ │
│  │ - recursive_insurance_search()│ │
│  │ - self_ask_search()           │ │
│  │ - multi_perspective_search()  │ │
│  └──────────┬────────────────────┘ │
└─────────────┼───────────────────────┘
              │ (3) Chama OpenAI API via LangChain
              ▼
┌─────────────────────────────────────┐
│       LangChain + OpenAI            │
│  ┌───────────────────────────────┐ │
│  │ ChatOpenAI                    │ │
│  │ - Processa prompts            │ │
│  │ - Gera respostas              │ │
│  │ - Avalia qualidade            │ │
│  └──────────┬────────────────────┘ │
└─────────────┼───────────────────────┘
              │ (4) Retorna resultado
              ▼
┌─────────────────────────────────────┐
│           main.py                   │
│  - Formata resposta JSON            │
│  - Adiciona métricas                │
└──────────┬──────────────────────────┘
           │ (5) Retorna ao usuário
           ▼
┌─────────────┐
│   USUÁRIO   │
│ Recebe:     │
│ - Resposta  │
│ - Score     │
│ - Iterações │
└─────────────┘
```

---

## 🎯 Casos de Uso dos Arquivos

### Você quer... | Use...
---|---
Iniciar a API | `python main.py`
Testar interativamente | `python test_recursive.py`
Ver exemplos de código | `exemplos_uso.py`
Aprender sobre busca recursiva | `RECURSIVE_SEARCH_GUIDE.md`
Consulta rápida | `CHEAT_SHEET.md`
Entender algoritmos | `FLUXOGRAMA.py`
Visão geral do projeto | `README.md`
Entender estrutura | Este arquivo
Configurar API key | `.env.example` → `.env`
Adicionar features | `main.py`, `recursive_search.py`
Documentação da API | `http://localhost:8000/docs`

---

## 🔄 Ciclo de Desenvolvimento

```
1. MODIFICAR CÓDIGO
   ├── main.py (endpoints)
   └── recursive_search.py (algoritmos)

2. TESTAR
   ├── python test_recursive.py
   └── python exemplos_uso.py

3. VALIDAR
   ├── Verificar lints
   └── Testar todos os endpoints

4. DOCUMENTAR
   ├── Atualizar README.md
   └── Atualizar GUIDE se necessário

5. COMMIT
   └── git commit -m "descrição"
```

---

## 💡 Dicas

### Para Desenvolvedores Iniciantes:
1. Comece lendo `README.md`
2. Execute `test_recursive.py` para ver funcionando
3. Leia `exemplos_uso.py` para entender o código
4. Consulte `CHEAT_SHEET.md` quando precisar

### Para Desenvolvedores Experientes:
1. Vá direto ao `main.py` e `recursive_search.py`
2. Use `CHEAT_SHEET.md` como referência
3. Consulte `FLUXOGRAMA.py` para entender os algoritmos
4. Customize conforme necessário

### Para Usuários Finais:
1. Configure seguindo `README.md`
2. Use `test_recursive.py` para testar
3. Consulte `CHEAT_SHEET.md` para uso rápido
4. Veja `exemplos_uso.py` para casos práticos

---

## 📈 Métricas do Projeto

| Métrica | Valor |
|---------|-------|
| Total de arquivos | 10 |
| Arquivos Python | 4 |
| Arquivos Markdown | 5 |
| Linhas de código | ~1.500+ |
| Endpoints REST | 5 |
| Tipos de busca | 3 |
| Exemplos incluídos | 5 |

---

## 🎓 Conceitos Implementados

- ✅ Busca recursiva com refinamento iterativo
- ✅ Self-Ask (decomposição de problemas)
- ✅ Multi-perspective analysis
- ✅ Avaliação automática de qualidade
- ✅ Síntese de respostas
- ✅ Chain-of-thought
- ✅ LangChain integration
- ✅ RESTful API design
- ✅ Pydantic validation
- ✅ Type hints completos

---

## 🌟 Próximos Passos Sugeridos

1. **Cache de respostas** - Evitar reprocessar perfis similares
2. **Streaming** - Ver respostas em tempo real
3. **Ferramentas externas** - Web search, APIs de seguradoras
4. **Métricas de custo** - Track gastos com OpenAI
5. **Mais idiomas** - Suporte a inglês, espanhol
6. **Frontend** - Interface web para facilitar uso

---

**🎉 Parabéns! Você agora tem uma visão completa do projeto!**

Para começar: `python main.py` + `python test_recursive.py`
