import os
# =================== Configuración de entorno ===================
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"
os.environ["SECRET_KEY"] = "testsecret"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRES_MINUTES"] = "30"
import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

from app.main import app
from app.schemas.userSchema import User
from app.controllers import userController
from app.core.tokenConfig import get_current_user
from app.core.userConfig import update_user
from tests.utils.dbMock import mock_get_db
from app.db.database import get_db



# =================== Mocks ===================
async def mock_get_current_user():
    return User(
        id_user=1,
        id=1,  # si tu modelo tiene ambos
        username="testuser",
        email="test@test.com",
        names="Test",
        last_names="User",
        gender="other",
        birthday="2000-01-01"
    )


async def mock_update_user(user_data, current_user, db):
    return {
        "message": "User updated",
        "user": {
            "id_user": 1,
            "username": "newname",
            "names": "Test",
            "last_names": "User",
            "email": "newemail@test.com",
            "gender": "other",
            "birthday": "2000-01-01"
        }
    }




# =================== Test ===================
@pytest.mark.asyncio
async def test_update_user_info_should_return_updated_user():

    # ----------------- Arrange -----------------
    app.dependency_overrides[get_current_user] = mock_get_current_user
    app.dependency_overrides[get_db] = mock_get_db

    # Sobreescribir la función update_user del controlador
    userController.update_user = mock_update_user

    payload = {
        "id_user": 1,
        "username": "newname",
        "names": "Test",
        "last_names": "User",
        "email": "newemail@test.com",
        "gender": "other",
        "birthday": "2000-01-01"
    }


    # ----------------- Act -----------------
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.put("/user/update", json=payload)

    # ----------------- Assert -----------------
    assert response.status_code == 200
    assert response.json() == {
        "message": "User updated",
        "user": {
            "id_user": 1,
            "username": "newname",
            "names": "Test",
            "last_names": "User",
            "email": "newemail@test.com",
            "gender": "other",
            "birthday": "2000-01-01"
    }
}


    # ----------------- Cleanup -----------------
    app.dependency_overrides.clear()
