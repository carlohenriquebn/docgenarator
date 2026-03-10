# 🚀 CHEAT SHEET - Busca Recursiva com LangChain

## ⚡ Início Rápido

### 1️⃣ Instalação
```bash
pip install -r requirements.txt
```

### 2️⃣ Configuração
```bash
# Crie arquivo .env
echo "OPENAI_API_KEY=sua_chave_aqui" > .env
```

### 3️⃣ Executar API
```bash
python main.py
```

### 4️⃣ Testar
```bash
python test_recursive.py
# ou
python exemplos_uso.py
```

---

## 📋 Endpoints

### Básico (Sem Recursão)
```bash
POST /chat/insurance
```

### Recursivo (Recomendado) 🔥
```bash
POST /chat/insurance/recursive
```

---

## 🎯 Tipos de Busca

| Tipo | Código | Quando Usar |
|------|--------|-------------|
| **Recursive** | `"recursive"` | Máxima qualidade, refinamento iterativo |
| **Self-Ask** | `"self_ask"` | Análise estruturada, perguntas complexas |
| **Multi-Perspective** | `"multi_perspective"` | Visão holística, múltiplos aspectos |

---

## 💻 Código Python

### Recursive Search (Refinamento Iterativo)
```python
import requests

response = requests.post("http://localhost:8000/chat/insurance/recursive", json={
    "profile": {
        "idade": 30,
        "cidade": "São Paulo",
        "modelo_carro": "Honda Civic",
        "ano_carro": 2022,
        "valor_carro": 120000.0,
        "mensagem": "Quero as melhores seguradoras"
    },
    "search_type": "recursive",
    "max_iterations": 3,
    "quality_threshold": 8.0
})

result = response.json()
print(f"Resposta: {result['response']}")
print(f"Qualidade: {result['quality_score']}/10")
```

### Self-Ask (Auto-Questionamento)
```python
response = requests.post("http://localhost:8000/chat/insurance/recursive", json={
    "profile": {
        "idade": 30,
        "modelo_carro": "Honda Civic",
        "valor_carro": 120000.0,
        "mensagem": "Qual a melhor seguradora?"
    },
    "search_type": "self_ask"
})

result = response.json()
for step in result['intermediate_steps']:
    print(f"P: {step['question']}")
    print(f"R: {step['answer']}\n")
print(f"Final: {result['response']}")
```

### Multi-Perspective (Múltiplas Perspectivas)
```python
response = requests.post("http://localhost:8000/chat/insurance/recursive", json={
    "profile": {
        "idade": 30,
        "modelo_carro": "Honda Civic",
        "valor_carro": 120000.0,
        "mensagem": "Quero análise completa"
    },
    "search_type": "multi_perspective"
})

result = response.json()
print(f"Perspectivas: {len(result['perspectives'])}")
print(f"Síntese: {result['response']}")
```

---

## 🔧 Parâmetros

### Profile (Perfil do Usuário)
```python
{
    "idade": int,                    # Idade do condutor
    "cidade": str,                   # Cidade
    "estado": str,                   # UF (ex: "SP")
    "modelo_carro": str,             # Modelo do veículo
    "ano_carro": int,                # Ano do veículo
    "valor_carro": float,            # Valor em R$
    "historico_sinistros": int,      # Nº de sinistros
    "uso_veiculo": str,              # "particular", "trabalho", "ambos"
    "cobertura_desejada": str,       # "compreensiva", "terceiros", "roubo_furto"
    "mensagem": str                  # Pergunta ou observação
}
```

### Configurações de Busca
```python
{
    "max_iterations": 3,              # 1-5 (recomendado: 2-3)
    "quality_threshold": 8.0,         # 0-10 (padrão: 8.0)
    "search_type": "recursive",       # "recursive" | "self_ask" | "multi_perspective"
    "model": "gpt-4o-mini"           # "gpt-4o-mini" | "gpt-4o"
}
```

---

## 📊 Comparação Rápida

### Qualidade
```
Multi-Perspective ⭐⭐⭐⭐⭐
Recursive        ⭐⭐⭐⭐⭐
Self-Ask         ⭐⭐⭐⭐
Básico           ⭐⭐⭐
```

### Velocidade
```
Básico           ⚡⚡⚡⚡⚡
Recursive        ⚡⚡⚡
Self-Ask         ⚡⚡
Multi-Perspective ⚡
```

### Custo
```
Básico           💰
Recursive        💰💰💰
Self-Ask         💰💰
Multi-Perspective 💰💰💰💰
```

---

## 🎯 Recomendações por Caso de Uso

### Consulta Rápida → Básico
```python
POST /chat/insurance
```

### Melhor Resposta Possível → Recursive
```python
"search_type": "recursive"
"max_iterations": 3
```

### Análise Detalhada → Self-Ask
```python
"search_type": "self_ask"
```

### Decisão Importante → Multi-Perspective
```python
"search_type": "multi_perspective"
```

---

## 🔍 Troubleshooting

### API não responde
```bash
# Verifique se está rodando
curl http://localhost:8000/
```

### Erro de API Key
```bash
# Verifique o arquivo .env
cat .env
# Deve conter: OPENAI_API_KEY=sk-...
```

### Timeout
```python
# Aumente o timeout
response = requests.post(url, json=payload, timeout=180)
```

### Qualidade baixa
```python
# Aumente iterações e threshold
"max_iterations": 4,
"quality_threshold": 9.0
```

---

## 📚 Arquivos Úteis

| Arquivo | Descrição |
|---------|-----------|
| `README.md` | Documentação completa |
| `RECURSIVE_SEARCH_GUIDE.md` | Guia detalhado de busca recursiva |
| `test_recursive.py` | Testes interativos |
| `exemplos_uso.py` | Exemplos práticos |
| `main.py` | Código da API |
| `recursive_search.py` | Motor de busca recursiva |

---

## 🌐 URLs Úteis

- API: `http://localhost:8000`
- Docs Swagger: `http://localhost:8000/docs`
- Docs ReDoc: `http://localhost:8000/redoc`

---

## 💡 Dicas Rápidas

✅ **DO:**
- Forneça máximo de informações no perfil
- Use `recursive` para melhor qualidade
- Use `gpt-4o-mini` para economia
- Ajuste `max_iterations` conforme necessidade

❌ **DON'T:**
- Não use `max_iterations > 5` (muito caro)
- Não omita campos importantes do perfil
- Não use `multi_perspective` para consultas simples
- Não esqueça de configurar `OPENAI_API_KEY`

---

## 🚀 Comando All-in-One

```bash
# Clone, instale e execute tudo de uma vez
pip install -r requirements.txt && \
echo "OPENAI_API_KEY=sua_chave" > .env && \
python main.py
```

---

**📖 Para mais detalhes, consulte `README.md` e `RECURSIVE_SEARCH_GUIDE.md`**
