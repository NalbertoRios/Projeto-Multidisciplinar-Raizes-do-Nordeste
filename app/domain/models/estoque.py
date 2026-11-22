from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Integer,
    DateTime,
    CheckConstraint
)

from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.database import Base


class Estoque(Base):

    __tablename__ = "estoques"

    __table_args__ = (
        CheckConstraint(
            "quantidade_disponivel >= 0",
            name="ck_estoque_quantidade_positiva"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    produto_unidade_id: Mapped[int] = mapped_column(
        ForeignKey("produto_unidade.id"),
        unique=True,
        nullable=False
    )

    quantidade_disponivel: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False
    )