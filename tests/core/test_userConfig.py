import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from app.core.userConfig import update_user

# Mock de usuario
class UserStub:
    def __init__(self, names=None, last_names=None, email=None, gender=None, birthday=None):
        self.names = names
        self.last_names = last_names
        self.email = email
        self.gender = gender
        self.birthday = birthday

class UserUpdateStub:
    def __init__(self):
        self.names = "New"
        self.last_names = "Tester"
        self.email = "new@test.com"
        self.gender = "male"
        self.birthday = "2005-05-15"

# Fixture para sesión de db mock
@pytest.fixture
def mock_db():
    db = MagicMock()  
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.rollback = AsyncMock()
    return db

@pytest.mark.asyncio
async def test_update_user_success(mock_db):
    # Arrange
    user = UserStub(names="Old", last_names="User", email="old@test.com", gender="other", birthday="2000-01-01")
    user_data = UserUpdateStub()

    # Act
    result = await update_user(user_data, user, mock_db)

    # Assert
    assert result["message"] == "User updated"
    assert result["user"].names == "New"
    assert result["user"].last_names == "Tester"
    assert result["user"].email == "new@test.com"
    assert result["user"].gender == "male"
    assert result["user"].birthday == "2005-05-15"
    mock_db.add.assert_called_once_with(user)
    mock_db.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_user_commit_exception(mock_db):
    # Arrange
    user = UserStub(names="Old")
    
    class UserData:
        names = "New" 
        last_names = None
        email = None
        gender = None
        birthday = None
    
    mock_db.commit.side_effect = Exception("DB error")
    
    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await update_user(UserData, user, mock_db)
    
    assert exc_info.value.status_code == 500
    assert "DB error" in exc_info.value.detail
    mock_db.rollback.assert_awaited_once()


