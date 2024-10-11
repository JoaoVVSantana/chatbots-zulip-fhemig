# Criei esse bot para ajudar os usuários a utilizar o Sistema Hospitalar Tasy de forma mais eficiente


import zulip
#import openai
#from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# Configurar cliente do Zulip
client = zulip.Client(config_file="bot_tasy\\zuliprc")

# Obter o perfil do bot para capturar o ID dele
bot_profile = client.get_profile()
bot_user_id = bot_profile['user_id']  # ID do bot

# Configurando LLM

## OpenAI

## OLLAMA
llm = ChatOllama(temperature = 0.2, model="llama3.2:1b")

# Função para gerar o prompt customizado para o LLM
def create_prompt(user_message, sender_full_name):
    # Aqui é onde fazemos o prompt engineering
    prompt_template = ChatPromptTemplate.from_template("""
    Você é um assistente especializado em Tasy, o sistema de gestão hospitalar. 
    Seu trabalho é ajudar os usuários da Fhemig - Fundação Hospitalar do Estado de Minas Gerais - a utilizarem o Tasy. 
    
    Responda de forma clara e objetiva.

    Sempre considere o nome do usuário para tratá-lo com cordialidade e de forma mais personalizada. O nome dele:
    "{sender_full_name}"

    Aqui está a pergunta do usuário:
    "{user_message}"

    Se a pergunta for relacionada ao Tasy, responda com as instruções necessárias. Se não for sobre o Tasy, peça que o usuário especifique melhor a questão.
    """)

    return prompt_template.format_messages(user_message=user_message, sender_full_name=sender_full_name)

def get_llm_response(user_message, sender_full_name):
    prompt = create_prompt(user_message, sender_full_name)
    response = llm(prompt)
    return response.content

# Função que o bot usará para responder a mensagens diretas
def respond_to_private_message(event):
    message = event['message']
    sender_id = message['sender_id']
    sender_full_name = message['sender_full_name']
    content = message['content']
    
    print(f"Mensagem recebida de {sender_full_name} (ID: {sender_id}), mensagem: {content}")


     # Chamar o LLM para processar o conteúdo da mensagem
    llm_response = get_llm_response(content, sender_full_name)

    # Resposta ao usuário
    client.send_message({
        "type": "private",
        "to": [sender_id],
        "content": f"{llm_response}"
    })

# Função que processa os eventos (só processa mensagens diretas)
def process_event(event):
    if event['type'] == 'message':
        message = event['message']
        sender_id = message['sender_id']
        
        if message['type'] == 'private' and sender_id != bot_user_id:  # Só responde a mensagens diretas de outros usuários
            respond_to_private_message(event)

# Função que usa long polling para "escutar" eventos e responder quando necessário
client.call_on_each_event(process_event, ['message'])
