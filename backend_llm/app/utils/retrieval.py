# utils/retrieval.py
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from typing import List
from rank_bm25 import BM25Okapi
from utils.logging_config import logger
from config import LLM_MODEL


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

# def retrieve_documents(db, query: str, k: int = 3) -> List:
#     try:
#         return db.similarity_search(query, k=k)
#     except Exception as e:
#         logger.error(f"Error retrieving documents: {e}")
#         return []
    

def retrieve_documents(db, documents, query: str, k: int = 3) -> List:
    """
    Perform both semantic search (FAISS) and keyword search (BM25), then combine results.
    """
    try:
        # Semantic search using FAISS
        semantic_results = db.similarity_search(query, k=k)

        # Keyword search using BM25
        keyword_results = bm25_search(documents, query, k=k)
        # Merge results while maintaining ranking priority
        results_dict = {doc.page_content: doc for doc in semantic_results}  # Prioritize FAISS results
        for doc in keyword_results:
            if doc.page_content not in results_dict:  # Add BM25 results if not already present
                results_dict[doc.page_content] = doc

        return list(results_dict.values())[:k]  # Return top-k merged results

    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        return []

def generate_response(llm, prompt_template, retrieved_results, query: str) -> str:
    if not retrieved_results:
        return "No relevant documents found."
    
    # # Prioritize documents based on relevance (e.g., similarity score)
    # max_docs = 3  # Adjust as needed
    # max_chars_per_doc = 500  # Adjust as needed
    
    # # Sort documents by relevance (assuming each doc has a `score` attribute)
    # sorted_docs = sorted(retrieved_results, key=lambda doc: doc.score, reverse=True)
    
    # # Extract the most relevant parts of the top documents
    # context = "\n".join([doc.page_content[:max_chars_per_doc] for doc in sorted_docs[:max_docs]])
    context = "\n".join([doc.page_content for doc in retrieved_results])
    
    final_prompt = prompt_template.format(context=context, question=query)
    
    try:
        response = llm.invoke(final_prompt)
        return response
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

    ### Response:
    """
)






# # utils/retrieval.py
# # utils/retrieval.py
# from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
# from langchain_huggingface import HuggingFacePipeline  # Updated import
# from langchain_core.prompts import PromptTemplate
# from typing import List
# import requests
# from langchain_community.llms import HuggingFaceTextGenInference
# from langchain_huggingface import HuggingFaceEndpoint
# from langchain_core.prompts import PromptTemplate
# import os
# from langchain_huggingface import HuggingFaceEndpoint
# from utils.logging_config import logger
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# from langchain_community.llms import HuggingFacePipeline
# import torch
# from config import HUGGINGFACEHUB_API_TOKEN


# # # Free LLM
# # def initialize_local_llm():
# #     model_name = "meta-llama/Llama-2-7b-chat-hf"  # Replace with your preferred local model (e.g., "gpt2", "Llama-2-7b")
# #     tokenizer = AutoTokenizer.from_pretrained(model_name)
# #     model = AutoModelForCausalLM.from_pretrained(model_name)

# #     # Adjust max_length or max_new_tokens
# #     pipe = pipeline(
# #         "text-generation",
# #         model=model,
# #         tokenizer=tokenizer,
# #         max_new_tokens=200,  # Limit the number of new tokens generated
# #         temperature=0.7,
# #         top_p=0.95,
# #         repetition_penalty=1.15,
# #         truncation=True,  # Explicitly enable truncation
# #         device="cpu"  # Use "cuda" if you have a GPU
# #     )
# #     return HuggingFacePipeline(pipeline=pipe)



# # # LLM With API KEY
# # def initialize_local_llm():
# #     # Hugging Face API endpoint for the model
# #     API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"

# #     # Fetch the Hugging Face API token from environment variables
# #     API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
# #     if not API_TOKEN:
# #         logger.error("HUGGINGFACEHUB_API_TOKEN environment variable not set.")
# #         raise ValueError("HUGGINGFACEHUB_API_TOKEN environment variable not set.")

# #     # Initialize the Hugging Face Inference API client
# #     try:
# #         llm = HuggingFaceEndpoint(
# #             endpoint_url=API_URL,
# #             max_new_tokens=200,  # Adjust based on your needs
# #             temperature=0.7,     # Adjust for creativity
# #             top_p=0.95,          # Adjust for diversity
# #             repetition_penalty=1.15,  # Adjust to avoid repetition
# #             headers={"Authorization": f"Bearer {API_TOKEN}"}
# #         )
# #         return llm
# #     except Exception as e:
# #         logger.error(f"Error initializing Hugging Face Inference API client: {e}")
# #         raise



# def initialize_local_llm():
#     # Define the model name
#     model_name = "meta-llama/Llama-2-7b-chat-hf"

#     # Check if Hugging Face token is set (required for gated models)
#     API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
#     if not API_TOKEN:
#         logger.error("HUGGINGFACEHUB_API_TOKEN environment variable not set.")
#         raise ValueError("HUGGINGFACEHUB_API_TOKEN environment variable not set.")

#     try:
#         # Load the tokenizer and model
#         tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=API_TOKEN)
        
#         # Load the model in 8-bit precision to save memory (requires `bitsandbytes` library)
#         model = AutoModelForCausalLM.from_pretrained(
#             model_name,
#             device_map="auto",  # Automatically offloads to CPU/GPU
#             load_in_8bit=True,  # Quantize the model to 8-bit
#             use_auth_token=API_TOKEN
#         )

#         # Return the tokenizer and model
#         return tokenizer, model

#     except Exception as e:
#         logger.error(f"Error initializing local LLM: {e}")
#         raise





# def retrieve_documents(db, query: str, k: int = 3) -> List:
#     try:
#         return db.similarity_search(query, k=k)
#     except Exception as e:
#         logger.error(f"Error retrieving documents: {e}")
#         return []
    

# # LLM With response = llm(final_prompt) METHOD
# # def generate_response(llm, prompt_template, retrieved_results, query: str) -> str:
# #     if not retrieved_results:
# #         return "No relevant documents found."
    
# #     context = "\n".join([doc.page_content for doc in retrieved_results])
# #     final_prompt = prompt_template.format(context=context, question=query)
    
# #     try:
# #         # Generate response using the Hugging Face Inference API
# #         response = llm(final_prompt)
# #         return response
# #     except Exception as e:
# #         logger.error(f"Error generating response: {e}")
# #         return "An error occurred while generating the response."

# #   TESTIN ONLY FOR NOW
# def generate_response(llm, prompt_template, retrieved_results, query: str) -> str:
#     """
#     Generates a response using the Hugging Face Inference API.

#     Args:
#         llm: Initialized HuggingFaceEndpoint object.
#         prompt_template: A string template for the prompt, with placeholders for `context` and `question`.
#         retrieved_results: List of documents (e.g., from a retriever).
#         query: The user's query.

#     Returns:
#         Generated response as a string.
#     """
#     if not retrieved_results:
#         return "No relevant documents found."
    
#     # Prepare the context from retrieved results
#     context = "\n".join([doc.page_content for doc in retrieved_results])
    
#     # Format the final prompt using the template
#     final_prompt = prompt_template.format(context=context, question=query)
    
#     try:
#         # Generate a response using the Hugging Face Inference API
#         response = llm.invoke(final_prompt)  # Use the `invoke` method
#         return response
#     except Exception as e:
#         logger.error(f"Error generating response: {e}")
#         return "An error occurred while generating the response."
    

# # Example usage
# def generate_response(prompt, tokenizer, model):
#     try:
#         # Tokenize the input
#         inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

#         # Generate a response
#         outputs = model.generate(
#             **inputs,
#             max_new_tokens=200,  # Adjust based on your needs
#             temperature=0.7,     # Adjust for creativity
#             top_p=0.95,          # Adjust for diversity
#             repetition_penalty=1.15  # Adjust to avoid repetition
#         )

#         # Decode the response
#         response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#         return response

#     except Exception as e:
#         logger.error(f"Error generating response: {e}")
#         raise
