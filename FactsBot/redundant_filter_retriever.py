from typing import Any, Dict, List
from langchain.embeddings.base import Embeddings
from langchain.vectorstores.chroma import Chroma
from langchain.schema import BaseRetriever

class RedundantFilterRetriever(BaseRetriever):
    embeddings: Embeddings
    chromaInstance: Chroma

    #This is must method when we use RetrievalQAChain, so we are customising it to remove duplicate documents
    def get_relevant_documents(self, query):
        #calculate embedding for the 'query' string
        emb = self.embeddings.embed_query(query)

        #take embeddings and feed the into that
        #max_marginal_relevance_serach_by_vector
        return self.chromaInstance.max_marginal_relevance_search_by_vector(embedding=emb,lambda_mult=0.8)


    #this method is not required but , it mandatory to define the function when we define a custom retriever
    async def aget_relevant_documents(self, query):
        return []