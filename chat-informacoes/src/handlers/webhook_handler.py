from flask import Flask, abort, request, jsonify

class WebhookHandler():
    """
    Classe responsável por gerenciar o endpoint do webhook e delegar o processamento para o bot.
    """
    def __init__(self, bot):
        """
        Inicializa o WebhookHandler com o bot e configura as rotas do Flask.
        :param bot: Instância do bot que processará as mensagens.
        """
        self.bot = bot  # Atribuir o bot
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        """
        Configura as rotas do Flask.
        """
        @self.app.route('/zulip-webhook', methods=['POST'])
        def zulip_webhook():
            event = request.json
            if not event or "type" not in event or "content" not in event:
                abort(400, "Payload inválido")
            print(f"Payload recebido: {event}")  # Log para depuração

            # Enviar o evento para o WebhookHandler
            response = self.handle_event(event)
            return jsonify(response), 200

    def handle_event(self, event):
        """
        Processa o evento recebido pelo webhook.
        :param event: Dicionário contendo os dados do evento recebido.
        :return: Resposta processada pelo bot.
        """
        try:
            # Passa o JSON completo para o método handle_message do bot
            from ..bot import FhemigChatbot
            print(event)
            response = FhemigChatbot.handle_message(event)
            print(response)
            return {"success": True, "response": response}
        except Exception as e:
            print(f"Erro ao processar o evento: {e}")
            return {"success": False, "message": "Erro ao processar a mensagem"}
