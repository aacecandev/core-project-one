import asyncio

import httpx
import pytest
from asgi_lifespan import LifespanManager
from fastapi import status

from app.tests.app import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


#     loop.close()


@pytest.fixture
async def test_client():
    async with LifespanManager(app):
        async with httpx.AsyncClient(
            app=app, base_url="http://localhost:8000"
        ) as test_client:
            yield test_client


@pytest.mark.asyncio
async def test_hello_world(test_client):
    response = await test_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"hello": "world"}
    # json = response.json()
    # assert json == {"hello": "world"}
