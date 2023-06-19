from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Milvus
from langchain.document_loaders import PyPDFLoader
# CONFIG
import config


def upload_pdf_from_url(path, coll_name):
    # MILVUS
    database = Milvus(
        embedding_function=config.embeddings, 
        collection_name=coll_name, 
        connection_args={
        "uri": config.ZILLIZ_CLOUD_URI,
        "user": config.ZILLIZ_CLOUD_USERNAME,
        "password": config.ZILLIZ_CLOUD_PASSWORD,
        "secure": True,
    })

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    loader = PyPDFLoader(path)
    document = loader.load()
    docs = text_splitter.split_documents(document)
    
    database.add_documents(
        documents=docs
    )

