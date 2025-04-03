import pytest


@pytest.mark.asyncio
async def test_ingest_txt_success(client, sample_document):
    """ Test successful ingestion of a text file. """
    files = {'file': ('test.txt', sample_document)}
    response = await client.post("/ingest", files=files)
    assert response.status_code == 200
    assert "message" in response.json()

@pytest.mark.asyncio
async def test_ingest_txt_invalid_file(client):
    """ Test ingestion of an invalid file type. """
    files = {'file': ('test.txt', b'Invalid content')}  
    response = await client.post("/ingest", files=files)
    assert response.status_code == 400 or response.status_code == 422


@pytest.mark.asyncio
async def test_select_documents_success(client):
    """ Test successful selection of documents. """
    payload = {
        "user_id": 1,
        "document_ids": [1]  # assuming the document was inserted
    }
    response = await client.post("/select_documents", json=payload)
    assert response.status_code == 200
    assert "message" in response.json()

@pytest.mark.asyncio
async def test_select_documents_invalid_payload(client):
    """ Test selection of documents with invalid payload. """
    payload = {
        "user_id": None,
        "document_ids": []
    }
    response = await client.post("/select_documents", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_query_success(client):
    """ Test successful query. """
    payload = {
        "user_id": 1,
        "question": "What is this document about?"
    }
    response = await client.post("/query", json=payload)
    assert response.status_code == 200
    assert "answer" in response.json()

@pytest.mark.asyncio
async def test_query_missing_docs(client):
    """ Test query with no documents selected. """
    payload = {
        "user_id": 999,  # no documents selected
        "question": "Will this work?"
    }
    response = await client.post("/query", json=payload)
    assert response.status_code == 404
