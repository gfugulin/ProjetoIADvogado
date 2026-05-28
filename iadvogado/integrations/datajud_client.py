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

Arquivo: iadvogado/integrations/datajud_client.py
Síntese: Cliente de integração processual com a API Pública do DataJud (CNJ) com resolução e mapeamento de aliases de tribunais.

Histórico de alterações:
- 23/05/2026 - Grupo IADvogado - Criação/atualização do arquivo.
- 28/05/2026 - Grupo IADvogado - Implementação da busca dinâmica via Elasticsearch no CNJ.
"""

import httpx
import re
import logging
from ..config.config import settings

logger = logging.getLogger(__name__)

def extract_tribunal_alias(process_number: str) -> str:
    """
    Extrai o alias do tribunal baseado no formato CNJ do número do processo.
    Formato: NNNNNNN-DD.AAAA.J.TR.OOOO
    J = Ramo da Justiça (ex: 8 = Estadual, 4 = Federal, 5 = Trabalho)
    TR = Tribunal respectivo
    """
    digits = re.sub(r'\D', '', process_number)
    if len(digits) != 20:
        return "tjsp"  # Fallback
        
    j = digits[13:14]
    tr = digits[14:16]
    
    mapping = {
        "826": "tjsp",
        "819": "tjrj",
        "813": "tjmg",
        "807": "tjdft",
        "403": "trf3",
        "401": "trf1",
        "402": "trf2",
        "404": "trf4",
        "405": "trf5",
        "406": "trf6",
        "502": "trt2",
        "515": "trt15",
        "100": "stf",
        "300": "stj",
    }
    key = f"{j}{tr}"
    return mapping.get(key, "tjsp")

async def fetch_process_metadata(process_number: str) -> dict:
    """
    Consulta metadados e movimentos públicos do processo na API DataJud do CNJ.
    """
    if not settings.datajud_api_key:
        logger.error("Chave de API do DataJud (datajud_api_key) não configurada.")
        return {"erro": "A chave de API do DataJud não está configurada. Configure DATAJUD_API_KEY para buscar processos reais."}
        
    tribunal = extract_tribunal_alias(process_number)
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{tribunal}/_search"
    
    headers = {
        "Authorization": f"APIKey {settings.datajud_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": {
            "match": {
                "numeroProcesso": process_number
            }
        }
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=10.0)
            
            if response.status_code == 200:
                data = response.json()
                hits = data.get("hits", {}).get("hits", [])
                if not hits:
                    return {"erro": "Processo não encontrado na base pública do DataJud."}
                
                # Pega o primeiro hit que corresponde ao processo
                processo = hits[0].get("_source", {})
                
                # Monta um resumo do andamento para passar ao LLM
                return format_process_for_llm(processo)
            else:
                logger.error(f"Erro DataJud: {response.status_code} - {response.text}")
                return {"erro": f"Falha na comunicação com DataJud: {response.status_code}"}
                
    except Exception as e:
        logger.error(f"Erro ao consultar DataJud: {e}")
        return {"erro": "Erro de comunicação com o tribunal."}

def format_process_for_llm(processo: dict) -> dict:
    """Extrai informações cruciais do JSON bruto do DataJud para alimentar a IA."""
    classe = processo.get("classe", {}).get("nome", "Desconhecida")
    orgao_julgador = processo.get("orgaoJulgador", {}).get("nome", "Não informado")
    data_ajuizamento = processo.get("dataAjuizamento", "")
    
    # Extrair os últimos movimentos
    movimentos_brutos = processo.get("movimentos", [])
    # Ordenar por data
    movimentos_brutos.sort(key=lambda x: x.get("dataHora", ""), reverse=True)
    
    ultimos_movimentos = []
    for mov in movimentos_brutos[:3]:  # Pega os 3 movimentos mais recentes
        data = mov.get("dataHora", "")[:10]
        nome = mov.get("nome", "Andamento")
        complementos = " ".join([c.get("descricao", "") for c in mov.get("complementosTabelados", [])])
        ultimos_movimentos.append(f"- {data}: {nome}. {complementos}")
        
    texto_contexto = (
        f"Classe Processual: {classe}\n"
        f"Órgão Julgador: {orgao_julgador}\n"
        f"Ajuizamento: {data_ajuizamento}\n"
        "Últimos Andamentos:\n" + "\n".join(ultimos_movimentos)
    )
    
    return {"sucesso": True, "texto_bruto": texto_contexto}


