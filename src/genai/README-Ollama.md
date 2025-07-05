Instalação do Ollama e Modelos LLM
Para que o agente de conhecimento funcione corretamente, você precisará ter o Ollama instalado em seu sistema e os modelos de linguagem necessários baixados. O Ollama permite que você execute LLMs localmente.

1. Instalar o Ollama
O Ollama é compatível com macOS, Linux e Windows. Siga as instruções de instalação para o seu sistema operacional no site oficial do Ollama:

Site Oficial do Ollama: https://ollama.com/download

Após a instalação, você pode verificar se o Ollama está funcionando corretamente abrindo seu terminal e executando:

ollama --version

Se o Ollama estiver instalado, você verá a versão do Ollama.

2. Baixar os Modelos LLM Necessários
Com o Ollama instalado, você precisará baixar os dois modelos que serão utilizados pelo agente: um para geração de embeddings (representações numéricas do texto) e outro para a geração de respostas textuais.

Abra seu terminal e execute os seguintes comandos, um por um:

Modelo para Embeddings (nomic-embed-text:latest):
Este modelo é otimizado para criar embeddings de texto de alta qualidade, essenciais para a funcionalidade de busca do agente (RAG).

ollama pull nomic-embed-text:latest

Modelo para Geração de Texto (gemma3:latest):
Este é o LLM principal que o agente usará para processar as perguntas e gerar as respostas.

ollama pull gemma3:latest

Aguarde a conclusão do download de cada modelo. O tamanho dos modelos pode variar, e o download pode levar algum tempo dependendo da sua conexão com a internet.

Após baixar ambos os modelos, você pode verificar se eles estão disponíveis no Ollama executando:

ollama list

Você deverá ver nomic-embed-text:latest e gemma3:latest listados.

Com o Ollama e os modelos instalados, seu ambiente estará pronto para executar o agente de conhecimento.