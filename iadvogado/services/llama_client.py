"""
Projeto: IADvogado
Disciplina: Inteligência Artificial - 7º Período - Ciência da Computação
Instituição: Universidade Presbiteriana Mackenzie
Professor: Prof. Dr. Ivan Carlos Alcântara de Oliveira

Integrantes:
- Gustavo Fugulin Soares da Silva - RA 10418552
- Otto Martins Mota - RA 10418170
- Renan Garrido - RA 10417093
- Rodrigo Roveratti Guerrero - RA 10417090

Arquivo: iadvogado/services/llama_client.py
Síntese: Cliente de simplificação textual em nuvem via API do OpenRouter com tolerância a falhas, rate-limits e fallbacks.

Histórico de alterações:
- 23/05/2026 - Grupo IADvogado - Criação/atualização do arquivo.
- 28/05/2026 - Grupo IADvogado - Migração para nuvem com OpenRouter Llama 3.3 70B e fallbacks dinâmicos.
"""

import httpx
import json
import re
import asyncio
import logging
from typing import Dict
from ..config.config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_system_prompt(level: str | None = None) -> str:
    """Retorna o prompt do sistema apropriado com base no nível cognitivo selecionado"""
    base_prompt = (
        "Você é um assistente jurídico brasileiro especializado em traduzir documentos "
        "jurídicos para linguagem clara e acessível.\n\n"
        "Regras obrigatórias:\n"
        "1. Responda APENAS com um JSON válido, sem texto antes ou depois\n"
        "2. O JSON deve ter exatamente 3 chaves: \"what_happened\", \"what_it_means\", \"what_to_do_now\"\n"
        "3. Seja específico — mencione valores, datas, nomes e prazos presentes no documento\n"
        "4. Em \"what_to_do_now\", dê orientações práticas e concretas\n"
    )

    if level == "easy":
        level_rules = (
            "5. Use a LINGUAGEM MAIS SIMPLES POSSÍVEL. Evite QUALQUER jargão, latim ou termo formal.\n"
            "6. Explique como se estivesse conversando com uma pessoa de baixíssima escolaridade. Use frases curtas, analogias cotidianas e vocabulário extremamente simples."
        )
    elif level == "technical":
        level_rules = (
            "5. Mantenha os TERMOS JURÍDICOS ORIGINAIS relevantes, mas explique a fundamentação teórica de cada um de forma clara e estruturada.\n"
            "6. Ideal para estudantes ou assistentes sociais que precisam entender os artigos citados e o embasamento legal específico no documento."
        )
    else: # normal / default
        level_rules = (
            "5. Use linguagem simples e direta, como se explicasse para alguém sem formação jurídica.\n"
            "6. Explique brevemente os termos técnicos essenciais quando surgirem no texto."
        )

    return f"{base_prompt}{level_rules}\n\nExemplo de formato:\n{{\"what_happened\": \"...\", \"what_it_means\": \"...\", \"what_to_do_now\": \"...\"}}"

class OpenRouterClient:
    """Cliente leve para consumir modelos em nuvem via OpenRouter"""
    
    def __init__(self):
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = settings.openrouter_model
        
    async def simplify_text(self, text: str, level: str | None = None) -> Dict[str, str]:
        if not settings.openrouter_api_key:
            logger.error("Chave de API do OpenRouter não configurada.")
            return self._fallback_response(text)
            
        logger.info(f"Enviando documento de {len(text)} caracteres (Nível: {level}) via OpenRouter...")
        
        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "IADvogado",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [
                {"role": "system", "content": get_system_prompt(level)},
                {"role": "user", "content": f"Simplifique este texto jurídico:\n\n{text}"}
            ]
        }
        
        models_to_try = [
            self.model, 
            "openrouter/free",
            "meta-llama/llama-3.3-70b-instruct:free",
            "meta-llama/llama-3.2-3b-instruct:free", 
            "google/gemma-2-9b-it:free",
            "qwen/qwen-2.5-7b-instruct:free",
            "deepseek/deepseek-r1:free"
        ]
        
        # Deduplicar preservando a ordem
        unique_models = []
        for m in models_to_try:
            if m and m not in unique_models:
                unique_models.append(m)
        models_to_try = unique_models
        
        # Estratégia de retry: para cada modelo, tenta até 2 vezes com espera entre tentativas.
        # O OpenRouter retorna retry_after_seconds ~1s nos erros 429, então 3s de espera é seguro.
        MAX_RETRIES_PER_MODEL = 2
        RETRY_DELAY_SECONDS = 3
        
        try:
            async with httpx.AsyncClient(timeout=90.0) as client:
                for model_index, current_model in enumerate(models_to_try):
                    payload["model"] = current_model
                    
                    for attempt in range(1, MAX_RETRIES_PER_MODEL + 1):
                        logger.info(f"Tentativa {attempt}/{MAX_RETRIES_PER_MODEL} com modelo {current_model}...")
                        response = await client.post(self.api_url, headers=headers, json=payload)
                        
                        if response.status_code == 200:
                            data = response.json()
                            raw_response = data['choices'][0]['message']['content']
                            logger.info(f"✅ Resposta recebida com sucesso (Modelo: {current_model}, Tentativa: {attempt}).")
                            parsed_response = self._parse_response(raw_response)
                            parsed_response = self._fill_empty_fields(parsed_response, text)
                            return parsed_response
                        
                        if response.status_code == 429:
                            # Extrair tempo de espera sugerido pelo OpenRouter nos cabeçalhos HTTP ou no corpo JSON
                            wait_time = RETRY_DELAY_SECONDS
                            try:
                                # 1. Tenta cabeçalho HTTP padrão "Retry-After"
                                retry_header = response.headers.get("Retry-After") or response.headers.get("retry-after")
                                if retry_header:
                                    wait_time = float(retry_header)
                                else:
                                    # 2. Tenta metadados JSON do OpenRouter
                                    err_data = response.json()
                                    wait_time = err_data.get('error', {}).get('metadata', {}).get('retry_after_seconds', RETRY_DELAY_SECONDS)
                                wait_time = max(float(wait_time), 1.0)
                            except Exception:
                                wait_time = RETRY_DELAY_SECONDS
                            
                            logger.warning(f"⏳ Modelo {current_model} rate-limited (429). Aguardando {wait_time:.0f}s antes de retry...")
                            await asyncio.sleep(wait_time)
                            continue  # Retenta o MESMO modelo
                        
                        # Qualquer outro erro (404, 502, etc) → pula para o próximo modelo
                        logger.warning(f"❌ Modelo {current_model} falhou (HTTP {response.status_code}). Pulando para próximo...")
                        break  # Sai do loop de retries e vai para o próximo modelo
                
                logger.error("Todos os modelos gratuitos falharam após múltiplas tentativas.")
                return self._fallback_response(text)
                
        except Exception as e:
            logger.error(f"Erro ao comunicar com OpenRouter: {e}")
            return self._fallback_response(text)
            
    def _parse_response(self, response: str) -> Dict[str, str]:
        """Extrai o JSON da resposta do modelo"""
        try:
            response = response.strip()
            # Remover possíveis blocos markdown de json
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
                
            # Regex robusto para extrair JSON
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                json_str = json_str.replace('\n', ' ').replace('\r', '')
                parsed = json.loads(json_str)
                
                required_keys = ['what_happened', 'what_it_means', 'what_to_do_now']
                if all(key in parsed for key in required_keys):
                    return {
                        'what_happened': str(parsed['what_happened']).strip(),
                        'what_it_means': str(parsed['what_it_means']).strip(),
                        'what_to_do_now': str(parsed['what_to_do_now']).strip(),
                    }
            
            # Se não achou JSON válido, faz fallback estruturado
            return self._semantic_parse(response)
        except Exception as e:
            logger.warning(f"Erro no parse JSON: {e}")
            return self._semantic_parse(response)
            
    def _semantic_parse(self, response: str) -> Dict[str, str]:
        # Versão simplificada para capturar o que o modelo responder fora do JSON
        return {
            'what_happened': response,
            'what_it_means': "Não foi possível extrair o significado estruturado.",
            'what_to_do_now': "Consulte um especialista para análise detalhada."
        }
        
    def _fallback_response(self, text: str) -> Dict[str, str]:
        return {
            'what_happened': "Ocorreu um erro ao comunicar com a inteligência artificial na nuvem.",
            'what_it_means': "A chave de API pode estar inválida ou o serviço está temporariamente indisponível.",
            'what_to_do_now': "Por favor, verifique a sua conexão, confirme sua chave de API e tente novamente."
        }
        
    def _fill_empty_fields(self, result: Dict[str, str], text: str) -> Dict[str, str]:
        if not result.get('what_happened'): result['what_happened'] = "Análise indisponível."
        if not result.get('what_it_means'): result['what_it_means'] = "Análise indisponível."
        if not result.get('what_to_do_now'): result['what_to_do_now'] = "Procure orientação especializada."
        return result

# Instância global para manter compatibilidade com o código antigo
llama_client = OpenRouterClient()

async def simplify_text(text: str, level: str | None = None) -> Dict[str, str]:
    """Interface principal, agora rodando via OpenRouter de forma 100% assíncrona"""
    return await llama_client.simplify_text(text, level)
