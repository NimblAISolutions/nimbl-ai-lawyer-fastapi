from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import TokenTextSplitter, RecursiveCharacterTextSplitter
import os

CODEXES_DIR = os.path.join(os.getcwd(), 'codexes')
SPLITTER = RecursiveCharacterTextSplitter()

mini_db = {
    "constitution.01-01-2023.pdf": "Конституция Республики Казахстан",
    "ugolovka.10-07-2023.pdf": "Уголовный кодекс Республики Казахстан",
    "administrativka.10-07-2023.pdf": "Об административных правонарушениях"
}

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
        print(documents[0].metadata.get("source"))


if __name__ == '__main__':
    main()
