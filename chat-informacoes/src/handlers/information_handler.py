from typing import Dict, Any, List
import json

class InformationHandler:
    """
    Classe responsável por gerenciar solicitações de informações,
    incluindo indicadores do Painel Fhemig do Futuro e outras informações.
    """

    def __init__(self, indicators_file: str, reports_file: str):
        """
        Inicializa o InformationHandler.

        :param indicators_file: Caminho para o arquivo JSON contendo os indicadores.
        :param reports_file: Caminho para o arquivo JSON contendo os relatórios disponíveis.
        """
        self.indicators = self.load_data(indicators_file)
        self.reports = self.load_data(reports_file)

    def load_data(self, file_path: str) -> Dict[str, Any]:
        """
        Carrega dados a partir de um arquivo JSON.

        :param file_path: Caminho para o arquivo JSON.
        :return: Dicionário contendo os dados carregados.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Erro: Arquivo não encontrado: {file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Erro: Falha ao decodificar o arquivo JSON: {file_path}")
            return {}

    def handle_indicator_request(self, indicator_choice: str, unit: str) -> Dict[str, Any]:
        """
        Processa a solicitação de um indicador específico do Painel Fhemig do Futuro.

        :param indicator_choice: Escolha do indicador pelo usuário.
        :param unit: Unidade selecionada pelo usuário.
        :return: Dicionário contendo a resposta formatada.
        """
        indicator_map = {
            "1": "Taxa de Ocupação (TOH)",
            "2": "Tempo Médio de Permanência Hospitalar (TMP)",
            "3": "Número de Internações",
            "4": "Número de Cirurgias",
            "5": "Número de Doadores Efetivos"
        }

        if indicator_choice in indicator_map:
            indicator_name = indicator_map[indicator_choice]
            # Aqui você implementaria a lógica para buscar o valor real do indicador
            indicator_value = self.get_indicator_value(indicator_name, unit)
            return {
                "success": True,
                "message": f"O {indicator_name} para a unidade {unit} é: {indicator_value}\n\n"
                           "Você gostaria de consultar mais alguma coisa?\n1. Sim\n2. Não"
            }
        else:
            return {
                "success": False,
                "message": "Opção de indicador inválida. Por favor, escolha um número de 1 a 5."
            }

    def get_indicator_value(self, indicator_name: str, unit: str) -> str:
        """
        Busca o valor de um indicador específico para uma unidade.
        (Esta é uma implementação de exemplo e deve ser substituída pela lógica real)

        :param indicator_name: Nome do indicador.
        :param unit: Nome da unidade.
        :return: Valor do indicador (como string).
        """
        # Implementação de exemplo - substitua pela lógica real de busca de dados
        return f"Valor exemplo para {indicator_name} em {unit}"

    def handle_other_info_request(self, info_request: str, unit: str, system: str) -> Dict[str, Any]:
        """
        Processa a solicitação de outras informações não cobertas pelos indicadores padrão.

        :param info_request: Descrição da informação solicitada pelo usuário.
        :param unit: Unidade selecionada pelo usuário.
        :param system: Sistema utilizado pela unidade (SIGH ou Tasy).
        :return: Dicionário contendo a resposta formatada.
        """
        # Aqui você implementaria a lógica para buscar ou direcionar para outras informações
        if system == "SIGH":
            response = self.handle_sigh_request(info_request, unit)
        elif system == "Tasy":
            response = self.handle_tasy_request(info_request, unit)
        else:
            response = "Desculpe, não foi possível identificar o sistema correto para sua unidade."

        return {
            "success": True,
            "message": f"{response}\n\nVocê gostaria de consultar mais alguma coisa?\n1. Sim\n2. Não"
        }

    def handle_sigh_request(self, info_request: str, unit: str) -> str:
        """
        Processa solicitações de informações para unidades que utilizam o sistema SIGH.

        :param info_request: Descrição da informação solicitada.
        :param unit: Nome da unidade.
        :return: String com a resposta ou orientação.
        """
        # Implementação de exemplo - substitua pela lógica real
        return (f"Para obter informações sobre '{info_request}' na unidade {unit}, "
                "que utiliza o sistema SIGH, por favor consulte o Fhemig em Números "
                "ou os relatórios disponíveis no Pentaho Azul.")

    def handle_tasy_request(self, info_request: str, unit: str) -> str:
        """
        Processa solicitações de informações para unidades que utilizam o sistema Tasy.

        :param info_request: Descrição da informação solicitada.
        :param unit: Nome da unidade.
        :return: String com a resposta ou orientação.
        """
        # Implementação de exemplo - substitua pela lógica real
        return (f"Para obter informações sobre '{info_request}' na unidade {unit}, "
                "que utiliza o sistema Tasy, por favor acesse os relatórios do Tasy "
                "com o prefixo 'FHEMIG - NI' através da funcionalidade 'Impressão de Relatórios' na aba utilitários.")
