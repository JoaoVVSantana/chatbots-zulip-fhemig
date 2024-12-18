import os
from queue import Queue
from threading import Thread, Event
import zulip
from dotenv import load_dotenv
from typing import Dict, Any
from src.handlers.unit_handler import UnitHandler
from src.handlers.information_handler import InformationHandler
from src.handlers.feedback_handler import FeedbackHandler
import time
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
        self.client = zulip.Client(config_file=r"C:\Users\nucleo.informacao\Desktop\chatbot-zulip\chat-informacoes\zuliprc")
        # Inicializa os handlers para diferentes funcionalidades
        self.unit_handler = UnitHandler(r'C:\Users\nucleo.informacao\Desktop\chatbot-zulip\chat-informacoes\data\units.json')
        self.information_handler = InformationHandler(
            r'C:\Users\nucleo.informacao\Desktop\chatbot-zulip\chat-informacoes\data\indicators.json',
            r'C:\Users\nucleo.informacao\Desktop\chatbot-zulip\chat-informacoes\data\fhemig_numeros.json',
            r'C:\Users\nucleo.informacao\Desktop\chatbot-zulip\chat-informacoes\data\sigh_reports.json',
            r'C:\Users\nucleo.informacao\Desktop\chatbot-zulip\chat-informacoes\data\tasy_reports.json'
        )
        self.feedback_handler = FeedbackHandler()
        # Dicionário para armazenar o estado da conversa de cada usuário
        self.user_states = {}
        self.user_unit = ''
        self.user_system = ''
        self.video_link=''
        self.message_queue = Queue() # Fila de mensagens para processar mensagens recebidas
        
        self.worker_thread = Thread(target=self.process_message_queue, daemon=True) # Inicia a thread com a fila
        self.worker_thread.start()

        
        self.stop_event_upload = Event()
        

    
    def process_message(self, message: Dict[str, Any]) -> None:
        """
        Adiciona a mensagem recebida à fila para processamento posterior.
        """
        self.message_queue.put(message)

    def process_message_queue(self):
        """
        Processa mensagens na fila de maneira síncrona para evitar bloqueios.
        """
        while True:
            message = self.message_queue.get()
            try:
                self.handle_message(message)  # Processa cada mensagem
            except Exception as e:
                print(f"Erro ao processar mensagem: {e}")
            self.message_queue.task_done()

    def handle_message(self, message: Dict[str, Any]) -> None:
        """
        Processa cada mensagem recebida e gerencia o fluxo da conversa.
        
        :param message: Dicionário contendo detalhes da mensagem recebida
        """
        
        content = message['content']
        sender_id = message['sender_id']
        sender_full_name = message['sender_full_name']
        if message.get("sender_email") == self.client.email:
            return
        print('HANDLE MESSAGE')
        # Inicializa o estado do usuário se for a primeira interação
        print(f'{sender_full_name} enviou a mensagem: {content}')
        if sender_id not in self.user_states:
            self.user_states[sender_id] = {'state': 'initial'}
            print("CONVERSA INICIALIZADA, AGUARDANDO RESPOSTA INICIAL. STATE: INITIAL")
            self.send_response(message, self.unit_handler.get_initial_message(nome_usuario=sender_full_name))
            return

        # Associa o id especifico ao state
        current_state = self.user_states[sender_id]['state']
        
        # Lógica para o estado inicial (seleção de unidade)
        if current_state == 'initial': self.state_inital(content,sender_id,current_state,message)
        # Lógica para o estado após a seleção da unidade
        elif current_state == 'unit_selected': self.state_unit_selected(content,sender_id,message)      
        # Lógica para feedback e continuação ou encerramento da conversa
        elif current_state == 'feedback': self.state_feedback(content,sender_id,message)    
        elif current_state == 'feedback_ni': self.state_feedback_ni(content,sender_id,sender_full_name,current_state,message)
        elif current_state == 're_select' : self.state_re_select(content,sender_id,message)
        else: self.invalid()
            
            
    def state_feedback_ni (self,content,sender_id,sender_full_name,_current_state,message) -> None:
            self.send_ni(original_message=message, response_content=content)
            self.user_states[sender_id] = {'state': 'feedback'}
            
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
            self.send_response(message, response)
    
    def state_inital (self,content,sender_id,current_state,message) -> None:
        print('STATE INITIAL')
        response = self.unit_handler.handle(content)
        if response['success']: ## Response é sempre o return das funções
    
            self.user_states[sender_id]['state']= 'unit_selected'
            self.user_states[sender_id]['unit']= response['selected_unit']
            self.user_unit = response['selected_unit']
            self.user_system = response['system']
            self.user_states[sender_id]['system']= response['system']
            
            #if(self.user_system=='SIGH'): 
                #thread_upload = Thread(target=self.generate_video_link) #thread pra executar upload do video
                #thread_upload.start() # executa a thread pra fazer upload do video

            print(f"Unidade selecionada: {response['selected_unit']}, Estado atual: {current_state}, Entrada do usuário: {content}")
            self.send_response(message, response['message'])
    
        else:
            self.send_response(message, response['message'])
    
    def state_unit_selected(self,content,sender_id,message) -> None:
        print('STATE UNIT SELECTED', self.user_states[sender_id]['state'])

        indicator = content
        response=self.unit_id(indicator,sender_id)

        self.send_response(message, response['message'] if isinstance(response, dict) else response)

    def generate_video_link(self) -> str:
        """Faz o upload de um arquivo local para o Zulip e gera o link."""
        tentativas_max_upload=15
        tentativa=0
        while tentativa < tentativas_max_upload and not self.stop_event_upload.is_set():
            try:
                file_path = r'chat-informacoes\\data\\video_fhemig_numeros.mp4'
                #file_path = r'chat-informacoes\\data\\OIP.jpg'
                with open(file_path, "rb") as fp:
                    result = self.client.upload_file(fp)
                    if result['result'] == 'success':
                        self.video_link = result['uri']
                        print(f"Link do vídeo gerado com sucesso: {self.video_link}")
                    else:
                        # Erro retornado pelo servidor
                        print(f"Erro no upload: {result['msg']}")
                        tentativa+=1
                        time.sleep(0.5)
                        #raise Exception(f"Erro ao fazer upload: {result['msg']}")
            except FileNotFoundError:
                print("Arquivo de vídeo não encontrado. Verifique o caminho.")
                raise Exception("Arquivo não encontrado. Verifique o caminho.")
        if (tentativa == tentativas_max_upload):
            print("Falha no upload após várias tentativas.")
                
    def unit_id(self,indicator,sender_id) -> None:
        print('UNIT ID', self.user_states[sender_id]['state'])

        if indicator in ['1', '2', '3', '4', '5']: ### Indicadores fhemig do futuro
                # Opção para consultar indicadores/informações
                self.user_states[sender_id]['state'] = 'feedback'
                return self.information_handler.handle_indicator_fhemig_futuro(indicator, self.user_unit)
                ## TODO: MENSAGEM FEEDBACK
        elif indicator in ['6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']:
                # Opção para buscar outras informações ## Aqui entra a lógica if SIGH (fhemig em numeros -> pentaho)| TASY
                if self.user_system == 'SIGH': ## Informações Fhemig em Números

                    self.user_states[sender_id]['state'] = 'feedback'
                    print(self.video_link)
                    return self.information_handler.handle_fhemig_em_numeros(indicator, self.user_unit )                             
                elif self.user_system == 'TASY': ##TODO: relatorios tasy
                    self.user_states[sender_id]['state'] = 'feedback'
                    return self.information_handler.handle_tasy(self.user_unit,self.user_system)                                             
        elif indicator == '17': ## Outras informações
                if self.user_system == 'SIGH': ## Pentaho
                    self.user_states[sender_id]['state'] = 'feedback'
                    return self.information_handler.handle_pentaho(self.user_unit,self.user_system)                 
                elif self.user_system == 'TASY': ##TODO: relatorios tasy
                    self.user_states[sender_id]['state'] = 'feedback'
                    return self.information_handler.handle_tasy(self.user_unit, self.user_system)                                     
        else:
                return self.information_handler.create_error_response()                 
                

    def state_re_select(self,content,sender_id,message) -> None:    
            print('STATE RE SELECTED', self.user_unit)
             
            indicator = content
            response=self.unit_id(indicator,sender_id)
            self.send_response(message, response["message"])

    def state_feedback(self,content,sender_id,message) -> None:
        if content == '1':
                # Usuário deseja solicitar informações de outros indicadores
                self.user_states[sender_id] = {'state': 're_select'}
                print (self.user_unit)
                response=self.unit_handler.show_re_select()
                print('Entrou no 1 do feedback')  
                self.send_response(message, response['message'] if isinstance(response, dict) else response)
                
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
                self.user_system =''
                self.user_unit= ''
        else:   

                response=self.feedback_handler.create_error_response()  
                self.send_response(message, response['message'] if isinstance(response, dict) else response)
   
                

    
    def invalid (self) -> None:
        response = "Opção inválida, por favor, selecione uma das opções apresentadas."
        
        return response
    
    def send_response(self, original_message: Dict[str, Any], response_content: str) -> None:
        """
        Envia uma resposta para o usuário através do Zulip.
        
        :param original_message: Mensagem original recebida
        :param response_content: Conteúdo da resposta a ser enviada
        """
        
        print(original_message['content'])
        try:
            self.client.send_message({
            "type": original_message["type"],
            "to": original_message["sender_email"],
            "content": response_content,
        })
            print('mensagem enviada')
        except Exception as e:
             print(f'erro dentro do send_response: {e}')
        

    def send_ni(self, original_message, response_content: str) -> None:
        print(response_content)
        self.client.send_message({
            "type": original_message["type"],
            "to": "user75@fhchat.expressomg.mg.gov.br", ## ID GRUPO NI
            "content": f"Mensagem de {original_message['sender_full_name']}: {response_content}",
        })

    def run(self) -> None:
        """
        Inicia o bot e configura o processamento contínuo de mensagens.
        """
        print("Fhemig Chatbot está rodando. Pressione Ctrl-C para sair.")
        self.client.call_on_each_message(self.process_message)

if __name__ == "__main__":
    bot = FhemigChatbot()
    bot.run()

