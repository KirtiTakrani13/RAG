from fastapi import FastAPI
from app.routes import pdf_upload, process_documents

app = FastAPI()

# Include PDF Upload and Document Processing routers
app.include_router(pdf_upload.router, prefix="/api", tags=["File Upload"])
app.include_router(process_documents.router, prefix="/api", tags=["Document Processing"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI PDF Upload and Processing!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
