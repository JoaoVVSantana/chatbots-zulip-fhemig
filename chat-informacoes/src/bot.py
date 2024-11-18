import os
import zulip
from dotenv import load_dotenv
from typing import Dict, Any
from src.handlers.unit_handler import UnitHandler
from src.handlers.information_handler import InformationHandler
from src.handlers.feedback_handler import FeedbackHandler

class FhemigChatbot:
    """
    Classe principal do chatbot Fhemig, responsável por gerenciar a interação com os usuários.
    """

    def __init__(self):
        # Carrega variáveis de ambiente
        load_dotenv()
        # Inicializa o cliente Zulip
        self.client = zulip.Client(config_file="zuliprc")
        # Inicializa os handlers para diferentes funcionalidades
        self.unit_handler = UnitHandler('data/units.json') ## Caminho JSON
        self.information_handler = InformationHandler()
        self.feedback_handler = FeedbackHandler()
        # Dicionário para armazenar o estado da conversa de cada usuário
        self.user_states = {}

    def handle_message(self, message: Dict[str, Any]) -> None:
        """
        Processa cada mensagem recebida e gerencia o fluxo da conversa.
        
        :param message: Dicionário contendo detalhes da mensagem recebida
        """
        content = message['content']
        sender_id = message['sender_id']
        
        # Inicializa o estado do usuário se for a primeira interação
        if sender_id not in self.user_states:
            self.user_states[sender_id] = {'state': 'initial'}
            self.send_response(message, self.unit_handler.get_initial_message())
            return

        current_state = self.user_states[sender_id]['state']

        # Lógica para o estado inicial (seleção de unidade)
        if current_state == 'initial':
            response = self.unit_handler.handle(content)
            if response['success']:
                self.user_states[sender_id]['state'] = 'unit_selected'
                self.user_states[sender_id]['unit'] = response['selected_unit']
                self.user_states[sender_id]['system'] = response['system']
            self.send_response(message, response['message'])
        
        # Lógica para o estado após a seleção da unidade
        elif current_state == 'unit_selected':
            if content == '1':
                # Opção para consultar indicadores
                response = "Ótimo! Vamos consultar os indicadores do Painel Fhemig do Futuro. Qual indicador você gostaria de ver?\n\n1. Taxa de Ocupação (TOH)\n2. Tempo Médio de Permanência Hospitalar (TMP)\n3. Número de Internações\n4. Número de Cirurgias\n5. Número de Doadores Efetivos"
                self.user_states[sender_id]['state'] = 'indicator_selection'
            elif content == '2':
                # Opção para buscar outras informações
                response = "Entendi que você precisa de outras informações. Por favor, descreva brevemente qual informação você está buscando."
                self.user_states[sender_id]['state'] = 'other_info'
            else:
                # Mensagem de erro para entrada inválida
                response = "Desculpe, não entendi sua escolha. Por favor, digite 1 para consultar indicadores ou 2 para buscar outras informações."
            self.send_response(message, response)

        # Lógica para seleção de indicador específico
        elif current_state == 'indicator_selection':
            # Placeholder para implementação futura da lógica de busca de indicador
            response = f"Você selecionou o indicador {content}. [Aqui entraria a lógica para buscar e apresentar o indicador]\n\nVocê gostaria de consultar mais alguma coisa?\n1. Sim\n2. Não"
            self.user_states[sender_id]['state'] = 'feedback'
            self.send_response(message, response)

        # Lógica para busca de outras informações
        elif current_state == 'other_info':
            # Placeholder para implementação futura da lógica de busca de outras informações
            response = f"Entendi que você está buscando informações sobre '{content}'. [Aqui entraria a lógica para buscar e apresentar a informação]\n\nVocê gostaria de consultar mais alguma coisa?\n1. Sim\n2. Não"
            self.user_states[sender_id]['state'] = 'feedback'
            self.send_response(message, response)

        # Lógica para feedback e continuação ou encerramento da conversa
        elif current_state == 'feedback':
            if content == '1':
                # Usuário deseja continuar
                response = "Ótimo! Como posso ajudar você agora?\n1. Consultar indicadores do Painel Fhemig do Futuro\n2. Buscar outras informações"
                self.user_states[sender_id]['state'] = 'unit_selected'
            elif content == '2':
                # Usuário deseja encerrar
                response = "Obrigado por usar nosso serviço! Se precisar de mais alguma coisa, é só me chamar. Tenha um ótimo dia!"
                self.user_states[sender_id] = {'state': 'initial'}
            else:
                # Mensagem de erro para entrada inválida
                response = "Desculpe, não entendi sua escolha. Por favor, digite 1 para continuar ou 2 para encerrar."
            self.send_response(message, response)

    def send_response(self, original_message: Dict[str, Any], response_content: str) -> None:
        """
        Envia uma resposta para o usuário através do Zulip.
        
        :param original_message: Mensagem original recebida
        :param response_content: Conteúdo da resposta a ser enviada
        """
        self.client.send_message({
            "type": original_message["type"],
            "to": original_message["sender_email"],
            "content": response_content,
        })

    def run(self) -> None:
        """
        Inicia o bot e configura o processamento contínuo de mensagens.
        """
        print("Fhemig Chatbot está rodando. Pressione Ctrl-C para sair.")
        self.client.call_on_each_message(self.handle_message)

if __name__ == "__main__":
    bot = FhemigChatbot()
    bot.run()
