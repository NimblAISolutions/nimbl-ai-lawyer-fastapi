from langchain.vectorstores import Milvus
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
import os

ZILLIZ_CLOUD_URI = os.environ.get("ZILLIZ_CLOUD_URI")
ZILLIZ_CLOUD_USERNAME = os.environ.get("ZILLIZ_CLOUD_USERNAME")
ZILLIZ_CLOUD_PASSWORD = os.environ.get("ZILLIZ_CLOUD_PASSWORD")


embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
# llm = OpenAI(temperature=0)

database = Milvus(
    embedding_function=embeddings,
    collection_name="egovkz",
    connection_args={
        "uri": ZILLIZ_CLOUD_URI,
        "user": ZILLIZ_CLOUD_USERNAME,
        "password": ZILLIZ_CLOUD_PASSWORD,
        "secure": True,
    }
)
# compressor = LLMChainExtractor.from_llm(llm)
# compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=database.as_retriever())

async def get_context_from_milvus(message: str):
    # return await compression_retriever.aget_relevant_documents(message)
    return database.similarity_search(message, k=2)[0]
