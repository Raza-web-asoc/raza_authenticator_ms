import os
from app.schemas.userSchema import User
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"
os.environ["SECRET_KEY"] = "testsecret"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRES_MINUTES"] = "30"
import pytest
from httpx._transports.asgi import ASGITransport
from unittest.mock import AsyncMock, patch
from app.main import app
from app.schemas.userSchema import User
from app.db.database import get_db 
from httpx import AsyncClient



@pytest.mark.asyncio
async def test_login_success(monkeypatch):
    # arrange
    # Creamos un fake user
    fake_user = AsyncMock()
    fake_user.username = "testuser"


    # Mockeamos authenticate_user en el módulo del endpoint
    monkeypatch.setattr(
        "app.controllers.auth.authenticate_user",
        AsyncMock(return_value=fake_user)
    )

    # Mockeamos create_access_token
    monkeypatch.setattr(
        "app.controllers.auth.create_access_token",
        lambda data, expires_delta: "fake-token"
    )

    # Mockeamos la DB aunque no se use realmente
    async def mock_get_db():
        yield AsyncMock()
    app.dependency_overrides[get_db] = mock_get_db

    # Payload para el login
    payload = {"username": "testuser", "password": "password123"}


    # act
    # Usamos AsyncClient para llamar al endpoint
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/signin", data=payload)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"access_token": "fake-token", "token_type": "bearer"}