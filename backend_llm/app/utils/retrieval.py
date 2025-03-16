# utils/retrieval.py
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from typing import List
from rank_bm25 import BM25Okapi
from app.utils.settings import LLM_MODEL
from app.utils.logging_config import get_logger
logger = get_logger()

def bm25_search(documents, query, k=3):
    """
    Perform BM25 keyword-based retrieval.
    """
    tokenized_corpus = [doc.page_content.split() for doc in documents]
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = query.split()
    doc_scores = bm25.get_scores(tokenized_query)
    
    # Rank and retrieve top-k results
    top_indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:k]
    return [documents[i] for i in top_indices]



def retrieve_documents(db, documents, query: str, k: int = 3) -> List:
    """
    Perform both semantic search (FAISS) and keyword search (BM25), then combine results.
    """
    try:
        semantic_results = db.similarity_search(query, k=k)
 
        # Keyword search using BM25
        keyword_results = bm25_search(documents, query, k=k)


        """
        # This code block is for displaying search results using BM25 and FAISS.
        # It is currently unused but may be used later.
        print("Keyword Search Results (BM25):")
        for i, doc in enumerate(keyword_results):
            print(f"Document {i + 1}: {doc.page_content}")
        print("--------------------------------------------------------------")    
        print("Semantic Search Results (FAISS):")
        for i, doc in enumerate(semantic_results):
            print(f"Document {i + 1}: {doc.page_content}")
        """  

        # Merge results while maintaining ranking priority
        results_dict = {doc.page_content: doc for doc in semantic_results}  
        for doc in keyword_results:
            if doc.page_content not in results_dict:  
                results_dict[doc.page_content] = doc

        return list(results_dict.values())[:k]  

    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        return []




def generate_response(llm, prompt_template, retrieved_results, query: str) -> str:
    if not retrieved_results:
        return "No relevant documents found."
    
    context = "\n".join([doc.page_content for doc in retrieved_results])
    
    final_prompt = prompt_template.format(context=context, question=query)
    
    try:
        response = llm.invoke(final_prompt)
        return response.content  # Extract content from AIMessage object
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "An error occurred while generating the response."

def initialize_llm():
    return ChatOpenAI(
        model=LLM_MODEL,
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()]
    )

PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    Answer the question based on the context. If the answer is not in the context, say "I don't know."

    Context:
    {context}

    Question:
    {question}

    Instructions:
    - If the context contains formulas or technical details pleaseinclude them in the response.
    - Summarize concisely but retain all critical information.

    Response:
    """
)






