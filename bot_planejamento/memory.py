
from langchain.memory import ConversationBufferMemory
from typing import Dict
import json
import os
from langchain.schema import HumanMessage, AIMessage
from datetime import datetime

class ChatbotMemoryManager:
    """
    Gerenciador de memória para chatbot, permitindo armazenar e recuperar históricos de conversas 
    personalizados para cada usuário. As memórias são salvas em um arquivo JSON para persistência.

    Attributes:
        memory_file (str): Nome do arquivo onde as memórias serão armazenadas.
        memories (dict): Dicionário contendo objetos de memória para cada usuário.
    """
    def __init__(self, memory_file="chat_memories.json"):
        """
        Inicializa o gerenciador de memória, carregando as memórias do arquivo JSON, se existente.

        Args:
            memory_file (str): Nome do arquivo onde as memórias serão armazenadas.
        """
        self.memory_file = memory_file
        self.memories: Dict[str, ConversationBufferMemory] = {}
        self.load_memories()
    
    def get_memory(self, user_id: str) -> ConversationBufferMemory:
        """
        Obtém ou cria um objeto de memória para o usuário especificado.

        Args:
            user_id (str): Identificador único do usuário.

        Returns:
            ConversationBufferMemory: Objeto de memória do usuário.
        """
        if user_id not in self.memories:
            self.memories[user_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                max_token_limit=1000
            )
        return self.memories[user_id]
    
    def message_to_dict(self, message):
        """
        Converte um objeto de mensagem em um dicionário serializável.

        Args:
            message (HumanMessage | AIMessage): Mensagem do usuário ou do assistente.

        Returns:
            dict: Dicionário representando a mensagem.
        """
        if isinstance(message, (HumanMessage, AIMessage)):
            return {
                "type": "human" if isinstance(message, HumanMessage) else "ai",
                "content": message.content,
                "timestamp": datetime.now().isoformat()
            }
        return None
    
    def dict_to_message(self, message_dict):
        """
        Converte um dicionário em um objeto de mensagem.

        Args:
            message_dict (dict): Dicionário representando a mensagem.

        Returns:
            HumanMessage | AIMessage: Objeto de mensagem.
        """
        if message_dict["type"] == "human":
            return HumanMessage(content=message_dict["content"])
        else:
            return AIMessage(content=message_dict["content"])
    
    def save_memories(self):
        """
        Salva as memórias no arquivo JSON, garantindo persistência do histórico.
        """
        memories_dict = {}
        for user_id, memory in self.memories.items():
            messages = memory.chat_memory.messages
            serialized_messages = [
                self.message_to_dict(msg) for msg in messages
                if msg is not None
            ]
            memories_dict[user_id] = {
                "messages": serialized_messages
            }
        
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(memories_dict, f, ensure_ascii=False, indent=2)
    
    def load_memories(self):
        """
        Carrega as memórias do arquivo JSON, restaurando os históricos de conversa salvos.

        Raises:
            Exception: Em caso de falha ao carregar o arquivo JSON.
        """
        if not os.path.exists(self.memory_file):
            return
        
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                memories_dict = json.load(f)
                
            for user_id, memory_data in memories_dict.items():
                memory = ConversationBufferMemory(
                    memory_key="chat_history",
                    return_messages=True,
                    max_token_limit=1000
                )
                
                # Restaurar mensagens anteriores
                for message_dict in memory_data["messages"]:
                    message = self.dict_to_message(message_dict)
                    memory.chat_memory.messages.append(message)
                    
                self.memories[user_id] = memory
                
        except Exception as e:
            print(f"Erro ao carregar memórias: {e}")

def format_chat_history(chat_history):
    """
    Formata o histórico do chat em texto, preparado para inclusão no prompt do modelo.

    Args:
        chat_history (list): Lista de mensagens do histórico.

    Returns:
        str: Histórico formatado como texto.
    """
    formatted_history = []
    for message in chat_history:
        if isinstance(message, HumanMessage):
            formatted_history.append(f"Usuário: {message.content}")
        elif isinstance(message, AIMessage):
            formatted_history.append(f"Assistente: {message.content}")
    return "\n".join(formatted_history)
