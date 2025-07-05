# Exemplos de IA Generativa

Esta pasta apresenta exemplos de IA generativa (com LangChain, BLIP, Ollama). Também inclui uma interface interativa com o **Chainlit**.

---

## Usando o Chainlit

O **Chainlit** permite criar uma interface de chat para interagir com seu agente baseado em LLM.

---

## App Chainlit (`app.py`)

Este programa em Python implementa um **Agente de Conhecimento conversacional** usando **Chainlit** e **LangChain**, projetado para responder a perguntas sobre a **Norma 175 da CVM e ofícios relacionados**.

Ele utiliza a arquitetura **Retrieval Augmented Generation (RAG)**, o que significa que ele **recupera informações** de um conjunto de documentos antes de **gerar uma resposta**.

**Como ele funciona:**

1.  **Inicialização (Chainlit `on_chat_start`):**
    * Carrega **documentos fictícios** sobre a Norma 175 e ofícios CVM (em uma aplicação real, esses seriam PDFs ou HTMLs reais).
    * Divide esses documentos em **pequenos pedaços (chunks)** para facilitar a busca.
    * Usa o modelo **`nomic-embed-text`** (via Ollama) para transformar cada chunk em um **embedding** (representação numérica), armazenando-os em um **banco de vetores (ChromaDB)** em memória.
    * Configura o **`gemma3:latest`** (via Ollama) como o Large Language Model (LLM) principal para gerar as respostas.
    * Cria uma **cadeia RAG** na LangChain, que inclui um `system prompt` para orientar o LLM a atuar como um especialista preciso em regulamentação, respondendo estritamente com base no contexto fornecido.

2.  **Interação (Chainlit `on_message`):**
    * Quando o usuário faz uma pergunta, o agente busca no banco de vetores pelos chunks mais relevantes.
    * Esses chunks, junto com a pergunta do usuário, são enviados ao LLM (`gemma3:latest`).
    * O LLM sintetiza uma resposta baseada *apenas* nas informações recuperadas.
    * A resposta é exibida no chat do Chainlit, e as **fontes** (chunks dos documentos) que foram utilizadas para gerar a resposta são mostradas para transparência.


Para iniciar a interface de conversação:

```bash
chainlit run app.py -w
```

A aplicação abrirá no navegador, permitindo que o usuário interaja com o agente.

## Gerador de legendas (`blip_caption_generator.py`)

Este programa Python demonstra o uso do modelo **BLIP** para gerar legendas (descrições) para imagens. Ele pode processar imagens fornecidas via URL ou caminho de arquivo local, inicializando o modelo BLIP da Hugging Face para converter o conteúdo visual em texto descritivo.


Para executar:

```bash
python blip_caption_generator.py
```
