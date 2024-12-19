from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from app.db.database import get_db
from app.db.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def authenticate_user(db, email: str, password: str):
    user = await get_user_with_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

async def get_user_with_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)