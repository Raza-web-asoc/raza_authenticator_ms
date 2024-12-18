from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.auth.auth import authenticate_user, create_access_token, get_current_user
from app.auth.signup import register_user
from app.models.models import Token, User, UserCreate
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware

#Importaciones para DB
from app.database import get_db, init_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.settings import settings

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"]
)

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.post("/signin")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user  = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password", headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/signup")
async def singup(form_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await register_user(form_data,db)
    return result

@app.get("/token", response_model=User)
async def verify_token(response: Response, current_user: User = Depends(get_current_user)):
    response.headers["X-Auth-User-Id"] = str(current_user.id_user)
    response.headers["X-Auth-Role"] = str(current_user.role)
    return current_user
