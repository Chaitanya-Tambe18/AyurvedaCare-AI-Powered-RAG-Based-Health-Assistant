import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL = "llama-3.1-8b-instant"
    GROQ_TEMPERATURE = 0.1
    GROQ_MAX_TOKENS = 1000
    
    FALLBACK_TO_OLLAMA = True
    OLLAMA_MODEL = "llama3"
    EMBEDDING_MODEL = "nomic-embed-text"
    OLLAMA_BASE_URL = "http://localhost:11434"
    
    CHROMA_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'chroma_db')
    
    PDF_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'health_pdfs')
    
    MAX_RETRIEVED_DOCS = 5
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
