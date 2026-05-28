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

Arquivo: iadvogado/services/ocr_worker.py
Síntese: Módulo de extração de texto para documentos PDF nativos (via pypdf) e imagens digitalizadas (OCR via pytesseract).

Histórico de alterações:
- 23/05/2026 - Grupo IADvogado - Criação/atualização do arquivo.
- 28/05/2026 - Grupo IADvogado - Implementação da leitura nativa de PDFs selecionáveis.
"""

from PIL import Image
import pytesseract
import io

# Simple OCR wrapper. For production consider using external OCR services for better accuracy.

def image_bytes_to_text(image_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    # You can add preprocessing here
    text = pytesseract.image_to_string(image, lang='por')
    return text

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text.strip()