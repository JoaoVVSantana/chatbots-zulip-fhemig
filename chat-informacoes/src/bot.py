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
        self.client = zulip.Client(config_file="chat-informacoes\\zuliprc")
        # Inicializa os handlers para diferentes funcionalidades
        self.unit_handler = UnitHandler('chat-informacoes\\data\\units.json')
        self.information_handler = InformationHandler(
            'chat-informacoes\\data\\indicators.json',
            'chat-informacoes\\data\\fhemig_numeros.json',
            'chat-informacoes\\data\\sigh_reports.json',
            'chat-informacoes\\data\\tasy_reports.json'
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
        sender_full_name = message['sender_full_name']
        
        # Inicializa o estado do usuário se for a primeira interação
        if sender_id not in self.user_states:
            self.user_states[sender_id] = {'state': 'initial'}
            self.send_response(message, self.unit_handler.get_initial_message(nome_usuario=sender_full_name))
            return

        # Associa o id especifico ao state
        current_state = self.user_states[sender_id]['state']

        # Lógica para o estado inicial (seleção de unidade)
        if current_state == 'initial':
            response = self.unit_handler.handle(content) ## Associa unidade e sistema, e pede a informação demandada
            if response['success']: ## Response é sempre o return das funções
                self.user_states[sender_id].update({
                    'state': 'unit_selected',
                    'unit': response['selected_unit'],
                    'system': response['system']
                })
                self.send_response(message, response['message'])
                print(f"Estado atual: {current_state}, Entrada do usuário: {content}")
        
        # Lógica para o estado após a seleção da unidade
        elif current_state == 'unit_selected':
            if content in ['1', '2', '3', '4', '5']: ### Indicadores fhemig do futuro
                # Opção para consultar indicadores/informações
                response = self.information_handler.handle_indicator_fhemig_futuro(content, self.user_states[sender_id]['unit'])
                self.user_states[sender_id]['state'] = 'feedback' ## Estado de feedback
                print(f"Estado atual: {current_state}, Entrada do usuário: {content}")
                ## TODO: MENSAGEM FEEDBACK
            elif content in ['6', '7', '8', '9', '10', '11', '12', '13', '14', '15']:
                # Opção para buscar outras informações ## Aqui entra a lógica if SIGH (fhemig em numeros -> pentaho)| TASY
                if self.user_states[sender_id]['system'] == 'SIGH': ## Informações Fhemig em Números
                    response = self.information_handler.handle_fhemig_em_numeros(indicator = content, unit = self.user_states[sender_id]['unit'])                 
                    self.user_states[sender_id]['state'] = 'feedback'
                    print(f"Estado atual: {current_state}, Entrada do usuário: {content}")
                elif self.user_states[sender_id]['system'] == 'TASY': ##TODO: relatorios tasy
                    response = self.information_handler.handle_tasy(unit = self.user_states[sender_id]['unit'], system=self.user_states[sender_id]['system'])                 
                    self.user_states[sender_id]['state'] = 'feedback'
                    print(f"Estado atual: {current_state}, Entrada do usuário: {content}")
            elif content in ['16']: ## Outras informações
                if self.user_states[sender_id]['system'] == 'SIGH': ## Pentaho
                    response = self.information_handler.handle_pentaho(unit = self.user_states[sender_id]['unit'], system=self.user_states[sender_id]['system'])                 
                    self.user_states[sender_id]['state'] = 'feedback'
                    print(f"Estado atual: {current_state}, Entrada do usuário: {content}")
                elif self.user_states[sender_id]['system'] == 'TASY': ##TODO: relatorios tasy
                    response = self.information_handler.handle_tasy(unit = self.user_states[sender_id]['unit'], system=self.user_states[sender_id]['system'])                 
                    self.user_states[sender_id]['state'] = 'feedback'
                    print(f"Estado atual: {current_state}, Entrada do usuário: {content}")
            self.send_response(message, response['message'] if isinstance(response, dict) else response)


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

