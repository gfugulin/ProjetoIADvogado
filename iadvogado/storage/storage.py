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

Arquivo: iadvogado/storage/storage.py
Síntese: Inicialização e gravação de histórico de análises de documentos no banco de dados local SQLite.

Histórico de alterações:
- 23/05/2026 - Grupo IADvogado - Criação/atualização do arquivo.
- 28/05/2026 - Grupo IADvogado - Transição completa para persistência ágil local em SQLite.
"""

import sqlite3
import json
import os
from ..config.config import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Configurar caminho do banco de dados local
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "database.db")

def _init_db():
    """Inicializa o banco de dados SQLite local garantindo que a tabela exista."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS processes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    raw_text TEXT,
                    simplified TEXT,
                    retention_until TEXT,
                    created_at TEXT
                )
            """)
            conn.commit()
    except Exception as e:
        logger.error(f"Erro ao inicializar SQLite local: {e}")

# Inicializa no momento do import
_init_db()

async def save_processing_record(user_id: str | None, raw_text: str, simplified: dict, retention_until: datetime):
    """Salva o histórico da análise no banco de dados SQLite local de forma segura."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO processes (user_id, raw_text, simplified, retention_until, created_at) VALUES (?, ?, ?, ?, ?)",
                (
                    user_id,
                    raw_text,
                    json.dumps(simplified, ensure_ascii=False),
                    retention_until.isoformat(),
                    datetime.utcnow().isoformat()
                )
            )
            conn.commit()
            logger.info("Registro salvo com sucesso no banco de dados local (SQLite).")
            return cursor.lastrowid
    except Exception as e:
        logger.error(f"Erro ao salvar no banco local: {e}")
        return None