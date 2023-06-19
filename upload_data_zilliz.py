from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Milvus
from langchain.document_loaders import PyPDFLoader
# OS
import os
# ENV
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

# DATA
ZILLIZ_CLOUD_URI = os.environ.get("ZILLIZ_CLOUD_URI")
ZILLIZ_CLOUD_USERNAME = os.environ.get("ZILLIZ_CLOUD_USERNAME")
ZILLIZ_CLOUD_PASSWORD = os.environ.get("ZILLIZ_CLOUD_PASSWORD")


def upload_pdf_from_url(path, coll_name):
    # MILVUS
    database = Milvus(
        embedding_function=embeddings, 
        collection_name=coll_name, 
        connection_args={
        "uri": ZILLIZ_CLOUD_URI,
        "user": ZILLIZ_CLOUD_USERNAME,
        "password": ZILLIZ_CLOUD_PASSWORD,
        "secure": True,
    })


    loader = PyPDFLoader(path)
    document = loader.load()
    docs = text_splitter.split_documents(document)
    
    database.add_documents(
        documents=docs
    )

