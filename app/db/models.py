from sqlalchemy import Column, Integer, String, Date, Enum, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class User(Base):
    __tablename__ = "user"

    id_user = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, comment="Nombre de usuario único")
    names = Column(String(100), nullable=True, comment="Nombres del usuario")  # <-- allow null for OAuth
    last_names = Column(String(100), nullable=True, comment="Apellidos del usuario")  # <-- allow null
    email = Column(String(100), unique=True, nullable=False, index=True, comment="Correo único")
    password_hash = Column(String(255), nullable=True, comment="Contraseña encriptada")  # <-- nullable for OAuth
    birthday = Column(Date, nullable=True, comment="Fecha de nacimiento del usuario")  # <-- nullable
    gender = Column(Enum("M", "F", "Otro"), nullable=True, comment="Género del usuario")  # <-- nullable
    role = Column(Integer, nullable=False, default=1, comment="Rol del usuario")
    creation_date = Column(DateTime, nullable=False, default=func.now(), comment="Fecha de creación del usuario")
    google_id = Column(String(255), unique=True, nullable=True, comment="Google Oauth ID")  # <-- new
