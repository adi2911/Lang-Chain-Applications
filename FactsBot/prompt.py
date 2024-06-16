from dotenv import load_dotenv
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from redundant_filter_retriever import RedundantFilterRetriever

load_dotenv()

embeddings = OpenAIEmbeddings()
chat = ChatOpenAI()

#getting the chromadb instance

chromaDBInstance = Chroma(
    persist_directory="emb",
    embedding_function=embeddings
)

#retriever = chromaDBInstance.as_retriever() #Duplicates documents

#ensuring no duplicate results are run using custom retriever
retriever = RedundantFilterRetriever(embeddings=embeddings,chromaInstance=chromaDBInstance)

chain = RetrievalQA.from_chain_type(
    lllm=chat,
    retriever = retriever,
    chain_type="stuff"
)


result = chain.run("What is an interesting fact about english language")