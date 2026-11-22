
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.database import Base


class Unidade(Base):

    __tablename__ = "unidades"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    cidade: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    regiao: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    ativa: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
