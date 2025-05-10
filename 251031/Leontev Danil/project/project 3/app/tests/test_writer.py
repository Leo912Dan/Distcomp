import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_writer():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1.0/writers", json={
            "login": "testuser",
            "password": "testpass",
            "firstname": "Имя",
            "lastname": "Фамилия"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["login"] == "testuser"
