from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRES_MINUTES: int

    google_client_id: str | None = None
    google_client_secret: str | None = None
    front_url: str | None = None
    auth_base_url: str | None = None

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"  # evita errores por variables adicionales
    }

settings = Settings()
