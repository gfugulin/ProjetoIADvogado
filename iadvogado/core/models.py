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

Arquivo: iadvogado/core/models.py
Síntese: Modelos de dados Pydantic para validação das requisições e respostas da API do IADvogado.

Histórico de alterações:
- 23/05/2026 - Grupo IADvogado - Criação/atualização do arquivo.
- 28/05/2026 - Grupo IADvogado - Ajuste nas propriedades dos modelos de dados.
"""

from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    process_number: Optional[str] = None
    user_id: Optional[str] = None

class SimplifyResponse(BaseModel):
    what_happened: str
    what_it_means: str
    what_to_do_now: str
    disclaimer: str