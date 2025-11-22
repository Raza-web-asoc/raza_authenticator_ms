import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.core.signinConfig import get_user_with_email
from app.db.models import User
from app.core.signinConfig import authenticate_user
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture
def fake_user():
    user = User()
    user.email = "test@test.com"
    user.password_hash = pwd_context.hash("password123")
    return user

@pytest.mark.asyncio
async def test_authenticate_user_success(fake_user):
    mock_db = AsyncMock()

    # Mockeamos get_user_with_email para devolver nuestro fake_user
    with patch("app.core.signinConfig.get_user_with_email", return_value=fake_user):
        user = await authenticate_user(mock_db, "test@test.com", "password123")
        assert user.email == "test@test.com"

@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(fake_user):
    mock_db = AsyncMock()
    with patch("app.core.signinConfig.get_user_with_email", return_value=fake_user):
        user = await authenticate_user(mock_db, "test@test.com", "wrongpassword")
        assert user is False

@pytest.mark.asyncio
async def test_authenticate_user_failed(fake_user):
    mock_db = AsyncMock()

    # Mockeamos get_user_with_email para devolver nuestro fake_user
    with patch("app.core.signinConfig.get_user_with_email", return_value=fake_user):
        user = await authenticate_user(mock_db, "test@test.com", "password123")
        assert user.email == "test@test.com"


@pytest.mark.asyncio
async def test_get_user_with_email_returns_user():
    # arrange
    # usuario fake
    fake_user = User()
    fake_user.email = "test@test.com"

    mock_scalars = Mock()
    mock_scalars.first.return_value = fake_user

  
    mock_result = Mock()
    mock_result.scalars.return_value = mock_scalars


    mock_db = AsyncMock()
    mock_db.execute.return_value = mock_result  

    # act
    user = await get_user_with_email(mock_db, "test@test.com")

    # assert
    assert user.email == "test@test.com"
