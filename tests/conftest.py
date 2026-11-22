import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient

from app.infrastructure.database.database import Base
from app.api.dependencies import get_db
from app.domain.models import *
from app.main import app


# Banco SQLite exclusivo para os testes
TEST_DATABASE_URL = "sqlite://"

engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

SessionTest = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test
)


@pytest.fixture
def db():
    # Cria todas as tabelas
    Base.metadata.create_all(bind=engine_test)

    session = SessionTest()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def client(db):
    # Substitui o banco oficial pelo banco de testes
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Restaura as dependências originais
    app.dependency_overrides.clear()