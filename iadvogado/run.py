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

Arquivo: iadvogado/run.py
Síntese: Ponto de entrada secundário para inicialização do servidor FastAPI do IADvogado com ajustes automáticos de path.

Histórico de alterações:
- 23/05/2026 - Grupo IADvogado - Criação/atualização do arquivo.
- 28/05/2026 - Grupo IADvogado - Ajustes de path e caminhos absolutos.
"""

import sys
import os

# Adicionar o diretório raiz do projeto ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Garantir que o diretório raiz está no path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Mudar para o diretório raiz para garantir imports corretos
os.chdir(parent_dir)

import uvicorn
from iadvogado.api.main import app
from iadvogado.config.config import settings

if __name__ == "__main__":
    print(f"🚀 Iniciando IADvogado em http://{settings.fastapi_host}:{settings.fastapi_port}")
    print(f"📱 Chatbot disponível em http://localhost:{settings.fastapi_port}/")
    print(f"📚 API Docs: http://localhost:{settings.fastapi_port}/docs")
    uvicorn.run(
        "iadvogado.api.main:app",
        host=settings.fastapi_host,
        port=settings.fastapi_port,
        reload=True
    )


