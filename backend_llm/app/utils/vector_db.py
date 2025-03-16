# # utils/vector_db.py
import os
from langchain_community.vectorstores import FAISS
from app.utils.settings import FAISS_INDEX_PATH
from app.utils.logging_config import get_logger

logger = get_logger() 

def create_vector_db(documents, embedding_model, save_path: str = FAISS_INDEX_PATH):
    try:
        db = FAISS.from_documents(documents, embedding_model)
        db.save_local(save_path)
        logger.info(f"FAISS database created and saved at {save_path}.")
        return db
    except Exception as e:
        logger.error(f"Error creating vector database: {e}")
        return None

def load_vector_db(embedding_model, load_path: str = FAISS_INDEX_PATH):
    try:
        if not os.path.exists(load_path):
            logger.warning(f"FAISS index not found at {load_path}.")
            return None
        db = FAISS.load_local(load_path, embedding_model, allow_dangerous_deserialization=True)
        logger.info(f"FAISS database loaded from {load_path}.")
        return db
    except Exception as e:
        logger.error(f"Error loading vector database: {e}")
        return None



