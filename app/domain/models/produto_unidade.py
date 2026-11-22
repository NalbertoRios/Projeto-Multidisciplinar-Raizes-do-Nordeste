
from datetime import date
from decimal import Decimal

from sqlalchemy import (
    ForeignKey,
    String,
    Boolean,
    Numeric,
    Date,
    UniqueConstraint
)

from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.database import Base


class ProdutoUnidade(Base):

    __tablename__ = "produto_unidade"

    __table_args__ = (
        UniqueConstraint(
            "unidade_id",
            "produto_id",
            name="uq_unidade_produto"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    unidade_id: Mapped[int] = mapped_column(
        ForeignKey("unidades.id"),
        nullable=False
    )

    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.id"),
        nullable=False
    )

    preco_especifico: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True
    )

    habilitado: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    data_inicio_disponibilidade: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    data_fim_disponibilidade: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    observacao_variacao: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
