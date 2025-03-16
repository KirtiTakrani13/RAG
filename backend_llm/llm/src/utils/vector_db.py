# # utils/vector_db.py
import os
from langchain_community.vectorstores import FAISS
from config import FAISS_INDEX_PATH
from utils.logging_config import logger


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



# -------------

# utils/vector_db.py Going to use this as embeding. 
# import os
# from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
# from langchain_community.vectorstores import FAISS
# from config import FAISS_INDEX_PATH
# from utils.logging_config import logger
# from transformers import AutoTokenizer, AutoModel
# import torch


# def create_vector_db(documents, embedding_model, save_path: str = FAISS_INDEX_PATH):
#     try:
#         db = FAISS.from_documents(documents, embedding_model)
#         db.save_local(save_path)
#         logger.info(f"FAISS database created and saved at {save_path}.")
#         return db
#     except Exception as e:
#         logger.error(f"Error creating vector database: {e}")
#         return None

# def load_vector_db(embedding_model, load_path: str = FAISS_INDEX_PATH):
#     try:
#         if not os.path.exists(load_path):
#             logger.warning(f"FAISS index not found at {load_path}.")
#             return None
#         db = FAISS.load_local(load_path, embedding_model, allow_dangerous_deserialization=True)
#         logger.info(f"FAISS database loaded from {load_path}.")
#         return db
#     except Exception as e:
#         logger.error(f"Error loading vector database: {e}")
#         return None
    

# # # Initialize local embedding model
# # def get_local_embedding_model():
# #     return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# # Initialize local embedding model
# def get_local_embedding_model():
#     return HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1")