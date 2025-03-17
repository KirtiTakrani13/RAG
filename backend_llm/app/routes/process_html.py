from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.utils.document_loader import load_and_chunk_documents
from app.utils.settings import FAISS_INDEX_PATH
from app.utils.global_vars import global_state, GlobalState
from app.utils.vector_db import create_vector_db
from app.utils.logging_config import get_logger

logger = get_logger()
router = APIRouter()

# Dependency function to inject the global state
def get_global_state():
    return global_state

# Pydantic model to parse the input URL
class URLInput(BaseModel):
    url: str

@router.post("/process-html/")
async def process_html(input: URLInput, state: GlobalState = Depends(get_global_state)):
    """
    Process an HTML website given its URL and update the FAISS vector database.
    """
    url = input.url.strip()
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Invalid URL provided. It must start with http:// or https://")

    logger.info("Received request to process HTML website: %s", url)

    # Load and chunk documents from the provided URL
    documents = load_and_chunk_documents(url=url)
    if not documents:
        raise HTTPException(status_code=400, detail="Unable to load or process HTML content from the provided URL.")

    embedding_model = state.embedding_model
    dbnn = state.get_vector_db()

    # Update vector DB with new documents
    if dbnn:
        dbnn.add_documents(documents)
        state.update_vector_db(dbnn)
    else:
        new_db = create_vector_db(documents, embedding_model, FAISS_INDEX_PATH)
        if not new_db:
            raise HTTPException(status_code=500, detail="Failed to create a new vector database.")
        state.update_vector_db(new_db)

    # Optionally track the processed URL here (similar to processed_files for PDFs)
    state.all_documents.extend(documents)
    return {"message": f"Processed HTML website {url} and updated FAISS index."}
