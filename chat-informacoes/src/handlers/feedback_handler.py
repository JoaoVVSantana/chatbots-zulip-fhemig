import json
from typing import Dict, Any
from datetime import datetime

class FeedbackHandler:
    """
    Classe responsável por gerenciar o feedback dos usuários do chatbot Fhemig.
    """

    def __init__(self, feedback_file: str = 'data/feedback.json'):
        """
        Inicializa o FeedbackHandler.

        :param feedback_file: Caminho para o arquivo JSON onde o feedback será armazenado.
        """
        self.feedback_file = feedback_file
        self.feedback_options = {
            '1': 'Muito Satisfeito',
            '2': 'Satisfeito',
            '3': 'Neutro',
            '4': 'Insatisfeito',
            '5': 'Muito Insatisfeito'
        }

    def get_feedback_message(self) -> str:
        """
        Retorna a mensagem solicitando feedback ao usuário.

        :return: Mensagem de solicitação de feedback.
        """
        message = "Por favor, avalie sua experiência com o chatbot:\n\n"
        for key, value in self.feedback_options.items():
            message += f"{key}. {value}\n"
        message += "\nDigite o número correspondente à sua avaliação."
        return message

    def handle_feedback(self, user_input: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa o feedback fornecido pelo usuário.

        :param user_input: Entrada do usuário (número correspondente à avaliação).
        :param user_data: Dicionário contendo dados do usuário e da interação.
        :return: Dicionário com o resultado do processamento do feedback.
        """
        if user_input not in self.feedback_options:
            return {
                'success': False,
                'message': "Opção inválida. Por favor, escolha um número de 1 a 5."
            }

        feedback = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_data.get('user_id', 'Unknown'),
            'unit': user_data.get('unit', 'Unknown'),
            'rating': self.feedback_options[user_input],
            'interaction_details': user_data.get('interaction_details', {})
        }

        self.save_feedback(feedback)

        return {
            'success': True,
            'message': f"Obrigado pelo seu feedback! Sua avaliação foi: {self.feedback_options[user_input]}."
        }

    def save_feedback(self, feedback: Dict[str, Any]) -> None:
        """
        Salva o feedback no arquivo JSON.

        :param feedback: Dicionário contendo os detalhes do feedback.
        """
        try:
            with open(self.feedback_file, 'r+') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []

                data.append(feedback)
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
        except FileNotFoundError:
            with open(self.feedback_file, 'w') as file:
                json.dump([feedback], file, indent=4)

    def get_feedback_summary(self) -> Dict[str, Any]:
        """
        Gera um resumo do feedback coletado.

        :return: Dicionário contendo um resumo das avaliações.
        """
        try:
            with open(self.feedback_file, 'r') as file:
                data = json.load(file)

            total_feedback = len(data)
            ratings_count = {option: 0 for option in self.feedback_options.values()}

            for feedback in data:
                ratings_count[feedback['rating']] += 1

            summary = {
                'total_feedback': total_feedback,
                'ratings_distribution': {
                    rating: f"{count} ({count/total_feedback*100:.2f}%)"
                    for rating, count in ratings_count.items()
                }
            }

            return summary
        except FileNotFoundError:
            return {'error': 'Nenhum feedback coletado ainda.'}
        except json.JSONDecodeError:
            return {'error': 'Erro ao ler o arquivo de feedback.'}
