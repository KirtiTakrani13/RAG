from fastapi import FastAPI
from app.routes import pdf_upload, process_documents, query, download_pdf, process_html
from contextlib import asynccontextmanager
from app.utils.global_vars import global_state, GlobalState
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Lifespan function to initialize global variables at startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources at startup and clean up at shutdown"""
    try:
        global_state._initialize_vector_db()  # Ensure vector DB is properly initialized
        print("✅ Global state initialized successfully.")
    except Exception as e:
        print(f"❌ Error initializing global state: {e}")
    yield  # Application runs here
    print("Shutting down application...")

# Initialize FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Include routers
app.include_router(pdf_upload.router, prefix="/api", tags=["File Upload"])
app.include_router(process_documents.router, prefix="/api", tags=["Document Processing"])
app.include_router(query.router, prefix="/api", tags=["Query"])
app.include_router(process_html.router, prefix="/api", tags=["HTML Processing"])
app.include_router(download_pdf.router, prefix="/api", tags=["Download PDF"]) 

@app.get("/")
def read_root():
    return {"message": "Welcome to PDF chat Upload and Processing!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
