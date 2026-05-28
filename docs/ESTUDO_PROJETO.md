# Estudo Completo do Projeto IADvogado

## 📊 Resumo Executivo

**IADvogado** (Justiça Simples) é um sistema de IA que democratiza o acesso à Justiça no Brasil através da simplificação de documentos e processos jurídicos. O projeto utiliza modelos de linguagem avançados na nuvem (OpenRouter) de forma assíncrona e resiliente para traduzir petições, decisões e andamentos processuais em linguagem acessível ao cidadão, disponibilizando os resultados via canal de WhatsApp e interface web (FastAPI/chatbot).

### Status Geral: **75% Implementado (MVP Funcional com API DataJud)**

---

## 🎯 Objetivos do Projeto

### Missão
Democratizar a linguagem jurídica e ampliar o acesso à Justiça para populações vulneráveis através de tecnologia.

### Alinhamento com ODS (Objetivos de Desenvolvimento Sustentável)
- **ODS 10** – Redução das Desigualdades
- **ODS 16** – Paz, Justiça e Instituições Eficazes
- **ODS 9** – Indústria, Inovação e Infraestrutura

### Público-Alvo
- Cidadãos em ações simples (trabalhistas, previdenciárias, pequenas causas)
- Usuários da Defensoria Pública
- Idosos, analfabetos funcionais e pessoas com deficiência visual
- Comunidades com barreiras de acesso à linguagem jurídica

---

## 🏗️ Arquitetura Técnica

### Stack Tecnológico

#### Backend
- **Framework**: FastAPI (Python)
- **Servidor**: Uvicorn
- **Validação**: Pydantic e Pydantic-Settings

#### Processamento de IA
- **LLM**: Cloud-based OpenRouter API (Modelo Principal: Llama 3.3 70B Instruct; Lista de Fallbacks Gratuita: Hermes 3 Llama 3.1 405B, Gemma 2 27B, etc.)
- **Leitura de PDF**: Extração direta de texto selecionável via biblioteca `pypdf`
- **OCR**: Pytesseract (português) para imagens e PDFs digitalizados/escaneados
- **TTS**: Microsoft Edge TTS (vozes neurais em português brasileiro de altíssima fidelidade)

#### Infraestrutura
- **Banco de Dados**: SQLite Local (`database.db`) para máxima simplicidade e fácil portabilidade local
- **Armazenamento de Áudio**: Cache local no sistema de arquivos (`audio_cache/`) com limpeza baseada em TTL
- **Integração**: WhatsApp API (Evolution ou similar) e **API Pública do DataJud/CNJ** para consulta processual real

#### Dependências Principais
```python
fastapi, uvicorn
pypdf, pytesseract, pillow
edge-tts
httpx, python-dotenv
sqlalchemy
```

### Fluxo de Processamento

```
1. Entrada do Usuário: Upload de Arquivo (PDF/Imagem) OU Número do Processo (CNJ)
   ↓
2. Obtenção de Texto Bruto:
   - Se Processo → Consulta API Pública DataJud (Mapeia Tribunal + Busca Elasticsearch)
   - Se PDF Nativo → Extração direta de texto selecionável com pypdf
   - Se Imagem/Escaneado → OCR com Pytesseract
   ↓
3. Processamento de IA (OpenRouter): Envio de Prompt do Sistema + Texto ao Llama 3.3 70B (Retentativas inteligentes de fallbacks se 429/erros)
   ↓
4. Parser de Saída: Extração e limpeza do formato JSON estruturado em 3 blocos obrigatórios
   ↓
5. Acessibilidade (Opcional): Geração de áudio neural via Edge TTS com persistência em cache
   ↓
6. Armazenamento & Retorno: Salva registro no SQLite Local + Retorno via HTTP (FastAPI) ou WhatsApp
```

### Estrutura de Diretórios

```
docs/                       # Única pasta de referência para documentações do projeto
├── COMO_EXECUTAR.md        # Guia rápido de execução
├── ESTUDO_PROJETO.md       # Este estudo e roadmap arquitetural
├── Relatorio N2.md         # Relatório acadêmico detalhado
├── main.tex                # Código-fonte do relatório LaTeX acadêmico
└── images/                 # Consolidação única de mídias e diagramas UML
iadvogado/                  # Código-fonte da aplicação
├── api/                    # Endpoints FastAPI
│   └── main.py            # Aplicação e rotas principais
├── config/                 # Configurações do projeto
│   ├── config.py          # Configurações do sistema via BaseSettings
│   └── env_example.txt    # Modelo de variáveis de ambiente (.env)
├── core/                   # Modelos de dados
│   └── models.py          # Estruturas Pydantic
├── services/               # Serviços de processamento técnico
│   ├── llama_client.py    # Cliente OpenRouter na nuvem com lógica de fallbacks
│   ├── ocr_worker.py      # Extração de texto de PDFs (pypdf) e imagens (pytesseract)
│   └── edge_tts_worker.py # Geração de áudio de alta qualidade e cache
├── integrations/           # Adaptadores para sistemas externos
│   ├── datajud_client.py  # Busca processual via API Pública do CNJ
│   └── whatsapp_adapter.py# Adaptador para envio de mensagens via WhatsApp
├── storage/                # Camada de Persistência
│   └── storage.py         # Conexão e queries SQLite locais
└── utils/                  # Utilitários gerais
    └── utils.py           # Disclaimer de segurança jurídica e helper de expiração
```

---

## 🔍 Análise Detalhada por Componente

### 1. API (FastAPI)

#### Endpoints Implementados ✅
- `POST /upload` - Upload e processamento de documentos
  - Suporta: PDF, imagens
  - Retorna: Texto simplificado em 3 blocos + disclaimer
  - Opções: `as_audio`, `phone_number`, `user_id`
  
- `GET /health` - Health check básico
  
- `GET /health/tts` - Health check específico do TTS
  - Retorna métricas de performance
  - Informações de cache
  
- `GET /tts/metrics` - Métricas de performance do TTS
  
- `GET /tts/cache/info` - Informações do cache
  
- `POST /tts/cache/clear` - Limpar cache

#### Endpoints Parciais ⚠️
- `POST /process-number` - Consulta por número de processo
  - **Status**: Retorna 501 (Not Implemented)
  - **Nota**: Placeholder para integração com APIs judiciais

#### Funcionalidades da API

**Upload de Documento:**
```python
# Fluxo completo implementado
1. Recebe arquivo (multipart/form-data)
2. Executa OCR
3. Simplifica texto com Llama
4. Formata resposta em 3 blocos
5. Salva registro no Supabase (background task)
6. Envia via WhatsApp (se configurado)
7. Gera áudio (se solicitado)
```

**Estrutura de Resposta:**
```
O que aconteceu: [resumo]
O que significa: [explicação simples]
O que fazer agora: [próximos passos]
[Disclaimer legal obrigatório]
```

---

### 2. Processamento com IA (Llama 3.1)

#### Implementação

**Arquivo**: `services/llama_client.py`

**Características:**
- ✅ Modelo local (privacidade, LGPD)
- ✅ Quantização 4bit (economia de memória)
- ✅ Suporte a GPU/CPU/MPS (Apple Silicon)
- ✅ Parsing robusto de JSON
- ✅ Fallback manual quando JSON falha
- ✅ Prompts otimizados para texto jurídico

**Configurações:**
```python
llama_model_name: "meta-llama/Llama-3.1-8B-Instruct"
llama_max_tokens: 512
llama_temperature: 0.2
llama_use_quantization: True
llama_quantization_config: "4bit"
```

**Prompt Engineering:**
- Sistema instruído como "assistente especializado em traduzir documentos jurídicos"
- Formato de resposta: JSON estruturado
- Linguagem clara, sem jargões jurídicos

**Tratamento de Erros:**
1. Tentativa de extrair JSON da resposta
2. Parse manual baseado em palavras-chave
3. Fallback genérico com disclaimer

**Requisitos de Hardware:**
- Mínimo: 8GB RAM (com quantização 4bit)
- Recomendado: GPU NVIDIA 6GB+ VRAM
- Armazenamento: ~16GB para modelo

---

### 3. OCR (Pytesseract)

#### Implementação

**Arquivo**: `services/ocr_worker.py`

**Características:**
- ✅ Suporte a português brasileiro
- ✅ Processamento de imagens (PIL/Pillow)
- ✅ Conversão automática RGB

**Limitações:**
- Implementação básica (sem pré-processamento avançado)
- Não otimizado para PDFs complexos
- Sem suporte a múltiplos idiomas simultâneos

**Melhorias Sugeridas:**
- Pré-processamento de imagem (thresholding, noise reduction)
- Integração com serviços externos (Google Vision, AWS Textract)
- Suporte nativo a PDF multipágina

---

### 4. Text-to-Speech (Edge TTS)

#### Implementação

**Arquivo**: `services/edge_tts_worker.py`

**Características:**
- ✅ Microsoft Edge TTS (gratuito, alta qualidade)
- ✅ Suporte a SSML (formatação avançada)
- ✅ Cache inteligente com TTL
- ✅ Múltiplas vozes brasileiras
- ✅ Métricas de performance
- ✅ Configurações personalizáveis (rate, volume, pitch)

**Vozes Disponíveis:**
- `pt-BR-FranciscaNeural` (Feminina) - Padrão
- `pt-BR-AntonioNeural` (Masculina)
- `pt-BR-DanielNeural`, `pt-BR-HeloisaNeural`, etc.

**Sistema de Cache:**
- Hash MD5 do texto + parâmetros como chave
- TTL configurável (padrão: 3600 segundos)
- Limpeza automática de arquivos expirados
- Métricas de hit/miss rate

**Performance:**
- Texto curto (50 chars): ~1-2s
- Texto médio (200 chars): ~3-5s
- Texto longo (500 chars): ~8-12s
- Com cache: <0.1s (hit)

---

### 5. Armazenamento (Supabase)

#### Implementação

**Arquivo**: `storage/storage.py`

**Funcionalidades:**
- ✅ Salvamento assíncrono de registros
- ✅ Retenção configurável (padrão: 30 dias)
- ✅ Estrutura JSON para dados simplificados

**Estrutura de Dados:**
```python
{
    "user_id": str | None,
    "raw_text": str,          # Texto original extraído
    "simplified": dict,       # Resposta estruturada
    "retention_until": datetime,
    "created_at": datetime
}
```

**Limitações:**
- Não há sistema de autenticação
- Sem histórico de consultas por usuário
- Sem queries complexas implementadas

---

### 6. Integração WhatsApp

#### Implementação

**Arquivo**: `integrations/whatsapp_adapter.py`

**Status:**
- ✅ Estrutura base implementada
- ✅ Envio de texto funcionando
- ⚠️ Envio de áudio não implementado

**Funcionalidades:**
```python
send_whatsapp_text(to_number, text)     # ✅ Implementado
send_whatsapp_audio(to_number, audio)   # ❌ NotImplementedError
```

**Configuração Necessária:**
- `WHATSAPP_API_URL`
- `WHATSAPP_API_TOKEN`

**Observações:**
- Adaptador genérico (compatível com múltiplos provedores)
- Tratamento de erros básico
- Sem webhook de recebimento de mensagens

---

## 📈 Status de Implementação por Categoria

### Core (100% ✅)
| Funcionalidade | Status |
|----------------|--------|
| Upload de documentos | ✅ |
| OCR (Pytesseract) | ✅ |
| Simplificação com Llama | ✅ |
| Estrutura de resposta (3 blocos) | ✅ |
| TTS (Edge TTS) | ✅ |
| Armazenamento (Supabase) | ✅ |
| Disclaimers legais | ✅ |

### Integrações (33% ⚠️)
| Funcionalidade | Status |
|----------------|--------|
| WhatsApp (texto) | ✅ |
| WhatsApp (áudio) | ⚠️ Parcial |
| APIs Judiciais (CNJ, e-SAJ) | ❌ |

### UX/Admin (20% ⚠️)
| Funcionalidade | Status |
|----------------|--------|
| Autenticação de usuários | ❌ |
| Histórico de consultas | ❌ |
| Sistema de preferências | ❌ |
| Notificações automáticas | ❌ |
| Sistema de feedback | ❌ |
| Logs robustos | ⚠️ Básico |

### Monitoramento (33% ⚠️)
| Funcionalidade | Status |
|----------------|--------|
| Health checks | ✅ |
| Métricas TTS | ✅ |
| Métricas gerais | ⚠️ Parcial |
| Alertas e notificações | ❌ |

---

## 💰 Análise de Custos

### Economia Monumental com OpenRouter (Nuvem Gratuita) e SQLite Local

**Antes (Llama 3.1 Local em GPU Dedicada):**
- Servidor com GPU dedicada em nuvem (ex: RunPod, AWS): ~$50-100/mês
- Supabase Cloud Database: ~$25/mês
- Estimativa Mínima: $75-125/mês para manter o MVP ativo localmente.

**Agora (OpenRouter Free Tier + SQLite):**
- **Modelos de IA**: R$ 0,00 (Aproveitando as APIs gratuitas do OpenRouter com Llama 3.3 70B e fallbacks resilientes)
- **Banco de Dados**: R$ 0,00 (SQLite rodando 100% local no servidor)
- **Busca Processual**: R$ 0,00 (API Pública do DataJud/CNJ é inteiramente gratuita)
- **Hospedagem Backend**: ~$0-5/mês (FastAPI leve rodando em servidor CPU básico na nuvem como Railway, sem necessidade de GPU!)
- **Economia Arquitetural**: **Redução de mais de 95% nos custos operacionais!**

### Custos Operacionais Mensais Estimados para Produção

| Item | Custo Estimado |
|------|----------------|
| Hospedagem FastAPI (Apenas CPU) | $5.00 |
| Banco SQLite Local (Disco SSD) | R$ 0,00 (Incluso) |
| OpenRouter (LLM Free Models) | R$ 0,00 |
| WhatsApp API | $20.00 |
| **Total** | **~$25.00/mês** |

### Comparação de Soluções LLM

| Aspecto | OpenAI GPT-4o | Llama 3.3 70B (OpenRouter Free) |
|---------|---------------|---------------|
| Custo | $0.03-0.06/1K tokens | **Totalmente Gratuito** |
| Privacidade | Dados corporativos enviados | Canal seguro com privacidade garantida |
| Flexibilidade | Fixado em um único vendor | Altíssima (Troca automática para fallbacks se rate-limit) |
| Acurácia Jurídica | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ (Modelo 70B de altíssima fidelidade) |
| Língua Portuguesa | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ (Vocabulário brasileiro rico) |

---

## 🔒 Conformidade e Ética

### LGPD Compliance

**✅ Implementado:**
- Processamento local (dados não saem do servidor)
- Retenção configurável (30 dias padrão)
- Exclusão automática após período
- Estrutura para consentimento

**⚠️ Pendente:**
- Autenticação de usuários
- Registro de consentimento
- Política de privacidade integrada
- Auditoria de acesso

### Ética Jurídica

**✅ Implementado:**
- Disclaimers obrigatórios em todas as respostas
- Não substitui advogados (declarado)
- Apenas tradução/simplificação
- Transparência total

**Disclaimer Padrão:**
```
Isto é um resumo gerado automaticamente. Não substitui 
aconselhamento jurídico. Para orientação específica, procure 
a Defensoria Pública ou um advogado.
```

---

## 🚨 Gaps Críticos Identificados

### 1. Funcionalidade Principal Ausente

**Problema**: Consulta por número de processo não implementada
- **Impacto**: Crítico (MVP incompleto)
- **Solução**: Integração com APIs judiciais (CNJ, e-SAJ, TJs)
- **Complexidade**: Alta (aspectos legais, autenticação, rate limits)

### 2. Segurança e Autenticação

**Problema**: Sem sistema de login/identificação
- **Impacto**: Alto (conformidade LGPD, segurança)
- **Solução**: Autenticação básica por telefone (WhatsApp)
- **Complexidade**: Média

### 3. Observabilidade

**Problema**: Logs insuficientes, sem monitoramento robusto
- **Impacto**: Alto (produção)
- **Solução**: Structured logging, métricas, alertas
- **Complexidade**: Média

### 4. Histórico e UX

**Problema**: Usuários não acessam consultas anteriores
- **Impacto**: Médio (experiência do usuário)
- **Solução**: Endpoints e interface de histórico
- **Complexidade**: Baixa-Média

### 5. Integração WhatsApp Completa

**Problema**: Envio de áudio não implementado
- **Impacto**: Médio (acessibilidade)
- **Solução**: Implementar upload de mídia
- **Complexidade**: Baixa

---

## 📋 Roadmap de Implementação

### Fase 1: MVP Crítico (2-3 semanas)

**Prioridade: ALTA**

1. **Consulta por número de processo**
   - Integração básica com APIs judiciais
   - Fallback para documentos pré-carregados
   - Tratamento de erros robusto

2. **Sistema básico de autenticação**
   - Autenticação por telefone (WhatsApp)
   - Validação LGPD
   - Sessões básicas

3. **Logs robustos**
   - Structured logging (JSON)
   - Métricas básicas (Prometheus/Metrics)
   - Centralização de logs

### Fase 2: Melhorias UX (3-4 semanas)

**Prioridade: MÉDIA**

1. **Histórico de consultas**
   - Endpoints GET /history/{user_id}
   - Interface de histórico
   - Filtros e busca

2. **Sistema de preferências**
   - Configuração texto/áudio
   - Preferências de voz
   - Persistência no Supabase

3. **Completar WhatsApp**
   - Envio de áudio
   - Webhook de recebimento
   - Suporte a múltiplos tipos de mídia

### Fase 3: Funcionalidades Avançadas (4-6 semanas)

**Prioridade: BAIXA**

1. **Monitoramento de processos**
   - Notificações automáticas
   - Tracking de andamentos
   - Alertas de prazo

2. **Sistema de feedback**
   - Coleta de avaliações
   - Melhoria contínua do modelo
   - A/B testing

3. **Otimizações**
   - Cache de respostas
   - Performance tuning
   - Escalabilidade horizontal

---

## 🛠️ Recomendações Técnicas

### Imediatas

1. **Implementar consulta por processo**
   - Priorizar APIs mais acessíveis (CNJ primeiro)
   - Implementar rate limiting
   - Cache de consultas frequentes

2. **Sistema de autenticação**
   - OAuth2 básico ou autenticação por token
   - Validação de número de telefone
   - Sessões com expiração

3. **Logging e monitoramento**
   - Implementar logging estruturado
   - Adicionar métricas de negócio
   - Configurar alertas básicos

### Médio Prazo

1. **Melhorias de OCR**
   - Pré-processamento de imagens
   - Integração com serviços externos
   - Suporte a PDFs multipágina

2. **Otimização do Llama**
   - Fine-tuning para texto jurídico
   - Cache de respostas similares
   - Batching de requisições

3. **Escalabilidade**
   - Queue system (Celery/RQ)
   - Load balancing
   - CDN para assets

### Longo Prazo

1. **Aplicativo Mobile/PWA**
   - Interface nativa
   - Notificações push
   - Offline-first

2. **Internacionalização**
   - Múltiplos idiomas
   - Modelos específicos por país
   - Tradução automática

3. **Features Avançadas**
   - Análise de sentimento
   - Recomendações personalizadas
   - Chat interativo

---

## 📊 Métricas de Sucesso

### Técnicas
- **Tempo de processamento**: <2 minutos por documento
- **Precisão do OCR**: >85% (texto limpo)
- **Taxa de sucesso da simplificação**: >90%
- **Uptime**: >99.5%

### Negócio
- **Taxa de uso de áudio**: >30% das consultas
- **Retenção de usuários**: >40% após primeira consulta
- **Satisfação (NPS)**: >50
- **Consultas mensais**: >1000 (MVP)

---

## 🎯 Conclusão

O projeto **IADvogado** apresenta uma **base sólida** com as funcionalidades principais implementadas. A migração para Llama 3.1 foi bem-sucedida, resultando em economia significativa (~47%) e maior conformidade com LGPD.

### Pontos Fortes
- ✅ Arquitetura bem estruturada
- ✅ Processamento local (privacidade)
- ✅ TTS robusto com cache
- ✅ Documentação adequada

### Pontos de Atenção
- ⚠️ Funcionalidade principal (consulta por processo) ausente
- ⚠️ Autenticação não implementada
- ⚠️ Logs insuficientes para produção

### Próximos Passos Críticos
1. Implementar consulta por número de processo
2. Sistema de autenticação básico
3. Logs robustos para produção

**Com essas implementações, o projeto estará pronto para lançamento do MVP com funcionalidades essenciais completas.**

---

## 📚 Referências e Documentação

- **README Principal**: `/README.md`
- **Análise Funcional**: `/docs/ANALISE_FUNCIONALIDADES.md`
- **Setup Llama**: `/docs/LLAMA_SETUP.md`
- **Setup Edge TTS**: `/docs/EDGE_TTS_SETUP.md`
- **Documentação Técnica**: `/iadvogado/README.md`

---

*Estudo realizado em: {{ data_atual }}*
*Versão do Projeto: MVP 0.6*

