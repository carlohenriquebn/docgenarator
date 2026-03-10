"""
API Backend em Python para integração com ChatGPT (OpenAI)
Com suporte a buscas recursivas usando LangChain
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import tempfile
from pathlib import Path
from recursive_search import RecursiveSearchEngine
from documentation_service import process_video_and_generate_docs, DOCS_SCREENSHOTS_DIR

load_dotenv()

app = FastAPI(
    title="ChatGPT API",
    description="API para integração com o modelo ChatGPT da OpenAI",
    version="1.0.0"
)

# CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class Message(BaseModel):
    """Mensagem individual do chat"""
    role: str  # "user" ou "assistant" ou "system"
    content: str


class ChatRequest(BaseModel):
    """Request para completar chat"""
    message: str
    model: str = "gpt-4o-mini"
    system_prompt: str | None = None
    history: list[Message] | None = None


class ChatResponse(BaseModel):
    """Resposta do chat"""
    message: str
    model: str
    usage: dict | None = None


# Prompt especializado para seguro de carro
INSURANCE_SYSTEM_PROMPT = """Você é um consultor especializado em seguros automotivos no Brasil com profundo conhecimento do mercado.

🚨 REGRAS CRÍTICAS - SIGA RIGOROSAMENTE:

1. O USUÁRIO JÁ FORNECEU SEU PERFIL na mensagem
2. LEIA ATENTAMENTE todas as informações do perfil antes de responder
3. NUNCA, EM HIPÓTESE ALGUMA, peça informações que já foram fornecidas
4. NUNCA crie perfis fictícios, hipotéticos ou exemplos
5. Se algo não foi fornecido, trabalhe com o que tem e mencione brevemente

📋 INFORMAÇÕES QUE O USUÁRIO JÁ FORNECEU:
Verifique na mensagem do usuário as informações sobre:
- Idade
- Localização (cidade/estado)
- Modelo e ano do carro
- Valor do veículo
- Histórico de sinistros
- Uso do veículo
- Cobertura desejada

✅ PROCESSO OBRIGATÓRIO:

1. **Reconheça o Perfil** (1 frase)
   - "Com base no seu perfil [resumir]..."

2. **Análise de Risco** (2-3 frases)
   - Avalie: idade, localização, veículo, sinistros
   - Classifique risco: baixo/médio/alto

3. **Recomendações de Seguradoras** (3-5 seguradoras)
   Para CADA seguradora:
   - Nome
   - Por que é adequada PARA ESTE PERFIL ESPECÍFICO
   - Faixa de preço anual estimada PARA ESTE PERFIL
   - Tipo de cobertura recomendada
   - Reputação (Reclame Aqui quando conhecido)

4. **Fatores de Preço Personalizados**
   Explique como OS DADOS FORNECIDOS impactam o preço:
   - Idade [usar a idade fornecida]
   - Localização [usar cidade/estado fornecido]
   - Veículo [usar modelo/ano/valor fornecido]
   - Sinistros [usar histórico fornecido]

5. **Dicas de Economia** (3-4 dicas ESPECÍFICAS para o perfil)

6. **Próximos Passos Práticos**

💰 DIRETRIZES DE PREÇO (use dados DO PERFIL FORNECIDO):

Preço base: R$ 2.000-4.000/ano
Ajustes:
- Jovem (<25): +30-60%
- Adulto (25-50): preço base
- Sênior (>50): +10-20%
- Sinistros: +20% por sinistro
- SP capital: +40%
- Interior: -20-30%
- Veículo >R$100k: +30-50%
- Uso trabalho: +20%

🎯 SEGURADORAS BRASILEIRAS:
Porto Seguro, Itaú, SulAmérica, Bradesco, Liberty, Azul, Zurich, HDI, Tokio Marine, Allianz, Mapfre

⚠️ LEMBRE-SE: Você TEM todas as informações. O usuário JÁ forneceu seu perfil. NÃO PEÇA NADA!"""


class InsuranceProfile(BaseModel):
    """Perfil do usuário para recomendação de seguro"""
    idade: int | None = None
    cidade: str | None = None
    estado: str | None = None
    modelo_carro: str | None = None
    ano_carro: int | None = None
    valor_carro: float | None = None  # em reais
    historico_sinistros: int | None = None  # quantos sinistros nos últimos anos
    uso_veiculo: str | None = None  # "particular", "trabalho", "ambos"
    cobertura_desejada: str | None = None  # "compreensiva", "terceiros", "roubo_furto"
    mensagem: str = ""  # pergunta ou observação adicional


class RecursiveSearchRequest(BaseModel):
    """Request para busca recursiva"""
    profile: InsuranceProfile
    model: str = "gpt-4o-mini"
    max_iterations: int = 3
    quality_threshold: float = 8.0
    search_type: str = "recursive"  # "recursive", "self_ask", "multi_perspective"
    enable_logging: bool = True  # Habilitar logs
    log_level: str = "INFO"  # "DEBUG", "INFO", "WARNING", "ERROR"


@app.get("/")
async def root():
    """Health check - frontend com abas em /app/"""
    return {"status": "ok", "message": "API ChatGPT está funcionando", "app": "/app/"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Envia uma mensagem para o ChatGPT e retorna a resposta.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY não configurada. Configure no arquivo .env"
        )

    messages = []

    if request.system_prompt:
        messages.append({"role": "system", "content": request.system_prompt})

    if request.history:
        for msg in request.history:
            messages.append({"role": msg.role, "content": msg.content})

    messages.append({"role": "user", "content": request.message})

    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=messages
        )

        return ChatResponse(
            message=response.choices[0].message.content,
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            } if response.usage else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/insurance", response_model=ChatResponse)
async def chat_insurance(profile: InsuranceProfile, model: str = "gpt-4o-mini"):
    """
    Consulta especializada: recomenda as melhores seguradoras de carro com base no seu perfil.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY não configurada. Configure no arquivo .env"
        )

    # Monta o texto do perfil para enviar ao modelo
    perfil_texto = []
    if profile.idade:
        perfil_texto.append(f"- Idade: {profile.idade} anos")
    if profile.cidade or profile.estado:
        local = ", ".join(filter(None, [profile.cidade, profile.estado]))
        perfil_texto.append(f"- Localização: {local}")
    if profile.modelo_carro:
        perfil_texto.append(f"- Carro: {profile.modelo_carro}")
    if profile.ano_carro:
        perfil_texto.append(f"- Ano: {profile.ano_carro}")
    if profile.valor_carro:
        perfil_texto.append(f"- Valor do veículo: R$ {profile.valor_carro:,.2f}")
    if profile.historico_sinistros is not None:
        perfil_texto.append(f"- Sinistros nos últimos anos: {profile.historico_sinistros}")
    if profile.uso_veiculo:
        perfil_texto.append(f"- Uso: {profile.uso_veiculo}")
    if profile.cobertura_desejada:
        perfil_texto.append(f"- Cobertura desejada: {profile.cobertura_desejada}")

    user_message = "Meu perfil:\n" + "\n".join(perfil_texto) if perfil_texto else ""
    if profile.mensagem:
        user_message += f"\n\nMinha pergunta/observação: {profile.mensagem}"
    if not user_message.strip():
        user_message = "Quais as melhores seguradoras para seguro de carro? Me ajude a escolher."

    messages = [
        {"role": "system", "content": INSURANCE_SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return ChatResponse(
            message=response.choices[0].message.content,
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            } if response.usage else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/simple")
async def chat_simple(message: str, model: str = "gpt-4o-mini"):
    """
    Endpoint simplificado: envia apenas o texto e recebe a resposta.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY não configurada. Configure no arquivo .env"
        )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/insurance/recursive")
async def chat_insurance_recursive(request: RecursiveSearchRequest):
    """
    BUSCA RECURSIVA AVANÇADA: Usa LangChain para refinar iterativamente
    a recomendação de seguradoras até obter o melhor resultado possível.
    
    Tipos de busca disponíveis:
    - "recursive": Refinamento iterativo com avaliação de qualidade
    - "self_ask": Gera perguntas intermediárias antes de responder
    - "multi_perspective": Analisa sob múltiplas perspectivas
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY não configurada. Configure no arquivo .env"
        )
    
    # Monta o perfil do usuário
    profile = request.profile
    perfil_texto = []
    if profile.idade:
        perfil_texto.append(f"- Idade: {profile.idade} anos")
    if profile.cidade or profile.estado:
        local = ", ".join(filter(None, [profile.cidade, profile.estado]))
        perfil_texto.append(f"- Localização: {local}")
    if profile.modelo_carro:
        perfil_texto.append(f"- Carro: {profile.modelo_carro}")
    if profile.ano_carro:
        perfil_texto.append(f"- Ano: {profile.ano_carro}")
    if profile.valor_carro:
        perfil_texto.append(f"- Valor do veículo: R$ {profile.valor_carro:,.2f}")
    if profile.historico_sinistros is not None:
        perfil_texto.append(f"- Sinistros nos últimos anos: {profile.historico_sinistros}")
    if profile.uso_veiculo:
        perfil_texto.append(f"- Uso: {profile.uso_veiculo}")
    if profile.cobertura_desejada:
        perfil_texto.append(f"- Cobertura desejada: {profile.cobertura_desejada}")
    
    user_profile = "Meu perfil:\n" + "\n".join(perfil_texto) if perfil_texto else "Não fornecido"
    
    # Monta a query COMPLETA com perfil + pergunta
    if profile.mensagem:
        query = f"{user_profile}\n\nMinha pergunta: {profile.mensagem}"
    else:
        query = f"{user_profile}\n\nQuais as melhores seguradoras para seguro de carro para o meu perfil?"
    
    try:
        # Mapeia string de log level para constante do logging
        import logging
        log_level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR
        }
        log_level = log_level_map.get(request.log_level.upper(), logging.INFO)
        
        # Inicializa o motor de busca recursiva
        search_engine = RecursiveSearchEngine(
            api_key=api_key,
            model=request.model,
            max_iterations=request.max_iterations,
            quality_threshold=request.quality_threshold,
            enable_logging=request.enable_logging,
            log_level=log_level
        )
        
        # Executa o tipo de busca solicitado
        if request.search_type == "recursive":
            result = search_engine.recursive_insurance_search(
                user_profile=user_profile,
                system_prompt=INSURANCE_SYSTEM_PROMPT,
                initial_query=query
            )
            
            return {
                "response": result["final_response"],
                "quality_score": result["final_score"],
                "iterations": result["iterations"],
                "total_iterations": result["total_iterations"],
                "converged": result["converged"],
                "search_type": "recursive"
            }
        
        elif request.search_type == "self_ask":
            result = search_engine.self_ask_search(
                user_profile=user_profile,
                main_question=query,
                system_prompt=INSURANCE_SYSTEM_PROMPT
            )
            
            return {
                "response": result["final_response"],
                "intermediate_steps": result["intermediate_steps"],
                "search_type": "self_ask"
            }
        
        elif request.search_type == "multi_perspective":
            result = search_engine.multi_perspective_search(
                user_profile=user_profile,
                query=query,
                system_prompt=INSURANCE_SYSTEM_PROMPT
            )
            
            return {
                "response": result["synthesis"],
                "perspectives": result["perspectives"],
                "search_type": "multi_perspective"
            }
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de busca inválido: {request.search_type}. Use 'recursive', 'self_ask' ou 'multi_perspective'."
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === Documentação a partir de vídeo + transcrição ===
FRONTEND_DIR = Path(__file__).parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/app", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="app")

# Servir screenshots da documentação
if DOCS_SCREENSHOTS_DIR.exists():
    app.mount("/documentation/screenshots", StaticFiles(directory=str(DOCS_SCREENSHOTS_DIR)), name="screenshots")


@app.post("/documentation/generate")
async def generate_documentation(video: UploadFile = File(...), vtt: UploadFile = File(...)):
    """
    Gera documentação a partir de um vídeo (MP4) e transcrição (VTT).
    - Extrai screenshots do vídeo em intervalos
    - Parseia a transcrição VTT
    - Usa GPT-4 Vision para gerar documentação estruturada
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY não configurada. Configure no arquivo .env"
        )

    if not video.filename or not video.filename.lower().endswith((".mp4", ".webm", ".mov")):
        raise HTTPException(status_code=400, detail="Arquivo de vídeo deve ser MP4, WebM ou MOV")
    if not vtt.filename or not vtt.filename.lower().endswith(".vtt"):
        raise HTTPException(status_code=400, detail="Arquivo de transcrição deve ser .vtt")

    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = Path(tmpdir) / (video.filename or "video.mp4")
        vtt_path = Path(tmpdir) / (vtt.filename or "transcript.vtt")

        video_content = await video.read()
        vtt_content = (await vtt.read()).decode("utf-8", errors="replace")

        with open(video_path, "wb") as f:
            f.write(video_content)
        with open(vtt_path, "w", encoding="utf-8") as f:
            f.write(vtt_content)

        try:
            result = process_video_and_generate_docs(
                video_path=str(video_path),
                vtt_content=vtt_content,
                openai_client=client,
                output_dir=DOCS_SCREENSHOTS_DIR,
                interval_sec=5.0,
                max_frames=10,
            )
            return {
                "documentation": result["documentation"],
                "screenshots_base64": result.get("screenshots_base64", {}),
                "screenshots_count": len(result["screenshots"]),
                "screenshots_folder": str(DOCS_SCREENSHOTS_DIR),
                "transcription_preview": result["transcription"][:500] + ("..." if len(result["transcription"]) > 500 else ""),
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao gerar documentação: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
