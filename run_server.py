#!/usr/bin/env python3
"""
Script alternativo para iniciar o servidor - execute da raiz do projeto
"""

import sys
import os

# Garantir que estamos no diretório correto
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

import uvicorn
from iadvogado.api.main import app
from iadvogado.config.config import settings
import logging

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    logger = logging.getLogger("IADvogado")
    logger.info(f"🚀 Iniciando IADvogado em http://{settings.fastapi_host}:{settings.fastapi_port}")
    logger.info(f"📱 Chatbot disponível em http://localhost:{settings.fastapi_port}/")
    uvicorn.run(
        "iadvogado.api.main:app",
        host=settings.fastapi_host,
        port=settings.fastapi_port,
        reload=True,
        log_level="info"
    )

