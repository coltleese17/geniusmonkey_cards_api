# tests/conftest.py
import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient
from cardapi.main import app, service  


# ------------------------------------------------------------------
#  Async-io event-loop fixture 
# ------------------------------------------------------------------
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ------------------------------------------------------------------
#  Auto-reset the in-memory deck before + after every test
# ------------------------------------------------------------------
@pytest.fixture(autouse=True)
def fresh_service():
    service.reset()
    yield
    service.reset()


# ------------------------------------------------------------------
#  Re-usable HTTP client fixture for endpoint tests
# ------------------------------------------------------------------
@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

