from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings


# Conexão com o banco de dados
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# Gerenciador de sessões
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Classe-base dos modelos
class Base(DeclarativeBase):
    pass