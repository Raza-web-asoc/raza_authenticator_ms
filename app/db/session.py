from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings

# Configura el motor para la base de datos asincrónica
engine = create_async_engine(settings.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession, 
    autoflush=False,
    autocommit=False
)
