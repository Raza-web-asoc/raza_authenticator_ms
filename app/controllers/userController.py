from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.userSchema import UserUpdate, User
from app.core.tokenConfig import get_current_user
from app.core.userConfig import update_user

router = APIRouter()

@router.put("/update")
async def update_user_info(user_data: UserUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await update_user(user_data,current_user,db)
    return result