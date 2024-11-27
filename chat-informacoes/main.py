import os
import sys
import logging
import threading
from dotenv import load_dotenv
from src.bot import FhemigChatbot

# Configuração de logging
def setup_logging():
    """
    Configura o sistema de logging para o chatbot.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("chatbot.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

# Carregamento de variáveis de ambiente
    """
    Carrega as variáveis de ambiente necessárias para o chatbot.
    """
    load_dotenv()
    required_vars = ['ZULIP_EMAIL', 'ZULIP_API_KEY', 'ZULIP_SITE']
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Variável de ambiente {var} não encontrada. Por favor, configure o arquivo .env")

def main():
    """
    Função principal que inicializa e executa o chatbot Fhemig.
    """
    # Configurar logging
    logger = setup_logging()
    logger.info("Iniciando o Chatbot Fhemig...")

    try:

         # Inicializar o chatbot
        bot = FhemigChatbot()
        logger.info("Chatbot Fhemig inicializado com sucesso.")

        # Executar o bot
        logger.info("Iniciando o loop principal do chatbot...")
        bot.run()

    except EnvironmentError as e:
        logger.error(f"Erro de configuração: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()


