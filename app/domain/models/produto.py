
from decimal import Decimal

from sqlalchemy import String, Boolean, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.database import Base


class Produto(Base):

    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    descricao: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    preco_padrao: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
