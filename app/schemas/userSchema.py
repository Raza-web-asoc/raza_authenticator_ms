from pydantic import BaseModel
import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    names: Optional[str] = None
    last_names: Optional[str] = None
    email: str
    gender: Optional[str] = None
    birthday: Optional[datetime.date] = None

class UserCreate(UserBase):
    password: str
    role: Optional[int] = 1  # Por defecto 1 (User)

class UserUpdate(BaseModel):
    names: Optional[str] = None
    last_names: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    birthday: Optional[str] = None
    gender: Optional[str] = None

class UserInDBBase(UserBase):
    id_user: int
    role: int = 1

    class Config:
        from_attributes = True  # Para mapear automáticamente a los atributos de SQLAlchemy

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    pass
