# config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini-search-preview"
FAISS_INDEX_PATH = "faiss_index"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")


# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "app.log"