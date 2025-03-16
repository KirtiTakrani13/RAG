from fastapi import APIRouter, File, UploadFile, HTTPException
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploads"  # Folder to store uploaded PDFs
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Create folder if not exists

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """ Uploads a PDF file and saves it to the server. """
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "status": "Uploaded successfully"}
