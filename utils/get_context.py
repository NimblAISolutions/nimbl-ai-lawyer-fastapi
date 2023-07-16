from langchain.vectorstores import Milvus, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
import os
from custom_types import Sources
# from langchain.llms import OpenAI
# from langchain.retrievers import ContextualCompressionRetriever
# from langchain.retrievers.document_compressors import LLMChainExtractor

ZILLIZ_CLOUD_URI = os.environ.get("ZILLIZ_CLOUD_URI")
ZILLIZ_CLOUD_USERNAME = os.environ.get("ZILLIZ_CLOUD_USERNAME")
ZILLIZ_CLOUD_PASSWORD = os.environ.get("ZILLIZ_CLOUD_PASSWORD")
PINECONE_API_KEY_SMALL = os.environ.get("PINECONE_API_KEY_SMALL")
PINECONE_API_KEY_LARGE = os.environ.get("PINECONE_API_KEY_LARGE")
PINECONE_ENVIRONMENT_LARGE = os.environ.get("PINECONE_ENVIRONMENT_LARGE")
PINECONE_ENVIRONMENT_SMALL = os.environ.get("PINECONE_ENVIRONMENT_SMALL")
PINECONE_INDEX_LARGE = os.environ.get("PINECONE_INDEX_LARGE")
PINECONE_INDEX_SMALL = os.environ.get("PINECONE_INDEX_SMALL")

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
# llm = OpenAI(temperature=1.0)

database_milvus_large = Milvus(
    embedding_function=embeddings,
    collection_name="egovkz_all_services",
    connection_args={
        "uri": ZILLIZ_CLOUD_URI,
        "user": ZILLIZ_CLOUD_USERNAME,
        "password": ZILLIZ_CLOUD_PASSWORD,
        "secure": True,
    }
)
database_milvus_small = Milvus(
    embedding_function=embeddings,
    collection_name="egovkz_all_services_small",
    connection_args={
        "uri": ZILLIZ_CLOUD_URI,
        "user": ZILLIZ_CLOUD_USERNAME,
        "password": ZILLIZ_CLOUD_PASSWORD,
        "secure": True,
    }
)


def get_database_pinecone(type: Sources):
    if type is Sources.pinecone_large:
        api_key = PINECONE_API_KEY_LARGE
        environment = PINECONE_ENVIRONMENT_LARGE
        index = PINECONE_INDEX_LARGE
    elif type is Sources.pinecone_small:
        api_key = PINECONE_API_KEY_SMALL
        environment = PINECONE_ENVIRONMENT_SMALL
        index = PINECONE_INDEX_SMALL
    else:
        raise ValueError("No such value for source: " + type.value)

    pinecone.init(
        api_key=api_key,
        environment=environment
    )
    index = pinecone.Index(index)

    return Pinecone(embedding_function=embeddings.embed_query, index=index, text_key="some")


async def get_context_from_milvus(message: str):

    # llm = OpenAI(temperature=1.0)
    # contexts = llm.predict(
    #     f"Вы помощник языковой модели ИИ. Ваша задача состоит в том, чтобы сгенерировать 2 разные версии данного вопроса пользователя, чтобы получить соответствующие документы из векторной базы данных. Создавая несколько точек зрения на вопрос пользователя, ваша цель — помочь пользователю преодолеть некоторые ограничения поиска сходства на основе расстояния. Оригинальный вопрос: {message} ответ должен быть в формате: 1.оригинальный вопрос 2. 1 версия 3. 2 версия")
    # print(contexts)
    context = database_milvus_large.similarity_search(message, k=5)
    print(context[0:5])
    # return await compression_retriever.aget_relevant_documents(message)
    return context[:5]


async def get_context_from_db(message: str, source: Sources):
    if source is Sources.zilliz_large:
        database = database_milvus_large
    elif source is Sources.zilliz_small:
        database = database_milvus_small
    elif source is Sources.pinecone_small or source is Sources.pinecone_large:
        database = get_database_pinecone(source)
    else:
        raise ValueError("Incorrect type!")
    context = database.similarity_search(message, k=5)[:5]
    print(context)

    return context
