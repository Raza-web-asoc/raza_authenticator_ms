from sqlalchemy import Column, Integer, String, Date, Enum, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class User(Base):
    __tablename__ = "user"

    id_user = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, comment="Nombre de usuario único")
    names = Column(String(100), nullable=False, comment="Nombres del usuario")
    last_names = Column(String(100), nullable=False, comment="Apellidos del usuario")
    email = Column(String(100), unique=True, nullable=False, index=True, comment="Correo único")
    password_hash = Column(String(255), nullable=False, comment="Contraseña encriptada")
    birthday = Column(Date, nullable=False, comment="Fecha de nacimiento del usuario")
    gender = Column(Enum("M", "F", "Otro"), nullable=False, comment="Género del usuario")
    role = Column(Integer, nullable=False, default=1, comment="Rol del usuario")
    creation_date = Column(DateTime, nullable=False, default=func.now(), comment="Fecha de creación del usuario")
