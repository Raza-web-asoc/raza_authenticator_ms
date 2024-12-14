from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from alembic import context
from app.models.models import Base
import pymysql
pymysql.install_as_MySQLdb()

from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL_SYNC = os.getenv("DB_SYNC")

config = context.config
fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", DATABASE_URL_SYNC)

target_metadata = Base.metadata  # El objeto metadata de tu modelo

def run_migrations_online():
    connectable = create_engine(DATABASE_URL_SYNC) 
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
