""" Configuration file for the app """

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DB_DSN", "postgresql+asyncpg://postgres:password@localhost:5432/ragdb"
)
HF_EMBED_MODEL = os.getenv("HF_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
HF_RAG_MODEL = os.getenv("HF_RAG_MODEL", "google/flan-t5-base")
