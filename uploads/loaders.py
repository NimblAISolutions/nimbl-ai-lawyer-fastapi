from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import OnlinePDFLoader
from langchain.vectorstores import Milvus
from all_types import Formats
import config


# Подходит для сайтов, online csv, json
def upload_web_from_url(path):
    loader = WebBaseLoader(path)
    documents = loader.load_and_split()

    return documents


def upload_pdf_from_url(path):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    loader = OnlinePDFLoader(path)
    document = loader.load()
    docs = text_splitter.split_documents(document)

    return docs


async def base_loader(path: str, collection_name: str, format: Formats):
    val = format.value
    database = Milvus(
        embedding_function=config.embeddings,
        collection_name=collection_name,
        connection_args={
            "uri": config.ZILLIZ_CLOUD_URI,
            "user": config.ZILLIZ_CLOUD_USERNAME,
            "password": config.ZILLIZ_CLOUD_PASSWORD,
            "secure": True,
        }
    )

    if val in (Formats.CSV, Formats.JSON, Formats.SITE):
        documents = upload_web_from_url(path)

    # elif val in (Formats.XLS, Formats.XLSX):
    #     pass
    
    # elif val in (Formats.DOC, Formats.DOCX):
    #     pass
    
    elif val is Formats.PDF:
        documents=upload_pdf_from_url(path)

    else:
        return {"info": "File format not added now", "status": "error"}
    
    try:
        database.add_documents(
            documents=documents,
        )
    except Exception as E:
        return {"info": "Error corrupted", "error": E, "status": "error"}
    
    return  {"info": "File uploaded successfully", "status":"ok"}

