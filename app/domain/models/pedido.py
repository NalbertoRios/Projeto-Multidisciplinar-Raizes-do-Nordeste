from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    DateTime,
    Numeric,
    Enum,
    CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.database import Base
from app.domain.enums.canal_pedido import CanalPedido
from app.domain.enums.status_pedido import StatusPedido

if TYPE_CHECKING:
    from app.domain.models.item_pedido import ItemPedido


class Pedido(Base):

    __tablename__ = "pedidos"

    __table_args__ = (
        CheckConstraint(
            "valor_total >= 0",
            name="ck_pedido_valor_total_positivo"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False
    )

    atendente_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=True
    )

    unidade_id: Mapped[int] = mapped_column(
        ForeignKey("unidades.id"),
        nullable=False
    )

    canal_pedido: Mapped[CanalPedido] = mapped_column(
        Enum(CanalPedido, name="canal_pedido"),
        nullable=False
    )

    status: Mapped[StatusPedido] = mapped_column(
        Enum(StatusPedido, name="status_pedido"),
        default=StatusPedido.AGUARDANDO_PAGAMENTO,
        nullable=False
    )

    valor_total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    data_criacao: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )

    itens: Mapped[list["ItemPedido"]] = relationship(
        "ItemPedido",
        back_populates="pedido"
    )