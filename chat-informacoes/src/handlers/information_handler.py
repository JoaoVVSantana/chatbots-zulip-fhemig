from typing import Dict, Any, List
import json

class InformationHandler:
    """
    Classe responsável por gerenciar solicitações de informações,
    incluindo indicadores do Fhemig em Números e outros relatórios do SIGH e Tasy.
    """

    def __init__(self, indicators_file: str, sigh_reports_file: str, tasy_reports_file: str):
        """
        Inicializa o InformationHandler.

        :param indicators_file: Caminho para o arquivo JSON contendo os indicadores.
        :param sigh_reports_file: Caminho para o arquivo JSON contendo informações sobre relatórios do SIGH.
        :param tasy_reports_file: Caminho para o arquivo JSON contendo informações sobre relatórios do Tasy.
        """
        self.indicators = self.load_data(indicators_file)
        self.sigh_reports = self.load_data(sigh_reports_file)
        self.tasy_reports = self.load_data(tasy_reports_file)
        self.fhemig_em_numeros_indicators = {
            "1": "Taxa de Ocupação Hospitalar",
            "2": "Tempo Médio de Permanência",
            "3": "Número de Internações",
            "4": "Número de Atendimentos de Urgência",
            "5": "Número de Cirurgias",
            "6": "Número de Consultas Ambulatoriais",
            "7": "Outros"
        }

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
def handle_indicator_request(self, indicator_choice: str, unit: str) -> Dict[str, Any]:
        """
        Processa a solicitação de um indicador específico do Painel Fhemig do Futuro.

        :param indicator_choice: Escolha do indicador pelo usuário.
        :param unit: Unidade selecionada pelo usuário.
        :return: Dicionário contendo a resposta formatada em Markdown.
        """
        indicator_map = {str(i): name for i, name in enumerate(self.indicators.keys(), 1)}
        
        if indicator_choice in indicator_map:
            indicator_name = indicator_map[indicator_choice]
            painel_url = "https://app.powerbi.com/view?r=eyJrIjoiZmY0NmIxZmYtMDdkMy00Yzg1LTkxY2ItZjBhOWEwMTJlNDVhIiwidCI6IjM4ZjAxMzYyLTRiMWMtNGU2ZS05MDE0LTAzN2M1ZDA0MTMyNyJ9"
            
            message = (
                f"Para visualizar o indicador **{indicator_name}** para a unidade **{unit}**, "
                "siga estas instruções:\n\n"
                f"1. Acesse o [Painel Fhemig do Futuro]({painel_url})\n"
                "2. Na barra superior, selecione sua unidade\n"
                f"3. Procure pelo indicador '{indicator_name}' no painel\n\n"
                "Se você tiver dificuldades para encontrar o indicador, entre em contato com o Núcleo de Informação.\n\n"
                
            )
            
            return {
                "success": True,
                "message": message,
                "next_state": "feedback"
            }
        else:
            return {
                "success": False,
                "message": "Opção de indicador inválida. Por favor, escolha um número válido.",
                "next_state": "indicator_selection"
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
        if system == "SIGH":
            return self.handle_sigh_request_initial(info_request, unit)
        elif system == "Tasy":
            return self.handle_tasy_request(info_request, unit)
        else:
            return {
                "success": False,
                "message": "Desculpe, não foi possível identificar o sistema correto para sua unidade.",
                "next_state": "feedback"
            }

    def handle_sigh_request_initial(self, info_request: str, unit: str) -> Dict[str, Any]:
        """
        Inicia o processo de solicitação de informações para o sistema SIGH,
        oferecendo uma lista de indicadores do Fhemig em Números e a opção 'Outros'.

        :param info_request: Descrição da informação solicitada.
        :param unit: Nome da unidade.
        :return: Dicionário com a resposta formatada.
        """
        indicator_list = "\n".join([f"{key}. {value}" for key, value in self.fhemig_em_numeros_indicators.items()])
        message = (
            f"Para sua solicitação sobre '{info_request}' na unidade {unit}, "
            "temos os seguintes indicadores disponíveis no Fhemig em Números:\n\n"
            f"{indicator_list}\n\n"
            "Por favor, escolha o número do indicador desejado ou '7' para outros relatórios."
        )
        return {
            "success": True,
            "message": message,
            "next_state": "sigh_indicator_selection",
            "context": {"info_request": info_request, "unit": unit}
        }

    def handle_sigh_indicator_selection(self, choice: str, context: Dict[str, str]) -> Dict[str, Any]:
        """
        Processa a escolha do usuário entre os indicadores do Fhemig em Números ou outros relatórios.

        :param choice: Escolha do usuário (número do indicador ou '7' para outros).
        :param context: Contexto da solicitação (info_request e unit).
        :return: Dicionário com a resposta formatada.
        """
        info_request = context['info_request']
        unit = context['unit']

        if choice in self.fhemig_em_numeros_indicators:
            if choice == '7':
                return self.handle_sigh_other_reports(info_request, unit)
            else:
                indicator = self.fhemig_em_numeros_indicators[choice]
                return self.handle_fhemig_em_numeros(indicator, unit)
        else:
            return {
                "success": False,
                "message": "Opção inválida. Por favor, escolha um número de 1 a 7.",
                "next_state": "sigh_indicator_selection",
                "context": context
            }

    def handle_fhemig_em_numeros(self, indicator: str, unit: str) -> Dict[str, Any]:
        """
        Fornece informações sobre como acessar o indicador específico no Fhemig em Números.

        :param indicator: Nome do indicador selecionado.
        :param unit: Nome da unidade.
        :return: Dicionário com a resposta formatada.
        """
        fhemig_em_numeros_info = self.sigh_reports.get("fhemig_em_numeros", {})
        message = (
            f"Para acessar o indicador '{indicator}' para a unidade {unit} no Fhemig em Números:\n\n"
            f"1. Acesse: {fhemig_em_numeros_info.get('url', 'URL não disponível')}\n"
            f"2. {fhemig_em_numeros_info.get('instrucoes', 'Instruções não disponíveis')}\n"
            f"3. Procure pelo indicador '{indicator}' na seção apropriada.\n\n"
            "Se você precisar de assistência adicional, entre em contato com o Núcleo de Informação."
        )
        return {
            "success": True,
            "message": message,
            "next_state": "feedback"
        }

    def handle_sigh_other_reports(self, info_request: str, unit: str) -> Dict[str, Any]:
        """
        Fornece informações sobre como acessar outros relatórios do SIGH no Pentaho Azul.

        :param info_request: Descrição da informação solicitada.
        :param unit: Nome da unidade.
        :return: Dicionário com a resposta formatada.
        """
        pentaho_info = self.sigh_reports.get("pentaho", {})
        message = (
            f"Para acessar outros relatórios sobre '{info_request}' para a unidade {unit} no Pentaho Azul:\n\n"
            f"1. Acesse: {pentaho_info.get('url', 'URL não disponível')}\n"
            f"2. {pentaho_info.get('instrucoes', 'Instruções não disponíveis')}\n\n"
            "Se você tiver dificuldades em encontrar o relatório específico, "
            "por favor, entre em contato com o Núcleo de Informação para assistência adicional."
        )
        return {
            "success": True,
            "message": message,
            "next_state": "feedback"
        }

    def handle_tasy_request(self, info_request: str, unit: str) -> Dict[str, Any]:
        """
        Processa solicitações de informações para unidades que utilizam o sistema Tasy.

        :param info_request: Descrição da informação solicitada.
        :param unit: Nome da unidade.
        :return: Dicionário com a resposta formatada.
        """
        tasy_info = self.tasy_reports.get("instrucoes_gerais", "Informações não disponíveis")
        message = (
            f"Para obter informações sobre '{info_request}' na unidade {unit}, que utiliza o sistema Tasy:\n\n"
            f"{tasy_info}\n\n"
            "Lembre-se de procurar por relatórios com o prefixo 'FHEMIG - NI'.\n"
            "Se você não encontrar a informação desejada, por favor, entre em contato com o Núcleo de Informação para assistência adicional."
        )
        return {
            "success": True,
            "message": message,
            "next_state": "feedback"
        }
