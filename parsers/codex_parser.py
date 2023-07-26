from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Milvus
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import TokenTextSplitter, RecursiveCharacterTextSplitter
import os

CODEXES_DIR = os.path.join(os.getcwd(), 'codexes')
SPLITTER = RecursiveCharacterTextSplitter()

mini_db = {
    "constitution.01-01-2023.pdf": "Конституция Республики Казахстан",
    "ugolovka.10-07-2023.pdf": "Уголовный кодекс Республики Казахстан",
    "administrativka.10-07-2023.pdf": "Об административных правонарушениях"
}
OPENAI_API_KEY = "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"
ZILLIZ_CLOUD_URI = "https://in01-5c83064561b8fa7.aws-us-west-2.vectordb.zillizcloud.com:19533"
ZILLIZ_CLOUD_USERNAME = "db_admin"
ZILLIZ_CLOUD_PASSWORD = "urVcsBEaw7ZYvsf"
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY
                              )
db = Milvus(
        embedding_function=embeddings,
        collection_name="laws",
        connection_args={
            "uri": ZILLIZ_CLOUD_URI,
            "user": ZILLIZ_CLOUD_USERNAME,
            "password": ZILLIZ_CLOUD_PASSWORD,
            "secure": True,
        }
    )
def main():
    for codex in os.listdir(CODEXES_DIR):
        codex_filename = '.'.join(codex.split('.')[:-1])
        print(codex_filename)
        loader = PyPDFLoader(os.path.join(CODEXES_DIR, codex),)
        unsplitted_docs = loader.load()
        for unsplitted_doc in unsplitted_docs:
            unsplitted_doc.metadata['source'] = mini_db[codex]
        documents = SPLITTER.split_documents(unsplitted_docs)

        # db loader logic...
        db.add_documents(documents)
        print(documents[0].metadata.get("source"))


if __name__ == '__main__':
    main()
