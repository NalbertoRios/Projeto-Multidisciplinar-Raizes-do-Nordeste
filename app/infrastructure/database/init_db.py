
# Importa os modelos para registrá-los no SQLAlchemy
from app.domain import models

# Importa a classe Base e a conexão
from app.infrastructure.database.database import Base, engine


def inicializar_banco():
    Base.metadata.create_all(bind=engine)
    print("Banco de dados inicializado com sucesso!")


if __name__ == "__main__":
    inicializar_banco()
