from fastapi import APIRouter
import os
from threading import Lock

# from langchain_openai import OpenAIEmbeddings
from app.utils.document_loader import load_and_chunk_documents
from app.utils.settings  import FAISS_INDEX_PATH 
from app.utils.global_vars import dbnn, db_lock, all_documents, processed_files, embedding_model, UPLOAD_DIR
from app.utils.vector_db import create_vector_db

router = APIRouter()


@router.post("/process/")
async def process_documents():
    """
    Process all PDFs in the uploads folder and update FAISS.
    """

    global dbnn, all_documents 

    # Get all PDF files in the upload directory
    pdf_files = [os.path.join(UPLOAD_DIR, f) for f in os.listdir(UPLOAD_DIR) if f.endswith(".pdf")]
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

    # Update the FAISS index with new documents
    with db_lock:
        if dbnn:
            dbnn.add_documents(new_extracted_docs)  # Append only new documents
            # dbnn = create_vector_db(new_extracted_docs, embedding_model, FAISS_INDEX_PATH)
        else:
            dbnn = create_vector_db(new_extracted_docs, embedding_model, FAISS_INDEX_PATH)  # Create new index if none exists
        
        # Update the global list of all documents
        all_documents.extend(new_extracted_docs)

    return {"message": f"Processed {len(new_files)} PDFs and updated FAISS index"}