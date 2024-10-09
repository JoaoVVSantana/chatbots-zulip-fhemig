# Chatbots Zulip - FHEMIG

Este projeto tem como objetivo desenvolver chatbots para a FHEMIG utilizando a API do Zulip e modelos de linguagem LLM, como o Llama 3.2:1b. Os chatbots serão responsáveis por auxiliar em tarefas administrativas e operacionais, promovendo automação e agilizando a comunicação interna.

## Estrutura do Projeto

- **API Zulip**: Usada para comunicação entre os chatbots e os usuários do sistema.
- **LLM Local**: Utilizamos o modelo Llama 3.2:1b, que será executado localmente para garantir a segurança dos dados.
- **RAG (Retrieval-Augmented Generation)**: A técnica RAG será utilizada para realizar buscas em bases de conhecimento e gerar respostas com maior precisão.

## Requisitos

- Python 3.9+
- Ambiente virtual (recomendado: `venv`)
- Zulip API key
- Acesso ao modelo Llama 3.2:1b, ou outro modelo local

## Configuração do Ambiente

1. Clone o repositório:

   ```bash
   git clone https://github.com/pedrow28/chatbots-zulip.git
   cd chatbots-zulip
   ```

2. Crie e ative o ambiente virtual:

   ```bash
   python3 -m venv venv_chatbots
   source venv_chatbots/bin/activate  # Linux/MacOS
   venv_chatbots\Scripts\activate  # Windows

   ```

3. Crie e ative o ambiente virtual:

    ```bash

      pip install -r requirements.txt

    ```

4. Configure as variáveis de ambiente para a API do Zulip e o modelo LLM.

## Pacotes

zulip - Biblioteca oficial para a integração com a API do Zulip.

transformers - Para trabalhar com o modelo Llama, já que o Hugging Face oferece suporte a diversos LLMs, incluindo a série Llama.

torch - Biblioteca necessária para trabalhar com os modelos de deep learning, como Llama.

faiss-cpu - Para implementação da técnica RAG, é necessário um sistema de busca eficiente como o FAISS para busca em grandes bases de dados.

langchain - Para orquestrar a execução da RAG, agentes e outras tarefas envolvendo LLMs.

python-dotenv - Para carregar variáveis de ambiente de um arquivo .env, como a chave de API do Zulip.

rich - Para logs e feedbacks no terminal com formatação mais legível.

requests - Para fazer requisições HTTP, útil para lidar com a API do Zulip e outros serviços, se necessário.