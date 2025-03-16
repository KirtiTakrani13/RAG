from app.utils.settings import LOG_LEVEL, LOG_FILE, OPENAI_API_KEY, HUGGINGFACEHUB_API_TOKEN
from app.utils.logging_config import get_logger  # Import function instead of logger object

# Initialize logger
logger = get_logger()

# ✅ Securely log API keys
def log_api_keys():
    if OPENAI_API_KEY:
        masked_api_key = OPENAI_API_KEY[:4] + "****" + OPENAI_API_KEY[-4:]
        logger.debug(f"🔑 OPENAI_API_KEY Loaded: {masked_api_key}")
    else:
        logger.debug("⚠️ WARNING: OPENAI_API_KEY is missing from environment variables.")

    if HUGGINGFACEHUB_API_TOKEN:
        masked_hf_token = HUGGINGFACEHUB_API_TOKEN[:4] + "****" + HUGGINGFACEHUB_API_TOKEN[-4:]
        logger.debug(f"🔑 HUGGINGFACEHUB_API_TOKEN Loaded: {masked_hf_token}")
    else:
        logger.debug("⚠️ WARNING: HUGGINGFACEHUB_API_TOKEN is missing from environment variables.")

# ✅ Log API keys securely at startup
log_api_keys()
