"""
API tests using pytest and httpx.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.database import Base, engine
from app.main import app


@pytest.fixture(autouse=True)
async def setup_database():
    """Create tables before each test and clean up after."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    """Async test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    """Test root endpoint returns API info."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "docs" in data


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    """Test health endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_create_and_get_item(client: AsyncClient):
    """Test creating and retrieving an item."""
    # Create
    create_response = await client.post(
        "/api/items",
        json={"name": "Test Item", "description": "A test item"},
    )
    assert create_response.status_code == 201
    item = create_response.json()
    assert item["name"] == "Test Item"
    item_id = item["id"]

    # Get
    get_response = await client.get(f"/api/items/{item_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Test Item"


@pytest.mark.asyncio
async def test_list_items(client: AsyncClient):
    """Test listing items."""
    response = await client.get("/api/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
