""" Main module for the FastAPI application. """

from fastapi import FastAPI
from app.routes import router as api_router

app = FastAPI(title="RAG-based Q&A API")
app.include_router(api_router)

