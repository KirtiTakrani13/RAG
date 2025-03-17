from threading import Lock
from app.utils.settings import EMBEDDING_MODEL, FAISS_INDEX_PATH
from app.utils.vector_db import create_vector_db, load_vector_db
from langchain_openai.embeddings import OpenAIEmbeddings
from app.utils.logging_config import get_logger
import os

class GlobalState:
    """Singleton class to manage global state in FastAPI."""
    
    def __init__(self):
        self.logger = get_logger()
        self.UPLOAD_DIR = "uploads"  # Define UPLOAD_DIR inside the class
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)  # Ensure directory exists
        self.embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        self.dbnn = None  # Placeholder for vector DB instance
        self.db_lock = Lock()
        self.all_documents = []  # Track all processed documents
        self.processed_files = set()  # Track processed files
        self._initialize_vector_db()

    def _initialize_vector_db(self):
        """Initialize the vector database."""
        try:
            self.dbnn = load_vector_db(self.embedding_model, FAISS_INDEX_PATH)
            if self.dbnn is None:
                self.logger.info("No existing FAISS index found. Creating a new one.")
                self.dbnn = create_vector_db([], self.embedding_model, FAISS_INDEX_PATH)
            self.logger.info("🔄 Vector DB initialized.")
        except Exception as e:
            self.logger.error(f"Failed to initialize Vector DB: {e}")
            raise RuntimeError(f"Failed to initialize Vector DB: {e}")

    def get_vector_db(self):
        """Return the vector DB instance."""
        return self.dbnn

    def update_vector_db(self, new_db):
        """Update the vector DB instance safely."""
        with self.db_lock:
            self.dbnn = new_db

# Create a single instance of GlobalState
global_state = GlobalState()
