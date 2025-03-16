import os
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")
load_dotenv(dotenv_path)

# Fetch the key
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini-search-preview"
FAISS_INDEX_PATH = "faiss_index"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
LOG_LEVEL = "INFO"
LOG_FILE = "app.log"


# Raise an error if the key is missing
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing. Please check your .env file.")
