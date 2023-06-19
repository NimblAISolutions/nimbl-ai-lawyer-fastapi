from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Milvus
from langchain.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
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

def upload_data_from_url(path, collection_name):

    loader = PyPDFLoader(path)
    document = loader.load()
    docs = text_splitter.split_documents(document)


    Milvus.add_documents(
        docs,
        embedding=embeddings,
        collection_name=collection_name,
        connection_args={
            "uri": ZILLIZ_CLOUD_URI,
            "user": ZILLIZ_CLOUD_USERNAME,
            "password": ZILLIZ_CLOUD_PASSWORD,
            "secure": True,
        }
    )

