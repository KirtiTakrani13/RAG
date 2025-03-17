# utils/document_loader.py
from typing import List, Optional
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.utils.settings import CHUNK_SIZE, CHUNK_OVERLAP
from app.utils.logging_config import get_logger

logger = get_logger() 

def load_pdf(file_path: str) -> List[Document]:
    if not file_path.endswith(".pdf"):
        logger.warning("Unsupported file format!")
        return []
    try:
        loader = PyPDFLoader(file_path)
        return loader.load()
    except Exception as e:
        logger.error(f"Error loading PDF: {e}")
        return []

def load_web(url: str) -> List[Document]:
    try:
        loader = WebBaseLoader(web_paths=[url])
        return loader.load()
    except Exception as e:
        logger.error(f"Error loading web content: {e}")
        return []


def chunk_documents(documents: List[Document]) -> List[Document]:
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        return text_splitter.split_documents(documents)
    except Exception as e:
        logger.error(f"Error chunking documents: {e}")
        return []

def load_and_chunk_documents(file_path: Optional[str] = None, url: Optional[str] = None) -> List[Document]:
    documents = []
    if url:
        if not url.startswith("http"):
            logger.warning("Invalid URL provided.")
            return []
        documents = load_web(url)
    elif file_path:
        documents = load_pdf(file_path)
    else:
        logger.warning("No file path or URL provided.")
        return []
    
    if not documents:
        logger.warning("No documents found. Check file path or URL.")
        return []
    
    return chunk_documents(documents)
