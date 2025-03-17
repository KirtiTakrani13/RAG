from fastapi import APIRouter, Depends
import os
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

@router.post("/process/")
async def process_documents(state: GlobalState = Depends(get_global_state)):
    """
    Process all PDFs in the uploads folder and update FAISS.
    """
    logger.info("Received request to process documents")

    # Access shared global variables
    dbnn = state.get_vector_db()
    embedding_model = state.embedding_model
    all_documents = state.all_documents
    processed_files = state.processed_files
    upload_dir = "uploads"

    # Get all PDF files in the upload directory
    pdf_files = [os.path.join(upload_dir, f) for f in os.listdir(upload_dir) if f.endswith(".pdf")]
    new_files = [file for file in pdf_files if file not in processed_files]

    if not new_files:
        return {"message": "No new PDFs found"}

    # Extract and chunk documents from new files
    new_extracted_docs = []
    for file_path in new_files:
        documents = load_and_chunk_documents(file_path=file_path)
        if documents:
            new_extracted_docs.extend(documents)
            processed_files.add(file_path)

    if not new_extracted_docs:
        return {"error": "No valid documents extracted"}

    # Update FAISS index
    new_db = create_vector_db(new_extracted_docs, embedding_model, FAISS_INDEX_PATH)
    state.update_vector_db(new_db)  # Ensures the global instance is updated

    all_documents.extend(new_extracted_docs)
    return {"message": f"Processed {len(new_files)} PDFs and updated FAISS index"}
