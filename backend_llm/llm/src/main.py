# main.py
from config import  FAISS_INDEX_PATH, EMBEDDING_MODEL
from typing import Optional
from utils.document_loader import load_and_chunk_documents
from utils.vector_db import create_vector_db, load_vector_db
from utils.retrieval import retrieve_documents, generate_response, initialize_llm, PROMPT_TEMPLATE
from utils.logging_config import logger
from langchain_openai import OpenAIEmbeddings



def main(file_path: Optional[str] = None, url: Optional[str] = None, query: str = "Who is former Governor of the Bank of Canada, ?"):
    # Load and chunk documents
    documents = load_and_chunk_documents(file_path=file_path, url=url)
    if not documents:
        return
    
    # # Initialize embedding model OPEN API NOT USING NOW.
    embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        
    # Initialize local embedding model
    # embedding_model = get_local_embedding_model()
    
    # Create or load vector database
    db = load_vector_db(embedding_model, FAISS_INDEX_PATH)
    if not db:
        db = create_vector_db(documents, embedding_model, FAISS_INDEX_PATH)
        if not db:
            return
        
    # Retrieve documents
    retrieved_results = retrieve_documents(db,documents, query)
    if not retrieved_results:
        logger.warning("No relevant documents found.")
        return
    
    # Initialize LLM
    llm = initialize_llm()
    
    # Generate response
    response = generate_response(llm, PROMPT_TEMPLATE, retrieved_results, query)
    # print(f"AI Response: {response}")
    logger.debug(f"AI Response: {response}")

if __name__ == "__main__":
    # Example usage
    main(file_path="researcher.pdf")  # or main(url="https://example.com")



# # main.py
# from typing import Optional
# from dotenv import load_dotenv
# import os
# from config import FAISS_INDEX_PATH
# from utils.document_loader import load_and_chunk_documents
# from utils.vector_db import create_vector_db, load_vector_db, get_local_embedding_model
# from utils.retrieval import retrieve_documents, generate_response, initialize_local_llm, PROMPT_TEMPLATE
# from utils.logging_config import logger

# # Load environment variables
# load_dotenv()

# def main(file_path: Optional[str] = None, url: Optional[str] = None, query: str = "what is Architecture Innovative Load Balancing Strategy and Training Objective"):
#     # Load and chunk documents
#     documents = load_and_chunk_documents(file_path=file_path, url=url)
#     if not documents:
#         logger.warning("No documents found.")
#         return
    
#     logger.info(f"Loaded {len(documents)} documents.")
    
#     # Initialize local embedding model
#     embedding_model = get_local_embedding_model()
    
#     # Create or load vector database
#     db = load_vector_db(embedding_model, FAISS_INDEX_PATH)
#     if not db:
#         logger.info("Creating new FAISS index...")
#         db = create_vector_db(documents, embedding_model, FAISS_INDEX_PATH)
#         if not db:
#             logger.error("Failed to create FAISS index.")
#             return
    
#     # Retrieve documents
#     retrieved_results = retrieve_documents(db, query)
#     if not retrieved_results:
#         logger.warning("No relevant documents found.")
#         return
    
#     logger.info(f"Retrieved {len(retrieved_results)} documents.")
    
#     # Initialize local LLM
#     llm = initialize_local_llm()

    
#     # Generate response
#     response = generate_response(llm, PROMPT_TEMPLATE, retrieved_results, query)
#     logger.info(f"AI Response: {response}")

# if __name__ == "__main__":
#     # Example usage
#     main(file_path="researcher.pdf")  # or main(url="https://example.com")