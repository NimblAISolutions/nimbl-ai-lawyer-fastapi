# LANGCHAIN
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Milvus
from langchain.prompts import PromptTemplate
# SYSTEM
import os
# CUSTOM
from utils.load_prompts import get_prompts
# ENV
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


# DATA
ZILLIZ_CLOUD_URI = os.environ.get("ZILLIZ_CLOUD_URI")
ZILLIZ_CLOUD_USERNAME = os.environ.get("ZILLIZ_CLOUD_USERNAME")
ZILLIZ_CLOUD_PASSWORD = os.environ.get("ZILLIZ_CLOUD_PASSWORD")

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
llm = OpenAI()
print("Model: " + llm.model_name)

coll = input("Collection name: ")
database = Milvus(
    embedding_function=embeddings, 
    collection_name=coll, 
    connection_args={
        "uri": ZILLIZ_CLOUD_URI,
        "user": ZILLIZ_CLOUD_USERNAME,
        "password": ZILLIZ_CLOUD_PASSWORD,
        "secure": True,
    })

query = input("Enter query: ")
docs = database.similarity_search(query)

context = docs[0].page_content

prompt = PromptTemplate.from_template(get_prompts().get("answer_by_context"))
AI_answer = llm(
    prompt.format(context=context, question=query)
)
print(AI_answer)

print("\n\n\n\n" + context)