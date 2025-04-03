# RAG-based Q&A System

This backend application enables document ingestion and intelligent question-answering using a Retrieval-Augmented Generation (RAG) pipeline with Hugging Face models.

---

## Features

- Upload `.txt` documents
- Chunk and embed with `sentence-transformers`
- Store vectors using PostgreSQL + pgvector
- Retrieve top-k chunks and generate answers via Hugging Face `transformers`
- Asynchronous FastAPI endpoints

## Setup

### 1. Clone & Configure

```bash
git clone https://github.com/SamChawla/rag_qa.git
cd rag_qa
cp .env.example .env
```

### 2. Run Locally (Dockerized)

```bash
docker-compose up --build
```

### 3. Initialize the Database

```bash
docker-compose exec app python init_db.py
```

---

## 📡 API Endpoints

| Method | Route               | Purpose                         |
|--------|---------------------|---------------------------------|
| POST   | `/ingest`           | Upload and index documents      |
| POST   | `/select_documents` | Choose documents for retrieval  |
| POST   | `/query`            | Ask questions via RAG           |
