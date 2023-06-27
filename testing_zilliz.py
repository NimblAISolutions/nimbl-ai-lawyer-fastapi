import sys
from langchain.chains import ConversationalRetrievalChain
# LANGCHAIN
from langchain.llms import OpenAI
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Milvus
from langchain.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
# SYSTEM
import os
# ENV
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


# DATA
ZILLIZ_CLOUD_URI = os.environ.get("ZILLIZ_CLOUD_URI")
ZILLIZ_CLOUD_USERNAME = os.environ.get("ZILLIZ_CLOUD_USERNAME")
ZILLIZ_CLOUD_PASSWORD = os.environ.get("ZILLIZ_CLOUD_PASSWORD")

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
llm = OpenAI(temperature=0)
print(llm.model_name)


database = Milvus(
    embedding_function=embeddings,
    collection_name="jusanInvest",
    connection_args={
        "uri": ZILLIZ_CLOUD_URI,
        "user": ZILLIZ_CLOUD_USERNAME,
        "password": ZILLIZ_CLOUD_PASSWORD,
        "secure": True,
    })

template = """
Вы являетесь помощником юриста в финансовой компании. \
Исходя из контекста, отвечайте дружелюбным и предупредительным тоном. \
с очень краткими ответами. \
Перепроверьте свои ответы на предмет точности и связности. \
При необходимости задавайте уточняющие вопросы, чтобы собрать больше информации, прежде чем давать ответ.\
Если вы столкнетесь с трудным вопросом, сохраняйте спокойствие и предлагайте помощь в меру своих возможностей.\
Контекст:\n{context}\n
Если не ответа нет в контексте, скажи что не знаешь ответ на вопрос \
История чата:
{chat_history}
Вопрос: {question}
"""

PROMPT = PromptTemplate(
    input_variables=["chat_history", "question", "context"],
    template=template
)


qa = ConversationalRetrievalChain.from_llm(
    llm=OpenAI(temperature=0),
    retriever=database.as_retriever(),
    return_source_documents=True,
    combine_docs_chain_kwargs={"prompt": PROMPT}
)


chat_history = []


def ask_question(question):
    if question.lower() == 'exit':
        print("\nThank you for using the AIFC chatbot!")
        sys.exit(0)
    docs = database.similarity_search(query)
    context = docs[0].page_content
    result = qa({"question": question, "context": context, "chat_history": chat_history})
    chat_history.append((question, result['answer']))

    print(f'User: {question}')
    print(f'Chatbot: {result["answer"]}')


print("Welcome to the AIFC chatbot! Type 'exit' to stop.")

while True:
    query = input("Please enter your question: ")
    ask_question(query)