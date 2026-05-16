"""
Configuration module for SmartShift.
Handles OpenRouter LLM setup and environment variables.
"""
import os
from crewai import LLM
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenRouter Configuration
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "openrouter/qwen/qwen-2.5-72b-instruct"

# Validate credentials
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY must be set in .env file")

# Initialize LLM with OpenRouter
llm = LLM(
    model=MODEL_NAME,
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
    max_tokens=2000,
    temperature=0.7
)

# ChromaDB Configuration
CHROMA_PERSIST_DIR = "./chroma_store"
CHROMA_COLLECTION_NAME = "warehouse_workers"

# Embedding Model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Made with Bob
