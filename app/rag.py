"""This module contains functions for interacting with the database and Hugging Face models."""

import uuid
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.models import Document, Embedding, UserSelectedDocument
from app.config import HF_EMBED_MODEL, HF_RAG_MODEL

# Load Hugging Face models
embedder = SentenceTransformer(HF_EMBED_MODEL)
tokenizer = AutoTokenizer.from_pretrained(HF_RAG_MODEL)
rag_model = AutoModelForSeq2SeqLM.from_pretrained(HF_RAG_MODEL)
rag_pipeline = pipeline(
    "text2text-generation",
    model=rag_model,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1,
)

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)


async def insert_document_and_embeddings(
    session: AsyncSession, file_content: str, filename: str
):
    """ Insert a document and its embeddings into the database. """ 
    doc_id = uuid.uuid4()
    session.add(Document(id=doc_id, name=filename, content=file_content))

    chunks = splitter.split_text(file_content)
    embeddings = embedder.encode(chunks).tolist()

    for chunk, emb in zip(chunks, embeddings):
        emb_str = [str(x) for x in emb]  # store as str[] for pgvector
        session.add(
            Embedding(
                id=uuid.uuid4(), document_id=doc_id, chunk=chunk, embedding=emb_str
            )
        )
    await session.commit()


async def select_user_documents(
    session: AsyncSession, user_id: str, doc_ids: list[str]
):
    """ Select documents for a user. """
    for doc_id in doc_ids:
        session.add(
            UserSelectedDocument(user_id=user_id, document_id=uuid.UUID(doc_id))
        )
    await session.commit()


async def query_with_rag(session: AsyncSession, question: str, user_id: str):
    """ Query the RAG model with a question and user context. """
    q_embedding = embedder.encode([question])[0]

    query = text(
        """
        SELECT e.chunk, (embedding <-> :embedding) AS distance
        FROM embeddings e
        JOIN user_selected_documents usd ON usd.document_id = e.document_id
        WHERE usd.user_id = :user_id
        ORDER BY distance ASC
        LIMIT 3
    """
    )
    result = await session.execute(
        query, {"embedding": q_embedding.tolist(), "user_id": user_id}
    )
    records = result.fetchall()

    if not records:
        return {"question": question, "answer": "No relevant context found."}

    context = "\n".join([r["chunk"] for r in records])
    prompt = f"Context: {context}\n\nQuestion: {question}"

    answer = rag_pipeline(prompt, max_new_tokens=256, do_sample=False)[0][
        "generated_text"
    ]
    return {"question": question, "answer": answer}
