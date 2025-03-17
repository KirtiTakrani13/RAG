# app/utils/global_vars.py
from threading import Lock
from app.utils.settings import EMBEDDING_MODEL, FAISS_INDEX_PATH
from app.utils.vector_db import create_vector_db, load_vector_db
from langchain_openai.embeddings import OpenAIEmbeddings
from app.utils.logging_config import get_logger

# Define global variables
UPLOAD_DIR = "uploads"

embedding_model = None

# Initialize variables as None (to be set at startup)
dbnn = None
db_lock = Lock()
all_documents = []  # Track all processed documents
processed_files = set()  # Track processed files

def initialize_globals():
    logger = get_logger()
    # """ Initialize vector database and other global variables """
    # global dbnn
    # try:
    #     dbnn = load_vector_db(embedding_model, FAISS_INDEX_PATH)
    #     if dbnn is None:
    #         logger.info("No existing FAISS index found. Creating a new one.")
    #         dbnn = create_vector_db([], embedding_model, FAISS_INDEX_PATH)  # Create an empty index
    #     logger.info("🔄 Vector DB initialized.")
    # except Exception as e:
    #     logger.error(f"Failed to initialize Vector DB: {e}")
    #     raise RuntimeError(f"Failed to initialize Vector DB: {e}")

