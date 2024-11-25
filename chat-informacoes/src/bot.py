import os
from threading import Thread
import threading
import zulip
from dotenv import load_dotenv
from typing import Dict, Any
from handlers.unit_handler import UnitHandler
from handlers.information_handler import InformationHandler
#from src.handlers.feedback_handler import FeedbackHandler
from handlers.webhook_handler import WebhookHandler #Endpoint é /zulip-webhook

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
        #self.feedback_handler = FeedbackHandler()
        
        # Inicializa o WebhookHandler e passa a instância do bot
        self.webhook_handler = WebhookHandler(self)
        
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
            print("CONVERSA INICIALIZADA, AGUARDANDO RESPOSTA INICIAL. STATE: INITIAL")
            self.send_response(message, self.unit_handler.get_initial_message(nome_usuario=sender_full_name))
            
            return

        # Associa o id especifico ao state
        current_state = self.user_states[sender_id]['state']

        # Lógica para o estado inicial (seleção de unidade)
        if current_state == 'initial':
            response = self.unit_handler.handle(content)
            if response['success']: ## Response é sempre o return das funções
                print("UNIDADE SELECIONADA")
                self.user_states[sender_id].update({
                    'state': 'unit_selected',
                    'unit': response['selected_unit'],
                    'system': response['system']
                })
                print(f"Unidade selecionada: {response['selected_unit']}, Estado atual: {current_state}, Entrada do usuário: {content}")
                print("SOLICITA INFORMAÇÃO")
                self.send_response(message, response['message'])
                print(f"INFORMAÇÃO SELECIONADA: Estado atual: {current_state}, Entrada do usuário: {content}")
            else:
                self.send_response(message, response['message'])
        
        # Lógica para o estado após a seleção da unidade
        elif current_state == 'unit_selected':
            if content in ['1', '2', '3', '4', '5']: ### Indicadores fhemig do futuro
                # Opção para consultar indicadores/informações
                response = self.information_handler.handle_indicator_fhemig_futuro(content, self.user_states[sender_id]['unit'])
                self.user_states[sender_id]['state'] = 'feedback' ## Estado de feedback
                print(f"Estado atual: {current_state}, Entrada do usuário: {content}")
                ## TODO: MENSAGEM FEEDBACK
            elif content in ['6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']:
                # Opção para buscar outras informações ## Aqui entra a lógica if SIGH (fhemig em numeros -> pentaho)| TASY
                if self.user_states[sender_id]['system'] == 'SIGH': ## Informações Fhemig em Números
                    response = self.information_handler.handle_fhemig_em_numeros(indicator = content, unit = self.user_states[sender_id]['unit'])                 
                    self.user_states[sender_id]['state'] = 'feedback'
                    print(f"Estado atual: {current_state}, Entrada do usuário: {content}")
                elif self.user_states[sender_id]['system'] == 'TASY': ##TODO: relatorios tasy
                    response = self.information_handler.handle_tasy(unit = self.user_states[sender_id]['unit'], system=self.user_states[sender_id]['system'])                 
                    self.user_states[sender_id]['state'] = 'feedback'
                    print(f"Estado atual: {current_state}, Entrada do usuário: {content}")
            elif content == '17': ## Outras informações
                if self.user_states[sender_id]['system'] == 'SIGH': ## Pentaho
                    response = self.information_handler.handle_pentaho(unit = self.user_states[sender_id]['unit'], system=self.user_states[sender_id]['system'])                 
                    self.user_states[sender_id]['state'] = 'feedback'
                    print(f"Estado atual: {current_state}, Entrada do usuário: {content}")
                elif self.user_states[sender_id]['system'] == 'TASY': ##TODO: relatorios tasy
                    print(f"Estado atual: {current_state}, Entrada do usuário: {content}")
                    response = self.information_handler.handle_tasy(unit = self.user_states[sender_id]['unit'], system=self.user_states[sender_id]['system'])                 
                    self.user_states[sender_id]['state'] = 'feedback'
            else:
                response = "Opção inválida, por favor, selecione uma das opções apresentadas."
                print(f"Estado atual: {current_state}, Entrada do usuário: {content}")
            self.send_response(message, response['message'] if isinstance(response, dict) else response)
            



        # Lógica para feedback e continuação ou encerramento da conversa
        elif current_state == 'feedback':
            if content == '1':
                # Usuário deseja continuar
                self.user_states[sender_id]['state'] = 'initial'
                self.send_response(message, self.unit_handler.get_initial_message(nome_usuario=sender_full_name))
                return
            elif content == '2':
                # Usuário deseja mandar mensagem
                response = self.information_handler.handle_feedback()
                self.user_states[sender_id] = {'state': 'feedback_ni'}
                self.send_response(message, response["message"])
            elif content == '3':
                # Usuário deseja encerrar
                response= (f"Obrigado por utilizar o Assistente Virtual da Fhemig! 👋\n\n"

                            "Foi um prazer ajudar você hoje com informações e orientações sobre nossos sistemas e indicadores. Espero que nossa interação tenha sido útil e esclarecedora.\n\n"

                            "🔑 **Pontos-chave para lembrar:**\n"
                            "• O Painel Fhemig do Futuro está sempre disponível para consultas rápidas\n"
                            "• O Fhemig em Números oferece análises detalhadas e personalizáveis\n"
                            "• Os sistemas de gestão hospitalares contêm relatórios importantes\n"
                            "• O Núcleo de Informação está à disposição para dúvidas mais complexas\n\n"

                            "💡 **Dica:** Mantenha-se atualizado sobre novos recursos e relatórios. Eles são frequentemente adicionados para melhorar nossa gestão de informações!\n\n"

                            "Se surgir qualquer dúvida adicional, não hesite em iniciar uma nova conversa. Estou aqui 24/7 para auxiliar você em suas necessidades de informação.\n\n"

                            "Desejo um excelente dia e sucesso em suas atividades na Fhemig! 🏥📊\n\n"

                            "**Até a próxima!**")
                
                self.send_response(message, response)
                


                self.user_states = {}
                

            else:
                response = "Opção inválida, por favor, selecione uma das opções apresentadas."
                print(f"Estado atual: {current_state}, Entrada do usuário: {content}")
            self.send_response(message, response['message'] if isinstance(response, dict) else response)

        elif current_state == 'feedback_ni':
            self.send_ni(original_message=message, response_content=content)
            response = (f"✅ **Ótimo, {message['sender_full_name']}!**\n"
                        "Sua mensagem foi enviada com sucesso ao Núcleo de Informação.\n\n"

                        "📬 **Confirmação:**\n"
                        "• **Destinatário:** Núcleo de Informação\n"
                        "• **Status:** Enviado\n"
                        "• **Prazo de resposta estimado:** Em breve\n\n"

                        "Fique tranquilo(a), um membro da equipe analisará sua solicitação e entrará em contato o mais rápido possível. Enquanto isso, há algo mais em que eu possa ajudar?\n\n"

                        "**Escolha uma das opções abaixo:**\n\n"
                        "1️⃣ Solicitar informações sobre outro tópico\n"
                        "2️⃣ Enviar uma nova mensagem ao Núcleo de Informação\n"
                        "3️⃣ Encerrar nossa conversa\n\n"

                        "💡 **Dica:** Se lembrar de algum detalhe adicional importante, você pode escolher a opção 2 para enviar uma nova mensagem complementar.\n\n"

                        "**Por favor, digite o número da sua escolha (1-3):**"
                        )
            self.user_states[sender_id] = {'state': 'feedback'}
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

    def send_ni(self, original_message, response_content: str) -> None:
        print(response_content)
        self.client.send_message({
            "type": original_message["type"],
            "to": "user75@fhchat.expressomg.mg.gov.br", ## ID GRUPO NI
            "content": f"Mensagem de {original_message['sender_full_name']}: {response_content}",
        })

    def run_bot(self):
        """
        Executa o loop principal do bot Zulip.
        """
        print("Fhemig Chatbot está rodando. Pressione Ctrl-C para sair.")
        if self.client:
            self.client.call_on_each_message(self.handle_message)


    def run(self):
        """
        Inicia o bot e o webhook.
        """
        print("Iniciando o Chatbot e o Webhook...")
        bot_thread = threading.Thread(target=self.run_bot)
        bot_thread.daemon = True
        bot_thread.start()
        self.webhook_handler.app.run(port=5000)
        

if __name__ == "__main__":
    bot = FhemigChatbot()
    
    bot.run()
