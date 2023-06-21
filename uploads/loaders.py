from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import OnlinePDFLoader


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

print(upload_web_from_url("https://rexydye.ink/MOCK_DATA.xlsx"))
