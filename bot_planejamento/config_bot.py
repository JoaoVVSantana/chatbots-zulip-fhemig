# Criei esse bot para ajudar os usuários a conhecer o planejamento estratégico


import zulip
#import openai
#from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.retriever import retriever ## retriever
from langchain.memory import ConversationBufferMemory

# Configurar cliente do Zulip
client = zulip.Client(config_file="bot_planejamento\\src\\zuliprc")

# Obter o perfil do bot para capturar o ID dele
bot_profile = client.get_profile()
bot_user_id = bot_profile['user_id']  # ID do bot

## OpenAI

## OLLAMA
llm = ChatOllama(temperature = 0.2, model="llama3.2:1b")
#memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Função para gerar o prompt customizado para o LLM
def create_prompt(user_message, sender_full_name, retriever):

    context = retriever.get_context(user_message)

    # Aqui é onde fazemos o prompt engineering
    prompt_template = ChatPromptTemplate.from_template("""
    Você é o **Zé**, um assistente especializado no Planejamento Estratégico da Fhemig (Fundação Hospitalar do Estado de Minas Gerais), no Pacto de Gestão Participativa e no sistema InPacto.

    A base de conhecimento que você deve acessar: {context}                                                   

    ### Instruções:

    1. Responda de forma objetiva e clara, utilizando as informações disponíveis nos documentos e manuais.
    2. Forneça explicações rápidas, sem complicações, e apresente apenas os passos essenciais para a resolução de problemas.
    3. Caso necessário, inclua links ou referências a seções específicas dos documentos para mais detalhes.
    4. Evite respostas longas. Concentre-se na simplicidade e na eficiência.
    5. Sempre considere o nome do usuário para tratá-lo com cordialidade e de forma mais personalizada. O nome dele:
    "{sender_full_name}".
    6. Sempre se atenha às informações sobre a FHEMIG e o Pacto de Gestão Participativa que estão na sua base de conhecimento.                                                  
                                                       

    Aqui está a pergunta do usuário:
    "{user_message}"

    
    """)

    return prompt_template.format_messages(user_message=user_message, sender_full_name=sender_full_name, context = context)

def get_llm_response(user_message, sender_full_name, retriever):
    #memory.save_context({"user": user_message}, {})
    prompt = create_prompt(user_message, sender_full_name, retriever)
    # chain
    response = llm(prompt)
    #memory.save_context({"user": user_message}, {"AI": response.content})
    return response.content

# Função que o bot usará para responder a mensagens diretas
def respond_to_private_message(event):
    message = event['message']
    sender_id = message['sender_id']
    sender_full_name = message['sender_full_name']
    content = message['content']
    
    print(f"Mensagem recebida de {sender_full_name} (ID: {sender_id}), mensagem: {content}")


     # Chamar o LLM para processar o conteúdo da mensagem
    llm_response = get_llm_response(content, sender_full_name, retriever)

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
