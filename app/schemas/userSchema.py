from pydantic import BaseModel
import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    names: str
    last_names: str
    email: str
    gender: str
    birthday: datetime.date

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    names: Optional[str] = None
    last_names: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    birthday: Optional[str] = None
    gender: Optional[str] = None

class UserInDBBase(UserBase):
    id_user: int 

    class Config:
        from_attributes = True  # Para mapear automáticamente a los atributos de SQLAlchemy

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    pass
