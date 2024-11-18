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
        """
        Inicializa o chatbot Fhemig, carregando configurações e inicializando handlers.
        """
        # Carrega variáveis de ambiente
        load_dotenv()
        # Inicializa o cliente Zulip
        self.client = zulip.Client(config_file="zuliprc")
        # Inicializa os handlers para diferentes funcionalidades
        self.unit_handler = UnitHandler('data/units.json')
        self.information_handler = InformationHandler(
            'data/indicators.json',
            'data/sigh_reports.json',
            'data/tasy_reports.json'
        )
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
                self.user_states[sender_id].update({
                    'state': 'unit_selected',
                    'unit': response['selected_unit'],
                    'system': response['system']
                })
            self.send_response(message, response['message'])
        
        # Lógica para o estado após a seleção da unidade
        elif current_state == 'unit_selected':
            if content == '1':
                # Opção para consultar indicadores/informações
                if self.user_states[sender_id]['system'] == 'SIGH':
                    response = self.information_handler.handle_sigh_request_initial("", self.user_states[sender_id]['unit'])
                    self.user_states[sender_id]['state'] = 'sigh_indicator_selection'
                else:  # Tasy
                    response = "Por favor, descreva brevemente qual informação você está buscando no sistema Tasy."
                    self.user_states[sender_id]['state'] = 'tasy_info_request'
            elif content == '2':
                # Opção para buscar outras informações
                response = "Por favor, descreva brevemente qual outra informação você está buscando."
                self.user_states[sender_id]['state'] = 'other_info'
            else:
                # Mensagem de erro para entrada inválida
                response = "Opção inválida. Digite 1 para consultar indicadores/informações ou 2 para outras informações."
            self.send_response(message, response['message'] if isinstance(response, dict) else response)

        # Lógica para seleção de indicador específico no SIGH
        elif current_state == 'sigh_indicator_selection':
            response = self.information_handler.handle_sigh_indicator_selection(content, {
                'info_request': "",
                'unit': self.user_states[sender_id]['unit']
            })
            if response['success']:
                self.user_states[sender_id]['state'] = 'feedback'
            self.send_response(message, response['message'])

        # Lógica para busca de informações no Tasy ou outras informações
        elif current_state == 'tasy_info_request' or current_state == 'other_info':
            system = self.user_states[sender_id]['system']
            unit = self.user_states[sender_id]['unit']
            response = self.information_handler.handle_other_info_request(content, unit, system)
            self.user_states[sender_id]['state'] = 'feedback'
            self.send_response(message, response['message'])

        # Lógica para feedback e continuação ou encerramento da conversa
        elif current_state == 'feedback':
            if content == '1':
                # Usuário deseja continuar
                response = "Como posso ajudar você agora?\n1. Consultar indicadores/informações\n2. Buscar outras informações"
                self.user_states[sender_id]['state'] = 'unit_selected'
            elif content == '2':
                # Usuário deseja encerrar
                response = "Obrigado por usar nosso serviço! Se precisar de mais alguma coisa, é só me chamar. Tenha um ótimo dia!"
                self.user_states[sender_id] = {'state': 'initial'}
            else:
                # Mensagem de erro para entrada inválida
                response = "Opção inválida. Digite 1 para continuar ou 2 para encerrar."
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
