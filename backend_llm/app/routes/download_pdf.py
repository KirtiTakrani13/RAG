from fastapi import APIRouter, HTTPException, Form
import shutil
import os
import requests
import re
from app.utils.global_vars import global_state, GlobalState

router = APIRouter()
# Dependency function to access global state
def get_global_state():
    return global_state

# Ensure the upload directory exists
os.makedirs(global_state.UPLOAD_DIR, exist_ok=True)

def sanitize_filename(filename):
    # Remove spaces and disallowed characters
    sanitized_filename = filename.replace(" ", "")  # Remove spaces
    sanitized_filename = re.sub(r'[^a-zA-Z0-9_.-]', '', sanitized_filename)  # Keep only safe characters

    # Ensure it starts with a lowercase letter
    if not sanitized_filename[0].islower():
        sanitized_filename = "a" + sanitized_filename  # Prepend 'a' if it doesn't start with lowercase
    
    # Ensure only one dot between name and extension
    # Split the filename into the name and extension (if any)
    parts = sanitized_filename.split('.')
    if len(parts) > 1:
        # Join all parts except the last one as the name, and the last part as the extension
        name_part = ''.join(parts[:-1])  # Combine all parts except the last one
        extension_part = parts[-1]  # Last part is the extension
        sanitized_filename = f"{name_part}.{extension_part}"  # Keep only one dot
    else:
        # If there's no extension, just use the name
        sanitized_filename = parts[0]

    return sanitized_filename

@router.post("/upload-pdf-from-url/")
async def upload_pdf_from_url(file_url: str = Form(...)):
    """ Downloads a PDF from a URL and ensures only one file exists in the upload folder at a time. """
    
    try:
        response = requests.get(file_url, stream=True)
        content_type = response.headers.get('Content-Type', '')

        # Validate if the file is a PDF
        if 'pdf' not in content_type.lower():
            raise HTTPException(status_code=400, detail="URL does not point to a valid PDF file")

        # Extract filename from URL
        filename = file_url.split("/")[-1]
        if not filename.endswith(".pdf"):
            filename += ".pdf"  # Ensure it has a .pdf extension
        
        # Sanitize the filename
        filename = sanitize_filename(filename)

        file_path = os.path.join(global_state.UPLOAD_DIR, filename)

        # Check for existing PDFs and delete them
        existing_files = [f for f in os.listdir(global_state.UPLOAD_DIR) if f.endswith(".pdf")]
        for existing_file in existing_files:
            os.remove(os.path.join(global_state.UPLOAD_DIR, existing_file))

        # Download and save the file
        with open(file_path, "wb") as pdf_file:
            shutil.copyfileobj(response.raw, pdf_file)

        return {"filename": filename, "status": "Downloaded and saved successfully"}

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to download file: {str(e)}")
