#!/usr/bin/env python3
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

Arquivo: run_server.py
Síntese: Script de entrada principal para inicializar o servidor FastAPI do IADvogado a partir da raiz do projeto.

Histórico de alterações:
- 23/05/2026 - Grupo IADvogado - Criação/atualização do arquivo.
- 28/05/2026 - Grupo IADvogado - Reestruturação e limpeza arquitetural.
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

