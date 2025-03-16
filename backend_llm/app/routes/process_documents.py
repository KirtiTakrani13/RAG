from fastapi import APIRouter
import os
from threading import Lock
from app.utils.document_loader import load_and_chunk_documents
router = APIRouter()

UPLOAD_DIR = "uploads"

# **Initialize global objects**
# embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)
# db = load_vector_db(embedding_model, FAISS_INDEX_PATH)
# db_lock = Lock()
all_documents = [] 

processed_files = set()

@router.post("/process/")
async def process_documents():
    """
    Process all PDFs in the uploads folder and update FAISS.
    """
    # global db
    global all_documents
    pdf_files = [os.path.join(UPLOAD_DIR, f) for f in os.listdir(UPLOAD_DIR) if f.endswith(".pdf")]
    new_files = [file for file in pdf_files if file not in processed_files]

    if not new_files:
        return {"message": "No new PDFs found"}

    new_extracted_docs = []
    for file_path in new_files:
        documents = load_and_chunk_documents(file_path=file_path)
        if documents:
            new_extracted_docs.extend(documents)
            processed_files.add(file_path)

    if not new_extracted_docs:
        return {"error": "No valid documents extracted"}

    # with db_lock:
    #     if db:
    #         db.add_documents(all_documents)
    #     else:
    #         db = create_vector_db(all_documents, embedding_model, FAISS_INDEX_PATH)

    return {"message": f"Processed {len(new_files)} PDFs and updated FAISS index"}

