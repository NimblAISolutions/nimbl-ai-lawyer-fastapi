from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv, find_dotenv
# Build a sample vectorDB
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
load_dotenv(find_dotenv())
template = """You are an AI language model assistant. Your task is 
    to generate 3 different versions of the given user 
    question to retrieve relevant documents from a vector  database. 
    By generating multiple perspectives on the user question, 
    your goal is to help the user overcome some of the limitations 
    of distance-based similarity search. Provide these alternative 
    questions seperated by newlines. Original question: {question}"""
# Load PDF
loaders = [
    PyPDFLoader(
        "/Users/alibiserikbay/Developer/ChatBot/data/ISLAMIC BANKING BUSINESS PRUDENTIAL RULES.pdf"),
    PyPDFLoader(
        "/Users/alibiserikbay/Developer/ChatBot/data/ISLAMIC FINANCE RULES.pdf"),
    PyPDFLoader("/Users/alibiserikbay/Developer/ChatBot/data/GENERAL RULES.pdf")
]

docs = []
for loader in loaders:
    docs.extend(loader.load())

# Split
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500, chunk_overlap=150)
splits = text_splitter.split_documents(docs)

# VectorDB
embedding = OpenAIEmbeddings()
vectordb = Chroma.from_documents(documents=splits, embedding=embedding)

retriever = vectordb.as_retriever()


prompt = PromptTemplate(
    input_variables=["question"], template=template)

llm = OpenAI(temperature=0)
chatgpt_chain = LLMChain(
    llm=llm,
    prompt=prompt,
)

compressor = LLMChainExtractor.from_llm(llm)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever)

output = chatgpt_chain.predict(
    question="What are the rules of Islamic Banking?")

string = str(output)
lines = string.strip().split('\n')

queries = [line.strip() for line in lines]

documents = []
for query in queries:
    docs = compression_retriever.get_relevant_documents(query)
    documents.extend(docs)

unique_documents_dict = {
    (doc.page_content, tuple(sorted(doc.metadata.items()))): doc
    for doc in documents
}

unique_documents = list(unique_documents_dict.values())

for docs in unique_documents:
    print(f'{docs} \n \n ')
