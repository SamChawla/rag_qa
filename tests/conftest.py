import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.db import async_session, engine
from app.models import Base

@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Create and drop tables before and after the test session."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client():
    """Provides an HTTP client for API tests."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def sample_document():
    """Returns dummy text for ingestion."""
    return "This is a test document for QA purposes."
