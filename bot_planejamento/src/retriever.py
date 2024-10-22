## Loader do PDF
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
# config.py
import os
from dotenv import load_dotenv

path = "C:\\Users\\FHEMIG\Desktop\\Pedro (1)\\Projetos\Zulip Bots\\chatbots-zulip\\data\\manual_impacto.pdf"

#loader_un = UnstructuredPDFLoader(path)
loader_structured = PyMuPDFLoader(path)

pages_str = loader_structured.load()

from langchain.text_splitter import CharacterTextSplitter

## Criando texto splitter
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=0
    )

## Split
texts = text_splitter.split_documents(pages_str)

## Função para remover espaço em branco

def remove_ws(d):
    text = d.page_content.replace("\n", "")
    d.page_content = text
    return d

# Clean texts by removing whitespace from each document
texts_cleaned = [remove_ws(d) for d in texts]

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv(dotenv_path="C:\\Users\\FHEMIG\\Desktop\\Pedro (1)\\Projetos\\Zulip Bots\\chatbots-zulip\\env\\.env")

# Acessar a chave da OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# uses OpenAI embeddings to build a retriever
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
# Creates the document retriever using docs and embeddings
db = FAISS.from_documents(texts_cleaned, embeddings)



# Asking the retriever to do similarity search based on Query
#query = "Foreign Aid for Lowari Road Tunnel & Access Roads Project (2nd Revised )"
#answer = db.similarity_search(query)

# Building the retriever
retriever = db.as_retriever(search_kwargs={'k': 3})