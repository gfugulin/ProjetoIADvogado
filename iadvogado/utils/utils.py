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

Arquivo: iadvogado/utils/utils.py
Síntese: Funções utilitárias auxiliares para geração de disclaimers de responsabilidade civil e cálculo de expiração para conformidade com a LGPD.

Histórico de alterações:
- 23/05/2026 - Grupo IADvogado - Criação/atualização do arquivo.
- 28/05/2026 - Grupo IADvogado - Adequação do disclaimer legal brasileiro.
"""

import io
from datetime import datetime, timedelta
from ..config.config import settings

def make_disclaimer() -> str:
    return (
        "Isto é um resumo gerado automaticamente. Não substitui aconselhamento jurídico. "
        "Para orientação específica, procure a Defensoria Pública ou um advogado."
    )

def expiration_date() -> datetime:
    return datetime.utcnow() + timedelta(days=settings.data_retention_days)