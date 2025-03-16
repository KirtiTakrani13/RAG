from fastapi import APIRouter, HTTPException, logger
from typing import Optional
import logging


from app.utils.retrieval import PROMPT_TEMPLATE, generate_response, initialize_llm, retrieve_documents
from app.utils.global_vars import dbnn, db_lock, all_documents, processed_files, embedding_model, UPLOAD_DIR
from app.utils.logging_config import get_logger
logger = get_logger()

router = APIRouter()



@router.post("/query/")
async def query_rag(query: str, top_k: Optional[int] = 3):
    """
    Endpoint for RAG pipeline.
    - query: User query.
    - top_k: Number of documents to retrieve (default: 3).
    """
    global dbnn  # Use the global vector database
    global all_documents  

    if not dbnn:
        logger.error("Vector database not initialized")
        raise HTTPException(status_code=500, detail="Vector database not initialized")

    try:
        # Retrieve documents
        retrieved_results = retrieve_documents(dbnn, all_documents ,query, top_k)
        if not retrieved_results:
            logger.warning("No relevant documents found.")
            return {"response": "No relevant documents found."}

        # Initialize LLM
        llm = initialize_llm()

        # Generate response
        response = generate_response(llm, PROMPT_TEMPLATE, retrieved_results, query)
        logger.debug(f"AI Response: {response}")
        # response = "Well"
        return {"response": response}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in RAG pipeline: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")