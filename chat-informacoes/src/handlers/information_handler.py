from typing import Dict, Any, List
import json

class InformationHandler:
    """
    Classe responsável por gerenciar solicitações de informações,
    incluindo indicadores do Fhemig em Números e outros relatórios do SIGH e Tasy.
    """

    def __init__(self, indicators_file: str, fhemig_numeros_file: str, sigh_reports_file: str, tasy_reports_file: str):
        """
        Inicializa o InformationHandler.

        :param indicators_file: Caminho para o arquivo JSON contendo os indicadores.
        :param sigh_reports_file: Caminho para o arquivo JSON contendo informações indicadores Fhemig do Futuro.
        :param sigh_reports_file: Caminho para o arquivo JSON contendo informações sobre relatórios do SIGH.
        :param tasy_reports_file: Caminho para o arquivo JSON contendo informações sobre relatórios do Tasy.
        """
        self.indicators_fhemig_futuro = self.load_data(indicators_file)
        self.indicators_fhemig_numeros = self.load_data(fhemig_numeros_file)
        self.sigh_reports = self.load_data(sigh_reports_file)
        self.tasy_reports = self.load_data(tasy_reports_file)
        self.fhemig_em_numeros_indicators = {
            "1": "Taxa de Ocupação Hospitalar",
            "2": "Tempo Médio de Permanência",
            "3": "Número de Internações",
            "4": "Número de Cirurgias",
            "5": "Número de Doadores Efetivos",
            "6": "Outros"
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

    def handle_indicator_fhemig_futuro(self, indicator_choice: str, unit: str) -> Dict[str, Any]:
        """
        Processa a solicitação de um indicador específico do Painel Fhemig do Futuro.

        :param indicator_choice: Escolha do indicador pelo usuário.
        :param unit: Unidade selecionada pelo usuário.
        :return: Dicionário contendo a resposta formatada em Markdown.
        """
        indicator_map = {str(i): indicator['nome'] for i, indicator in enumerate(self.indicators_fhemig_futuro.values(), 1)}
        
        
        if indicator_choice in indicator_map:
            indicator_name = indicator_map[indicator_choice]
            painel_url = "https://app.powerbi.com/view?r=eyJrIjoiZmY0NmIxZmYtMDdkMy00Yzg1LTkxY2ItZjBhOWEwMTJlNDVhIiwidCI6IjM4ZjAxMzYyLTRiMWMtNGU2ZS05MDE0LTAzN2M1ZDA0MTMyNyJ9"
            
            message = (
                f"Para visualizar o indicador **{indicator_name}** para a unidade **{unit}**, "
                "siga estas instruções:\n\n"
                f"1. Acesse o [Painel Fhemig do Futuro]({painel_url})\n"
                "2. Na barra superior, selecione sua unidade\n"
                f"3. Procure pelo indicador '{indicator_name}' no painel\n\n"
                "Se você tiver dificuldades para encontrar o indicador, entre em contato com o Núcleo de Informação, por meio do endereço: nucleo.informacao@fhemig.mg.gov.br.\n\n"               
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
    def handle_other_sigh(self, indicator_name: str, unit: str) -> str:
        """
        Busca o valor de um indicador específico para uma unidade.
        (Esta é uma implementação de exemplo e deve ser substituída pela lógica real)

        :param indicator_name: Nome do indicador.
        :param unit: Nome da unidade.
        :return: Valor do indicador (como string).
        """
        # Messagem indicadores fhemig em numeros

        message = ("Qual informação você deseja obter?\n\n"
                    "1: Pacientes Dia\n"
                    "2: Saídas Hospitalares\n"
                    "3: Óbitos Hospitalares\n"
                    "4: Óbitos Institucionais\n"
                    "5: Leitos Dia\n"
                    "6: Internações Hospitalares\n"
                    "7: Consultas Médicas Eletivas\n"
                    "8: Consultas Médicas de Urgência\n"
                    "9: Saídas por Clínicas\n"
                    "10: Média de Permanência (Dias)\n"
                    "11: Taxa de Ocupação (%)\n"
                    "12: Taxa de Mortalidade Hospitalar Geral (%)\n"
                    "13: Taxa de Mortalidade Institucional (%)\n"
                    "14: Índice de Renovação de Leitos\n"
                    "15: Outros")


        return {
                "success": True,
                "message": message,
                "next_state": "sigh_indicator_selection"
            }

    def handle_other_than_fhemig_numeros(self, unit: str, system: str) -> Dict[str, Any]:
        """
        Processa encaminhamento de indicadores dentro do SIGH mas que não estão no Fhemig em Números

        :param info_request: Descrição da informação solicitada pelo usuário.
        :param unit: Unidade selecionada pelo usuário.
        :param system: Sistema utilizado pela unidade (SIGH ou Tasy).
        :return: Dicionário contendo a resposta formatada.
        """
        if system == "SIGH":
            message =(
                "Para buscar outras informações além das mencionadas dentro do SIGH, "
                "acesse os relatórios do Pentaho.\n\n"
                "Caso não possua acesso ao Pentaho, envie um e-mail com:\n"
                "* Nome completo\n"
                "* CPF\n"
                "Para o endereço: nucleo.informacao@fhemig.mg.gov.br, solicitando "
                "acesso ao sistema."

            )
            return {
                "success": True,
                "message": message,
                "next_state": "feedback"
            }
        elif system == "Tasy":
            pass
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
        
        indicator_map = {str(i): indicator['nome'] for i, indicator in enumerate(self.indicators_fhemig_numeros.values(), 1)}
        url_fhemig_numeros = "pentaho.fhemig.mg.gov.br:8080"

        if indicator in indicator_map:
            indicator_name = indicator_map[indicator]
            message = (
                ## Mensagem para instruir Fhemig em Números
                f"Para visualizar o indicador **{indicator_name}** para a unidade **{unit}**, "
                "siga estas instruções:\n\n"
                f"1. Acesse o **[Fhemig em Números]({url_fhemig_numeros})**\n"
                "2. Clique em 'Create a new query'\n"
                "3. Selecione o cubo 'Atendimentos'\n"
                f"4. Selecione o indicador '{indicator_name}'\n"
                "5. Clique no campo 'Datas'\n"
                "6. Arraste o campo 'Mês' para o espaço com título 'Colunas' na tela principal\n"
                "7. Arrastte também o campo 'Ano'\n"
                "8. Dentro do campo 'Colunas', na tela, clique em 'Ano' duas vezes\n"
                "9. Escolha os anos desejados\n"
                "10. Clique em '>'\n"
                "11. Clique em 'OK'\n"
                "12. Agora, de novo no canto inferior esquerdo, clique na setinha com campo 'Hospitais'\n"
                "13. Agora no campo 'Linhas', arraste para lá o campo 'Hospitais' que foi aberto\n"
                "14. Clique em 'Hospital' duas vezes para abrir o filtro\n"
                f"15. Selecione '{unit}'\n"
                "16. Clique em '>'\n"
                "17. Clique em 'OK'\n\n"
                "Abaixo, segue vídeo com passo a passo ilustrado. Como exemplo, é demonstrado como tirar "
                "o indicador 'Taxa de Ocupação Hospitalar'.\n\n"


            )
            return {
                "success": True,
                "message": message,
                "next_state": "feedback"
            }
        else:
            return {
                "success": False,
                "message": "Opção Inválida",
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
