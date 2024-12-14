from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
import asyncio
from app.settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session

# Función para inicializar la base de datos y crear tablas
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def test_connection():
    try:
        async with async_session() as session:
            result = await session.execute(text("SELECT VERSION()"))
            version = result.scalar()
            print(f"conexion success: MYSQL version {version}")
    except Exception as e:
        print(f"Error to conect to DB: {e}")

    finally:
        await engine.dispose()