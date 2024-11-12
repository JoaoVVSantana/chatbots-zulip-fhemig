# Caderno para construção e teste do BOT

# Loading
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import UnstructuredPDFLoader

path = "data/base_conhecimento.pdf"

# Loaders structured and unstructured
loader_structured = PyMuPDFLoader(path)

pages_str = loader_structured.load()

# Cleaning
from langchain.text_splitter import CharacterTextSplitter

# Criando text splitter
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=0
)

# Split
texts = text_splitter.split_documents(pages_str)

# Função para remover espaço em branco
def remove_ws(d):
    text = d.page_content.replace("\n", " ")
    d.page_content = text
    return d

# Clean texts by removing whitespace from each document
texts_cleaned = [remove_ws(d) for d in texts]

# OpenAI API
import os
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv(dotenv_path="env/.env")

# Acessar a chave da OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Retriever setup
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Usando embeddings OpenAI para criar o retriever
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

# Cria o document retriever usando FAISS
db = FAISS.from_documents(texts_cleaned, embeddings)

# Building the retriever
retriever = db.as_retriever(search_kwargs={'k': 3})

# Criação do controle de fluxo
categories = {
    "Faturamento": [
        "Cadastro de Contratos", 
        "Parâmetros de Faturamento", 
        "Relatórios de Faturamento"
    ],
    "Auditoria": [
        "Auditoria de Contas", 
        "Regras de Auditoria"
    ],
    "Estoque": [
        "Cadastro de Materiais", 
        "Movimentação de Estoques"
    ],
    "Relatórios": [
        "Indicadores Gerenciais", 
        "Relatórios de Auditoria"
    ]
}

def present_menu():
    print("Selecione uma categoria:")
    for idx, category in enumerate(categories.keys(), 1):
        print(f"{idx}. {category}")
    
    choice = int(input("Digite o número da categoria: "))
    selected_category = list(categories.keys())[choice - 1]
    
    print(f"\nVocê escolheu: {selected_category}")
    print("Agora selecione um tópico:")
    for idx, topic in enumerate(categories[selected_category], 1):
        print(f"{idx}. {topic}")
    
    topic_choice = int(input("Digite o número do tópico: "))
    selected_topic = categories[selected_category][topic_choice - 1]
    
    return selected_category, selected_topic

# Integração com LLM
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

template = """
Você é Baby, assistente virtual especializada no sistema Tasy de gestão hospitalar. Seu objetivo é fornecer suporte eficiente e preciso aos usuários.

Contexto atual:
- Categoria: {category}
- Tópico: {topic}

Instruções:
- Analise cuidadosamente a pergunta do usuário.
- Forneça uma resposta clara e objetiva, baseada na base de conhecimento do Tasy.
- Use linguagem simples e direta.
- Quando aplicável, liste os passos do processo em formato numerado.

{query}
"""

# Converter o template em prompt_template
prompt = ChatPromptTemplate.from_template(template)

# Configurar llm com OpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Configurar chain
chain = (
    {"context": retriever, "query": RunnablePassthrough()}
    | prompt
    | llm
)

# Função principal
def chatbot():
    category, topic = present_menu()
    query = input(f"Você está no tópico {topic}. Pergunte algo: ")
    
    response = chain.invoke({"context": retriever, "query": query})
    print(response)

# Testando
chatbot()
