from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.base_class import Base
from app.core.settings import settings
from app.db.models import User

engine = create_async_engine(settings.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession, 
    expire_on_commit=False
)

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Tablas creadas exitosamente")
    except Exception as error:
        print(f"Error al conectar a la base de datos: {error}")

async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            pass
