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

Arquivo: iadvogado/api/main.py
Síntese: Definição dos endpoints da API FastAPI e orquestração de upload, OCR, processamento processual e síntese de voz.

Histórico de alterações:
- 23/05/2026 - Grupo IADvogado - Criação/atualização do arquivo.
- 28/05/2026 - Grupo IADvogado - Implementação do endpoint /process-number e integração do DataJud.
"""

from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from ..services.ocr_worker import image_bytes_to_text
from ..services.llama_client import simplify_text  # Mudança: usando Llama ao invés de OpenAI
from ..services.edge_tts_worker import text_to_speech_bytes, edge_tts_worker  # Mudança: usando Edge TTS
from ..storage.storage import save_processing_record
from ..utils.utils import make_disclaimer, expiration_date
from ..integrations.whatsapp_adapter import send_whatsapp_text
from ..integrations.datajud_client import fetch_process_metadata
import asyncio
import logging
import os
import base64

logger = logging.getLogger(__name__)

app = FastAPI(title="IADvogado - Justiça Simples")

# Servir arquivos estáticos
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    """Redireciona para a página do chatbot"""
    chatbot_path = os.path.join(static_dir, "chatbot.html")
    if os.path.exists(chatbot_path):
        return FileResponse(chatbot_path)
    return {"message": "IADvogado API", "chatbot": "/static/chatbot.html"}

@app.post('/upload')
async def upload_document(
    background: BackgroundTasks,
    user_id: str | None = Form(None),
    phone_number: str | None = Form(None),
    file: UploadFile = File(...),
    as_audio: bool = Form(False),
):
    contents = await file.read()
    try:
        if file.filename.lower().endswith('.pdf'):
            from ..services.ocr_worker import extract_text_from_pdf
            raw_text = extract_text_from_pdf(contents)
        else:
            raw_text = image_bytes_to_text(contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OCR failed: {e}")

    simplified = await simplify_text(raw_text)
    disclaimer = make_disclaimer()
    payload_text = (
        f"O que aconteceu:\n{simplified['what_happened']}\n\n"
        f"O que significa:\n{simplified['what_it_means']}\n\n"
        f"O que fazer agora:\n{simplified['what_to_do_now']}\n\n"
        f"{disclaimer}"
    )

    # Save record asynchronously
    background.add_task(save_processing_record, user_id, raw_text, simplified, expiration_date())

    # If phone provided, send via WhatsApp (best-effort)
    if phone_number:
        try:
            await send_whatsapp_text(phone_number, payload_text)
        except Exception as e:
            # log and continue
            logger.error(f'Failed to send WhatsApp message: {e}')

        if as_audio:
            try:
                audio_bytes = await text_to_speech_bytes(payload_text)
                logger.info(f"Áudio gerado com sucesso: {len(audio_bytes)} bytes")
                # TODO: Implementar envio de áudio via WhatsApp
                # background.add_task(send_whatsapp_audio, phone_number, audio_bytes)
            except Exception as e:
                logger.error(f'Erro ao gerar áudio: {e}')

    # Gerar áudio se solicitado (mesmo sem WhatsApp)
    audio_base64 = None
    if as_audio:
        try:
            audio_bytes = await text_to_speech_bytes(payload_text)
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            logger.info(f"Áudio gerado com sucesso: {len(audio_bytes)} bytes")
        except Exception as e:
            logger.error(f'Erro ao gerar áudio: {e}')

    response = {"success": True, "text": payload_text}
    if audio_base64:
        response["audio_base64"] = audio_base64
        response["audio_format"] = "mp3"
    
    return JSONResponse(response)

@app.post('/process-number')
async def process_by_number(
    background: BackgroundTasks,
    process_number: str = Form(...), 
    user_id: str | None = Form(None), 
    phone_number: str | None = Form(None), 
    as_audio: bool = Form(False)
):
    """
    Consulta o processo na API Pública do DataJud, obtém os andamentos
    e utiliza o Llama 3.1 para simplificar o 'juridiquês' para o usuário.
    """
    logger.info(f"Iniciando consulta ao DataJud para o processo: {process_number}")
    
    # 1. Buscar metadados no DataJud
    datajud_result = await fetch_process_metadata(process_number)
    
    if "erro" in datajud_result:
        raise HTTPException(status_code=404, detail=datajud_result["erro"])
        
    raw_text = datajud_result.get("texto_bruto", "")
    
    # 2. Simplificar o texto retornado usando o LLM Local
    try:
        simplified = await simplify_text(raw_text)
    except Exception as e:
        logger.error(f"Erro na simplificação via LLM: {e}")
        raise HTTPException(status_code=500, detail="Erro ao simplificar os andamentos do processo.")

    disclaimer = make_disclaimer()
    payload_text = (
        f"O que aconteceu no processo:\n{simplified['what_happened']}\n\n"
        f"O que significa:\n{simplified['what_it_means']}\n\n"
        f"O que fazer agora:\n{simplified['what_to_do_now']}\n\n"
        f"{disclaimer}"
    )

    # 3. Salvar o histórico
    background.add_task(save_processing_record, user_id, raw_text, simplified, expiration_date())

    # 4. Envio opcional via WhatsApp
    if phone_number:
        try:
            await send_whatsapp_text(phone_number, payload_text)
        except Exception as e:
            logger.error(f'Falha ao enviar WhatsApp: {e}')

    # 5. Gerar áudio se solicitado
    audio_base64 = None
    if as_audio:
        try:
            audio_bytes = await text_to_speech_bytes(payload_text)
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            logger.info(f"Áudio gerado com sucesso: {len(audio_bytes)} bytes")
        except Exception as e:
            logger.error(f'Erro ao gerar áudio: {e}')

    response = {"success": True, "text": payload_text}
    if audio_base64:
        response["audio_base64"] = audio_base64
        response["audio_format"] = "mp3"
    
    return JSONResponse(response)

@app.get('/health')
async def health():
    return {"status": "ok"}

@app.get('/health/tts')
async def health_tts():
    """Health check específico para o sistema TTS"""
    try:
        # Testar geração de áudio
        test_audio = await text_to_speech_bytes("Teste de saúde do TTS")
        metrics = edge_tts_worker.get_metrics()
        cache_info = edge_tts_worker.get_cache_info()
        
        return {
            "status": "ok",
            "tts_provider": "edge",
            "audio_size": len(test_audio),
            "voice": edge_tts_worker.voice,
            "metrics": metrics,
            "cache": cache_info
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@app.get('/tts/metrics')
async def get_tts_metrics():
    """Retorna métricas de performance do TTS"""
    return edge_tts_worker.get_metrics()

@app.get('/tts/cache/info')
async def get_cache_info():
    """Retorna informações sobre o cache de áudio"""
    return edge_tts_worker.get_cache_info()

@app.post('/tts/cache/clear')
async def clear_cache():
    """Limpa o cache de áudio"""
    removed_count = edge_tts_worker.clear_cache()
    return {
        "success": True,
        "removed_files": removed_count,
        "message": f"Cache limpo: {removed_count} arquivos removidos"
    }
