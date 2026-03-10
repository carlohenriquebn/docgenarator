"""
Módulo de Busca Recursiva com LangChain
Implementa diferentes estratégias de busca recursiva para melhorar resultados
"""
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import os
import logging
from datetime import datetime


class QualityScore(BaseModel):
    """Pontuação de qualidade da resposta"""
    score: float = Field(description="Pontuação de 0 a 10")
    reasoning: str = Field(description="Justificativa da pontuação")
    missing_aspects: List[str] = Field(description="Aspectos que faltam ou podem melhorar")
    is_complete: bool = Field(description="Se a resposta está completa o suficiente")


class RefinementSuggestion(BaseModel):
    """Sugestão de refinamento para próxima iteração"""
    focus_areas: List[str] = Field(description="Áreas que precisam de mais atenção")
    additional_questions: List[str] = Field(description="Perguntas adicionais a serem respondidas")


# Configuração de logging
def setup_logger(name: str = "recursive_search", level: int = logging.INFO) -> logging.Logger:
    """Configura logger para busca recursiva"""
    logger = logging.getLogger(name)
    
    # Remove handlers existentes para evitar duplicação
    if logger.handlers:
        logger.handlers.clear()
    
    logger.setLevel(level)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Handler para arquivo
    file_handler = logging.FileHandler('recursive_search.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Formato dos logs
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


class RecursiveSearchEngine:
    """
    Motor de busca recursiva que melhora iterativamente os resultados
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        max_iterations: int = 3,
        quality_threshold: float = 8.0,
        enable_logging: bool = True,
        log_level: int = logging.INFO
    ):
        self.llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            temperature=0.7
        )
        self.max_iterations = max_iterations
        self.quality_threshold = quality_threshold
        self.enable_logging = enable_logging
        
        # Setup logger
        self.logger = setup_logger(level=log_level) if enable_logging else None
        
        if self.logger:
            self.logger.info("="*80)
            self.logger.info(f"🚀 RecursiveSearchEngine inicializado")
            self.logger.info(f"   Modelo: {model}")
            self.logger.info(f"   Max Iterações: {max_iterations}")
            self.logger.info(f"   Threshold Qualidade: {quality_threshold}")
            self.logger.info("="*80)
        
    def recursive_insurance_search(
        self,
        user_profile: str,
        system_prompt: str,
        initial_query: str
    ) -> Dict[str, Any]:
        """
        Busca recursiva especializada para seguros
        Refina a resposta iterativamente até atingir qualidade satisfatória
        """
        if self.logger:
            self.logger.info("\n" + "="*80)
            self.logger.info("🔄 INICIANDO BUSCA RECURSIVA")
            self.logger.info("="*80)
            self.logger.info(f"📝 Query Inicial: {initial_query}")
            self.logger.info(f"👤 Perfil do Usuário:\n{user_profile}")
        
        conversation_history = []
        iterations_data = []
        
        current_query = initial_query
        best_response = None
        best_score = 0.0
        
        for iteration in range(self.max_iterations):
            if self.logger:
                self.logger.info(f"\n{'─'*80}")
                self.logger.info(f"🔄 ITERAÇÃO {iteration + 1}/{self.max_iterations}")
                self.logger.info(f"{'─'*80}")
                self.logger.info(f"❓ Query: {current_query[:100]}...")
            
            # Gera resposta para a query atual
            if self.logger:
                self.logger.info("🤖 Gerando resposta do LLM...")
            
            response = self._generate_response(
                system_prompt=system_prompt,
                user_query=current_query,
                conversation_history=conversation_history
            )
            
            if self.logger:
                self.logger.info(f"✅ Resposta gerada ({len(response)} caracteres)")
                self.logger.debug(f"Resposta completa: {response[:200]}...")
            
            # Avalia a qualidade da resposta
            if self.logger:
                self.logger.info("📊 Avaliando qualidade da resposta...")
            
            quality = self._evaluate_quality(
                query=initial_query,
                response=response,
                user_profile=user_profile
            )
            
            if self.logger:
                self.logger.info(f"📈 Score de Qualidade: {quality.score:.1f}/10")
                self.logger.info(f"💭 Raciocínio: {quality.reasoning}")
                if quality.missing_aspects:
                    self.logger.warning(f"⚠️  Aspectos Faltantes: {', '.join(quality.missing_aspects)}")
                else:
                    self.logger.info("✅ Nenhum aspecto faltante identificado")
            
            # Armazena dados da iteração
            iteration_info = {
                "iteration": iteration + 1,
                "query": current_query,
                "response": response,
                "quality_score": quality.score,
                "reasoning": quality.reasoning,
                "missing_aspects": quality.missing_aspects
            }
            iterations_data.append(iteration_info)
            
            # Atualiza melhor resposta
            if quality.score > best_score:
                best_score = quality.score
                best_response = response
                if self.logger:
                    self.logger.info(f"🏆 Nova melhor resposta! Score: {best_score:.1f}/10")
            
            # Adiciona ao histórico
            conversation_history.append({"role": "user", "content": current_query})
            conversation_history.append({"role": "assistant", "content": response})
            
            # Verifica se atingiu qualidade satisfatória
            if quality.is_complete and quality.score >= self.quality_threshold:
                if self.logger:
                    self.logger.info(f"\n{'='*80}")
                    self.logger.info(f"🎯 CONVERGÊNCIA ATINGIDA!")
                    self.logger.info(f"   Score: {quality.score:.1f}/10 >= Threshold: {self.quality_threshold}")
                    self.logger.info(f"   Iterações usadas: {iteration + 1}/{self.max_iterations}")
                    self.logger.info(f"{'='*80}")
                break
            
            # Se não é a última iteração, gera refinamento
            if iteration < self.max_iterations - 1:
                if self.logger:
                    self.logger.info("🔧 Gerando refinamento para próxima iteração...")
                
                refinement = self._generate_refinement(
                    original_query=initial_query,
                    current_response=response,
                    quality=quality,
                    user_profile=user_profile
                )
                
                if self.logger:
                    self.logger.info(f"🎯 Áreas de foco: {', '.join(refinement.focus_areas)}")
                    self.logger.info(f"❓ Perguntas adicionais: {len(refinement.additional_questions)}")
                
                # Prepara próxima query com foco nos aspectos faltantes
                current_query = self._build_refinement_query(
                    original_query=initial_query,
                    refinement=refinement,
                    previous_response=response
                )
        else:
            # Loop completou todas iterações sem convergir
            if self.logger:
                self.logger.warning(f"\n{'='*80}")
                self.logger.warning(f"⚠️  LIMITE DE ITERAÇÕES ATINGIDO")
                self.logger.warning(f"   Score final: {best_score:.1f}/10 < Threshold: {self.quality_threshold}")
                self.logger.warning(f"   Iterações usadas: {self.max_iterations}/{self.max_iterations}")
                self.logger.warning(f"{'='*80}")
        
        result = {
            "final_response": best_response,
            "final_score": best_score,
            "iterations": iterations_data,
            "total_iterations": len(iterations_data),
            "converged": best_score >= self.quality_threshold
        }
        
        if self.logger:
            self.logger.info(f"\n{'='*80}")
            self.logger.info(f"✅ BUSCA RECURSIVA FINALIZADA")
            self.logger.info(f"   Score Final: {best_score:.1f}/10")
            self.logger.info(f"   Convergiu: {'Sim ✅' if result['converged'] else 'Não ❌'}")
            self.logger.info(f"   Total de Iterações: {result['total_iterations']}")
            self.logger.info(f"{'='*80}\n")
        
        return result
    
    def self_ask_search(
        self,
        user_profile: str,
        main_question: str,
        system_prompt: str
    ) -> Dict[str, Any]:
        """
        Implementa Self-Ask: o agente faz perguntas intermediárias
        para coletar informações antes de responder
        """
        if self.logger:
            self.logger.info("\n" + "="*80)
            self.logger.info("🤔 INICIANDO SELF-ASK SEARCH")
            self.logger.info("="*80)
            self.logger.info(f"❓ Pergunta Principal: {main_question}")
        
        # Gera perguntas intermediárias
        if self.logger:
            self.logger.info("📋 Gerando perguntas intermediárias...")
        
        intermediate_questions = self._generate_intermediate_questions(
            main_question=main_question,
            user_profile=user_profile
        )
        
        if self.logger:
            self.logger.info(f"✅ {len(intermediate_questions)} perguntas geradas:")
            for i, q in enumerate(intermediate_questions, 1):
                self.logger.info(f"   {i}. {q}")
        
        # Responde cada pergunta intermediária
        intermediate_answers = []
        for i, question in enumerate(intermediate_questions, 1):
            if self.logger:
                self.logger.info(f"\n{'─'*80}")
                self.logger.info(f"🔍 Respondendo pergunta {i}/{len(intermediate_questions)}")
                self.logger.info(f"❓ {question}")
            
            answer = self._generate_response(
                system_prompt=system_prompt,
                user_query=question,
                conversation_history=[]
            )
            
            if self.logger:
                self.logger.info(f"✅ Resposta gerada ({len(answer)} caracteres)")
                self.logger.debug(f"Resposta: {answer[:150]}...")
            
            intermediate_answers.append({
                "question": question,
                "answer": answer
            })
        
        # Gera resposta final com base nas respostas intermediárias
        if self.logger:
            self.logger.info(f"\n{'─'*80}")
            self.logger.info("🎯 Sintetizando resposta final...")
        
        final_response = self._synthesize_final_answer(
            main_question=main_question,
            intermediate_qa=intermediate_answers,
            system_prompt=system_prompt,
            user_profile=user_profile
        )
        
        if self.logger:
            self.logger.info(f"✅ Síntese final gerada ({len(final_response)} caracteres)")
            self.logger.info(f"\n{'='*80}")
            self.logger.info(f"✅ SELF-ASK SEARCH FINALIZADO")
            self.logger.info(f"   Perguntas intermediárias: {len(intermediate_questions)}")
            self.logger.info(f"{'='*80}\n")
        
        return {
            "intermediate_steps": intermediate_answers,
            "final_response": final_response
        }
    
    def multi_perspective_search(
        self,
        user_profile: str,
        query: str,
        system_prompt: str
    ) -> Dict[str, Any]:
        """
        Analisa a questão sob múltiplas perspectivas e sintetiza
        """
        perspectives = [
            "custo-benefício e economia",
            "qualidade de atendimento e satisfação do cliente",
            "abrangência de cobertura e proteção",
            "facilidade de contratação e burocracia",
            "reputação e confiabilidade no mercado"
        ]
        
        if self.logger:
            self.logger.info("\n" + "="*80)
            self.logger.info("👁️  INICIANDO MULTI-PERSPECTIVE SEARCH")
            self.logger.info("="*80)
            self.logger.info(f"❓ Query: {query}")
            self.logger.info(f"📊 Perspectivas a analisar: {len(perspectives)}")
        
        perspective_responses = []
        for i, perspective in enumerate(perspectives, 1):
            if self.logger:
                self.logger.info(f"\n{'─'*80}")
                self.logger.info(f"🔍 Analisando perspectiva {i}/{len(perspectives)}")
                self.logger.info(f"📌 {perspective.upper()}")
            
            focused_query = f"{query}\n\nFOCO ESPECIAL: Analise principalmente do ponto de vista de {perspective}."
            
            if self.logger:
                self.logger.info("🤖 Gerando análise...")
            
            response = self._generate_response(
                system_prompt=system_prompt,
                user_query=focused_query,
                conversation_history=[]
            )
            
            if self.logger:
                self.logger.info(f"✅ Análise gerada ({len(response)} caracteres)")
                self.logger.debug(f"Resposta: {response[:150]}...")
            
            perspective_responses.append({
                "perspective": perspective,
                "response": response
            })
        
        # Sintetiza todas as perspectivas
        if self.logger:
            self.logger.info(f"\n{'─'*80}")
            self.logger.info("🎯 Sintetizando todas as perspectivas...")
        
        synthesis = self._synthesize_perspectives(
            query=query,
            perspectives=perspective_responses,
            user_profile=user_profile
        )
        
        if self.logger:
            self.logger.info(f"✅ Síntese final gerada ({len(synthesis)} caracteres)")
            self.logger.info(f"\n{'='*80}")
            self.logger.info(f"✅ MULTI-PERSPECTIVE SEARCH FINALIZADO")
            self.logger.info(f"   Perspectivas analisadas: {len(perspectives)}")
            self.logger.info(f"{'='*80}\n")
        
        return {
            "perspectives": perspective_responses,
            "synthesis": synthesis
        }
    
    def _generate_response(
        self,
        system_prompt: str,
        user_query: str,
        conversation_history: List[Dict[str, str]]
    ) -> str:
        """Gera uma resposta do LLM"""
        if self.logger:
            self.logger.debug(f"Chamando LLM com query de {len(user_query)} caracteres")
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_query})
        
        try:
            response = self.llm.invoke(messages)
            if self.logger:
                self.logger.debug(f"LLM retornou resposta de {len(response.content)} caracteres")
            return response.content
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ Erro ao chamar LLM: {str(e)}")
            raise
    
    def _evaluate_quality(
        self,
        query: str,
        response: str,
        user_profile: str
    ) -> QualityScore:
        """Avalia a qualidade de uma resposta"""
        if self.logger:
            self.logger.debug("Iniciando avaliação de qualidade...")
        
        parser = PydanticOutputParser(pydantic_object=QualityScore)
        
        evaluation_prompt = ChatPromptTemplate.from_template(
            """Você é um avaliador RIGOROSO especializado em qualidade de respostas sobre seguros automotivos.

CRITÉRIOS DE AVALIAÇÃO (seja crítico e exigente):

1. **Uso do Perfil do Usuário** (peso: 30%)
   - A resposta usa DIRETAMENTE as informações fornecidas?
   - Evita criar perfis fictícios ou hipotéticos?
   - ❌ PENALIZE FORTEMENTE se pedir informações já fornecidas
   - ❌ PENALIZE FORTEMENTE se usar perfil fictício em vez do real

2. **Especificidade** (peso: 25%)
   - Recomendações são específicas para ESTE perfil?
   - Preços consideram idade, localização, veículo, sinistros?
   - Fornece valores concretos e acionáveis?

3. **Completude** (peso: 20%)
   - Cobre todos os aspectos importantes?
   - Análise de todas as informações fornecidas?
   - Recomendações justificadas?

4. **Utilidade Prática** (peso: 15%)
   - Ajuda genuinamente na tomada de decisão?
   - Fornece próximos passos claros?
   - Dicas aplicáveis ao perfil?

5. **Precisão** (peso: 10%)
   - Informações sobre seguradoras corretas?
   - Faixas de preço realistas?
   - Fatores de risco bem explicados?

PONTUAÇÃO:
- 9-10: EXCEPCIONAL - Personalizado, específico, completo, acionável
- 7-8: BOM - Usa o perfil, mas pode melhorar especificidade
- 5-6: REGULAR - Genérico demais ou pede informações já fornecidas
- 3-4: RUIM - Cria perfis fictícios ou ignora informações fornecidas
- 0-2: MUITO RUIM - Não responde adequadamente ou irrelevante

PERFIL DO USUÁRIO:
{user_profile}

PERGUNTA ORIGINAL:
{query}

RESPOSTA A SER AVALIADA:
{response}

{format_instructions}

SEJA CRÍTICO E RIGOROSO. Se a resposta pede informações já fornecidas ou usa perfil fictício, dê nota BAIXA (3-5)."""
        )
        
        chain = evaluation_prompt | self.llm | parser
        
        try:
            quality = chain.invoke({
                "user_profile": user_profile,
                "query": query,
                "response": response,
                "format_instructions": parser.get_format_instructions()
            })
            
            if self.logger:
                self.logger.debug(f"Avaliação concluída: Score {quality.score}/10")
            
            return quality
        except Exception as e:
            if self.logger:
                self.logger.warning(f"⚠️  Erro no parsing da avaliação: {str(e)}. Usando fallback.")
            
            # Fallback se o parsing falhar
            return QualityScore(
                score=7.0,
                reasoning="Avaliação automática indisponível",
                missing_aspects=[],
                is_complete=True
            )
    
    def _generate_refinement(
        self,
        original_query: str,
        current_response: str,
        quality: QualityScore,
        user_profile: str
    ) -> RefinementSuggestion:
        """Gera sugestões de refinamento"""
        parser = PydanticOutputParser(pydantic_object=RefinementSuggestion)
        
        refinement_prompt = ChatPromptTemplate.from_template(
            """Você é um especialista em melhorar respostas sobre seguros automotivos.

Analise a resposta atual e identifique:
1. Quais áreas precisam de mais detalhamento
2. Quais perguntas adicionais ajudariam a melhorar a resposta
3. Quais aspectos importantes foram negligenciados

PERFIL DO USUÁRIO:
{user_profile}

PERGUNTA ORIGINAL:
{original_query}

RESPOSTA ATUAL:
{current_response}

ASPECTOS FALTANTES IDENTIFICADOS:
{missing_aspects}

{format_instructions}

Seja específico e construtivo nas sugestões."""
        )
        
        chain = refinement_prompt | self.llm | parser
        
        try:
            refinement = chain.invoke({
                "user_profile": user_profile,
                "original_query": original_query,
                "current_response": current_response,
                "missing_aspects": "\n".join(f"- {aspect}" for aspect in quality.missing_aspects),
                "format_instructions": parser.get_format_instructions()
            })
            return refinement
        except Exception as e:
            # Fallback
            return RefinementSuggestion(
                focus_areas=quality.missing_aspects or ["Detalhar mais as recomendações"],
                additional_questions=["Pode fornecer mais detalhes sobre os preços?"]
            )
    
    def _build_refinement_query(
        self,
        original_query: str,
        refinement: RefinementSuggestion,
        previous_response: str
    ) -> str:
        """Constrói uma query refinada para a próxima iteração"""
        query_parts = [
            "Considerando sua resposta anterior, por favor aprimore e expanda focando em:",
            ""
        ]
        
        for area in refinement.focus_areas:
            query_parts.append(f"- {area}")
        
        query_parts.append("\nPerguntas adicionais a responder:")
        for question in refinement.additional_questions:
            query_parts.append(f"- {question}")
        
        query_parts.append(f"\nMantenha o foco na pergunta original: {original_query}")
        
        return "\n".join(query_parts)
    
    def _generate_intermediate_questions(
        self,
        main_question: str,
        user_profile: str
    ) -> List[str]:
        """Gera perguntas intermediárias para Self-Ask"""
        prompt = ChatPromptTemplate.from_template(
            """Você precisa responder a seguinte pergunta principal sobre seguros de carro:

PERGUNTA PRINCIPAL: {main_question}

PERFIL DO USUÁRIO: {user_profile}

Para responder bem essa pergunta, quais são as 3-4 perguntas intermediárias
mais importantes que você deveria responder primeiro?

Liste apenas as perguntas, uma por linha, iniciando cada uma com "- ".
Seja específico e relevante ao perfil do usuário."""
        )
        
        chain = prompt | self.llm
        response = chain.invoke({
            "main_question": main_question,
            "user_profile": user_profile
        })
        
        # Extrai as perguntas do texto
        lines = response.content.strip().split("\n")
        questions = [line.strip("- ").strip() for line in lines if line.strip().startswith("-")]
        
        return questions[:4]  # Limita a 4 perguntas
    
    def _synthesize_final_answer(
        self,
        main_question: str,
        intermediate_qa: List[Dict[str, str]],
        system_prompt: str,
        user_profile: str
    ) -> str:
        """Sintetiza resposta final baseada em perguntas intermediárias"""
        qa_text = "\n\n".join([
            f"P: {item['question']}\nR: {item['answer']}"
            for item in intermediate_qa
        ])
        
        synthesis_prompt = f"""Baseando-se nas seguintes análises intermediárias, forneça uma resposta
completa e integrada para a pergunta principal do usuário.

PERFIL DO USUÁRIO:
{user_profile}

PERGUNTA PRINCIPAL:
{main_question}

ANÁLISES INTERMEDIÁRIAS:
{qa_text}

Forneça uma resposta final coesa, bem estruturada e acionável."""
        
        return self._generate_response(
            system_prompt=system_prompt,
            user_query=synthesis_prompt,
            conversation_history=[]
        )
    
    def _synthesize_perspectives(
        self,
        query: str,
        perspectives: List[Dict[str, str]],
        user_profile: str
    ) -> str:
        """Sintetiza múltiplas perspectivas em uma resposta unificada"""
        perspectives_text = "\n\n".join([
            f"PERSPECTIVA: {item['perspective']}\n{item['response']}"
            for item in perspectives
        ])
        
        synthesis_prompt = ChatPromptTemplate.from_template(
            """Você recebeu análises de diferentes perspectivas sobre seguros automotivos.
Sintetize essas análises em uma resposta única, coesa e equilibrada.

PERFIL DO USUÁRIO:
{user_profile}

PERGUNTA ORIGINAL:
{query}

ANÁLISES POR PERSPECTIVA:
{perspectives_text}

Forneça uma síntese que:
1. Integre os pontos-chave de todas as perspectivas
2. Seja bem estruturada e fácil de entender
3. Destaque trade-offs importantes
4. Forneça recomendações claras e acionáveis"""
        )
        
        chain = synthesis_prompt | self.llm
        response = chain.invoke({
            "user_profile": user_profile,
            "query": query,
            "perspectives_text": perspectives_text
        })
        
        return response.content
