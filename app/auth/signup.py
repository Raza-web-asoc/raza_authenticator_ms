from app.database import get_db
from app.models.models import UserInDB, UserCreate
from app.settings import settings
from datetime import date
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def register_user(data:UserCreate, db: AsyncSession):
    try:
        hashed_password = get_password_hash(data.password)

        user = UserInDB(
            username = data.username,
            names = data.names,
            last_names = data.last_names,
            email = data.email,
            password_hash = hashed_password,
            birthday = data.birthday,
            gender = data.gender
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return JSONResponse(
            content={"message": "User created"},
            status_code=201
        )

    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email or user already registered"
        )

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )