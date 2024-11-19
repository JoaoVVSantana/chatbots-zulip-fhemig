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

        ## Índice e nome dos indicadores FF
        indicator_map = {str(i): indicator['nome'] for i, indicator in enumerate(self.indicators_fhemig_futuro.values(), 1)}
        
        
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
    
    def handle_fhemig_em_numeros(self, indicator: str, unit: str) -> Dict[str, Any]:
            """
            Fornece informações sobre como acessar o indicador específico no Fhemig em Números.

            :param indicator: Nome do indicador selecionado.
            :param unit: Nome da unidade.
            :return: Dicionário com a resposta formatada.
            """
            
            indicator_map = {str(i): indicator['nome'] for i, indicator in enumerate(self.indicators_fhemig_numeros.values(), 1)}
            url_fhemig_numeros = "https://pentaho.fhemig.mg.gov.br:8080"

            
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

    def handle_pentaho(self, unit: str, system: str) -> Dict[str, Any]:
        """
        Processa encaminhamento de indicadores dentro do SIGH mas que não estão no Fhemig em Números

        :param info_request: Descrição da informação solicitada pelo usuário.
        :param unit: Unidade selecionada pelo usuário.
        :param system: Sistema utilizado pela unidade (SIGH ou Tasy).
        :return: Dicionário contendo a resposta formatada.
        """

        url_pentaho = "url"
        ## IDEIA - funcionalidade para solicitar automaticamente o acesso ao Pentaho
        message = (f"Para acessar outras informações sobre a **{unit}**, " 
                   f"acesse o **[Pentaho]({url_pentaho})**.\n\n"
                   "## Não possui acesso?\n\n"
                   "Caso ainda não possua acesso ao Pentaho, entre em contato com o Núcleo de Informação,"
                   "por meio do endereço: nucleo.informacao@fhemig.mg.gov.br, solicitando o acesso e informando:\n\n"
                   "* Nome completo do usuário\n"
                   "* Unidade\n"
                   "* Setor\n\n"
                   "## Já tem login e senha?\n\n"
                   "1. Acesse o [Pentaho]({url_pentaho})\n"
                   "2. Clique em 'Login'\n"
                   "3. Insira o login e senha do Pentaho\n"
                   "4. Clique em 'Entrar'"
                   
                   )


        return {
                "success": True,
                "message": message,
                "next_state": "feedback"
            }

    def handle_tasy(self, unit: str, system: str) -> Dict[str, Any]:
        """
        Processa encaminhamento de indicadores dentro do SIGH mas que não estão no Fhemig em Números

        :param info_request: Descrição da informação solicitada pelo usuário.
        :param unit: Unidade selecionada pelo usuário.
        :param system: Sistema utilizado pela unidade (SIGH ou Tasy).
        :return: Dicionário contendo a resposta formatada.
        """

        message = (f"Para acessar outras informações sobre a **{unit}**, que utiliza o {system}, acesse o "
                   "módulo de relatórios do sistema.\n\n"
                   "Para acessar os relatórios do Tasy, siga os passos abaixo:\n\n"
                    "## Acessando os relatórios\n\n"
                    "2. Na tela inicial, clique na aba 'Utilitários'\n"
                    "3. Selecione a funcionalidade 'Impressão de Relatórios'\n"
                    "4. Na janela que se abrir, insira no campo título o termo **FHEMIG - NI**\n"
                    "5. Clique em 'Filtrar'\n"
                    "6. Na janela do lado direito, clique duas vezes sobre o nome do relatório desejado\n"
                    "7. Preencha os campos indicados na tela\n"
                    "8. Clique no botão 'Exportar XLS'\n"
                    "9. Na tela seguinte, clique no botão 'Continuar'\n"
                    "10. O download iniciará no canto superior direito da tela\n"
                    "11. Clique no botão 'Manter' após o início do download\n"
                    "12. O documento será salvo na pasta de downloads do seu computador\n\n"
                    "## Observações importantes\n\n"
                    "* Utilize apenas relatórios com título 'FHEMIG - NI', pois estes foram validados pelo Núcleo de Informação\n"
                    "* Após baixar o relatório, avalie se a estrutura está adequada e se os dados não apresentam problemas aparentes\n"
                    "* Informe no histórico da ordem de serviço se são necessários ajustes ou se o relatório está aprovado\n\n"
                    "## Não encontrou o relatório que precisava?\n\n"
                    "Procure a referência de informação da sua unidade para solicitar a criação de novo relatório.")

        
        return {
                "success": True,
                "message": message,
                "next_state": "feedback"
            }

