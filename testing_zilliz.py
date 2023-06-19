# LANGCHAIN
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Milvus
from langchain.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
# SYSTEM
import os
# CUSTOM
from load_prompts import get_prompts
# ENV
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


# DATA
ZILLIZ_CLOUD_URI = os.environ.get("ZILLIZ_CLOUD_URI")
ZILLIZ_CLOUD_USERNAME = os.environ.get("ZILLIZ_CLOUD_USERNAME")
ZILLIZ_CLOUD_PASSWORD = os.environ.get("ZILLIZ_CLOUD_PASSWORD")

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
llm = OpenAI()
print(llm.model_name)


loader = PyPDFLoader("./GENERAL RULES.pdf")
document = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(document)


vector_db = Milvus.from_documents(
    docs,
    embedding=embeddings,
    collection_name="afsaindextest",
    connection_args={
        "uri": ZILLIZ_CLOUD_URI,
        "user": ZILLIZ_CLOUD_USERNAME,
        "password": ZILLIZ_CLOUD_PASSWORD,
        "secure": True,
    }
)

query = "Who is Governing Body?"
docs = vector_db.similarity_search(query)

context = docs[0].page_content

prompt = PromptTemplate.from_template(get_prompts().get("answer_by_context"))
AI_answer = llm(
    prompt.format(context=context, question=query)
)
print(AI_answer)
