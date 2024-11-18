
import os
import sys
import logging
from dotenv import load_dotenv
from src.fhemig_chatbot import FhemigChatbot

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def load_environment():
    """
    Carrega as variáveis de ambiente do arquivo .env.
    """
    load_dotenv()
    required_vars = ['ZULIP_EMAIL', 'ZULIP_API_KEY', 'ZULIP_SITE']
    for var in required_vars:
        if not os.getenv(var):
            logger.error(f"Variável de ambiente {var} não encontrada. Por favor, configure o arquivo .env")
            sys.exit(1)

def main():
    """
    Função principal que inicializa e executa o chatbot Fhemig.
    """
    logger.info("Iniciando o Chatbot Fhemig...")
    
    # Carrega as variáveis de ambiente
    load_environment()
    
    try:
        # Inicializa o chatbot
        bot = FhemigChatbot()
        
        # Executa o bot
        logger.info("Chatbot Fhemig está pronto e rodando.")
        bot.run()
    except Exception as e:
        logger.error(f"Erro ao executar o chatbot: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
