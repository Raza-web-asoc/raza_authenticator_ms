from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

async def update_user(user_data, user, db: AsyncSession):
    try:
        if user_data.names:
            user.names = user_data.names
        if user_data.email:
            user.email = user_data.email
        if user_data.last_names:
            user.last_names = user_data.last_names
        if user_data.gender:
            user.gender = user_data.gender
        if user_data.birthday:
            user.birthday = user_data.birthday

        db.add(user)
        await db.commit()

        return {"message": "User updated", "user": user}
    
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the user: {str(e)}"
        )
