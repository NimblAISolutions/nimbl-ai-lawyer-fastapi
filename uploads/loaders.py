from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import OnlinePDFLoader, WebBaseLoader, UnstructuredURLLoader, CSVLoader
from langchain.vectorstores import Milvus
import myconfig as config

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

# Подходит для тела сайтов
def upload_web_from_url(path):
    loader = WebBaseLoader(path)
    documents = loader.load()
    docs = text_splitter.split_documents(documents)

    return docs

# Для всего всего загружающегося
def upload_url(url):
    try:
        loader = UnstructuredURLLoader(urls=[url])
        data = loader.load()
        docs = text_splitter.split_documents(data)
    except Exception as e:
        return "Error: " + e

    return docs
 


async def base_loader(path: str, collection_name: str):
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
    
    documents = upload_url(path)

    if len(documents) < 1:
        try:
            documents = upload_web_from_url(path)
        except:
            return {"info": "Error corrupted", "error": "Erorr while uploading file", "status": "error"}
    
    try:
        database.add_documents(
            documents=documents,
        )
    except Exception as E:
        return {"info": "Error corrupted", "error": str(E), "status": "error"}
    
    return  {"info": "File uploaded successfully", "status":"ok"}

