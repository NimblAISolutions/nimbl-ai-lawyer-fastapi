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
# llm = OpenAI(temperature=1.0)

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

async def get_context_from_milvus(message: str):

    # llm = OpenAI(temperature=1.0)
    # contexts = llm.predict(
    #     f"Вы помощник языковой модели ИИ. Ваша задача состоит в том, чтобы сгенерировать 2 разные версии данного вопроса пользователя, чтобы получить соответствующие документы из векторной базы данных. Создавая несколько точек зрения на вопрос пользователя, ваша цель — помочь пользователю преодолеть некоторые ограничения поиска сходства на основе расстояния. Оригинальный вопрос: {message} ответ должен быть в формате: 1.оригинальный вопрос 2. 1 версия 3. 2 версия")
    # print(contexts)
    context = database.similarity_search(message, k=5)
    print(context[0:5])
    # return await compression_retriever.aget_relevant_documents(message)
    return context[:5]
