# IADvogado

## Visão Geral

Justiça Simples é uma iniciativa tecnológica que busca democratizar o acesso à Justiça no Brasil por meio de Inteligência Artificial. A proposta consiste em um sistema capaz de traduzir documentos jurídicos — petições, decisões e andamentos processuais — em linguagem clara e acessível para a população.

A solução é acessível por meio de um aplicativo web dedicado (PWA) no formato de Chat Conversacional (estilo WhatsApp) e, futuramente, por meio de integração direta com aplicativos de mensageria, oferecendo respostas em formato texto e áudio para aumentar a inclusão de pessoas com baixa escolaridade, idosos e cidadãos com deficiência visual ou motora.

O projeto tem como foco principal reduzir as barreiras de entendimento que afastam os cidadãos de seus direitos, promovendo transparência e cidadania. Além disso, a iniciativa está alinhada aos seguintes Objetivos de Desenvolvimento Sustentável (ODS) da ONU:

- ODS 10 – Redução das Desigualdades  
- ODS 16 – Paz, Justiça e Instituições Eficazes  
- ODS 9 – Indústria, Inovação e Infraestrutura  

---

## Objetivos

- Democratizar a linguagem jurídica: tornar compreensíveis termos técnicos e documentos judiciais.  
- Ampliar a acessibilidade: oferecer opções de saída em texto e áudio.  
- Promover cidadania: garantir que os cidadãos compreendam os prazos, as etapas e as implicações de seus processos.  
- Suporte à Defensoria Pública e ONGs: fornecer uma ferramenta de apoio que fortaleça o atendimento a populações vulneráveis.

---

## Público-Alvo

- Cidadãos em ações simples (trabalhistas, previdenciárias, pequenas causas).  
- Usuários da Defensoria Pública.  
- Idosos, analfabetos funcionais e pessoas com deficiência visual.  
- Comunidades que enfrentam barreiras de acesso à linguagem jurídica.

---

## Funcionalidades do MVP

- Upload de documentos ou fornecimento de número do processo.  
- Tradução automática para linguagem acessível em três blocos principais:  
  1. O que aconteceu  
  2. O que significa  
  3. O que fazer agora  
- Retorno em texto no WhatsApp.  
- Geração opcional de áudio com explicação simplificada.  
- Inclusão de mensagens de responsabilidade e disclaimers legais.

---

## Arquitetura em Alto Nível

1. **Interação**: Web App PWA dedicado em formato de Chat Conversacional (com pílulas cognitivas, entrada de voz, acessibilidade visual/motora e histórico local persistido) e estrutura preparada para integração de canais de mensageria (WhatsApp).  
2. **Backend**: FastAPI em Python, servindo o PWA e APIs, com banco de dados local SQLite (`database.db`).  
3. **Processamento**:  
   - Extração nativa de texto de PDFs (`pypdf`) e OCR para imagens escaneadas (`Pytesseract`);  
   - **LLM na Nuvem (OpenRouter)**: Uso do modelo de última geração **Llama 3.3 70B Instruct** com prompts adaptativos dependendo do nível cognitivo (Fácil, Padrão ou Técnico) e contingências de fallback dinâmico;  
   - **TTS para conversão em áudio**: Microsoft Edge TTS (vozes neurais brasileiras de altíssima qualidade).  
4. **Entrega**: resposta estruturada em balões de chat e player de áudio integrado simulando nota de voz, com feedback háptico móvel.

### **Mudanças na Arquitetura (2026)**
- **Migração de IA Local para OpenRouter Cloud**: Inferência assíncrona usando o modelo robusto Llama 3.3 70B. Evita a necessidade de hardware local potente (GPU dedicada com 6GB+ VRAM, PyTorch, Transformers, etc.), reduzindo o tempo de setup local e melhorando radicalmente a qualidade da simplificação.
- **Extração Direta de PDF**: Uso da biblioteca `pypdf` para leitura direta de texto selecionável em arquivos PDF, acelerando o tempo de processamento em até 10x e evitando erros comuns de OCR.
- **Banco de Dados SQLite**: Armazenamento ágil e simplificado no banco local, dispensando dependências de serviços de nuvem complexos como Supabase para testes locais.

---

## Status de Implementação

### ✅ **Funcionalidades Implementadas**
- Redesenho Conversacional Chat-First: interface focada em calor humano com paleta acolhedora, sem emojis e com ícones SVG inline
- Acessibilidade Digital (WCAG 2.1 POUR): navegação por teclado contrastante (`:focus-visible`), tags `tabindex` e suporte a leitores de tela
- Entrada por Voz Nativa (Speech-to-Text) com Web Speech API local integrada ao campo de texto do chat
- Níveis de Tradução IA: pílulas de seleção de complexidade linguística (Fácil, Padrão, Técnico) no chat e prompts dinâmicos
- Feedback háptico (Vibration API) para eventos de sucesso em dispositivos móveis
- Suporte a instalação e caching offline PWA (Service Worker e Manifesto integrados ao FastAPI)
- Histórico de conversas completas agrupadas por threads persistidas em local storage
- Upload e processamento inteligente de documentos (PDF nativo e imagens)
- Extração de texto selecionável direta com `pypdf`
- OCR com Pytesseract (português) para imagens e PDFs escaneados
- Consulta processual real integrada à **API Pública do DataJud/CNJ** (com mapeamento de tribunais)
- Simplificação de texto jurídico na nuvem via OpenRouter (Llama 3.3 70B-Instruct)
- Estrutura de resposta em 4 blocos (O que aconteceu, O que significa, Próximos passos, Importante/Disclaimer)
- Geração de áudio (TTS) com vozes neurais brasileiras via Edge TTS, cache e player integrado
- Armazenamento local robusto em SQLite (`database.db`)
- Integração WhatsApp (estrutura pronta)

### ⚠️ **Funcionalidades Parcialmente Implementadas**
- Envio de áudio via WhatsApp
- Logs de sistema (básico)

### ❌ **Funcionalidades Pendentes**
- Autenticação de usuários (ex: Supabase/OTP)
- Notificações automáticas
- Sistema de feedback de qualidade
- Monitoramento robusto

### 📊 **Progresso Geral: ~90% implementado**

---

## Licença e Ética

- O projeto adota postura ética rigorosa e respeita os limites do exercício legal da advocacia. O sistema atua como tradutor popular e **não substitui advogados**.  
- Todos os dados processados estarão sujeitos à **Lei Geral de Proteção de Dados (LGPD)**, com exclusão periódica das informações e uso restrito ao propósito do serviço.  
- Licença sugerida: MIT ou AGPL, permitindo uso e expansão comunitária.

---

