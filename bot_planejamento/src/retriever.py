## Loader do PDF

from langchain_community.document_loaders import PyMuPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter

# Caminho do PDF a ser processado
path = "data\\planejamento_estrategico.pdf"

# Carrega o PDF usando PyMuPDFLoader
# PyMuPDFLoader é eficiente para extrair texto estruturado de documentos PDF.
loader_structured = PyMuPDFLoader(path)

# Carrega todas as páginas do PDF em uma lista de documentos
pages_str = loader_structured.load()

# Criar o TextSplitter para dividir os documentos em chunks menores
text_splitter = CharacterTextSplitter(
    separator="\n",  # Define o separador de texto
    chunk_size=1000,  # Define o tamanho máximo de cada chunk em caracteres
    chunk_overlap=0   # Define a sobreposição entre os chunks
)

# Dividir os documentos carregados em chunks menores
texts = text_splitter.split_documents(pages_str)

def remove_ws(d):
    """
    Remove quebras de linha do conteúdo do documento para limpeza.

    Args:
        d (Document): Documento com conteúdo a ser limpo.

    Returns:
        Document: Documento com quebras de linha removidas.
    """
    text = d.page_content.replace("\n", "")
    d.page_content = text
    return d

# Limpa os textos removendo espaços em branco e quebras de linha
texts_cleaned = [remove_ws(d) for d in texts]

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv(dotenv_path="env\\.env")

# Acessar a chave da OpenAI do arquivo .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inicializa as embeddings usando o modelo OpenAI
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

# Cria a base de dados FAISS para armazenar os chunks de texto vetorizados
db = FAISS.from_documents(texts_cleaned, embeddings)

# Cria o retriever usando o banco de dados FAISS
# O retriever será usado para buscar textos semelhantes com base na consulta
retriever = db.as_retriever(search_kwargs={'k': 3})

# Comentários adicionais:
# O `retriever` permite buscar os chunks mais relevantes no banco de dados 
# para qualquer consulta realizada no modelo. Isso é útil para responder perguntas
# com base no conteúdo do PDF carregado.
