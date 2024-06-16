from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from dotenv import load_dotenv



load_dotenv()

embeddings = OpenAIEmbeddings()

#chunking text into different document
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size = 200, #If number of characters tghat is 200 here reached, it will find the nearest seperater and split.
    chunk_overlap = 0 #It takes x number of characters from the last chunk and start from that
)


loader = TextLoader("facts.txt")
# we cannot put all the details in fact file to the LLM , it will cost us way more in
# terms of cost and time and relevance in output

docs = loader.load_and_split(text_splitter=text_splitter)

#storing to chromadb


# Every time below line is exceuted the embeeding are recalculated and stored back in the same db , which makes the data duplicate
db = Chroma.from_documents(docs, embedding=embeddings, persist_directory="emb")

result = db.similarity_search_with_score("What is an interesting fact about  english language?",
                                         k=1) # k gives the number of documents that we want to fetch. 

for res in result:
    print("\n")
    print(res[1])
    print(res[0].page_content)







