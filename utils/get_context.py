from langchain.vectorstores import Milvus
from langchain.embeddings.openai import OpenAIEmbeddings
import os

ZILLIZ_CLOUD_URI = os.environ.get("ZILLIZ_CLOUD_URI")
ZILLIZ_CLOUD_USERNAME = os.environ.get("ZILLIZ_CLOUD_USERNAME")
ZILLIZ_CLOUD_PASSWORD = os.environ.get("ZILLIZ_CLOUD_PASSWORD")


embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

database = Milvus(
    embedding_function=embeddings,
    collection_name="afsaindextest",
    connection_args={
        "uri": ZILLIZ_CLOUD_URI,
        "user": ZILLIZ_CLOUD_USERNAME,
        "password": ZILLIZ_CLOUD_PASSWORD,
        "secure": True,
    }
)

def get_context_from_milvus(message: str):
    
    return database.similarity_search(message, k=2)[0]