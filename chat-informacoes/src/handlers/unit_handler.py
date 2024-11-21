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
            f"Olá, **{nome_usuario}**!\n\n"
             
             "👋 Bem-vindo(a) ao Assistente Virtual da Fhemig!\n\n"

            "Estou aqui para facilitar seu acesso às informações cruciais para seu dia a dia de trabalho.\n\n"

            "Vamos começar nossa jornada selecionando a sua unidade de trabalho.\n\n"

            "Por favor, **escolha o número correspondente à sua unidade** na lista abaixo:\n\n"

            f"{unit_list}\n\n"

            "Após a seleção, poderei te ajudar com:\n\n"
            "• Consulta de indicadores específicos da sua unidade\n"
            "• Acesso a relatórios e informações do sistema de gestão hospitalar\n"
            "• Esclarecimento de dúvidas sobre os dados disponíveis\n\n"

            "Estou animado para auxiliar você! Vamos lá, qual é o número da sua unidade? 😊"
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
            else:
                return self.create_error_response()
        else:
            return self.create_error_response()

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

                f"Obrigado!\n\n"
             
                "Você selecionou a unidade "
                f"**{unit['name']}**, que utiliza o sistema **{unit['system']}**.\n\n"

                "Agora, vamos acessar as informações mais relevantes para você.\n\n"

                "Por favor, selecione o número correspondente ao indicador que você deseja consultar:\n\n"

                "1️⃣ Taxa de Ocupação Hospitalar\n"
                "2️⃣ Tempo Médio de Permanência\n"
                "3️⃣ Número de Internações\n"
                "4️⃣ Número de Cirurgias\n"
                "5️⃣ Número de Doadores Efetivos\n"
                "6️⃣ Pacientes Dia\n"
                "7️⃣ Saídas Hospitalares\n"
                "8️⃣ Óbitos Hospitalares\n"
                "9️⃣ Óbitos Institucionais\n"
                "🔟 Leitos Dia\n"
                "1️⃣1️⃣ Consultas Médicas Eletivas\n"
                "1️⃣2️⃣ Consultas Médicas de Urgência\n"
                "1️⃣3️⃣ Saídas por Clínicas\n"
                "1️⃣4️⃣ Taxa de Mortalidade Hospitalar Geral (%)\n"
                "1️⃣5️⃣ Taxa de Mortalidade Institucional (%)\n"
                "1️⃣6️⃣ Índice de Renovação de Leitos\n"
                "1️⃣7️⃣ Outros\n\n"

                "Digite apenas o número da sua escolha (1-6).\n\n"

                "Após sua seleção, lhe informarei como acessar essa informação nas fontes oficiais da Fhemig.\n\n"
                            
                "Se você precisar de informações não listadas aqui, a\n"
                "opção \"Outros\" está disponível para atender às suas necessidades específicas.\n\n"

                "Estou aqui para ajudar! Qual informação você precisa? 📊"


            )
        }

    def create_error_response(self) -> Dict[str, Any]:
        """
        Cria uma resposta de erro para seleção inválida de unidade.

        :param error_message: Mensagem de erro a ser exibida.
        :return: Dicionário com a resposta formatada de erro.
        """
        return {
            "success": False,
            "message": "Por favor, digite apenas o número da unidade desejada."
        }
