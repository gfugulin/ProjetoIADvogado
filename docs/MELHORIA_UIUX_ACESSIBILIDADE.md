# Diretrizes de IHC, Acessibilidade e Evolução de UI/UX — IADvogado

Este documento apresenta uma análise de **Interação Humano-Computador (IHC)** e **Acessibilidade Digital** para o sistema **IADvogado (Justiça Simples)**, estabelecendo as bases teóricas adotadas na interface de chat e propondo melhorias práticas para evolução futura em conformidade com as diretrizes internacionais e a legislação nacional.

---

## 🏛️ 1. Fundamentação Teórica de IHC e Usabilidade

A interface do IADvogado foi reestruturada sob o paradigma de **Chat Conversacional** para aproximar o cidadão leigo de sistemas complexos. Essa decisão é sustentada por três pilares teóricos de IHC:

### 1.1. Redução do Golfo de Execução e Avaliação (Donald Norman)
Segundo Donald Norman (*The Design of Everyday Things*), a facilidade de uso de um sistema depende de quão pequeno é o esforço do usuário para:
1. **Executar uma ação (Golfo de Execução):** O que eu preciso fazer para conseguir o que quero?
2. **Avaliar o estado do sistema (Golfo de Avaliação):** O que aconteceu após minha ação?

* **Aplicação no IADvogado:** Ao unificar a entrada de dados em uma barra de digitação simples (semelhante ao WhatsApp, amplamente utilizado por todas as faixas etárias e classes sociais no Brasil), o Golfo de Execução é minimizado. O usuário não precisa aprender a navegar em menus complexos. O Golfo de Avaliação é reduzido por meio de estados visuais claros de digitação (Loader animado de chat) e cartões temáticos autoexplicativos que dividem a resposta de IA.

### 1.2. Heurísticas de Usabilidade (Jakob Nielsen)
O design atual atende diretamente às heurísticas consagradas de Nielsen:
* **Correspondência com o Mundo Real (Heurística 2):** Utiliza terminologias familiares e metáforas físicas (como o clipe para anexo e o balão de fala para diálogo).
* **Flexibilidade e Eficiência de Uso (Heurística 7):** Permite atalhos (tecla *Enter* para envio) e disponibiliza cartões de ações rápidas na abertura (Onboarding Cards) para acelerar a curva de aprendizado de usuários inexperientes.
* **Estética e Design Minimalista (Heurística 8):** A interface removeu ruídos inativos (como configurações complexas expostas), mantendo apenas as ações essenciais ao fluxo principal.

### 1.3. Teoria da Carga Cognitiva (John Sweller)
A memória de trabalho humana possui limites rígidos de processamento. Apresentar um documento jurídico complexo e sua simplificação em um bloco de texto contínuo gera sobrecarga cognitiva.
* **Aplicação no IADvogado:** A segmentação em **Cards Estruturados** ("O que aconteceu", "Significado", "Próximos Passos") atua como uma técnica de *chunking* (agrupamento de informações), permitindo ao usuário leigo absorver a mensagem em etapas lógicas e lineares.

---

## ♿ 2. Acessibilidade Digital (WCAG 2.1 e Lei 13.146/15)

O acesso à informação jurídica é um direito fundamental. A **Lei Brasileira de Inclusão da Pessoa com Deficiência (Estatuto da Pessoa com Deficiência - Lei nº 13.146/2015)**, em seu Art. 63, exige a acessibilidade em sites e sistemas mantidos por instituições públicas ou de interesse público.

O IADvogado alinha-se a esse requisito seguindo as recomendações do **WCAG 2.1 (Web Content Accessibility Guidelines)** da W3C sob os quatro princípios fundamentais (POUR):

```
       ┌────────────────────────────────────────────────────────┐
       │             PRINCÍPIOS POUR (W3C WCAG 2.1)             │
       └────────────────────────────────────────────────────────┘
                    /           │          │           \
                   /            │          │            \
      ┌───────────┐      ┌──────────┐  ┌──────────────┐  ┌──────────┐
      │ Perceptível│      │ Operável │  │Compreensível │  │ Robusto  │
      └───────────┘      └──────────┘  └──────────────┘  └──────────┘
```

1. **Perceptível (Perceivable):** 
   * **Contraste e Temas:** A paleta de cores acolhedora bege/creme possui contraste adequado para leitura. O usuário dispõe de um botão de **Alto Contraste** instantâneo e alternância de Tema Escuro para reduzir a fadiga ocular.
   * **Redimensionamento de Fonte:** Ferramenta dedicada no painel lateral permite ampliar o tamanho do texto em até 140% sem quebras de layout.
2. **Operável (Operable):**
   * **Sem Emojis e com SVGs Inline:** A substituição de emojis por ícones vetoriais inline limpos elimina a poluição visual e garante compatibilidade perfeita com leitores de tela (como NVDA ou TalkBack), que frequentemente leem descrições de emojis confusas.
3. **Compreensível (Understandable):**
   * **Conversão de Mídia (TTS):** A síntese de voz (TTS) neural avançada auxilia idosos, analfabetos funcionais e deficientes visuais a ouvir a tradução do processo. O player em formato de **nota de voz** é uma interface familiar de fácil operação.
4. **Robusto (Robust):**
   * **Responsividade Híbrida e Mobile-First:** A interface se adapta de forma fluida de telas desktop a dispositivos móveis compactos. Em telas menores de 768px, a barra lateral recolhe-se em um menu Hambúrguer oculto sob um backdrop com desfoque e as bolhas de chat expandem-se para até 95% da largura para otimizar o espaço de leitura. Em telas de smartphones (abaixo de 576px), os botões da barra de digitação são reduzidos para 36px, o espaçamento de borda é minimizado e o indicador de segurança do cabeçalho passa a exibir apenas a sinalização visual pulsante para prevenir quebras horizontais e poluição visual.
   * Interface construída em HTML5/CSS3 puro sem dependências pesadas de frameworks, garantindo execução rápida em celulares antigos ou redes móveis limitadas (3G/4G).

---

## 🛠️ 3. Implementação e Recursos de Acessibilidade e UI/UX

Todos os recursos de acessibilidade e melhorias de UI/UX listados nas diretrizes foram totalmente desenvolvidos e integrados à aplicação:

### 3.1. Navegação Completa via Teclado e Foco Visível (Acessibilidade Motora)
* **Status:** Implementado no arquivo [chatbot.html](file:///c:/Users/gusta/Downloads/IADvogado/static/chatbot.html).
* **Solução Técnica:**
  * Inclusão de regras CSS `:focus-visible` dedicadas que geram anéis de foco coloridos de alto contraste (`outline: 3px solid var(--primary) !important`) em qualquer elemento selecionado por teclado.
  * Atribuição de `tabindex="0"` em todos os controles customizados (cartões de histórico, botões de acessibilidade, pílulas de nível cognitivo e cartões de boas-vindas).
  * Inclusão de listeners de eventos JavaScript que mapeiam as teclas *Space* e *Enter* para acionar cliques nos elementos focados.

### 3.2. Entrada por Voz Nativa (Speech-to-Text)
* **Status:** Implementado no arquivo [chatbot.html](file:///c:/Users/gusta/Downloads/IADvogado/static/chatbot.html).
* **Solução Técnica:**
  * Integração com a **Web Speech API** nativa (`window.SpeechRecognition` ou `window.webkitSpeechRecognition`).
  * Inclusão de botão de microfone ao lado do campo de texto com animação visual de pulsação vermelha (`recording-voice`) durante a captação de voz.
  * Transcrição automática local do áudio direto na caixa de texto em tempo real, mitigando erros de digitação e facilitando o uso para idosos ou pessoas com letramento digital reduzido.

### 3.3. Níveis Adaptativos de Simplificação Linguística (Acessibilidade Cognitiva)
* **Status:** Implementado nos arquivos [chatbot.html](file:///c:/Users/gusta/Downloads/IADvogado/static/chatbot.html), [main.py](file:///c:/Users/gusta/Downloads/IADvogado/iadvogado/api/main.py) e [llama_client.py](file:///c:/Users/gusta/Downloads/IADvogado/iadvogado/services/llama_client.py).
* **Solução Técnica:**
  * Exposição de botões de seleção tipo pílula (*Pills*) para os níveis `Fácil`, `Padrão` (ativo por padrão) e `Técnico` posicionados diretamente acima da barra de digitação.
  * Envio do parâmetro `translation_level` nos payloads HTTP (`/upload` e `/process-number`) e tratamento dinâmico no backend ajustando as regras restritivas do `SYSTEM_PROMPT` para o modelo Llama 3.3 70B (gerando frases simplificadas de baixa complexidade ou mantendo termos técnicos com fundamentação estendida conforme solicitado).

### 3.4. Feedback Háptico e Micro-interações de Confirmação (UX Sensorial)
* **Status:** Implementado no arquivo [chatbot.html](file:///c:/Users/gusta/Downloads/IADvogado/static/chatbot.html).
* **Solução Técnica:**
  * Integração com a **Vibration API** (`navigator.vibrate`) como melhoria progressiva encapsulada em blocos try/catch.
  * Disparos de pequenas pulsações de 10-15ms em eventos como: cópia de respostas para área de transferência, sucesso no retorno de consultas da API e alternância de temas.

---

## 📚 Referências Bibliográficas

1. **JURAFSKY, Dan; MARTIN, James H.** *Speech and Language Processing*. Stanford University, 2024.
2. **NIELSEN, Jakob.** *Usability Engineering*. Morgan Kaufmann, 1994.
3. **NORMAN, Donald A.** *The Design of Everyday Things*. Basic Books, 2013.
4. **SWELLER, John.** *Cognitive Load Theory, Learning Difficulty, and Instructional Design*. Learning and Instruction, 1994.
5. **W3C.** *Web Content Accessibility Guidelines (WCAG) 2.1*. World Wide Web Consortium Recommendation, 2018.
6. **BRASIL.** *Lei nº 13.146, de 6 de julho de 2015. Lei Brasileira de Inclusão da Pessoa com Deficiência (Estatuto da Pessoa com Deficiência)*. Diário Oficial da União, Brasília, DF, 2015.
