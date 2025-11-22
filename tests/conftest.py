# tests/conftest.py
import os
import pytest

def pytest_generate_tests(metafunc):
    # Variables de entorno necesarias para tu app
    os.environ['DATABASE_URL'] = "sqlite:///./test.db"
    os.environ['SECRET_KEY'] = "testsecret"
    os.environ['ALGORITHM'] = "HS256"
    os.environ['ACCESS_TOKEN_EXPIRES_MINUTES'] = "30"  # siempre string en env

@pytest.fixture
def settings_env():
    return {
        "DATABASE_URL": os.environ.get("DATABASE_URL"),
        "SECRET_KEY": os.environ.get("SECRET_KEY"),
        "ALGORITHM": os.environ.get("ALGORITHM"),
        "ACCESS_TOKEN_EXPIRES_MINUTES": int(os.environ.get("ACCESS_TOKEN_EXPIRES_MINUTES")),
    }
