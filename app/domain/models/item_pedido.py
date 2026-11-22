from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    Integer,
    Numeric,
    CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.database import Base

if TYPE_CHECKING:
    from app.domain.models.pedido import Pedido


class ItemPedido(Base):

    __tablename__ = "itens_pedido"

    __table_args__ = (
        CheckConstraint(
            "quantidade > 0",
            name="ck_item_pedido_quantidade_positiva"
        ),
        CheckConstraint(
            "preco_unitario >= 0",
            name="ck_item_pedido_preco_positivo"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id"),
        nullable=False
    )

    produto_unidade_id: Mapped[int] = mapped_column(
        ForeignKey("produto_unidade.id"),
        nullable=False
    )

    quantidade: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    preco_unitario: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    pedido: Mapped["Pedido"] = relationship(
        "Pedido",
        back_populates="itens"
    )