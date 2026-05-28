from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000
    supabase_url: str | None = None
    supabase_key: str | None = None
    # openai_api_key: str | None = None  # Comentado - usando Llama local
    whatsapp_api_url: str | None = None
    whatsapp_api_token: str | None = None
    # Token do Hugging Face para acessar modelos gated (Llama 3.1)
    hugging_face_hub_token: str | None = None
    
    # Chave da API Pública do DataJud/CNJ
    datajud_api_key: str | None = None
    
    data_retention_days: int = 30
    ocr_engine: str = "pytesseract"
    
    # Configurações da IA (OpenRouter / Nuvem)
    openrouter_api_key: str | None = None
    openrouter_model: str = "openrouter/free"
    
    # Configurações do LLM Local (Desativado/Legado)
    
    # Configurações do Edge TTS
    tts_provider: str = "edge"  # edge, google, amazon
    tts_voice: str = "pt-BR-FranciscaNeural"  # Voz padrão
    tts_rate: str = "+5%"  # Velocidade: -100% a +200%
    tts_volume: str = "+0%"  # Volume: -100% a +100%
    tts_pitch: str = "+2Hz"  # Tom: -100Hz a +100Hz
    tts_use_ssml: bool = True  # Usar SSML para melhor qualidade
    tts_cache_enabled: bool = True  # Cache de áudios
    tts_cache_ttl: int = 3600  # TTL do cache em segundos

    class Config:
        # Buscar .env na raiz do projeto e também em iadvogado/config/
        env_file = [
            ".env",  # Raiz do projeto
            os.path.join(os.path.dirname(__file__), ".env"),  # iadvogado/config/.env
        ]
        env_file_encoding = "utf-8"

settings = Settings()