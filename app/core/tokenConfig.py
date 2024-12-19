from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from app.schemas.tokenSchema import TokenData
from app.db.database import get_db
from sqlalchemy.future import select
from app.core.settings import settings
from jose import JWTError, jwt
from datetime import datetime, timedelta

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

async def get_current_user(token: str = Depends(oauth_2_scheme), db: AsyncSession = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed to validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = await get_user_with_username(db, username=token_data.username)
    if user is None:
        raise credential_exception

    return user

async def get_user_with_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()
    return user

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt