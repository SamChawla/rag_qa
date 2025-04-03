""" This module contains the FastAPI routes for the application. """

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.schema import QueryRequest, SelectDocumentsRequest
from app.rag import (
    insert_document_and_embeddings,
    select_user_documents,
    query_with_rag,
)

router = APIRouter()


@router.post("/ingest")
async def ingest(
    file: UploadFile = File(...), session: AsyncSession = Depends(get_session)
):
    """ Ingest a document into the system."""
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files supported")

    content = await file.read()
    await insert_document_and_embeddings(session, content.decode(), file.filename)
    return {"status": "success", "filename": file.filename}


@router.post("/select_documents")
async def select_documents(
    data: SelectDocumentsRequest, session: AsyncSession = Depends(get_session)
):
    """ Select documents for a user."""
    await select_user_documents(session, data.user_id, data.document_ids)
    return {"status": "documents selected"}


@router.post("/query")
async def query(data: QueryRequest, session: AsyncSession = Depends(get_session)):
    """ Query the system."""
    return await query_with_rag(session, data.question, data.user_id)
