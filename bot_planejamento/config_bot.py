"""
Este código é um chatbot que utiliza o modelo de linguagem LLM (Large Language Model) 
para responder a perguntas de usuários sobre planejamento estratégico. O chatbot é integrado ao Zulip,
uma plataforma de comunicação em equipe.


"""

import zulip
from langchain_ollama import ChatOllama
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.retriever import retriever  # Módulo responsável por recuperar informações do contexto
from memory import ChatbotMemoryManager, format_chat_history

# config.py
import os
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv(dotenv_path="env\\.env")

# Acessar a chave da OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurar cliente do Zulip
client = zulip.Client(config_file="env\\zuliprc")

# Obter o perfil do bot para capturar o ID dele
bot_profile = client.get_profile()
bot_user_id = bot_profile['user_id']  # ID do bot

# Inicializar o modelo LLM com configurações específicas
llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
memory_manager = ChatbotMemoryManager()

def create_prompt(user_message, sender_full_name, retriever, chat_history):
    """
    Cria um prompt customizado para o modelo LLM com base na mensagem do usuário, histórico da conversa e contexto.

    Args:
        user_message (str): Mensagem enviada pelo usuário.
        sender_full_name (str): Nome completo do remetente da mensagem.
        retriever (str): Contexto ou base de conhecimento para embasar a resposta.
        chat_history (list): Histórico da conversa formatado.

    Returns:
        str: Prompt estruturado para o modelo LLM.
    """
    formatted_history = format_chat_history(chat_history)

    # Prompt Engineering: Define as instruções e formato de resposta para o LLM
    prompt_template = ChatPromptTemplate.from_template("""
    Você é o **Zé**, um chatbot especializado em responder perguntas sobre o Planejamento Estratégico da Fhemig 2024-2027. Sua base de conhecimento está organizada em módulos como Missão, Visão, Valores, Objetivos Estratégicos, Indicadores e Iniciativas. Use as informações fornecidas no {context} para responder de forma assertiva, clara e objetiva. Se não encontrar informações relevantes no contexto, informe que não pode responder e sugira que o usuário refine sua pergunta.

    ### Histórico da Conversa:
    {chat_history}
                                                       
    ### Contexto:
    {context}

    ### Instruções:
    1. Use o histórico da conversa para manter contexto e coerência nas respostas
    2. Leia o contexto acima para obter informações necessárias para responder
    3. Responda de forma clara, usando exemplos práticos se aplicável
    4. Se a pergunta estiver ambígua ou incompleta, peça esclarecimentos
    5. Nunca invente informações que não estejam no {context}
    6. Ofereça respostas em linguagem acessível, mas técnica quando necessário
    7. O nome completo dele é: "{sender_full_name}", considere isso ao conversar com ele, não precisa ficar repetindo toda hora, mas use seu nome da forma como um ser humano conversaria.

    ### Formato da Resposta:
    1. Comece respondendo diretamente à pergunta.
    2. Inclua exemplos ou explicações adicionais para enriquecer a resposta.
    3. Caso relevante, apresente conexões com outras áreas do Planejamento Estratégico.
    4. Retorne as respostas organizadas e formatadas em markdown.                                                  

    ### Exemplos de perguntas:
    - Qual é a missão da Fhemig?
    - Como o Planejamento Estratégico impacta a experiência do usuário?
    - Qual é a meta para a Taxa de Ocupação Hospitalar?
    - O que significa "fortalecer a governança corporativa" no contexto da Fhemig?

    Agora, responda à pergunta fornecida pelo usuário:

    PERGUNTA DO USUÁRIO: {pergunta}
    """)

    return prompt_template.format_messages(
        pergunta=user_message,
        sender_full_name=sender_full_name,
        context=retriever,
        chat_history=formatted_history
    )

def get_llm_response(user_message, sender_full_name, retriever, memory):
    """
    Processa a mensagem do usuário, criando um prompt para o modelo LLM e retornando a resposta.

    Args:
        user_message (str): Mensagem enviada pelo usuário.
        sender_full_name (str): Nome completo do remetente.
        retriever (str): Contexto ou base de conhecimento.
        memory (ChatbotMemoryManager): Objeto de memória para gerenciar histórico de conversas.

    Returns:
        str: Resposta gerada pelo modelo LLM.
    """
    # Recuperar histórico da conversa
    chat_history = memory.load_memory_variables({})["chat_history"]
    # Criar prompt com histórico
    prompt = create_prompt(user_message, sender_full_name, retriever, chat_history)
    # Chamar o modelo para obter a resposta
    response = llm(prompt)
    # Salvar a interação na memória
    memory.save_context(
        {"input": user_message},
        {"output": response.content}
    )

    return response.content

def respond_to_private_message(event):
    """
    Responde a mensagens privadas enviadas ao bot.

    Args:
        event (dict): Evento contendo informações da mensagem, remetente e tipo.
    """
    message = event['message']
    sender_id = message['sender_id']
    sender_full_name = message['sender_full_name']
    content = message['content']

    # Obter memória específica do usuário
    user_memory = memory_manager.get_memory(sender_id)

    print(f"Mensagem recebida de {sender_full_name} (ID: {sender_id}), mensagem: {content}")

    # Chamar o LLM para processar o conteúdo da mensagem
    llm_response = get_llm_response(content, sender_full_name, retriever, user_memory)

    # Salvar memórias após cada interação
    memory_manager.save_memories()

    # Enviar a resposta ao usuário
    client.send_message({
        "type": "private",
        "to": [sender_id],
        "content": f"{llm_response}"
    })

def process_event(event):
    """
    Processa eventos de mensagem e responde apenas a mensagens diretas.

    Args:
        event (dict): Evento capturado pelo cliente Zulip.
    """
    if event['type'] == 'message':
        message = event['message']
        sender_id = message['sender_id']
        
        # Responde apenas a mensagens privadas de usuários que não sejam o próprio bot
        if message['type'] == 'private' and sender_id != bot_user_id:
            respond_to_private_message(event)

# Escuta eventos usando long polling e responde a mensagens privadas
client.call_on_each_event(process_event, ['message'])
