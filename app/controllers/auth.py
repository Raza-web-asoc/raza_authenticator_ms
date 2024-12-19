from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

from app.schemas.userSchema import User, UserCreate
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.tokenConfig import get_current_user
from app.core.signinConfig import authenticate_user
from app.core.tokenConfig import create_access_token
from app.core.signupConfig import register_user
from app.core.settings import settings

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

router = APIRouter()

@router.get("/token", response_model=User)
async def verify_token(response: Response, current_user: User = Depends(get_current_user)):
    response.headers["X-Auth-User-Id"] = str(current_user.id_user)
    response.headers["X-Auth-Role"] = str(current_user.role)
    return current_user

@router.get("/signin")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user  = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password", headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup")
async def singup(form_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await register_user(form_data,db)
    return result