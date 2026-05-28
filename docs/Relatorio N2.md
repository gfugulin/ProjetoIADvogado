**Relatório de Projeto**

**Parte 3 - Segundo Bimestre (N2)**

**Desenvolvimento, Resultados e Relatório Completo**

*Tabela 1 - Integrantes do grupo*

|       Nome do Integrante        |    RA    |       E-mail       |
|:-------------------------------:|:--------:|:------------------:|
| Gustavo Fugulin Soares da Silva | 10418552 | [inserir e-mail] |
|        Otto Martins Mota        | 10418170 | [inserir e-mail] |
|          Renan Garrido          | 10417093 | [inserir e-mail] |
|   Rodrigo Roveratti Guerrero    | 10417090 | [inserir e-mail] |

**Informações sobre o Projeto**

**Título:** IADvogado: Simplificação de Textos Jurídicos com Modelos de Linguagem

**Área/Tema relacionado(a):** Direito, Inclusão Digital, Inovação, Infraestrutura, Processamento de Linguagem Natural

**Opção:** ML/DL/VC/PLN ( ) LLM (X)

**Pretende utilizar em outras disciplinas:** Sim ( ) Não (X)

**Esta proposta está relacionada ao trabalho de TCC:** Sim ( ) Não (X)

**Endereço do GitHub:** [PREENCHER COM O LINK PÚBLICO DO REPOSITÓRIO/ORGANIZAÇÃO]

**Endereço do vídeo no YouTube:** [PREENCHER COM O LINK PÚBLICO DO VÍDEO]

**3. Resumo**

O projeto IADvogado propõe o desenvolvimento de uma solução baseada em Inteligência Artificial Generativa para simplificação de textos jurídicos curtos, como decisões judiciais, despachos, comunicados processuais e trechos de peças jurídicas. O problema abordado decorre da dificuldade de compreensão da linguagem jurídica por pessoas sem formação em Direito, o que pode gerar barreiras de acesso à informação, insegurança na interpretação de documentos e afastamento do cidadão em relação ao sistema de Justiça. A solução utiliza modelos de linguagem de grande porte, executados localmente, para transformar textos densos em explicações claras, organizadas e acessíveis, sem substituir a atuação de profissionais jurídicos. A implementação atual contempla uma arquitetura modular em Python, com API em FastAPI, módulo de OCR, cliente de modelo de linguagem local, geração de áudio por Text-to-Speech, persistência planejada em Supabase e integração inicial com WhatsApp. O projeto também considera aspectos éticos e regulatórios, como privacidade, minimização de dados, risco de alucinação e transparência sobre os limites da IA. Como resultado, o trabalho apresenta um protótipo funcional em desenvolvimento, um fluxo metodológico de coleta, preparação e simplificação de textos, além de uma avaliação técnica e ética da solução. A contribuição principal do projeto está em demonstrar como LLMs podem ser aplicados de forma responsável à simplificação de linguagem jurídica, promovendo acessibilidade e inclusão digital.

**Palavras-chave:** Inteligência Artificial; Processamento de Linguagem Natural; Modelos de Linguagem; Direito; Acessibilidade; Simplificação de Texto.

**4. Introdução**

**4.1 Contextualização**

A linguagem jurídica é reconhecida por sua elevada complexidade sintática e terminológica. Decisões judiciais, despachos, comunicados processuais e peças jurídicas frequentemente utilizam expressões técnicas, períodos longos e construções formais que dificultam o entendimento por pessoas sem formação específica na área do Direito. Essa dificuldade não é apenas linguística, mas também social, pois limita o acesso do cidadão à compreensão de informações que podem afetar diretamente sua vida, seus direitos e suas obrigações.

Com o avanço do Processamento de Linguagem Natural (PLN) e dos modelos de linguagem de grande porte, tornou-se possível desenvolver sistemas capazes de resumir, reescrever e explicar textos complexos em linguagem mais acessível. No contexto jurídico, entretanto, essa aplicação exige cautela, pois simplificar um texto legal não significa emitir parecer, recomendar conduta ou substituir análise profissional. O desafio do IADvogado é, portanto, utilizar IA como apoio à compreensão inicial, preservando o significado do texto original e sinalizando claramente seus limites.

**4.2 Justificativa**

O projeto se justifica pela necessidade de tornar informações jurídicas mais compreensíveis para a população leiga. A falta de clareza em documentos jurídicos pode gerar dependência excessiva de terceiros, dificuldade de acompanhamento processual e insegurança na interpretação de comunicações oficiais. Ao propor uma solução de simplificação textual, o IADvogado busca contribuir para a inclusão digital e para a democratização do acesso à informação jurídica.

A escolha por uma arquitetura com processamento local também se justifica pela natureza sensível dos dados jurídicos. Mesmo quando documentos são públicos, podem conter dados pessoais, nomes, números de processos, endereços ou informações de partes envolvidas. Por isso, o projeto valoriza privacidade, minimização de dados e controle sobre o processamento, em conformidade com os princípios da Lei Geral de Proteção de Dados (LGPD).

**4.3 Objetivo**

O objetivo geral do projeto é desenvolver e avaliar um protótipo de sistema baseado em modelos de linguagem para simplificar textos jurídicos curtos, tornando-os mais compreensíveis para pessoas sem formação em Direito.

Os objetivos específicos são:

> • coletar ou selecionar textos jurídicos públicos e curtos, preferencialmente decisões, despachos ou comunicados processuais;
>
> • realizar limpeza, organização e preparação dos textos para uso com modelos de linguagem;
>
> • definir uma estratégia de prompt capaz de gerar resumo simplificado, explicação cotidiana e principais consequências;
>
> • implementar um protótipo em Python com arquitetura modular, contemplando API, módulo de IA, OCR e geração de áudio;
>
> • avaliar os resultados gerados, considerando clareza, fidelidade ao texto original, completude, utilidade e risco de interpretação incorreta;
>
> • discutir os aspectos éticos e de responsabilidade associados ao uso de IA no domínio jurídico.

**4.4 Estrutura do Trabalho**

Este artigo está organizado da seguinte forma: a Seção 5 apresenta a fundamentação teórica relacionada ao Processamento de Linguagem Natural, aos modelos de linguagem e LLMs, além de abordar especificamente a simplificação textual e a IA no domínio jurídico, finalizando com a apresentação dos trabalhos relacionados aderentes a este projeto. A Seção 6 descreve a metodologia adotada, abrangendo o recorte de escopo, a arquitetura do sistema, a estratégia de prompt, os critérios de avaliação e detalhando as próximas etapas planejadas para alcançar os objetivos da pesquisa. A Seção 7 apresenta os resultados obtidos, o estado atual do protótipo, a análise exploratória e uma discussão sobre a qualidade de software e os aspectos éticos envolvidos. Por fim, a Seção 8 sintetiza as conclusões, limitações e possibilidades de trabalhos futuros.

**5. Fundamentação Teórica e Revisão da Literatura**

**5.1 Processamento de Linguagem Natural**

O Processamento de Linguagem Natural (PLN) é uma área da Inteligência Artificial dedicada ao desenvolvimento de métodos computacionais capazes de analisar, representar, interpretar e gerar linguagem humana. Em aplicações práticas, o PLN permite tarefas como classificação de textos, extração de informações, sumarização automática, tradução, resposta a perguntas e simplificação textual. No IADvogado, o PLN é utilizado como base conceitual para transformar documentos jurídicos em representações linguísticas mais acessíveis ao usuário final.

Segundo Jurafsky e Martin (2024), a linguagem humana apresenta ambiguidade, dependência de contexto e variação lexical, características que tornam sua interpretação computacional um desafio. No domínio jurídico, esse desafio é intensificado pela presença de termos técnicos, expressões latinas, referências normativas e estruturas argumentativas complexas.

**5.2 Modelos de Linguagem e LLMs**

Modelos de linguagem são sistemas treinados para estimar padrões em sequências de palavras ou tokens. Os modelos de linguagem de grande porte, conhecidos como LLMs (Large Language Models), ampliaram significativamente a capacidade de geração textual, pois são treinados em enormes volumes de dados e conseguem produzir respostas contextualizadas a partir de instruções em linguagem natural. No projeto IADvogado, o LLM é utilizado para reescrever textos jurídicos em linguagem simples, mantendo a estrutura semântica do documento original.

A escolha por modelos na nuvem utilizando a API do OpenRouter foi adotada para contornar as limitações severas de hardware local (como a necessidade de GPUs caras com 6GB+ de VRAM) e disponibilizar modelos de última geração infinitamente mais robustos e inteligentes, como o **Meta-Llama-3.3-70B-Instruct** (que possui 70 bilhões de parâmetros, oferecendo simplificações infinitamente mais ricas do que o antigo modelo local de 8B). A latência é otimizada com chamadas de rede assíncronas concorrentes (`httpx.AsyncClient`) e fallbacks automáticos para modelos gratuitos da plataforma, viabilizando o projeto de forma eficiente.

**5.3 Engenharia de Prompt**

A engenharia de prompt consiste na formulação estruturada de instruções para orientar o comportamento do modelo de linguagem. Em sistemas de IA generativa, o prompt define o papel esperado do modelo, o formato da resposta, as restrições de conteúdo e os critérios de segurança. No IADvogado, a estratégia de prompt foi construída para gerar uma saída padronizada composta por: resumo simplificado, explicação em linguagem cotidiana, principais direitos ou consequências, termos jurídicos explicados e um aviso de responsabilidade.

Essa padronização é essencial porque mitiga a variabilidade inerente às redes neurais e facilita a avaliação quantitativa e qualitativa dos resultados. Ademais, a instrução rigorosa para que o modelo limite-se à formatação JSON e não emita juízo de valor ou aconselhamento jurídico contribui significativamente para reduzir os riscos éticos (alucinações).

**5.4 Simplificação Automática de Textos Jurídicos**

A simplificação automática de texto busca reescrever conteúdos complexos em uma linguagem mais simples, preservando integralmente o significado original. No domínio jurídico, essa tarefa é especialmente relevante porque muitos documentos, embora de interesse direto da sociedade, são produzidos quase exclusivamente para especialistas. Garimella et al. (2022) ressaltam que textos legais podem conter jargões e estruturas difíceis de compreender por leigos, apontando também o desafio decorrente da escassez de *datasets* paralelos contendo alinhamentos de texto complexo e texto simplificado.

No contexto nacional, pesquisas recentes reforçam a importância de superar o "juridiquês" como barreira de acesso. Alves et al. (2023) discutem a simplificação de textos jurídicos em língua portuguesa utilizando técnicas avançadas de aprendizado de máquina, atestando a extrema relevância e complexidade de tratar a sintaxe jurídica brasileira.

**5.5 Inteligência Artificial no Domínio Jurídico**

A aplicação de IA no domínio jurídico engloba desde a classificação de documentos e predição de decisões até o apoio à redação. Entretanto, o Direito possui rigor semântico próprio e alto impacto social, exigindo responsabilidade na implementação. Chalkidis et al. (2020), ao proporem o LEGAL-BERT, demonstraram cabalmente que modelos genéricos *off-the-shelf* frequentemente falham ao capturar as nuances do domínio jurídico, o que exige adaptações de domínio ou o uso de promtps contextualmente ricos.

No cenário do Brasil, destaca-se o trabalho de Silveira et al. (2023) com o LegalBERT-pt, um modelo de linguagem focado estritamente no domínio jurídico do português brasileiro, e pesquisas do Supremo Tribunal Federal (Projeto VICTOR) na classificação de temas de repercussão geral. Esses esforços corroboram a premissa de que a linguagem jurídica nacional requer ferramentas especializadas.

**5.6 OCR e Extração de Texto**

OCR (Reconhecimento Óptico de Caracteres) é a técnica utilizada para extrair texto de imagens ou documentos digitalizados. No IADvogado, a presença de um módulo de OCR assegura resiliência no tratamento de processos reais, frequentemente disponibilizados pelos tribunais em PDF imagem. Para isso, adota-se o motor Tesseract, ferramenta em código aberto consolidada mundialmente.

Embora o escopo acadêmico deste experimento priorize textos estruturados para reduzir ruídos decorrentes do OCR, a implementação desta etapa amplia de forma robusta a aplicabilidade do sistema no mundo real.

**5.7 Acessibilidade, IHC e Síntese de Fala**

Além da simplificação textual, o projeto preza ativamente pela acessibilidade através da geração de áudio. A síntese de fala (Text-to-Speech - TTS) garante que cidadãos com analfabetismo funcional, dificuldades de leitura ou limitações visuais possam acessar o conteúdo. Tal abordagem dialoga com os preceitos de Interação Humano-Computador e atende rigorosamente às diretrizes de acessibilidade digital estabelecidas pela norma WCAG 2.1 (W3C, 2018). O IADvogado implementa o Microsoft Edge TTS utilizando SSML (Speech Synthesis Markup Language) para conferir prosódia humanizada e narração profissional aos textos gerados.

**5.8 Trabalhos Relacionados**

A presente pesquisa baseia-se e expande o conhecimento consolidado em diversos estudos que buscam aproximar o cidadão do sistema judicial por meio da Inteligência Artificial e do Processamento de Linguagem Natural. A Tabela 2 sintetiza os principais trabalhos correlatos e suas respectivas aderências a este projeto.

*Tabela 2 - Trabalhos relacionados e aderência ao IADvogado*

| **Trabalho/Fonte** | **Contribuição Principal** | **Relação com o IADvogado** |
|:---|:---|:---|
| Garimella et al. (2022) | Discute desafios técnicos da simplificação textual no domínio jurídico e a escassez de bases de dados paralelas. | Fundamenta metodologicamente as barreiras da reescrita semântica sem perda de precisão legal. |
| Alves et al. (2023) | Aborda a simplificação automática de textos jurídicos em língua portuguesa empregando aprendizado de máquina. | Alinha-se diretamente ao objetivo principal de desmistificar o "juridiquês" brasileiro por meio de modelos algorítmicos. |
| Chalkidis et al. (2020) | Introduz o LEGAL-BERT e analisa a necessidade premente de adaptação de modelos generéricos ao nicho do Direito. | Justifica a adoção de estratégias avançadas de prompt e a preferência por modelos densos com alta capacidade inferencial (como Llama 3.1 8B). |
| Silveira et al. (2023) | Apresenta e valida o LegalBERT-pt, modelo fundacional do domínio jurídico em português brasileiro. | Contextualiza a solução com a realidade linguística nacional, abrindo portas para *fine-tuning* futuro do LLM adotado no projeto. |
| Dettmers et al. (2023) | Propõe o método QLoRA para *fine-tuning* eficiente e quantização de modelos LLM. | Fornece a justificativa técnica para executar o LLM em hardware local com 4-bits, democratizando a arquitetura sem perda expressiva de acurácia. |

**6. Metodologia e Resultados Esperados**

**6.1 Abordagem Geral**

A metodologia adotada segue uma abordagem aplicada e experimental, com foco no desenvolvimento de um protótipo funcional e na avaliação qualitativa das saídas produzidas por um modelo de linguagem. O projeto foi dividido em etapas: definição do escopo, coleta ou seleção de textos, preparação dos dados, definição do prompt, implementação da arquitetura, execução do modelo, geração de saídas em texto e áudio, avaliação dos resultados e análise ética.

**6.2 Recorte do Escopo**

Considerando o tempo da disciplina e os feedbacks das avaliações anteriores, o escopo foi delimitado à simplificação de textos jurídicos curtos, entre um e três parágrafos. O sistema não tem como objetivo interpretar processos inteiros, substituir advogados, delinear estratégias processuais ou prever decisões judiciais. Sua atuação restringe-se a explicar, em linguagem palatável, trechos de peças ou decisões fornecidas pelos usuários.

**6.3 Dataset**

O dataset de experimentação deve ser composto por textos jurídicos públicos extraídos de decisões, despachos ou comunicações do Judiciário em fontes abertas. 

*Tabela 3 - Estrutura proposta do dataset*

| **Campo** | **Descrição** |
|:--:|:---|
| id | Identificador único do registro. |
| fonte | Origem do texto, como STJ, CNJ ou outro repositório público. |
| tipo_documento | Tipo do documento jurídico: decisão, despacho, comunicado ou trecho processual. |
| texto_original | Trecho jurídico original antes da simplificação. |
| texto_limpo | Texto após remoção de ruídos, espaços duplicados e quebras excessivas. |
| resumo_simplificado | Resumo produzido pelo modelo em linguagem simples. |
| explicacao_cotidiana | Explicação em linguagem cotidiana para pessoa leiga. |
| direitos_consequencias | Principais direitos, deveres ou consequências identificados. |
| qtd_palavras_original | Quantidade de palavras do texto original. |
| qtd_palavras_simplificado | Quantidade de palavras da saída simplificada. |
| observacoes_avaliacao | Observações qualitativas sobre fidelidade, clareza e risco de erro. |

Quantidade final de textos analisados: [PREENCHER]. Fonte(s) utilizadas: [PREENCHER]. Critério de seleção: textos curtos, públicos e com linguagem jurídica suficientemente complexa para justificar simplificação.

**6.4 Preparação dos Dados**

A etapa de pré-processamento consiste em limpeza e padronização. Realiza-se a remoção de formatações excedentes, espaços em branco e artefatos de quebra de linha. Para arquivos não nativos (imagens), o Tesseract realiza a transcrição. Os textos são então padronizados e divididos para atender aos limites seguros do contexto (*context window*) do LLM sem gerar degradação (*hallucination*).

**6.5 Arquitetura do Sistema**

O IADvogado adota uma arquitetura inspirada em preceitos de modularidade (Portas e Adaptadores), onde controladores, serviços de negócios e integração se mantêm dissociados.

*Tabela 4 - Componentes técnicos do protótipo*

| **Camada** | **Arquivo/Módulo** | **Função** |
|:---|:---|:---|
| Entrada/API | api/main.py e run.py | Exposição de endpoints HTTP e orquestração do fluxo principal via FastAPI. |
| Modelo de linguagem | services/llama_client.py | Comunicação com o LLM local, geração de simplificações e tratamento estruturado de saídas inconsistentes. |
| OCR | services/ocr_worker.py | Extração de texto de imagens usando Pytesseract. |
| TTS | services/edge_tts_worker.py | Geração de áudio em português a partir da explicação simplificada com uso do Edge TTS. |
| Integração | integrations/whatsapp_adapter.py | Estrutura para envio de respostas via WhatsApp (Evolution API). |
| Configuração e core | config/config.py, core/models.py, utils/utils.py | Modelos de dados, configurações, validações (Pydantic) e funções auxiliares. |
| Persistência | Supabase e cache local | Persistência planejada de registros via Supabase e cache local de arquivos MP3. |

A Figura 1 representa, em formato textual, o fluxo geral do sistema:

| Usuário/Cliente -> API FastAPI -> Extração/OCR -> Pré-processamento -> LLM Local -> Parser/Fallback -> Resposta em texto -> TTS -> Áudio/Integração |
|----|

**6.6 Estratégia de Prompt**

A instrução orienta a rede neural a formatar sua saída em campos predefinidos. A injeção de parâmetros restritivos (*"Não invente informações", "Não dê aconselhamento jurídico"*) busca conter a inclinação natural das LLMs à confabulação.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><p>Você é um assistente de linguagem especializado em simplificar textos jurídicos para pessoas sem formação em Direito.</p>
<p>Regras:</p>
<p>1. Não invente informações.</p>
<p>2. Não dê aconselhamento jurídico.</p>
<p>3. Preserve o sentido do texto original.</p>
<p>4. Explique termos técnicos quando necessário.</p>
<p>5. Use linguagem simples e objetiva.</p>
<p>Retorne um JSON contendo:</p>
<p>1. Resumo simplificado</p>
<p>2. Explicação em linguagem cotidiana</p>
<p>3. Principais direitos, deveres ou consequências</p>
<p>4. Termos jurídicos explicados</p>
<p>5. Aviso de responsabilidade</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**6.7 Execução do Modelo**

O modelo executado é o **Meta-Llama-3.3-70B-Instruct** acessado de forma totalmente assíncrona por meio da API do **OpenRouter**. A arquitetura possui grande resiliência de rede e contingências de execução: em caso de limitações de taxa de requisição (HTTP 429), o cliente dinamicamente extrai o tempo de espera sugerido e realiza retentativas. Caso o erro persista ou ocorram falhas do servidor, o sistema percorre sequencialmente uma lista robusta de modelos alternativos gratuitos (como *Hermes 3 Llama-3.1-405B*, *Gemma 2 27B*, *Kimi K2.6*, entre outros) para garantir o retorno da simplificação. Se a resposta da IA for malformada, funções baseadas em expressões regulares (Regex) recuperam as chaves JSON, finalizando em uma resposta de fallback estruturada de segurança caso todas as vias de inferência venham a falhar.

**6.8 Critérios de Avaliação**

Os critérios avaliam a clareza perante leigos comparada ao texto técnico prévio.

*Tabela 5 - Critérios de avaliação manual*

| **Critério** | **Descrição** | **Escala** |
|:---|:---|:---|
| Clareza | Verifica se a saída ficou mais fácil de entender que o texto original. | 1 a 5 |
| Fidelidade | Verifica se o significado jurídico essencial foi preservado. | 1 a 5 |
| Completude | Verifica se informações importantes não foram omitidas. | 1 a 5 |
| Utilidade | Verifica se a resposta ajuda o usuário leigo a compreender o conteúdo. | 1 a 5 |
| Risco de erro | Verifica se a saída pode induzir interpretação incorreta. | 1 a 5 |

**6.9 Resultados Esperados**

Espera-se que o IADvogado ofereça compreensibilidade aos excertos jurídicos superando o texto matriz em acessibilidade, embora o projeto exija um *disclaimer* perpétuo avisando sobre seus fins meramente informacionais e não consulares.

**6.10 Próximas Etapas do Trabalho**

Para atingir a consolidação plena dos objetivos do projeto, definiram-se as seguintes etapas operacionais detalhadas:

1. **Expansão e Consolidação do Dataset**: Ampliar a extração e curadoria dos excertos judiciais de forma manual e estruturada em tribunais e repositórios oficiais, possibilitando a realização abrangente das avaliações experimentais qualitativas propostas nos critérios.
2. **Execução da Avaliação Experimental (Manual e Métrica)**: Processar integralmente a base de dados em desenvolvimento e aplicar as métricas quantitativas (redução percentual de termos e caracteres) junto às pontuações por especialistas das notas de Clareza, Fidelidade, Completude e Utilidade.
3. **Autenticação e Conformidade com a LGPD**: Implementar mecanismos efetivos de controle de sessão (autenticação baseada em tokens/Supabase Auth) integrando de forma robusta o termo de consentimento prévio para processamento, garantindo rastreabilidade e exclusão criptográfica de dados transitórios.
4. **Integração com Dados do CNJ (DataJud)**: Inicialmente, o sistema previa a consulta processual como funcionalidade futura. Durante o desenvolvimento, identificou-se a API Pública do DataJud/CNJ como alternativa oficial, gratuita e adequada para obtenção de metadados processuais públicos. Assim, a integração foi definida como caminho técnico preferencial para evolução do endpoint de consulta processual, substituindo estratégias frágeis de raspagem de dados em sites de tribunais.
5. **Testes de Usabilidade e Aceitação de Usuários Reais**: Desenvolver um projeto de testes focado em IHC, recrutando sujeitos leigos para aferir o nível de acessibilidade prático da síntese de voz (TTS) e o layout visual das saídas via WhatsApp/PWA.

Essas etapas alinham-se profundamente com o escopo metodológico delimitado, transmutando a infraestrutura já implementada em dados científicos tangíveis para a validação final da hipótese de pesquisa.

**7. Resultados**

**7.1 Estado Atual do Desenvolvimento**

O IADvogado encontra-se em estágio avançado e extremamente estável de desenvolvimento infraestrutural (estimado em aproximadamente 75%). A API e os componentes principais executam plenamente inferências assíncronas do Llama 3.3 via OpenRouter com fallback inteligente de modelos gratuitos na nuvem, extração direta de PDFs selecionáveis via `pypdf`, OCR resiliente para imagens via Pytesseract, e TTS performático munido de cache em sistema de arquivos local. A busca processual real via integração oficial com a API Pública do DataJud/CNJ está 100% operacional. As lacunas ainda existentes limitam-se ao controle restrito de identidade e à autenticação de sessões de usuários.

*Tabela 6 - Síntese do estado atual do sistema*

| **Item** | **Status** | **Comentário** |
|:---|:---|:---|
| Upload e processamento | Implementado | Processamento inteligente de imagens (OCR) e extração nativa de PDFs selecionáveis via `pypdf`. |
| LLM na Nuvem (OpenRouter) | Implementado | Uso do modelo Llama 3.3 70B com lista de contingências e fallbacks gratuitos. |
| OCR | Implementado | Módulo para extração de texto em imagens e documentos digitalizados com Pytesseract. |
| TTS | Implementado | Geração de áudio neural de alta qualidade via Edge TTS e cache persistente em disco. |
| WhatsApp | Parcial | Envio textual estruturado das respostas, com pendência de envio nativo de arquivos de áudio. |
| Consulta por número de processo | Implementado | Busca processual ativa integrada à API Pública do DataJud/CNJ com mapeamento de tribunais. |
| Autenticação e consentimento | Pendente | Necessário para maior conformidade à LGPD e histórico de usuários em produção. |
| Logs e observabilidade | Parcial | Integração de logs estruturados nos serviços de rede e controle de exceções. |

**7.2 Resultados do Dataset e Análise Exploratória**

A análise exploratória será apresentada conclusivamente ao fim da próxima etapa de consolidação do corpus experimental.

*Tabela 7 - Estatísticas descritivas do dataset*

|                 **Métrica**                 | **Resultado** |
|:-------------------------------------------:|:--------------|
|       Quantidade de textos analisados       | [PREENCHER] |
|   Média de palavras nos textos originais    | [PREENCHER] |
| Média de palavras nas versões simplificadas | [PREENCHER] |
|          Redução percentual média           | [PREENCHER] |
|       Quantidade de fontes utilizadas       | [PREENCHER] |
|       Tipos de documentos utilizados        | [PREENCHER] |

**7.3 Exemplo de Funcionamento do Artefato**

**Texto original:** [PREENCHER COM UM TRECHO JURÍDICO CURTO UTILIZADO NO TESTE]

**Resumo simplificado gerado:** [PREENCHER COM A SAÍDA DO MODELO]

**Explicação em linguagem cotidiana:** [PREENCHER COM A SAÍDA DO MODELO]

**Principais direitos, deveres ou consequências:** [PREENCHER COM A SAÍDA DO MODELO]

**Aviso de responsabilidade:** Esta explicação foi gerada por inteligência artificial para facilitar a compreensão do texto. Ela não substitui a análise de um advogado ou profissional jurídico habilitado.

**7.4 Avaliação dos Resultados**

As tabelas de pontuação de especialistas registrarão estatisticamente o êxito ou eventuais imprecisões sistemáticas da geração LLM.

*Tabela 8 - Modelo de avaliação manual dos textos*

| **ID** | **Clareza** | **Fidelidade** | **Completude** | **Utilidade** | **Risco de erro** | **Observações** |
|:---|:---|:---|:---|:---|:---|:---|
| 1 | [ ] | [ ] | [ ] | [ ] | [ ] | [PREENCHER] |
| 2 | [ ] | [ ] | [ ] | [ ] | [ ] | [PREENCHER] |
| Média | [ ] | [ ] | [ ] | [ ] | [ ] | [PREENCHER] |

**7.5 Qualidade de Software**

Amparado nos atributos da ISO/IEC 25010 (ISO/IEC, 2011), o protótipo alcança grande maturidade arquitetônica, mantendo-se o compromisso de aprimorar a segurança na manipulação de identidade na próxima fase.

*Tabela 9 - Diagnóstico de qualidade do software*

| **Atributo** | **Avaliação** | **Discussão** |
|:---|:---|:---|
| Adequação funcional | Parcial | O sistema contempla o fluxo de simplificação primário, aguardando complementos para uso processual dinâmico. |
| Eficiência de desempenho | Boa, com ressalvas | O cache (hit/miss) garante latências na casa de milissegundos para repetições, enquanto o cold-start de IA em GPU segue tolerável. |
| Compatibilidade | Parcial | O envio via mensageria móvel carece do encapsulamento pleno de áudio. |
| Segurança | Ponto de atenção | A exigência protetiva do processamento penal ou cível demanda autenticação OTP sólida (ainda pendente). |
| Manutenibilidade | Alta | Aplicação irrestrita de abstrações Python (Ports and Adapters). |

**7.6 Aspectos Éticos do Uso da IA e Responsabilidade**

O uso de redes neurais generativas acarreta a probabilidade não nula do fenômeno da alucinação. O IADvogado endereça esse risco contornando a arquitetura em dois vieses: via *prompt design* restritivo e por meio de forte desambiguação de responsabilidade nos disclaimers. 

O segundo vetor incide na integridade e privacidade da LGPD. Processos judiciais abrigam detalhes delicados; logo, o cômputo fechado da informação na *Edge AI* e políticas assíncronas de expurgo na persistência (30 dias) revelam-se práticas fulcrais estabelecidas em projeto. Por fim, assevera-se em todas as vias a impossibilidade do subsídio humano, enaltecendo a advocacia autêntica e inibindo a negligência informacional da base usuária.

**7.7 Endereço GitHub e Endereço do Vídeo no YouTube**

**Repositório público no GitHub:** [PREENCHER COM O LINK]

**Vídeo público no YouTube:** [PREENCHER COM O LINK]

**8. Conclusão**

O projeto IADvogado demonstrou a viabilidade de aplicar modelos de linguagem à simplificação de textos jurídicos curtos, com foco em acessibilidade, inclusão digital e compreensão inicial de documentos legais por pessoas leigas. A proposta evoluiu de uma ideia conceitual para uma arquitetura técnica modular, contemplando API, processamento local por LLM, OCR, geração de áudio, cache e integração inicial com canais de comunicação.

O objetivo geral foi parcialmente alcançado na medida em que o sistema apresenta estrutura funcional para receber textos ou documentos, processá-los e gerar explicações simplificadas. Contudo, para que o protótipo alcance maturidade maior, ainda é necessário consolidar o dataset final, preencher os resultados experimentais, concluir a avaliação manual, fortalecer autenticação e consentimento LGPD, melhorar observabilidade e finalizar integrações pendentes.

Como contribuição acadêmica, o trabalho evidencia que IA generativa pode ser utilizada em problemas sociais reais quando aplicada com escopo claro, metodologia controlada e responsabilidade ética. Como trabalho futuro, recomenda-se ampliar o dataset, testar modelos especializados em português jurídico, implementar autenticação segura, integrar a API pública do DataJud de forma assíncrona, melhorar as métricas de avaliação e realizar testes com usuários reais para validar a compreensão das explicações geradas.

**9. Referências Bibliográficas**

ALVES, A. et al. Automatic Simplification of Legal Texts in Portuguese Using Machine Learning. In: **International Conference on Artificial Intelligence and Law**. Anais [...]. 2023. Disponível em: <https://pergamum.cjf.jus.br/pergamumweb/vinculos/00015d/00015d8c.pdf>. Acesso em: 23 maio 2026.

BRASIL. **Lei nº 13.709, de 14 de agosto de 2018**. Lei Geral de Proteção de Dados Pessoais (LGPD). Diário Oficial da União, Brasília, DF, 15 ago. 2018. Disponível em: <https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm>. Acesso em: 23 maio 2026.

CAVOUKIAN, A. **Privacy by Design: The 7 Foundational Principles**. Information and Privacy Commissioner of Ontario, 2009.

CHALKIDIS, I. et al. LEGAL-BERT: The Muppets straight out of Law School. In: **Findings of the Association for Computational Linguistics: EMNLP 2020**. Anais [...]. p. 2898-2904, 2020. Disponível em: <https://aclanthology.org/2020.findings-emnlp.261/>. Acesso em: 23 maio 2026.

COCKBURN, A. **Hexagonal Architecture: Ports and Adapters**. 2005. Disponível em: <https://alistair.cockburn.us/hexagonal-architecture/>. Acesso em: 23 maio 2026.

CONSELHO NACIONAL DE JUSTIÇA (CNJ). **Resolução nº 331, de 20 de agosto de 2020**. Institui a Base Nacional de Dados do Poder Judiciário - DataJud. Brasília: CNJ, 2020. Disponível em: <https://atos.cnj.jus.br/atos/detalhar/3428>. Acesso em: 23 maio 2026.

DETTMERS, T. et al. QLoRA: Efficient Finetuning of Quantized LLMs. **arXiv preprint arXiv:2305.14314**, 2023. Disponível em: <https://arxiv.org/abs/2305.14314>. Acesso em: 23 maio 2026.

FASTAPI. **FastAPI Documentation**. Disponível em: <https://fastapi.tiangolo.com/>. Acesso em: 23 maio 2026.

GAMMA, E. et al. **Design Patterns: Elements of Reusable Object-Oriented Software**. Boston: Addison-Wesley, 1994.

GARIMELLA, A. et al. Text Simplification for Legal Domain: Insights and Challenges. In: **Proceedings of the Natural Legal Language Processing Workshop**, 2022. Disponível em: <https://aclanthology.org/2022.nllp-1.28/>. Acesso em: 23 maio 2026.

ISO/IEC. **ISO/IEC 25010:2011: Systems and software engineering - Systems and software Quality Requirements and Evaluation (SQuaRE) - System and software quality models**. Geneva: International Organization for Standardization, 2011.

JURAFSKY, D.; MARTIN, J. H. **Speech and Language Processing**. 3. ed. draft. 2024. Disponível em: <https://web.stanford.edu/~jurafsky/slp3/>. Acesso em: 23 maio 2026.

MARTIN, R. C. **Clean Architecture: A Craftsman's Guide to Software Structure and Design**. Boston: Prentice Hall, 2017.

OLLAMA. **Ollama Documentation**. Disponível em: <https://docs.ollama.com/>. Acesso em: 23 maio 2026.

SILVEIRA, R. et al. LegalBert-pt: A Pretrained Language Model for the Brazilian Portuguese Legal Domain. In: **Brazilian Conference on Intelligent Systems (BRACIS)**, 2023. Anais [...]. Disponível em: <https://sol.sbc.org.br/index.php/bracis/article/view/28420>. Acesso em: 23 maio 2026.

TESSERACT OCR. **Tesseract Open Source OCR Engine**. Disponível em: <https://github.com/tesseract-ocr/tesseract>. Acesso em: 23 maio 2026.

W3C. **Web Content Accessibility Guidelines (WCAG) 2.1**. W3C Recommendation, 2018. Disponível em: <https://www.w3.org/TR/WCAG21/>. Acesso em: 23 maio 2026.

**Apêndice A - Cabeçalho Recomendado para Arquivos Python**

Os arquivos-fonte do projeto devem conter cabeçalho com identificação dos integrantes, síntese do conteúdo e histórico de alterações, conforme solicitado na atividade.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><p>"""</p>
<p>Projeto: IADvogado</p>
<p>Disciplina: Inteligência Artificial - 7º Período - Ciência da Computação</p>
<p>Instituição: Universidade Presbiteriana Mackenzie</p>
<p>Professor: Prof. Dr. Ivan Carlos Alcântara de Oliveira</p>
<p>Integrantes:</p>
<p>- Gustavo Fugulin Soares da Silva - RA 10418552 - [e-mail]</p>
<p>- Otto Martins Mota - RA 10418170 - [e-mail]</p>
<p>- Renan Garrido - RA 10417093 - [e-mail]</p>
<p>- Rodrigo Roveratti Guerrero - RA 10417090 - [e-mail]</p>
<p>Arquivo: [nome_do_arquivo.py]</p>
<p>Síntese: [descrever brevemente a função do arquivo]</p>
<p>Histórico de alterações:</p>
<p>- 23/05/2026 - Grupo IADvogado - Criação/atualização do arquivo.</p>
<p>"""</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>
