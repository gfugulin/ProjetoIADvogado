# IADvogado - Sistema de IA para Simplificação de Documentos Jurídicos

## Estrutura do Projeto

```
iadvogado/
├── api/                    # Endpoints da API FastAPI
│   ├── __init__.py
│   └── main.py            # Aplicação principal FastAPI
├── config/                 # Configurações do sistema
│   ├── __init__.py
│   ├── config.py          # Settings usando Pydantic
│   └── env_example.txt    # Exemplo de variáveis de ambiente
├── core/                   # Modelos de dados e estruturas core
│   ├── __init__.py
│   └── models.py          # Modelos Pydantic
├── services/               # Serviços de IA, OCR e TTS
│   ├── __init__.py
│   ├── llama_client.py    # Cliente OpenRouter na nuvem com resiliência
│   ├── edge_tts_worker.py # Text-to-Speech usando Edge TTS e cache
│   └── ocr_worker.py      # Extração de PDF (pypdf) e imagens (pytesseract)
├── integrations/           # Integrações externas
│   ├── __init__.py
│   ├── datajud_client.py  # Busca processual via API Pública do CNJ
│   └── whatsapp_adapter.py # Integração com WhatsApp
├── storage/                # Camada de persistência local
│   ├── __init__.py
│   └── storage.py          # Queries e inicialização SQLite
├── utils/                  # Utilitários e funções auxiliares
│   ├── __init__.py
│   └── utils.py           # Disclaimer jurídico e expiração
├── __init__.py            # Pacote principal
├── run.py                 # Ponto de entrada da aplicação
└── requirements.txt       # Dependências Python
```

## Funcionalidades

### 🤖 IA e Processamento de Texto
- **Llama 3.1 8B**: Simplificação de documentos jurídicos usando modelo local
- **OCR**: Extração de texto de imagens usando Pytesseract
- **TTS**: Conversão de texto em áudio usando Microsoft Edge TTS

### 📱 Integrações
- **WhatsApp**: Envio de respostas via WhatsApp
- **Supabase**: Armazenamento de dados e histórico

### 🔧 Configuração
- Configuração via variáveis de ambiente
- Suporte a diferentes provedores de IA
- Cache inteligente para TTS

## Como Executar

1. **Instalar dependências**:
```bash
pip install -r requirements.txt
```

2. **Configurar variáveis de ambiente**:
```bash
cp config/env_example.txt .env
# Editar .env com suas configurações
```

3. **Executar a aplicação**:
```bash
python run.py
```

## Endpoints da API

- `POST /upload` - Upload e processamento de documentos
- `POST /process-number` - Processamento por número do processo
- `GET /health` - Health check geral
- `GET /health/tts` - Health check específico do TTS
- `GET /tts/metrics` - Métricas de performance do TTS
- `GET /tts/cache/info` - Informações do cache
- `POST /tts/cache/clear` - Limpar cache

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **OpenRouter (Llama 3.3 70B)**: Inferência de IA resiliente baseada na nuvem
- **DataJud API / CNJ**: Busca e integração de processos reais
- **pypdf**: Extração nativa ultrarrápida de textos em PDF
- **Pytesseract**: OCR para extração de texto de imagens
- **Edge TTS**: Text-to-Speech com vozes neurais brasileiras de alta qualidade
- **SQLite**: Banco de dados relacional leve e local
- **Pydantic**: Validação de dados e configurações do sistema


