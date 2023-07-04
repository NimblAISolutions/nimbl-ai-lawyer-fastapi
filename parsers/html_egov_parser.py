from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.vectorstores import Milvus
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import os
import re
from enum import Enum
from colorama import Fore, Style

driver = webdriver.Edge()

### CONFIG
OPENAI_API_KEY="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"
ZILLIZ_CLOUD_URI = "https://in01-5c83064561b8fa7.aws-us-west-2.vectordb.zillizcloud.com:19533"
ZILLIZ_CLOUD_USERNAME = "db_admin"
ZILLIZ_CLOUD_PASSWORD = "urVcsBEaw7ZYvsf"
###

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

class Statuses(Enum):
    WARNING = Fore.RED
    SUCCESS = Fore.LIGHTGREEN_EX
    INFO = Fore.LIGHTYELLOW_EX

# LOGGER HELPER FUNC
def log(status: Statuses, text: str):
    print(status.value + text + Style.RESET_ALL)

def upload_html(path: str, source: str):
    try:
        loader = UnstructuredHTMLLoader(
            path,
        )

        data = loader.load()
        docs = text_splitter.split_documents(data)
        def processor(doc):
            doc.metadata["source"] = source
            return doc
        docs = list(map(processor, docs))
    except Exception as e:
        return "Error: " + str(e)

    return docs


def open_page_and_parse(url: str):
    driver.get(url)

    service, category, subcategory = url.split("/")[-3: ]
    BASE_PATH = os.path.join(service, category, subcategory)
    RAW_HTML_PATH = os.path.join(BASE_PATH, "raw.html")
    LINK_TXT_PATH = os.path.join(BASE_PATH, "link.txt")
    PARSED_TXT_PATH = os.path.join(BASE_PATH, "parsed.txt")

    isExist = os.path.exists(f"./{BASE_PATH}")
   
    if not isExist:
        os.makedirs(f"./{BASE_PATH}")

    html = driver.page_source
    with open(LINK_TXT_PATH, "w", encoding="utf-8") as f:
        f.write(url)

    with open(RAW_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    parsed_html = upload_html(RAW_HTML_PATH, url)
    
    with open(PARSED_TXT_PATH, "w", encoding="utf-8") as f:
        f.write(str(parsed_html))
        
    return parsed_html


# Engine 
def base_loader(path: str, collection_name: str):
    database = Milvus(
        embedding_function=embeddings,
        collection_name=collection_name,
        connection_args={
            "uri": ZILLIZ_CLOUD_URI,
            "user": ZILLIZ_CLOUD_USERNAME,
            "password": ZILLIZ_CLOUD_PASSWORD,
            "secure": True,
        }
    )
    
    documents = open_page_and_parse(path)
    if len(documents) < 1:
        return "No content"

    try:
        database.add_documents(
            documents=documents,
        )
        log(Statuses.SUCCESS, path + " loaded")

    except Exception as E:
        print({"info": "Error corrupted", "error": str(E), "status": "error"})
        return {"info": "Error corrupted", "error": str(E), "status": "error"}
    
    return  {"info": "File uploaded successfully", "status":"ok"}


# Engine
def parse_services_and_upload(url: str, collection_name: str):
    driver.get(url)
    protocol, host = re.split(r'://|/', url)[0:2]
    base_url = protocol + "://" + host

    html = bs(driver.page_source, 'html.parser')
    services = html.find_all("div", class_="block-horizontal items-list")[0]
    links = [i.get("href") for i in services.find_all("a", {"rel": "noopener noreferrer"})]
    for link in links:
        base_loader(base_url + link, collection_name)


service_urls = [
    "https://egov.kz/cms/ru/categories/passport",
    "https://egov.kz/cms/ru/categories/registration",
    "https://egov.kz/cms/ru/categories/for_foreigners",
    "https://egov.kz/cms/ru/categories/move_abroad",
    "https://egov.kz/cms/ru/categories/job_search",
    "https://egov.kz/cms/ru/categories/employment_relations",
    "https://egov.kz/cms/ru/categories/state_service",
    "https://egov.kz/cms/ru/categories/customs",
    "https://egov.kz/cms/ru/categories/taxation",
    "https://egov.kz/cms/ru/categories/economics",
]

info_urls = [
    "https://egov.kz/cms/ru/information/about/help-elektronnoe-pravitelstvo",
    "https://egov.kz/cms/ru/information/about/projects",
    "https://egov.kz/cms/ru/information/about/mobile_application",
    "https://egov.kz/cms/ru/articles/instruction-issuance-of-technicalpassport",
    "https://egov.kz/cms/ru/articles/instruction-realestate-owners",
    "https://egov.kz/cms/ru/articles/instruction-registration-for-non-owners",
    
]

for info_url in info_urls:
    log(Statuses.INFO, info_url + " loading...")
    base_loader(info_url, "egovkz")
    log(Statuses.INFO, info_url + " loaded!")
    print()

driver.close()
log(Statuses.SUCCESS, "FINISH")
