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
                f"""Entendi! 📊 Vamos acessar o indicador **{indicator_name}** para a unidade **{unit}**.

                O **Painel Fhemig do Futuro** é uma ferramenta essencial para monitorar o desempenho e a qualidade dos serviços em nossa instituição. 

                Siga estas etapas simples para visualizar o indicador:

                1️⃣ Acesse o **[Painel Fhemig do Futuro]({painel_url})**
                2️⃣ No menu lateral, selecione sua unidade: {unit}
                3️⃣ Localize o indicador '{indicator_name}' no painel

                Se encontrar qualquer dificuldade, não hesite em contatar nosso Núcleo de Informação:
                📧 nucleo.informacao@fhemig.mg.gov.br

                Lembre-se, explorar diferentes indicadores pode oferecer insights valiosos sobre o desempenho da sua unidade!

                O que você gostaria de fazer agora?

                1️⃣ Solicitar informações sobre outro indicador
                2️⃣ Entrar em contato diretamente com o Núcleo de Informação
                3️⃣ Encerrar nossa conversa

                Por favor, digite o número da sua escolha (1-3)."""               
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
            message = (f"""Entendi! 📊 Vamos acessar o indicador **{indicator_name}** para a unidade **{unit}** usando o Fhemig em Números.

                        Esta ferramenta poderosa permite uma análise detalhada dos dados. Siga estas instruções passo a passo para obter as informações que você precisa:

                        🔹 Acesso e Configuração Inicial:
                        1. Acesse o **[Fhemig em Números]({url_fhemig_numeros})**
                        2. Clique em 'Create a new query'
                        3. Selecione o cubo 'Atendimentos'
                        4. Selecione o indicador '{indicator_name}'

                        🔹 Configuração de Datas:
                        5. Clique no campo 'Datas'
                        6. Arraste o campo 'Mês' para o espaço 'Colunas' na tela principal
                        7. Arraste também o campo 'Ano'
                        8. Na área 'Colunas', clique duas vezes em 'Ano'
                        9. Escolha os anos desejados
                        10. Clique em '>'
                        11. Clique em 'OK'

                        🔹 Seleção da Unidade:
                        12. No canto inferior esquerdo, clique na setinha do campo 'Hospitais'
                        13. Arraste o campo 'Hospitais' para a área 'Linhas'
                        14. Clique duas vezes em 'Hospital' para abrir o filtro
                        15. Selecione '{unit}'
                        16. Clique em '>'
                        17. Finalize clicando em 'OK'

                        💡 Dica: Para uma visualização mais clara, você pode ajustar a ordem das colunas e linhas conforme sua preferência.

                        📹 Tutorial Visual:
                        Para uma demonstração prática, confira o vídeo tutorial abaixo. Ele mostra como obter o indicador 'Taxa de Ocupação Hospitalar' como exemplo, mas o processo é similar para outros indicadores.

                        [Inserir link do vídeo aqui]

                        Precisa de mais alguma orientação ou gostaria de explorar outro indicador? Estou aqui para ajudar! 😊

                        1️⃣ Solicitar informações sobre outro indicador
                        2️⃣ Tirar dúvidas sobre o Fhemig em Números
                        3️⃣ Encerrar nossa conversa

                        Por favor, digite o número da sua escolha (1-3)."""
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
        message = (f"""🏥 Informações Detalhadas sobre {unit} 📊

                    Para acessar um conjunto abrangente de relatórios e dados sobre a **{unit}**, utilize nossa ferramenta de gerenciamento de relatórios, o **Pentaho**.

                    🔐 Acesso ao Pentaho:

                    Já possui login e senha?
                    1. Visite o [Pentaho]({url_pentaho})
                    2. Clique em 'Login'
                    3. Digite seu login e senha
                    4. Clique em 'Entrar'

                    🆕 Precisa de acesso?

                    Se você ainda não tem acesso ao Pentaho, siga estas etapas:

                    1. Envie um e-mail para: nucleo.informacao@fhemig.mg.gov.br
                    2. Assunto: "Solicitação de Acesso ao Pentaho"
                    3. No corpo do e-mail, inclua:
                    • Nome completo
                    • Unidade: {unit}
                    • Setor em que trabalha

                    Nossa equipe do Núcleo de Informação processará sua solicitação o mais rápido possível.

                    💡 Dica: O Pentaho oferece uma variedade de relatórios personalizáveis. 

                    Precisa de mais alguma orientação?

                    1️⃣ Saiba mais sobre os tipos de relatórios disponíveis no Pentaho
                    2️⃣ Solicitar ajuda com outra ferramenta ou indicador
                    3️⃣ Encerrar nossa conversa

                    Digite o número da sua escolha (1-3)."""
                   
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

        message = (f"""📊 Acessando Relatórios do Tasy para {unit} 🏥

                    Você pode obter informações detalhadas sobre a **{unit}** através do módulo de relatórios do sistema {system}. Siga este guia passo a passo para acessar os relatórios do Tasy:

                    🔍 Localizando os Relatórios:
                    1. Na tela inicial do Tasy, clique na aba 'Utilitários'
                    2. Selecione 'Impressão de Relatórios'
                    3. Na nova janela, digite **FHEMIG - NI** no campo 'título'
                    4. Clique em 'Filtrar'

                    📄 Selecionando e Exportando o Relatório:
                    5. Na janela à direita, dê um duplo clique no relatório desejado
                    6. Preencha os campos solicitados
                    7. Clique em 'Exportar XLS'
                    8. Na próxima tela, clique em 'Continuar'

                    💾 Baixando o Relatório:
                    9. O download iniciará no canto superior direito
                    10. Clique em 'Manter' após o início do download
                    11. O arquivo será salvo na pasta de downloads do seu computador

                    ⚠️ Observações Importantes:
                    • Use apenas relatórios com título 'FHEMIG - NI' (validados pelo Núcleo de Informação)
                    • Verifique a estrutura e os dados do relatório baixado
                    • Informe no histórico da ordem de serviço se são necessários ajustes ou se o relatório está aprovado

                    ❓ Não encontrou o relatório necessário?
                    Entre em contato com a referência de informação da sua unidade para solicitar a criação de um novo relatório.

                    💡 Dica: Familiarize-se com os relatórios disponíveis. Isso pode ajudar a identificar oportunidades de melhoria e tomada de decisões baseadas em dados!

                    Precisa de mais alguma orientação?

                    1️⃣ Tirar dúvidas sobre os relatórios do Tasy
                    2️⃣ Solicitar informações sobre outro sistema ou indicador
                    3️⃣ Encerrar nossa conversa

                    Digite o número da sua escolha (1-3).""")

        
        return {
                "success": True,
                "message": message,
                "next_state": "feedback"
            }



    def handle_feedback(self) -> Dict[str, Any]:
        message = (f"""Claro! 📬 Estou pronto para ajudar você a entrar em contato com o Núcleo de Informação.

                    Por favor, digite sua mensagem abaixo. Procure incluir:

                    • Uma descrição clara da sua solicitação ou dúvida
                    • Detalhes relevantes (por exemplo, unidade, sistema ou indicador específico)
                    • Qualquer prazo ou urgência, se aplicável

                    Sua mensagem será encaminhada diretamente ao Núcleo de Informação. Eles analisarão sua solicitação e entrarão em contato o mais breve possível.

                    💡 Dica: Quanto mais detalhada for sua mensagem, mais rápido e eficiente será o atendimento!

                    Assim que terminar de digitar sua mensagem, envie-a e eu confirmarei o encaminhamento.

                    Pronto para começar? Digite sua mensagem agora:""")
        
        return {
                "success": True,
                "message": message,
                "next_state": "feedback"
            }