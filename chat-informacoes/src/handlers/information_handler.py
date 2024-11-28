from typing import Dict, Any, List
import json
import time

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
                    f"Entendi! 📊 Vamos acessar o indicador **{indicator_name}** para a unidade **{unit}**.\n\n"

                    "O **Painel Fhemig do Futuro** é uma ferramenta essencial para monitorar o desempenho e a qualidade dos serviços em nossa instituição.\n\n"

                    "Siga estas etapas simples para visualizar o indicador:\n\n"

                    f"1️⃣ Acesse o **[Painel Fhemig do Futuro]({painel_url})**\n"
                    f"2️⃣ No menu lateral, selecione sua unidade: **{unit}**\n"
                    f"3️⃣ Localize o indicador **'{indicator_name}'** no painel\n\n"

                    "Se encontrar qualquer dificuldade, não hesite em contatar nosso Núcleo de Informação:\n"
                    "📧 nucleo.informacao@fhemig.mg.gov.br\n\n"

                    "Lembre-se, explorar diferentes indicadores pode oferecer insights valiosos sobre o desempenho da sua unidade!\n\n"

                    "O que você gostaria de fazer agora?\n\n"

                    "1️⃣ Solicitar informações sobre outro indicador\n"
                    "2️⃣ Entrar em contato diretamente com o Núcleo de Informação\n"
                    "3️⃣ Encerrar nossa conversa\n\n"

                    "Por favor, digite o número da sua escolha (1-3)."
         
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
            message = (f"Entendi! 📊 Vamos acessar o indicador **{indicator_name}** para a unidade **{unit}** usando o Fhemig em Números.\n\n"

                        "Esta ferramenta poderosa permite uma análise detalhada dos dados. Siga estas instruções passo a passo para obter as informações que você precisa:\n\n"

                        "🔹 **Acesso e Configuração Inicial:**\n"
                        f"1. Acesse o **[Fhemig em Números]({url_fhemig_numeros})**\n"
                        "2. Clique em 'Create a new query'\n"
                        "3. Selecione o cubo 'Atendimentos'\n"
                        f"4. Selecione o indicador **'{indicator_name}'**\n\n"

                        "🔹 **Configuração de Datas:**\n"
                        "5. Clique no campo 'Datas'\n"
                        "6. Arraste o campo 'Mês' para o espaço 'Colunas' na tela principal\n"
                        "7. Arraste também o campo 'Ano'\n"
                        "8. Na área 'Colunas', clique duas vezes em 'Ano'\n"
                        "9. Escolha os anos desejados\n"
                        "10. Clique em '>'\n"
                        "11. Clique em 'OK'\n\n"

                        "🔹 **Seleção da Unidade:**\n"
                        "12. No canto inferior esquerdo, clique na setinha do campo 'Hospitais'\n"
                        "13. Arraste o campo 'Hospitais' para a área 'Linhas'\n"
                        "14. Clique duas vezes em 'Hospital' para abrir o filtro\n"
                        f"15. Selecione **'{unit}'**\n"
                        "16. Clique em '>'\n"
                        "17. Finalize clicando em 'OK'\n\n"

                        "💡 **Dica:** Para uma visualização mais clara, você pode ajustar a ordem das colunas e linhas conforme sua preferência.\n\n"

                        "📹 **Tutorial Visual:**\n"
                        "Para uma demonstração prática, confira o vídeo tutorial abaixo. Ele mostra como obter o indicador 'Taxa de Ocupação Hospitalar' como exemplo, mas o processo é similar para outros indicadores.\n\n"
                        "[Inserir link do vídeo aqui]\n\n"

                        "Precisa de mais alguma orientação ou gostaria de explorar outro indicador? Estou aqui para ajudar! 😊\n\n"

                        "1️⃣ Solicitar informações sobre outro indicador\n"
                        "2️⃣ Tirar dúvidas sobre o Fhemig em Números\n"
                        "3️⃣ Encerrar nossa conversa\n\n"

                        "Por favor, digite o número da sua escolha (1-3)."

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
        message = (f"🏥 **Informações Detalhadas sobre {unit}** 📊\n\n"

                    f"Para acessar um conjunto abrangente de relatórios e dados sobre a **{unit}**, utilize nossa ferramenta de gerenciamento de relatórios, o **Pentaho**.\n\n"

                    "🔐 **Acesso ao Pentaho:**\n\n"

                    "Já possui login e senha?\n"
                    f"1. Visite o **[Pentaho]({url_pentaho})**\n"
                    "2. Clique em 'Login'\n"
                    "3. Digite seu login e senha\n"
                    "4. Clique em 'Entrar'\n\n"

                    "🆕 **Precisa de acesso?**\n\n"

                    "Se você ainda não tem acesso ao Pentaho, siga estas etapas:\n\n"
                    "1. Envie um e-mail para: **nucleo.informacao@fhemig.mg.gov.br**\n"
                    "2. Assunto: \"Solicitação de Acesso ao Pentaho\"\n"
                    "3. No corpo do e-mail, inclua:\n"
                    "   • Nome completo\n"
                    f"  • Unidade: **{unit}**\n"
                    "   • Setor em que trabalha\n\n"

                    "Nossa equipe do Núcleo de Informação processará sua solicitação o mais rápido possível.\n\n"

                    "💡 **Dica:** O Pentaho oferece uma variedade de relatórios personalizáveis.\n\n"

                    "Precisa de mais alguma orientação?\n\n"

                    "1️⃣ Saiba mais sobre os tipos de relatórios disponíveis no Pentaho\n"
                    "2️⃣ Solicitar ajuda com outra ferramenta ou indicador\n"
                    "3️⃣ Encerrar nossa conversa\n\n"

                    "Digite o número da sua escolha (1-3)."

                   
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

        message = (f"📊 **Acessando Relatórios do Tasy para {unit}** 🏥\n\n"

                    f"Você pode obter informações detalhadas sobre a **{unit}** através do módulo de relatórios do sistema {system}. Siga este guia passo a passo para acessar os relatórios do Tasy:\n\n"

                    "🔍 **Localizando os Relatórios:**\n"
                    "1. Na tela inicial do Tasy, clique na aba 'Utilitários'\n"
                    "2. Selecione 'Impressão de Relatórios'\n"
                    "3. Na nova janela, digite **FHEMIG - NI** no campo 'título'\n"
                    "4. Clique em 'Filtrar'\n\n"

                    "📄 **Selecionando e Exportando o Relatório:**\n"
                    "5. Na janela à direita, dê um duplo clique no relatório desejado\n"
                    "6. Preencha os campos solicitados\n"
                    "7. Clique em 'Exportar XLS'\n"
                    "8. Na próxima tela, clique em 'Continuar'\n\n"

                    "💾 **Baixando o Relatório:**\n"
                    "9. O download iniciará no canto superior direito\n"
                    "10. Clique em 'Manter' após o início do download\n"
                    "11. O arquivo será salvo na pasta de downloads do seu computador\n\n"

                    "⚠️ **Observações Importantes:**\n"
                    "• Use apenas relatórios com título **'FHEMIG - NI'** (validados pelo Núcleo de Informação)\n"
                    "• Verifique a estrutura e os dados do relatório baixado\n"
                    "• Informe no histórico da ordem de serviço se são necessários ajustes ou se o relatório está aprovado\n\n"

                    "❓ **Não encontrou o relatório necessário?**\n"
                    "Entre em contato com a referência de informação da sua unidade para solicitar a criação de um novo relatório.\n\n"

                    "💡 **Dica:** Familiarize-se com os relatórios disponíveis. Isso pode ajudar a identificar oportunidades de melhoria e tomada de decisões baseadas em dados!\n\n"

                    "Precisa de mais alguma orientação?\n\n"

                    "1️⃣ Tirar dúvidas sobre os relatórios do Tasy\n"
                    "2️⃣ Solicitar informações sobre outro sistema ou indicador\n"
                    "3️⃣ Encerrar nossa conversa\n\n"

                    "Digite o número da sua escolha (1-3).")

        
        return {
                "success": True,
                "message": message,
                "next_state": "feedback"
            }

    def handle(self, user_input: str) -> Dict[str, Any]:
        """
        Processa a entrada do usuário para seleção de unidade.

        :param user_input: Entrada do usuário (número da unidade).
        :return: Dicionário contendo o resultado do processamento.
        """
        if user_input in [str(i) for i in range(1, 19)]:
            selected_unit = self.units[int(user_input) - 1]
            return self.create_success_response(selected_unit)
        else:
            return self.create_error_response()

    def create_error_response(self) -> Dict[str, Any]:
        """
        Cria uma resposta de erro para seleção inválida de informação.

        :param error_message: Mensagem de erro a ser exibida.
        :return: Dicionário com a resposta formatada de erro.
        """
        return {
            "success": False,
            "message": "🚨 Opção inválida. Por favor, selecione uma das opções fornecidas! 🚨"
        }



    def handle_feedback(self) -> Dict[str, Any]:
        message = (f"Claro! 📬 Estou pronto para ajudar você a entrar em contato com o Núcleo de Informação.\n\n"

                    "**Por favor, digite sua mensagem abaixo. Procure incluir:**\n\n"
                    "• Uma descrição clara da sua solicitação ou dúvida\n"
                    "• Detalhes relevantes (por exemplo, unidade, sistema ou indicador específico)\n"
                    "• Qualquer prazo ou urgência, se aplicável\n\n"

                    "Sua mensagem será encaminhada diretamente ao Núcleo de Informação. Eles analisarão sua solicitação e entrarão em contato o mais breve possível.\n\n"

                    "💡 **Dica:** Quanto mais detalhada for sua mensagem, mais rápido e eficiente será o atendimento!\n\n"

                    "Assim que terminar de digitar sua mensagem, envie-a e eu confirmarei o encaminhamento.\n\n"

                    "**Pronto para começar? Digite sua mensagem agora:**")
        
        return {
                "success": True,
                "message": message,
                "next_state": "feedback"
            }