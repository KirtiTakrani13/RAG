from fastapi import FastAPI
from app.routes import pdf_upload, process_documents,query
from app.utils.document_loader import load_and_chunk_documents
from app.utils.settings  import EMBEDDING_MODEL, FAISS_INDEX_PATH, OPENAI_API_KEY
from app.utils.vector_db import create_vector_db, load_vector_db
from langchain_openai.embeddings import OpenAIEmbeddings 
from threading import Lock
from contextlib import asynccontextmanager
from app.utils.global_vars import initialize_globals



# Lifespan function to initialize global variables at startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources at startup and clean up at shutdown"""
    print("Initializing Vector Database...")
    initialize_globals()
    yield  # Application runs here
    print("Shutting down application...")  


# Initialize FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)


# Include PDF Upload and Document Processing routers
app.include_router(pdf_upload.router, prefix="/api", tags=["File Upload"])
app.include_router(process_documents.router, prefix="/api", tags=["Document Processing"])
app.include_router(query.router, prefix="/api", tags=["Query"])


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI PDF Upload and Processing!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
