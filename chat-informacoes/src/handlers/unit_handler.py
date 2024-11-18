from typing import Dict, List, Any
import json

class UnitHandler:
    """
    Classe responsável por gerenciar a seleção de unidades da Fhemig.
    """

    def __init__(self, units_file: str):
        """
        Inicializa o UnitHandler.

        :param units_file: Caminho para o arquivo JSON contendo as informações das unidades.
        """
        self.units = self.load_units(units_file)
        self.unit_names = [unit['name'] for unit in self.units]

    def load_units(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Carrega as unidades a partir de um arquivo JSON.

        :param file_path: Caminho para o arquivo JSON das unidades.
        :return: Lista de dicionários contendo informações das unidades.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Erro: Arquivo de unidades não encontrado: {file_path}")
            return []
        except json.JSONDecodeError:
            print(f"Erro: Falha ao decodificar o arquivo JSON: {file_path}")
            return []

    def get_initial_message(self, nome_usuario) -> str:
        """
        Retorna a mensagem inicial para seleção de unidade.

        :return: String contendo a mensagem de boas-vindas e a lista de unidades.
        """
        unit_list = "\n".join([f"{i+1}. {unit['name']}" for i, unit in enumerate(self.units)])
        return (
            f"Olá, {nome_usuario}! Para eu te ajudar, vamos primeiro selecionar sua unidade. "
            f"Escolha na lista abaixo, o número da sua unidade:\n\n{unit_list}"
        )

    def handle(self, user_input: str) -> Dict[str, Any]:
        """
        Processa a entrada do usuário para seleção de unidade.

        :param user_input: Entrada do usuário (número da unidade).
        :return: Dicionário contendo o resultado do processamento.
        """
        if user_input.isdigit():
            index = int(user_input) - 1
            print(f"User input: {user_input}, Calculated index: {index}")
            if 0 <= index < len(self.units):
                selected_unit = self.units[index]
                print(f"Selected unit: {selected_unit}")
                return self.create_success_response(selected_unit)
        
        return self.create_error_response("Por favor, digite apenas o número da unidade desejada.")

    def create_success_response(self, unit: Dict[str, str]) -> Dict[str, Any]:
        """
        Cria uma resposta de sucesso para a seleção de unidade.

        :param unit: Dicionário contendo informações da unidade selecionada.
        :return: Dicionário com a resposta formatada de sucesso.
        """
        return {
            "success": True,
            "selected_unit": unit['name'],
            "system": unit['system'],
            "message": (
                f"Ótimo! Você selecionou a unidade {unit['name']}. "
                f"Esta unidade utiliza o sistema {unit['system']}. "
                "Qual informação você deseja obter?	\n\n"
                "1: Taxa de Ocupação Hospitalar\n"
                "2: Tempo Médio de Permanência\n"
                "3: Número de Internações\n"
                "4: Número de Cirurgias\n"
                "5: Número de Doadores Efetivos\n"
                "6: Outros"
            )
        }

    def create_error_response(self, error_message: str) -> Dict[str, Any]:
        """
        Cria uma resposta de erro para seleção inválida de unidade.

        :param error_message: Mensagem de erro a ser exibida.
        :return: Dicionário com a resposta formatada de erro.
        """
        return {
            "success": False,
            "message": f"{error_message}"
        }
