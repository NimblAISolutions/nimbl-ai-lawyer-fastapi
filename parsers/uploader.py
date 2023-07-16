import pinecone
from time import sleep
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone, Milvus
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from enum import Enum
from colorama import Fore, Style


OPENAI_API_KEY = ""
DATA_PATH = r""
ZILLIZ_CLOUD_URI = ""
ZILLIZ_CLOUD_USERNAME = ""
ZILLIZ_CLOUD_PASSWORD = ""
ZILLIZ_CLOUD_COLLECTION = ""
PINECONE_API_KEY = ""
PINECONE_ENVIRONMENT = ""
PINECONE_INDEX = ""

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)


class LogStatuses(Enum):
    WARNING = Fore.RED
    SUCCESS = Fore.LIGHTGREEN_EX
    INFO = Fore.LIGHTYELLOW_EX
    ERROR = Fore.RED


# LOGGER HELPER FUNC
def log(status: LogStatuses, text: str):
    print(status.value + text + Style.RESET_ALL)


def get_db(type):
    if type == "zilliz":
        db = Milvus(
            embedding_function=embeddings, 
            collection_name=ZILLIZ_CLOUD_COLLECTION,
            connection_args={
                "uri": ZILLIZ_CLOUD_URI,
                "user": ZILLIZ_CLOUD_USERNAME,
                "password": ZILLIZ_CLOUD_PASSWORD,
                "secure": True,
            }
        )
    elif type == "pinecone":        
        pinecone.init(      
            api_key=PINECONE_API_KEY,
            environment=PINECONE_ENVIRONMENT
        )
        index = pinecone.Index(PINECONE_ENVIRONMENT)

        db = Pinecone(embedding_function=embeddings.embed_query, index=index, text_key="some")
    else:
        log(LogStatuses.ERROR, "Not supported type of DB!")
        raise ValueError("No such type")

    return db


# @param type zilliz/pinecone
def custom_loader(directory_path: str, source):
    cnt = 0
    DB = get_db(source)

    # Iterate through folders in the directory
    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path, folder_name)
        for folder_name2 in os.listdir(folder_path):
            folder_path2 = os.path.join(folder_path, folder_name2)
            for folder_name3 in os.listdir(folder_path2):
                folder_path3 = os.path.join(folder_path2, folder_name3)
        # Check if the item is a directory
                if os.path.exists(folder_path3 + "/success.txt"):
                    log(LogStatuses.SUCCESS, folder_path3 + " skipped!")
                    continue
                loader = TextLoader(
                    folder_path3 + "/parsed.txt", encoding="utf-8")
                documents = loader.load()
                # print(documents)
                final = text_splitter.split_documents(documents)

                # Open the text file and read its contents
                with open(folder_path3+"/link.txt", 'r') as file:
                    content = file.read()

                # Remove newline characters and create a single string
                content = content.replace('\n', '')
                for i in range(len(final)):
                    final[i].metadata["source"] = content

                try:
                    DB.add_documents(final)
                    log(LogStatuses.SUCCESS, folder_path3 + " loaded")
                    with open(folder_path3 + "/success.txt", "w", encoding="utf-8") as f:
                        f.write("ok")

                    cnt += 1
                    print(cnt)
                except Exception as e:
                    log(LogStatuses.ERROR, "\nError: " + str(e))
                    sleep(60*5)
                    DB.add_documents(final)


    log(LogStatuses.SUCCESS, "SUCCESSFULLY")


def success_remover(directory_path: str):
    # Iterate through folders in the directory
    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path, folder_name)
        for folder_name2 in os.listdir(folder_path):
            folder_path2 = os.path.join(folder_path, folder_name2)
            for folder_name3 in os.listdir(folder_path2):
                folder_path3 = os.path.join(folder_path2, folder_name3)
        # Check if the item is a directory
                if os.path.exists(folder_path3 + "/success.txt"):
                    log(LogStatuses.ERROR, folder_path3 + " cleared!")
                    os.remove(folder_path3 + "/success.txt")
                    continue


# success_remover(DATA_PATH) # removes all success marks within folders
# custom_loader(DATA_PATH, "zilliz")
# custom_loader(DATA_PATH, "pinecone")

