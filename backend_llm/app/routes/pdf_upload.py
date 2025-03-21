from fastapi import APIRouter, File, UploadFile, HTTPException
import shutil
import os
from app.utils.global_vars import global_state, GlobalState

router = APIRouter()
# Dependency function to access global state
def get_global_state():
    return global_state

# Ensure the upload directory exists
os.makedirs(global_state.UPLOAD_DIR, exist_ok=True)

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """ Uploads a PDF file and ensures only one file exists in the upload folder at a time. """
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Check if there is already a file in the folder
    existing_files = [f for f in os.listdir(global_state.UPLOAD_DIR) if f.endswith(".pdf")]

    if existing_files:
        # If the same file already exists, return it instead of re-uploading
        if file.filename in existing_files:
            return {"filename": file.filename, "status": "File already exists"}

        # Remove existing files to ensure only one file is in the folder
        for existing_file in existing_files:
            existing_file_path = os.path.join(global_state.UPLOAD_DIR, existing_file)
            os.remove(existing_file_path)

    # Save the new file
    file_path = os.path.join(global_state.UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "status": "Uploaded successfully"}